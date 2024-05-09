from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import *
from .serializer import *
from django.shortcuts import get_object_or_404
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.pagination import PageNumberPagination
from .filters import *
from django.contrib.auth import authenticate, login, logout
from rest_framework.authentication import TokenAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.decorators import authentication_classes, permission_classes
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import random

#-----------------------------------------------------------------------------------------------------
# Inicio de Sesión
#-----------------------------------------------------------------------------------------------------

class WelcomeAPIView(APIView):
    def get(self, request):
        welcome_message = "¡Bienvenido! Por favor, disfruta de nuestra aplicación."

        return Response(welcome_message)

class UserLoginAPIView(APIView):
    authentication_classes = []

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        username = username.lower()
        User = get_user_model()
        user = User.objects.filter(username=username).first()
        if user is not None and user.check_password(password):
            if user.is_active:
                login(request, user)
                token, created = Token.objects.get_or_create(user=user)
                return Response({'message': 'Inicio de sesión exitoso', 'token': token.key, 'usuario': user.id}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Este usuario está inactivo'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({"detail": "Nombre de usuario o contraseña inválidos."}, status=status.HTTP_400_BAD_REQUEST)
#-----------------------------------------------------------------------------------------------------
# Cerrar Sesión
#-----------------------------------------------------------------------------------------------------

class UserLogoutAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        Token.objects.filter(user=request.user).delete()
        logout(request)
        return Response({'message': 'Sesión cerrada exitosamente'}, status=status.HTTP_200_OK)
  
#-----------------------------------------------------------------------------------------------------
# Registrarse
#-----------------------------------------------------------------------------------------------------

class UserRegisterAPIView(APIView):
    def post(self, request):
        try:
            serializer = RegisterSerializer(data=request.data)
            if serializer.is_valid():
                verification_code = ''.join([str(random.randint(0, 9)) for _ in range(6)])

                user = serializer.save(verification_code=verification_code, is_active=False)

                send_verification_email(user.email, user.username, verification_code)

                return Response({'message': 'Se ha enviado un correo electrónico de verificación'}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "data": {
                    "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "title": ["Se produjo un error interno"],
                    "errors": str(e)
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def send_verification_email(user_email, username, verification_code):
    subject = 'Verifica tu dirección de correo electrónico'
    html_content = render_to_string('verify_email.html', {'username': username, 'verification_code': verification_code, 'user_email': user_email})
    send_mail(
        subject,
        '',
        'escuchamos2024@gmail.com', 
        [user_email],
        html_message=html_content,
    )
    
# class UserVerifyAPIView(APIView):
#     def get(self, request, token):
#         try:
#             user = User.objects.get(email_verification_token=token)
#             user.is_email_verified = True
#             user.save()
#             return Response({'message': 'Tu correo electrónico ha sido verificado exitosamente.'}, status=status.HTTP_200_OK)
#         except User.DoesNotExist:
#             return Response({'message': 'El token de verificación no es válido.'}, status=status.HTTP_400_BAD_REQUEST)


class EmailVerificationAPIView(APIView):
    def post(self, request):
        verification_code = request.data.get('verification_code')
        user_email = request.data.get('user_email')

        try:
            user = User.objects.get(email=user_email)
        except User.DoesNotExist:
            return Response({'message': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        if user.verification_code == verification_code:
            user.is_active = True
            user.is_email_verified = True
            user.save()
            return Response({'message': 'Tu dirección de correo electrónico ha sido verificada correctamente'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'El código de verificación es incorrecto'}, status=status.HTTP_400_BAD_REQUEST)


class CustomPagination(PageNumberPagination):
    page_size_query_param = 'pag'

#-----------------------------------------------------------------------------------------------------
# CRUD USUARIOS
#-----------------------------------------------------------------------------------------------------
  

class UserIndexAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # required_permissions = 'view_user'

    def get(self, request):
        try:
            users = User.objects.all()

            user_filter = UserFilter(request.query_params, queryset=users)
            filtered_users = user_filter.qs

            if 'pag' in request.query_params:
                pagination = CustomPagination()
                paginated_users = pagination.paginate_queryset(filtered_users, request)
                serializer = UserSerializer(paginated_users, many=True)
                return pagination.get_paginated_response({"users": serializer.data})
            
            serializer = UserSerializer(filtered_users, many=True)
            return Response({"users": serializer.data})
        
        except Exception as e:
            return Response({
                "data": {
                    "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "title": ["Se produjo un error interno"],
                    "errors": str(e)
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
           
class UserStoreAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # required_permissions = 'add_user'

    def post(self, request):
        try:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                role_id = serializer.validated_data.get('role_id')
                if role_id is not None:
                    if not Role.objects.filter(pk=role_id).exists():
                        return Response({"error": "El role_id proporcionado no existe"}, status=status.HTTP_400_BAD_REQUEST)
                serializer.save()
                username = serializer.validated_data.get('username')
                username = username.lower()  # Agregar esta línea para convertir el nombre de usuario a minúsculas
                return Response({"message": "¡Has sido registrado exitosamente!"}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({
                "error": "Se produjo un error interno",
                "details": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        
class UserShowAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # required_permissions = 'view_user'

    def get(self, request, pk):
        try:

            user = User.objects.filter(pk=pk).first()
            if not user:
                return Response({
                    "mensaje": "El ID de usuario no está registrado."
                }, status=status.HTTP_404_NOT_FOUND)

            serializer = UserSerializer(user)
            return Response(serializer.data)

        except Exception as e:
            return Response({
                "data": {
                    "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "title": ["Se produjo un error interno"],
                    "errors": str(e)
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        
class UserUpdateAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # required_permissions = 'change_user'

    def put(self, request, pk):
        try:
            user = User.objects.filter(pk=pk).first()
            if not user:
                return Response({
                    "message": "El ID de usuario no está registrado."
                }, status=status.HTTP_404_NOT_FOUND)
            
            data = request.data
            
            for field, value in data.items():
                if field == 'password':
                    if len(value) < 8:
                        raise serializers.ValidationError("La contraseña debe tener al menos 8 caracteres.")
                    if not any(char.isdigit() for char in value) or not any(char.isalpha() for char in value):
                        raise serializers.ValidationError("La contraseña debe ser alfanumérica.")
                    value = make_password(value)
                if (value not in ('', 'null') and value is not None) and hasattr(user, field):
                     setattr(user, field, value)
            user.save()

            username = data.get('username', None)
            if username:
                data['username'] = username.lower()
            
            serializer = UserSerializer(user, data=data, partial=True)  # Permitir actualizaciones parciales
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "data": {
                    "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "title": ["Se produjo un error interno"],
                    "errors": str(e)
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class UserDeleteAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # required_permissions = 'delete_user'

    def delete(self, request, pk):
        try:
            user = get_object_or_404(User, pk=pk)
            user.delete()
            return Response({"message": "¡Usuario eliminado exitosamente!"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({
                "data": {
                    "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "title": ["Se produjo un error interno"],
                    "errors": str(e)
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UserRestoreAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # required_permissions = 'delete_user'

    def get(self, request, pk):
        try:
            user = get_object_or_404(User, pk=pk, deleted_at__isnull=False)
            user.deleted_at = None
            user.save()
            return Response({"message": "¡Usuario restaurada exitosamente!"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "data": {
                    "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "title": ["Se produjo un error interno"],
                    "errors": str(e)
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#-----------------------------------------------------------------------------------------------------
# PERFIL
#-----------------------------------------------------------------------------------------------------    
class UserPhotoUpload(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # required_permissions = 'delete_user'
    
    def post(self, request, format=None):
        try:
            serializer = UserSerializer(request.user, data=request.data, partial=True)
            if serializer.is_valid():
                user = serializer.save()
                photo_file = request.data.get('photo')  # Obtén el archivo de la solicitud POST
                image_type = request.data.get('image_type')  # Obtén el tipo de imagen de la solicitud POST
                if image_type not in ['perfil', 'portada']:
                    return Response({'error': 'El tipo de imagen debe ser "perfil" o "portada"'}, status=status.HTTP_400_BAD_REQUEST)
                user.upload_photo(photo_file, image_type=image_type)  # Llama al método upload_photo() en el modelo User con el tipo de imagen
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)     
        
#-----------------------------------------------------------------------------------------------------
# CRUD PAISES
#-----------------------------------------------------------------------------------------------------

class CountryIndexAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # required_permissions = 'view_country'
    def get(self, request):
        try:
            countries = Country.objects.all()
            serializer = CountrySerializer(countries, many=True)
            return Response({"countries": serializer.data})
        except Exception as e:
            return Response({
                "data": {
                    "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "title": ["Se produjo un error interno"],
                    "errors": str(e)
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CountryShowAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # required_permissions = 'view_country'
    def get(self, request, pk):
        try:
            country = Country.objects.filter(pk=pk).first()
            if not country:
                return Response({
                    "mensaje": "El ID del país no está registrado."
                }, status=status.HTTP_404_NOT_FOUND)
            serializer = CountrySerializer(country)
            return Response(serializer.data)
        except Exception as e:
            return Response({
                "data": {
                    "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "title": ["Se produjo un error interno"],
                    "errors": str(e)
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

#-----------------------------------------------------------------------------------------------------
# CRUD ESTADOS
#-----------------------------------------------------------------------------------------------------
  
class StatusIndexAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # required_permissions = 'view_status'

    def get(self, request):
        try:
            statuses = Status.objects.all()

            if 'pag' in request.query_params:
                status_filter = StatusFilter(request.query_params, queryset=statuses)
                filtered_statuses = status_filter.qs

                pagination = CustomPagination()
                paginated_statuses = pagination.paginate_queryset(filtered_statuses, request)
                serializer = StatusSerializer(paginated_statuses, many=True)
                return pagination.get_paginated_response({"statuses": serializer.data})

            serializer = StatusSerializer(statuses, many=True)
            return Response({"statuses": serializer.data})
        
        except Exception as e:
            return Response({
                "data": {
                    "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "title": ["Se produjo un error interno"],
                    "errors": str(e)
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class StatusShowAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # required_permissions = 'view_status'

    def get(self, request, pk):
        try:
            status_obj = Status.objects.filter(pk=pk).first()
            if not status_obj:
                return Response({
                    "mensaje": "El ID de estado no está registrado."
                }, status=status.HTTP_404_NOT_FOUND)

            serializer = StatusSerializer(status_obj)
            return Response(serializer.data)

        except Exception as e:
            return Response({
                "data": {
                    "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "title": ["Se produjo un error interno"],
                    "errors": str(e)
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

#-----------------------------------------------------------------------------------------------------
# CRUD CATEGORIAS
#-----------------------------------------------------------------------------------------------------
  

class CategoryIndexAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # required_permissions = 'view_category'

    def get(self, request):
        try:
            categories = Category.objects.all()

            if request.query_params:
                category_filter = CategoryFilter(request.query_params, queryset=categories)
                categories = category_filter.qs
            if 'pag' in request.query_params:
                pagination = CustomPagination()
                paginated_categories = pagination.paginate_queryset(categories, request)
                serializer = CategorySerializer(paginated_categories, many=True)
                return pagination.get_paginated_response({"categories": serializer.data})
            
            serializer = CategorySerializer(categories, many=True)
            return Response({"categories": serializer.data})
        
        except Exception as e:
            return Response({
                "data": {
                    "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "title": ["Se produjo un error interno"],
                    "errors": str(e)
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
          
class CategoryStoreAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # required_permissions = 'add_category'

    def post(self, request):
        try:
            serializer = CategorySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "¡Categoría registrada exitosamente!"}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "data": {
                    "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "title": ["Se produjo un error interno"],
                    "errors": str(e)
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CategoryShowAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # required_permissions = 'view_category'

    def get(self, request, pk):
        try:

            category = Category.objects.filter(pk=pk).first()
            if not category:
                return Response({
                    "mensaje": "El ID de la categoría no está registrado."
                }, status=status.HTTP_404_NOT_FOUND)
            serializer = CategorySerializer(category)
            return Response(serializer.data)

        except Exception as e:
            return Response({
                "data": {
                    "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "title": ["Se produjo un error interno"],
                    "errors": str(e)
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CategoryUpdateAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # required_permissions = 'change_category'

    def put(self, request, pk):
        try:

            try:
                category = Category.objects.get(pk=pk)
            except Category.DoesNotExist:
                return Response({"message": "El ID de categoría no está registrado"}, status=status.HTTP_404_NOT_FOUND)
            data = request.data
            
            for field, value in data.items():
                if (value not in ('', 'null') and value is not None) and hasattr(category, field):
                     setattr(category, field, value)

            category.save()

            serializer = CategorySerializer(category)
            return Response(serializer.data)
        except Exception as e:
            return Response({
                "data": {
                    "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "title": ["Se produjo un error interno"],
                    "errors": str(e)
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class CategoryDeleteAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # required_permissions = 'delete_category'

    def delete(self, request, pk):
        try:
            category = get_object_or_404(Category, pk=pk)
            category.delete()
            return Response({"message": "¡Categoría eliminada exitosamente!"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({
                "data": {
                    "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "title": ["Se produjo un error interno"],
                    "errors": str(e)
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CategoryRestoreAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # required_permissions = 'delete_category'

    def get(self, request, pk):
        try:
            category = get_object_or_404(Category, pk=pk, deleted_at__isnull=False)
            category.deleted_at = None
            category.save()
            return Response({"message": "¡Categoría restaurada exitosamente!"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "data": {
                    "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "title": ["Se produjo un error interno"],
                    "errors": str(e)
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
#-----------------------------------------------------------------------------------------------------
# CRUD UNIDADES DE MEDIDA
#-----------------------------------------------------------------------------------------------------
  
    
class UnitIndexAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # required_permissions = 'view_unit'

    def get(self, request):
        try:
            units = Unit.objects.all()

            if request.query_params:
                unit_filter = UnitFilter(request.query_params, queryset=units)
                units = unit_filter.qs

            if 'pag' in request.query_params:
                pagination = CustomPagination() 
                paginated_units = pagination.paginate_queryset(units, request)
                serializer = UnitSerializer(paginated_units, many=True)
                return pagination.get_paginated_response({"units": serializer.data})
            
            serializer = UnitSerializer(units, many=True)
            return Response({"units": serializer.data})
        
        except Exception as e:
            return Response({
                "data": {
                    "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "title": ["Se produjo un error interno"],
                    "errors": str(e)
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class UnitStoreAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # required_permissions = 'add_unit'

    def post(self, request):
        try:
            serializer = UnitSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "¡Unidad de medida registrada exitosamente!"}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "data": {
                    "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "title": ["Se produjo un error interno"],
                    "errors": str(e)
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UnitShowAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # required_permissions = 'view_unit'

    def get(self, request, pk):
        try:
            unit = Unit.objects.filter(pk=pk).first()
            if not unit:
                return Response({
                    "mensaje": "El ID de la unidad no está registrado."
                }, status=status.HTTP_404_NOT_FOUND)

            serializer = UnitSerializer(unit)
            return Response(serializer.data)

        except Exception as e:
            return Response({
                "data": {
                    "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "title": ["Se produjo un error interno"],
                    "errors": str(e)
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class UnitUpdateAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # required_permissions = 'change_unit'


    def put(self, request, pk):
        try:

            if not Unit.objects.filter(pk=pk).exists():
                return Response({
                    "message": "El ID no está registrado"
                }, status=status.HTTP_404_NOT_FOUND)
            
            unit = get_object_or_404(Unit, pk=pk)
            
            data = request.data
            
            for field, value in data.items():
                if (value not in ('', 'null') and value is not None) and hasattr(unit, field):
                     setattr(unit, field, value)
            
            unit.save()
            
            serializer = UnitSerializer(unit)
            return Response(serializer.data)
        except Exception as e:
            return Response({
                "data": {
                    "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "title": ["Se produjo un error interno"],
                    "errors": str(e)
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class UnitDeleteAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # required_permissions = ['delete_units']

    def delete(self, request, pk):
        try:
            unit = get_object_or_404(Unit, pk=pk)
            unit.delete()
            return Response({"message": "¡Unidad de medida eliminada exitosamente!"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({
                "data": {
                    "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "title": ["Se produjo un error interno"],
                    "errors": str(e)
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class UnitRestoreAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # required_permissions = ['delete_units']

    def get(self, request, pk):
        try:
            unit = get_object_or_404(Unit, pk=pk, deleted_at__isnull=False)
            unit.deleted_at = None
            unit.save()
            return Response({"message": "¡Unidad de medida restaurada exitosamente!"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "data": {
                    "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "title": ["Se produjo un error interno"],
                    "errors": str(e)
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#-----------------------------------------------------------------------------------------------------
# CRUD TIPO DE PUBLICACION
#-----------------------------------------------------------------------------------------------------
          
class TypePostIndexAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # required_permissions = 'view_type_post'

    def get(self, request):
        try:
            type_posts = TypePost.objects.all()

            if request.query_params:
                type_post_filter = TypePostFilter(request.query_params, queryset=type_posts)
                type_posts = type_post_filter.qs

            if 'pag' in request.query_params:
                pagination = CustomPagination() 
                paginated_type_posts = pagination.paginate_queryset(type_posts, request)
                serializer = TypePostSerializer(paginated_type_posts, many=True)
                return pagination.get_paginated_response({"type_posts": serializer.data})
            
            serializer = TypePostSerializer(type_posts, many=True)
            return Response({"type_posts": serializer.data})
        
        except Exception as e:
            return Response({
                "data": {
                    "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "title": ["Se produjo un error interno"],
                    "errors": str(e)
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class TypePostStoreAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # required_permissions = 'add_type_post'

    def post(self, request):
        try:
            serializer = TypePostSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "¡Tipo de publicación registrado exitosamente!"}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "data": {
                    "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "title": ["Se produjo un error interno"],
                    "errors": str(e)
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class TypePostShowAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # required_permissions = 'view_type_post'

    def get(self, request, pk):
        try:
            type_post = TypePost.objects.filter(pk=pk).first()
            if not type_post:
                return Response({
                    "mensaje": "El ID del tipo de publicación no está registrado."
                }, status=status.HTTP_404_NOT_FOUND)

            serializer = TypePostSerializer(type_post)
            return Response(serializer.data)

        except Exception as e:
            return Response({
                "data": {
                    "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "title": ["Se produjo un error interno"],
                    "errors": str(e)
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class TypePostUpdateAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # required_permissions = 'change_type-post'
           
    def put(self, request, pk):
        try:

            if not TypePost.objects.filter(pk=pk).exists():
                return Response({
                    "message": "El ID no está registrado"
                }, status=status.HTTP_404_NOT_FOUND)
            
            typepost = get_object_or_404(TypePost, pk=pk)
            
            data = request.data
            
            for field, value in data.items():
                if (value not in ('', 'null') and value is not None) and hasattr(typepost, field):
                     setattr(typepost, field, value)
            
            typepost.save()
            
            serializer = TypePostSerializer(typepost)
            return Response(serializer.data)
        except Exception as e:
            return Response({
                "data": {
                    "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "title": ["Se produjo un error interno"],
                    "errors": str(e)
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        
class TypePostDeleteAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # required_permissions = ['delete_type_posts']

    def delete(self, request, pk):
        try:
            type_post = get_object_or_404(TypePost, pk=pk)
            type_post.delete()
            return Response({"message": "¡Tipo de publicación eliminado exitosamente!"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({
                "data": {
                    "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "title": ["Se produjo un error interno"],
                    "errors": str(e)
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class TypePostRestoreAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # required_permissions = ['delete_type_posts']

    def get(self, request, pk):
        try:
            type_post = get_object_or_404(TypePost, pk=pk, deleted_at__isnull=False)
            type_post.deleted_at = None
            type_post.save()
            return Response({"message": "¡Tipo de publicación restaurado exitosamente!"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "data": {
                    "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "title": ["Se produjo un error interno"],
                    "errors": str(e)
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


#-----------------------------------------------------------------------------------------------------
# CRUD ESTADOS DE PEDIDO
#-----------------------------------------------------------------------------------------------------

class OrderStatusesIndexAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # required_permissions = 'view_type_post'

    def get(self, request):
        try:
            order_statuses = OrderStatuses.objects.all()

            if request.query_params:
                order_status_filter = OrderStatusesFilter(request.query_params, queryset=order_statuses)
                order_statuses = order_status_filter.qs

            if 'pag' in request.query_params:
                pagination = CustomPagination() 
                paginated_order_statuses = pagination.paginate_queryset(order_statuses, request)
                serializer = OrderStatusesSerializer(paginated_order_statuses, many=True)
                return pagination.get_paginated_response({"order_statuses": serializer.data})
            
            serializer = OrderStatusesSerializer(order_statuses, many=True)
            return Response({"order_statuses": serializer.data})
        
        except Exception as e:
            return Response({
                "data": {
                    "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "title": ["Se produjo un error interno"],
                    "errors": str(e)
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class OrderStatusesStoreAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # required_permissions = 'add_type_post'

    def post(self, request):
        try:
            serializer = OrderStatusesSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "¡Estado de orden registrado exitosamente!"}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "data": {
                    "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "title": ["Se produjo un error interno"],
                    "errors": str(e)
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class OrderStatusesShowAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # required_permissions = 'view_type_post'

    def get(self, request, pk):
        try:
            order_status = OrderStatuses.objects.filter(pk=pk).first()
            if not order_status:
                return Response({
                    "mensaje":
"El ID del estado de orden no está registrado."
                }, status=status.HTTP_404_NOT_FOUND)

            serializer = OrderStatusesSerializer(order_status)
            return Response(serializer.data)

        except Exception as e:
            return Response({
                "data": {
                    "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "title": ["Se produjo un error interno"],
                    "errors": str(e)
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class OrderStatusesUpdateAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # required_permissions = 'change_type-post'
           
    def put(self, request, pk):
        try:

            if not OrderStatuses.objects.filter(pk=pk).exists():
                return Response({
                    "message": "El ID no está registrado"
                }, status=status.HTTP_404_NOT_FOUND)
            
            orderstatus = get_object_or_404(OrderStatuses, pk=pk)
            
            data = request.data
            
            for field, value in data.items():
                if (value not in ('', 'null') and value is not None) and hasattr(orderstatus, field):
                     setattr(orderstatus, field, value)
            
            orderstatus.save()
            
            serializer = OrderStatusesSerializer(orderstatus)
            return Response(serializer.data)
        except Exception as e:
            return Response({
                "data": {
                    "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "title": ["Se produjo un error interno"],
                    "errors": str(e)
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        
class OrderStatusesDeleteAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # required_permissions = ['delete_type_posts']

    def delete(self, request, pk):
        try:
            order_status = get_object_or_404(OrderStatuses, pk=pk)
            order_status.delete()
            return Response({"message": "¡Estado de orden eliminado exitosamente!"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({
                "data": {
                    "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "title": ["Se produjo un error interno"],
                    "errors": str(e)
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class OrderStatusesRestoreAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # required_permissions = ['delete_type_posts']

    def get(self, request, pk):
        try:
            order_status = get_object_or_404(OrderStatuses, pk=pk, deleted_at__isnull=False)
            order_status.deleted_at = None
            order_status.save()
            return Response({"message": "¡Estado de orden restaurado exitosamente!"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "data": {
                    "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "title": ["Se produjo un error interno"],
                    "errors": str(e)
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


#-----------------------------------------------------------------------------------------------------
# CRUD GENERO
#-----------------------------------------------------------------------------------------------------

class GenderIndexAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # required_permissions = 'view_type_post'

    def get(self, request):
        try:
            genders = Gender.objects.all()

            if request.query_params:
                gender_filter = GenderFilter(request.query_params, queryset=genders)
                genders = gender_filter.qs

            if 'pag' in request.query_params:
                pagination = CustomPagination() 
                paginated_genders = pagination.paginate_queryset(genders, request)
                serializer = GenderSerializer(paginated_genders, many=True)
                return pagination.get_paginated_response({"genders": serializer.data})
            
            serializer = GenderSerializer(genders, many=True)
            return Response({"genders": serializer.data})
        
        except Exception as e:
            return Response({
                "data": {
                    "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "title": ["Se produjo un error interno"],
                    "errors": str(e)
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class GenderStoreAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # required_permissions = 'add_type_post'

    def post(self, request):
        try:
            serializer = GenderSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "¡Género registrado exitosamente!"}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "data": {
                    "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "title": ["Se produjo un error interno"],
                    "errors": str(e)
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GenderShowAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # required_permissions = 'view_type_post'

    def get(self, request, pk):
        try:
            gender = Gender.objects.filter(pk=pk).first()
            if not gender:
                return Response({
                    "mensaje": "El ID del género no está registrado."
                }, status=status.HTTP_404_NOT_FOUND)

            serializer = GenderSerializer(gender)
            return Response(serializer.data)

        except Exception as e:
            return Response({
                "data": {
                    "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "title": ["Se produjo un error interno"],
                    "errors": str(e)
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class GenderUpdateAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # required_permissions = 'change_type-post'
           
    def put(self, request, pk):
        try:

            if not Gender.objects.filter(pk=pk).exists():
                return Response({
                    "message": "El ID no está registrado"
                }, status=status.HTTP_404_NOT_FOUND)
            
            gender = get_object_or_404(Gender, pk=pk)
            
            data = request.data
            
            for field, value in data.items():
                if (value not in ('', 'null') and value is not None) and hasattr(gender, field):
                     setattr(gender, field, value)
            
            gender.save()
            
            serializer = GenderSerializer(gender)
            return Response(serializer.data)
        except Exception as e:
            return Response({
                "data": {
                    "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "title": ["Se produjo un error interno"],
                    "errors": str(e)
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        
class GenderDeleteAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # required_permissions = ['delete_type_posts']

    def delete(self, request, pk):
        try:
            gender = get_object_or_404(Gender, pk=pk)
            gender.delete()
            return Response({"message": "¡Género eliminado exitosamente!"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({
                "data": {
                    "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "title": ["Se produjo un error interno"],
                    "errors": str(e)
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class GenderRestoreAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # required_permissions = ['delete_type_posts']

    def get(self, request, pk):
        try:
            gender = get_object_or_404(Gender, pk=pk, deleted_at__isnull=False)
            gender.deleted_at = None
            gender.save()
            return Response({"message": "¡Género restaurado exitosamente!"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "data": {
                    "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "title": ["Se produjo un error interno"],
                    "errors": str(e)
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#-----------------------------------------------------------------------------------------------------
# CRUD TIPO DE PERSONA
#-----------------------------------------------------------------------------------------------------

class TypePersonIndexAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # required_permissions = 'view_type_persons'

    def get(self, request):
        try:
            type_persons = TypePerson.objects.all()

            if request.query_params:
                type_persons_filter = TypePersonFilter(request.query_params, queryset=type_persons)
                type_persons = type_persons_filter.qs

            if 'pag' in request.query_params:
                pagination = CustomPagination() 
                paginated_type_persons = pagination.paginate_queryset(type_persons, request)
                serializer = TypePersonSerializer(paginated_type_persons, many=True)
                return pagination.get_paginated_response({"type_persons": serializer.data})
            
            serializer = TypePersonSerializer(type_persons, many=True)
            return Response({"type_persons": serializer.data})
        
        except Exception as e:
            return Response({
                "data": {
                    "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "title": ["Se produjo un error interno"],
                    "errors": str(e)
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
class TypePersonStoreAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # required_permissions = 'add_type_persons'

    def post(self, request):
        try:
            serializer = TypePersonSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "¡Tipo de persona registrado exitosamente!"}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "data": {
                    "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "title": ["Se produjo un error interno"],
                    "errors": str(e)
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class TypePersonShowAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # required_permissions = 'view_type_person'

    def get(self, request, pk):
        try:
            type_person = TypePerson.objects.filter(pk=pk).first()
            if not type_person:
                return Response({
                    "mensaje": "El ID del tipo de persona no está registrado."
                }, status=status.HTTP_404_NOT_FOUND)

            serializer = TypePersonSerializer(type_person)
            return Response(serializer.data)

        except Exception as e:
            return Response({
                "data": {
                    "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "title": ["Se produjo un error interno"],
                    "errors": str(e)
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class TypePersonUpdateAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # required_permissions = 'change_type_person'


    def put(self, request, pk):
        try:

            if not TypePerson.objects.filter(pk=pk).exists():
                return Response({
                    "message": "El ID no está registrado"
                }, status=status.HTTP_404_NOT_FOUND)
            
            type_person = get_object_or_404(TypePerson, pk=pk)
            
            data = request.data
            
            for field, value in data.items():
                if (value not in ('', 'null') and value is not None) and hasattr(type_person, field):
                     setattr(type_person, field, value)
            
            type_person.save()
            
            serializer = TypePostSerializer(type_person)
            return Response(serializer.data)
        except Exception as e:
            return Response({
                "data": {
                    "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "title": ["Se produjo un error interno"],
                    "errors": str(e)
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class TypePersonDeleteAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # required_permissions = ['delete_type_person']

    def delete(self, request, pk):
        try:
            type_person = get_object_or_404(TypePerson, pk=pk)
            type_person.delete()
            return Response({"message": "¡Tipo de persona eliminado exitosamente!"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({
                "data": {
                    "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "title": ["Se produjo un error interno"],
                    "errors": str(e)
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class TypePersonRestoreAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # required_permissions = ['delete_type_person']

    def get(self, request, pk):
        try:
            type_person = get_object_or_404(TypePerson, pk=pk, deleted_at__isnull=False)
            type_person.deleted_at = None
            type_person.save()
            return Response({"message": "¡Tipo de persona restaurado exitosamente!"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "data": {
                    "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "title": ["Se produjo un error interno"],
                    "errors": str(e)
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# #-----------------------------------------------------------------------------------------------------
# # CRUD ACTIVIDADES
# #-----------------------------------------------------------------------------------------------------

class ActivityIndexAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # required_permissions = 'view_activity'

    def get(self, request):
        try:
            activities = Activity.objects.all()

            activity_filter = ActivityFilter(request.query_params, queryset=activities)
            filtered_activities = activity_filter.qs

            if 'pag' in request.query_params:
                pagination = CustomPagination()
                paginated_activities = pagination.paginate_queryset(filtered_activities, request)
                serializer = ActivityIndexSerializer(paginated_activities, many=True)
                return pagination.get_paginated_response({"activities": serializer.data})
            
            serializer = ActivityIndexSerializer(filtered_activities, many=True)
            return Response({"activities": serializer.data})
        
        except Exception as e:
            return Response({
                "data": {
                    "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "title": ["Se produjo un error interno"],
                    "errors": str(e)
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class ActivityStoreAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # required_permissions = ['add_activity']

    def post(self, request):
        benefited_data = request.data.pop('benefited', None)

        try:
            user_id = request.data.get('user_id')
            existing_user = User.objects.filter(id=user_id).exists()

            if existing_user:
                current_user = User.objects.get(id=user_id)
            else:
                return Response({"message": "El usuario especificado no existe"}, status=status.HTTP_404_NOT_FOUND)

            activity_serializer = ActivitySerializer(data=request.data)
            if activity_serializer.is_valid():
                activity = activity_serializer.save(user=current_user)
            else:
                return Response(activity_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            if benefited_data:
                for benefited_item in benefited_data:
                    benefited_item['activity_id'] = activity.id
                    benefited_serializer = BenefitedSerializer(data=benefited_item)
                    if benefited_serializer.is_valid():
                        benefited_serializer.save()
                    else:
                        return Response(benefited_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            return Response({"message": "Actividad creada satisfactoriamente!"}, status=status.HTTP_201_CREATED)

        except User.DoesNotExist:
            return Response({"message": "El usuario especificado no existe"}, status=status.HTTP_404_NOT_FOUND)


        
class ActivityShowAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # required_permissions = 'view_activity'

    def get(self, request, pk):
        try:

            activity = Activity.objects.filter(pk=pk).first()
            if not activity:
                return Response({
                    "mensaje": "El ID de actividad no está registrado."
                }, status=status.HTTP_404_NOT_FOUND)

            serializer = ActivitySerializer(activity)
            return Response(serializer.data)

        except Exception as e:
            return Response({
                "data": {
                    "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "title": ["Se produjo un error interno"],
                    "errors": str(e)
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        
class ActivityUpdateAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # required_permissions = 'change_activity'

    def put(self, request, pk):
        try:

            if not Activity.objects.filter(pk=pk).exists():
                return Response({
                    "message": "El ID no está registrado"
                }, status=status.HTTP_404_NOT_FOUND)
            
            activity = get_object_or_404(Activity, pk=pk)
            
            data = request.data
            
            for field, value in data.items():
                if (value not in ('', 'null') and value is not None) and hasattr(activity, field):
                     setattr(activity, field, value)
            
            activity.save()
            
            serializer = ActivitySerializer(activity)
            return Response(serializer.data)
        except Exception as e:
            return Response({
                "data": {
                    "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "title": ["Se produjo un error interno"],
                    "errors": str(e)
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        
class ActivityDeleteAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # required_permissions = 'delete_activity'

    def delete(self, request, pk):
        try:
            activity = get_object_or_404(Activity, pk=pk)
            activity.delete()
            return Response({"message": "¡Actividad eliminada exitosamente!"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({
                "data": {
                    "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "title": ["Se produjo un error interno"],
                    "errors": str(e)
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ActivityRestoreAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # required_permissions = 'delete_activity'

    def get(self, request, pk):
        try:
            activity = get_object_or_404(Activity, pk=pk, deleted_at__isnull=False)
            activity.deleted_at = None
            activity.save()
            return Response({"message": "¡Actividad restaurada exitosamente!"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "data": {
                    "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "title": ["Se produjo un error interno"],
                    "errors": str(e)
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# #-----------------------------------------------------------------------------------------------------
# # CRUD BENEFICIADOS
# #-----------------------------------------------------------------------------------------------------

class BenefitedIndexAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # required_permissions = 'view_activity'

    def get(self, request):
        try:
            benefited = Benefited.objects.all()

            benefited_filter = BenefitedFilter(request.query_params, queryset=benefited)
            filtered_benefited = benefited_filter.qs

            if 'pag' in request.query_params:
                pagination = CustomPagination()
                paginated_benefited = pagination.paginate_queryset(filtered_benefited, request)
                serializer = BenefitedSerializer(paginated_benefited, many=True)
                return pagination.get_paginated_response({"benefited": serializer.data})
            
            serializer = BenefitedSerializer(filtered_benefited, many=True)
            return Response({"benefited": serializer.data})
        
        except Exception as e:
            return Response({
                "data": {
                    "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "title": ["Se produjo un error interno"],
                    "errors": str(e)
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class BenefitedStoreAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # required_permissions = 'add_activity'

    def post(self, request):
        try:
            serializer = BenefitedSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "¡Beneficiario registrado exitosamente!"}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({
                "error": "Se produjo un error interno",
                "details": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class BenefitedShowAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # required_permissions = 'view_activity'

    def get(self, request, pk):
        try:

            benefited = Benefited.objects.filter(pk=pk).first()
            if not benefited:
                return Response({
                    "mensaje": "El ID del beneficiario no está registrado."
                }, status=status.HTTP_404_NOT_FOUND)

            serializer = BenefitedSerializer(benefited)
            return Response(serializer.data)

        except Exception as e:
            return Response({
                "data": {
                    "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "title": ["Se produjo un error interno"],
                    "errors": str(e)
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class BenefitedUpdateAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # required_permissions = 'change_activity'

    def put(self, request, pk):
        try:

            if not Benefited.objects.filter(pk=pk).exists():
                return Response({
                    "message": "El ID no está registrado"
                }, status=status.HTTP_404_NOT_FOUND)
            
            benefited = get_object_or_404(Benefited, pk=pk)
            
            data = request.data
            
            for field, value in data.items():
                if (value not in ('', 'null') and value is not None) and hasattr(benefited, field):
                     setattr(benefited, field, value)
            
            benefited.save()
            
            serializer = BenefitedSerializer(benefited)
            return Response(serializer.data)
        except Exception as e:
            return Response({
                "data": {
                    "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "title": ["Se produjo un error interno"],
                    "errors": str(e)
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class BenefitedDeleteAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # required_permissions = 'delete_activity'

    def delete(self, request, pk):
        try:
            benefited = get_object_or_404(Benefited, pk=pk)
            benefited.delete()
            return Response({"message": "¡Beneficiario eliminado exitosamente!"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({
                "data": {
                    "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "title": ["Se produjo un error interno"],
                    "errors": str(e)
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class BenefitedRestoreAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # required_permissions = 'delete_activity'

    def get(self, request, pk):
        try:
            benefited = get_object_or_404(Benefited, pk=pk, deleted_at__isnull=False)
            benefited.deleted_at = None
            benefited.save()
            return Response({"message": "¡Beneficiario restaurado exitosamente!"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "data": {
                    "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "title": ["Se produjo un error interno"],
                    "errors": str(e)
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# #-----------------------------------------------------------------------------------------------------
# # CRUD PRODUCTOS
# #-----------------------------------------------------------------------------------------------------


class ProductIndexAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # required_permissions = 'view_product'

    def get(self, request):
        try:
            product = Product.objects.all()

            product_filter = ProductFilter(request.query_params, queryset=product)
            filtered_product = product_filter.qs

            if 'pag' in request.query_params:
                pagination = CustomPagination()
                paginated_product = pagination.paginate_queryset(filtered_product, request)
                serializer = ProductSerializer(paginated_product, many=True)
                return pagination.get_paginated_response({"product": serializer.data})
            
            serializer = ProductSerializer(filtered_product, many=True)
            return Response({"product": serializer.data})
        
        except Exception as e:
            return Response({
                "data": {
                    "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "title": ["Se produjo un error interno"],
                    "errors": str(e)
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ProductStoreAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # required_permissions = 'add_product'

    def post(self, request):
        try:
            serializer = ProductSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "¡Producto registrado exitosamente!"}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({
                "error": "Se produjo un error interno",
                "details": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class ProductShowAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # required_permissions = 'view_product'

    def get(self, request, pk):
        try:

            product = Product.objects.filter(pk=pk).first()
            if not product:
                return Response({
                    "mensaje": "El ID del producto no está registrado."
                }, status=status.HTTP_404_NOT_FOUND)

            serializer = ProductSerializer(product)
            return Response(serializer.data)

        except Exception as e:
            return Response({
                "data": {
                    "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "title": ["Se produjo un error interno"],
                    "errors": str(e)
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ProductUpdateAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # required_permissions = 'change_product'

    def put(self, request, pk):
        try:

            if not Product.objects.filter(pk=pk).exists():
                return Response({
                    "message": "El ID no está registrado"
                }, status=status.HTTP_404_NOT_FOUND)
            
            product = get_object_or_404(Product, pk=pk)
            
            data = request.data
            
            for field, value in data.items():
                if (value not in ('', 'null') and value is not None) and hasattr(product, field):
                     setattr(product, field, value)
            
            product.save()
            
            serializer = ProductSerializer(product)
            return Response(serializer.data)
        except Exception as e:
            return Response({
                "data": {
                    "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "title": ["Se produjo un error interno"],
                    "errors": str(e)
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class ProductDeleteAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # required_permissions = 'delete_product'

    def delete(self, request, pk):
        try:
            product = get_object_or_404(Product, pk=pk)
            product.delete()
            return Response({"message": "¡Producto eliminado exitosamente!"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({
                "data": {
                    "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "title": ["Se produjo un error interno"],
                    "errors": str(e)
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class ProductRestoreAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # required_permissions = 'delete_product'

    def get(self, request, pk):
        try:
            product = get_object_or_404(Product, pk=pk, deleted_at__isnull=False)
            product.deleted_at = None
            product.save()
            return Response({"message": "¡Producto restaurado exitosamente!"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "data": {
                    "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "title": ["Se produjo un error interno"],
                    "errors": str(e)
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
# #-----------------------------------------------------------------------------------------------------
# # CRUD INVENTARIO
# #-----------------------------------------------------------------------------------------------------

class InventoryIndexAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # required_permissions = 'view_inventory'

    def get(self, request):
        try:
            inventories = Inventory.objects.all()

            if request.query_params:
                inventory_filter = InventoryFilter(request.query_params, queryset=inventories)
                inventories = inventory_filter.qs
                
            if 'pag' in request.query_params:
                pagination = CustomPagination()
                paginated_inventories = pagination.paginate_queryset(inventories, request)
                serializer = InventorySerializer(paginated_inventories, many=True)
            else:
                serializer = InventorySerializer(inventories, many=True)

            # for inventory_data in serializer.data:
            #     product_data = inventory_data.get('product')
            #     if product_data and 'img' in product_data:

            #         product_data['image_url'] = settings.PRODUCT_IMAGE_BASE_URL + str(product_data['img'])

            #         product_data.pop('img')

            if 'pag' in request.query_params:
                return pagination.get_paginated_response({"inventories": serializer.data})
            else:
                return Response({"inventories": serializer.data})
        
        except Exception as e:
            return Response({
                "data": {
                    "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "title": ["Se produjo un error interno"],
                    "errors": str(e)
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class InventoryAddInputAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity')
        user = request.user

        if not Product.objects.filter(id=product_id).exists():
            return Response({"message": "Este producto no existe."}, status=status.HTTP_404_NOT_FOUND)

        try:
            inventory = Inventory.objects.get(product_id=product_id)
            inventory.quantity += int(quantity)
            inventory.save()

            Input.objects.create(
                inventory=inventory,
                quantity=quantity,
                user=user
            )

            return Response({"message": "¡El inventario se actualizó exitosamente!", "Cantidad actual": inventory.quantity}, status=status.HTTP_200_OK)
        except Inventory.DoesNotExist:
            product = Product.objects.get(id=product_id)
            inventory = Inventory.objects.create(product=product, quantity=quantity)

            Input.objects.create(
                inventory=inventory,
                quantity=quantity,
                user=user
            )
            return Response({"message": f"¡Producto agregado exitosamente!", "Cantidad actual": inventory.quantity}, status=status.HTTP_201_CREATED)
        
class InventorySubOutputAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # required_permissions = 'add_inventory'

    def post(self, request):
        products = request.data.get('products', [])
        try:
            
            
            for product in products:
                product_id = product.get('product_id')
                quantity = product.get('quantity')

                inventory = Inventory.objects.get(product_id=product_id)
                if inventory.quantity < quantity:
                    return Response({"message": f"La cantidad solicitada para el producto {inventory.product.name} es mayor que la cantidad en inventario", "cantidad existente": inventory.quantity}, status=status.HTTP_400_BAD_REQUEST)

                Order.objects.create(
                    inventory=inventory,
                    quantity=quantity
                )

        except Inventory.DoesNotExist:
            return Response({"message": f"Uno de los productos no existe en el inventario"}, status=status.HTTP_404_NOT_FOUND)

class InventoryShowAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # required_permissions = 'view_inventory'

    def get(self, request, pk):
        try:

            inventory = Inventory.objects.filter(pk=pk).first()
            
            if not inventory:
                return Response({
                    "mensaje": "El ID del inventario no está registrado."
                }, status=status.HTTP_404_NOT_FOUND)

            inventory_serializer = InventorySerializer(inventory)

            return Response(inventory_serializer.data)

        except Exception as e:
            return Response({
                "data": {
                    "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "title": ["Se produjo un error interno"],
                    "errors": str(e)
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# #-----------------------------------------------------------------------------------------------------
# # CRUD ENTRADAS
# #-----------------------------------------------------------------------------------------------------

class InputIndexAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # required_permissions = 'view_input'

    def get(self, request):
        try:
            inputs = Input.objects.all()

            if request.query_params:
                input_filter = InputFilter(request.query_params, queryset=inputs)
                inputs = input_filter.qs

            if 'pag' in request.query_params:
                pagination = CustomPagination()
                paginated_inputs = pagination.paginate_queryset(inputs, request)
                serializer = InputSerializer(paginated_inputs, many=True)
                return pagination.get_paginated_response({"inputs": serializer.data})

            serializer = InputSerializer(inputs, many=True)
            return Response({"inputs": serializer.data})

        except Exception as e:
            return Response({
                "data": {
                    "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "title": ["Se produjo un error interno"],
                    "errors": str(e)
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class InputShowAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # required_permissions = 'view_input'

    def get(self, request, pk):
        try:
            input_obj = Input.objects.filter(pk=pk).first()
            if not input_obj:
                return Response({
                    "mensaje": "El ID de la entrada no está registrado."
                }, status=status.HTTP_404_NOT_FOUND)

            serializer = InputSerializer(input_obj)
            return Response(serializer.data)

        except Exception as e:
            return Response({
                "data": {
                    "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "title": ["Se produjo un error interno"],
                    "errors": str(e)
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
# #-----------------------------------------------------------------------------------------------------
# # CRUD RECIPES
# #-----------------------------------------------------------------------------------------------------

class OrderIndexAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # required_permissions = 'view_order'

    def get(self, request):
        try:
            orders = Order.objects.all()

            if request.query_params:
                order_filter = OrderFilter(request.query_params, queryset=orders)
                orders = order_filter.qs

            if 'pag' in request.query_params:
                pagination = CustomPagination()
                paginated_orders = pagination.paginate_queryset(orders, request)
                serializer = OrderSerializer(paginated_orders, many=True)
                return pagination.get_paginated_response({"orders": serializer.data})

            serializer = OrderSerializer(orders, many=True)
            return Response({"orders": serializer.data})

        except Exception as e:
            return Response({
                "data": {
                    "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "title": ["Se produjo un error interno"],
                    "errors": str(e)
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class OrderShowAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # required_permissions = 'view_order'

    def get(self, request, pk):
        try:
            order_obj = Order.objects.filter(pk=pk).first()
            if not order_obj:
                return Response({
                    "mensaje": "El ID de la entrada no está registrado."
                }, status=status.HTTP_404_NOT_FOUND)

            serializer = OrderSerializer(order_obj)
            return Response(serializer.data)

        except Exception as e:
            return Response({
                "data": {
                    "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "title": ["Se produjo un error interno"],
                    "errors": str(e)
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
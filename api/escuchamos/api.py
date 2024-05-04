from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import User, Role, Country  
from .serializer import *
from django.shortcuts import get_object_or_404
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.pagination import PageNumberPagination
from .filters import UserFilter, RoleFilter, StatusFilter
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
# CRUD USERS
#-----------------------------------------------------------------------------------------------------
  

class UserIndexAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

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

    def put(self, request, pk):
        try:
            user = User.objects.filter(pk=pk).first()
            if not user:
                return Response({
                    "message": "El ID de usuario no está registrado."
                }, status=status.HTTP_404_NOT_FOUND)
            
            data = request.data
            
            # Verificar si hay una nueva contraseña en los datos de la solicitud
            new_password = data.get('password', None)
            if new_password:
                # Encriptar la nueva contraseña
                data['password'] = make_password(new_password)

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
        
class CountryIndexAPIView(APIView):
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
        
class StatusIndexAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

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



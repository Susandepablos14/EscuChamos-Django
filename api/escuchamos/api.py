from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import User, Role
from .serializer import *
from django.shortcuts import get_object_or_404
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.pagination import PageNumberPagination
from .filters import UserFilter, RoleFilter
from django.contrib.auth import authenticate, login, logout
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.decorators import authentication_classes, permission_classes
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_encode
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse

#-----------------------------------------------------------------------------------------------------
# Inicio de Sesión
#-----------------------------------------------------------------------------------------------------

class UserLoginAPIView(APIView):
    authentication_classes = []

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        User = get_user_model()
        user = User.objects.filter(username=username).first()
        if user is not None and user.check_password(password):
            if user.is_active:
                login(request, user)
                token, created = Token.objects.get_or_create(user=user)
                return Response({'message': 'Inicio de sesión exitoso', 'token': token.key}, status=status.HTTP_200_OK)
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
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # Generar el token de verificación
            verification_token = default_token_generator.make_token(user)

            # Establecer el estado de verificación de correo electrónico como False y guardar el token
            user.is_email_verified = False 
            user.email_verification_token = verification_token
            user.save()

            # Construir el enlace de verificación de correo electrónico
            current_site = get_current_site(request)
            verification_url = reverse('verify_email', kwargs={'token': verification_token})
            full_verification_url = 'http://' + current_site.domain + verification_url

            # Enviar el correo electrónico de verificación
            send_verification_email(user.email, user.username, full_verification_url)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def send_verification_email(user_email, username, verification_link):
    subject = 'Verifica tu dirección de correo electrónico'
    html_content = render_to_string('verify_email.html', {'username': username, 'verification_link': verification_link, 'user_email' : user_email})
    send_mail(
        subject,
        '',
        'escuchamos2024@gmail.com', 
        [user_email],
        html_message=html_content,
    )
    
class UserVerifyAPIView(APIView):
    def get(self, request, token):
        try:
            user = User.objects.get(email_verification_token=token)
            user.is_email_verified = True
            user.save()
            return Response({'message': 'Tu correo electrónico ha sido verificado exitosamente.'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'message': 'El token de verificación no es válido.'}, status=status.HTTP_400_BAD_REQUEST)
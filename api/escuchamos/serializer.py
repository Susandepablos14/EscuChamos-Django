from rest_framework import serializers
from django.contrib.auth.hashers import make_password 
from .models import User, Role, Country

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 
                  'name', 
                  'description', 
                  'created_at',
                  'updated_at',
                  'deleted_at',  ]

class UserSerializer(serializers.ModelSerializer):
    role = RoleSerializer(read_only=True)

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("La contraseña debe tener al menos 8 caracteres.")
        if not any(char.isdigit() for char in value) or not any(char.isalpha() for char in value):
            raise serializers.ValidationError("La contraseña debe ser alfanumérica.")
        return value

    def create(self, validated_data):
        default_role = Role.objects.get(id=3)
        validated_data['role'] = default_role
        validated_data['password'] = make_password(validated_data['password']) 
        return super().create(validated_data)
    class Meta:
        model = User
        fields = ['id', 
                  'password',
                  'username', 
                  'email', 
                  'name', 
                  'last_name', 
                  'role_id',
                  'address',
                  'phone_number',
                  'is_active',
                  'is_staff',
                  'created_at',
                  'updated_at',
                  'deleted_at',  
                  'role', ]

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ('id', 'name', 'abbreviation', 'dialing_code', 'created_at', 'updated_at', 'deleted_at')
        read_only_fields = ('created_at', 'updated_at', 'deleted_at')

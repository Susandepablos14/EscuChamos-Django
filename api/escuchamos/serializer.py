from rest_framework import serializers
from django.contrib.auth.hashers import make_password 
from .models import User, Role, Country


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ('id',
                  'name', 
                  'abbreviation', 
                  'dialing_code', 
                  'created_at', 
                  'updated_at', 
                  'deleted_at')
        read_only_fields = ('created_at', 'updated_at', 'deleted_at')

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
    role_id = serializers.IntegerField(write_only=True) 
    country_id = serializers.PrimaryKeyRelatedField(queryset=Country.objects.all(), write_only=True, source='country')


    def validate_role_id(self, value):
        try:
            role = Role.objects.get(pk=value) 
        except Role.DoesNotExist:
            raise serializers.ValidationError("El ID de rol proporcionado no existe.") 
        return value

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("La contraseña debe tener al menos 8 caracteres.")
        if not any(char.isdigit() for char in value) or not any(char.isalpha() for char in value):
            raise serializers.ValidationError("La contraseña debe ser alfanumérica.")
        return value
    
    def create(self, validated_data):
        role_id = validated_data.pop('role_id')
        validated_data['password'] = make_password(validated_data['password']) 
        user = super().create(validated_data)
        role = Role.objects.get(pk=role_id)
        user.role = role
        user.save()
        return user

    class Meta:
        model = User
        fields = ['id', 
                  'password',
                  'username', 
                  'email', 
                  'name', 
                  'last_name', 
                  'role_id',
                  'country_id',
                  'address',
                  'phone_number',
                  'is_active',
                  'is_staff',
                  'created_at',
                  'updated_at',
                  'deleted_at',  
                  'role', ]
        extra_kwargs = {
            'password': {'write_only': True},  
        }

class RegisterSerializer(serializers.ModelSerializer):
    role = RoleSerializer(read_only=True)
    country_id = serializers.PrimaryKeyRelatedField(queryset=Country.objects.all(), write_only=True, source='country')

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
                  'country_id',
                  'address',
                  'phone_number',
                  'is_active',
                  'is_staff',
                  'created_at',
                  'updated_at',
                  'deleted_at',  
                  'role', ]



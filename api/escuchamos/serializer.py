from rest_framework import serializers
from django.contrib.auth.hashers import make_password 
from .models import *

#-----------------------------------------------------------------------------------------------------
# Paises
#-----------------------------------------------------------------------------------------------------

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

#-----------------------------------------------------------------------------------------------------
# Roles
#-----------------------------------------------------------------------------------------------------

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 
                  'name', 
                  'description', 
                  'created_at',
                  'updated_at',
                  'deleted_at',  ]

#-----------------------------------------------------------------------------------------------------
# Estados
#-----------------------------------------------------------------------------------------------------

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id',
                  'name', 
                  'description', 
                  'created_at',
                  'updated_at',
                  'deleted_at',  ]
        
#-----------------------------------------------------------------------------------------------------
# Usuario
#-----------------------------------------------------------------------------------------------------

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
        validated_data['username'] = validated_data['username'].lower()
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
#-----------------------------------------------------------------------------------------------------
# Registro
#-----------------------------------------------------------------------------------------------------

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
        validated_data['username'] = validated_data['username'].lower()
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
        
#-----------------------------------------------------------------------------------------------------
# Categoria
#-----------------------------------------------------------------------------------------------------
        
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 
                  'name', 
                  'description', 
                  'created_at',
                  'updated_at',
                  'deleted_at',  ]

    def validate_name(self, value):
        if Category.objects.filter(name=value).exists():
            raise serializers.ValidationError("Ya existe una categoría con este nombre.")
        return value

    def create(self, validated_data):
        return Category.objects.create(**validated_data)

#-----------------------------------------------------------------------------------------------------
# Unidades de medida
#-----------------------------------------------------------------------------------------------------

class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = ['id', 
                  'name', 
                  'description', 
                  'created_at',
                  'updated_at',
                  'deleted_at']

    def validate_name(self, value):
        if Unit.objects.filter(name=value).exists():
            raise serializers.ValidationError("Ya existe una unidad con este nombre.")
        return value

    def create(self, validated_data):
        return Unit.objects.create(**validated_data)
    
#-----------------------------------------------------------------------------------------------------
# Tipo de publicacion
#-----------------------------------------------------------------------------------------------------
    
class TypePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypePost 
        fields = ['id', 
                  'name', 
                  'description', 
                  'created_at',
                  'updated_at',
                  'deleted_at']

    def validate_name(self, value):
        if TypePost.objects.filter(name=value).exists():
            raise serializers.ValidationError("Ya existe un tipo de post con este nombre.")
        return value

    def create(self, validated_data):
        return TypePost.objects.create(**validated_data)
    
#-----------------------------------------------------------------------------------------------------
# Estados de pedido
#-----------------------------------------------------------------------------------------------------
    
class OrderStatusesSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderStatuses 
        fields = ['id', 
                  'name', 
                  'description', 
                  'created_at',
                  'updated_at',
                  'deleted_at']

    def validate_name(self, value):
        if OrderStatuses.objects.filter(name=value).exists():
            raise serializers.ValidationError("Ya existe un estado de pedido con este nombre.")
        return value

    def create(self, validated_data):
        return OrderStatuses.objects.create(**validated_data)
    
#-----------------------------------------------------------------------------------------------------
# Generos
#-----------------------------------------------------------------------------------------------------
    
class GenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gender 
        fields = ['id', 
                  'name', 
                  'description', 
                  'created_at',
                  'updated_at',
                  'deleted_at']

    def validate_name(self, value):
        if Gender.objects.filter(name=value).exists():
            raise serializers.ValidationError("Ya existe un estado de pedido con este nombre.")
        return value

    def create(self, validated_data):
        return Gender.objects.create(**validated_data)
    
#-----------------------------------------------------------------------------------------------------
# Tipo de persona
#-----------------------------------------------------------------------------------------------------
    
class TypePersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypePerson 
        fields = ['id', 
                  'name', 
                  'description', 
                  'created_at',
                  'updated_at',
                  'deleted_at']

    def validate_name(self, value):
        if TypePerson.objects.filter(name=value).exists():
            raise serializers.ValidationError("Ya existe un tipo de persona con este nombre.")
        return value

    def create(self, validated_data):
        return TypePerson.objects.create(**validated_data)
    
#-----------------------------------------------------------------------------------------------------
# Actividades
#-----------------------------------------------------------------------------------------------------

class ActivitySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True) 
    
    def create(self, validated_data):
        user_id = validated_data.pop('user_id')
        activity = super().create(validated_data)
        user = User.objects.get(pk=user_id)
        activity.user = user
        activity.save()
        return activity

    class Meta:
        model = Activity
        fields = ['id',  
                  'name', 
                  'description', 
                  'place',
                  'user_id',
                  'created_at',
                  'updated_at',
                  'deleted_at',  
                  'user',
                    ]
        

#-----------------------------------------------------------------------------------------------------
# Beneficiados
#-----------------------------------------------------------------------------------------------------

class BenefitedSerializer(serializers.ModelSerializer):
    type_person = TypePersonSerializer(read_only=True)
    type_person_id = serializers.PrimaryKeyRelatedField(queryset=TypePerson.objects.all(), write_only=True)
    activity =ActivitySerializer(read_only=True)
    activity_id = serializers.PrimaryKeyRelatedField(queryset=Activity.objects.all(), write_only=True)
    gender = GenderSerializer(read_only=True)
    gender_id = serializers.PrimaryKeyRelatedField(queryset= Gender.objects.all(), write_only=True)
    class Meta:
        model = Benefited
        fields = ['id', 
                  'type_person_id', 
                  'activity_id', 
                  'gender_id', 
                  'quantity', 
                  'observation', 
                  'created_at',
                  'updated_at',
                  'deleted_at',
                  'type_person', 
                  'activity', 
                  'gender', 
                  ]

    def validate_quantity(self, value):
        if value < 0:
            raise serializers.ValidationError("La cantidad debe ser un número positivo.")
        return value

    def create(self, validated_data):
        type_person_id = validated_data.pop('type_person_id', None)
        activity_id = validated_data.pop('activity_id', None)
        gender_id = validated_data.pop('gender_id', None)

        benefited = Benefited.objects.create(**validated_data)

        if type_person_id:
            benefited.type_person = type_person_id
        if activity_id:
            benefited.activity = activity_id
        if gender_id:
            benefited.gender = gender_id

        benefited.save()
        return benefited

#-----------------------------------------------------------------------------------------------------
# Productos
#-----------------------------------------------------------------------------------------------------

class ProductSerializer(serializers.ModelSerializer):
    unit = UnitSerializer(read_only=True)
    unit_id = serializers.PrimaryKeyRelatedField(queryset=Unit.objects.all(), write_only=True)
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), write_only=True)
    
    class Meta:
        model = Product
        fields = ['id',
                  'name',
                  'description',
                  'unit_id',
                  'category_id',
                  'unit',
                  'category',
                  ]
        
    def validate_quantity(self, value):
        if value < 0:
            raise serializers.ValidationError("La cantidad debe ser un número positivo.")
        return value

    def create(self, validated_data):
        unit_id = validated_data.pop('unit_id', None)
        category_id = validated_data.pop('category_id', None)

        product = Product.objects.create(**validated_data)

        if unit_id:
            product.unit = unit_id
        if category_id:
            product.category = category_id

        product.save()
        return product
        
#-----------------------------------------------------------------------------------------------------
# Actividades mostrar beneficiados
#-----------------------------------------------------------------------------------------------------

class ActivityIndexSerializer(serializers.ModelSerializer):
    benefited = BenefitedSerializer(many=True, read_only=True)
    user = UserSerializer(read_only=True)
    user_id = UserSerializer(write_only=True) 

    class Meta:
        model = Activity
        fields = ['id',  
                  'name', 
                  'description', 
                  'place',
                  'user_id',
                  'created_at',
                  'updated_at',
                  'deleted_at',  
                  'user',
                  'benefited'
                ]

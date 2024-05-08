from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin, Permission
from django.utils import timezone
from simple_history.models import HistoricalRecords
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from .mixins import StoresFileMixin
#-----------------------------------------------------------------------------------------------------
# País 
#-----------------------------------------------------------------------------------------------------

class Country(models.Model):
    name = models.CharField(max_length=255)
    abbreviation = models.CharField(max_length=10, blank=True, null=True)
    dialing_code = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField('Fecha de creación', auto_now_add=True)
    updated_at = models.DateTimeField('Fecha de actualización', auto_now=True)
    deleted_at = models.DateTimeField('Fecha de eliminación', blank=True, null=True)

    class Meta:
        db_table = 'countries' 
        verbose_name = 'País'
        verbose_name_plural = 'Países'

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        self.deleted_at = timezone.now()
        self.save()

    def restore(self, *args, **kwargs):
        self.deleted_at = None
        self.save()
        
#-----------------------------------------------------------------------------------------------------
# Rol
#-----------------------------------------------------------------------------------------------------

class Role(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    permissions = models.ManyToManyField(Permission, through='RolePermission')
    created_at = models.DateTimeField('Fecha de creación', auto_now_add=True)
    updated_at = models.DateTimeField('Fecha de actualización', auto_now=True)
    deleted_at = models.DateTimeField('Fecha de eliminación', blank=True, null=True)
    
    class Meta:
        db_table = 'roles' 
        verbose_name = 'Rol'
        verbose_name_plural = 'Roles'

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        self.deleted_at = timezone.now()
        self.save()

    def restore(self, *args, **kwargs):
        self.deleted_at = None
        self.save()

#-----------------------------------------------------------------------------------------------------
# Super Usuario 
#-----------------------------------------------------------------------------------------------------

class UserManager(BaseUserManager):
    def _create_user(self, username, email, name, last_name, password, is_staff, is_superuser, **extra_fields):
        user = self.model(
            username=username,
            email=email,
            name=name,
            last_name=last_name,
            is_staff=is_staff,
            is_superuser=is_superuser,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_user(self, username, email, name, last_name, password=None, **extra_fields):
        return self._create_user(username, email, name, last_name, password, False, False, **extra_fields)

    def create_superuser(self, username, email, name, last_name, password=None, **extra_fields):
        extra_fields.setdefault('role_id', 1)
        return self._create_user(username, email, name, last_name, password, True, True, **extra_fields)

#-----------------------------------------------------------------------------------------------------
# Usuario 
#-----------------------------------------------------------------------------------------------------

class User(AbstractBaseUser, PermissionsMixin, StoresFileMixin):
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    email = models.EmailField('Correo Electrónico', max_length=255, unique=True)
    is_email_verified = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=6, blank=True, null=True)
    name = models.CharField('Nombres', max_length=255, blank=True, null=True)
    last_name = models.CharField('Apellidos', max_length=255, blank=True, null=True)
    phone_number = models.CharField('Número de teléfono', max_length=255, unique=True)
    birthdate = models.DateField('Fecha de nacimiento', blank=True, null=True) 
    address = models.CharField('Dirección', max_length=255, blank=True, null=True)
    country = models.ForeignKey(Country, on_delete=models.PROTECT, null=True, related_name='users')
    role = models.ForeignKey(Role, on_delete=models.PROTECT, null=True, related_name='users')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    historical = HistoricalRecords()
    created_at = models.DateTimeField('Fecha de creación', auto_now_add=True)
    updated_at = models.DateTimeField('Fecha de actualización', auto_now=True)
    deleted_at = models.DateTimeField('Fecha de eliminación', blank=True, null=True)
    objects = UserManager()
    
    files = GenericRelation('File', related_query_name='user')

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'name', 'last_name']

    class Meta:
        db_table = 'users' 
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return f'{self.name} {self.last_name}'

    def delete(self, *args, **kwargs):
        self.deleted_at = timezone.now()
        self.save()

    def restore(self, *args, **kwargs):
        self.deleted_at = None
        self.save()
        
    def upload_photo(self, photo_file, image_type):
        if image_type not in ['perfil', 'portada']:
            raise ValueError("El tipo de imagen debe ser 'perfil' o 'portada'")
        
        if image_type == 'perfil':
            destination_path = 'user_photos/perfil/'
        else:
            destination_path = 'user_photos/portada/'

        # Guarda la foto utilizando el mixin
        stored_info = self.store_file(file=photo_file, destination_path=destination_path)
        # Crea y guarda un registro en la base de datos
        File.objects.create(
            fileable_type=ContentType.objects.get_for_model(self),
            fileable_id=self.id,
            path=stored_info[0],
            extension=stored_info[1],
            size=stored_info[2]
        )

#-----------------------------------------------------------------------------------------------------
# Estado
#-----------------------------------------------------------------------------------------------------

class Status(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField('Fecha de creación', auto_now_add=True)
    updated_at = models.DateTimeField('Fecha de actualización', auto_now=True)
    deleted_at = models.DateTimeField('Fecha de eliminación', blank=True, null=True)

    class Meta:
        db_table = 'statuses'
        verbose_name = 'Estado'
        verbose_name_plural = 'Estados'

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        self.deleted_at = timezone.now()
        self.save()

    def restore(self, *args, **kwargs):
        self.deleted_at = None
        self.save()

#-----------------------------------------------------------------------------------------------------
# Categoria
#-----------------------------------------------------------------------------------------------------

class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField('Fecha de creación', auto_now_add=True)
    updated_at = models.DateTimeField('Fecha de actualización', auto_now=True)
    deleted_at = models.DateTimeField('Fecha de eliminación', blank=True, null=True)

    class Meta:
        db_table = 'categories'
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        self.deleted_at = timezone.now()
        self.save()

    def restore(self, *args, **kwargs):
        self.deleted_at = None
        self.save()

#-----------------------------------------------------------------------------------------------------
# Unidades de medida
#-----------------------------------------------------------------------------------------------------

class Unit(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField('Fecha de creación', auto_now_add=True)
    updated_at = models.DateTimeField('Fecha de actualización', auto_now=True)
    deleted_at = models.DateTimeField('Fecha de eliminación', blank=True, null=True)

    class Meta:
        db_table = 'units'
        verbose_name = 'Unidad'
        verbose_name_plural = 'Unidades'

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        self.deleted_at = timezone.now()
        self.save()

    def restore(self, *args, **kwargs):
        self.deleted_at = None
        self.save()

#-----------------------------------------------------------------------------------------------------
# Tipo de publicacion
#-----------------------------------------------------------------------------------------------------

class TypePost(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField('Fecha de creación', auto_now_add=True)
    updated_at = models.DateTimeField('Fecha de actualización', auto_now=True)
    deleted_at = models.DateTimeField('Fecha de eliminación', blank=True, null=True)

    class Meta:
        db_table = 'type_posts'
        verbose_name = 'Tipo de publicacion'
        verbose_name_plural = 'Tipo de publicaciones'

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        self.deleted_at = timezone.now()
        self.save()

    def restore(self, *args, **kwargs):
        self.deleted_at = None
        self.save()

#-----------------------------------------------------------------------------------------------------
# Roles y Permisos
#-----------------------------------------------------------------------------------------------------
       
class RolePermission(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)

    class Meta:
        db_table = 'role_has_permissions' 
        unique_together = ('role', 'permission')
        
#-----------------------------------------------------------------------------------------------------
# Archivos
#-----------------------------------------------------------------------------------------------------

class File(models.Model):
    fileable_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    fileable_id = models.PositiveIntegerField()
    fileable = GenericForeignKey('fileable_type', 'fileable_id')
    path = models.CharField(max_length=255)
    extension = models.CharField(max_length=10)
    size = models.CharField(max_length=20)
    type = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField('Fecha de creación', auto_now_add=True)
    updated_at = models.DateTimeField('Fecha de actualización', auto_now=True)
    deleted_at = models.DateTimeField('Fecha de eliminación', blank=True, null=True)
    
    class Meta:
        db_table = 'files'
        verbose_name = 'Archivo'
        verbose_name_plural = 'Archivos'
        
    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        self.deleted_at = timezone.now()
        self.save()

    def restore(self, *args, **kwargs):
        self.deleted_at = None
        self.save()

#-----------------------------------------------------------------------------------------------------
# Estados de pedido
#-----------------------------------------------------------------------------------------------------

class OrderStatuses(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField('Fecha de creación', auto_now_add=True)
    updated_at = models.DateTimeField('Fecha de actualización', auto_now=True)
    deleted_at = models.DateTimeField('Fecha de eliminación', blank=True, null=True)

    class Meta:
        db_table = 'order_statuses'
        verbose_name = 'Estado de pedido'
        verbose_name_plural = 'Estado de pedidos'

    def _str_(self):
        return self.name

    def delete(self, *args, **kwargs):
        self.deleted_at = timezone.now()
        self.save()

    def restore(self, *args, **kwargs):
        self.deleted_at = None
        self.save()

#-----------------------------------------------------------------------------------------------------
# Genero
#-----------------------------------------------------------------------------------------------------

class Gender(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField('Fecha de creación', auto_now_add=True)
    updated_at = models.DateTimeField('Fecha de actualización', auto_now=True)
    deleted_at = models.DateTimeField('Fecha de eliminación', blank=True, null=True)

    class Meta:
        db_table = 'genders'
        verbose_name = 'Genero'
        verbose_name_plural = 'Generos'

    def _str_(self):
        return self.name

    def delete(self, *args, **kwargs):
        self.deleted_at = timezone.now()
        self.save()

    def restore(self, *args, **kwargs):
        self.deleted_at = None
        self.save()

#-----------------------------------------------------------------------------------------------------
# Tipo de persona
#-----------------------------------------------------------------------------------------------------

class TypePerson(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField('Fecha de creación', auto_now_add=True)
    updated_at = models.DateTimeField('Fecha de actualización', auto_now=True)
    deleted_at = models.DateTimeField('Fecha de eliminación', blank=True, null=True)

    class Meta:
        db_table = 'type_persons'
        verbose_name = 'Tipo de persona'
        verbose_name_plural = 'Tipo de persona'

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        self.deleted_at = timezone.now()
        self.save()

    def restore(self, *args, **kwargs):
        self.deleted_at = None
        self.save()

#-----------------------------------------------------------------------------------------------------
# Actividad
#-----------------------------------------------------------------------------------------------------

class Activity(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    place = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, related_name='activities')
    created_at = models.DateTimeField('Fecha de creación', auto_now_add=True)
    updated_at = models.DateTimeField('Fecha de actualización', auto_now=True)
    deleted_at = models.DateTimeField('Fecha de eliminación', blank=True, null=True)

    class Meta:
        db_table = 'activities'
        verbose_name = 'Actividad'
        verbose_name_plural = 'Actividades'

    def _str_(self):
        return self.name

    def delete(self, *args, **kwargs):
        self.deleted_at = timezone.now()
        self.save()

    def restore(self, *args, **kwargs):
        self.deleted_at = None
        self.save()

#-----------------------------------------------------------------------------------------------------
# Beneficiados
#-----------------------------------------------------------------------------------------------------

class Benefited(models.Model):
    type_person = models.ForeignKey(TypePerson, on_delete=models.PROTECT, null=True)
    activity = models.ForeignKey(Activity, on_delete=models.PROTECT, null=True)
    gender = models.ForeignKey(Gender, on_delete=models.PROTECT, null=True)
    quantity = models.IntegerField()
    observation = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField('Fecha de creación', auto_now_add=True)
    updated_at = models.DateTimeField('Fecha de actualización', auto_now=True)
    deleted_at = models.DateTimeField('Fecha de eliminación', blank=True, null=True)

    class Meta:
        db_table = 'benefiteds'
        verbose_name = 'Beneficiado'
        verbose_name_plural = 'Beneficiados'

    def _str_(self):
        return self.name

    def delete(self, *args, **kwargs):
        self.deleted_at = timezone.now()
        self.save()

    def restore(self, *args, **kwargs):
        self.deleted_at = None
        self.save()

#-----------------------------------------------------------------------------------------------------
# Producto
#-----------------------------------------------------------------------------------------------------
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT, null=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True)
    created_at = models.DateTimeField('Fecha de creación', auto_now_add=True)
    updated_at = models.DateTimeField('Fecha de actualización', auto_now=True)
    deleted_at = models.DateTimeField('Fecha de eliminación', blank=True, null=True)

    class Meta:
        db_table = 'pruducts'
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'

    def _str_(self):
        return self.name

    def delete(self, *args, **kwargs):
        self.deleted_at = timezone.now()
        self.save()

    def restore(self, *args, **kwargs):
        self.deleted_at = None
        self.save()
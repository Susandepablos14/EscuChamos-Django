import django_filters
from .models import *
#-----------------------------------------------------------------------------------------------------
# Filtro usuarios
#-----------------------------------------------------------------------------------------------------

class UserFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(lookup_expr='icontains')
    email = django_filters.CharFilter(lookup_expr='icontains')
    name = django_filters.CharFilter(lookup_expr='icontains')
    last_name = django_filters.CharFilter(lookup_expr='icontains')
    role_id = django_filters.NumberFilter(field_name='role__id') 
    document = django_filters.CharFilter(lookup_expr='icontains')
    address = django_filters.CharFilter(lookup_expr='icontains')
    phone_number = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
            model = User
            fields = [
                    'username', 
                    'email', 
                    'name', 
                    'last_name', 
                    'role_id',
                    'address',
                    'phone_number', ]
            
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.filters:
            if 'icontains' in self.filters[field_name].lookup_expr:
                self.filters[field_name].lookup_expr = 'icontains' 
                self.filters[field_name].label = f'{self.filters[field_name].label} (similarity)'
        
#-----------------------------------------------------------------------------------------------------
# Filtro roles
#-----------------------------------------------------------------------------------------------------

class RoleFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    description = django_filters.CharFilter(lookup_expr='icontains')


    class Meta:
            model = Role
            fields = [ 
                    'name', 
                    'description',  ]
            
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.filters:
            if 'icontains' in self.filters[field_name].lookup_expr:
                self.filters[field_name].lookup_expr = 'icontains' 
                self.filters[field_name].label = f'{self.filters[field_name].label} (similarity)'        

#-----------------------------------------------------------------------------------------------------
# Filtro paises
#----------------------------------------------------------------------------------------------------- 

class CountryFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    abbreviation = django_filters.CharFilter(lookup_expr='icontains')
    dialing_code = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
            model = User
            fields = [
                    'name', 
                    'abbreviation', 
                    'dialing_code', 
                     ]
            
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.filters:
            if 'icontains' in self.filters[field_name].lookup_expr:
                self.filters[field_name].lookup_expr = 'icontains' 
                self.filters[field_name].label = f'{self.filters[field_name].label} (similarity)'

#-----------------------------------------------------------------------------------------------------
# Filtro estados
#-----------------------------------------------------------------------------------------------------

class StatusFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    description = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Status
        fields = ['name', 'description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.filters:
            if 'icontains' in self.filters[field_name].lookup_expr:
                self.filters[field_name].lookup_expr = 'icontains'
                self.filters[field_name].label = f'{self.filters[field_name].label} (similarity)'

#-----------------------------------------------------------------------------------------------------
# Filtro categoria
#-----------------------------------------------------------------------------------------------------

class CategoryFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    description = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Category
        fields = [
            'name',
            'description',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.filters:
            if 'icontains' in self.filters[field_name].lookup_expr:
                self.filters[field_name].lookup_expr = 'icontains'
                self.filters[field_name].label = f'{self.filters[field_name].label} (similarity)'
            
#-----------------------------------------------------------------------------------------------------
# Filtro unidades de medida
#-----------------------------------------------------------------------------------------------------

class UnitFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    description = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Unit
        fields = [
            'name',
            'description',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.filters:
            if 'icontains' in self.filters[field_name].lookup_expr:
                self.filters[field_name].lookup_expr = 'icontains'
                self.filters[field_name].label = f'{self.filters[field_name].label} (similarity)'
#-----------------------------------------------------------------------------------------------------
# Filtro tipo de publicacion
#-----------------------------------------------------------------------------------------------------

class TypePostFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    description = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Unit
        fields = [
            'name',
            'description',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.filters:
            if 'icontains' in self.filters[field_name].lookup_expr:
                self.filters[field_name].lookup_expr = 'icontains'
                self.filters[field_name].label = f'{self.filters[field_name].label} (similarity)'

#-----------------------------------------------------------------------------------------------------
# Filtro Estados de pedido
#-----------------------------------------------------------------------------------------------------

class OrderStatusesFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    description = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Unit
        fields = [
            'name',
            'description',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.filters:
            if 'icontains' in self.filters[field_name].lookup_expr:
                self.filters[field_name].lookup_expr = 'icontains'
                self.filters[field_name].label = f'{self.filters[field_name].label} (similarity)'
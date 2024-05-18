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
    role_id = django_filters.NumberFilter() 
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

class OrderStatusFilter(django_filters.FilterSet):
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
# Filtro genero
#-----------------------------------------------------------------------------------------------------

class GenderFilter(django_filters.FilterSet):
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
# Filtro tipo de persona
#-----------------------------------------------------------------------------------------------------

class TypePersonFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    description = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = TypePerson
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
# Filtro actividades
#-----------------------------------------------------------------------------------------------------

class ActivityFilter (django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    description = django_filters.CharFilter(lookup_expr='icontains')
    place = django_filters.CharFilter(lookup_expr='icontains')
    user_id = django_filters.NumberFilter() 

    class Meta:
        model = Activity
        fields = [
            'name',
            'description',
            'place',
            'user_id'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.filters:
            if 'icontains' in self.filters[field_name].lookup_expr:
                self.filters[field_name].lookup_expr = 'icontains'
                self.filters[field_name].label = f'{self.filters[field_name].label} (similarity)'

#-----------------------------------------------------------------------------------------------------
# Filtro beneficiados
#-----------------------------------------------------------------------------------------------------

class BenefitedFilter(django_filters.FilterSet):
    quantity = django_filters.NumberFilter()
    activity_id = django_filters.NumberFilter() 
    gender_id = django_filters.NumberFilter() 
    type_person_id = django_filters.NumberFilter() 
    observation = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Benefited
        fields = [
            'quantity',
            'activity_id',
            'gender_id',
            'type_person_id',
            'observation',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.filters:
            if 'icontains' in self.filters[field_name].lookup_expr:
                self.filters[field_name].lookup_expr = 'icontains'
                self.filters[field_name].label = f'{self.filters[field_name].label} (similarity)'

#-----------------------------------------------------------------------------------------------------
# Filtro Productos
#-----------------------------------------------------------------------------------------------------
class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    description = django_filters.CharFilter(lookup_expr='icontains')
    unit_id = django_filters.NumberFilter()
    category_id = django_filters.NumberFilter()

    class Meta:
        model = Product
        fields = [
            'name',
            'description',
            'unit_id',
            'category_id',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.filters:
            if 'icontains' in self.filters[field_name].lookup_expr:
                self.filters[field_name].lookup_expr = 'icontains'
                self.filters[field_name].label = f'{self.filters[field_name].label} (similarity)'

#-----------------------------------------------------------------------------------------------------
# Filtro Inventario
#-----------------------------------------------------------------------------------------------------

class InventoryFilter(django_filters.FilterSet):
    quantity = django_filters.NumberFilter()
    inventory_id = django_filters.NumberFilter()
    user_id = django_filters.NumberFilter()

    class Meta:
        model = Inventory
        fields = [
            'quantity',
            'inventory_id',
            'user_id'
        ]

#-----------------------------------------------------------------------------------------------------
# Filtro Entradas
#-----------------------------------------------------------------------------------------------------

class InputFilter(django_filters.FilterSet):
    user_id = django_filters.NumberFilter()
    inventory_id = django_filters.NumberFilter()
    quantity = django_filters.NumberFilter()
    date = django_filters.DateFilter(lookup_expr='date')

    class Meta:
        model = Input
        fields = [
                  'user_id', 
                  'inventory_id', 
                  'quantity', 
                  'date',
        ]

#-----------------------------------------------------------------------------------------------------
# Filtro Recipes
#-----------------------------------------------------------------------------------------------------

class OrderFilter(django_filters.FilterSet):
    user_id = django_filters.NumberFilter()
    inventory_id = django_filters.NumberFilter()
    quantity = django_filters.NumberFilter()
    date = django_filters.DateFilter(lookup_expr='date')
    order_status_id = django_filters.NumberFilter()

    class Meta:
        model = Order
        fields = [
            'user_id', 
            'inventory_id', 
            'quantity', 
            'date',
            'order_status_id'
        ]
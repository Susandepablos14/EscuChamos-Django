from django.core.management.base import BaseCommand
from escuchamos.models import *

class Command(BaseCommand):
    help = 'Sembrar datos en modelos de la aplicación'

    def handle(self, *args, **options):
        self.seed_countries()
        self.seed_roles()
        self.seed_statuses()
        self.seed_units()
        self.seed_genders()
        self.seed_type_persons()

    def seed_countries(self):
        countries = [
            {'name': 'Antigua and Barbuda', 'abbreviation': 'ATG', 'dialing_code': '+1-268'},
            {'name': 'Argentina', 'abbreviation': 'ARG', 'dialing_code': '+54'},
            {'name': 'Bahamas', 'abbreviation': 'BHS', 'dialing_code': '+1-242'},
            {'name': 'Barbados', 'abbreviation': 'BRB', 'dialing_code': '+1-246'},
            {'name': 'Belice', 'abbreviation': 'BLZ', 'dialing_code': '+501'},
            {'name': 'Bolivia', 'abbreviation': 'BOL', 'dialing_code': '+591'},
            {'name': 'Brasil', 'abbreviation': 'BRA', 'dialing_code': '+55'},
            {'name': 'Canadá', 'abbreviation': 'CAN', 'dialing_code': '+1'},
            {'name': 'Chile', 'abbreviation': 'CHL', 'dialing_code': '+56'},
            {'name': 'Colombia', 'abbreviation': 'COL', 'dialing_code': '+57'},
            {'name': 'Costa Rica', 'abbreviation': 'CRI', 'dialing_code': '+506'},
            {'name': 'Cuba', 'abbreviation': 'CUB', 'dialing_code': '+53'},
            {'name': 'Dominica', 'abbreviation': 'DMA', 'dialing_code': '+1-767'},
            {'name': 'República Dominicana', 'abbreviation': 'DOM', 'dialing_code': '+1-809'},
            {'name': 'Ecuador', 'abbreviation': 'ECU', 'dialing_code': '+593'},
            {'name': 'El Salvador', 'abbreviation': 'SLV', 'dialing_code': '+503'},
            {'name': 'Granada', 'abbreviation': 'GRD', 'dialing_code': '+1-473'},
            {'name': 'Guatemala', 'abbreviation': 'GTM', 'dialing_code': '+502'},
            {'name': 'Guyana', 'abbreviation': 'GUY', 'dialing_code': '+592'},
            {'name': 'Haití', 'abbreviation': 'HTI', 'dialing_code': '+509'},
            {'name': 'Honduras', 'abbreviation': 'HND', 'dialing_code': '+504'},
            {'name': 'Jamaica', 'abbreviation': 'JAM', 'dialing_code': '+1-876'},
            {'name': 'México', 'abbreviation': 'MEX', 'dialing_code': '+52'},
            {'name': 'Nicaragua', 'abbreviation': 'NIC', 'dialing_code': '+505'},
            {'name': 'Panamá', 'abbreviation': 'PAN', 'dialing_code': '+507'},
            {'name': 'Paraguay', 'abbreviation': 'PRY', 'dialing_code': '+595'},
            {'name': 'Perú', 'abbreviation': 'PER', 'dialing_code': '+51'},
            {'name': 'San Cristóbal y Nieves', 'abbreviation': 'KNA', 'dialing_code': '+1-869'},
            {'name': 'Santa Lucía', 'abbreviation': 'LCA', 'dialing_code': '+1-758'},
            {'name': 'San Vicente y las Granadinas', 'abbreviation': 'VCT', 'dialing_code': '+1-784'},
            {'name': 'Surinam', 'abbreviation': 'SUR', 'dialing_code': '+597'},
            {'name': 'Trinidad y Tobago', 'abbreviation': 'TTO', 'dialing_code': '+1-868'},
            {'name': 'Estados Unidos', 'abbreviation': 'USA', 'dialing_code': '+1'},
            {'name': 'Uruguay', 'abbreviation': 'URY', 'dialing_code': '+598'},
            {'name': 'Venezuela', 'abbreviation': 'VEN', 'dialing_code': '+58'},
        ]
        for country_data in countries:
            Country.objects.get_or_create(**country_data)

    def seed_roles(self):
        roles = [
            ('Administrador', 'Rol para la Asociación'),
            ('Voluntario', 'Rol para Voluntarios'),
            ('Usuario Normal', 'Rol para Usuarios Normales'),
        ]
        for name, description in roles:
            Role.objects.get_or_create(name=name, description=description)

    def seed_statuses(self):
        statuses = [
            ('Activo', 'Estado normal sin infracciones'),
            ('Infracción', 'Estado de infracción por violación de reglas'),
            ('En revisión', 'Estado de revisión pendiente'),
            ('Resuelto', 'Estado de infracción resuelto'),
            ('Bloqueado', 'Estado de contenido bloqueado'),
            ('Reportado', 'Estado de contenido reportado'),
        ]
        for name, description in statuses:
            Status.objects.get_or_create(name=name, description=description)

    def seed_units(self):
        units = [
            {'name': 'Tableta', 'description': 'Una forma de dosificación sólida que generalmente contiene un medicamento, y que está destinada para ser ingerida por vía oral.'},
            {'name': 'Cápsula', 'description': 'Una forma de dosificación sólida que consiste en un envase duro o blando, generalmente de gelatina, que contiene medicamento en forma de polvo, líquido o gránulos.'},
            {'name': 'Miligramo', 'description': 'Es una unidad de medida de masa que equivale a una milésima parte de un gramo'},
            {'name': 'Microgramo', 'description': 'Es una unidad de medida de masa que equivale a una millonésima parte de un gramo'},
            {'name': 'Unidad Internacional', 'description': 'Una unidad de medida estandarizada para expresar la cantidad de una sustancia biológicamente activa'},
            {'name': 'Mililitro', 'description': 'Es una unidad de medida de volumen que equivale a una milésima parte de un litro'},
            {'name': 'Gotas', 'description': 'Pequeñas cantidades de líquido que se administran usando un gotero.'},
        ]
        for unit_data in units:
            Unit.objects.get_or_create(**unit_data)
    
    def seed_genders(self):
        genders = [
            {'name': 'Masculino', 'description': 'Género masculino.'},
            {'name': 'Femenino', 'description': 'Género femenino.'},
            {'name': 'Otro', 'description': 'Otros géneros.'},
        ]
        for gender_data in genders:
            Gender.objects.get_or_create(**gender_data)

    def seed_type_persons(self):
        types = [
            {'name': 'Niño', 'description': 'Persona en edad infantil.'},
            {'name': 'Adolescente', 'description': 'Persona en edad adolescente.'},
            {'name': 'Adulto', 'description': 'Persona en edad adulta.'},
            {'name': 'Adulto mayor', 'description': 'Persona en edad avanzada.'},
            {'name': 'Discapacidad', 'description': 'Persona con alguna discapacidad.'},
            {'name': 'Embarazada', 'description': 'Mujer en estado de embarazo.'},
            {'name': 'Estudiante', 'description': 'Persona que está estudiando.'},
            {'name': 'Trabajador', 'description': 'Persona que trabaja regularmente.'},
            {'name': 'Desempleado', 'description': 'Persona que está desempleada.'},
            {'name': 'Indígena', 'description': 'Persona perteneciente a una comunidad indígena.'},
        ]
        for type_data in types:
            TypePerson.objects.get_or_create(**type_data)


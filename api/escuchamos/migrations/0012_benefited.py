# Generated by Django 5.0.3 on 2024-05-07 01:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('escuchamos', '0011_activity'),
    ]

    operations = [
        migrations.CreateModel(
            name='Benefited',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')),
                ('deleted_at', models.DateTimeField(blank=True, null=True, verbose_name='Fecha de eliminación')),
                ('activity', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='escuchamos.activity')),
                ('gender', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='escuchamos.gender')),
                ('type_person', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='escuchamos.typeperson')),
            ],
            options={
                'verbose_name': 'Beneficiado',
                'verbose_name_plural': 'Beneficiados',
                'db_table': 'benefiteds',
            },
        ),
    ]

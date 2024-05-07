# Generated by Django 5.0.3 on 2024-05-06 23:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('escuchamos', '0009_gender'),
    ]

    operations = [
        migrations.CreateModel(
            name='TypePerson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')),
                ('deleted_at', models.DateTimeField(blank=True, null=True, verbose_name='Fecha de eliminación')),
            ],
            options={
                'verbose_name': 'Tipo de persona',
                'verbose_name_plural': 'Tipo de persona',
                'db_table': 'type_persons',
            },
        ),
    ]
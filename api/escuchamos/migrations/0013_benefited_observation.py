# Generated by Django 5.0.3 on 2024-05-07 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('escuchamos', '0012_benefited'),
    ]

    operations = [
        migrations.AddField(
            model_name='benefited',
            name='observation',
            field=models.TextField(blank=True, null=True),
        ),
    ]

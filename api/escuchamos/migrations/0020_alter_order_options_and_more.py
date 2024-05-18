# Generated by Django 5.0.3 on 2024-05-09 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('escuchamos', '0019_remove_order_description'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'verbose_name': 'Pedido', 'verbose_name_plural': 'Pedidos'},
        ),
        migrations.RenameField(
            model_name='order',
            old_name='orderstatuses',
            new_name='order_status',
        ),
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Fecha del pedido'),
        ),
    ]

# Generated by Django 5.1.5 on 2025-02-27 19:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_product_is_rentable'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='is_available',
        ),
    ]

# Generated by Django 4.2.2 on 2023-11-30 13:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_alter_product_poster'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='rate',
        ),
        migrations.RemoveField(
            model_name='seller',
            name='rate',
        ),
    ]
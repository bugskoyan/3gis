# Generated by Django 4.2.2 on 2023-12-18 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_remove_product_rate_remove_seller_rate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productcomment',
            name='user',
            field=models.CharField(max_length=100, verbose_name='пользователь'),
        ),
    ]

# Generated by Django 4.2.2 on 2023-11-24 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_product_rate_seller_rate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='poster',
            field=models.ImageField(blank=True, null=True, upload_to='posters/', verbose_name='постер'),
        ),
    ]

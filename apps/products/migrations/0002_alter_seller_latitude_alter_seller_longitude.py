# Generated by Django 4.2.7 on 2023-11-07 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seller',
            name='latitude',
            field=models.FloatField(verbose_name='широта'),
        ),
        migrations.AlterField(
            model_name='seller',
            name='longitude',
            field=models.FloatField(verbose_name='долгота'),
        ),
    ]

# Generated by Django 3.0.4 on 2020-05-07 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Proformas', '0003_modalite_garantie'),
    ]

    operations = [
        migrations.AddField(
            model_name='commande',
            name='Date_validation',
            field=models.DateField(),
        ),
    ]
# Generated by Django 3.0.4 on 2020-06-09 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Gestion_Achats', '0002_auto_20200512_0037'),
    ]

    operations = [
        migrations.AlterField(
            model_name='association',
            name='Quantite',
            field=models.IntegerField(),
        ),
    ]

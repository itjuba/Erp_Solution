# Generated by Django 3.0.4 on 2020-05-02 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Gestion_Achats', '0004_auto_20200502_1651'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payements',
            name='mode_de_payement',
            field=models.IntegerField(choices=[('Chéck', 'Chéck'), ('espèces', 'Espèces'), ('par virement bancaire', 'Virement')]),
        ),
    ]
# Generated by Django 3.0.4 on 2020-05-28 21:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Transactionb', '0004_auto_20200528_2114'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactionb',
            name='Numero_facture',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='transactionb',
            name='reference',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]

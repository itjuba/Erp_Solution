# Generated by Django 3.0.4 on 2020-05-28 21:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Transactionb', '0003_auto_20200528_2049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactionb',
            name='mode_de_payement',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]

# Generated by Django 3.0.4 on 2020-05-15 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Transactionb',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Date', models.DateField()),
                ('Date_transaction', models.DateField()),
                ('validation', models.CharField(max_length=200)),
                ('E_S', models.CharField(max_length=10)),
                ('mode_de_payement', models.CharField(max_length=200)),
                ('reference', models.IntegerField()),
                ('Montant_HT', models.DecimalField(decimal_places=2, max_digits=10)),
                ('Montant_TVA', models.DecimalField(decimal_places=2, max_digits=10)),
                ('Montant_TTC', models.DecimalField(decimal_places=2, max_digits=10)),
                ('Numero_facture', models.IntegerField()),
                ('Numero_payement', models.IntegerField()),
            ],
        ),
    ]

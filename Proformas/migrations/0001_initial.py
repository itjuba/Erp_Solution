# Generated by Django 3.0.4 on 2020-05-05 22:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Client_Section', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Commande',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Date', models.DateField()),
                ('Numero_commande', models.CharField(max_length=200)),
                ('Montant_HT', models.DecimalField(decimal_places=2, max_digits=10)),
                ('Montant_TVA', models.DecimalField(decimal_places=2, max_digits=10)),
                ('Montant_TTC', models.DecimalField(decimal_places=2, max_digits=10)),
                ('Type_Service', models.CharField(choices=[('Hébergmeent', 'Hébergmeent'), ('Assistance', 'Assistance'), ('Réseau', 'Réseau'), ('Développement', 'Développement'), ('Matérial', 'Matérial')], max_length=200)),
                ('validation', models.BooleanField(default=0)),
                ('Client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Client_Section.Client_Data')),
            ],
        ),
        migrations.CreateModel(
            name='Modalite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modalite_payement', models.TextField(blank=True, default='', null=True)),
                ('Arret_Facture', models.TextField(blank=True, default='', null=True)),
                ('Formation', models.TextField(blank=True, default='', null=True)),
                ('Period_Réalisation', models.TextField(blank=True, default='', null=True)),
                ('Echéancier_payement', models.TextField(blank=True, default='', null=True)),
                ('Command', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='Proformas.Commande')),
            ],
        ),
        migrations.CreateModel(
            name='Commande_Designation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Designation', models.TextField()),
                ('Prix_Unitaire', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('Quantite', models.IntegerField(default=1)),
                ('Montant_HT', models.DecimalField(decimal_places=2, max_digits=10)),
                ('Montant_TVA', models.DecimalField(decimal_places=2, max_digits=10)),
                ('Montant_TTC', models.DecimalField(decimal_places=2, max_digits=10)),
                ('Command', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Proformas.Commande')),
            ],
        ),
    ]

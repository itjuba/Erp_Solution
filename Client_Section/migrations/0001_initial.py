# Generated by Django 3.0.4 on 2020-04-27 13:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client_Data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('RC', models.CharField(max_length=50)),
                ('Raison_social', models.CharField(max_length=254)),
                ('NIF', models.CharField(max_length=50, unique=True)),
                ('AI', models.CharField(max_length=50, unique=True)),
                ('NIS', models.CharField(max_length=50, unique=True)),
                ('Banque', models.CharField(max_length=50, unique=True)),
                ('CB', models.CharField(max_length=50)),
                ('adresse', models.CharField(max_length=50)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Nom', models.CharField(max_length=50)),
                ('post', models.CharField(max_length=50)),
                ('Tel', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('contact_type', models.CharField(default='Client_contact', max_length=50)),
                ('client', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='Client_Section.Client_Data')),
            ],
        ),
    ]

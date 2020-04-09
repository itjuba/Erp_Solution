# Generated by Django 3.0.4 on 2020-04-02 20:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Client_Section', '0003_auto_20200402_1811'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Nom', models.CharField(max_length=50)),
                ('post', models.CharField(max_length=50)),
                ('Tel', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('contact_type', models.CharField(default='Client_contact', max_length=50)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Client_Section.Client_Data')),
            ],
        ),
    ]
# Generated by Django 3.0.8 on 2020-07-29 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Fournis_Section', '0002_auto_20200622_1442'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fournis_data',
            name='adresse',
            field=models.CharField(max_length=150),
        ),
    ]
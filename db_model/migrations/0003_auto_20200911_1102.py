# Generated by Django 3.0.6 on 2020-09-11 08:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('db_model', '0002_cartridgeprice'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='brands',
            options={'managed': False, 'ordering': ['name']},
        ),
    ]

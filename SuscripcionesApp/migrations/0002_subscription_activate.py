# Generated by Django 4.2.1 on 2023-05-22 05:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SuscripcionesApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='activate',
            field=models.BooleanField(default=False),
        ),
    ]
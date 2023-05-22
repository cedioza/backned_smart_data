# Generated by Django 4.2.1 on 2023-05-22 09:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('UsuariosApp', '0003_alter_usuario_correo'),
        ('SuscripcionesApp', '0007_service_api_key_service_url_api'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='service',
            field=models.ForeignKey(db_column='service', on_delete=django.db.models.deletion.CASCADE, to='SuscripcionesApp.service', to_field='name'),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='user',
            field=models.ForeignKey(db_column='user', on_delete=django.db.models.deletion.CASCADE, to='UsuariosApp.usuario', to_field='correo'),
        ),
    ]

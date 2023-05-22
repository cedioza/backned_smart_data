from django.db import models
from UsuariosApp.models import Usuario

class Service(models.Model):
    name = models.CharField(max_length=255, unique=True)
    url_api = models.CharField(max_length=255, default='www')
    api_key = models.CharField(max_length=255, default='None')
    
    # Otros campos relevantes para la gestión de servicios

    def __str__(self):
        return self.name
    

class Subscription(models.Model):
    user = models.ForeignKey(Usuario, on_delete=models.CASCADE, to_field='correo', db_column='user')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, to_field='name', db_column='service')
    activate = models.BooleanField(default=True)
    # Otros campos relevantes para la gestión de suscripciones

    def __str__(self):
        return f"{self.user} - {self.service}"
    
    class Meta:
        unique_together = ('user', 'service')
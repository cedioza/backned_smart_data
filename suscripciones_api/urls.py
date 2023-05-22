"""
URL configuration for suscripciones_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path ,include
from rest_framework.routers import DefaultRouter
from UsuariosApp.views import UsuarioViewSet
from SuscripcionesApp.views import SubscriptionViewSet , ServiceViewSet


# Crea una instancia de DefaultRouter
router = DefaultRouter()

# Registra las vistas de cada aplicación en el router
router.register('usuarios', UsuarioViewSet)
router.register('subscripciones', SubscriptionViewSet)
router.register('servicios', ServiceViewSet)



# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('api/', include('UsuariosApp.urls')),
#     path('api/', include('SuscripcionesApp.urls')),
# ]

urlpatterns = [
    # Ruta raíz del API
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]
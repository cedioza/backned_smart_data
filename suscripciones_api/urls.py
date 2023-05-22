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
from SuscripcionesApp.views import SubscriptionViewSet , ServiceViewSet,SubscriptionByUserViewSet  ,consumir ,suscribir, desuscribir
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Crea una instancia de DefaultRouter
router = DefaultRouter()

# Registra las vistas de cada aplicación en el router

router.register('usuarios', UsuarioViewSet)
router.register('suscripciones', SubscriptionViewSet)
router.register('servicios', ServiceViewSet)




# urlpatterns = [
#     # Ruta raíz del API
#     path('admin/', admin.site.urls),
#     path('api/', include(router.urls)),
#     path('consumir/', prueba, name='prueba'),
#     path('suscribir/', suscribir, name='suscribir'),
#     path('desuscribir/', desuscribir, name='suscribir'),

# ]


schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation",
        default_version='v1',
        description="Your API description",
        terms_of_service="https://www.example.com/policies/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
)

urlpatterns = [
    # ... otras rutas de URL de tu aplicación ...
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('consumir/', consumir, name='prueba'),
    path('suscribir/', suscribir, name='suscribir'),
    path('desuscribir/', desuscribir, name='suscribir'),
    path('api/suscripciones_por_correo/<str:correo>/', SubscriptionByUserViewSet.as_view({'get': 'list'}), name='subscription-by-user'),
]
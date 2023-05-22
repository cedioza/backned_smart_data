from django.urls import include, path
from rest_framework import routers
from .views import ServiceViewSet, SubscriptionViewSet 
router = routers.DefaultRouter()
router.register(r'servicios', ServiceViewSet)
router.register(r'subscripcion', SubscriptionViewSet)


urlpatterns = [
    path('', include(router.urls)),
]

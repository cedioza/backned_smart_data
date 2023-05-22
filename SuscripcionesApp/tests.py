from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Service, Subscription
from .serializers import ServiceSerializer, SubscriptionSerializer
from django.test import TestCase
from rest_framework.test import APIRequestFactory
from .views import SubscriptionByUserViewSet, desuscribir
from UsuariosApp.models import Usuario
class ServiceViewSetTestCase(APITestCase):
    def setUp(self):
        self.url = reverse('service-list')  # Obtén la URL para crear un servicio
        self.valid_payload = {'name': 'Servicio de ejemplo', 'description': 'Descripción del servicio'}

    def test_create_service(self):
        response = self.client.post(self.url, self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verifica si el servicio se creó correctamente en la base de datos
        service = Service.objects.get(pk=response.data['id'])
        self.assertEqual(service.name, self.valid_payload['name'])
        
        # Verifica si la respuesta contiene los datos del servicio creado
        serializer = ServiceSerializer(instance=service)
        self.assertEqual(response.data, serializer.data)

    def test_create_service_with_invalid_data(self):
        invalid_payload = {'name': '', 'description': 'Descripción del servicio'}
        response = self.client.post(self.url, invalid_payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Verifica si el servicio no se creó en la base de datos
        self.assertFalse(Service.objects.exists())




class SubscriptionByUserViewSetTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.viewset = SubscriptionByUserViewSet()
        self.user = Usuario.objects.create(nombre='John Doe', correo='john@example.com')
        self.service = Service.objects.create(name='Service 1', url_api='www.example.com', api_key='api_key')

    def test_get_queryset(self):
        # Crea una suscripción para el usuario y servicio
        subscription = Subscription.objects.create(user=self.user, service=self.service, activate=True)

        # Crea una solicitud de API con el correo del usuario en los query params
        request = self.factory.get('/subscriptions/', {'correo': self.user.correo})

        # Asigna la solicitud al viewset
        self.viewset.request = request


        # Verifica que el serializer_class sea SubscriptionSerializer
        self.assertEqual(self.viewset.serializer_class, SubscriptionSerializer)

    def test_get_queryset_services(self):
        # Crea un usuario de ejemplo
        user_email = "example@gmail.com"
        user = Usuario.objects.create(correo=user_email)
        service1 = Service.objects.create(name="service1")
        service2 = Service.objects.create(name="service2")

        # Crea suscripciones de ejemplo asociadas al usuario
        subscription1 = Subscription.objects.create(user=user, service=service1, activate=True)
        subscription2 = Subscription.objects.create(user=user, service=service2, activate=True)

        # Mockea el objeto de la vista para obtener el queryset
        self.viewset.kwargs = {'correo': user_email}
        queryset = self.viewset.get_queryset()

        # Verifica que el queryset contenga las suscripciones correctas
        self.assertIn(subscription1, queryset)
        self.assertIn(subscription2, queryset)
        self.assertEqual(len(queryset), 2)


class DesuscribirTestCase(APITestCase):
    def test_desuscribir(self):
        # Crea una suscripción de ejemplo
        user_email = "correo@example.com"
        service_name = "servicio1"
        user = Usuario.objects.create(correo=user_email)
        service1 = Service.objects.create(name="service1")
        suscripcion = Subscription.objects.create(user=user, service=service1, activate=True)

        # Crea una instancia de APIRequestFactory
        factory = APIRequestFactory()

        # Crea una solicitud POST con los datos necesarios
        data = {'correo': user_email, 'servicio': service_name}
        request = factory.post('/desuscribir/', data)

        # Realiza la llamada a la función desuscribir
        response = desuscribir(request)

        # Verifica el código de respuesta y el mensaje esperado
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {'mensaje': 'El correo o servicio no existe para desvincular'})

        # Verifica que la suscripción haya sido actualizada en la base de datos
        suscripcion.refresh_from_db()
        self.assertTrue(suscripcion.activate)

from rest_framework import viewsets ,status
from .models import Service, Subscription
from .serializers import ServiceSerializer, SubscriptionSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests

from UsuariosApp.models import Usuario
from SuscripcionesApp.models import Subscription


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

class SubscriptionByUserViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = SubscriptionSerializer

    def get_queryset(self):
        correo = self.request.query_params.get('user', None)
        if correo:
            queryset = Subscription.objects.filter(user=correo)
            return queryset
        return Subscription.objects.none()

#Suscribir 
@api_view(['POST'])
def suscribir(request):
    correo = request.data.get('correo')
    servicio = request.data.get('servicio')

    try:
        suscripcion = Subscription.objects.get(user__correo=correo, service__name=servicio)
        if suscripcion :
            if suscripcion.activate :
                return Response({'mensaje': 'Ya estas suscrito a este servicio'})
            suscripcion.activate = True
            suscripcion.save()
            serializer = SubscriptionSerializer(suscripcion)
            return Response(serializer.data)
    except Subscription.DoesNotExist:
         return Response({'mensaje': 'El correo o servicio no existe para vincular'}, status=status.HTTP_404_NOT_FOUND)

#Desuscribir
@api_view(['POST'])
def desuscribir(request):
    correo = request.data.get('correo')
    servicio = request.data.get('servicio')
    try:
        suscripcion = Subscription.objects.get(user__correo=correo, service__name=servicio)
        if suscripcion :
            if suscripcion.activate == False :
                return Response({'mensaje': 'Ya estas desuscrito a este servicio'})
            suscripcion.activate = False
            suscripcion.save()
            serializer = SubscriptionSerializer(suscripcion)
            return Response(serializer.data)
    except Subscription.DoesNotExist:
        return Response({'mensaje': 'El correo o servicio no existe para desvincular'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def prueba(request):
    correo = request.data.get('correo')
    servicio = request.data.get('servicio')

    try:
        subscription = Subscription.objects.get(user=correo, service__name=servicio)
        service = Service.objects.get(name=servicio)

        if subscription.activate:
            if service.api_key == 'None':
                response = requests.get(service.url_api)
                print("response",response)
                # La suscripción está activada, puedes consumir el servicio
                # Realizar la llamada a la API externa correspondiente
            else :
                url = service.url_api + service.api_key
                print("url",url)
                response = requests.get(url)

            if response.status_code == 400:
                return Response({'mensaje': 'Url no valida '})
            else :
            # Procesar los datos según tus necesidades
                data = response.json()
            # ...
                return Response({'mensaje': 'Servicio consumido ','data:':data})

        else:
            # La suscripción no está activada
            return Response({'mensaje': 'La suscripción no está activada'})

    except Subscription.DoesNotExist:
        # El usuario no está suscrito al servicio
        return Response({'mensaje': 'No estás suscrito al servicio'}, status=status.HTTP_404_NOT_FOUND)

    except Service.DoesNotExist:
        # El servicio no existe
        return Response({'mensaje': 'El servicio no existe'}, status=status.HTTP_404_NOT_FOUND)

from rest_framework import viewsets ,status
from .models import Service, Subscription
from .serializers import ServiceSerializer, SubscriptionSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


import requests

from UsuariosApp.models import Usuario
from SuscripcionesApp.models import Subscription


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

   
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

@swagger_auto_schema(
    manual_parameters=[
        openapi.Parameter(
            'correo', openapi.IN_QUERY, type=openapi.TYPE_STRING, required=True,
            description='Correo del usuario para filtrar las suscripciones'
        ),
    ],
)
class SubscriptionByUserViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = SubscriptionSerializer
    
    def get_queryset(self):
        correo = self.kwargs['correo']
        queryset = Subscription.objects.filter(user=correo)
        return queryset


@swagger_auto_schema(
    method='post',
    operation_description="Desuscribir a un servicio",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'correo': openapi.Schema(type=openapi.TYPE_STRING, description='Correo del usuario a suscribir'),
            'servicio': openapi.Schema(type=openapi.TYPE_STRING, description='Nombre del servicio al que se desea suscribir')
        },
        required=['correo', 'servicio']
    ),
    responses={
        200: "Desuscripción exitosa",
        404: "No se encontró la suscripción correspondiente al correo y servicio proporcionados"
    },
)
@api_view(['POST'])
def desuscribir(request):

    correo = request.data.get('correo')
    servicio = request.data.get('servicio')
    try:
        suscripcion = Subscription.objects.get(user__correo=correo, service__name=servicio)
        if suscripcion:
            if suscripcion.activate == False:
                return Response({'mensaje': 'Ya estás desuscrito de este servicio'})
            suscripcion.activate = False
            suscripcion.save()
            serializer = SubscriptionSerializer(suscripcion)
            return Response(serializer.data)
    except Subscription.DoesNotExist:
        return Response({'mensaje': 'El correo o servicio no existe para desvincular'}, status=status.HTTP_404_NOT_FOUND)


@swagger_auto_schema(
    method='post',
    operation_description="Consumir un servicio con un correo y servicio",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'correo': openapi.Schema(type=openapi.TYPE_STRING, description='Correo del usuario a consumir'),
            'servicio': openapi.Schema(type=openapi.TYPE_STRING, description='Nombre del servicio al que se desea consumir')
        },
        required=['correo', 'servicio']
    ),
    responses={
        200: "Consumo exitoso",
        404: "No se encontró la suscripción correspondiente al correo y servicio proporcionados"
    },
)
@api_view(['POST'])
def consumir(request):
    correo = request.data.get('correo')
    servicio = request.data.get('servicio')

    try:
        subscription = Subscription.objects.get(user=correo, service__name=servicio)
        service = Service.objects.get(name=servicio)

        if subscription.activate:
            if service.api_key.startswith('api_key'):
                url = service.url_api + service.api_key
                print("url",url)
                response = requests.get(url)

                # La suscripción está activada, puedes consumir el servicio
                # Realizar la llamada a la API externa correspondiente
            else :
                response = requests.get(service.url_api)
                print("response",response)

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


@swagger_auto_schema(
    method='post',
    operation_description="Suscribir a un servicio",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'correo': openapi.Schema(type=openapi.TYPE_STRING, description='Correo del usuario a suscribir'),
            'servicio': openapi.Schema(type=openapi.TYPE_STRING, description='Nombre del servicio al que se desea suscribir')
        },
        required=['correo', 'servicio']
    ),
    responses={
        200: "Suscripción exitosa",
        404: "No se encontró la suscripción correspondiente al correo y servicio proporcionados"
    },
)
@api_view(['POST'])
def suscribir(request):
    """
    Suscribir a un servicio.

    Suscribe un usuario a un servicio específico.

    ---
    parameters:
      - name: correo
        type: string
        required: true
        description: Correo del usuario a suscribir.
      - name: servicio
        type: string
        required: true
        description: Nombre del servicio al que se desea suscribir.

    """
    correo = request.data.get('correo')
    servicio = request.data.get('servicio')

    try:
        suscripcion = Subscription.objects.get(user__correo=correo, service__name=servicio)
        if suscripcion:
            if suscripcion.activate:
                return Response({'mensaje': 'Ya estás suscrito a este servicio'})
            suscripcion.activate = True
            suscripcion.save()
            serializer = SubscriptionSerializer(suscripcion)
            return Response(serializer.data)
    except Subscription.DoesNotExist:
        return Response({'mensaje': 'El correo o servicio no existe para vincular'}, status=status.HTTP_404_NOT_FOUND)

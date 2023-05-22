from django.test import TestCase
from .models import Usuario

class UsuarioTestCase(TestCase):
    def test_crear_usuario(self):
        # Crea un nuevo objeto Usuario
        usuario = Usuario.objects.create(
            nombre='John Doe',
            correo='john@example.com',
            contraseña='password',
            telefono='123456789'
        )

        # Verifica que el objeto Usuario se haya creado correctamente
        self.assertEqual(usuario.nombre, 'John Doe')
        self.assertEqual(usuario.correo, 'john@example.com')
        self.assertEqual(usuario.contraseña, 'password')
        self.assertEqual(usuario.telefono, '123456789')

        # Verifica que el objeto Usuario tenga una fecha de creación y actualización
        self.assertIsNotNone(usuario.fecha_creacion)
        self.assertIsNotNone(usuario.fecha_actualizacion)


from django.test import TestCase
from rest_framework import status
from unittest.mock import Mock
from .models import Usuario
from .serializers import UsuarioSerializer
from .views import UsuarioViewSet

class UsuarioViewSetTestCase(TestCase):
    def setUp(self):
        self.usuario = Usuario.objects.create(nombre='John Doe', correo='john@example.com')
        self.viewset = UsuarioViewSet()

    def test_destroy(self):
        # Crea un objeto mock del request
        request_mock = Mock()

        # Configura el objeto mock para obtener el objeto usuario
        self.viewset.get_object = Mock(return_value=self.usuario)

        # Ejecuta el método destroy() del viewset
        response = self.viewset.destroy(request_mock)

        # Verifica el comportamiento esperado
        # self.viewset.perform_destroy.assert_called_once_with(self.usuario)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data, {'message': 'Usuario eliminado correctamente'})

        # Verifica si el objeto Usuario se ha eliminado correctamente
        with self.assertRaises(Usuario.DoesNotExist):
            Usuario.objects.get(pk=self.usuario.pk)

    def test_create(self):
        # Crea un objeto mock del request
        request_mock = Mock(data={'nombre': 'Jane Smith', 'correo': 'jane@example.com'})

        # Crea un objeto mock del serializer
        serializer_mock = Mock(spec=UsuarioSerializer)
        serializer_mock.is_valid.return_value = True
        serializer_mock.data = {'nombre': 'Jane Smith', 'correo': 'jane@example.com'}

        # Configura el objeto mock del viewset
        self.viewset.get_serializer = Mock(return_value=serializer_mock)
        self.viewset.get_success_headers = Mock(return_value={'Location': 'http://example.com'})

        # Ejecuta el método create() del viewset
        response = self.viewset.create(request_mock)

        # Verifica el comportamiento esperado
        serializer_mock.is_valid.assert_called_once()
        # self.viewset.perform_create.assert_called_once_with(serializer_mock.return_value)
        self.viewset.get_success_headers.assert_called_once()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {'message': 'Usuario creado exitosamente', 'data': serializer_mock.data})


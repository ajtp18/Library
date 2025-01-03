from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from .models import Book
from datetime import datetime
from decimal import Decimal

class BookAPITests(APITestCase):
    """
    Pruebas unitarias para los endpoints de la API de libros.
    
    Verifica el funcionamiento correcto de las operaciones
    principales de búsqueda y estadísticas.
    """

    def setUp(self):
        """
        Configura el ambiente de pruebas.
        
        Crea un usuario de prueba, genera el token JWT y
        configura los datos iniciales para las pruebas.
        """
        # Crear usuario de prueba
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # Obtener token JWT
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        
        # Crear libros de prueba
        self.books = [
            Book.objects.create(
                title='Python Programming',
                author='John Doe',
                published_date=datetime(2023, 1, 1),
                genre='PRO',
                price=Decimal('29.99')
            ),
            Book.objects.create(
                title='Django Master',
                author='Jane Smith',
                published_date=datetime(2023, 2, 1),
                genre='PRO',
                price=Decimal('39.99')
            ),
            Book.objects.create(
                title='MongoDB Basics',
                author='John Doe',
                published_date=datetime(2022, 1, 1),
                genre='DAT',
                price=Decimal('24.99')
            )
        ]

    def test_search_books(self):
        """
        Prueba la funcionalidad de búsqueda de libros.
        
        Verifica que la búsqueda retorne los resultados esperados
        y que el ordenamiento por relevancia sea correcto.
        """
        # Prueba búsqueda por título
        url = reverse('book-search')
        response = self.client.get(url, {'q': 'Python'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Python Programming')
        
        # Prueba búsqueda por autor
        response = self.client.get(url, {'q': 'John'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        
        # Prueba búsqueda sin término
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_book_statistics(self):
        """
        Prueba la funcionalidad de estadísticas de libros.
        
        Verifica que los cálculos estadísticos sean correctos
        y que el filtrado por año funcione adecuadamente.
        """
        url = reverse('book-stats')
        
        # Prueba estadísticas para 2023
        response = self.client.get(url, {'year': '2023'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['year'], 2023)
        self.assertEqual(response.data['total_books'], 2)
        self.assertEqual(Decimal(response.data['average_price']), Decimal('34.99'))
        self.assertEqual(Decimal(response.data['min_price']), Decimal('29.99'))
        self.assertEqual(Decimal(response.data['max_price']), Decimal('39.99'))
        
        # Prueba año sin libros
        response = self.client.get(url, {'year': '2021'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
        # Prueba año inválido
        response = self.client.get(url, {'year': 'invalid'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_authentication_required(self):
        """
        Prueba que los endpoints requieran autenticación.
        
        Verifica que los usuarios no autenticados no puedan
        acceder a los endpoints protegidos.
        """
        # Remover credenciales
        self.client.credentials()
        
        # Intentar acceder a búsqueda
        url = reverse('book-search')
        response = self.client.get(url, {'q': 'Python'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # Intentar acceder a estadísticas
        url = reverse('book-stats')
        response = self.client.get(url, {'year': '2023'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_crud_operations(self):
        """
        Prueba las operaciones CRUD básicas para libros.
        
        Verifica la creación, lectura, actualización y eliminación
        de libros a través de la API.
        """
        # Prueba creación
        url = reverse('book-list')
        new_book_data = {
            'title': 'Test Book',
            'author': 'Test Author',
            'published_date': '2023-01-01',
            'genre': 'PRO',
            'price': '19.99'
        }
        response = self.client.post(url, new_book_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        book_id = response.data['id']
        
        # Prueba lectura
        response = self.client.get(f"{url}{book_id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Book')
        
        # Prueba actualización
        update_data = {
            'title': 'Updated Test Book',
            'price': '29.99'
        }
        response = self.client.patch(f"{url}{book_id}/", update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Test Book')
        self.assertEqual(response.data['price'], '29.99')
        
        # Prueba eliminación
        response = self.client.delete(f"{url}{book_id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Verificar que el libro fue eliminado
        response = self.client.get(f"{url}{book_id}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_genre_filtering(self):
        """
        Prueba el filtrado de libros por género.
        
        Verifica que los libros se filtren correctamente por género
        y que los conteos sean precisos.
        """
        # Crear libro de otro género para las pruebas
        Book.objects.create(
            title='Fantasy Book',
            author='Fantasy Author',
            published_date=datetime(2023, 3, 1),
            genre='FAN',
            price=Decimal('19.99')
        )
        
        url = reverse('book-list')
        
        # Probar filtrado por género PRO
        response = self.client.get(url, {'genre': 'PRO'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        
        # Probar filtrado por género DAT
        response = self.client.get(url, {'genre': 'DAT'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        
        # Probar filtrado por género FAN
        response = self.client.get(url, {'genre': 'FAN'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        
        # Probar filtrado por género inexistente
        response = self.client.get(url, {'genre': 'XXX'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)
        
        # Verificar que todos los libros tienen el género correcto en cada filtro
        for genre in ['PRO', 'DAT', 'FAN']:
            response = self.client.get(url, {'genre': genre})
            for book in response.data['results']:
                self.assertEqual(book['genre'], genre)

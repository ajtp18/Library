from django.core.management.base import BaseCommand
from faker import Faker
from decimal import Decimal
import random
from libros.models import Book

class Command(BaseCommand):
    """
    Comando de Django para generar datos de prueba para libros.
    
    Este comando utiliza la librería Faker para generar datos aleatorios
    y crear registros de libros en la base de datos usando bulk_create.
    """

    help = 'Crea una cantidad específica de libros con datos aleatorios'
    CHUNK_SIZE = 50

    def add_arguments(self, parser):
        """
        Define los argumentos que acepta el comando.
        
        Args:
            parser: Parser de argumentos de Django
        """
        parser.add_argument(
            'total', 
            type=int, 
            help='Cantidad de libros a crear'
        )
        parser.add_argument(
            '--locale',
            type=str,
            default='es_ES',
            help='Idioma para los datos generados (default: es_ES)'
        )

    def handle(self, *args, **kwargs):
        """
        Ejecuta la lógica principal del comando.
        
        Genera libros con datos aleatorios utilizando Faker y
        los guarda en la base de datos en chunks para mejor rendimiento.
        """
        total = kwargs['total']
        locale = kwargs['locale']
        fake = Faker(locale)
        genres = [choice[0] for choice in Book.GENRE_CHOICES]
        authors = [
            'Gabriel García Márquez', 'Jorge Luis Borges',
            'Isabel Allende', 'Julio Cortázar',
            'Mario Vargas Llosa', 'Pablo Neruda',
            'Octavio Paz', 'Miguel de Cervantes',
            'Federico García Lorca', 'Carlos Ruiz Zafón'
        ]

        self.stdout.write(f'Creando {total} libros en chunks de {self.CHUNK_SIZE}...')
        
        books_created = 0
        while books_created < total:
            chunk_size = min(self.CHUNK_SIZE, total - books_created)
            chunk = [
                Book(
                    title=fake.catch_phrase(),
                    author=random.choice(authors),
                    published_date=fake.date_between(start_date='-50y', end_date='today'),
                    genre=random.choice(genres),
                    price=Decimal(str(round(random.uniform(10.0, 150.0), 2)))
                )
                for _ in range(chunk_size)
            ]
            
            Book.objects.bulk_create(chunk)
            books_created += chunk_size
            self.stdout.write(
                self.style.SUCCESS(f'Creados {books_created} libros de {total}')
            )

        self.stdout.write(
            self.style.SUCCESS(f'¡Proceso completado! Se crearon {total} libros exitosamente')
        ) 
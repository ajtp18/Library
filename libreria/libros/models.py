from django.db import models

class Book(models.Model):
    """
    Modelo que representa un libro en la librería.
    
    Este modelo almacena la información básica de los libros incluyendo
    título, autor, fecha de publicación, género y precio.
    """
    
    GENRE_CHOICES = [
        ('FIC', 'Ficción'),
        ('NOF', 'No Ficción'),
        ('SCI', 'Ciencia'),
        ('ROM', 'Romance'),
        ('MIS', 'Misterio'),
        ('FAN', 'Fantasía'),
        ('PRO', 'Programación'),
        ('DAT', 'Base de datos'),
    ]

    title = models.CharField(max_length=200, verbose_name='Título')
    author = models.CharField(max_length=100, verbose_name='Autor')
    published_date = models.DateField(verbose_name='Fecha de Publicación')
    genre = models.CharField(max_length=3, choices=GENRE_CHOICES, verbose_name='Género')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Precio')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Libro'
        verbose_name_plural = 'Libros'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.author}"

from django.contrib import admin
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """
    Configuración del panel de administración para el modelo Book.
    
    Proporciona una interfaz administrativa personalizada con funciones
    de búsqueda y filtrado.
    """
    
    list_display = ('title', 'author', 'published_date', 'genre', 'price')
    list_filter = ('genre', 'published_date')
    search_fields = ('title', 'author')

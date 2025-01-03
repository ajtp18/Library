from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Book.
    
    Convierte objetos Book a JSON y viceversa, manejando todas
    las operaciones CRUD a través de la API.
    """
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'published_date', 'genre', 'price', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class BookStatItemSerializer(serializers.Serializer):
    """
    Serializador para elementos individuales en las estadísticas de libros.
    """
    title = serializers.CharField()
    author = serializers.CharField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)

class BookStatsSerializer(serializers.Serializer):
    """
    Serializador para las estadísticas de libros por año.
    """
    year = serializers.IntegerField()
    average_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    min_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    max_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_books = serializers.IntegerField()
    books = BookStatItemSerializer(many=True) 
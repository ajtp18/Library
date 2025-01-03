from django.shortcuts import render
from rest_framework import viewsets, views, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiParameter, extend_schema_view
from drf_spectacular.types import OpenApiTypes
from .models import Book
from .serializers import BookSerializer, BookStatsSerializer
from .pagination import Pagination
from rest_framework_simplejwt.authentication import JWTAuthentication
from .utils.mongo import MongoConnection

@extend_schema_view(
    list=extend_schema(
        tags=['Books'],
        parameters=[
            OpenApiParameter(
                name='genre',
                description='Filtrar por género',
                required=False,
                type=str,
                enum=['FIC', 'NOF', 'SCI', 'ROM', 'MIS', 'FAN', 'PRO', 'DAT']
            )
        ]
    ),
    create=extend_schema(tags=['Books']),
    retrieve=extend_schema(tags=['Books']),
    update=extend_schema(tags=['Books']),
    partial_update=extend_schema(tags=['Books']),
    destroy=extend_schema(tags=['Books']),
)
class BookViewSet(viewsets.ModelViewSet):
    """
    ViewSet para operaciones CRUD en el modelo Book.
    
    Proporciona endpoints estándar REST y búsqueda de texto completo
    utilizando las capacidades de agregación de MongoDB.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = Pagination

    def get_queryset(self):
        """
        Obtiene el queryset de libros aplicando los filtros especificados.
        """
        queryset = super().get_queryset()
        genre = self.request.query_params.get('genre')
        
        if genre:
            queryset = queryset.filter(genre=genre)
        
        return queryset

    @extend_schema(
        tags=['Books'],
        parameters=[
            OpenApiParameter(
                name='q',
                description='Término de búsqueda',
                required=True,
                type=str
            )
        ],
        responses={
            200: BookSerializer(many=True),
            400: OpenApiTypes.OBJECT,
            500: OpenApiTypes.OBJECT,
        }
    )
    @action(detail=False, methods=['get'])
    def search(self, request):
        """
        Endpoint para búsqueda de texto completo en libros.
        
        Utiliza el motor de búsqueda de MongoDB para realizar
        búsquedas en los campos de texto del libro.
        
        Args:
            request: Objeto Request con el parámetro de búsqueda 'q'
            
        Returns:
            Response: Resultados paginados ordenados por relevancia
        """
        search_term = request.query_params.get('q', '')
        if not search_term:
            return Response(
                {'error': 'El parámetro de búsqueda "q" es requerido'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        pipeline = [
            {
                '$match': {
                    '$or': [
                        {'title': {'$regex': search_term, '$options': 'i'}},
                        {'author': {'$regex': search_term, '$options': 'i'}},
                        {'genre': {'$regex': search_term, '$options': 'i'}}
                    ]
                }
            },
            {
                '$addFields': {
                    'score': {
                        '$add': [
                            {'$cond': [{'$regexMatch': {'input': '$title', 'regex': search_term, 'options': 'i'}}, 3, 0]},
                            {'$cond': [{'$regexMatch': {'input': '$author', 'regex': search_term, 'options': 'i'}}, 2, 0]},
                            {'$cond': [{'$regexMatch': {'input': '$genre', 'regex': search_term, 'options': 'i'}}, 1, 0]}
                        ]
                    }
                }
            },
            {
                '$sort': {
                    'score': -1,
                    'title': 1
                }
            }
        ]

        try:
            mongo = MongoConnection()
            collection = mongo.get_collection('libros_book')
            results = list(collection.aggregate(pipeline))

            # Normalizar los ObjectId y Decimal128 para la serialización JSON
            for result in results:
                if '_id' in result:
                    result['_id'] = str(result['_id'])
                if 'price' in result:
                    result['price'] = str(result['price'])

            page = self.paginate_queryset(results)
            if page is not None:
                return self.get_paginated_response(page)

            return Response(results)
        except Exception as e:
            return Response(
                {'error': f'Error en la búsqueda: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

@extend_schema(tags=['Books'])
class BookStatsView(views.APIView):
    """
    Vista para obtener estadísticas de libros.
    
    Proporciona endpoints para análisis estadístico de los datos de libros
    utilizando las capacidades de agregación de MongoDB.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=['Books'],
        parameters=[
            OpenApiParameter(
                name='year',
                description='Year to filter statistics',
                required=True,
                type=int
            )
        ],
        responses={
            200: BookStatsSerializer,
            400: OpenApiTypes.OBJECT,
            404: OpenApiTypes.OBJECT,
            500: OpenApiTypes.OBJECT
        }
    )
    def get(self, request):
        """
        Get average book price by year.
        """
        year = request.query_params.get('year')
        
        if not year or not year.isdigit():
            return Response(
                {'error': 'Year parameter is required and must be a number'},
                status=status.HTTP_400_BAD_REQUEST
            )

        pipeline = [
            {
                '$sort': {
                    'price': -1
                }
            },
            {
                '$match': {
                    '$expr': {
                        '$eq': [{'$year': '$published_date'}, int(year)]
                    }
                }
            },
            {
                '$group': {
                    '_id': None,
                    'average_price': {'$avg': '$price'},
                    'min_price': {'$min': '$price'},
                    'max_price': {'$max': '$price'},
                    'total_books': {'$sum': 1},
                    'books': {
                        '$push': {
                            'title': '$title',
                            'author': '$author',
                            'price': '$price'
                        }
                    }
                }
            },
            {
                '$project': {
                    '_id': 0,
                    'year': {'$literal': int(year)},
                    'average_price': {'$round': ['$average_price', 2]},
                    'min_price': 1,
                    'max_price': 1,
                    'total_books': 1,
                    'books': 1
                }
            }
        ]

        try:
            mongo = MongoConnection()
            collection = mongo.get_collection('libros_book')
            result = list(collection.aggregate(pipeline))

            if not result:
                return Response(
                    {
                        'year': int(year),
                        'message': f'No books found for year {year}'
                    },
                    status=status.HTTP_404_NOT_FOUND
                )

            serializer = BookStatsSerializer(data=result[0])
            serializer.is_valid(raise_exception=True)
            
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {'error': f'Error processing aggregation: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

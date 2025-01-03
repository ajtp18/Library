from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class Pagination(PageNumberPagination):
    """
    Clase de paginación personalizada para la API.
    
    Proporciona paginación con información adicional como total de páginas
    y enlaces de navegación.
    """
    
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        """
        Personaliza la respuesta de paginación incluyendo metadatos adicionales.
        
        Args:
            data: Los datos a paginar
            
        Returns:
            Response: Respuesta con metadatos de paginación y resultados
        """
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'total_pages': self.page.paginator.num_pages,
            'count': self.page.paginator.count,
            'results': data
        }) 
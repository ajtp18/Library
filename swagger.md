# Documentación de API - Librería

## Información General
- **Base URL**: http://libreria-app-887967250.sa-east-1.elb.amazonaws.com
- **Versión**: 1.0.0
- **Descripción**: API REST para gestión de librería con MongoDB

## Autenticación

### Obtener Token JWT
```http
POST /api/token/
```

#### Request Body
```json
{
    "username": "test",
    "password": "test"
}
```

#### Response
```json
{
    "refresh": "string",
    "access": "string"
}
```

### Refrescar Token
```http
POST /api/token/refresh/
```

#### Request Body
```json
{
    "refresh": "string"
}
```

## Endpoints de Libros

### Listar Libros
```http
GET /api/books/
```

#### Query Parameters
- `page`: número de página (default: 1)
- `page_size`: elementos por página (default: 10, max: 100)
- `genre`: filtrar por género (opcional)
  - Valores permitidos: `FIC`, `NOF`, `SCI`, `ROM`, `MIS`, `FAN`, `PRO`, `DAT`

#### Response
```json
{
    "links": {
        "next": "string",
        "previous": "string"
    },
    "total_pages": 0,
    "count": 0,
    "results": [
        {
            "id": 0,
            "title": "string",
            "author": "string",
            "published_date": "YYYY-MM-DD",
            "genre": "string",
            "price": "0.00",
            "created_at": "YYYY-MM-DDThh:mm:ss",
            "updated_at": "YYYY-MM-DDThh:mm:ss"
        }
    ]
}
```

### Crear Libro
```http
POST /api/books/
```

#### Request Body
```json
{
    "title": "string",
    "author": "string",
    "published_date": "YYYY-MM-DD",
    "genre": "string",
    "price": "0.00"
}
```

### Obtener Libro
```http
GET /api/books/{id}/
```

### Actualizar Libro
```http
PUT /api/books/{id}/
```

#### Request Body
```json
{
    "title": "string",
    "author": "string",
    "published_date": "YYYY-MM-DD",
    "genre": "string",
    "price": "0.00"
}
```

### Actualización Parcial
```http
PATCH /api/books/{id}/
```

### Eliminar Libro
```http
DELETE /api/books/{id}/
```

### Búsqueda de Libros
```http
GET /api/books/search/
```

#### Query Parameters
- `q`: término de búsqueda (requerido)
- `page`: número de página
- `page_size`: elementos por página

#### Response
```json
{
    "links": {
        "next": "string",
        "previous": "string"
    },
    "total_pages": 0,
    "count": 0,
    "results": [
        {
            "id": 0,
            "title": "string",
            "author": "string",
            "published_date": "YYYY-MM-DD",
            "genre": "string",
            "price": "0.00",
            "created_at": "YYYY-MM-DDThh:mm:ss",
            "updated_at": "YYYY-MM-DDThh:mm:ss"
        }
    ]
}
```

### Estadísticas por Año
```http
GET /api/book_stats/
```

#### Query Parameters
- `year`: año para filtrar estadísticas (requerido)

#### Response
```json
{
    "year": 0,
    "average_price": "0.00",
    "min_price": "0.00",
    "max_price": "0.00",
    "total_books": 0,
    "books": [
        {
            "title": "string",
            "author": "string",
            "price": "0.00"
        }
    ]
}
```

## Códigos de Estado

- `200 OK`: Petición exitosa
- `201 Created`: Recurso creado exitosamente
- `204 No Content`: Recurso eliminado exitosamente
- `400 Bad Request`: Error en la petición
- `401 Unauthorized`: No autenticado
- `403 Forbidden`: No autorizado
- `404 Not Found`: Recurso no encontrado
- `500 Internal Server Error`: Error del servidor

## Géneros Disponibles

- `FIC`: Ficción
- `NOF`: No Ficción
- `SCI`: Ciencia
- `ROM`: Romance
- `MIS`: Misterio
- `FAN`: Fantasía
- `PRO`: Programación
- `DAT`: Base de datos

## Notas Adicionales

1. Todos los endpoints requieren autenticación JWT
2. El token debe incluirse en el header como:
   ```
   Authorization: Bearer <token>
   ```
3. La paginación está habilitada por defecto en las listas
4. Los precios se manejan con 2 decimales
5. Las fechas siguen el formato ISO 8601
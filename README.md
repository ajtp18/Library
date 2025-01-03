# API de Librería con Django y MongoDB Atlas

API REST para gestión de libros utilizando Django, Django REST Framework y MongoDB Atlas como base de datos.

## Demo en vivo
Como parte de la prueba aqui esta la demo en vivo bajo AWS y MongoDB Atlas: [Link swagger](http://libreria-app-887967250.sa-east-1.elb.amazonaws.com/swagger/)

Las credenciales del usuario de prueba son: `usuario: test  contraseña: test`.

## Características

- CRUD completo para libros
- Búsqueda de texto completo
- Estadísticas por año
- Filtrado por género
- Autenticación JWT
- Documentación con Swagger/OpenAPI
- Pruebas unitarias
- Paginación personalizada

## Requisitos Previos

- Python 3.12+
- MongoDB Atlas cuenta (gratuita o de pago)
- Git

## Configuración del Entorno

1. Clonar el repositorio:

```bash
git clone <url-del-repositorio>
cd libreria
```

2. Crear y activar el entorno virtual:

```bash
python -m venv venv
source venv/bin/activate
```

3. Instalar las dependencias:

```bash
pip install -r requirements.txt
```

4. Configurar el archivo .env con las variables de entorno

```bash
MONGO_HOST=HOST_MONGODB
MONGO_PORT=PORT_MONGODB
MONGO_USER=MONGO_USER
MONGO_PASSWORD=MONGO_PASSWORD
```

5. Migraciones, crear super usuario y correr seeders

- Ejecutar migraciones
```bash
python manage.py migrate
```

- Crear super usuario
```bash
python manage.py createsuperuser
```

- Crear seeders (Opcional)
```bash
python .\manage.py seed_books {especificar cantidad de libros a crear, ejemplo: 100}
```

6. Ejecutar el servidor en desarrollo

```bash
python manage.py runserver
```

7. Acceder a la api y su documentación,

- API: http://localhost:8000/api/
- Admin: http://localhost:8000/admin/
- Swagger: http://localhost:8000/swagger/
- ReDoc: http://localhost:8000/redoc/

## Autenticación

La API utiliza autenticación JWT. Para obtener un token:

8. Hacer POST a `/api/token/` con:

```json
{
    "username": "tu-usuario",
    "password": "tu-contraseña"
}
```

9. Usar el token en el header de las peticiones:

```
Authorization: Bearer <tu-token>
```

## Endpoints Principales

- `GET /api/books/`: Lista de libros (soporta filtrado por género)
- `POST /api/books/`: Crear nuevo libro
- `GET /api/books/{id}/`: Detalle de libro
- `PUT/PATCH /api/books/{id}/`: Actualizar libro
- `DELETE /api/books/{id}/`: Eliminar libro
- `GET /api/books/search/?q=término`: Búsqueda de libros
- `GET /api/stats/?year=2023`: Estadísticas por año

## Estructura del Proyecto

```
libreria/
├── libreria/          # Configuración principal
├── libros/            # App principal
│   ├── models.py      # Modelos de datos
│   ├── views.py       # Vistas y lógica
│   ├── serializers.py # Serializadores
│   ├── tests.py       # Pruebas unitarias
│   └── urls.py        # Rutas de la API
└── manage.py
```

## Ejecutar Pruebas

```bash
python manage.py test
```

## Consideraciones de Seguridad

1. Nunca compartir el archivo `.env`
2. Mantener las credenciales de MongoDB Atlas seguras
3. Usar HTTPS en producción
4. Rotar regularmente las claves JWT
5. Limitar el acceso a la red en MongoDB Atlas

## Solución de Problemas

1. Error de conexión a MongoDB:
   - Verificar URI de conexión
   - Comprobar IP en lista blanca
   - Verificar credenciales

2. Error en autenticación:
   - Verificar formato del token
   - Comprobar que el token no ha expirado
   - Verificar credenciales de usuario

## Licencia

Este proyecto está bajo la licencia MIT.




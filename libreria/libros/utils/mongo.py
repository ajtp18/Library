from pymongo import MongoClient
from django.conf import settings
import os

class MongoConnection:
    """
    Clase para manejar la conexión a MongoDB usando pymongo.
    
    Proporciona una interfaz para interactuar directamente con MongoDB
    utilizando la configuración de Django.
    """
    
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MongoConnection, cls).__new__(cls)
            # Obtener la configuración de MongoDB desde settings
            mongo_settings = settings.DATABASES['default']
            cls._instance.client = MongoClient(mongo_settings['CLIENT']['host'])
            cls._instance.db = cls._instance.client[mongo_settings['NAME']]
        return cls._instance

    def get_collection(self, collection_name: str):
        """
        Obtiene una colección específica de MongoDB.
        
        Args:
            collection_name: Nombre de la colección
            
        Returns:
            Collection: Objeto de colección de MongoDB
        """
        return self.db[collection_name]

    def __del__(self):
        """
        Cierra la conexión al destruir la instancia.
        """
        if hasattr(self, 'client'):
            self.client.close() 
from flask_restx import fields
from dataclasses import dataclass
from typing import Optional

@dataclass
class InsertVideoDto:
    """
    Data Transfer Object para insertar un nuevo video
    """
    name: str
    views: int
    likes: int
    
    def __init__(self, name: str, views: int = 0, likes: int = 0):
        self.name = name
        self.views = views
        self.likes = likes
    
    @classmethod
    def from_dict(cls, data: dict):
        """
        Crea una instancia del DTO desde un diccionario
        
        Args:
            data (dict): Datos del video
            
        Returns:
            InsertVideoDto: Instancia del DTO
        """
        return cls(
            name=data.get('name', ''),
            views=data.get('views', 0),
            likes=data.get('likes', 0)
        )
    
    def to_dict(self):
        """
        Convierte el DTO a un diccionario
        
        Returns:
            dict: Datos del video
        """
        return {
            'name': self.name,
            'views': self.views,
            'likes': self.likes
        }
    
    def validate(self):
        """
        Valida los datos del DTO
        
        Returns:
            tuple: (bool, str) - (es_valido, mensaje_error)
        """
        if not self.name or len(self.name.strip()) == 0:
            return False, "El nombre del video es requerido"
        
        if self.views < 0:
            return False, "El número de vistas no puede ser negativo"
        
        if self.likes < 0:
            return False, "El número de likes no puede ser negativo"
        
        if len(self.name) > 100:
            return False, "El nombre del video no puede exceder 100 caracteres"
        
        return True, "Válido"

# Modelo para Flask-RESTX Swagger Documentation
def create_insert_video_model(api):
    """
    Crea el modelo de Flask-RESTX para la documentación Swagger
    
    Args:
        api: Instancia de Flask-RESTX Api
        
    Returns:
        Model: Modelo para Swagger
    """
    return api.model('InsertVideo', {
        'name': fields.String(required=True, description='Nombre del video', example='Mi video favorito'),
        'views': fields.Integer(required=False, description='Número de vistas', example=1000, default=0),
        'likes': fields.Integer(required=False, description='Número de likes', example=50, default=0)
    })
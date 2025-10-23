"""
Modelo de datos para Video
"""
from models import db

class VideoModel(db.Model):
    """
    Modelo para representar un video.
    
    Atributos:
        id (int): Identificador único del video
        name (str): Nombre del video
        views (int): Número de vistas del video
        likes (int): Número de likes del video
    """
    # Nombre de la tabla en la base de datos
    __tablename__ = 'videos'
    
    # Definición de columnas
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        """
        Representación en string del objeto Video
        """
        return f"Video(id={self.id}, name={self.name}, views={self.views}, likes={self.likes})"

    def create(self):
        """
        Método de clase para crear un nuevo video
        
        Args:
            name (str): Nombre del video
            views (int): Número de vistas
            likes (int): Número de likes
            
        Returns:
            VideoModel: El video creado
        """
        db.session.add(self)
        db.session.commit()
        return self
    

    @classmethod
    def save(cls):
        db.session.commit()
        print(cls)

    @classmethod
    def edit(cls, name, views, likes):
        video = cls(name=name, views=views, likes=likes)
        db.session.add(video)
        db.session.commit()
        return video
    

    @classmethod
    def delete(cls, video):
        db.session.delete(video)
        db.session.commit()

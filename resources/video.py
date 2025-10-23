"""
Recursos y rutas para la API de videos
"""
from flask_restx import Resource, abort, fields, Namespace
from flask import Flask, request
from models.video import VideoModel
from models import db
from schemes.insertVideoDTo import InsertVideoDto, create_insert_video_model

# Crear namespace para organizar la API
api = Namespace('videos', description='Operaciones con videos')

# Crear modelos para Swagger
insert_video_model = create_insert_video_model(api)

# Modelo para respuestas de video
video_response_model = api.model('VideoResponse', {
    'id': fields.Integer(required=True, description='ID único del video'),
    'name': fields.String(required=True, description='Nombre del video'),
    'views': fields.Integer(required=True, description='Número de vistas'),
    'likes': fields.Integer(required=True, description='Número de likes')
})

# Modelo para actualización de video (campos opcionales)
video_update_model = api.model('VideoUpdate', {
    'name': fields.String(required=False, description='Nuevo nombre del video'),
    'views': fields.Integer(required=False, description='Nuevo número de vistas'),
    'likes': fields.Integer(required=False, description='Nuevo número de likes')
})

# Los parsers ya no son necesarios, usamos JSON directamente con los modelos de Flask-RESTX

def abort_if_video_doesnt_exist(video_id):
    """
    Verifica si un video existe, y si no, aborta la solicitud
    
    Args:
        video_id (int): ID del video a verificar
    """
    video = VideoModel().query.filter_by(id=video_id).first()
    if not video:
        abort(404, message=f"No se encontró un video con el ID {video_id}")
    return video

def isInExistence(videoId):
    if not VideoModel.query.filter_by(id=videoId).first():
        return False
    return True

@api.route('/<int:video_id>')
class Video(Resource):
    """
    Recurso para gestionar videos individuales
    
    Métodos:
        get: Obtener un video por ID
        post: Crear un nuevo video
        patch: Actualizar un video existente
        delete: Eliminar un video
    """

    @api.marshal_with(video_response_model)
    @api.doc('get_video')
    def get(self, video_id):
        """Obtener un video por ID"""
        return abort_if_video_doesnt_exist(video_id)
    

    @api.marshal_with(video_response_model)
    @api.expect(insert_video_model)
    @api.doc('create_video')
    def post(self, video_id):
        """
        Crea un nuevo video con un ID específico usando DTO
        
        Args:
            video_id (int): ID para el nuevo video
            
        Returns:
            VideoModel: El video creado
        """
        # Obtener datos JSON del request
        json_data = request.get_json()
        
        if not json_data:
            abort(400, message="No se proporcionaron datos JSON")
        
        # Crear DTO desde los datos JSON
        video_dto = InsertVideoDto.from_dict(json_data)
        
        # Validar DTO
        is_valid, error_message = video_dto.validate()
        if not is_valid:
            abort(400, message=error_message)
        
        # Verificar si el video ya existe
        if isInExistence(video_id):
            abort(409, message=f"Ya existe un video con el ID {video_id}")
        
        # Crear nuevo video con los datos del DTO
        new_video = VideoModel(
            id=video_id,
            name=video_dto.name,
            views=video_dto.views,
            likes=video_dto.likes
        )
        
        # Insertar en la base de datos
        new_video.create()
        
        return new_video

    @api.marshal_with(video_response_model)
    @api.expect(video_update_model)
    @api.doc('update_video')
    def patch(self, video_id):
        """
        Actualiza un video existente
        
        Args:
            video_id (int): ID del video a actualizar
            
        Returns:
            VideoModel: El video actualizado
        """
        # Obtener datos JSON del request
        json_data = request.get_json()
        
        if not json_data:
            abort(400, message="No se proporcionaron datos JSON")
        
        # Verificar que el video existe
        video = abort_if_video_doesnt_exist(video_id)
        
        # Actualizar solo los campos proporcionados
        if 'name' in json_data and json_data['name'] is not None:
            if len(json_data['name'].strip()) == 0:
                abort(400, message="El nombre del video no puede estar vacío")
            video.name = json_data['name']
        
        if 'views' in json_data and json_data['views'] is not None:
            if json_data['views'] < 0:
                abort(400, message="El número de vistas no puede ser negativo")
            video.views = json_data['views']
        
        if 'likes' in json_data and json_data['likes'] is not None:
            if json_data['likes'] < 0:
                abort(400, message="El número de likes no puede ser negativo")
            video.likes = json_data['likes']
        
        # Guardar cambios
        VideoModel().save()
        
        return video, 200

    @api.doc('delete_video')
    def delete(self, video_id):
        """
        Elimina un video existente
        
        Args:
            video_id (int): ID del video a eliminar
            
        Returns:
            str: Mensaje vacío con código 204
        """
        # Verificar que el video existe
        video = abort_if_video_doesnt_exist(video_id)
        
        # Eliminar el video de la base de datos
        VideoModel().delete(video)
        
        # Retornar respuesta vacía con código 204 (No Content)
        return '', 204

@api.route('/all')
class Videos(Resource):
    @api.marshal_list_with(video_response_model)
    @api.doc('get_all')
    def get(self):
        """Obtener listado videos"""
        videos = VideoModel.query.all() 
        return videos
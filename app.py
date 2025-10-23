import os
from flask import Flask
from flask_restx import Resource, Api
from models import db
from resources.video import api as videos_api
from config import config

def create_app(config_name='development'):
    """
    Función factory para crear la aplicación Flask
    
    Args:
        config_name (str): Nombre de la configuración a utilizar
        
    Returns:
        Flask: Aplicación Flask configurada
    """
    # Crear el objeto Flask
    app = Flask(__name__)
    
    # Cargar configuración
    app.config.from_object(config[config_name])
    
    # Inicializar extensiones
    db.init_app(app)
    api = Api(app, doc='/swagger/', title='Videos API', description='API para gestionar videos')
    
    # Registrar namespaces
    api.add_namespace(videos_api, path='/videos')

    return app

if __name__ == "__main__":
    # Obtener configuración del entorno o usar 'development' por defecto
    config_name = os.getenv('FLASK_CONFIG', 'development')
    
    # Crear aplicación
    app = create_app(config_name)
    
    # Crear todas las tablas en la base de datos
    with app.app_context():
        db.create_all()
    
    # Ejecutar servidor
    app.run(host='0.0.0.0', port=5000, debug=True)


## DTO InsertVideoDto

El DTO `InsertVideoDto` para estructurar los datos al insertar un nuevo video.

### Estructura del DTO:

```python
@dataclass
class InsertVideoDto:
    name: str          
    views: int = 0     
    likes: int = 0     
```

### Validaciones incluidas:

- El nombre no puede estar vacío
- Las vistas no pueden ser negativas
- Los likes no pueden ser negativos
- El nombre no puede exceder 100 caracteres

## Endpoints disponibles:

### 1. Crear un video
**POST** `/videos/{video_id}`

```json
{
  "name": "Mi video increíble",
  "views": 1500,
  "likes": 120
}
```

### 2. Obtener un video
**GET** `/videos/{video_id}`

### 3. Actualizar un video
**PATCH** `/videos/{video_id}`

### 4. Eliminar un video
**DELETE** `/videos/{video_id}`

## Ejemplos de uso con curl:

### Crear un nuevo video:
```bash
curl -X POST "http://127.0.0.1:5000/videos/1" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "Tutorial de Python",
       "views": 1000,
       "likes": 50
     }'
```

### Crear un video con valores por defecto:
```bash
curl -X POST "http://127.0.0.1:5000/videos/2" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "Introducción a Flask"
     }'
```

### Obtener un video:
```bash
curl -X GET "http://127.0.0.1:5000/videos/1"
```

## Swagger UI:
**http://127.0.0.1:5000/swagger/**


## Respuestas de ejemplo:

### Éxito (201 Created):
```json
{
  "id": 1,
  "name": "Tutorial de Python",
  "views": 1000,
  "likes": 50
}
```

### Error de validación (400 Bad Request):
```json
{
  "message": "El nombre del video es requerido"
}
```

### Video ya existe (409 Conflict):
```json
{
  "message": "Ya existe un video con el ID 1"
}
```
# FastAPI Challenge

## 🚀 Características

- **Autenticación JWT** - Registro, inicio de sesión y gestión de perfiles de usuario
- **Publicaciones** - Crear, leer, actualizar y eliminar publicaciones
- **Comentarios** - Agregar y gestionar comentarios en publicaciones
- **Etiquetas** - Categorizar publicaciones con etiquetas
- **Búsqueda** - Buscar publicaciones por contenido o etiquetas
- **Paginación** - Soporte para paginación en listados
- **Middleware de Tiempo** - Registro del tiempo de respuesta de las peticiones

## 🛠️ Tecnologías

- **Backend**: Python + FastAPI
- **Base de datos**: PostgreSQL con SQLAlchemy ORM
- **Despliegue**: Uvicorn
- **Otras herramientas**: 
  - Pydantic para validación de datos
  - Alembic para migraciones
  - SQLAlchemy como ORM

## 🚀 Configuración

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/Bryan4638/gestion-de-productos.git
   cd FastAPIChallenge
   ```

2. **Configurar entorno virtual**
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar variables de entorno**
   ```bash
   cp ..env.example .env
   # Editar el archivo .env con tus credenciales
   ```

5. **Ejecutar migraciones**
   ```bash
   alembic upgrade head
   ```

6. **Iniciar el servidor**
   ```bash
   uvicorn main:app --reload
   ```

7. **Documentación de la API**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## 📚 Módulos

### 1. Autenticación
- Registro de usuarios
- Inicio de sesión
- Validación de tokens JWT
- Protección de rutas

### 2. Publicaciones
- Crear, leer, actualizar y eliminar publicaciones
- Búsqueda por texto en título o contenido
- Filtrado por etiquetas
- Paginación de resultados

### 3. Comentarios
- Agregar comentarios a publicaciones
- Gestión de comentarios propios


## 🛠️ Estructura del Proyecto

```
FastAPIChallenge/
├── migrations/               # Migraciones de la base de datos
│   ├── versions/          # Archivos de migración
│   ├── env.py             # Configuración de Alembic
│   └── script.py.mako     # Plantilla para migraciones
│
├── core/                  # Configuración y utilidades principales
│   ├── __init__.py
│   ├── config.py          # Configuración de la aplicación
│   ├── database.py        # Configuración de la base de datos
│   ├── middleware.py      # Middleware personalizados
│   ├── security.py        # Utilidades de seguridad
│   ├── mixin_soft_delete.py  # Mixin para borrado lógico
│   └── mixin_timestamp.py    # Mixin para timestamps
│
├── modules/               # Módulos de la aplicación
│   ├── __init__.py
│   ├── auth/             # Autenticación y autorización
│   ├── comment/          # Gestión de comentarios
│   ├── posts/            # Gestión de publicaciones
│   └── user/             # Gestión de usuarios
│
├── scripts/              # Scripts de utilidad
│
├── .env.example          # Variables de entorno de ejemplo
├── alembic.ini          # Configuración de Alembic
├── main.py              # Punto de entrada de la aplicación
├── README.md            # Documentación del proyecto
└── requirements.txt     # Dependencias del proyecto
```

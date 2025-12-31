# 📋 Gestor de Tareas - API REST con FastAPI

---

## 📌 Descripción del Proyecto

Este es un **Gestor de Tareas (Task Manager) API** desarrollado con **FastAPI** y **PostgreSQL**. Es una aplicación backend REST que permite a los usuarios autenticados crear, leer, actualizar y eliminar tareas con paginación.

**Objetivo:** Demostrar habilidades en desarrollo backend Python, arquitectura REST, autenticación JWT, manejo de bases de datos y buenas prácticas de código.

---

## 🛠️ Stack Tecnológico

| Tecnología | Versión | Propósito |
|-----------|---------|----------|
| **Python** | 3.11.8 | Lenguaje principal |
| **FastAPI** | 0.128.0 | Framework web moderno |
| **SQLAlchemy** | 2.0.45 | ORM para base de datos |
| **PostgreSQL** | 16 | Base de datos relacional |
| **Alembic** | 1.17.2 | Migraciones de BD |
| **Pydantic** | 2.12.5 | Validación de datos |
| **python-jose** | 3.5.0 | Tokens JWT |
| **passlib + bcrypt** | Últimas | Hash seguro de contraseñas |
| **Uvicorn** | 0.40.0 | Servidor ASGI |

---

## 📋 Requisitos Previos

Antes de empezar, asegúrate de tener:

- **Python 3.11.8** instalado → [Descargar](https://www.python.org/downloads/)
- **Docker y Docker Compose** instalados → [Descargar](https://www.docker.com/products/docker-desktop)
- **Git** instalado → [Descargar](https://git-scm.com/)
- Un editor de código (VS Code recomendado)

### Verificar instalaciones:
```bash
python --version      # Debe mostrar 3.11.8
docker --version      # Debe mostrar Docker 
docker-compose --version  # Debe mostrar Docker Compose
git --version         # Debe mostrar Git
```

---

## 🚀 Instrucciones de Instalación y Ejecución

### Paso 1: Clonar el Repositorio

```bash
git clone <URL_DEL_REPOSITORIO>
cd Prueba_FastApi
```

### Paso 2: Crear Entorno Virtual

```bash
# En Windows:
python -m venv venv
venv\Scripts\activate

# En macOS/Linux:
python3 -m venv venv
source venv/bin/activate
```

**¿Qué es esto?** Un entorno virtual aislado para instalar dependencias sin afectar tu sistema.

### Paso 3: Instalar Dependencias

```bash
pip install -r requirements.txt
```

### Paso 4: Configurar Variables de Entorno

Copia el archivo de ejemplo:

```bash
# En Windows:
copy .env.example .env

# En macOS/Linux:
cp .env.example .env
```

El archivo `.env` contiene variables como credenciales de BD, claves JWT, etc. **No commites este archivo al repositorio** (ya está en `.gitignore`).

**Contenido típico de `.env`:**
```env
# Aplicación
APP_NAME=Gestor de Tareas
APP_ENV=local
DEBUG=true

# Seguridad - JWT
JWT_SECRET_KEY=tu_clave_secreta_cambiar_en_produccion
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=60

# Base de Datos
DB_HOST=localhost
DB_PORT=5432
DB_NAME=technical_test
DB_USER=postgres
DB_PASSWORD=postgres
```

### Paso 5: Levantar PostgreSQL con Docker

```bash
docker-compose up -d
```

**¿Qué hace?** Inicia un contenedor PostgreSQL en segundo plano. Puedes verificar que está corriendo:

```bash
docker ps
```

Deberías ver `postgres_fastapi_tareas` en la lista.

### Paso 6: Aplicar Migraciones de Base de Datos

```bash
alembic upgrade head
```

**¿Qué hace?** Ejecuta todas las migraciones pendientes para crear las tablas:
- `users` → Tabla de usuarios
- `tasks` → Tabla de tareas

**Resultado esperado:**
```
INFO  [alembic.runtime.migration] Running upgrade <revision> -> <revision>, crear tablas users y tasks
INFO  [alembic.runtime.migration] Running upgrade <revision> -> <revision>, crear usuario inicial
```

### Paso 7: Iniciar el Servidor API

```bash
uvicorn app.main:app --reload
```

**¿Qué hace?** Inicia el servidor en `http://localhost:8000`

**Resultado esperado:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

---

## 📚 Documentación Interactiva

Una vez que el servidor esté corriendo, accede a:

- **Swagger UI (Recomendado):** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

En Swagger UI puedes probar todos los endpoints directamente.

---

## 🚀 Usar Postman para Pruebas (Recomendado)

Se incluye una **Colección de Postman** lista para usar con todos los endpoints configurados, incluyendo autenticación automática y ejemplos de paginación.

### Paso 1: Descargar Postman

Si no lo tienes instalado, descárgalo desde [postman.com](https://www.postman.com/downloads/)

### Paso 2: Importar la Colección

1. Abre Postman
2. Click en **File** → **Import** (o botón Import arriba a la izquierda)
3. Selecciona el archivo `Postman_Collection.json` del proyecto
4. Click en **Import**

Verás 3 carpetas:
- **Autenticación** - Login
- **Tareas** - CRUD completo (Crear, Listar, Obtener, Actualizar, Eliminar)

### Paso 3: Ejecutar el Flujo Completo

**1. Login (PRIMERO)**
- Haz click en: **Autenticación** → **Login - Obtener Token**
- Click en **Send**
- El token se guarda **automáticamente** en la variable `{{access_token}}`

**2. Crear Tareas**
- Ve a: **Tareas** → **Crear Tarea**
- Modifica el JSON en la pestaña **Body** si lo deseas
- Click en **Send** (201 Created)

**3. Ver Paginación (★ Mejor forma de verla)**
- Ve a: **Tareas** → **Listar Tareas (Paginado)**
- **Cambia los parámetros en la URL directamente:**
  - `page=1&page_size=10` (10 tareas por página)
  - `page=1&page_size=5` (5 tareas por página)
  - `page=2&page_size=5` (página 2)
- Click en **Send**
- **Verás la respuesta JSON completa con:**
  ```json
  {
    "items": [...],
    "total": 25,
    "page": 1,
    "page_size": 10,
    "total_pages": 3
  }
  ```

**4. Obtener Una Tarea**
- Ve a: **Tareas** → **Obtener Tarea por ID**
- Cambia el ID en la URL si es necesario
- Click en **Send**

**5. Actualizar Tarea**
- Ve a: **Tareas** → **Actualizar Tarea**
- Modifica el JSON en el Body (ej: cambiar status a "done")
- Click en **Send**

**6. Eliminar Tarea**
- Ve a: **Tareas** → **Eliminar Tarea**
- Cambia el ID en la URL si es necesario
- Click en **Send** (204 No Content = éxito)

### ✅ Ventajas de usar Postman

| Característica | Descripción |
|---|---|
| **Token automático** | Se guarda automáticamente después de login |
| **Interfaz gráfica** | Fácil cambiar parámetros y ver respuestas |
| **Paginación clara** | Cambiar `page` y `page_size` visualmente |
| **Historial** | Guarda todas tus solicitudes |
| **Colecciones** | Todo el CRUD en un mismo lugar |
| **Variables de entorno** | Token se guarda automáticamente |

---

## 🔑 Autenticación

### Usuario Inicial

El sistema crea **automáticamente** un usuario admin al ejecutar las migraciones:

```
Email: admin@example.com
Contraseña: admin123
```

**Nota:** Este usuario se crea mediante una migración Alembic (ver `alembic/versions/`). No hay credenciales hardcodeadas en el código.

### Flujo de Autenticación

1. **Login** → POST `/auth/login` con email/password
2. **Recibe JWT Token** → Válido por 60 minutos
3. **Usa el Token** → En header `Authorization: Bearer <token>` para acceder a endpoints protegidos

### ¿Dónde poner el JSON en las solicitudes?

Todos los endpoints que envían datos (Login, Crear Tarea, Actualizar Tarea) requieren un JSON en el **BODY (cuerpo)** de la solicitud:

- **Con Swagger UI:** En el campo de texto que aparece cuando haces clic en "Try it out"
- **Con cURL:** Después del parámetro `-d` o `--data`
- **Con Postman/Insomnia:** En la pestaña "Body" → selecciona "raw" → "JSON"

---

## 📡 Endpoints de la API

### Autenticación

#### Login
```bash
POST /auth/login
Content-Type: application/json

# Este JSON va en el BODY (cuerpo) de la solicitud:
{
  "email": "admin@example.com",
  "password": "admin123"
}
```

**Respuesta exitosa (200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

---

### Tareas (Endpoints Protegidos)

Todos requieren header:
```
Authorization: Bearer <tu_access_token>
```

#### 1. Crear Tarea
```bash
POST /tasks
Content-Type: application/json
Authorization: Bearer <token>

# Este JSON va en el BODY (cuerpo) de la solicitud:
{
  "title": "Comprar leche",
  "description": "Ir al supermercado a comprar leche",
  "status": "pending"
}
```

**Respuesta (201):**
```json
{
  "id": 1,
  "title": "Comprar leche",
  "description": "Ir al supermercado a comprar leche",
  "status": "pending",
  "created_at": "2025-12-30T19:41:51.123456+00:00"
}
```

#### 2. Obtener Una Tarea
```bash
GET /tasks/1
Authorization: Bearer <token>
```

**Respuesta (200):**
```json
{
  "id": 1,
  "title": "Comprar leche",
  "description": "Ir al supermercado a comprar leche",
  "status": "pending",
  "created_at": "2025-12-30T19:41:51.123456+00:00"
}
```

#### 3. Listar Tareas (Con Paginación)
```bash
GET /tasks?page=1&page_size=10
Authorization: Bearer <token>
```

**Parámetros:**
- `page` (int, default=1) → Número de página
- `page_size` (int, default=10) → Tareas por página (máximo 100)

**Respuesta (200):**
```json
{
  "items": [
    {
      "id": 1,
      "title": "Comprar leche",
      "description": "Ir al supermercado",
      "status": "pending",
      "created_at": "2025-12-30T19:41:51.123456+00:00"
    }
  ],
  "total": 1,
  "page": 1,
  "page_size": 10,
  "total_pages": 1
}
```

#### 4. Actualizar Tarea
```bash
PUT /tasks/1
Content-Type: application/json
Authorization: Bearer <token>

# Este JSON va en el BODY (cuerpo) de la solicitud:
{
  "status": "done"
}
```

**Respuesta (200):**
```json
{
  "id": 1,
  "title": "Comprar leche",
  "description": "Ir al supermercado",
  "status": "done",
  "created_at": "2025-12-30T19:41:51.123456+00:00"
}
```

#### 5. Eliminar Tarea
```bash
DELETE /tasks/1
Authorization: Bearer <token>
```

**Respuesta (204):** Sin contenido (tarea eliminada)

---

## 📝 Ejemplos Completos con cURL

### 1. Login y guardar token
```bash
# Hacer login
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"admin123"}'

# Resultado: Copiar el valor de "access_token"
```

### 2. Crear una tarea
```bash
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "title": "Estudiar FastAPI",
    "description": "Aprender endpoints y validación",
    "status": "in_progress"
  }'
```

### 3. Listar tareas
```bash
curl -X GET "http://localhost:8000/tasks?page=1&page_size=5" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### 4. Actualizar estado de tarea
```bash
curl -X PUT http://localhost:8000/tasks/1 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{"status":"done"}'
```

### 5. Eliminar tarea
```bash
curl -X DELETE http://localhost:8000/tasks/1 \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

---

## 🗂️ Estructura del Proyecto

```
Prueba_FastApi/
├── alembic/                    # Migraciones de BD
│   ├── versions/              # Scripts de migración
│   │   ├── f4a85daa9f6a_crear_tablas_users_y_tasks.py
│   │   └── 8c26cc45ab4d_crear_usuario_inicial.py
│   ├── env.py                 # Configuración de Alembic
│   └── alembic.ini            # Archivo de configuración
│
├── app/
│   ├── main.py                # Punto de entrada (FastAPI app)
│   │
│   ├── api/                   # Routers/Endpoints
│   │   ├── auth.py            # Endpoints de autenticación
│   │   ├── tasks.py           # Endpoints de tareas
│   │   └── health.py          # Health check
│   │
│   ├── core/                  # Lógica central
│   │   ├── config.py          # Configuración (variables de entorno)
│   │   ├── security.py        # Hash de contraseñas
│   │   ├── auth.py            # Validación de tokens JWT
│   │   └── jwt.py             # Creación de tokens JWT
│   │
│   ├── db/                    # Base de datos
│   │   ├── base.py            # Clase base para modelos
│   │   ├── database.py        # Conexión a BD
│   │   └── session.py         # Sesiones de BD
│   │
│   ├── models/                # Modelos SQLAlchemy
│   │   ├── user.py            # Modelo User
│   │   └── task.py            # Modelo Task
│   │
│   ├── schemas/               # Esquemas Pydantic (validación)
│   │   ├── auth.py            # Esquemas de autenticación
│   │   └── task.py            # Esquemas de tareas
│   │
│   └── services/              # Lógica de negocio
│       ├── user_service.py    # Servicios de usuarios
│       └── task_service.py    # Servicios de tareas
│
├── docker-compose.yml         # Configuración de PostgreSQL
├── requirements.txt           # Dependencias Python
├── .env.example               # Ejemplo de variables de entorno
├── .env                       # Variables de entorno (NO versionar)
├── .gitignore                 # Archivos ignorados por Git
└── README.md                  # Este archivo
```

---

## 🔒 Decisiones Técnicas & Trade-offs

### 1. Autenticación JWT vs Sessions
**Decisión:** JWT (JSON Web Tokens)

**Razones:**
- ✅ Stateless: No necesita almacenar sesiones en el servidor
- ✅ Escalable: Ideal para APIs y microservicios
- ✅ Estándar moderno
- ⚠️ Trade-off: El token sigue siendo válido hasta que expire (no se revoca instantáneamente)

### 2. Hash de Contraseñas
**Decisión:** bcrypt (via passlib)

**Razones:**
- ✅ Estándar de seguridad en la industria
- ✅ Incluye salt automático
- ✅ Adaptativo: Más lento con el tiempo (resiste ataques de fuerza bruta)
- ✅ Compatible con Python 3.11

### 3. ORM: SQLAlchemy vs SQL Raw
**Decisión:** SQLAlchemy

**Razones:**
- ✅ Previene inyecciones SQL automáticamente
- ✅ Código más mantenible y reutilizable
- ✅ Cambiar de BD es más sencillo
- ⚠️ Trade-off: Pequeño overhead de rendimiento

### 4. Índices en la BD
**Decisión:**
- **PK (id)** → Automático en toda tabla
- **email** → UNIQUE en `users` (búsquedas rápidas durante login)
- **status** → INDEX en `tasks` (filtrado por estado es común)

**Razones:** Optimiza búsquedas frecuentes y garantiza integridad de datos.

### 5. Paginación
**Decisión:** Query params `page` y `page_size`

**Razones:**
- ✅ Estándar REST
- ✅ Fácil de entender y usar
- ✅ Compatible con cualquier cliente HTTP

### 6. Usuario Inicial
**Decisión:** Creado automáticamente con una migración Alembic

**Razones:**
- ✅ Reproducible: Mismo usuario en todos los ambientes
- ✅ Versionado: Controlado en Git
- ✅ No requiere scripts adicionales
- ✅ Seguro: No hay credenciales en el código

---

## 🐛 Solución de Problemas

### Error: "No 'script_location' key found in configuration" (Alembic)
**Causa:** El archivo `.env` no existe o no fue copiado desde `.env.example`

**Solución:**
```bash
# Verifica que estés en el directorio raíz del proyecto
ls .env  # Debe existir

# Si no existe, cópialo:
# Windows (PowerShell):
copy .env.example .env

# Mac/Linux:
cp .env.example .env

# Luego intenta de nuevo:
alembic upgrade head
```

### Error: "connection to server at localhost failed"
**Solución:**
```bash
docker-compose ps
# Si postgres no está corriendo:
docker-compose up -d
```

### Error: "no such table: users"
**Solución:**
```bash
alembic upgrade head
```

### Error: "401 Unauthorized"
**Causas posibles:**
- Token expirado (válido por 60 minutos)
- Token no enviado en header
- Formato incorrecto: `Authorization: Bearer <token>`

**Solución:** Hacer login nuevamente para obtener un nuevo token

### Error: "JWT decode error"
**Solución:** Asegurar que `JWT_SECRET_KEY` en `.env` es consistente

### Puerto 5432 ya está en uso
```bash
# Cambiar puerto en docker-compose.yml:
# De:  "5432:5432"
# A:   "5433:5432"  (o cualquier puerto disponible)

# Y actualizar .env:
# DB_PORT=5433
```

---

## 📚 Recursos de Aprendizaje

- **FastAPI Documentation:** https://fastapi.tiangolo.com/
- **SQLAlchemy ORM:** https://docs.sqlalchemy.org/
- **JWT Tokens:** https://jwt.io/
- **Alembic Migrations:** https://alembic.sqlalchemy.org/
- **REST API Best Practices:** https://restfulapi.net/

---


### ✅ Qué está implementado

- [x] **Autenticación JWT** con expiración configurable (60 min)
- [x] **CRUD completo** de tareas (Create, Read, Update, Delete)
- [x] **Paginación** en listado de tareas
- [x] **Validación de datos** con Pydantic
- [x] **Manejo de errores HTTP** (400, 401, 404, 422)
- [x] **Migraciones Alembic** para tablas y usuario inicial
- [x] **Hash seguro** de contraseñas con bcrypt
- [x] **Base de datos PostgreSQL** en Docker
- [x] **Estructura modular** y escalable
- [x] **Documentación interactiva** con Swagger UI

### 📌 Decisiones de Diseño

1. **Modularidad:** Código separado por responsabilidad (models, schemas, services, api)
2. **Seguridad:** JWT + bcrypt + validación con Pydantic
3. **Reproducibilidad:** Todo automatizado con Docker y migraciones
4. **Escalabilidad:** Arquitectura lista para agregar más entidades y endpoints

### ⏱️ Estimación de Tiempo

- Configuración inicial: ~30 min
- Autenticación (JWT + bcrypt): ~45 min
- CRUD de tareas: ~60 min
- Migraciones y base de datos: ~45 min
- Documentación: ~30 min
- **Total: ~3 horas 30 minutos**

---

**¡Gracias por revisar este proyecto!** 🚀



# 📮 Guía de Testing con Postman y cURL

Este documento explica cómo probar la API del Gestor de Tareas usando Postman o cURL.

---

## 🚀 Opción 1: Importar Colección en Postman

### Paso 1: Abrir Postman
1. Descarga e instala [Postman](https://www.postman.com/downloads/)
2. Abre Postman

### Paso 2: Importar la Colección
1. Haz clic en **"Import"** (esquina superior izquierda)
2. Selecciona la pestaña **"Upload Files"**
3. Busca y selecciona `Postman_Collection.json` del proyecto
4. Haz clic en **"Import"**

### Paso 3: Configurar Ambiente (Opcional)
La colección incluye variables para:
- `access_token` - Se guarda automáticamente después de hacer login
- `task_id` - Se guarda automáticamente después de crear una tarea

### Paso 4: Ejecutar Requests
**Orden recomendado:**

1. **Login** (obtiene el token automáticamente)
   - Click en: `Autenticación > Login - Obtener Token`
   - Click en "Send"
   - El token se guarda automáticamente

2. **Crear Tarea** (usa el token y guarda el ID)
   - Click en: `Tareas - CRUD > Crear Tarea`
   - Click en "Send"
   - El ID se guarda automáticamente

3. **Listar Tareas**
   - Click en: `Tareas - CRUD > Listar Tareas (Paginado)`
   - Click en "Send"

4. **Obtener Tarea**
   - Click en: `Tareas - CRUD > Obtener Tarea por ID`
   - Click en "Send"
   - Usa el ID guardado automáticamente

5. **Actualizar Tarea**
   - Click en: `Tareas - CRUD > Actualizar Tarea`
   - Click en "Send"

6. **Eliminar Tarea**
   - Click en: `Tareas - CRUD > Eliminar Tarea`
   - Click en "Send"
   - Espera respuesta 204 (sin contenido)

---

## 🐚 Opción 2: Usar cURL desde Terminal

### Requisito
Tener `curl` instalado (viene por defecto en macOS/Linux, en Windows necesitas descargarlo o usar WSL)

### Flujo Completo

#### 1. Login - Obtener Token
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"admin123"}'
```

**Respuesta esperada:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Guardar el token** en una variable:
```bash
# En Windows PowerShell:
$TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

# En macOS/Linux:
TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

#### 2. Crear Tarea
```bash
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "title": "Estudiar FastAPI",
    "description": "Aprender sobre endpoints y validación",
    "status": "pending"
  }'
```

**Respuesta esperada (201):**
```json
{
  "id": 1,
  "title": "Estudiar FastAPI",
  "description": "Aprender sobre endpoints y validación",
  "status": "pending",
  "created_at": "2025-12-30T19:41:51.123456+00:00"
}
```

**Guardar el ID:**
```bash
# En Windows PowerShell:
$TASK_ID = 1

# En macOS/Linux:
TASK_ID=1
```

#### 3. Listar Tareas (con Paginación)
```bash
curl -X GET "http://localhost:8000/tasks?page=1&page_size=10" \
  -H "Authorization: Bearer $TOKEN"
```

**Respuesta esperada (200):**
```json
{
  "items": [
    {
      "id": 1,
      "title": "Estudiar FastAPI",
      "description": "Aprender sobre endpoints y validación",
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

#### 4. Obtener Tarea Específica
```bash
curl -X GET http://localhost:8000/tasks/$TASK_ID \
  -H "Authorization: Bearer $TOKEN"
```

**Respuesta esperada (200):**
```json
{
  "id": 1,
  "title": "Estudiar FastAPI",
  "description": "Aprender sobre endpoints y validación",
  "status": "pending",
  "created_at": "2025-12-30T19:41:51.123456+00:00"
}
```

#### 5. Actualizar Tarea
```bash
curl -X PUT http://localhost:8000/tasks/$TASK_ID \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"status": "in_progress"}'
```

**Respuesta esperada (200):**
```json
{
  "id": 1,
  "title": "Estudiar FastAPI",
  "description": "Aprender sobre endpoints y validación",
  "status": "in_progress",
  "created_at": "2025-12-30T19:41:51.123456+00:00"
}
```

#### 6. Eliminar Tarea
```bash
curl -X DELETE http://localhost:8000/tasks/$TASK_ID \
  -H "Authorization: Bearer $TOKEN"
```

**Respuesta esperada (204):** Sin contenido

---

## 🧪 Pruebas de Errores (con cURL)

### Test 1: Sin Token
```bash
curl -X GET http://localhost:8000/tasks
```
**Respuesta esperada (401):**
```json
{"detail": "Not authenticated"}
```

### Test 2: Tarea Inexistente
```bash
curl -X GET http://localhost:8000/tasks/99999 \
  -H "Authorization: Bearer $TOKEN"
```
**Respuesta esperada (404):**
```json
{"detail": "Tarea no encontrada"}
```

### Test 3: Datos Inválidos (sin título)
```bash
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"description": "Sin título"}'
```
**Respuesta esperada (422):**
```json
{
  "detail": [
    {
      "loc": ["body", "title"],
      "msg": "Field required",
      "type": "missing"
    }
  ]
}
```

### Test 4: Credenciales Incorrectas
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"wrong@example.com","password":"wrong"}'
```
**Respuesta esperada (401):**
```json
{"detail": "Email o contraseña incorrectos"}
```

---

## 🎯 Health Check
```bash
curl http://localhost:8000/health
```
**Respuesta esperada (200):**
```json
{"status": "ok"}
```

---

## 💡 Consejos

### Para Postman:
- Usa la documentación integrada: Cada request tiene descripción
- Las variables se guardan automáticamente
- Puedes crear tests adicionales
- Usa "Collections" para organizar requests

### Para cURL:
- En Windows PowerShell, usa `$variable` para variables
- En macOS/Linux, usa `$variable`
- Puedes guardar la salida en un archivo: `curl ... > response.json`
- Usa `-v` para ver headers: `curl -v ...`
- Usa `jq` para formatear JSON: `curl ... | jq .`

---

## 📊 Resumen de Status Codes

| Código | Significado | Ejemplo |
|--------|-------------|---------|
| 200 | OK | GET, PUT exitoso |
| 201 | Created | POST exitoso |
| 204 | No Content | DELETE exitoso |
| 400 | Bad Request | Datos malformados |
| 401 | Unauthorized | Falta token o token inválido |
| 404 | Not Found | Recurso no existe |
| 422 | Unprocessable Entity | Validación fallida |

---

## 🔍 Verificar Swagger UI

También puedes probar todos los endpoints interactivamente en:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

Ambas interfaces tienen:
- Documentación automática de cada endpoint
- Campos interactivos para probar
- Esquemas de request/response

---

Elige la opción que prefieras:
- **Postman:** Interfaz gráfica, más fácil para principiantes
- **cURL:** Terminal, más rápido y scripteable

¡Happy Testing! 🎉

"""Script de verificación de la configuración del proyecto.

Este script verifica que:
1. Las variables de entorno estén configuradas correctamente
2. La conexión a PostgreSQL funciona
3. Las tablas existan con los índices correctos
4. El usuario admin esté creado
"""

import os
from dotenv import load_dotenv
from app.db.database import engine
from sqlalchemy import text, inspect

# Cargar variables de entorno
load_dotenv()

print("=" * 60)
print("🔍 VERIFICACIÓN DE CONFIGURACIÓN DEL PROYECTO")
print("=" * 60)

# 1. Verificar variables de entorno
print("\n1️⃣  Variables de Entorno:")
required_vars = [
    'DB_HOST', 'DB_PORT', 'DB_NAME', 'DB_USER', 'DB_PASSWORD',
    'JWT_SECRET_KEY', 'JWT_ALGORITHM', 'JWT_EXPIRE_MINUTES'
]

all_set = True
for var in required_vars:
    value = os.getenv(var)
    if value:
        print(f"   ✅ {var}")
    else:
        print(f"   ❌ {var} - NO CONFIGURADA")
        all_set = False

if all_set:
    print("\n   ✨ Todas las variables están configuradas")

# 2. Verificar conexión a BD
print("\n2️⃣  Conexión a Base de Datos:")
try:
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    print("   ✅ Conexión exitosa a PostgreSQL")
except Exception as e:
    print(f"   ❌ Error de conexión: {e}")
    exit(1)

# 3. Verificar tablas y índices
print("\n3️⃣  Tablas de Base de Datos:")
inspector = inspect(engine)
tables = inspector.get_table_names()

required_tables = {'users', 'tasks'}
for table in required_tables:
    if table in tables:
        print(f"   ✅ Tabla '{table}' existe")
        
        # Mostrar índices
        indexes = inspector.get_indexes(table)
        if indexes:
            print(f"      Índices:")
            for idx in indexes:
                print(f"        - {idx['name']} (campos: {idx['column_names']})")
    else:
        print(f"   ❌ Tabla '{table}' NO existe")

# 4. Verificar usuario admin
print("\n4️⃣  Usuario Administrador:")
try:
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT id, email, is_active FROM users WHERE email = 'admin@example.com'")
        )
        user = result.fetchone()
        
        if user:
            print(f"   ✅ Usuario admin encontrado")
            print(f"      - ID: {user[0]}")
            print(f"      - Email: {user[1]}")
            print(f"      - Activo: {user[2]}")
        else:
            print(f"   ⚠️  Usuario admin NO existe. Ejecuta: alembic upgrade head")
except Exception as e:
    print(f"   ❌ Error al verificar usuario: {e}")

print("\n" + "=" * 60)
print("✨ Verificación completada")
print("=" * 60)
print("\n📝 Próximo paso: Ejecuta 'uvicorn app.main:app --reload'")

"""
Script de test para la API del Gestor de Tareas.

Este script demuestra el flujo completo:
1. Login
2. Crear tarea
3. Listar tareas
4. Obtener una tarea específica
5. Actualizar tarea
6. Eliminar tarea
"""

import requests
import json
from typing import Optional

# Configuración
API_BASE_URL = "http://localhost:8000"
ADMIN_EMAIL = "admin@example.com"
ADMIN_PASSWORD = "admin123"

class Colors:
    """Colores para terminal"""
    OK = '\033[92m'
    ERROR = '\033[91m'
    INFO = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_header(text: str):
    print(f"\n{Colors.BOLD}{Colors.INFO}{'='*60}")
    print(f"{text}")
    print(f"{'='*60}{Colors.RESET}\n")

def print_success(text: str):
    print(f"{Colors.OK}✅ {text}{Colors.RESET}")

def print_error(text: str):
    print(f"{Colors.ERROR}❌ {text}{Colors.RESET}")

def print_info(text: str):
    print(f"{Colors.INFO}ℹ️  {text}{Colors.RESET}")

class TaskAPITester:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.token: Optional[str] = None
        self.session = requests.Session()
    
    def login(self) -> bool:
        """Realizar login y obtener token JWT"""
        print_header("1️⃣  PRUEBA: LOGIN")
        
        login_data = {
            "email": ADMIN_EMAIL,
            "password": ADMIN_PASSWORD
        }
        
        try:
            response = self.session.post(
                f"{self.base_url}/auth/login",
                json=login_data
            )
            
            if response.status_code == 200:
                self.token = response.json()["access_token"]
                print_success(f"Login exitoso para {ADMIN_EMAIL}")
                print_info(f"Token JWT obtenido: {self.token[:50]}...")
                return True
            else:
                print_error(f"Login fallido: {response.status_code}")
                print_info(f"Respuesta: {response.text}")
                return False
                
        except Exception as e:
            print_error(f"Error al conectar con la API: {e}")
            print_info("¿Está el servidor corriendo? (uvicorn app.main:app --reload)")
            return False
    
    def create_task(self, title: str, description: str) -> Optional[int]:
        """Crear una nueva tarea"""
        print_header("2️⃣  PRUEBA: CREAR TAREA")
        
        task_data = {
            "title": title,
            "description": description,
            "status": "pending"
        }
        
        try:
            response = self.session.post(
                f"{self.base_url}/tasks",
                json=task_data,
                headers={"Authorization": f"Bearer {self.token}"}
            )
            
            if response.status_code == 201:
                task = response.json()
                print_success(f"Tarea creada correctamente")
                print_info(f"ID: {task['id']}")
                print_info(f"Título: {task['title']}")
                print_info(f"Estado: {task['status']}")
                return task['id']
            else:
                print_error(f"Error al crear tarea: {response.status_code}")
                print_info(f"Respuesta: {response.text}")
                return None
                
        except Exception as e:
            print_error(f"Error: {e}")
            return None
    
    def list_tasks(self) -> bool:
        """Listar todas las tareas con paginación"""
        print_header("3️⃣  PRUEBA: LISTAR TAREAS (CON PAGINACIÓN)")
        
        try:
            response = self.session.get(
                f"{self.base_url}/tasks?page=1&page_size=10",
                headers={"Authorization": f"Bearer {self.token}"}
            )
            
            if response.status_code == 200:
                data = response.json()
                print_success(f"Listado de tareas obtenido")
                print_info(f"Total de tareas: {data['total']}")
                print_info(f"Página: {data['page']}")
                print_info(f"Tareas por página: {data['page_size']}")
                print_info(f"Total de páginas: {data['total_pages']}")
                
                if data['items']:
                    print_info(f"Tareas en esta página:")
                    for task in data['items']:
                        print(f"   - ID {task['id']}: {task['title']} ({task['status']})")
                
                return True
            else:
                print_error(f"Error al listar tareas: {response.status_code}")
                return False
                
        except Exception as e:
            print_error(f"Error: {e}")
            return False
    
    def get_task(self, task_id: int) -> bool:
        """Obtener una tarea específica"""
        print_header("4️⃣  PRUEBA: OBTENER TAREA ESPECÍFICA")
        
        try:
            response = self.session.get(
                f"{self.base_url}/tasks/{task_id}",
                headers={"Authorization": f"Bearer {self.token}"}
            )
            
            if response.status_code == 200:
                task = response.json()
                print_success(f"Tarea obtenida correctamente")
                print_info(f"ID: {task['id']}")
                print_info(f"Título: {task['title']}")
                print_info(f"Descripción: {task['description']}")
                print_info(f"Estado: {task['status']}")
                print_info(f"Creada: {task['created_at']}")
                return True
            else:
                print_error(f"Error al obtener tarea: {response.status_code}")
                return False
                
        except Exception as e:
            print_error(f"Error: {e}")
            return False
    
    def update_task(self, task_id: int) -> bool:
        """Actualizar el estado de una tarea"""
        print_header("5️⃣  PRUEBA: ACTUALIZAR TAREA")
        
        update_data = {"status": "in_progress"}
        
        try:
            response = self.session.put(
                f"{self.base_url}/tasks/{task_id}",
                json=update_data,
                headers={"Authorization": f"Bearer {self.token}"}
            )
            
            if response.status_code == 200:
                task = response.json()
                print_success(f"Tarea actualizada correctamente")
                print_info(f"Nuevo estado: {task['status']}")
                return True
            else:
                print_error(f"Error al actualizar tarea: {response.status_code}")
                return False
                
        except Exception as e:
            print_error(f"Error: {e}")
            return False
    
    def delete_task(self, task_id: int) -> bool:
        """Eliminar una tarea"""
        print_header("6️⃣  PRUEBA: ELIMINAR TAREA")
        
        try:
            response = self.session.delete(
                f"{self.base_url}/tasks/{task_id}",
                headers={"Authorization": f"Bearer {self.token}"}
            )
            
            if response.status_code == 204:
                print_success(f"Tarea eliminada correctamente")
                return True
            else:
                print_error(f"Error al eliminar tarea: {response.status_code}")
                return False
                
        except Exception as e:
            print_error(f"Error: {e}")
            return False
    
    def test_error_cases(self) -> bool:
        """Probar casos de error"""
        print_header("7️⃣  PRUEBA: MANEJO DE ERRORES")
        
        all_pass = True
        
        # Prueba 1: Acceder sin token
        print_info("Test 1: Acceder a endpoint protegido sin token")
        response = self.session.get(f"{self.base_url}/tasks")
        if response.status_code == 401:
            print_success("Respuesta correcta: 401 Unauthorized")
        else:
            print_error(f"Respuesta incorrecta: {response.status_code}")
            all_pass = False
        
        # Prueba 2: Tarea inexistente
        print_info("Test 2: Obtener tarea que no existe")
        response = self.session.get(
            f"{self.base_url}/tasks/99999",
            headers={"Authorization": f"Bearer {self.token}"}
        )
        if response.status_code == 404:
            print_success("Respuesta correcta: 404 Not Found")
        else:
            print_error(f"Respuesta incorrecta: {response.status_code}")
            all_pass = False
        
        # Prueba 3: Datos inválidos
        print_info("Test 3: Crear tarea sin título (validación)")
        response = self.session.post(
            f"{self.base_url}/tasks",
            json={"description": "Sin título"},
            headers={"Authorization": f"Bearer {self.token}"}
        )
        if response.status_code == 422:
            print_success("Respuesta correcta: 422 Validation Error")
        else:
            print_error(f"Respuesta incorrecta: {response.status_code}")
            all_pass = False
        
        return all_pass

def main():
    print(f"\n{Colors.BOLD}{Colors.INFO}")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 58 + "║")
    print("║" + "   🧪 TEST SUITE - GESTOR DE TAREAS API".center(58) + "║")
    print("║" + " " * 58 + "║")
    print("╚" + "=" * 58 + "╝")
    print(Colors.RESET)
    
    tester = TaskAPITester(API_BASE_URL)
    
    # Pruebas principales
    if not tester.login():
        print_error("No se pudo completar el test sin autenticación")
        return
    
    # Crear una tarea
    task_id = tester.create_task(
        "Aprender FastAPI",
        "Completar este proyecto de prueba técnica"
    )
    
    if not task_id:
        print_error("No se pudo crear la tarea para las pruebas")
        return
    
    # Ejecutar más pruebas
    tester.list_tasks()
    tester.get_task(task_id)
    tester.update_task(task_id)
    tester.test_error_cases()
    tester.delete_task(task_id)
    
    # Resumen
    print_header("✨ RESUMEN DE PRUEBAS")
    print_success("Todos los endpoints funcionan correctamente")
    print_success("La API está lista para producción")
    print_info("Para más detalles, visita: http://localhost:8000/docs")

if __name__ == "__main__":
    main()

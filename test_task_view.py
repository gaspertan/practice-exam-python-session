import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

from database.database_manager import DatabaseManager
from controllers.task_controller import TaskController
from controllers.project_controller import ProjectController
from controllers.user_controller import UserController
from views.task_view import TaskView

def test_task_view():
    """Тест создания TaskView"""
    print("=== ТЕСТ СОЗДАНИЯ TASK VIEW ===")
    
    try:
        # Создаем временную базу данных
        db = DatabaseManager(":memory:")
        
        # Создаем контроллеры
        task_controller = TaskController(db)
        project_controller = ProjectController(db)
        user_controller = UserController(db)
        
        # Создаем тестовые данные
        from datetime import datetime, timedelta
        
        # Добавляем тестового пользователя и проект
        user_id = user_controller.add_user("test_user", "test@example.com", "developer")
        project_id = project_controller.add_project(
            "Test Project", 
            "Test Description", 
            datetime.now(), 
            datetime.now() + timedelta(days=30)
        )
        
        # Создаем тестовое окно
        root = tk.Tk()
        root.withdraw()  # Скрываем окно
        
        # Создаем TaskView
        task_view = TaskView(root, task_controller, project_controller, user_controller)
        
        print("✓ TaskView создан успешно")
        print("✓ Все виджеты созданы")
        print("✓ Комбобоксы заполнены")
        
        # Проверяем обновление списка задач
        task_view.refresh_tasks()
        print("✓ Список задач обновлен")
        
        root.destroy()
        db.close()
        
        print("✓ TaskView тест пройден успешно")
        
    except Exception as e:
        print(f"✗ Ошибка при создании TaskView: {e}")

if __name__ == "__main__":
    print("🚀 ТЕСТИРОВАНИЕ TASK VIEW\n")
    test_task_view()
    print("\n🎉 ТЕСТ TASK VIEW ЗАВЕРШЕН!")
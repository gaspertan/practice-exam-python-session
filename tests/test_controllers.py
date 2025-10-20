import sys
import os
import tempfile
from datetime import datetime, timedelta

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from database.database_manager import DatabaseManager
from controllers.task_controller import TaskController
from controllers.project_controller import ProjectController
from controllers.user_controller import UserController
from models.user import User as UserModel

def run_controller_tests():
    """Запуск тестов контроллеров"""
    print(" ЗАПУСК ТЕСТОВ КОНТРОЛЛЕРОВ")
    
    
    tests_passed = 0
    tests_failed = 0
    
    # Создаем временную базу данных
    temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
    db_manager = DatabaseManager(temp_db.name)
    
    try:
        # Создаем контроллеры
        task_controller = TaskController(db_manager)
        project_controller = ProjectController(db_manager)
        user_controller = UserController(db_manager)
        
        print("\n ТЕСТЫ TASK CONTROLLER ")
        
        try:
            # Test 1: Добавление задачи
            due_date = datetime.now() + timedelta(days=7)
            task_id = task_controller.add_task(
                title="Test Task",
                description="Test Description", 
                priority=2,
                due_date=due_date,
                project_id=1,
                assignee_id=1
            )
            assert task_id == 1
            print("✓ test_add_task - ПРОЙДЕН")
            tests_passed += 1
        except Exception as e:
            print(f"✗ test_add_task - ОШИБКА: {e}")
            tests_failed += 1
        
        try:
            # Test 2: Получение задачи
            task = task_controller.get_task(1)
            assert task is not None
            assert task.title == "Test Task"
            print("✓ test_get_task - ПРОЙДЕН")
            tests_passed += 1
        except Exception as e:
            print(f"✗ test_get_task - ОШИБКА: {e}")
            tests_failed += 1
        
        try:
            # Test 3: Получение всех задач
            tasks = task_controller.get_all_tasks()
            assert len(tasks) == 1
            assert tasks[0].title == "Test Task"
            print("✓ test_get_all_tasks - ПРОЙДЕН")
            tests_passed += 1
        except Exception as e:
            print(f"✗ test_get_all_tasks - ОШИБКА: {e}")
            tests_failed += 1
        
        try:
            # Test 4: Обновление статуса задачи
            result = task_controller.update_task_status(1, "in_progress")
            assert result == True
            updated_task = task_controller.get_task(1)
            assert updated_task.status == "in_progress"
            print("✓ test_update_task_status - ПРОЙДЕН")
            tests_passed += 1
        except Exception as e:
            print(f"✗ test_update_task_status - ОШИБКА: {e}")
            tests_failed += 1
        
        try:
            # Test 5: Поиск задач
            results = task_controller.search_tasks("Test")
            assert len(results) == 1
            print("✓ test_search_tasks - ПРОЙДЕН")
            tests_passed += 1
        except Exception as e:
            print(f"✗ test_search_tasks - ОШИБКА: {e}")
            tests_failed += 1
        
        try:
            # Test 6: Валидация приоритета
            try:
                task_controller.add_task("Invalid", "Desc", 5, datetime.now(), 1, 1)
                print("✗ test_priority_validation - ОШИБКА: Невалидный приоритет прошел")
                tests_failed += 1
            except ValueError:
                print("✓ test_priority_validation - ПРОЙДЕН")
                tests_passed += 1
        except Exception as e:
            print(f"✗ test_priority_validation - ОШИБКА: {e}")
            tests_failed += 1
        
        print("\n ТЕСТЫ PROJECT CONTROLLER ")
        
        try:
            # Test 7: Добавление проекта
            project_id = project_controller.add_project(
                "Test Project",
                "Test Description",
                datetime.now() + timedelta(days=1),
                datetime.now() + timedelta(days=30)
            )
            assert project_id == 1
            print("✓ test_add_project - ПРОЙДЕН")
            tests_passed += 1
        except Exception as e:
            print(f"✗ test_add_project - ОШИБКА: {e}")
            tests_failed += 1
        
        try:
            # Test 8: Получение проекта
            project = project_controller.get_project(1)
            assert project is not None
            assert project.name == "Test Project"
            print("✓ test_get_project - ПРОЙДЕН")
            tests_passed += 1
        except Exception as e:
            print(f"✗ test_get_project - ОШИБКА: {e}")
            tests_failed += 1
        
        try:
            # Test 9: Обновление статуса проекта
            result = project_controller.update_project_status(1, "completed")
            assert result == True
            updated_project = project_controller.get_project(1)
            assert updated_project.status == "completed"
            print("✓ test_update_project_status - ПРОЙДЕН")
            tests_passed += 1
        except Exception as e:
            print(f"✗ test_update_project_status - ОШИБКА: {e}")
            tests_failed += 1
        
        print("\n ТЕСТЫ USER CONTROLLER ")
        
        try:
            # Test 10: Добавление пользователя
            user_id = user_controller.add_user(
                "testuser",
                "test@example.com", 
                "developer"
            )
            assert user_id == 1
            print("✓ test_add_user - ПРОЙДЕН")
            tests_passed += 1
        except Exception as e:
            print(f"✗ test_add_user - ОШИБКА: {e}")
            tests_failed += 1
        
        try:
            # Test 11: Получение пользователя
            user = user_controller.get_user(1)
            assert user is not None
            assert user.username == "testuser"
            print("✓ test_get_user - ПРОЙДЕН")
            tests_passed += 1
        except Exception as e:
            print(f"✗ test_get_user - ОШИБКА: {e}")
            tests_failed += 1
        
        try:
            # Test 12: Обновление пользователя
            result = user_controller.update_user(1, username="updateduser", role="admin")
            assert result == True
            updated_user = user_controller.get_user(1)
            assert updated_user.username == "updateduser"
            assert updated_user.role == "admin"
            print("✓ test_update_user - ПРОЙДЕН")
            tests_passed += 1
        except Exception as e:
            print(f"✗ test_update_user - ОШИБКА: {e}")
            tests_failed += 1
        
        try:
            # Test 13: Валидация роли пользователя
            try:
                user_controller.add_user("invalid", "test@example.com", "invalid_role")
                print("✗ test_user_role_validation - ОШИБКА: Невалидная роль прошел")
                tests_failed += 1
            except ValueError:
                print("✓ test_user_role_validation - ПРОЙДЕН")
                tests_passed += 1
        except Exception as e:
            print(f"✗ test_user_role_validation - ОШИБКА: {e}")
            tests_failed += 1
        
    finally:
        # Очистка
        db_manager.close()
        os.unlink(temp_db.name)
    
    # Итоги
    
    print(f"ИТОГ: {tests_passed} пройдено, {tests_failed} не пройдено")
    
    if tests_failed == 0:
        print(" ВСЕ ТЕСТЫ КОНТРОЛЛЕРОВ ПРОЙДЕНЫ УСПЕШНО!")
    else:
        print(" Есть непройденные тесты!!!")
    
    return tests_passed, tests_failed

if __name__ == "__main__":
    run_controller_tests()
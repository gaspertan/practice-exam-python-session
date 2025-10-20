import sys
import os
import tempfile
from datetime import datetime, timedelta

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from database.database_manager import DatabaseManager
from models.task import Task
from models.project import Project
from models.user import User

def run_database_tests():
    """Запуск тестов базы данных"""
    print(" ЗАПУСК ТЕСТОВ БАЗЫ ДАННЫХ")
    
    
    tests_passed = 0
    tests_failed = 0
    
    # Создаем временную базу данных
    temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
    db_manager = DatabaseManager(temp_db.name)
    
    try:
        print("\nТЕСТЫ СОЗДАНИЯ ТАБЛИЦ ")
        
        try:
            # Test 1: Проверка создания таблиц
            # Таблицы создаются автоматически в конструкторе DatabaseManager
            # Проверяем что можем выполнять запросы к таблицам
            users = db_manager.get_all_users()
            projects = db_manager.get_all_projects()
            tasks = db_manager.get_all_tasks()
            
            # Должны вернуться пустые списки, а не ошибки
            assert isinstance(users, list)
            assert isinstance(projects, list)
            assert isinstance(tasks, list)
            print("✓ test_create_tables - ПРОЙДЕН")
            tests_passed += 1
        except Exception as e:
            print(f"✗ test_create_tables - ОШИБКА: {e}")
            tests_failed += 1
        
        print("\n ТЕСТЫ ОПЕРАЦИЙ С ПОЛЬЗОВАТЕЛЯМИ ")
        
        try:
            # Test 2: Добавление пользователя
            user = User("testuser", "test@example.com", "developer")
            user_id = db_manager.add_user(user)
            assert user_id == 1
            assert user.id == 1
            print("✓ test_add_user - ПРОЙДЕН")
            tests_passed += 1
        except Exception as e:
            print(f"✗ test_add_user - ОШИБКА: {e}")
            tests_failed += 1
        
        try:
            # Test 3: Получение пользователя по ID
            user = db_manager.get_user_by_id(1)
            assert user is not None
            assert user.username == "testuser"
            assert user.email == "test@example.com"
            assert user.role == "developer"
            print("✓ test_get_user_by_id - ПРОЙДЕН")
            tests_passed += 1
        except Exception as e:
            print(f"✗ test_get_user_by_id - ОШИБКА: {e}")
            tests_failed += 1
        
        try:
            # Test 4: Получение всех пользователей
            users = db_manager.get_all_users()
            assert len(users) == 1
            assert users[0].username == "testuser"
            print("✓ test_get_all_users - ПРОЙДЕН")
            tests_passed += 1
        except Exception as e:
            print(f"✗ test_get_all_users - ОШИБКА: {e}")
            tests_failed += 1
        
        try:
            # Test 5: Обновление пользователя
            result = db_manager.update_user(1, username="updateduser", role="admin")
            assert result == True
            updated_user = db_manager.get_user_by_id(1)
            assert updated_user.username == "updateduser"
            assert updated_user.role == "admin"
            print("✓ test_update_user - ПРОЙДЕН")
            tests_passed += 1
        except Exception as e:
            print(f"✗ test_update_user - ОШИБКА: {e}")
            tests_failed += 1
        
        print("\n ТЕСТЫ ОПЕРАЦИЙ С ПРОЕКТАМИ ")
        
        try:
            # Test 6: Добавление проекта
            project = Project(
                "Test Project",
                "Test Description",
                datetime.now() + timedelta(days=1),
                datetime.now() + timedelta(days=30)
            )
            project_id = db_manager.add_project(project)
            assert project_id == 1
            assert project.id == 1
            print("✓ test_add_project - ПРОЙДЕН")
            tests_passed += 1
        except Exception as e:
            print(f"✗ test_add_project - ОШИБКА: {e}")
            tests_failed += 1
        
        try:
            # Test 7: Получение проекта по ID
            project = db_manager.get_project_by_id(1)
            assert project is not None
            assert project.name == "Test Project"
            assert project.status == "active"
            print("✓ test_get_project_by_id - ПРОЙДЕН")
            tests_passed += 1
        except Exception as e:
            print(f"✗ test_get_project_by_id - ОШИБКА: {e}")
            tests_failed += 1
        
        try:
            # Test 8: Обновление проекта
            result = db_manager.update_project(1, name="Updated Project", status="completed")
            assert result == True
            updated_project = db_manager.get_project_by_id(1)
            assert updated_project.name == "Updated Project"
            assert updated_project.status == "completed"
            print("✓ test_update_project - ПРОЙДЕН")
            tests_passed += 1
        except Exception as e:
            print(f"✗ test_update_project - ОШИБКА: {e}")
            tests_failed += 1
        
        print("\n=== ТЕСТЫ ОПЕРАЦИЙ С ЗАДАЧАМИ ===")
        
        try:
            # Test 9: Добавление задачи
            task = Task(
                "Test Task",
                "Test Description",
                2,
                datetime.now() + timedelta(days=7),
                1,  # project_id
                1   # assignee_id
            )
            task_id = db_manager.add_task(task)
            assert task_id == 1
            assert task.id == 1
            print("✓ test_add_task - ПРОЙДЕН")
            tests_passed += 1
        except Exception as e:
            print(f"✗ test_add_task - ОШИБКА: {e}")
            tests_failed += 1
        
        try:
            # Test 10: Получение задачи по ID
            task = db_manager.get_task_by_id(1)
            assert task is not None
            assert task.title == "Test Task"
            assert task.priority == 2
            assert task.status == "pending"
            print("✓ test_get_task_by_id - ПРОЙДЕН")
            tests_passed += 1
        except Exception as e:
            print(f"✗ test_get_task_by_id - ОШИБКА: {e}")
            tests_failed += 1
        
        try:
            # Test 11: Получение всех задач
            tasks = db_manager.get_all_tasks()
            assert len(tasks) == 1
            assert tasks[0].title == "Test Task"
            print("✓ test_get_all_tasks - ПРОЙДЕН")
            tests_passed += 1
        except Exception as e:
            print(f"✗ test_get_all_tasks - ОШИБКА: {e}")
            tests_failed += 1
        
        try:
            # Test 12: Поиск задач
            tasks = db_manager.search_tasks("Test")
            assert len(tasks) == 1
            assert tasks[0].title == "Test Task"
            print("✓ test_search_tasks - ПРОЙДЕН")
            tests_passed += 1
        except Exception as e:
            print(f"✗ test_search_tasks - ОШИБКА: {e}")
            tests_failed += 1
        
        try:
            # Test 13: Получение задач по проекту
            tasks = db_manager.get_tasks_by_project(1)
            assert len(tasks) == 1
            assert tasks[0].project_id == 1
            print("✓ test_get_tasks_by_project - ПРОЙДЕН")
            tests_passed += 1
        except Exception as e:
            print(f"✗ test_get_tasks_by_project - ОШИБКА: {e}")
            tests_failed += 1
        
        try:
            # Test 14: Получение задач по пользователю
            tasks = db_manager.get_tasks_by_user(1)
            assert len(tasks) == 1
            assert tasks[0].assignee_id == 1
            print("✓ test_get_tasks_by_user - ПРОЙДЕН")
            tests_passed += 1
        except Exception as e:
            print(f"✗ test_get_tasks_by_user - ОШИБКА: {e}")
            tests_failed += 1
        
        try:
            # Test 15: Обновление задачи
            result = db_manager.update_task(1, status="in_progress", priority=1)
            assert result == True
            updated_task = db_manager.get_task_by_id(1)
            assert updated_task.status == "in_progress"
            assert updated_task.priority == 1
            print("✓ test_update_task - ПРОЙДЕН")
            tests_passed += 1
        except Exception as e:
            print(f"✗ test_update_task - ОШИБКА: {e}")
            tests_failed += 1
        
        try:
            # Test 16: Удаление задачи
            result = db_manager.delete_task(1)
            assert result == True
            deleted_task = db_manager.get_task_by_id(1)
            assert deleted_task is None
            print("✓ test_delete_task - ПРОЙДЕН")
            tests_passed += 1
        except Exception as e:
            print(f"✗ test_delete_task - ОШИБКА: {e}")
            tests_failed += 1
        
        print("\n ТЕСТЫ ЦЕЛОСТНОСТИ ДАННЫХ ")
        
        try:
            # Test 17: Проверка внешних ключей
            # Создаем новую задачу с существующими project_id и assignee_id
            task = Task("New Task", "Desc", 1, datetime.now(), 1, 1)
            task_id = db_manager.add_task(task)
            assert task_id == 2  # ID должен быть 2, так как первая задача удалена
            print("✓ test_foreign_keys - ПРОЙДЕН")
            tests_passed += 1
        except Exception as e:
            print(f"✗ test_foreign_keys - ОШИБКА: {e}")
            tests_failed += 1
        
    finally:
        # Очистка
        db_manager.close()
        os.unlink(temp_db.name)
    
    # Итоги
    
    print(f"ИТОГ: {tests_passed} пройдено, {tests_failed} не пройдено")
    
    if tests_failed == 0:
        print(" ВСЕ ТЕСТЫ БАЗЫ ДАННЫХ ПРОЙДЕНЫ УСПЕШНО!")
    else:
        print("  Есть непройденные тесты")
    
    return tests_passed, tests_failed

if __name__ == "__main__":
    run_database_tests()
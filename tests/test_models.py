import sys
import os
from datetime import datetime, timedelta

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from models.task import Task
from models.project import Project
from models.user import User

def run_tests():
    """Запуск тестов без использования pytest"""
    print("ЗАПУСК ТЕСТОВ МОДЕЛЕЙ")
    
    
    tests_passed = 0
    tests_failed = 0
    
    # Тесты для Task
    print("\n ТЕСТЫ КЛАССА TASK ")
    
    try:
        # Test 1: Создание задачи
        due_date = datetime.now() + timedelta(days=7)
        task = Task("Test Task", "Test Description", 2, due_date, 1, 1)
        assert task.title == "Test Task"
        assert task.status == "pending"
        print("✓ test_task_creation - ПРОЙДЕН")
        tests_passed += 1
    except Exception as e:
        print(f"✗ test_task_creation - ОШИБКА: {e}")
        tests_failed += 1
    
    try:
        # Test 2: Обновление статуса
        task = Task("Test", "Desc", 1, datetime.now(), 1, 1)
        assert task.update_status("in_progress") == True
        assert task.status == "in_progress"
        print("✓ test_task_update_status_valid - ПРОЙДЕН")
        tests_passed += 1
    except Exception as e:
        print(f"✗ test_task_update_status_valid - ОШИБКА: {e}")
        tests_failed += 1
    
    try:
        # Test 3: Невалидный статус
        task = Task("Test", "Desc", 1, datetime.now(), 1, 1)
        assert task.update_status("invalid_status") == False
        assert task.status == "pending"
        print("✓ test_task_update_status_invalid - ПРОЙДЕН")
        tests_passed += 1
    except Exception as e:
        print(f"✗ test_task_update_status_invalid - ОШИБКА: {e}")
        tests_failed += 1
    
    try:
        # Test 4: Проверка просрочки
        overdue_task = Task("Overdue", "Desc", 1, datetime.now() - timedelta(days=1), 1, 1)
        future_task = Task("Future", "Desc", 1, datetime.now() + timedelta(days=1), 1, 1)
        assert overdue_task.is_overdue() == True
        assert future_task.is_overdue() == False
        print("✓ test_task_is_overdue - ПРОЙДЕН")
        tests_passed += 1
    except Exception as e:
        print(f"✗ test_task_is_overdue - ОШИБКА: {e}")
        tests_failed += 1
    
    try:
        # Test 5: Преобразование в словарь
        task = Task("Test Task", "Test Desc", 1, datetime.now(), 1, 1)
        task.id = 1
        task_dict = task.to_dict()
        assert task_dict["title"] == "Test Task"
        assert "created_at" in task_dict
        print("✓ test_task_to_dict - ПРОЙДЕН")
        tests_passed += 1
    except Exception as e:
        print(f"✗ test_task_to_dict - ОШИБКА: {e}")
        tests_failed += 1
    
    # Тесты для Project
    print("\n ТЕСТЫ КЛАССА PROJECT ")
    
    try:
        # Test 6: Создание проекта
        project = Project("Test Project", "Test Description", datetime.now(), datetime.now() + timedelta(days=30))
        assert project.name == "Test Project"
        assert project.status == "active"
        print("✓ test_project_creation - ПРОЙДЕН")
        tests_passed += 1
    except Exception as e:
        print(f"✗ test_project_creation - ОШИБКА: {e}")
        tests_failed += 1
    
    try:
        # Test 7: Обновление статуса проекта
        project = Project("Test", "Desc", datetime.now(), datetime.now() + timedelta(days=1))
        assert project.update_status("completed") == True
        assert project.status == "completed"
        print("✓ test_project_update_status - ПРОЙДЕН")
        tests_passed += 1
    except Exception as e:
        print(f"✗ test_project_update_status - ОШИБКА: {e}")
        tests_failed += 1
    
    try:
        # Test 8: Прогресс проекта
        project = Project("Test", "Desc", datetime.now(), datetime.now() + timedelta(days=1))
        progress = project.get_progress()
        assert isinstance(progress, float)
        print("✓ test_project_get_progress - ПРОЙДЕН")
        tests_passed += 1
    except Exception as e:
        print(f"✗ test_project_get_progress - ОШИБКА: {e}")
        tests_failed += 1
    
    # Тесты для User
    print("\n ТЕСТЫ КЛАССА USER ")
    
    try:
        # Test 9: Создание пользователя
        user = User("testuser", "test@example.com", "developer")
        assert user.username == "testuser"
        assert user.email == "test@example.com"
        print("✓ test_user_creation - ПРОЙДЕН")
        tests_passed += 1
    except Exception as e:
        print(f"✗ test_user_creation - ОШИБКА: {e}")
        tests_failed += 1
    
    try:
        # Test 10: Обновление информации пользователя
        user = User("olduser", "old@example.com", "developer")
        user.update_info(username="newuser", email="new@example.com", role="admin")
        assert user.username == "newuser"
        assert user.role == "admin"
        print("✓ test_user_update_info - ПРОЙДЕН")
        tests_passed += 1
    except Exception as e:
        print(f"✗ test_user_update_info - ОШИБКА: {e}")
        tests_failed += 1
    
    try:
        # Test 11: Валидация email
        try:
            User("testuser", "invalid-email", "developer")
            print("✗ test_user_email_validation - ОШИБКА: Невалидный email прошел")
            tests_failed += 1
        except ValueError:
            print("✓ test_user_email_validation - ПРОЙДЕН")
            tests_passed += 1
    except Exception as e:
        print(f"✗ test_user_email_validation - ОШИБКА: {e}")
        tests_failed += 1
    
    # Итоги
    print(f"ИТОГ: {tests_passed} пройдено, {tests_failed} не пройдено")
    
    if tests_failed == 0:
        print(" ВСЕ ТЕСТЫ МОДЕЛЕЙ ПРОЙДЕНЫ УСПЕШНО!")
    else:
        print(" Есть непройденные тесты!!!!")
    
    return tests_passed, tests_failed

if __name__ == "__main__":
    run_tests()
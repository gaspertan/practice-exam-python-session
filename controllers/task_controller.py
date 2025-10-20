from models.task import Task
from datetime import datetime

class TaskController:
    def __init__(self, db_manager) -> None:
        self.db_manager = db_manager

    def add_task(self, title, description, priority, due_date, project_id, assignee_id) -> int:
    
        
        if priority not in [1, 2, 3]:
            raise ValueError("Приоритет должен быть 1, 2 или 3")
        
        
        if due_date < datetime.now():
            raise ValueError("Срок выполнения не может быть в прошлом")
        
        
        task = Task(
            title=title,
            description=description,
            priority=priority,
            due_date=due_date,
            project_id=project_id,
            assignee_id=assignee_id
        )
        
        
        return self.db_manager.add_task(task)

    def get_task(self, task_id) -> Task | None:
       
        return self.db_manager.get_task_by_id(task_id)

    def get_all_tasks(self) -> list[Task]:
        
        return self.db_manager.get_all_tasks()

    def update_task(self, task_id, **kwargs) -> bool:
       
        
        if 'priority' in kwargs and kwargs['priority'] not in [1, 2, 3]:
            raise ValueError("Приоритет должен быть 1, 2 или 3")
        
       
        if 'status' in kwargs and kwargs['status'] not in ['pending', 'in_progress', 'completed']:
            raise ValueError("Некорректный статус")
        
        return self.db_manager.update_task(task_id, **kwargs)

    def delete_task(self, task_id) -> bool:
        
        return self.db_manager.delete_task(task_id)

    def search_tasks(self, query) -> list[Task]:
        
        if not query or not query.strip():
            return []
        
        return self.db_manager.search_tasks(query.strip())

    def update_task_status(self, task_id, new_status) -> bool:
      
        valid_statuses = ['pending', 'in_progress', 'completed']
        if new_status not in valid_statuses:
            raise ValueError(f"Некорректный статус. Допустимые: {valid_statuses}")
        
        return self.db_manager.update_task(task_id, status=new_status)

    def get_overdue_tasks(self) -> list[Task]:
        
        all_tasks = self.db_manager.get_all_tasks()
        return [task for task in all_tasks if task.is_overdue()]

    def get_tasks_by_project(self, project_id) -> list[Task]:
        
        return self.db_manager.get_tasks_by_project(project_id)

    def get_tasks_by_user(self, user_id) -> list[Task]:
      
        return self.db_manager.get_tasks_by_user(user_id)
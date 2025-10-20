from models.project import Project
from datetime import datetime

class ProjectController:
    def __init__(self, db_manager) -> None:
        self.db_manager = db_manager

    def add_project(self, name, description, start_date, end_date) -> int:
       
        
        if start_date >= end_date:
            raise ValueError("Дата окончания должна быть позже даты начала")
        
        if start_date < datetime.now():
            raise ValueError("Дата начала не может быть в прошлом")
        
        
        project = Project(
            name=name,
            description=description,
            start_date=start_date,
            end_date=end_date
        )
        
        
        return self.db_manager.add_project(project)

    def get_project(self, project_id) -> Project | None:
       
        return self.db_manager.get_project_by_id(project_id)

    def get_all_projects(self) -> list[Project]:
      
        return self.db_manager.get_all_projects()

    def update_project(self, project_id, **kwargs) -> bool:
       
        if 'status' in kwargs and kwargs['status'] not in ['active', 'completed', 'on_hold']:
            raise ValueError("Некорректный статус проекта")
        
        
        if 'start_date' in kwargs and 'end_date' in kwargs:
            if kwargs['start_date'] >= kwargs['end_date']:
                raise ValueError("Дата окончания должна быть позже даты начала")
        
        return self.db_manager.update_project(project_id, **kwargs)

    def delete_project(self, project_id) -> bool:
       
        
        project_tasks = self.db_manager.get_tasks_by_project(project_id)
        if project_tasks:
            raise ValueError("Нельзя удалить проект с задачами. Сначала удалите или переместите задачи.")
        
        return self.db_manager.delete_project(project_id)

    def update_project_status(self, project_id, new_status) -> bool:
      
        valid_statuses = ['active', 'completed', 'on_hold']
        if new_status not in valid_statuses:
            raise ValueError(f"Некорректный статус. Допустимые: {valid_statuses}")
        
        return self.db_manager.update_project(project_id, status=new_status)

    def get_project_progress(self, project_id) -> float:
       
        project = self.get_project(project_id)
        if not project:
            raise ValueError("Проект не найден")
        
        
        tasks = self.db_manager.get_tasks_by_project(project_id)
        
        if not tasks:
            return 0.0
        
     
        completed_tasks = sum(1 for task in tasks if task.status == 'completed')
        progress = (completed_tasks / len(tasks)) * 100.0
        
        return round(progress, 2)
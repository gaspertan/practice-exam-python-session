import sqlite3
from models.task import Task
from models.project import Project
from models.user import User
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_path="tasks.db") -> None:
        self.db_path = db_path
        self.connection = None
        self.connect()
        self.create_tables()

    def connect(self) -> None:
        
        self.connection = sqlite3.connect(self.db_path)
        self.connection.row_factory = sqlite3.Row  # Чтобы получать строки как словари

    def close(self) -> None:
       
        if self.connection:
            self.connection.close()

    def create_tables(self) -> None:
        
        self._create_user_table()
        self._create_project_table()
        self._create_task_table()

    def _create_user_table(self) -> None:
        
        query = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            role TEXT NOT NULL,
            registration_date DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """
        self.connection.execute(query)
        self.connection.commit()

    def _create_project_table(self) -> None:
        
        query = """
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            start_date DATETIME NOT NULL,
            end_date DATETIME NOT NULL,
            status TEXT DEFAULT 'active',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """
        self.connection.execute(query)
        self.connection.commit()

    def _create_task_table(self) -> None:
        
        query = """
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            priority INTEGER NOT NULL,
            status TEXT DEFAULT 'pending',
            due_date DATETIME NOT NULL,
            project_id INTEGER,
            assignee_id INTEGER,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (project_id) REFERENCES projects (id),
            FOREIGN KEY (assignee_id) REFERENCES users (id)
        )
        """
        self.connection.execute(query)
        self.connection.commit()

   

    def add_task(self, task: Task) -> int:
        
        query = """
        INSERT INTO tasks (title, description, priority, status, due_date, project_id, assignee_id)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        cursor = self.connection.execute(query, (
            task.title, task.description, task.priority, task.status,
            task.due_date, task.project_id, task.assignee_id
        ))
        self.connection.commit()
        task.id = cursor.lastrowid
        return task.id

    def get_task_by_id(self, task_id) -> Task | None:
        
        query = "SELECT * FROM tasks WHERE id = ?"
        result = self.connection.execute(query, (task_id,)).fetchone()
        
        if not result:
            return None
            
        return self._row_to_task(result)

    def get_all_tasks(self) -> list[Task]:
        
        query = "SELECT * FROM tasks ORDER BY created_at DESC"
        results = self.connection.execute(query).fetchall()
        return [self._row_to_task(row) for row in results]

    def update_task(self, task_id, **kwargs) -> bool:
       
        if not kwargs:
            return False
        
        set_clause = ", ".join([f"{key} = ?" for key in kwargs.keys()])
        query = f"UPDATE tasks SET {set_clause} WHERE id = ?"
        
        values = list(kwargs.values())
        values.append(task_id)
        
        self.connection.execute(query, values)
        self.connection.commit()
        return self.connection.total_changes > 0

    def delete_task(self, task_id) -> bool:
        
        query = "DELETE FROM tasks WHERE id = ?"
        self.connection.execute(query, (task_id,))
        self.connection.commit()
        return self.connection.total_changes > 0

    def search_tasks(self, query) -> list[Task]:
        
        search_query = f"%{query}%"
        sql = """
        SELECT * FROM tasks 
        WHERE title LIKE ? OR description LIKE ?
        ORDER BY created_at DESC
        """
        results = self.connection.execute(sql, (search_query, search_query)).fetchall()
        return [self._row_to_task(row) for row in results]

    def get_tasks_by_project(self, project_id) -> list[Task]:
        
        query = "SELECT * FROM tasks WHERE project_id = ? ORDER BY created_at DESC"
        results = self.connection.execute(query, (project_id,)).fetchall()
        return [self._row_to_task(row) for row in results]

    def get_tasks_by_user(self, user_id) -> list[Task]:
        
        query = "SELECT * FROM tasks WHERE assignee_id = ? ORDER BY created_at DESC"
        results = self.connection.execute(query, (user_id,)).fetchall()
        return [self._row_to_task(row) for row in results]

   
    def _row_to_task(self, row) -> Task:
        
        task = Task(
            title=row['title'],
            description=row['description'],
            priority=row['priority'],
            due_date=datetime.fromisoformat(row['due_date']),
            project_id=row['project_id'],
            assignee_id=row['assignee_id']
        )
        task.id = row['id']
        task.status = row['status']
        task.created_at = datetime.fromisoformat(row['created_at'])
        return task 
    
    def add_project(self, project: Project) -> int:
        
        query = """
        INSERT INTO projects (name, description, start_date, end_date, status)
        VALUES (?, ?, ?, ?, ?)
        """
        cursor = self.connection.execute(query, (
            project.name, project.description, project.start_date,
            project.end_date, project.status
        ))
        self.connection.commit()
        project.id = cursor.lastrowid
        return project.id

    def get_project_by_id(self, project_id) -> Project | None:
        
        query = "SELECT * FROM projects WHERE id = ?"
        result = self.connection.execute(query, (project_id,)).fetchone()
        
        if not result:
            return None
            
        return self._row_to_project(result)

    def get_all_projects(self) -> list[Project]:
       
        query = "SELECT * FROM projects ORDER BY created_at DESC"
        results = self.connection.execute(query).fetchall()
        return [self._row_to_project(row) for row in results]

    def update_project(self, project_id, **kwargs) -> bool:
        
        if not kwargs:
            return False
        
        set_clause = ", ".join([f"{key} = ?" for key in kwargs.keys()])
        query = f"UPDATE projects SET {set_clause} WHERE id = ?"
        
        values = list(kwargs.values())
        values.append(project_id)
        
        self.connection.execute(query, values)
        self.connection.commit()
        return self.connection.total_changes > 0

    def delete_project(self, project_id) -> bool:
       
        query = "DELETE FROM projects WHERE id = ?"
        self.connection.execute(query, (project_id,))
        self.connection.commit()
        return self.connection.total_changes > 0

    # === МЕТОДЫ ДЛЯ РАБОТЫ С ПОЛЬЗОВАТЕЛЯМИ ===

    def add_user(self, user: User) -> int:
        
        query = """
        INSERT INTO users (username, email, role)
        VALUES (?, ?, ?)
        """
        cursor = self.connection.execute(query, (
            user.username, user.email, user.role
        ))
        self.connection.commit()
        user.id = cursor.lastrowid
        return user.id

    def get_user_by_id(self, user_id) -> User | None:
       
        query = "SELECT * FROM users WHERE id = ?"
        result = self.connection.execute(query, (user_id,)).fetchone()
        
        if not result:
            return None
            
        return self._row_to_user(result)

    def get_all_users(self) -> list[User]:
        
        query = "SELECT * FROM users ORDER BY registration_date DESC"
        results = self.connection.execute(query).fetchall()
        return [self._row_to_user(row) for row in results]

    def update_user(self, user_id, **kwargs) -> bool:
      
        if not kwargs:
            return False
        
        set_clause = ", ".join([f"{key} = ?" for key in kwargs.keys()])
        query = f"UPDATE users SET {set_clause} WHERE id = ?"
        
        values = list(kwargs.values())
        values.append(user_id)
        
        self.connection.execute(query, values)
        self.connection.commit()
        return self.connection.total_changes > 0

    def delete_user(self, user_id) -> bool:
       
        query = "DELETE FROM users WHERE id = ?"
        self.connection.execute(query, (user_id,))
        self.connection.commit()
        return self.connection.total_changes > 0

    # === ВСПОМОГАТЕЛЬНЫЕ МЕТОДЫ ===

    def _row_to_project(self, row) -> Project:
       
        project = Project(
            name=row['name'],
            description=row['description'],
            start_date=datetime.fromisoformat(row['start_date']),
            end_date=datetime.fromisoformat(row['end_date'])
        )
        project.id = row['id']
        project.status = row['status']
        project.created_at = datetime.fromisoformat(row['created_at'])
        return project

    def _row_to_user(self, row) -> User:
        
        user = User(
            username=row['username'],
            email=row['email'],
            role=row['role']
        )
        user.id = row['id']
        user.registration_date = datetime.fromisoformat(row['registration_date'])
        return user
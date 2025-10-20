from models.user import User

class UserController:
    def __init__(self, db_manager) -> None:
        self.db_manager = db_manager

    def add_user(self, username, email, role) -> int:
       
        valid_roles = ['admin', 'manager', 'developer']
        if role not in valid_roles:
            raise ValueError(f"Некорректная роль. Допустимые: {valid_roles}")
        
        
        user = User(
            username=username,
            email=email,
            role=role
        )
        
        
        return self.db_manager.add_user(user)

    def get_user(self, user_id) -> User | None:
       
        return self.db_manager.get_user_by_id(user_id)

    def get_all_users(self) -> list[User]:
        
        return self.db_manager.get_all_users()

    def update_user(self, user_id, **kwargs) -> bool:
       
        if 'role' in kwargs:
            valid_roles = ['admin', 'manager', 'developer']
            if kwargs['role'] not in valid_roles:
                raise ValueError(f"Некорректная роль. Допустимые: {valid_roles}")
        
       
        if 'email' in kwargs:
            
            temp_user = User("temp", kwargs['email'], "developer")
            
        
        return self.db_manager.update_user(user_id, **kwargs)

    def delete_user(self, user_id) -> bool:
    
        user_tasks = self.db_manager.get_tasks_by_user(user_id)
        if user_tasks:
            raise ValueError("Нельзя удалить пользователя с задачами. Сначала переназначьте или удалите задачи.")
        
        return self.db_manager.delete_user(user_id)

    def get_user_tasks(self, user_id) -> list:
        
        return self.db_manager.get_tasks_by_user(user_id)
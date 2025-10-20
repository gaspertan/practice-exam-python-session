from datetime import datetime

class Project:
    def __init__(self, name, description, start_date, end_date) -> None:
        self.id = None  
        self.name = name
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.status = 'active'  
        self.created_at = datetime.now()  

    def update_status(self, new_status) -> bool:
      
        valid_statuses = ['active', 'completed', 'on_hold']
        
        if new_status in valid_statuses:
            self.status = new_status
            return True
        return False

    def get_progress(self) -> float:
    
        
        return 0.0

    def to_dict(self) -> dict:
     
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'status': self.status,
            'created_at': self.created_at,
            'progress': self.get_progress()  
        }
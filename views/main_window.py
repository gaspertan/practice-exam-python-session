# Главное окно приложения согласно README.md

import tkinter as tk
from tkinter import ttk
from views.task_view import TaskView
from views.project_view import ProjectView
from views.user_view import UserView

class MainWindow(tk.Tk):
    def __init__(self, task_controller, project_controller, user_controller) -> None:
        super().__init__()
        
        self.task_controller = task_controller
        self.project_controller = project_controller
        self.user_controller = user_controller
        
        self.title("Система управления задачами")
        self.geometry("1000x700")
        self.configure(bg='#f0f0f0')
        
        self._create_menu()
        self._create_notebook()
        self._create_status_bar()
        
    def _create_menu(self):
       
        menubar = tk.Menu(self)
        
        
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Выход", command=self.quit)
        menubar.add_cascade(label="Файл", menu=file_menu)
        
        
        view_menu = tk.Menu(menubar, tearoff=0)
        view_menu.add_command(label="Задачи", command=lambda: self.notebook.select(0))
        view_menu.add_command(label="Проекты", command=lambda: self.notebook.select(1))
        view_menu.add_command(label="Пользователи", command=lambda: self.notebook.select(2))
        menubar.add_cascade(label="Вид", menu=view_menu)
        
        
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="О программе", command=self._show_about)
        menubar.add_cascade(label="Справка", menu=help_menu)
        
        self.config(menu=menubar)
    
    def _create_notebook(self):
        
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
       
        self.task_frame = ttk.Frame(self.notebook)
        self.project_frame = ttk.Frame(self.notebook)
        self.user_frame = ttk.Frame(self.notebook)
        
      
        self.notebook.add(self.task_frame, text="Задачи")
        self.notebook.add(self.project_frame, text="Проекты")
        self.notebook.add(self.user_frame, text="Пользователи")
        
        
        self.task_view = TaskView(self.task_frame, self.task_controller, 
                                 self.project_controller, self.user_controller)
        self.project_view = ProjectView(self.project_frame, self.project_controller,
                                       self.task_controller)
        self.user_view = UserView(self.user_frame, self.user_controller,
                                 self.task_controller)
    
    def _create_status_bar(self):
       
        self.status_bar = ttk.Label(self, text="Готово", relief='sunken', anchor='w')
        self.status_bar.pack(side='bottom', fill='x')
    
    def _show_about(self):
        
        about_text = """Система управления задачами
        
Версия 1.0
Разработано на Python с использованием:
- Tkinter для GUI
- SQLite для хранения данных
- Архитектура MVC
        
© 2024"""
        
        tk.messagebox.showinfo("О программе", about_text)
    
    def update_status(self, message):
        
        self.status_bar.config(text=message)
    
    def run(self):
        
        self.mainloop()

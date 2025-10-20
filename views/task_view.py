import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta

class TaskView(ttk.Frame):
    def __init__(self, parent, task_controller, project_controller, user_controller) -> None:
        super().__init__(parent)
        self.task_controller = task_controller
        self.project_controller = project_controller
        self.user_controller = user_controller
        
        self.pack(fill='both', expand=True)
        self.create_widgets()
        self.refresh_tasks()

    def create_widgets(self) -> None:
       
        main_frame = ttk.Frame(self)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        
        left_frame = ttk.LabelFrame(main_frame, text="Добавить/Редактировать задачу", padding=10)
        left_frame.pack(side='left', fill='y', padx=(0, 5))
        
       
        right_frame = ttk.LabelFrame(main_frame, text="Список задач", padding=10)
        right_frame.pack(side='right', fill='both', expand=True, padx=(5, 0))
        
      
        ttk.Label(left_frame, text="Название:").grid(row=0, column=0, sticky='w', pady=2)
        self.title_entry = ttk.Entry(left_frame, width=25)
        self.title_entry.grid(row=0, column=1, sticky='ew', pady=2, padx=(5, 0))
        
        ttk.Label(left_frame, text="Описание:").grid(row=1, column=0, sticky='nw', pady=2)
        self.description_text = tk.Text(left_frame, width=25, height=4)
        self.description_text.grid(row=1, column=1, sticky='ew', pady=2, padx=(5, 0))
        
        ttk.Label(left_frame, text="Приоритет:").grid(row=2, column=0, sticky='w', pady=2)
        self.priority_var = tk.StringVar(value="2")
        priority_combo = ttk.Combobox(left_frame, textvariable=self.priority_var, 
                                     values=["1 - Высокий", "2 - Средний", "3 - Низкий"], 
                                     state="readonly", width=22)
        priority_combo.grid(row=2, column=1, sticky='ew', pady=2, padx=(5, 0))
        
        ttk.Label(left_frame, text="Срок выполнения:").grid(row=3, column=0, sticky='w', pady=2)
        self.due_date_entry = ttk.Entry(left_frame, width=25)
        self.due_date_entry.insert(0, (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d"))
        self.due_date_entry.grid(row=3, column=1, sticky='ew', pady=2, padx=(5, 0))
        
        ttk.Label(left_frame, text="Проект:").grid(row=4, column=0, sticky='w', pady=2)
        self.project_var = tk.StringVar()
        self.project_combo = ttk.Combobox(left_frame, textvariable=self.project_var, 
                                         state="readonly", width=22)
        self.project_combo.grid(row=4, column=1, sticky='ew', pady=2, padx=(5, 0))
        
        ttk.Label(left_frame, text="Исполнитель:").grid(row=5, column=0, sticky='w', pady=2)
        self.assignee_var = tk.StringVar()
        self.assignee_combo = ttk.Combobox(left_frame, textvariable=self.assignee_var, 
                                          state="readonly", width=22)
        self.assignee_combo.grid(row=5, column=1, sticky='ew', pady=2, padx=(5, 0))
        
        ttk.Label(left_frame, text="Статус:").grid(row=6, column=0, sticky='w', pady=2)
        self.status_var = tk.StringVar(value="pending")
        status_combo = ttk.Combobox(left_frame, textvariable=self.status_var,
                                   values=["pending", "in_progress", "completed"], 
                                   state="readonly", width=22)
        status_combo.grid(row=6, column=1, sticky='ew', pady=2, padx=(5, 0))
        
        
        button_frame = ttk.Frame(left_frame)
        button_frame.grid(row=7, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="Добавить задачу", 
                  command=self.add_task).pack(side='left', padx=(0, 5))
        ttk.Button(button_frame, text="Обновить задачу", 
                  command=self.update_task).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Удалить выбранную", 
                  command=self.delete_selected).pack(side='left', padx=(5, 0))
        
       
        search_frame = ttk.Frame(right_frame)
        search_frame.pack(fill='x', pady=(0, 10))
        
        ttk.Label(search_frame, text="Поиск:").pack(side='left')
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=20)
        search_entry.pack(side='left', padx=5)
        search_entry.bind('<KeyRelease>', self.on_search)
        
        ttk.Button(search_frame, text="Обновить список", 
                  command=self.refresh_tasks).pack(side='right')
        
        
        columns = ("ID", "Название", "Приоритет", "Статус", "Срок", "Проект", "Исполнитель")
        self.tasks_tree = ttk.Treeview(right_frame, columns=columns, show='headings', height=15)
        
       
        for col in columns:
            self.tasks_tree.heading(col, text=col)
            self.tasks_tree.column(col, width=100)
        
        self.tasks_tree.column("Название", width=150)
        self.tasks_tree.column("Срок", width=100)
        
        
        scrollbar = ttk.Scrollbar(right_frame, orient='vertical', command=self.tasks_tree.yview)
        self.tasks_tree.configure(yscrollcommand=scrollbar.set)
        
        self.tasks_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        
        self.tasks_tree.bind('<Double-1>', self.on_task_select)
        
        
        self.refresh_comboboxes()

    def refresh_comboboxes(self):
       
        try:
            
            projects = self.project_controller.get_all_projects()
            project_values = [f"{p.id}: {p.name}" for p in projects]
            self.project_combo['values'] = project_values
            if project_values:
                self.project_combo.set(project_values[0])
            
            
            users = self.user_controller.get_all_users()
            user_values = [f"{u.id}: {u.username}" for u in users]
            self.assignee_combo['values'] = user_values
            if user_values:
                self.assignee_combo.set(user_values[0])
                
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить данные: {e}")

    def refresh_tasks(self) -> None:
        
        try:
            
            for item in self.tasks_tree.get_children():
                self.tasks_tree.delete(item)
            
            
            tasks = self.task_controller.get_all_tasks()
            
           
            for task in tasks:
                
                project_name = "Не указан"
                if task.project_id:
                    project = self.project_controller.get_project(task.project_id)
                    if project:
                        project_name = project.name
                
                assignee_name = "Не указан"
                if task.assignee_id:
                    user = self.user_controller.get_user(task.assignee_id)
                    if user:
                        assignee_name = user.username
                
                
                priority_map = {1: "Высокий", 2: "Средний", 3: "Низкий"}
                priority_text = priority_map.get(task.priority, "Неизвестно")
                
                
                status_map = {"pending": "Ожидает", "in_progress": "В работе", "completed": "Завершена"}
                status_text = status_map.get(task.status, task.status)
                
                self.tasks_tree.insert("", "end", values=(
                    task.id,
                    task.title,
                    priority_text,
                    status_text,
                    task.due_date.strftime("%Y-%m-%d"),
                    project_name,
                    assignee_name
                ))
                
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить задачи: {e}")

    def add_task(self) -> None:
       
        try:
           
            title = self.title_entry.get().strip()
            description = self.description_text.get("1.0", "end-1c").strip()
            priority_str = self.priority_var.get().split(" - ")[0]
            due_date_str = self.due_date_entry.get().strip()
            project_str = self.project_var.get()
            assignee_str = self.assignee_var.get()
            status = self.status_var.get()
            
            
            if not title:
                messagebox.showwarning("Предупреждение", "Введите название задачи")
                return
            
            
            priority = int(priority_str)
            due_date = datetime.strptime(due_date_str, "%Y-%m-%d")
            project_id = int(project_str.split(":")[0]) if project_str else None
            assignee_id = int(assignee_str.split(":")[0]) if assignee_str else None
            
           
            task_id = self.task_controller.add_task(
                title=title,
                description=description,
                priority=priority,
                due_date=due_date,
                project_id=project_id,
                assignee_id=assignee_id
            )
            
            
            if status != "pending":
                self.task_controller.update_task_status(task_id, status)
            
            messagebox.showinfo("Успех", f"Задача '{title}' добавлена с ID: {task_id}")
            
            
            self.clear_form()
            self.refresh_tasks()
            
        except ValueError as e:
            messagebox.showerror("Ошибка", f"Некорректные данные: {e}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось добавить задачу: {e}")

    def update_task(self) -> None:
        
        selected = self.tasks_tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите задачу для редактирования")
            return
        
        
        messagebox.showinfo("Инфо", "Функция обновления будет реализована позже")

    def delete_selected(self) -> None:
        
        selected = self.tasks_tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите задачу для удаления")
            return
        
        task_id = self.tasks_tree.item(selected[0])['values'][0]
        task_title = self.tasks_tree.item(selected[0])['values'][1]
        
        if messagebox.askyesno("Подтверждение", f"Удалить задачу '{task_title}'?"):
            try:
                if self.task_controller.delete_task(task_id):
                    messagebox.showinfo("Успех", "Задача удалена")
                    self.refresh_tasks()
                else:
                    messagebox.showerror("Ошибка", "Не удалось удалить задачу")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка при удалении: {e}")

    def on_task_select(self, event):
        
        selected = self.tasks_tree.selection()
        if selected:
            
            values = self.tasks_tree.item(selected[0])['values']
            self.title_entry.delete(0, 'end')
            self.title_entry.insert(0, values[1])
            

    def on_search(self, event):
       
        query = self.search_var.get().strip()
        if not query:
            self.refresh_tasks()
        else:
            
            pass

    def clear_form(self):
        
        self.title_entry.delete(0, 'end')
        self.description_text.delete("1.0", "end")
        self.priority_var.set("2 - Средний")
        self.due_date_entry.delete(0, 'end')
        self.due_date_entry.insert(0, (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d"))
        self.status_var.set("pending")
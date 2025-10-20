import tkinter as tk
from tkinter import ttk, messagebox

class UserView(ttk.Frame):
    def __init__(self, parent, user_controller, task_controller) -> None:
        super().__init__(parent)
        self.user_controller = user_controller
        self.task_controller = task_controller
        
        self.pack(fill='both', expand=True)
        self.create_widgets()
        self.refresh_users()

    def create_widgets(self) -> None:
       
        main_frame = ttk.Frame(self)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        
        left_frame = ttk.LabelFrame(main_frame, text="Добавить/Редактировать пользователя", padding=10)
        left_frame.pack(side='left', fill='y', padx=(0, 5))
        
        
        right_frame = ttk.LabelFrame(main_frame, text="Список пользователей", padding=10)
        right_frame.pack(side='right', fill='both', expand=True, padx=(5, 0))
        
        
        ttk.Label(left_frame, text="Имя пользователя:").grid(row=0, column=0, sticky='w', pady=2)
        self.username_entry = ttk.Entry(left_frame, width=25)
        self.username_entry.grid(row=0, column=1, sticky='ew', pady=2, padx=(5, 0))
        
        ttk.Label(left_frame, text="Email:").grid(row=1, column=0, sticky='w', pady=2)
        self.email_entry = ttk.Entry(left_frame, width=25)
        self.email_entry.grid(row=1, column=1, sticky='ew', pady=2, padx=(5, 0))
        
        ttk.Label(left_frame, text="Роль:").grid(row=2, column=0, sticky='w', pady=2)
        self.role_var = tk.StringVar(value="developer")
        role_combo = ttk.Combobox(left_frame, textvariable=self.role_var,
                                 values=["admin", "manager", "developer"], 
                                 state="readonly", width=22)
        role_combo.grid(row=2, column=1, sticky='ew', pady=2, padx=(5, 0))
        
        
        button_frame = ttk.Frame(left_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="Добавить пользователя", 
                  command=self.add_user).pack(side='left', padx=(0, 5))
        ttk.Button(button_frame, text="Обновить пользователя", 
                  command=self.update_user).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Удалить выбранного", 
                  command=self.delete_selected).pack(side='left', padx=(5, 0))
        
        
        self.info_frame = ttk.LabelFrame(left_frame, text="Информация о пользователе", padding=5)
        self.info_frame.grid(row=4, column=0, columnspan=2, pady=10, sticky='ew')
        
        self.info_label = ttk.Label(self.info_frame, text="Выберите пользователя")
        self.info_label.pack(pady=5)
        
        
        control_frame = ttk.Frame(right_frame)
        control_frame.pack(fill='x', pady=(0, 10))
        
        ttk.Button(control_frame, text="Обновить список", 
                  command=self.refresh_users).pack(side='right')
        
        ttk.Button(control_frame, text="Показать задачи", 
                  command=self.show_user_tasks).pack(side='right', padx=(0, 5))
        
        
        columns = ("ID", "Имя пользователя", "Email", "Роль", "Регистрация", "Задач")
        self.users_tree = ttk.Treeview(right_frame, columns=columns, show='headings', height=15)
        
        
        column_widths = {
            "ID": 50,
            "Имя пользователя": 120,
            "Email": 150,
            "Роль": 80,
            "Регистрация": 100,
            "Задач": 60
        }
        
        for col in columns:
            self.users_tree.heading(col, text=col)
            self.users_tree.column(col, width=column_widths.get(col, 100))
        
        
        scrollbar = ttk.Scrollbar(right_frame, orient='vertical', command=self.users_tree.yview)
        self.users_tree.configure(yscrollcommand=scrollbar.set)
        
        self.users_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        
        self.users_tree.bind('<<TreeviewSelect>>', self.on_user_select)

    def refresh_users(self) -> None:
        
        try:
            
            for item in self.users_tree.get_children():
                self.users_tree.delete(item)
            
            
            users = self.user_controller.get_all_users()
            
            
            for user in users:
                
                tasks_count = len(self.task_controller.get_tasks_by_user(user.id))
                
                
                role_map = {
                    "admin": "Администратор",
                    "manager": "Менеджер", 
                    "developer": "Разработчик"
                }
                role_text = role_map.get(user.role, user.role)
                
                self.users_tree.insert("", "end", values=(
                    user.id,
                    user.username,
                    user.email,
                    role_text,
                    user.registration_date.strftime("%Y-%m-%d"),
                    tasks_count
                ))
                
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить пользователей: {e}")

    def add_user(self) -> None:
        
        try:
            
            username = self.username_entry.get().strip()
            email = self.email_entry.get().strip()
            role = self.role_var.get()
            
            
            if not username:
                messagebox.showwarning("Предупреждение", "Введите имя пользователя")
                return
            
            if not email:
                messagebox.showwarning("Предупреждение", "Введите email")
                return
            
            
            user_id = self.user_controller.add_user(
                username=username,
                email=email,
                role=role
            )
            
            messagebox.showinfo("Успех", f"Пользователь '{username}' добавлен с ID: {user_id}")
            
            
            self.clear_form()
            self.refresh_users()
            
        except ValueError as e:
            messagebox.showerror("Ошибка", f"Некорректные данные: {e}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось добавить пользователя: {e}")

    def update_user(self) -> None:
        
        selected = self.users_tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите пользователя для редактирования")
            return
        
        user_id = self.users_tree.item(selected[0])['values'][0]
        
        try:
            
            username = self.username_entry.get().strip()
            email = self.email_entry.get().strip()
            role = self.role_var.get()
            
            if not username:
                messagebox.showwarning("Предупреждение", "Введите имя пользователя")
                return
            
            if not email:
                messagebox.showwarning("Предупреждение", "Введите email")
                return
            
            
            self.user_controller.update_user(
                user_id,
                username=username,
                email=email,
                role=role
            )
            
            messagebox.showinfo("Успех", f"Пользователь '{username}' обновлен")
            self.refresh_users()
            
        except ValueError as e:
            messagebox.showerror("Ошибка", f"Некорректные данные: {e}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось обновить пользователя: {e}")

    def delete_selected(self) -> None:
        
        selected = self.users_tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите пользователя для удаления")
            return
        
        user_id = self.users_tree.item(selected[0])['values'][0]
        username = self.users_tree.item(selected[0])['values'][1]
        
        if messagebox.askyesno("Подтверждение", f"Удалить пользователя '{username}'?"):
            try:
                if self.user_controller.delete_user(user_id):
                    messagebox.showinfo("Успех", "Пользователь удален")
                    self.refresh_users()
                    self.clear_form()
                else:
                    messagebox.showerror("Ошибка", "Не удалось удалить пользователя")
            except ValueError as e:
                messagebox.showerror("Ошибка", f"Нельзя удалить пользователя: {e}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка при удалении: {e}")

    def on_user_select(self, event):
      
        selected = self.users_tree.selection()
        if selected:
            # Заполняем форму данными выбранного пользователя
            values = self.users_tree.item(selected[0])['values']
            
            self.username_entry.delete(0, 'end')
            self.username_entry.insert(0, values[1])
            
            self.email_entry.delete(0, 'end')
            self.email_entry.insert(0, values[2])
            
           
            role_map_reverse = {
                "Администратор": "admin",
                "Менеджер": "manager", 
                "Разработчик": "developer"
            }
            self.role_var.set(role_map_reverse.get(values[3], "developer"))
            
           
            user_id = values[0]
            tasks_count = len(self.task_controller.get_tasks_by_user(user_id))
            self.info_label.config(
                text=f"Пользователь: {values[1]}\nЗадач: {tasks_count}\nРоль: {values[3]}"
            )

    def show_user_tasks(self):
        
        selected = self.users_tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите пользователя")
            return
        
        user_id = self.users_tree.item(selected[0])['values'][0]
        username = self.users_tree.item(selected[0])['values'][1]
        
        tasks = self.task_controller.get_tasks_by_user(user_id)
        
        if not tasks:
            messagebox.showinfo("Информация", f"У пользователя '{username}' нет задач")
            return
        
        
        tasks_window = tk.Toplevel(self)
        tasks_window.title(f"Задачи пользователя: {username}")
        tasks_window.geometry("700x400")
        
        
        columns = ("ID", "Название", "Приоритет", "Статус", "Срок", "Проект")
        tasks_tree = ttk.Treeview(tasks_window, columns=columns, show='headings', height=15)
        
        column_widths = {
            "ID": 50,
            "Название": 200,
            "Приоритет": 80,
            "Статус": 100,
            "Срок": 100,
            "Проект": 150
        }
        
        for col in columns:
            tasks_tree.heading(col, text=col)
            tasks_tree.column(col, width=column_widths.get(col, 100))
        
        
        for task in tasks:
            priority_map = {1: "Высокий", 2: "Средний", 3: "Низкий"}
            status_map = {"pending": "Ожидает", "in_progress": "В работе", "completed": "Завершена"}
            
            
            project_name = "Не указан"
            if task.project_id:
                from controllers.project_controller import ProjectController
                project = self.task_controller.project_controller.get_project(task.project_id)
                if project:
                    project_name = project.name
            
            tasks_tree.insert("", "end", values=(
                task.id,
                task.title,
                priority_map.get(task.priority, "Неизвестно"),
                status_map.get(task.status, task.status),
                task.due_date.strftime("%Y-%m-%d"),
                project_name
            ))
        
        scrollbar = ttk.Scrollbar(tasks_window, orient='vertical', command=tasks_tree.yview)
        tasks_tree.configure(yscrollcommand=scrollbar.set)
        
        tasks_tree.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        scrollbar.pack(side='right', fill='y', pady=10)

    def clear_form(self):
        
        self.username_entry.delete(0, 'end')
        self.email_entry.delete(0, 'end')
        self.role_var.set("developer")
        self.info_label.config(text="Выберите пользователя")
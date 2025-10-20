import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta

class ProjectView(ttk.Frame):
    def __init__(self, parent, project_controller, task_controller) -> None:
        super().__init__(parent)
        self.project_controller = project_controller
        self.task_controller = task_controller
        
        self.pack(fill='both', expand=True)
        self.create_widgets()
        self.refresh_projects()

    def create_widgets(self) -> None:
       
        main_frame = ttk.Frame(self)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        
        left_frame = ttk.LabelFrame(main_frame, text="Добавить/Редактировать проект", padding=10)
        left_frame.pack(side='left', fill='y', padx=(0, 5))
        
        
        right_frame = ttk.LabelFrame(main_frame, text="Список проектов", padding=10)
        right_frame.pack(side='right', fill='both', expand=True, padx=(5, 0))
        
        
        ttk.Label(left_frame, text="Название:").grid(row=0, column=0, sticky='w', pady=2)
        self.name_entry = ttk.Entry(left_frame, width=25)
        self.name_entry.grid(row=0, column=1, sticky='ew', pady=2, padx=(5, 0))
        
        ttk.Label(left_frame, text="Описание:").grid(row=1, column=0, sticky='nw', pady=2)
        self.description_text = tk.Text(left_frame, width=25, height=4)
        self.description_text.grid(row=1, column=1, sticky='ew', pady=2, padx=(5, 0))
        
        ttk.Label(left_frame, text="Дата начала:").grid(row=2, column=0, sticky='w', pady=2)
        self.start_date_entry = ttk.Entry(left_frame, width=25)
        self.start_date_entry.insert(0, (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"))
        self.start_date_entry.grid(row=2, column=1, sticky='ew', pady=2, padx=(5, 0))
        
        ttk.Label(left_frame, text="Дата окончания:").grid(row=3, column=0, sticky='w', pady=2)
        self.end_date_entry = ttk.Entry(left_frame, width=25)
        self.end_date_entry.insert(0, (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d"))
        self.end_date_entry.grid(row=3, column=1, sticky='ew', pady=2, padx=(5, 0))
        
        ttk.Label(left_frame, text="Статус:").grid(row=4, column=0, sticky='w', pady=2)
        self.status_var = tk.StringVar(value="active")
        status_combo = ttk.Combobox(left_frame, textvariable=self.status_var,
                                   values=["active", "completed", "on_hold"], 
                                   state="readonly", width=22)
        status_combo.grid(row=4, column=1, sticky='ew', pady=2, padx=(5, 0))
        
        
        button_frame = ttk.Frame(left_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="Добавить проект", 
                  command=self.add_project).pack(side='left', padx=(0, 5))
        ttk.Button(button_frame, text="Обновить проект", 
                  command=self.update_project).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Удалить выбранный", 
                  command=self.delete_selected).pack(side='left', padx=(5, 0))
        
        
        self.progress_frame = ttk.LabelFrame(left_frame, text="Прогресс проекта", padding=5)
        self.progress_frame.grid(row=6, column=0, columnspan=2, pady=10, sticky='ew')
        
        self.progress_label = ttk.Label(self.progress_frame, text="Выберите проект")
        self.progress_label.pack(pady=5)
        
        
        control_frame = ttk.Frame(right_frame)
        control_frame.pack(fill='x', pady=(0, 10))
        
        ttk.Button(control_frame, text="Обновить список", 
                  command=self.refresh_projects).pack(side='right')
        
        ttk.Button(control_frame, text="Показать задачи", 
                  command=self.show_project_tasks).pack(side='right', padx=(0, 5))
        
        
        columns = ("ID", "Название", "Статус", "Начало", "Окончание", "Прогресс", "Задач")
        self.projects_tree = ttk.Treeview(right_frame, columns=columns, show='headings', height=15)
        
        
        column_widths = {
            "ID": 50,
            "Название": 150,
            "Статус": 100,
            "Начало": 100,
            "Окончание": 100,
            "Прогресс": 80,
            "Задач": 60
        }
        
        for col in columns:
            self.projects_tree.heading(col, text=col)
            self.projects_tree.column(col, width=column_widths.get(col, 100))
        
        
        scrollbar = ttk.Scrollbar(right_frame, orient='vertical', command=self.projects_tree.yview)
        self.projects_tree.configure(yscrollcommand=scrollbar.set)
        
        self.projects_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        
        self.projects_tree.bind('<<TreeviewSelect>>', self.on_project_select)

    def refresh_projects(self) -> None:
        
        try:
            
            for item in self.projects_tree.get_children():
                self.projects_tree.delete(item)
            
            
            projects = self.project_controller.get_all_projects()
            
            
            for project in projects:
                
                tasks_count = len(self.task_controller.get_tasks_by_project(project.id))
                
                
                progress = self.project_controller.get_project_progress(project.id)
                
                
                status_map = {
                    "active": "Активный",
                    "completed": "Завершен", 
                    "on_hold": "На паузе"
                }
                status_text = status_map.get(project.status, project.status)
                
                self.projects_tree.insert("", "end", values=(
                    project.id,
                    project.name,
                    status_text,
                    project.start_date.strftime("%Y-%m-%d"),
                    project.end_date.strftime("%Y-%m-%d"),
                    f"{progress}%",
                    tasks_count
                ))
                
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить проекты: {e}")

    def add_project(self) -> None:
        
        try:
            # Получаем данные из формы
            name = self.name_entry.get().strip()
            description = self.description_text.get("1.0", "end-1c").strip()
            start_date_str = self.start_date_entry.get().strip()
            end_date_str = self.end_date_entry.get().strip()
            status = self.status_var.get()
            
            
            if not name:
                messagebox.showwarning("Предупреждение", "Введите название проекта")
                return
            
            
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
            
            
            project_id = self.project_controller.add_project(
                name=name,
                description=description,
                start_date=start_date,
                end_date=end_date
            )
            
            
            if status != "active":
                self.project_controller.update_project_status(project_id, status)
            
            messagebox.showinfo("Успех", f"Проект '{name}' добавлен с ID: {project_id}")
            
            
            self.clear_form()
            self.refresh_projects()
            
        except ValueError as e:
            messagebox.showerror("Ошибка", f"Некорректные данные: {e}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось добавить проект: {e}")

    def update_project(self) -> None:
        
        selected = self.projects_tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите проект для редактирования")
            return
        
        project_id = self.projects_tree.item(selected[0])['values'][0]
        
        try:
           
            name = self.name_entry.get().strip()
            description = self.description_text.get("1.0", "end-1c").strip()
            start_date_str = self.start_date_entry.get().strip()
            end_date_str = self.end_date_entry.get().strip()
            status = self.status_var.get()
            
            if not name:
                messagebox.showwarning("Предупреждение", "Введите название проекта")
                return
            
            
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
            
            
            self.project_controller.update_project(
                project_id,
                name=name,
                description=description,
                start_date=start_date,
                end_date=end_date,
                status=status
            )
            
            messagebox.showinfo("Успех", f"Проект '{name}' обновлен")
            self.refresh_projects()
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось обновить проект: {e}")

    def delete_selected(self) -> None:
        
        selected = self.projects_tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите проект для удаления")
            return
        
        project_id = self.projects_tree.item(selected[0])['values'][0]
        project_name = self.projects_tree.item(selected[0])['values'][1]
        
        if messagebox.askyesno("Подтверждение", f"Удалить проект '{project_name}'?"):
            try:
                if self.project_controller.delete_project(project_id):
                    messagebox.showinfo("Успех", "Проект удален")
                    self.refresh_projects()
                    self.clear_form()
                else:
                    messagebox.showerror("Ошибка", "Не удалось удалить проект")
            except ValueError as e:
                messagebox.showerror("Ошибка", f"Нельзя удалить проект: {e}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка при удалении: {e}")

    def on_project_select(self, event):
        
        selected = self.projects_tree.selection()
        if selected:
            
            values = self.projects_tree.item(selected[0])['values']
            
            self.name_entry.delete(0, 'end')
            self.name_entry.insert(0, values[1])
            
            
            project_id = values[0]
            project = self.project_controller.get_project(project_id)
            if project:
                self.description_text.delete("1.0", "end")
                self.description_text.insert("1.0", project.description or "")
                
                self.start_date_entry.delete(0, 'end')
                self.start_date_entry.insert(0, project.start_date.strftime("%Y-%m-%d"))
                
                self.end_date_entry.delete(0, 'end')
                self.end_date_entry.insert(0, project.end_date.strftime("%Y-%m-%d"))
                
               
                status_map_reverse = {
                    "Активный": "active",
                    "Завершен": "completed",
                    "На паузе": "on_hold"
                }
                self.status_var.set(status_map_reverse.get(values[2], "active"))
                
                
                progress = self.project_controller.get_project_progress(project_id)
                tasks_count = len(self.task_controller.get_tasks_by_project(project_id))
                self.progress_label.config(
                    text=f"Прогресс: {progress}%\nЗадач: {tasks_count}"
                )

    def show_project_tasks(self):
        
        selected = self.projects_tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите проект")
            return
        
        project_id = self.projects_tree.item(selected[0])['values'][0]
        project_name = self.projects_tree.item(selected[0])['values'][1]
        
        tasks = self.task_controller.get_tasks_by_project(project_id)
        
        if not tasks:
            messagebox.showinfo("Информация", f"В проекте '{project_name}' нет задач")
            return
        
      
        tasks_window = tk.Toplevel(self)
        tasks_window.title(f"Задачи проекта: {project_name}")
        tasks_window.geometry("600x400")
        
        
        columns = ("ID", "Название", "Приоритет", "Статус", "Срок")
        tasks_tree = ttk.Treeview(tasks_window, columns=columns, show='headings', height=15)
        
        for col in columns:
            tasks_tree.heading(col, text=col)
            tasks_tree.column(col, width=100)
        
        tasks_tree.column("Название", width=200)
        
       
        for task in tasks:
            priority_map = {1: "Высокий", 2: "Средний", 3: "Низкий"}
            status_map = {"pending": "Ожидает", "in_progress": "В работе", "completed": "Завершена"}
            
            tasks_tree.insert("", "end", values=(
                task.id,
                task.title,
                priority_map.get(task.priority, "Неизвестно"),
                status_map.get(task.status, task.status),
                task.due_date.strftime("%Y-%m-%d")
            ))
        
        scrollbar = ttk.Scrollbar(tasks_window, orient='vertical', command=tasks_tree.yview)
        tasks_tree.configure(yscrollcommand=scrollbar.set)
        
        tasks_tree.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        scrollbar.pack(side='right', fill='y', pady=10)

    def clear_form(self):
        
        self.name_entry.delete(0, 'end')
        self.description_text.delete("1.0", "end")
        self.start_date_entry.delete(0, 'end')
        self.start_date_entry.insert(0, (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"))
        self.end_date_entry.delete(0, 'end')
        self.end_date_entry.insert(0, (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d"))
        self.status_var.set("active")
        self.progress_label.config(text="Выберите проект")
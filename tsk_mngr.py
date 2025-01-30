#Менеджер задач

#Задача: Создай класс `Task`, который позволяет управлять задачами (делами).
#У задачи должны быть атрибуты: описание задачи, срок выполнения и статус
#(выполнено/не выполнено). Реализуй функцию для добавления задач, отметки
#выполненных задач и вывода списка текущих (не выполненных) задач.

import datetime
class Task:
    def __init__(self, name, description, due_date, status=False):
        self.name = name
        self.description = description
        try:
            self.due_date = datetime.datetime.strptime(due_date, '%d.%m.%Y').date()
        except ValueError:
            raise ValueError("Неверный формат даты! Используйте 'ДД.ММ.ГГГГ'")
        self.status = status

    def mark_as_done(self):
        self.status = True

    def mark_as_undone(self):
        self.status = False

    def __repr__(self):
        return f"{self.name}: {self.description}, до {self.due_date.strftime('%d.%m.%Y')}, {'Выполнена' if self.status else 'Не выполнена'}"


import tkinter as tk
from tkinter import messagebox, filedialog
from functools import partial
import pickle


# Функция для сохранения задач в файл
def save_tasks(tasks, filename="tasks.pkl"):
    with open(filename, 'wb') as file:
        pickle.dump(tasks, file)


# Функция для загрузки задач из файла
def load_tasks(filename="tasks.pkl"):
    try:
        with open(filename, 'rb') as file:
            tasks = pickle.load(file)
        return tasks
    except FileNotFoundError:
        return []


# Главная функция приложения
def main():
    # Загрузка задач из файла
    tasks = load_tasks()

    # Окно главного меню
    root = tk.Tk()
    root.title("Менеджер задач")

    # Лэйбл для отображения статуса списка задач
    label_status = tk.Label(root,
                            text=f"В списке {'есть' if any(task.status == False for task in tasks) else 'нет'} невыполненны{'е' if any(task.status == False for task in tasks) else 'х'} зада{'чи' if any(task.status == False for task in tasks) else 'ч'}.")
    label_status.pack(pady=10)

    # Кнопки для вызова различных функций
    button_add_task = tk.Button(root, text="Добавить задачу", command=lambda: add_task_window(root, tasks))
    button_mark_done = tk.Button(root, text="Отметить выполнение", command=lambda: mark_done_window(root, tasks))
    button_view_current_tasks = tk.Button(root, text="Просмотреть текущие задачи",
                                          command=lambda: view_current_tasks_window(root, tasks))
    button_view_old_tasks = tk.Button(root, text="Просмотреть выполненные задачи",
                                      command=lambda: view_old_tasks_window(root, tasks))

    button_add_task.pack(pady=5)
    button_mark_done.pack(pady=5)
    button_view_current_tasks.pack(pady=5)
    button_view_old_tasks.pack(pady=5)

    # Обновляем статус списка задач при изменении
    def update_label_status():
        label_status.config(
            text=f"В списке {'есть' if any(task.status == False for task in tasks) else 'нет'} невыполненных задач.")

    # Функции для работы с задачами

    # Окно для добавления новой задачи
    def add_task_window(parent, tasks):
        def on_save():
            name = entry_name.get().strip()
            description = entry_description.get("1.0", tk.END).strip()
            due_date = entry_due_date.get().strip()

            if not name or not description or not due_date:
                messagebox.showerror("Ошибка", "Пожалуйста, заполните все поля!")
                return

            try:
                new_task = Task(name, description, due_date)
                tasks.append(new_task)
                save_tasks(tasks)
                update_label_status()
                window.destroy()
            except ValueError as e:
                messagebox.showerror("Ошибка", str(e))

        def on_cancel():
            window.destroy()

        window = tk.Toplevel(parent)
        window.title("Добавить задачу")

        label_name = tk.Label(window, text="Название задачи:")
        label_description = tk.Label(window, text="Описание задачи:")
        label_due_date = tk.Label(window, text="Срок выполнения (ДД.ММ.ГГГГ):")

        entry_name = tk.Entry(window)
        entry_description = tk.Text(window, height=5, width=30)
        entry_due_date = tk.Entry(window)

        button_save = tk.Button(window, text="Сохранить", command=on_save)
        button_cancel = tk.Button(window, text="Отмена", command=on_cancel)

        label_name.grid(row=0, column=0, sticky='w', pady=5)
        entry_name.grid(row=0, column=1, padx=5, pady=5)

        label_description.grid(row=1, column=0, sticky='nw', pady=5)
        entry_description.grid(row=1, column=1, rowspan=3, padx=5, pady=5)

        label_due_date.grid(row=4, column=0, sticky='w', pady=5)
        entry_due_date.grid(row=4, column=1, padx=5, pady=5)

        button_save.grid(row=5, column=0, pady=5)
        button_cancel.grid(row=5, column=1, pady=5)

    # Окно для отметки выполнения задач
    def mark_done_window(parent, tasks):
        def on_save():
            for i, var in enumerate(vars):
                if var.get() == 1:
                    tasks[i].mark_as_done()
            save_tasks(tasks)
            update_label_status()
            window.destroy()

        def on_cancel():
            window.destroy()

        window = tk.Toplevel(parent)
        window.title("Отметить выполнение")

        vars = []
        labels = []

        for i, task in enumerate(tasks):
            if not task.status:
                var = tk.IntVar(value=0)
                label = tk.Checkbutton(window, text=task.name, variable=var)
                label.pack(anchor='w')
                vars.append(var)
                labels.append(label)

        button_save = tk.Button(window, text="Сохранить", command=on_save)
        button_cancel = tk.Button(window, text="Отмена", command=on_cancel)

        button_save.pack(pady=5)
        button_cancel.pack(pady=5)

    # Окно для просмотра текущих (невыполненных) задач
    def view_current_tasks_window(parent, tasks):
        def select_task(event):
            index = listbox.curselection()[0]
            selected_task = tasks[index]
            text_description.delete('1.0', tk.END)
            text_description.insert(tk.END, selected_task.description + "\nЗадачу необходимо выполнить до: " + selected_task.due_date.strftime('%d.%m.%Y'))
            listbox.itemconfig(index, fg='blue')

        def deselect_task(event):
            index = listbox.curselection()[0]
            listbox.itemconfig(index, fg='black')
            text_description.delete('1.0', tk.END)

        window = tk.Toplevel(parent)
        window.title("Текущие задачи")

        frame_listbox = tk.Frame(window)
        frame_description = tk.Frame(window)

        listbox = tk.Listbox(frame_listbox, width=40, height=10)
        scrollbar = tk.Scrollbar(frame_listbox, orient=tk.VERTICAL, command=listbox.yview)
        listbox.config(yscrollcommand=scrollbar.set)

        text_description = tk.Text(frame_description, width=50, height=10)

        button_back = tk.Button(window, text="Вернуться в главное меню", command=window.destroy)

        for task in tasks:
            if not task.status:
                listbox.insert(tk.END, task.name)

        listbox.bind('<<ListboxSelect>>', select_task)
        listbox.bind('<Double-Button-1>', deselect_task)

        frame_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        frame_description.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        text_description.pack(fill=tk.BOTH, expand=True)

        button_back.pack(side=tk.BOTTOM, pady=10)

    # Окно для просмотра старых (выполненных) задач
    def view_old_tasks_window(parent, tasks):
        def on_save():
            for i, var in enumerate(vars):
                if var.get() == 1:
                    tasks[i].mark_as_undone()
            save_tasks(tasks)
            update_label_status()
            window.destroy()

        def on_cancel():
            window.destroy()

        window = tk.Toplevel(parent)
        window.title("Просмотр старых задач")

        vars = []
        labels = []

        for i, task in enumerate(tasks):
            if task.status:
                var = tk.IntVar(value=0)
                label = tk.Checkbutton(window, text=task.name, variable=var)
                label.pack(anchor='w')
                vars.append(var)
                labels.append(label)

        button_save = tk.Button(window, text="Сохранить", command=on_save)
        button_cancel = tk.Button(window, text="Отмена", command=on_cancel)

        button_save.pack(pady=5)
        button_cancel.pack(pady=5)

    root.mainloop()


if __name__ == "__main__":
    main()

#Менеджер задач

#Задача: Создай класс `Task`, который позволяет управлять задачами (делами).
#У задачи должны быть атрибуты: описание задачи, срок выполнения и статус
#(выполнено/не выполнено). Реализуй функцию для добавления задач, отметки
#выполненных задач и вывода списка текущих (не выполненных) задач.

class Task ():
    def __init__(self, description, expiration, status=False):
        self.description = description
        self.expiration = expiration
        self.status = status
    def add_task (self):

    def mark_done(self):

    def show_tasks(self):

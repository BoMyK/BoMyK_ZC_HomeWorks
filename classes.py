#Разработай систему управления учетными записями пользователей
# для небольшой компании. Компания разделяет сотрудников на
# обычных работников и администраторов. У каждого сотрудника
# есть уникальный идентификатор (ID), имя и уровень доступа.
# Администраторы, помимо обычных данных пользователей, имеют
# дополнительный уровень доступа и могут добавлять или
# удалять пользователя из системы.

#Требования:
#1.Класс `User*: Этот класс должен инкапсулировать данные о пользователе:
# ID, имя и уровень доступа ('user' для обычных сотрудников).
#2.Класс `Admin`: Этот класс должен наследоваться от класса `User`.
# Добавь дополнительный атрибут уровня доступа, специфичный для администраторов ('admin').
# Класс должен также содержать методы `add_user` и `remove_user`, которые
# позволяют добавлять и удалять пользователей из списка
# (представь, что это просто список экземпляров `User`).
#3.Инкапсуляция данных: Убедись, что атрибуты классов защищены от
# прямого доступа и модификации снаружи. Предоставь доступ к необходимым
# атрибутам через методы (например, get и set методы).
class User:
    def __init__(self, user_id, name):
        self.__id = user_id
        self.__name = name
        self.__access_level = 'user'

    # Приватные методы для доступа к защищённым атрибутам
    def _get_id(self):
        return self.__id

    def _get_name(self):
        return self.__name

    def _get_access_level(self):
        return self.__access_level

    def _set_name(self, new_name):
        if isinstance(new_name, str):
            self.__name = new_name


class Admin(User):
    users = []  # Общий список пользователей для всех админов

    def __init__(self, admin_id, name):
        super().__init__(admin_id, name)
        self.__access_level = 'admin'

    # Геттеры
    def get_id(self, user):
        return user._get_id()

    def get_name(self, user):
        return user._get_name()

    def get_access_level(self, user):
        return user._get_access_level()

    # Сеттеры
    def set_name(self, user, new_name):
        user._set_name(new_name)

    def add_user(self, user): # Добавление нового пользователя
        if not isinstance(user, User):
            raise TypeError("Добавляемый объект должен быть экземпляром класса User")
        Admin.users.append(user)
        print(f"Пользователь {self.get_name(user)} добавлен в список пользователей.")

    def remove_user(self, user):  # Удаление пользователя
        try:
            index = Admin.users.index(user)
            removed_user = Admin.users.pop(index)
            print(f"Пользователь {self.get_name(removed_user)} удален из списка пользователей.")
        except ValueError:
            print(f"Пользователь {self.get_name(user)} не найден в списке пользователей.")

# Пример использования
# Создание двух админов
admin1 = Admin(101, "Петр Петров")
admin2 = Admin(102, "Анна Иванова")

# Создание обычных юзеров
user1 = User(1, "Иван Иванов")
user2 = User(2, "Сидор Сидоров")
user3 = User(3,"Павел Павлов")

# Добавляем пользователя через разных админов в список с проверкой
admin1.add_user(user1)
print(f"Проверяем список одного админа")
for user in Admin.users:
    print(admin1.get_name(user))
print(f"Проверяем список другого админа")
for user in Admin.users:
    print(admin2.get_name(user))

admin2.add_user(user2)
print(f"Опять проверяем список админа после добавления")
for user in Admin.users:
    print(admin1.get_name(user))
print(f"И тоже у второго админа")
for user in Admin.users:
    print(admin1.get_name(user))

# Удаляем пользователя через админов
admin1.remove_user(user3) #Пользователь не из списка
admin2.remove_user(user1)

print(f"Проверяем список другого админа после удаления")
for user in Admin.users:
    print(admin1.get_name(user))
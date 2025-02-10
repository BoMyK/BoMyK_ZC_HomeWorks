import json
import os


# 1. Базовый класс Animal
class Animal:
    def __init__(self, name, age, sound):
        self.name = name
        self.age = age
        self.sound = sound

    def make_sound(self):
        print(f"{self.name} говорит: {self.sound}")

    def eat(self):
        print(f"{self.name} кушает.")


# 2. Подклассы Bird, Mammal, и Reptile
class Bird(Animal):
    def __init__(self, name, age, sound, wingspan):
        super().__init__(name, age, sound)
        self.wingspan = wingspan


class Mammal(Animal):
    def __init__(self, name, age, sound, fur_color):
        super().__init__(name, age, sound)
        self.fur_color = fur_color


class Reptile(Animal):
    def __init__(self, name, age, sound, scale_type):
        super().__init__(name, age, sound)
        self.scale_type = scale_type


# 3. Полиморфизм
def animal_sound(animals):
    for animal in animals:
        animal.make_sound()


# 4. Классы для сотрудников
class ZooKeeper:
    def __init__(self, name):
        self.name = name

    def feed_animal(self, animal):
        print(f"{self.name} кормит животное {animal.name}.")


class Vet:
    def __init__(self, name):
        self.name = name

    def treat_animal(self, animal):
        print(f"{self.name} лечит животное {animal.name}.")


# 5. Класс Zoo с использованием композиции
class Zoo:
    def __init__(self):
        self.animals = []
        self.staff = []

    def add_animal(self, animal):
        self.animals.append(animal)
        print(f"Животное {animal.name} добавлено в зоопарк.")

    def add_staff(self, staff_member):
        self.staff.append(staff_member)
        print(f"Сотрудник {staff_member.name} добавлен в зоопарк.")

    def save_to_file(self, filename):
        zoo_data = {
            "animals": [{"type": type(animal).__name__, "name": animal.name, "age": animal.age, "sound": animal.sound}
                        for animal in self.animals],
            "staff": [{"type": type(staff).__name__, "name": staff.name} for staff in self.staff]
        }
        with open(filename, 'w') as file:
            json.dump(zoo_data, file)
        print(f"Данные зоопарка сохранены в файл {filename}.")

    def load_from_file(self, filename):
        if not os.path.exists(filename) or os.path.getsize(filename) == 0:
            print("Файл с данными о зоопарке не найден.")
            return

        with open(filename, 'r') as file:
            zoo_data = json.load(file)

        for animal_data in zoo_data["animals"]:
            if animal_data["type"] == "Bird":
                animal = Bird(animal_data["name"], animal_data["age"], animal_data["sound"], wingspan=0)
            elif animal_data["type"] == "Mammal":
                animal = Mammal(animal_data["name"], animal_data["age"], animal_data["sound"], fur_color="")
            elif animal_data["type"] == "Reptile":
                animal = Reptile(animal_data["name"], animal_data["age"], animal_data["sound"], scale_type="")
            self.animals.append(animal)

        for staff_data in zoo_data["staff"]:
            if staff_data["type"] == "ZooKeeper":
                staff = ZooKeeper(staff_data["name"])
            elif staff_data["type"] == "Vet":
                staff = Vet(staff_data["name"])
            self.staff.append(staff)

        print(f"Zoo data loaded from {filename}.")

    def display_zoo_info(self):
        if not self.animals and not self.staff:
            print("Зоопарк пуст.")
        else:
            print("Сейчас в зоопарке:")
            if self.animals:
                print("Животные:")
                for animal in self.animals:
                    print(f"- {animal.name} ({type(animal).__name__}), возраст: {animal.age}, звук: {animal.sound}")
            if self.staff:
                print("Сотрудники:")
                for staff in self.staff:
                    print(f"- {staff.name} ({type(staff).__name__})")


# Демонстрация работы
if __name__ == "__main__":
    zoo = Zoo()
    filename = "zoo_data.json"

    # Проверка существования файла и загрузка данных
    if os.path.exists(filename) and os.path.getsize(filename) > 0:
        zoo.load_from_file(filename)
        zoo.display_zoo_info()

        # Запрос на перезапись данных
        response = input("Хотите перезаписать данные зоопарка? (да/нет): ").strip().lower()
        if response != "да":
            print("Программа завершена.")
            exit()
        else:
            # Очищаем текущие данные зоопарка
            zoo = Zoo()
            print("Создаем новый зоопаркт.")
    else:
        print("Файл зоопарка пуст или не существует. Создаем новый зоопарк.")

    # Добавляем животных
    parrot = Bird("Попугай", 5, "Фьють!", 30)
    cow = Mammal("Корова", 7, "Мууу!", "Чернобелая")
    cat = Mammal("Кот", 3, "Мяу!", "Рыжий")
    lion = Mammal("Большой кот", 8, "Р-р-р!", "Золотистый")
    snake = Reptile("Змея", 3, "Ш-ш-ш!", "Гладкая")

    zoo.add_animal(parrot)
    zoo.add_animal(cow)
    zoo.add_animal(cat)
    zoo.add_animal(lion)
    zoo.add_animal(snake)

    # Добавляем сотрудников
    keeper1 = ZooKeeper("Иван Жирафов")
    keeper2 = ZooKeeper("Василий Бабочкин")
    vet1 = Vet("Доктор Айболит")
    vet2 = Vet("Доктор Дулиттл")

    zoo.add_staff(keeper1)
    zoo.add_staff(keeper2)
    zoo.add_staff(vet1)
    zoo.add_staff(vet2)

    # Демонстрация полиморфизма
    animal_sound(zoo.animals)

    # Сотрудники зоопарка в работе
    keeper1.feed_animal(cat)
    vet1.treat_animal(lion)
    keeper2.feed_animal(parrot)
    vet2.treat_animal(cow)

    # Сохраняем данные в файл
    zoo.save_to_file(filename)
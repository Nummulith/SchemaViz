class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        raise NotImplementedError("Subclasses should implement this!")

# Функция для создания дочернего класса
def create_class(class_name, base_classes, attributes):
    # Добавляем стандартные атрибуты
    attrs = {key: None for key in attributes if not callable(attributes[key])}
    # Добавляем функции (методы) и проверяем, статические ли они
    methods = {
        key: (staticmethod(value) if key.startswith("static_") else value)
        for key, value in attributes.items() if callable(value)
    }

    # Объединяем атрибуты и методы и создаем дочерний класс
    return type(class_name, base_classes, {**attrs, **methods})

# Пример статического метода
def make_static_bark(saying):
    @staticmethod
    def static_bark():
        return saying + "!"
    return static_bark

# Создаем дочерний класс Cat, наследуемый от Animal
Cat = create_class("Cat", (Animal,), {
    "flag": bool, 
    "speak": lambda self: f"{self.name} says meow",
    "static_bark": make_static_bark("mew")
})

# Создаем дочерний класс Dog, наследуемый от Animal
Dog = create_class("Dog", (Animal,), {
    "flag": bool, 
    "speak": lambda self: f"{self.name} says woof",
    "static_bark": make_static_bark("woof")
})

# Проверка
cat_instance = Cat("Kitty")
dog_instance = Dog("Buddy")

print(cat_instance.speak())  # Выведет: Kitty says meow
print(dog_instance.speak())  # Выведет: Buddy says woof
print(Cat.static_bark())     # Выведет: mew!
print(Dog.static_bark())     # Выведет: woof!

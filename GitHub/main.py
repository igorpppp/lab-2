"""ЛБ №2: п'ять демонстрацій принципів ООП. Python 3.10+."""
from abc import ABC, abstractmethod

# 1. Спадковість і поліморфізм: предметна область — транспорт
class Transport:
    def __init__(self, name: str, capacity: int):
        self.name, self.capacity = name, capacity
    def travel(self, distance: int) -> str:
        return f"{self.name}: маршрут {distance} км"
    def __str__(self):
        return f"{self.name} (місць: {self.capacity})"

class Bus(Transport):
    def __init__(self, name, capacity, stops):
        super().__init__(name, capacity); self.stops = stops
    def travel(self, distance):
        return f"Автобус {self.name}: {distance} км, зупинок {self.stops}"

class Train(Transport):
    def __init__(self, name, capacity, wagons):
        super().__init__(name, capacity); self.wagons = wagons
    def travel(self, distance):
        return f"Потяг {self.name}: {distance} км, вагонів {self.wagons}"

class Bicycle(Transport):
    def __init__(self, name, capacity, gears):
        super().__init__(name, capacity); self.gears = gears
    def travel(self, distance):
        return f"Велосипед {self.name}: {distance} км, передач {self.gears}"

# 2. Інкапсуляція: окрема предметна область — навчальні оцінки
class GradeRecord:
    def __init__(self, student, score):
        self._student = student
        self.__score = 0
        self.score = score
    @property
    def score(self):
        return self.__score
    @score.setter
    def score(self, value):
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError("Оцінка повинна бути числом")
        if not 0 <= value <= 100:
            raise ValueError("Оцінка має бути від 0 до 100")
        self.__score = value
    @property
    def passed(self):
        return self.score >= 60

# 3. Магічні методи: вектор із двома координатами
class Vector2:
    def __init__(self, x, y):
        self.x, self.y = float(x), float(y)
    def __str__(self):
        return f"({self.x:g}; {self.y:g})"
    def __repr__(self):
        return f"Vector2({self.x!r}, {self.y!r})"
    def __add__(self, other):
        if not isinstance(other, Vector2): return NotImplemented
        return Vector2(self.x + other.x, self.y + other.y)
    def __sub__(self, other):
        if not isinstance(other, Vector2): return NotImplemented
        return Vector2(self.x - other.x, self.y - other.y)
    def __eq__(self, other):
        if not isinstance(other, Vector2): return NotImplemented
        return (self.x, self.y) == (other.x, other.y)
    def __abs__(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5

# 4. Абстракція та композиція: доставка посилок
class Delivery(ABC):
    @property
    @abstractmethod
    def method(self): ...
    @abstractmethod
    def cost(self, weight): ...
    @abstractmethod
    def eta(self): ...
    def summary(self, weight):
        return f"{self.method}: {self.cost(weight)} грн, {self.eta()} дн."

class Courier(Delivery):
    @property
    def method(self): return 'Кур’єр'
    def cost(self, weight): return 70 + weight * 12
    def eta(self): return 1

class Post(Delivery):
    @property
    def method(self): return 'Пошта'
    def cost(self, weight): return 35 + weight * 8
    def eta(self): return 3

class ParcelOrder:
    def __init__(self, delivery: Delivery, weight: float):
        self.delivery, self.weight = delivery, weight
    def checkout(self):
        return self.delivery.summary(self.weight)

# 5. Strategy: рекомендації книг (нова предметна область)
class RecommendationStrategy(ABC):
    @abstractmethod
    def choose(self, books): ...

class Cheapest(RecommendationStrategy):
    def choose(self, books): return min(books, key=lambda b: b['price'])

class HighestRated(RecommendationStrategy):
    def choose(self, books): return max(books, key=lambda b: b['rating'])

class Newest(RecommendationStrategy):
    def choose(self, books): return max(books, key=lambda b: b['year'])

class BookRecommender:
    def __init__(self, strategy: RecommendationStrategy): self.strategy = strategy
    def recommend(self, books): return self.strategy.choose(books)


def main():
    print('ЗАВДАННЯ 1 — Поліморфізм')
    fleet = [Bus('Міський', 40, 12), Train('Експрес', 300, 8), Bicycle('Турист', 1, 21)]
    for item in fleet: print(str(item), '→', item.travel(15))
    print('isinstance:', isinstance(fleet[0], Transport), 'issubclass:', issubclass(Train, Transport))
    print('\nЗАВДАННЯ 2 — Інкапсуляція')
    record = GradeRecord('Студент', 75)
    print('Оцінка:', record.score, 'Склав:', record.passed)
    for bad in (-5, 'сто'):
        try: record.score = bad
        except (TypeError, ValueError) as exc: print(type(exc).__name__, str(exc))
    try: print(record.__score)
    except AttributeError: print('Прямий доступ __score заблоковано')
    print('Name mangling:', record._GradeRecord__score)
    record.score = 55
    print('Після зміни оцінки склав:', record.passed)
    print('\nЗАВДАННЯ 3 — Магічні методи')
    a, b = Vector2(3, 4), Vector2(1, 2)
    print('str:', str(a), 'repr:', repr(a), '+:', a+b, '-:', a-b, '==:', a==b, 'abs:', abs(a))
    print('\nЗАВДАННЯ 4 — ABC та композиція')
    try: Delivery()
    except TypeError: print('Абстрактний Delivery не можна створити')
    for method in (Courier(), Post()): print(ParcelOrder(method, 2).checkout())
    print('\nЗАВДАННЯ 5 — Strategy')
    books = BOOKS
    for strategy in (Cheapest(), HighestRated(), Newest()):
        print(type(strategy).__name__, '→', BookRecommender(strategy).recommend(books)['title'])

BOOKS = [{'title':'Алгоритми щодня','price':270,'rating':4.7,'year':2025},{'title':'Короткі історії','price':150,'rating':4.4,'year':2022},{'title':'Шлях до знань','price':330,'rating':5.0,'year':2024}]
if __name__ == '__main__': main()

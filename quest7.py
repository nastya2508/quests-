#Глибина познання

from abc import ABC, abstractmethod


class Transport(ABC):

    def __init__(self, name: str, speed: int, capacity: int):
        self.name = name
        self.speed = speed
        self.capacity = capacity

    @abstractmethod
    def move(self, distance: float) -> float:
        pass

    @abstractmethod
    def fuel_consumption(self, distance: float):
        pass

    @abstractmethod
    def info(self) -> str:
        pass

    def calculate_cost(self, distance: float, price_per_unit: float) -> float:
        spent = self.fuel_consumption(distance)
        if spent == "Перевантажено!":
            return 0
        return spent * price_per_unit


class Car(Transport):

    def move(self, distance: float) -> float:
        return distance / self.speed

    def fuel_consumption(self, distance: float) -> float:
        return distance * 0.07

    def info(self) -> str:
        return f"Машина: {self.name}"


class Bus(Transport):

    def __init__(
        self, name: str, speed: int, capacity: int, passengers: int = 0
    ):
        super().__init__(name, speed, capacity)
        self.passengers = passengers  

    def move(self, distance: float) -> float:
        return distance / self.speed

    def fuel_consumption(self, distance: float):
        if self.passengers > self.capacity:
            return "Перевантажено!"
        return distance * 0.15

    def info(self) -> str:
        return f"Автобус: {self.name}"


class Bicycle(Transport):

    def __init__(self, name: str, speed: int, capacity: int = 1):
        if speed > 20:
            speed = 20
        super().__init__(name, speed, capacity)

    def move(self, distance: float) -> float:
        return distance / self.speed

    def fuel_consumption(self, distance: float) -> float:
        return 0

    def info(self) -> str:
        return f"Велосипед: {self.name}"


class ElectricCar(Car):

    def battery_usage(self, distance: float) -> float:
        return distance * 0.2

    def fuel_consumption(self, distance: float) -> float:
        return 0

    def calculate_cost(self, distance: float, price_per_unit: float) -> float:
        return self.battery_usage(distance) * price_per_unit

    def info(self) -> str:
        return f"Електрокар: {self.name}"


transports = [
    Car("Toyota", speed=100, capacity=5),
    Bus("Богдан", speed=50, capacity=30, passengers=20),
    Bus("Маршрутка", speed=40, capacity=15, passengers=22),  
    Bicycle("Ardis", speed=30, capacity=1), 
    ElectricCar("Tesla", speed=100, capacity=5),
]

distance = 100  

for t in transports:
    time = t.move(distance)
    fuel = t.fuel_consumption(distance)

    print(f"Назва: {t.name}")
    print(f"  Час у дорозі на {distance} км: {time} год.")
    print(f"  Витрати пального: {fuel}")
    print("-" * 35)

print("\nРозрахунок вартості поїздки:")

car = transports[0]
print(
    f"{car.name} (бензин 55 грн/л): {car.calculate_cost(distance, 55.0)} грн"
)

tesla = transports[4]
print(
    f"{tesla.name} (електрика 4.32 грн/кВт): {tesla.calculate_cost(distance, 4.32)} грн"
)
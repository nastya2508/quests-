from abc import ABC, abstractmethod


class Medicine(ABC):
    def __init__(self, name: str, quantity: int, price: float):
        # Перевірка типів даних
        if not isinstance(name, str):
            raise TypeError("Назва (name) має бути рядком (str)")
        if not isinstance(quantity, int):
            raise TypeError("Кількість (quantity) має бути цілим числом (int)")
        if not isinstance(price, (int, float)):
            raise TypeError("Ціна (price) має бути числом (float або int)")

        self.name = name
        self.quantity = quantity
        self.price = float(price)

    @abstractmethod
    def requires_prescription(self) -> bool:
        """Чи потрібен рецепт (має бути реалізовано в кожному підкласі)."""
        pass

    @abstractmethod
    def storage_requirements(self) -> str:
        """Умови зберігання (має бути реалізовано в кожному підкласі)."""
        pass

    def total_price(self) -> float:
        """Базовий розрахунок вартості за замовчуванням."""
        return self.quantity * self.price

    def info(self) -> str:
        """Формування рядка з інформацією (використовує поліморфні методи)."""
        prescription = "Потрібен рецепт" if self.requires_prescription() else "Без рецепта"
        return (
            f"[{self.__class__.__name__}] {self.name} | "
            f"Кількість: {self.quantity} шт. | "
            f"Загальна сума: {self.total_price():.2f} грн | "
            f"Зберігання: {self.storage_requirements()} | "
            f"{prescription}"
        )


class Antibiotic(Medicine):
    def __init__(self, name: str, quantity: int, price: float):
        super().__init__(name, quantity, price)

    def requires_prescription(self) -> bool:
        return True

    def storage_requirements(self) -> str:
        return "8–15°C, темне місце"


class Vitamin(Medicine):
    def __init__(self, name: str, quantity: int, price: float):
        super().__init__(name, quantity, price)

    def requires_prescription(self) -> bool:
        return False

    def storage_requirements(self) -> str:
        return "15–25°C, сухо"


class Vaccine(Medicine):
    def __init__(self, name: str, quantity: int, price: float):
        super().__init__(name, quantity, price)

    def requires_prescription(self) -> bool:
        return True

    def storage_requirements(self) -> str:
        return "2–8°C, холодильник"

    def total_price(self) -> float:
        return super().total_price() * 1.10
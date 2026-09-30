#Домашнє прибирання
from abc import ABC, abstractmethod


class JunkItem:

    def __init__(self, name: str, quantity: int, value: float):
        self.name = name
        self.quantity = int(quantity)
        self.value = float(value)

    def __repr__(self):
        return f"JunkItem(назва='{self.name}', кількість={self.quantity}, ціна={self.value})"


class StorageBackend(ABC):

    @abstractmethod
    def save(self, items: list[JunkItem]):
        pass

    @abstractmethod
    def load(self) -> list[JunkItem]:
        pass


class FileJunkStorage(StorageBackend):

    def __init__(self, filename: str):
        self.filename = filename

    def serialize(self, items: list[JunkItem], filename: str):
        with open(filename, "w", encoding="utf-8") as f:
            for item in items:
                val_str = str(item.value).replace(".", ",")
                f.write(f"{item.name}|{item.quantity}|{val_str}\n")

    def parse(self, filename: str) -> list[JunkItem]:
        items = []
        try:
            with open(filename, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue

                    parts = line.split("|")

                    if len(parts) != 3:
                        print(
                            f"[УВАГА] Пропущено рядок (немає 3 полів): '{line}'"
                        )
                        continue

                    name, qty_str, val_str = parts

                    try:
                        quantity = int(qty_str)
                        value = float(val_str.replace(",", "."))
                        items.append(JunkItem(name, quantity, value))
                    except ValueError:
                        print(
                            f"[УВАГА] Пропущено рядок (помилка в числах): '{line}'"
                        )
                        continue
        except FileNotFoundError:
            print(f"[УВАГА] Файл {filename} ще не створено.")

        return items

    def save(self, items: list[JunkItem]):
        self.serialize(items, self.filename)

    def load(self) -> list[JunkItem]:
        return self.parse(self.filename)


class JunkWarehouse:

    def __init__(self, storage: StorageBackend):
        self.storage = storage
        self.items = self.storage.load()

    def add(self, item: JunkItem):
        self.items.append(item)
        self.storage.save(self.items)

    def get_all(self) -> list[JunkItem]:
        return self.items

    def find(self, name: str):
        for item in self.items:
            if item.name.lower() == name.lower():
                return item
        return None


if __name__ == "__main__":
    storage_file = "junk_data.txt"

    storage = FileJunkStorage(storage_file)
    warehouse = JunkWarehouse(storage)

    print("--- 1. Додавання предметів на склад ---")
    warehouse.add(JunkItem("Бляшанка", 5, 2.5))
    warehouse.add(JunkItem("Стара плата", 3, 7.8))
    warehouse.add(JunkItem("Купка дротів", 10, 1.2))

    with open(storage_file, "a", encoding="utf-8") as f:
        f.write("Зламане_залізо|не_число|3,5\n")
        f.write("Тільки одне поле\n")

    print("\n--- 2. Читання з файлу через новий об'єкт складу ---")
    new_warehouse = JunkWarehouse(FileJunkStorage(storage_file))

    print("\n--- 3. Успішно завантажені предмети ---")
    for item in new_warehouse.get_all():
        print(item)

    print("\n--- 4. Пошук предмета на складі ---")
    found = new_warehouse.find("Стара плата")
    print(f"Знайдено: {found}")
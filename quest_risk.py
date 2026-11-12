import threading
import time
import random

class Warehouse:
    def __init__(self, name, meds, price_per_unit):
        self.name = name
        self.meds = meds
        self.initial_meds = meds
        self.price_per_unit = price_per_unit
        self.total_stolen = 0
        self.lock = threading.Lock()

    def steal(self, amount):
        with self.lock:
            status = random.choices(["success", "partial", "caught"], weights=[70, 20, 10])[0]
            if status == "caught":
                return 0
            elif status == "partial":
                amount = amount // 2
                
            if amount > self.meds:
                amount = self.meds
            self.meds -= amount
            self.total_stolen += amount
            return amount

class Runner(threading.Thread):
    def __init__(self, name, warehouses):
        super().__init__()
        self.name = name
        self.warehouses = warehouses
        self.progress = 0

    def run(self):
        for _ in range(10):
            target_warehouse = random.choice(self.warehouses)
            stolen_amount = random.randint(10, 30)
            target_warehouse.steal(stolen_amount)
            self.progress += 1
            time.sleep(random.uniform(0.1, 0.5))

def print_progress(runners):
    while any(r.is_alive() for r in runners):
        bar_line = ""
        for r in runners:
            completed = r.progress
            bar = "#" * completed + "-" * (10 - completed)
            bar_line += f"{r.name}: [{bar}] {completed*10}%  "
        print(f"\r{bar_line}", end="", flush=True)
        time.sleep(0.05)
    print()

def run_simulation():
    warehouses = [
        Warehouse(f"Склад-{i+1}", random.randint(100, 300), random.randint(10, 20))
        for i in range(4)
    ]
    runners = [Runner(f"Бігун-{i+1}", warehouses) for i in range(5)]

    for r in runners:
        r.start()

    print_progress(runners)

    for r in runners:
        r.join()

    total_profit = 0
    for w in warehouses:
        profit = w.total_stolen * w.price_per_unit
        total_profit += profit
        assert w.meds >= 0, f"Інваріант зламався: на складі {w.name} менше 0 медикаментів!"
        assert w.initial_meds == w.meds + w.total_stolen, f"Інваріант зламався на {w.name}!"
    return total_profit

if __name__ == "__main__":
    print("=== Запуск симуляції 100 разів з перевіркою інваріантів ===")
    for run_idx in range(1, 101):
        run_simulation()
    print("Успішно пройдено 100 прогонів! Усі інваріанти виконуються.")
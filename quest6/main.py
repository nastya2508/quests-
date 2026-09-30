from models import Medicine, Antibiotic, Vitamin, Vaccine


def show_medicines_info(medicines: list[Medicine]):
    """
    Головна функція: просто викликає info() для кожного елемента.
    Тут немає жодної перевірки типу (if isinstance/type) — працює поліморфізм!
    """
    for item in medicines:
        print(item.info())


if __name__ == "__main__":
    medicines_list = [
        Antibiotic("Амоксицилін", 2, 150.0),
        Vitamin("Вітамін D3", 4, 90.0),
        Vaccine("Вакцина проти грипу", 3, 400.0),
        Vitamin("Вітамін C", 10, 45.0),
        Antibiotic("Азитроміцин", 1, 220.0),
    ]

    print("--- Інформація про медикаменти на складі ---")
    show_medicines_info(medicines_list)
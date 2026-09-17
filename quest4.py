
medicines = [
    ["Амоксицилін", 50, "antibiotic", 18.5],
    ["Вітамін D3", 100, "vitamin", 3.0],
    ["Вакцина від грипу", 25, "vaccine", 6.0],
    ["Парацетамол", "тридцять", "antibiotic", 20.0],  # помилка в кількості (str)
    ["Аспірин", 40, "painkiller", 22.0],  # невідома категорія
    ["Сироп від кашлю", 15, "vitamin", "12.5"],  # помилка в температурі (str)
    ["Очні краплі", 10, "vitamin", 27.0],
]

for med in medicines:
  name = med[0]
  quantity = med[1]
  category = med[2]
  temp = med[3]

  if type(quantity) != int or type(temp) != float:
    print(f"{name} — Помилка даних")
    continue

  match category:
    case "antibiotic":
      category_status = "Рецептурний препарат"
    case "vitamin":
      category_status = "Вільний продаж"
    case "vaccine":
      category_status = "Потребує спецзберігання"
    case _:
      category_status = "Невідома категорія"

  if temp < 5:
    temp_status = "Надто холодно"
  elif temp > 25:
    temp_status = "Надто жарко"
  else:
    temp_status = "Норма"

  print(f"{name}: {category_status}, {temp_status}")
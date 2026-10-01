deals = [
    ["Олена", 50.0, "clean"],
    ["Іван", 450, "suspicious"],
    ["Максим", 1500, "fraud"],
    ["Дмитро", "тисяча", "clean"],  
    ["Анна", 200.5, "vip"],  
]

for deal in deals:
  name = deal[0]
  amount = deal[1]
  status = deal[2]

  if type(amount) not in (int, float):
    print(f"{name} — Фальшиві дані")
    continue

  if amount < 100:
    amount_category = "Дрібнота"
  elif amount <= 999:
    amount_category = "Середнячок"
  else:
    amount_category = "Великий клієнт"

  match status:
    case "clean":
      decision = "Працювати без питань"
    case "suspicious":
      decision = "Перевірити документи"
    case "fraud":
      decision = "У чорний список"
    case _:
      decision = "Невідомий статус"

  print(f"{name}: {amount_category}, {decision}")
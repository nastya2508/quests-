num1 = float(input("Введіть перше число: "))
operation = input("Виберіть операцію (+, -, *, /): ").strip()
num2 = float(input("Введіть друге число: "))

if operation == "+":
    result = num1 + num2
    print(f"Результат: {num1} + {num2} = {result}")
elif operation == "-":
    result = num1 - num2
    print(f"Результат: {num1} - {num2} = {result}")
elif operation == "*":
    result = num1 * num2
    print(f"Результат: {num1} * {num2} = {result}")
elif operation == "/":
    if num2 == 0:
        print("Помилка: ділення на нуль неможливе!")
    else:
        result = num1 / num2
        print(f"Результат: {num1} / {num2} = {result}")
else:
    print("Помилка: невідома операція.")
from tracking import load_events, events_between

# Завантажуємо події з журналу хабу (переконайся, що шлях до файлу правильний)
events = load_events("hub_log.txt") 

# Задаємо часовий проміжок згідно із завданням
start_time = "2026-10-13T23:00:00"
end_time = "2026-10-14T04:00:00"

# Фільтруємо події
filtered_events = events_between(events, start_time, end_time)

# Сортуємо за повним часом
filtered_events.sort(key=lambda e: e.ts)

# Формуємо текст хронології
output_lines = []
for e in filtered_events:
    line = f"{e.ts} | {e.kind} | {e.fields}"
    output_lines.append(line)
    print(line)

# Зберігаємо результат у файл chronology.txt
with open("chronology.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(output_lines))

print("\n[OK] Файл chronology.txt успішно створено!")
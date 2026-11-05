with open("hub_log.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

with open("chronology.txt", "w", encoding="utf-8") as f:
    f.writelines(lines)

print(f"ГОТОВО! Успішно записано рядків у chronology.txt: {len(lines)}")
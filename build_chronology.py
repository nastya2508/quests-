from tracking import load_events, events_between

events = load_events("hub_log.txt") 

filtered_events = events_between(events, "2026-10-13T23:00:00", "2026-10-14T04:00:00")

filtered_events.sort(key=lambda e: e.ts)

with open("chronology.txt", "w", encoding="utf-8") as f:
    for e in filtered_events:
        f.write(f"{e.ts} | {e.kind} | {e.fields}\n")

print("УСПІХ! Файл chronology.txt заповнено рядками:", len(filtered_events))
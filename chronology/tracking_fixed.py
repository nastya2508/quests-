class Event:
    def __init__(self, ts, kind, fields):
        self.ts = ts          # Часова мітка (рядок типу "2026-10-14T00:35:12")
        self.kind = kind      # Тип події (ALARM, GATE, ACCESS, SENSOR, CARGO, CALL, SYSTEM)
        self.fields = fields  # Словник з додатковими параметрами (наприклад, зона, картка тощо)

def load_events(filename):
    """Зчитує файл журналу та перетворює кожен рядок на об'єкт Event"""
    events = []
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or "|" not in line:
                continue
            
            parts = line.split("|")
            ts = parts[0]
            kind = parts[1]
            
            fields = {}
            for part in parts[2:]:
                if "=" in part:
                    key, value = part.split("=", 1)
                    fields[key] = value
                else:
                    fields["raw"] = part
                    
            events.append(Event(ts, kind, fields))
    return events

def events_between(events, start_time, end_time):
    """Фільтрує події за заданим часовим проміжком [start_time, end_time]"""
    filtered = []
    for event in events:
        if start_time <= event.ts <= end_time:
            filtered.append(event)
    return filtered
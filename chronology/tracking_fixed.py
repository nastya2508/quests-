from dataclasses import dataclass, field

@dataclass
class Event:
    ts: str
    kind: str
    fields: dict = field(default_factory=dict)


def load_events(file_path):
    events_list = []
    with open(file_path, encoding="utf-8") as file_object:
        for line in file_object:
            line = line.strip()
            if not line:
                continue
            
            timestamp, *rest_of_line = line.split("|")
            
            if len(timestamp) != 19 or "T" not in timestamp or not rest_of_line:
                continue
                
            kind, *key_value_pairs = rest_of_line
            
            try:
                fields_dictionary = dict(pair.split("=", 1) for pair in key_value_pairs)
            except ValueError:
                continue
                
            events_list.append(Event(timestamp, kind, fields_dictionary))
            
    return events_list


def events_between(events_list, start_time, end_time):
    return [event for event in events_list if start_time <= event.ts < end_time]


def gate_openings(events_list, target_gate, start_time, end_time):
    return [
        event for event in events_between(events_list, start_time, end_time)
        if event.kind == "GATE" and event.fields.get("gate") == str(target_gate)
        and event.fields.get("action") == "open"
    ]


def zone_access(events_list, target_zone, start_time, end_time):
    return [
        event for event in events_between(events_list, start_time, end_time)
        if event.kind == "ACCESS" and event.fields.get("zone") == target_zone
    ]


def sensor_alerts(events_list, target_zone, sensor_type, start_time, end_time):
    return [
        event for event in events_between(events_list, start_time, end_time)
        if event.kind == "SENSOR" and event.fields.get("zone") == target_zone
        and event.fields.get("type") == sensor_type
    ]


def batch_movements(events_list, target_batch):
    return [
        event for event in events_list
        if event.kind == "CARGO" and event.fields.get("batch") == target_batch
    ]


def alarm_enabled_at(events_list, target_moment):
    is_enabled = True
    for event in sorted(events_list, key=lambda current_event: current_event.ts):
        if event.ts > target_moment:
            break
        if event.kind == "ALARM" and event.fields.get("zone") == "all":
            is_enabled = event.fields.get("action") != "disable"
    return is_enabled
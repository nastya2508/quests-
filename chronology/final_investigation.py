from tracking_fixed import load_events, events_between

def build_timeline():
    events_list = load_events("hub_log.txt")
    
    start_time = "2026-10-13T23:00:00"
    end_time = "2026-10-14T04:00:00"
    
    night_events = events_between(events_list, start_time, end_time)
    
    timeline_events = []
    
    for event in night_events:
        if event.kind == "ALARM":
            timeline_events.append(event)
        elif event.kind == "GATE" and event.fields.get("gate") == "3":
            timeline_events.append(event)
        elif event.kind == "ACCESS" and event.fields.get("zone") == "C":
            timeline_events.append(event)
        elif event.kind == "SENSOR" and event.fields.get("type") == "smoke":
            timeline_events.append(event)
        elif event.kind == "CARGO":
            timeline_events.append(event)
        elif event.kind == "CALL":
            timeline_events.append(event)
        elif event.kind == "SYSTEM" and event.fields.get("status") == "offline":
            timeline_events.append(event)
            
    sorted_timeline = sorted(timeline_events, key=lambda current_event: current_event.ts)
    
    print("=== ХРОНОЛОГІЯ ПОДІЙ ===")
    for event in sorted_timeline:
        print(f"{event.ts} | {event.kind} | {event.fields}")

if __name__ == "__main__":
    build_timeline()
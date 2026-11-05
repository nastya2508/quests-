"""РњРѕРґСѓР»СЊ С‚СЂРµРєС–РЅРіСѓ С‚СЂР°РЅСЃРїРѕСЂС‚РЅРѕРіРѕ С…Р°Р±Сѓ Р¤Р°СЂРјРё Р†РЅРє.

Р’С–РґРЅРѕРІР»РµРЅРѕ Р· С‡РѕСЂРЅРѕС— СЃРєСЂРёРЅСЊРєРё РїС–СЃР»СЏ РїРѕР¶РµР¶С– 14.10. Р§Р°СЃС‚РёРЅР° РєРѕРґСѓ РјРѕРіР»Р°
РїРѕС€РєРѕРґРёС‚РёСЃСЏ, РіР°СЂР°РЅС‚С–Р№ РЅС–С…С‚Рѕ РЅРµ РґР°С”.

Р¤РѕСЂРјР°С‚ Р¶СѓСЂРЅР°Р»Сѓ: ISO-С‡Р°СЃ|РўРРџ|РєР»СЋС‡=Р·РЅР°С‡РµРЅРЅСЏ|РєР»СЋС‡=Р·РЅР°С‡РµРЅРЅСЏ...
Р§Р°СЃ Р·Р°РІР¶РґРё Сѓ С„РѕСЂРјР°С‚С– YYYY-MM-DDTHH:MM:SS.
"""
from dataclasses import dataclass, field


@dataclass
class Event:
    ts: str                      # '2026-10-14T00:41:30'
    kind: str                    # 'ACCESS', 'GATE', 'CARGO', ...
    fields: dict = field(default_factory=dict)


def load_events(path):
    """Р§РёС‚Р°С” Р¶СѓСЂРЅР°Р» С– РїРѕРІРµСЂС‚Р°С” СЃРїРёСЃРѕРє РїРѕРґС–Р№. Р‘РёС‚С– СЂСЏРґРєРё РїСЂРѕРїСѓСЃРєР°С”."""
    events = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            ts, *rest = line.split("|")
            if len(ts) != 19 or "T" not in ts or not rest:
                continue
            kind, *pairs = rest
            try:
                fields = dict(pair.split("=", 1) for pair in pairs)
            except ValueError:
                continue
            events.append(Event(ts, kind, fields))
    return events


def _clock(ts):
    return ts.split("T")[1]


def events_between(events, start, end):
    """РџРѕРґС–С— РІС–Рґ start (РІРєР»СЋС‡РЅРѕ) РґРѕ end (РЅРµ РІРєР»СЋС‡РЅРѕ).

    start С– end Сѓ С„РѕСЂРјР°С‚С– 'YYYY-MM-DDTHH:MM:SS'.
    """
    return [e for e in events if _clock(start) <= _clock(e.ts) < _clock(end)]


def gate_openings(events, gate, start, end):
    """Р’С–РґРєСЂРёС‚С‚СЏ РІРѕСЂС–С‚ gate Р·Р° РїСЂРѕРјС–Р¶РѕРє С‡Р°СЃСѓ."""
    return [
        e for e in events_between(events, start, end)
        if e.kind == "GATE" and e.fields.get("gate") == str(gate)
        and e.fields.get("action") == "open"
    ]


def zone_access(events, zone, start, end):
    """РџСЂРѕС…РѕРґРё РІ Р·РѕРЅСѓ zone Р·Р° РїСЂРѕРјС–Р¶РѕРє С‡Р°СЃСѓ."""
    return [
        e for e in events_between(events, start, end)
        if e.kind == "ACCESS" and e.fields.get("zone") == zone
    ]


def sensor_alerts(events, zone, sensor_type, start, end):
    """РџРѕРєР°Р·РЅРёРєРё РґР°С‚С‡РёРєР° sensor_type Сѓ Р·РѕРЅС– zone Р·Р° РїСЂРѕРјС–Р¶РѕРє С‡Р°СЃСѓ."""
    return [
        e for e in events_between(events, start, end)
        if e.kind == "SENSOR" and e.fields.get("zone") == zone
        and e.fields.get("type") == sensor_type
    ]


def batch_movements(events, batch):
    """РЈСЃС– РїРµСЂРµРјС–С‰РµРЅРЅСЏ РїР°СЂС‚С–С— batch."""
    return [
        e for e in events
        if e.kind == "CARGO" and e.fields.get("batch") == batch
    ]


def alarm_enabled_at(events, moment):
    """Р§Рё Р±СѓР»Р° СЃРёРіРЅР°Р»С–Р·Р°С†С–СЏ СѓРІС–РјРєРЅРµРЅР° РІ РјРѕРјРµРЅС‚ moment."""
    enabled = True
    for e in sorted(events, key=lambda e: e.ts):
        if e.ts > moment:
            break
        if e.kind == "ALARM" and e.fields.get("zone") == "all":
            enabled = e.fields.get("action") != "disable"
    return enabled
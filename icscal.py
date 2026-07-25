"""
Sample program to read and process events from an .ics calendar file.

Install dependency first:
    pip install icalendar          (on desktop/Termux)
    or use Pydroid's pip manager   (on Pydroid 3)
"""

from icalendar import Calendar
from datetime import datetime, date

ICS_FILE_PATH = "sample_calendar.ics"   # change to your file's path


def load_events(ics_path):
    """Parse an .ics file and return a list of event dicts."""
    with open(ics_path, "rb") as f:
        cal = Calendar.from_ical(f.read())

    events = []
    for component in cal.walk():
        if component.name != "VEVENT":
            continue

        start = component.get("dtstart").dt
        end = component.get("dtend").dt if component.get("dtend") else None

        events.append({
            "summary": str(component.get("summary", "")),
            "description": str(component.get("description", "")),
            "location": str(component.get("location", "")),
            "start": start,
            "end": end,
            "recurring": component.get("rrule") is not None,
        })

    return events


def format_when(dt):
    """Pretty-print a date or datetime value."""
    if isinstance(dt, datetime):
        return dt.strftime("%Y-%m-%d %H:%M %Z").strip()
    if isinstance(dt, date):
        return dt.strftime("%Y-%m-%d (all day)")
    return str(dt)


def format_event_string(e):
    tag = " [recurring]" if e["recurring"] else ""
    lines = [
        f"- {e['summary']}{tag}",
        f"    When:  {format_when(e['start'])}",
    ]
    if e["end"]:
        lines.append(f"    Until: {format_when(e['end'])}")
    if e["location"]:
        lines.append(f"    Where: {e['location']}")
    if e["description"]:
        lines.append(f"    Note:  {e['description']}")
    return "\n".join(lines)


def collect_events_string(events):
    """Collect formatted event strings into a single text block."""
    event_strings = [format_event_string(e) for e in events]
    return "\n\n".join(event_strings)


def icscal_main():
    events = load_events(ICS_FILE_PATH)

    # Sort by start time (all-day dates sort fine alongside datetimes if we
    # normalize; here we just sort using a string key to keep it simple)
    events.sort(key=lambda e: str(e["start"]))

    events_text = collect_events_string(events)
    reminders = [e for e in events if "bill" in e["summary"].lower()]

    if reminders:
        reminder_lines = ["Bill-related reminders:"]
        for e in reminders:
            reminder_lines.append(f"  - {e['summary']} on {format_when(e['start'])}")
        reminder_text = "\n".join(reminder_lines)
        events_text = f"{events_text}\n\n{reminder_text}" if events_text else reminder_text

    return events_text

'''
if __name__ == "__main__":
    events_text = icscal_main()
    print(events_text)
'''
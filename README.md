# BillPayReminder

A simple Python project that reads bill reminders from an `.ics` calendar file and sends them over WhatsApp using Twilio.

## Project Structure

- `main.py` - Entry point. Loads calendar events, formats them, and sends the message.
- `icscal.py` - Reads and formats events from `sample_calendar.ics`.
- `wm.py` - Sends WhatsApp messages through the Twilio API.
- `requirements.txt` - Python dependencies.
- `sample_calendar.ics` - Example calendar file used by the project.
- `config/twilio_config.json` - Twilio credentials and WhatsApp sender number.

## Prerequisites

- Python 3.8+ installed.
- A Twilio account with WhatsApp enabled.
- A WhatsApp-enabled Twilio number or sandbox configured.

## Install Dependencies

1. Create and activate a virtual environment (recommended):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install required packages:

```powershell
pip install -r requirements.txt
```

## Configure Twilio

1. Open `config/twilio_config.json`.
2. Set the following values:

- `TWILIO_ACCOUNT_SID`
- `TWILIO_AUTH_TOKEN`
- `TWILIO_WHATSAPP_NUMBER`

Example:

```json
{
  "TWILIO_ACCOUNT_SID": "ACXXXXX",
  "TWILIO_AUTH_TOKEN": "your_auth_token",
  "TWILIO_WHATSAPP_NUMBER": "whatsapp:+14155238886"
}
```

> Do not commit your Twilio credentials to version control.

## Configure Calendar Input

The calendar file is configured in `icscal.py` with the `ICS_FILE_PATH` constant:

```python
ICS_FILE_PATH = "sample_calendar.ics"
```

Replace this with the path to your own `.ics` file if needed.

## Configure Recipient

In `main.py`, replace the `to_number` value with the recipient WhatsApp number in this format:

```python
whatsapp:+<country_code><phone_number>
```

Example:

```python
to_number = "whatsapp:+919966216488"
```

## Run the Project

```powershell
python main.py
```

The script will:

1. Load events from the configured `.ics` file.
2. Format bill-related reminders.
3. Send the event summary to the configured WhatsApp recipient.

## Notes

- `icscal.py` only processes `VEVENT` entries.
- Messages are sent through Twilio WhatsApp and may require sandbox approval for non-production use.
- If you encounter Twilio errors, verify the WhatsApp channel, phone numbers, and sandbox settings.

## License

This repository does not include a license file. Add one if you want to share or reuse the code publicly.

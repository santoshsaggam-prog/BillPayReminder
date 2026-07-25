import json
from pathlib import Path
from twilio.rest import Client

CONFIG_FILE = Path(__file__).resolve().parent / "config" / "twilio_config.json"


def load_twilio_config():
    try:
        with CONFIG_FILE.open("r", encoding="utf-8") as file:
            config = json.load(file)

        required_keys = [
            "TWILIO_ACCOUNT_SID",
            "TWILIO_AUTH_TOKEN",
            "TWILIO_WHATSAPP_NUMBER",
        ]

        missing = [key for key in required_keys if not config.get(key)]
        if missing:
            raise RuntimeError(
                "Missing Twilio values in twilio_config.json: " + ", ".join(missing)
            )

        return config
    except FileNotFoundError as exc:
        raise RuntimeError(
            f"Configuration file not found: {CONFIG_FILE}. Create twilio_config.json first."
        ) from exc
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Invalid JSON in {CONFIG_FILE}: {exc}") from exc


def send_whatsapp_message(to_number, message_body, config=None):
    try:
        config = config or load_twilio_config()

        account_sid = config["TWILIO_ACCOUNT_SID"]
        auth_token = config["TWILIO_AUTH_TOKEN"]
        from_number = config["TWILIO_WHATSAPP_NUMBER"]

        client = Client(account_sid, auth_token)
        message = client.messages.create(
            body=message_body,
            from_=from_number,
            to=to_number,
        )
        return message.sid
    except Exception as exc:
        if "Channel with the specified From address" in str(exc):
            raise RuntimeError(
                "Twilio could not find a WhatsApp channel for the configured from number. "
                "Verify that TWILIO_WHATSAPP_NUMBER in twilio_config.json matches the "
                "exact number shown in the Twilio WhatsApp console, or join the sandbox "
                "correctly before sending."
            ) from exc
        raise RuntimeError(f"Failed to send WhatsApp message: {exc}") from exc

def send_msg(to_number, message_body):
    try:
        config = load_twilio_config()
        print("Twilio configuration loaded successfully.")
        print(config)
        message_sid = send_whatsapp_message(to_number, message_body, config=config)
        print(f"Message sent successfully. SID: {message_sid}")
        return message_sid
    except RuntimeError as e:
        print(f"Error sending message: {e}")

'''
if __name__ == "__main__":
    
    aashrey="whatsapp:+917901491803"
    santosh="whatsapp:+919966216488"
    bhargav="whatsapp:+918790760202"
    to_number=santosh  # Replace with the recipient's WhatsApp number in the format 'whatsapp:+<country_code><number>'
    print("sending message to ",to_number)

    message_body = "!!! Hello. This is from Santosh Saggam. INR 200/- transferred to your SBI account !!!"

    message_sid = send_msg(to_number, message_body)
    if message_sid:
        print(f"Message sent successfully. SID: {message_sid}")
    else:
        print("Failed to send message.")
'''    
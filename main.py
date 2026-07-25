from icscal import icscal_main as icscal_main
from wm import send_msg


def main():
    try:
        print("Loading events from Calendar...")
        event_txt = icscal_main()
        aashrey = "whatsapp:+91790149180X"
        santosh = "whatsapp:+91996621648X"
        bhargav = "whatsapp:+91879076020X"
        to_number = santosh  # Replace with the recipient's WhatsApp number in the format 'whatsapp:+<country_code><number>'
        print("sending message to ", to_number)
        msg_id = send_msg(to_number, event_txt)
        if msg_id:
            print(f"Message sent successfully. SID: {msg_id}")
        else:
            print("Failed to send message.")
    except FileNotFoundError as e:
        print(f"Calendar file error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()

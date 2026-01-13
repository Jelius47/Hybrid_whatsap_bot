import logging
import json
import requests
import re
from dotenv import load_dotenv
import os
from flask import jsonify

# This is the responsible function from GeminAi to the use
# from app.services.gemin_configuration import generate_response

# The configuration for OpenAi
from app.services.openai_service import generate_response


# Load environment variables
load_dotenv()
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
RECIPIENT_WAID = os.getenv("RECIPIENT_WAID")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
VERSION = os.getenv("VERSION")
APP_ID = os.getenv("APP_ID")
APP_SECRET = os.getenv("APP_SECRET")


# Utility function to log HTTP response details
def log_http_response(response):
    logging.info(f"Status: {response.status_code}")
    logging.info(f"Content-type: {response.headers.get('content-type')}")
    logging.info(f"Body: {response.text}")


# Construct a text message payload for the WhatsApp API
def get_text_message_input(recipient, text):
    return json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": recipient,
            "type": "text",
            "text": {"preview_url": False, "body": text},
        }
    )


# Where integration with WhatsApp API to send the response back
import requests


def send_whatsapp_message(recipient_waid, message, reply_to_message_id=None):
    """
    Send a WhatsApp message with optional reply context.

    Args:
        recipient_waid: Recipient's WhatsApp ID
        message: Message text to send
        reply_to_message_id: Optional message ID to reply to (for quoting messages)
    """
    url = (
        f"https://graph.facebook.com/{VERSION}/{os.getenv('PHONE_NUMBER_ID')}/messages"
    )
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }
    data = {
        "messaging_product": "whatsapp",
        "to": recipient_waid,
        "type": "text",
        "text": {"body": message},
    }

    # Add reply context if message_id is provided (for replying to messages)
    if reply_to_message_id:
        data["context"] = {"message_id": reply_to_message_id}

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        logging.info(f"Message sent to {recipient_waid}")
        return response.json()
    else:
        logging.error(f"Failed to send message to {recipient_waid}: {response.text}")
        return None


def send_reaction(recipient_waid, message_id, emoji):
    """
    Send an emoji reaction to a specific message using WhatsApp Business API.

    Args:
        recipient_waid: Recipient's WhatsApp ID
        message_id: ID of the message to react to
        emoji: Emoji to react with (e.g., "👍", "❤️", "😊", "😂", "😮", "😢", "🙏")
    """
    url = (
        f"https://graph.facebook.com/{VERSION}/{os.getenv('PHONE_NUMBER_ID')}/messages"
    )
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }
    data = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": recipient_waid,
        "type": "reaction",
        "reaction": {
            "message_id": message_id,
            "emoji": emoji
        }
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        logging.info(f"Reaction {emoji} sent to message {message_id}")
        return True
    else:
        logging.error(f"Failed to send reaction: {response.text}")
        return False


def mark_as_read_with_typing(message_id):
    """
    Mark a message as read and show typing indicator using WhatsApp Business API.

    Args:
        message_id: ID of the message to mark as read
    """
    url = (
        f"https://graph.facebook.com/{VERSION}/{os.getenv('PHONE_NUMBER_ID')}/messages"
    )
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }
    data = {
        "messaging_product": "whatsapp",
        "status": "read",
        "message_id": message_id,
        "typing_indicator": {
            "type": "text"
        }
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        logging.info(f"Message {message_id} marked as read with typing indicator")
        return True
    else:
        logging.error(f"Failed to mark message as read with typing: {response.text}")
        return False


# Process text to match WhatsApp message style (e.g., replacing brackets, formatting text)
def process_text_for_whatsapp(text):
    # Remove brackets and their content
    text = re.sub(r"\【.*?\】", "", text).strip()

    # Replace double asterisks with single asterisks (for bold formatting in WhatsApp)
    whatsapp_style_text = re.sub(r"\*\*(.*?)\*\*", r"*\1*", text)

    return whatsapp_style_text


# Handle incoming WhatsApp message and respond
def process_whatsapp_message(body):
    try:
        wa_id = body["entry"][0]["changes"][0]["value"]["contacts"][0]["wa_id"]
        name = body["entry"][0]["changes"][0]["value"]["contacts"][0]["profile"]["name"]
        message = body["entry"][0]["changes"][0]["value"]["messages"][0]
        message_body = message["text"]["body"]
        message_id = message["id"]

        logging.info(f"Received message from {name} ({wa_id}): {message_body}")

        # Mark message as read and show typing indicator (mimic human behavior)
        mark_as_read_with_typing(message_id)

        # Process and respond
        response = generate_response(message_body, wa_id, name)
        formatted_response = process_text_for_whatsapp(response)

        # Send the response as a reply to the original message (mimic human behavior)
        send_whatsapp_message(wa_id, formatted_response, reply_to_message_id=message_id)

        # Optional: Send a reaction emoji to acknowledge the message
        # Uncomment the line below to enable automatic reactions
        # send_reaction(wa_id, message_id, "👍")

    except KeyError as e:
        logging.error(f"KeyError during message processing: {e}")
    except Exception as e:
        logging.error(f"Unexpected error during message processing: {e}")


# Check if the incoming event is a valid WhatsApp message
def is_valid_whatsapp_message(body):
    try:
        return (
            body.get("object") == "whatsapp_business_account"
            and "entry" in body
            and "changes" in body["entry"][0]
            and "value" in body["entry"][0]["changes"][0]
            and "messages" in body["entry"][0]["changes"][0]["value"]
        )
    except KeyError:
        return False


def send_button_message(recipient_waid, body_text, buttons, header_text=None, footer_text=None):
    """
    Send an interactive button message.

    Args:
        recipient_waid: Recipient's WhatsApp ID
        body_text: Main body text of the message
        buttons: List of button dicts with 'id' and 'title' keys (max 3 buttons)
                 Example: [{"id": "btn1", "title": "Option 1"}, {"id": "btn2", "title": "Option 2"}]
        header_text: Optional header text
        footer_text: Optional footer text

    Example:
        buttons = [
            {"id": "yes", "title": "Yes"},
            {"id": "no", "title": "No"}
        ]
        send_button_message(wa_id, "Do you want to continue?", buttons)
    """
    url = f"https://graph.facebook.com/{VERSION}/{os.getenv('PHONE_NUMBER_ID')}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }

    action_buttons = []
    for btn in buttons[:3]:  # Max 3 buttons
        action_buttons.append({
            "type": "reply",
            "reply": {
                "id": btn["id"],
                "title": btn["title"][:20]  # Max 20 chars
            }
        })

    data = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": recipient_waid,
        "type": "interactive",
        "interactive": {
            "type": "button",
            "body": {"text": body_text},
            "action": {"buttons": action_buttons}
        }
    }

    if header_text:
        data["interactive"]["header"] = {"type": "text", "text": header_text}
    if footer_text:
        data["interactive"]["footer"] = {"text": footer_text}

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        logging.info(f"Button message sent to {recipient_waid}")
        return response.json()
    else:
        logging.error(f"Failed to send button message: {response.text}")
        return None


def send_list_message(recipient_waid, body_text, button_text, sections, header_text=None, footer_text=None):
    """
    Send an interactive list message.

    Args:
        recipient_waid: Recipient's WhatsApp ID
        body_text: Main body text
        button_text: Text for the list button (e.g., "View Options")
        sections: List of section dicts with 'title' and 'rows' keys
                  Each row has 'id', 'title', and optional 'description'
        header_text: Optional header text
        footer_text: Optional footer text

    Example:
        sections = [
            {
                "title": "Payment Methods",
                "rows": [
                    {"id": "cash", "title": "Cash", "description": "Pay with cash"},
                    {"id": "card", "title": "Card", "description": "Pay with card"}
                ]
            }
        ]
        send_list_message(wa_id, "Choose payment method", "Select", sections)
    """
    url = f"https://graph.facebook.com/{VERSION}/{os.getenv('PHONE_NUMBER_ID')}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }

    data = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": recipient_waid,
        "type": "interactive",
        "interactive": {
            "type": "list",
            "body": {"text": body_text},
            "action": {
                "button": button_text[:20],  # Max 20 chars
                "sections": sections
            }
        }
    }

    if header_text:
        data["interactive"]["header"] = {"type": "text", "text": header_text}
    if footer_text:
        data["interactive"]["footer"] = {"text": footer_text}

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        logging.info(f"List message sent to {recipient_waid}")
        return response.json()
    else:
        logging.error(f"Failed to send list message: {response.text}")
        return None


def send_contact(recipient_waid, contacts):
    """
    Send contact card(s).

    Args:
        recipient_waid: Recipient's WhatsApp ID
        contacts: List of contact dicts with name and phone information

    Example:
        contacts = [
            {
                "name": {"formatted_name": "John Doe", "first_name": "John", "last_name": "Doe"},
                "phones": [{"phone": "+1234567890", "type": "CELL"}],
                "emails": [{"email": "john@example.com", "type": "WORK"}]
            }
        ]
        send_contact(wa_id, contacts)
    """
    url = f"https://graph.facebook.com/{VERSION}/{os.getenv('PHONE_NUMBER_ID')}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }

    data = {
        "messaging_product": "whatsapp",
        "to": recipient_waid,
        "type": "contacts",
        "contacts": contacts
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        logging.info(f"Contact sent to {recipient_waid}")
        return response.json()
    else:
        logging.error(f"Failed to send contact: {response.text}")
        return None


def send_location(recipient_waid, latitude, longitude, name=None, address=None):
    """
    Send location message.

    Args:
        recipient_waid: Recipient's WhatsApp ID
        latitude: Location latitude
        longitude: Location longitude
        name: Optional location name
        address: Optional location address

    Example:
        send_location(wa_id, -6.7924, 39.2083, "Dar es Salaam", "Tanzania")
    """
    url = f"https://graph.facebook.com/{VERSION}/{os.getenv('PHONE_NUMBER_ID')}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }

    location_data = {
        "latitude": latitude,
        "longitude": longitude
    }

    if name:
        location_data["name"] = name
    if address:
        location_data["address"] = address

    data = {
        "messaging_product": "whatsapp",
        "to": recipient_waid,
        "type": "location",
        "location": location_data
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        logging.info(f"Location sent to {recipient_waid}")
        return response.json()
    else:
        logging.error(f"Failed to send location: {response.text}")
        return None


def send_media(recipient_waid, media_type, media_id=None, media_link=None, caption=None, filename=None):
    """
    Send media message (image, video, document, audio).

    Args:
        recipient_waid: Recipient's WhatsApp ID
        media_type: Type of media - "image", "video", "document", "audio"
        media_id: Media ID from uploaded file (use either media_id or media_link)
        media_link: Direct URL to media file (use either media_id or media_link)
        caption: Optional caption for image/video
        filename: Optional filename for document

    Example:
        # Using media link
        send_media(wa_id, "image", media_link="https://example.com/image.jpg", caption="Check this out!")

        # Using media ID
        send_media(wa_id, "document", media_id="123456", filename="report.pdf")
    """
    url = f"https://graph.facebook.com/{VERSION}/{os.getenv('PHONE_NUMBER_ID')}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }

    media_data = {}
    if media_id:
        media_data["id"] = media_id
    elif media_link:
        media_data["link"] = media_link
    else:
        logging.error("Either media_id or media_link must be provided")
        return None

    if caption and media_type in ["image", "video"]:
        media_data["caption"] = caption

    if filename and media_type == "document":
        media_data["filename"] = filename

    data = {
        "messaging_product": "whatsapp",
        "to": recipient_waid,
        "type": media_type,
        media_type: media_data
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        logging.info(f"{media_type.capitalize()} sent to {recipient_waid}")
        return response.json()
    else:
        logging.error(f"Failed to send {media_type}: {response.text}")
        return None


def send_template(recipient_waid, template_name, language_code="en", components=None):
    """
    Send template message.

    Args:
        recipient_waid: Recipient's WhatsApp ID
        template_name: Name of the approved template
        language_code: Language code (default: "en")
        components: Optional list of component parameters

    Example:
        components = [
            {
                "type": "body",
                "parameters": [
                    {"type": "text", "text": "John"},
                    {"type": "text", "text": "5"}
                ]
            }
        ]
        send_template(wa_id, "hello_world", "en", components)
    """
    url = f"https://graph.facebook.com/{VERSION}/{os.getenv('PHONE_NUMBER_ID')}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }

    data = {
        "messaging_product": "whatsapp",
        "to": recipient_waid,
        "type": "template",
        "template": {
            "name": template_name,
            "language": {"code": language_code}
        }
    }

    if components:
        data["template"]["components"] = components

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        logging.info(f"Template message sent to {recipient_waid}")
        return response.json()
    else:
        logging.error(f"Failed to send template: {response.text}")
        return None


def send_quick_reply_buttons(recipient_waid, body_text, quick_replies):
    """
    Convenience function to send quick reply buttons (simplified button interface).

    Args:
        recipient_waid: Recipient's WhatsApp ID
        body_text: Message text
        quick_replies: List of button titles (will auto-generate IDs)

    Example:
        send_quick_reply_buttons(wa_id, "Choose an option:", ["Yes", "No", "Maybe"])
    """
    buttons = [{"id": f"btn_{i}", "title": title} for i, title in enumerate(quick_replies[:3])]
    return send_button_message(recipient_waid, body_text, buttons)


# # Generate a simple response (you can replace this with your AI assistant or custom logic)
# def generate_response(message):
#     # Here we simply return the message in uppercase as a response
#     return message.upper()

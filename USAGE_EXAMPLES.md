# WhatsApp Bot - Usage Examples

This document provides examples of how to use all the WhatsApp message components in your bot.

## Table of Contents
1. [Basic Text Messages](#basic-text-messages)
2. [Interactive Buttons](#interactive-buttons)
3. [Interactive Lists](#interactive-lists)
4. [Contact Messages](#contact-messages)
5. [Location Messages](#location-messages)
6. [Media Messages](#media-messages)
7. [Template Messages](#template-messages)
8. [Reactions](#reactions)
9. [Reply to Messages](#reply-to-messages)
10. [Read Receipts & Typing](#read-receipts--typing)

---

## Basic Text Messages

```python
from app.utils.whatsapp_utils import send_whatsapp_message

# Simple text message
send_whatsapp_message(wa_id, "Hello, how can I help you?")

# Reply to a message (quote)
send_whatsapp_message(wa_id, "Thanks for your message!", reply_to_message_id="msg_123")
```

---

## Interactive Buttons

Send up to 3 buttons for user interaction:

```python
from app.utils.whatsapp_utils import send_button_message

# Example 1: Yes/No buttons
buttons = [
    {"id": "yes", "title": "Yes"},
    {"id": "no", "title": "No"}
]
send_button_message(wa_id, "Do you want to continue?", buttons)

# Example 2: With header and footer
buttons = [
    {"id": "register", "title": "Register"},
    {"id": "login", "title": "Login"},
    {"id": "help", "title": "Help"}
]
send_button_message(
    wa_id,
    "Welcome to our service!",
    buttons,
    header_text="Gas Station Bot",
    footer_text="Powered by SmartGas"
)

# Example 3: Quick reply buttons (simplified)
from app.utils.whatsapp_utils import send_quick_reply_buttons

send_quick_reply_buttons(wa_id, "Choose an option:", ["Yes", "No", "Maybe"])
```

---

## Interactive Lists

Send a menu with multiple options organized in sections:

```python
from app.utils.whatsapp_utils import send_list_message

# Example 1: Payment methods
sections = [
    {
        "title": "Payment Methods",
        "rows": [
            {"id": "cash", "title": "Cash", "description": "Pay with cash on delivery"},
            {"id": "card", "title": "Card", "description": "Pay with credit/debit card"},
            {"id": "mobile", "title": "Mobile Money", "description": "M-Pesa or Tigo Pesa"}
        ]
    }
]
send_list_message(wa_id, "Choose your payment method", "Select Payment", sections)

# Example 2: Multiple sections
sections = [
    {
        "title": "Fuel Types",
        "rows": [
            {"id": "petrol", "title": "Petrol", "description": "Regular unleaded petrol"},
            {"id": "diesel", "title": "Diesel", "description": "Diesel fuel"}
        ]
    },
    {
        "title": "Services",
        "rows": [
            {"id": "car_wash", "title": "Car Wash", "description": "Professional car washing"},
            {"id": "oil_change", "title": "Oil Change", "description": "Engine oil change service"}
        ]
    }
]
send_list_message(
    wa_id,
    "What would you like today?",
    "View Menu",
    sections,
    header_text="Available Options",
    footer_text="Select from the list"
)
```

---

## Contact Messages

Send contact cards:

```python
from app.utils.whatsapp_utils import send_contact

# Example 1: Single contact
contacts = [
    {
        "name": {
            "formatted_name": "John Doe",
            "first_name": "John",
            "last_name": "Doe"
        },
        "phones": [
            {"phone": "+255123456789", "type": "CELL"}
        ],
        "emails": [
            {"email": "john@example.com", "type": "WORK"}
        ]
    }
]
send_contact(wa_id, contacts)

# Example 2: Multiple contacts
contacts = [
    {
        "name": {"formatted_name": "Support Team"},
        "phones": [{"phone": "+255111222333", "type": "WORK"}]
    },
    {
        "name": {"formatted_name": "Emergency Line"},
        "phones": [{"phone": "+255999888777", "type": "CELL"}]
    }
]
send_contact(wa_id, contacts)
```

---

## Location Messages

Send location pins:

```python
from app.utils.whatsapp_utils import send_location

# Example 1: Basic location
send_location(wa_id, -6.7924, 39.2083)

# Example 2: Location with name and address
send_location(
    wa_id,
    -6.7924,
    39.2083,
    name="Shell Gas Station",
    address="Msasani Road, Dar es Salaam, Tanzania"
)
```

---

## Media Messages

Send images, videos, documents, and audio:

```python
from app.utils.whatsapp_utils import send_media

# Example 1: Send image with caption
send_media(
    wa_id,
    "image",
    media_link="https://example.com/image.jpg",
    caption="Check out our new station!"
)

# Example 2: Send document
send_media(
    wa_id,
    "document",
    media_link="https://example.com/receipt.pdf",
    filename="receipt.pdf"
)

# Example 3: Send video
send_media(
    wa_id,
    "video",
    media_link="https://example.com/video.mp4",
    caption="How to use our app"
)

# Example 4: Send audio
send_media(
    wa_id,
    "audio",
    media_link="https://example.com/audio.mp3"
)

# Example 5: Using media ID (if you've uploaded to WhatsApp)
send_media(
    wa_id,
    "image",
    media_id="123456789",
    caption="Your receipt"
)
```

---

## Template Messages

Send pre-approved template messages:

```python
from app.utils.whatsapp_utils import send_template

# Example 1: Simple template
send_template(wa_id, "hello_world", "en")

# Example 2: Template with parameters
components = [
    {
        "type": "body",
        "parameters": [
            {"type": "text", "text": "John"},
            {"type": "text", "text": "5"}
        ]
    }
]
send_template(wa_id, "booking_confirmation", "en", components)
```

---

## Reactions

Send emoji reactions to messages:

```python
from app.utils.whatsapp_utils import send_reaction

# React to a message
send_reaction(wa_id, message_id, "👍")

# Other reactions
send_reaction(wa_id, message_id, "❤️")
send_reaction(wa_id, message_id, "😊")
send_reaction(wa_id, message_id, "😂")

# Remove reaction (send empty emoji)
send_reaction(wa_id, message_id, "")
```

---

## Reply to Messages

Quote/reply to specific messages:

```python
from app.utils.whatsapp_utils import send_whatsapp_message

# Reply to a message
send_whatsapp_message(
    wa_id,
    "Thanks for your question! Here's the answer...",
    reply_to_message_id="wamid.HBgLMTY1..."
)
```

---

## Read Receipts & Typing

Mark messages as read and show typing indicator:

```python
from app.utils.whatsapp_utils import mark_as_read_with_typing

# Mark as read and show typing indicator
mark_as_read_with_typing(message_id)
```

---

## Complete Example: Gas Station Bot

Here's a complete example showing how to handle user interactions:

```python
from app.utils.whatsapp_utils import (
    send_button_message,
    send_list_message,
    send_location,
    send_contact,
    send_reaction,
    mark_as_read_with_typing,
    send_whatsapp_message
)

def handle_user_message(wa_id, message_text, message_id):
    # Mark as read and show typing
    mark_as_read_with_typing(message_id)

    if message_text.lower() == "start":
        # Send welcome message with buttons
        buttons = [
            {"id": "find_station", "title": "Find Station"},
            {"id": "book_fuel", "title": "Book Fuel"},
            {"id": "help", "title": "Help"}
        ]
        send_button_message(
            wa_id,
            "Welcome to SmartGas! How can I help you today?",
            buttons,
            header_text="Gas Station Assistant"
        )

    elif message_text.lower() == "find station":
        # Send list of nearby stations
        sections = [
            {
                "title": "Nearby Stations",
                "rows": [
                    {"id": "station_1", "title": "Shell Msasani", "description": "2.5 km away - 5 min wait"},
                    {"id": "station_2", "title": "Puma Mikocheni", "description": "3.1 km away - 10 min wait"},
                    {"id": "station_3", "title": "Engen Oysterbay", "description": "4.2 km away - 3 min wait"}
                ]
            }
        ]
        send_list_message(wa_id, "Select a station to view details", "View Stations", sections)

    elif message_text.lower() == "station_1":
        # Send station details
        send_whatsapp_message(wa_id, "Shell Msasani Station\n\nFuel: Available\nWait Time: 5 minutes\n\nSending location...")
        send_location(wa_id, -6.7924, 39.2083, "Shell Msasani", "Msasani Road, Dar es Salaam")

        # Send contact
        contacts = [{
            "name": {"formatted_name": "Shell Msasani"},
            "phones": [{"phone": "+255123456789", "type": "WORK"}]
        }]
        send_contact(wa_id, contacts)

    elif "thank" in message_text.lower():
        # React with heart
        send_reaction(wa_id, message_id, "❤️")
        send_whatsapp_message(wa_id, "You're welcome! Feel free to ask if you need anything else.", reply_to_message_id=message_id)
```

---

## Handling Button/List Responses

When users click buttons or select from lists, WhatsApp sends the response in a specific format:

```python
def process_whatsapp_message(body):
    try:
        message = body["entry"][0]["changes"][0]["value"]["messages"][0]
        wa_id = body["entry"][0]["changes"][0]["value"]["contacts"][0]["wa_id"]
        message_id = message["id"]

        # Handle button response
        if message["type"] == "interactive":
            interactive = message["interactive"]

            if interactive["type"] == "button_reply":
                button_id = interactive["button_reply"]["id"]
                button_title = interactive["button_reply"]["title"]

                # Handle based on button ID
                if button_id == "yes":
                    send_whatsapp_message(wa_id, "Great! Let's proceed...")
                elif button_id == "no":
                    send_whatsapp_message(wa_id, "No problem. Let me know if you need help.")

            elif interactive["type"] == "list_reply":
                list_id = interactive["list_reply"]["id"]
                list_title = interactive["list_reply"]["title"]

                # Handle based on list selection
                if list_id == "cash":
                    send_whatsapp_message(wa_id, "You selected Cash payment.")
                elif list_id == "card":
                    send_whatsapp_message(wa_id, "You selected Card payment.")

        # Handle text message
        elif message["type"] == "text":
            message_body = message["text"]["body"]
            # Process text message...

    except Exception as e:
        logging.error(f"Error processing message: {e}")
```

---

## Tips for Developers

1. **Message Limits**: Buttons are limited to 3, button titles to 20 characters
2. **Lists**: Can have multiple sections with up to 10 rows per section
3. **Media**: Use either `media_id` OR `media_link`, not both
4. **Templates**: Must be pre-approved by WhatsApp before use
5. **Reactions**: Can be removed by sending an empty string emoji
6. **Read Receipts**: Automatically shows typing indicator when marking as read
7. **Error Handling**: All functions return `None` on failure, check return values

---

## Need Help?

Check the [WhatsApp Business API Documentation](https://developers.facebook.com/docs/whatsapp) for more details.

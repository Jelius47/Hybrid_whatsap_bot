# # import os
# # import logging
# # import shelve
# # import time
# # from dotenv import load_dotenv
# # import google.generativeai as genai

# # # Load environment variables from .env file
# # load_dotenv()

# # # Configure Gemini API using the API key
# # genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# # # Define constants
# # MODEL_NAME = "gemini-1.5-flash"  # Adjust the model name as per Gemini's current offerings
# # SHELVE_FILE = "threads_db"  # File for storing conversation threads
# # SYSTEM_INSTRUCTION = os.getenv("SYSTEM_INSTRUCTION",
# #                                "Respond to customer queries in a helpful and friendly manner.")  # Default system instruction if not provided

# # # Initialize the model with system instructions
# # model = genai.GenerativeModel(
# #     model_name=MODEL_NAME,
# #     system_instruction=SYSTEM_INSTRUCTION
# # )

# # # Check if a thread exists for the given WhatsApp ID (wa_id)
# # def check_if_thread_exists(wa_id):
# #     with shelve.open(SHELVE_FILE) as threads_shelf:
# #         return threads_shelf.get(wa_id, None)

# # # Store a new thread in the shelve DB
# # def store_thread(wa_id, thread_id):
# #     with shelve.open(SHELVE_FILE, writeback=True) as threads_shelf:
# #         threads_shelf[wa_id] = thread_id

# # # Run the assistant to generate a response
# # def run_assistant(thread_id, name, message):
# #     try:
# #         logging.info(f"Running assistant for thread: {thread_id}")

# #         # Start or continue the conversation
# #         chat = model.start_chat(
# #             history=[
# #                 {"role": "user", "parts": f"Naitwa {name} nahitaji {SYSTEM_INSTRUCTION}"},
# #                 {"role": "model", "parts": message},  # Use the user's message here
# #             ]
# #         )

# #         # Send the message and get the response
# #         response = chat.send_message(message)

# #         if response and response.text:
# #             new_message = response.text  # Fetch the generated content
# #             logging.info(f"Generated message: {new_message}")
# #             return new_message
# #         else:
# #             logging.error("No response generated.")
# #             return "Samahani, kuna tatizo. Tafadhali jaribu tena baadaye."

# #     except Exception as e:
# #         logging.error(f"Error running assistant: {str(e)}")
# #         return "Samahani, kuna tatizo. Tafadhali jaribu tena baadaye."

# # # Generate a response based on the user's input
# # def generate_response(message_body, wa_id, name):
# #     # Check if a conversation thread already exists for this WhatsApp user
# #     thread_id = check_if_thread_exists(wa_id)

# #     # If the thread doesn't exist, create one and store it
# #     if thread_id is None:
# #         logging.info(f"Creating a new thread for {name} with wa_id {wa_id}")
# #         thread_id = f"thread_{wa_id}_{int(time.time())}"  # Create a unique thread ID
# #         store_thread(wa_id, thread_id)
# #     else:
# #         # Retrieve the existing thread for this user
# #         logging.info(f"Retrieving existing thread for {name} with wa_id {wa_id}")

# #     # Add the user's message to the conversation thread (in-memory for now)
# #     logging.info(f"Processing message from {name}: {message_body}")

# #     # Run the assistant and get the response
# #     new_message = run_assistant(thread_id, name, message_body)

# #     return new_message
# import os
# import logging
# import shelve
# import time
# from dotenv import load_dotenv
# import google.generativeai as genai

# # Load environment variables from .env file
# load_dotenv()

# # Configure Gemini API using the API key
# genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# # Define constants
# MODEL_NAME = "gemini-1.5-flash"
# SHELVE_FILE = "threads_db"  # File for storing conversation threads
# SYSTEM_INSTRUCTION_FILE_PATH = "app/Bot_Data/music_info.txt"

# # Read system instruction from a file (use text content instead of file object)
# with open(SYSTEM_INSTRUCTION_FILE_PATH, "r") as f:
#     SYSTEM_INSTRUCTION = f.read()

# # Define functions for the ticket event process (these will be used as tools)

# def check_ticket_availability(event_id: int) -> dict:
#     """Check ticket availability for a specific event."""
#     print(f"Checking ticket availability for event {event_id}.")
#     return {
#         "VIP": {"price": 200, "available": True},
#         "Regular": {"price": 100, "available": True},
#         "Economy": {"price": 50, "available": False}
#     }

# def select_ticket_type(ticket_type: str) -> bool:
#     """Choose the desired ticket type."""
#     available_types = ["VIP", "Regular", "Economy"]
#     if ticket_type in available_types:
#         print(f"Selected ticket type: {ticket_type}")
#         return True
#     else:
#         print(f"Invalid ticket type: {ticket_type}")
#         return False

# def process_payment(ticket_type: str, amount: float) -> bool:
#     """Process the payment for the selected ticket type."""
#     print(f"Processing payment for {ticket_type} ticket: ${amount}.")
#     return True  # Assuming payment is always successful

# def confirm_ticket_purchase(user_id: int, ticket_type: str) -> str:
#     """Confirm the ticket purchase and generate a ticket ID."""
#     ticket_id = f"TICKET-{user_id}-{ticket_type}-1234"
#     print(f"Ticket confirmed for {ticket_type}. Ticket ID: {ticket_id}")
#     return ticket_id

# def provide_event_details(event_id: int) -> str:
#     """Provide event details such as time, date, and location."""
#     print(f"Providing details for event {event_id}.")
#     return "The event will be held on 25th December at the National Stadium, starting at 6 PM."

# # Set the tools (functions) to be used by the model
# tools = [check_ticket_availability, select_ticket_type, process_payment, confirm_ticket_purchase, provide_event_details]

# # Initialize the model with system instructions and tools
# model = genai.GenerativeModel(model_name=MODEL_NAME, tools=tools, system_instruction=SYSTEM_INSTRUCTION)

# # Check if a thread exists for the given WhatsApp ID (wa_id)
# def check_if_thread_exists(wa_id):
#     with shelve.open(SHELVE_FILE) as threads_shelf:
#         return threads_shelf.get(wa_id, None)

# # Store a new thread in the shelve DB
# def store_thread(wa_id, thread_id):
#     with shelve.open(SHELVE_FILE, writeback=True) as threads_shelf:
#         threads_shelf[wa_id] = thread_id

# # Run the assistant and implement function calling
# def run_assistant(thread_id, name, message):
#     try:
#         logging.info(f"Running assistant for thread: {thread_id}")

#         # Start or continue the conversation
#         chat = model.start_chat(
#             history=[
#                 {"role": "user", "parts": f"Naitwa {name}, nahitaji msaada wa tiketi."},  # Set up the context
#                 {"role": "model", "parts": message},  # Use the user's message here
#             ]
#         )

#         # Send the message and get the response
#         response = chat.send_message(message)

#         # If the response includes function calls, handle them
#         for part in response.parts:
#             if fn := part.function_call:
#                 args = fn.args  # Get function arguments

#                 # Handle specific function calls
#                 if fn.name == "check_ticket_availability":
#                     event_id = args.get("event_id", 1)  # Default to event_id=1
#                     tickets = check_ticket_availability(event_id)
#                     return f"Available tickets: {tickets}"

#                 elif fn.name == "select_ticket_type":
#                     ticket_type = args.get("ticket_type", "VIP")  # Default to VIP
#                     success = select_ticket_type(ticket_type)
#                     return f"You selected {ticket_type}" if success else "Invalid ticket type."

#                 elif fn.name == "process_payment":
#                     ticket_type = args.get("ticket_type", "VIP")  # Default to VIP
#                     amount = args.get("amount", 200)  # Default to $200
#                     success = process_payment(ticket_type, amount)
#                     return "Payment successful!" if success else "Payment failed."

#                 elif fn.name == "confirm_ticket_purchase":
#                     user_id = args.get("user_id", 123)  # Default user_id
#                     ticket_type = args.get("ticket_type", "VIP")  # Default to VIP
#                     ticket_id = confirm_ticket_purchase(user_id, ticket_type)
#                     return f"Your ticket has been confirmed. Ticket ID: {ticket_id}"

#                 elif fn.name == "provide_event_details":
#                     event_id = args.get("event_id", 1)  # Default to event_id=1
#                     details = provide_event_details(event_id)
#                     return details

#         # Handle fallback response when no function calls are made
#         if response and response.text:
#             new_message = response.text  # Fetch the generated content
#             logging.info(f"Generated message: {new_message}")
#             return new_message
#         else:
#             logging.error("No response generated.")
#             return "Samahani, kuna tatizo. Tafadhali jaribu tena baadaye."

#     except Exception as e:
#         logging.error(f"Error running assistant: {str(e)}")
#         return "Samahani, kuna tatizo. Tafadhali jaribu tena baadaye."

# # Generate a response based on the user's input
# def generate_response(message_body, wa_id, name):
#     # Check if a conversation thread already exists for this WhatsApp user
#     thread_id = check_if_thread_exists(wa_id)

#     # If the thread doesn't exist, create one and store it
#     if thread_id is None:
#         logging.info(f"Creating a new thread for {name} with wa_id {wa_id}")
#         thread_id = f"thread_{wa_id}_{int(time.time())}"  # Create a unique thread ID
#         store_thread(wa_id, thread_id)
#     else:
#         # Retrieve the existing thread for this user
#         logging.info(f"Retrieving existing thread for {name} with wa_id {wa_id}")

#     # Add the user's message to the conversation thread (in-memory for now)
#     logging.info(f"Processing message from {name}: {message_body}")

#     # Run the assistant and get the response
#     new_message = run_assistant(thread_id, name, message_body)

#     return new_message

# # Example usage
# # wa_id = "255123456789"
# # name = "John"
# # message_body = "Can you check the availability of VIP tickets?"
# # response_message = generate_response(message_body, wa_id, name)
# # print(response_message)



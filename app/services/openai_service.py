


import os
import logging
import shelve
import time
from dotenv import load_dotenv
import openai
import json
from .function_descriptions import ona_functions # Importing the JSON-like function definitions

# Load environment variables from .env file
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_ASSISTANT_ID = os.getenv("OPENAI_ASSISTANT_ID")
client = openai.OpenAI(api_key=OPENAI_API_KEY)

# Constants
SHELVE_FILE = "threads_db"
SYSTEM_PROMPT_= """
You are a helpful assistant called Amani Mashsauri managing an event ticketing system the event name is CHEKA TU. Ensure responses are friendly, clear, and easy for users to understand.
When calling functions, please use the information provided to generate human-readable responses for each function result.
be playful learn to be funny and be creative maching the mood of the customer whhile maintaining customer language and emoji
"""
SYSTEM_PROMPT = """
You are Ona, an AI-powered storytelling assistant. Your role is to guide users through interactive stories, answer questions about characters, and suggest stories based on their interests.
Be engaging, friendly, and create a sense of wonder. If a user wants to start a new story or learn something, use your functions to provide the best experience.
You should know when to end coversation with the user in a kindly manner.
"""

# Define the functions for Ona Stories assistant
def what_is_ona_stories() -> str:
    return (
        "Ona Stories is a storytelling platform focused on creating immersive, engaging, and impactful stories "
        "that connect people and foster understanding. We specialize in interactive stories that highlight cultural, "
        "social, and personal narratives in a unique and memorable way."
    )

def provide_contact_and_location() -> dict:
    return {
        "phone": "+1234567890",
        "email": "contact@onastories.com",
        "location": "123 Storyteller Lane, Fiction City, FC 45678"
    }

def provide_sample_works() -> list:
    return [
        {"title": "Utanzania ni nini", "description": "An insightful exploration into Tanzanian identity and culture."},
        {"title": "The Story of Dala Dala Documentation", "description": "A documentary uncovering the history and culture of Tanzania's iconic Dala Dala transportation."},
        {"title": "Singeli Music Documentary", "description": "A vibrant exploration of Singeli music and its impact on Tanzanian youth culture."},
        {"title": "More Works", "description": "For additional projects, please visit our website at www.onastories.com."}
    ]


# Thread management functions
def check_if_thread_exists(wa_id):
    with shelve.open(SHELVE_FILE) as threads_shelf:
        return threads_shelf.get(wa_id, None)

def store_thread(wa_id, thread_id):
    with shelve.open(SHELVE_FILE, writeback=True) as threads_shelf:
        threads_shelf[wa_id] = thread_id


def handle_request(request_data):

    # Assuming request_data is a JSON string containing a dictionary
    data = json.loads(request_data)  # Deserialize JSON to a Python dictionary
    
    # Extracting list and dictionary parameters
    project_list = data.get("projects", [])  # Default to empty list if not found
    contact_info = data.get("contact", {})  # Default to empty dict if not found
    if project_list:
        return project_list
    else:
        return contact_info


# Main assistant function to handle user input and function calling
def run_assistant(thread_id, name, message):
    try:
        logging.info(f"Running assistant for thread: {thread_id}")
        
        # Initialize conversation history with system instructions
        conversation_history = [
            {'role': 'system', 'content': f"You are having a conversation with the client named {name}. Instructions: {SYSTEM_PROMPT}"},
            {'role': 'user', 'content': message}
        ]

        # Continuously handle responses until no function call is pending
        while True:
            # Send the message and get the response
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=conversation_history,
                functions=ona_functions,
                function_call="auto"
            )

            # Check if choices and message content exist
            if not response.choices or not response.choices[0].message:
                logging.error("No response choices or message content from assistant.")
                return "Samahani, kuna tatizo. Tafadhali jaribu tena baadaye."

            # Retrieve the message from the response
            response_message = response.choices[0].message

            # Process function call if available
            if hasattr(response_message, "function_call") and response_message.function_call:
                function_called = response_message.function_call.name
                function_args = json.loads(response_message.function_call.arguments)

                # Map function names to actual implementations
                available_functions = {
                    "what_is_ona_stories": what_is_ona_stories,
                    "provide_contact_and_location": provide_contact_and_location,
                    "provide_sample_works": provide_sample_works
                }

                # Call the function and store result if function exists
                if function_called in available_functions:
                    function_to_call = available_functions[function_called]

                    # Call the function and store the result if it exists
                    function_result = function_to_call(**function_args)
                    logging.info(f"Function {function_called} executed with result: {function_result}")

                    # Ensure the result is a string before appending to the conversation history
                    if isinstance(function_result, list):
                        function_result_str = "\n".join([f"{item['title']}: {item['description']}" for item in function_result])
                    else:
                        function_result_str = str(function_result)

                    # Append function result as assistant's response in conversation history
                    conversation_history.append({"role": "assistant", "content": function_result_str})
                else:
                    logging.error(f"Function {function_called} not found.")
                    return "Samahani, kuna tatizo. Tafadhali jaribu tena baadaye."

            else:
                # If no function call is detected, break with final response content
                return response_message.content

    except Exception as e:
        logging.error(f"Error running assistant: {str(e)}")
        return "Samahani, kuna tatizo. Tafadhali jaribu tena baadaye."


# Generate a response for the user's input
def generate_response(message_body, wa_id, name):
    # Check for an existing thread or create a new one
    thread_id = check_if_thread_exists(wa_id)
    if thread_id is None:
        logging.info(f"Creating a new thread for {name} with wa_id {wa_id}")
        thread = client.Chat.create()
        store_thread(wa_id, thread["id"])
        thread_id = thread["id"]
    else:
        logging.info(f"Retrieving existing thread for {name} with wa_id {wa_id}")

    # Process the message and get the assistant's response
    new_message = run_assistant(thread_id, name, message_body)
    
    return new_message

# Example usage
# wa_id = "255123456789"
# name = "John"
# message_body = "Can you check the availability of VIP tickets?"
# response_message = generate_response(message_body, wa_id, name)
# print(response_message)


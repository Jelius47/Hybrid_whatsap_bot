import logging
import shelve
import os
import json
import time
from dotenv import load_dotenv
import openai
from .functions import *  # Import function implementations
from .function_descriptions import eastc_functions

# Configure logging
logging.basicConfig(level=logging.INFO)

# Load environment variables and set up OpenAI client
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    logging.error("Missing OpenAI API Key.")
    raise ValueError("Set OPENAI_API_KEY in environment variables.")
client = openai.OpenAI(api_key=OPENAI_API_KEY)


# # Constants
THREAD_DB_FILE = "threads_db"
VECTOR_STORE_META_FILE = "vector_store_meta.json"
SYSTEM_PROMPT = """Project Overview: Gas Station Assistance Bot for Dar es Salaam
This project focuses on creating a bot to assist automobile owners around Dar es Salaam in efficiently accessing and redistributing traffic across the limited number of gas stations in the city. By addressing congestion at the filling stations, the bot will improve customer experience and optimize service delivery for station operators.

Key Features of the Bot
The bot will handle:

Payment Assistance (Not covered here).
Order Confirmation (Not covered here).
Registration (Not covered here).
Request for Filling Station (Not covered here).
Apart from these, the bot will also need to handle normal user queries related to the gas station services. Below is a detailed breakdown of additional system data and functionalities the bot can provide.

System Data for Handling User Queries
1. Real-Time Fuel Availability
Data Required:
Current fuel types available (e.g., petrol, diesel, LPG).
Quantity available at each station.
Purpose: Helps users decide the station to visit based on fuel availability.
Example Query: "Is LPG available at Station X?"
2. Station Location Information
Data Required:
Geographical coordinates of each gas station.
Nearest landmarks for easy identification.
Purpose: Provides directions or the nearest station to a user.
Example Query: "Where is the closest gas station to Mikocheni?"
3. Real-Time Traffic and Queue Status
Data Required:
Number of vehicles currently waiting at each station.
Estimated waiting time based on queue length and service speed.
Purpose: Helps users avoid congested stations and choose less busy alternatives.
Example Query: "How long is the wait time at Station A?"
4. Operating Hours
Data Required:
Opening and closing hours of each gas station.
Any scheduled maintenance or closures.
Purpose: Ensures users know when a station is operational.
Example Query: "What time does Station B open?"
5. Services Offered
Data Required:
Additional services available (e.g., car wash, tire checks, oil changes).
Purpose: Helps users select a station that offers the services they need.
Example Query: "Does Station C provide oil change services?"
6. Promotions and Discounts
Data Required:
Current discounts or loyalty programs at each station.
Purpose: Informs users about cost-saving opportunities.
Example Query: "Are there any discounts on diesel today?"
7. Emergency Services
Data Required:
Emergency contacts for gas station issues.
Nearby mechanics or towing services for users in need of assistance.
Purpose: Provides critical support to users in distress.
Example Query: "Who can I call if my car breaks down?"
8. User Feedback and Complaints
Data Required:
System to log user feedback about services.
Mechanism for resolving complaints (e.g., response timeline, escalation contacts).
Purpose: Improves service quality and builds user trust.
Example Query: "How do I report an issue with the service at Station D?"
9. Fuel Price Updates
Data Required:
Current prices for all fuel types.
Historical price trends for user reference.
Purpose: Keeps users informed about costs.
Example Query: "What’s the price of petrol today at Station A?"
10. Environmental and Safety Information
Data Required:
Tips for safe fueling.
Environmental policies or updates (e.g., eco-friendly initiatives by stations).
Purpose: Educates users on safety and sustainability practices.
Example Query: "How can I safely refuel my car?"
."""
VECTOR_STORE_NAME = "smartGas_vector_store"
FILE_PATHS = ["../Hybrid_whatsap_bot/app/Bot_Data/LPG.txt"]


# Constants
VECTOR_STORE_META_FILE = "vector_store_metadata.json"


def load_metadata(file_path):
    """Load metadata from a JSON file."""
    if not os.path.exists(file_path):
        return None
    with open(file_path, "r") as f:
        return json.load(f)


def save_metadata(file_path, data):
    """Save metadata to a JSON file."""
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)


def upload_file_with_vector_store(file_paths, vector_store_name="DefaultVectorStore"):
    """
    Upload files to OpenAI and associate them with a vector store, checking for existing metadata.

    Args:
        file_paths (list of str): Paths of files to upload.
        vector_store_name (str): The name of the vector store.

    Returns:
        dict: Metadata about the vector store and uploaded files.
    """
    try:
        # Load existing metadata
        metadata = load_metadata(VECTOR_STORE_META_FILE)
        if metadata:
            logging.info(f"Loaded existing metadata: {metadata}")

            # Check if the vector store and files match
            if metadata.get("vector_store_name") == vector_store_name and set(
                metadata.get("uploaded_files", [])
            ) == set(file_paths):
                logging.info(
                    f"Vector store '{vector_store_name}' and files already uploaded."
                )
                return metadata

        # No matching metadata; proceed with upload
        logging.info(f"Creating vector store: {vector_store_name}")
        vector_store = client.beta.vector_stores.create(name=vector_store_name)
        logging.info(f"Vector store created with ID: {vector_store.id}")

        # Prepare file streams
        file_streams = [open(path, "rb") for path in file_paths]
        logging.info(f"Uploading files to vector store '{vector_store_name}'...")

        # Upload files and associate them with the vector store
        file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
            vector_store_id=vector_store.id, files=file_streams
        )

        # Safely extract file counts if available
        file_counts = {}
        if hasattr(file_batch, "file_counts"):
            file_counts = {
                "processed_files": getattr(file_batch.file_counts, "processed", None),
                "failed_files": getattr(file_batch.file_counts, "failed", None),
                "pending_files": getattr(file_batch.file_counts, "pending", None),
            }

        # Close file streams
        for stream in file_streams:
            stream.close()

        # Prepare and save metadata
        metadata = {
            "vector_store_name": vector_store_name,
            "vector_store_id": vector_store.id,
            "file_batch_status": file_batch.status,
            "file_counts": file_counts,
            "uploaded_files": file_paths,
        }
        save_metadata(VECTOR_STORE_META_FILE, metadata)

        # Log the result
        logging.info(f"File batch upload completed with status: {file_batch.status}")
        logging.info(f"File counts: {file_counts}")

        return metadata

    except Exception as e:
        logging.error(f"Error uploading files to vector store: {e}")
        raise RuntimeError("Failed to upload files to vector store.")


# Metadata File for Assistants
ASSISTANT_META_FILE = "assistants_meta.json"


def load_assistant_metadata():
    """Load assistant metadata from a local file."""
    if os.path.exists(ASSISTANT_META_FILE):
        with open(ASSISTANT_META_FILE, "r") as f:
            return json.load(f)
    return {}


def save_assistant_metadata(data):
    """Save assistant metadata to a local file."""
    with open(ASSISTANT_META_FILE, "w") as f:
        json.dump(data, f)


import time


#  Main assistant function to handle user input and function calling
def run_assistant(thread_id, name, message_body):
    try:
        logging.info(f"Running assistant for thread: {thread_id}")

        # Initialize conversation history with system instructions
        conversation_history = [
            {
                "role": "system",
                "content": f"You are having a conversation with the client named {name}. Instructions: {SYSTEM_PROMPT}",
            },
            {"role": "user", "content": message_body},
        ]

        # Continuously handle responses until no function call is pending
        while True:
            # Send the message and get the response
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=conversation_history,
                functions=eastc_functions,
                function_call="auto",
            )

            # Check if choices and message content exist
            if not response.choices or not response.choices[0].message:
                logging.error("No response choices or message content from assistant.")
                return "Samahani, kuna tatizo. Tafadhali jaribu tena baadaye."

            # Retrieve the message from the response
            response_message = response.choices[0].message

            # Process function call if available
            if (
                hasattr(response_message, "function_call")
                and response_message.function_call
            ):
                function_called = response_message.function_call.name
                function_args = json.loads(response_message.function_call.arguments)

                # Map function names to actual implementations
                available_functions = {
                    "register_user": register_user,
                    "payment_options": payment_options,
                    "request_filling_station": request_filling_station,
                    "confirm_booking": confirm_booking,
                }

                # Call the function and store result if function exists
                if function_called in available_functions:
                    function_to_call = available_functions[function_called]

                    # Call the function and store the result if it exists
                    function_result = function_to_call(**function_args)
                    logging.info(
                        f"Function {function_called} executed with result: {function_result}"
                    )

                    # Ensure the result is a string before appending to the conversation history
                    if isinstance(function_result, list):
                        function_result_str = "\n".join(
                            [
                                f"{item['title']}: {item['description']}"
                                for item in function_result
                            ]
                        )
                    else:
                        function_result_str = str(function_result)

                    # Append function result as assistant's response in conversation history
                    conversation_history.append(
                        {"role": "assistant", "content": function_result_str}
                    )
                else:
                    logging.error(f"Function {function_called} not found.")
                    return "Samahani, kuna tatizo. Tafadhali jaribu tena baadaye."

            else:
                # If no function call is detected, break with final response content
                return response_message.content

    except Exception as e:
        logging.error(f"Error running assistant: {str(e)}")
        return "Samahani, kuna tatizo. Tafadhali jaribu tena baadaye."


"""
Dealing with the retrieval assistant
"""


def get_or_create_retrieval_assistant(vector_store_id):
    """Retrieve or create a retrieval assistant."""
    metadata = load_assistant_metadata()
    if "retrieval_assistant_id" in metadata:
        logging.info(
            f"Using existing Retrieval Assistant ID: {metadata['retrieval_assistant_id']}"
        )
        return metadata["retrieval_assistant_id"]

    try:
        # Create the retrieval assistant
        assistant = client.beta.assistants.create(
            name="RetrievalAssistant",
            instructions=SYSTEM_PROMPT,
            model="gpt-3.5-turbo",
            tools=[{"type": "file_search"}],
        )
        updated_assistant = client.beta.assistants.update(
            assistant_id=assistant.id,
            tool_resources={"file_search": {"vector_store_ids": [vector_store_id]}},
        )
        logging.info(
            f"Retrieval assistant created successfully with ID: {updated_assistant.id}"
        )

        # Save the assistant ID
        metadata["retrieval_assistant_id"] = updated_assistant.id
        save_assistant_metadata(metadata)
        return updated_assistant.id

    except Exception as e:
        logging.error(f"Failed to create retrieval assistant: {e}")
        raise RuntimeError("Failed to create the retrieval assistant.")


# Initialize Assistants
def initialize_assistants():
    """Initialize vector store and assistants."""
    # Check if metadata for vector store exists and matches files
    metadata = upload_file_with_vector_store(FILE_PATHS, VECTOR_STORE_NAME)
    vector_store_id = metadata["vector_store_id"]

    # Retrieve or create the retrieval assistant
    retrieval_assistant_id = get_or_create_retrieval_assistant(vector_store_id)

    logging.info(f"Retrieval Assistant ID: {retrieval_assistant_id}")
    return retrieval_assistant_id


# Initialize assistants
retrieval_assistant_id = initialize_assistants()

# Define routing keywords and determine assistant type
function_call_keywords = {"payment", "contact", "info"}


def determine_assistant(message_body):
    """Determines the appropriate assistant based on message content."""
    if any(keyword in message_body.lower() for keyword in function_call_keywords):
        return "function"
    return "retrieval"


# Thread management for user interactions
def get_or_create_thread(wa_id):
    with shelve.open(THREAD_DB_FILE, writeback=True) as threads_shelf:
        thread_id = threads_shelf.get(wa_id)
        if not thread_id:
            try:
                thread = client.beta.threads.create()
                threads_shelf[wa_id] = thread.id
                logging.info(
                    f"New thread created for wa_id '{wa_id}' with thread ID: {thread.id}"
                )
                return thread.id
            except Exception as e:
                logging.error(f"Error creating new thread: {e}")
                raise RuntimeError("Failed to create thread.")
        return thread_id


def run_retrieval_assistant(thread_id, name, message_body, assistant_id):
    """Run retrieval assistant and get a response."""
    try:
        # Add the user message to the thread
        user_message = client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=f"{message_body},my name is {name}",
        )

        # Run the assistant
        run = client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id="asst_Mvq8PfboUCg0clWKdGq8L1XT",
        )

        # Wait for the run to complete
        while run.status != "completed":
            time.sleep(0.5)
            run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
        # Get the assistant's response
        messages = client.beta.threads.messages.list(thread_id=thread_id)
        for msg in messages.data:
            if msg.role == "assistant" and msg.content:
                # Check if content is in a complex structure and extract text
                if isinstance(msg.content, list):
                    for content_block in msg.content:
                        if hasattr(content_block, "text") and hasattr(
                            content_block.text, "value"
                        ):
                            logging.info(
                                f"Assistant responded with: {content_block.text.value}"
                            )
                            return content_block.text.value
                elif isinstance(msg.content, str):
                    logging.info(f"Assistant responded with: {msg.content}")
                    return msg.content

        return "Sorry, no valid response received from the assistant."

    except Exception as e:
        logging.error(f"Error running retrieval assistant: {e}")
        return "Sorry, an error occurred. Please try again later."


def get_or_create_thread(wa_id):
    """Retrieve or create a thread for the user."""
    with shelve.open(THREAD_DB_FILE, writeback=True) as threads_shelf:
        thread_id = threads_shelf.get(wa_id)
        if thread_id:
            logging.info(f"Found existing thread ID for wa_id '{wa_id}': {thread_id}")
            return thread_id

        try:
            thread = client.beta.threads.create()
            threads_shelf[wa_id] = thread.id
            logging.info(
                f"New thread created for wa_id '{wa_id}' with thread ID: {thread.id}"
            )
            return thread.id
        except Exception as e:
            logging.error(f"Error creating new thread: {e}")
            raise RuntimeError("Failed to create thread.")


# Generate response
def generate_response(message_body, wa_id, name):
    """Route the message to the appropriate assistant."""
    thread_id = get_or_create_thread(wa_id)

    # Determine assistant type based on the message content
    assistant_type = determine_assistant(message_body)
    if assistant_type == "function":
        logging.info("Routing to function assistant.")
        return run_assistant(thread_id, name, message_body)
    else:
        logging.info("Routing to retrieval assistant.")
        return run_retrieval_assistant(
            thread_id, name, message_body, retrieval_assistant_id
        )


# import logging
# import shelve
# import os
# import json
# import time
# from dotenv import load_dotenv
# import openai
# import re

# # from openai.error import OpenAIError  # Correctly import OpenAIError
# from .functions import *  # Import function implementations
# from .function_descriptions import eastc_functions

# # Configure logging
# logging.basicConfig(level=logging.INFO)

# # Load environment variables
# load_dotenv()
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# if not OPENAI_API_KEY:
#     logging.error("Missing OpenAI API Key.")
#     raise ValueError("Set OPENAI_API_KEY in environment variables.")
# client = openai.OpenAI(api_key=OPENAI_API_KEY)

# # Constants
# THREAD_DB_FILE = "threads_db"
# VECTOR_STORE_META_FILE = "vector_store_meta.json"
# SYSTEM_PROMPT = """You are assisting EASTC customers. Provide responses based on EASTC information and payment processing requests.
# If you can't answer, advise contacting EASTC directly."""
# VECTOR_STORE_NAME = "EastcVectorStore"
# FILE_PATHS = ["../Hybrid_whatsap_bot/app/Bot_Data/EASTC.txt"]

# FUNCTION_CALL_KEYWORDS = r"(provide payment instructions|check payment status|process payment|get contact info|info)"

# def determine_assistant(message_body):
#     """Determine the type of assistant to use based on message content."""
#     return "function" if re.search(FUNCTION_CALL_KEYWORDS, message_body, re.IGNORECASE) else "retrieval"



# # Thread Management
# def get_or_create_thread(wa_id):
#     """Retrieve or create a thread for a user."""
#     with shelve.open(THREAD_DB_FILE, writeback=True) as db:
#         if wa_id in db:
#             thread_id = db[wa_id]
#             try:
#                 client.beta.threads.retrieve(thread_id=thread_id)
#                 logging.info(f"Retrieved existing thread ID: {thread_id} for WA ID: {wa_id}")
#                 return thread_id
#             except Exception as e:
#                 logging.warning(f"Thread ID {thread_id} is invalid. Creating a new thread for WA ID: {wa_id}.")
        
#         # Create a new thread
#         thread = client.beta.threads.create(messages=[{"role": "user", "content": "Start a new conversation"}])
#         thread_id = thread.id
#         db[wa_id] = thread_id
#         logging.info(f"Created new thread ID: {thread_id} for WA ID: {wa_id}")
#         return thread_id


# # Vector Store Management
# import json

# VECTOR_STORE_META_FILE = "vector_store_metadata.json"

# def save_metadata(file_path, data):
#     """
#     Save metadata to a JSON file.

#     Args:
#         file_path (str): Path to the metadata file.
#         data (dict): Metadata to save.
#     """
#     try:
#         with open(file_path, "w") as f:
#             json.dump(data, f, indent=4)
#         logging.info(f"Metadata saved to {file_path}.")
#     except Exception as e:
#         logging.error(f"Failed to save metadata: {e}")
#         raise RuntimeError("Failed to save metadata.")

# def load_metadata(file_path):
#     """
#     Load metadata from a JSON file.

#     Args:
#         file_path (str): Path to the metadata file.

#     Returns:
#         dict: Loaded metadata.
#     """
#     try:
#         with open(file_path, "r") as f:
#             metadata = json.load(f)
#         logging.info(f"Metadata loaded from {file_path}.")
#         return metadata
#     except FileNotFoundError:
#         logging.warning(f"Metadata file {file_path} not found. Starting fresh.")
#         return {}
#     except Exception as e:
#         logging.error(f"Failed to load metadata: {e}")
#         raise RuntimeError("Failed to load metadata.")

# import os
# import json
# import logging

# # Constants
# VECTOR_STORE_META_FILE = "vector_store_metadata.json"

# def load_metadata(file_path):
#     """Load metadata from a JSON file."""
#     if not os.path.exists(file_path):
#         return None
#     with open(file_path, "r") as f:
#         return json.load(f)

# def save_metadata(file_path, data):
#     """Save metadata to a JSON file."""
#     with open(file_path, "w") as f:
#         json.dump(data, f, indent=4)

# def upload_file_with_vector_store(file_paths, vector_store_name="DefaultVectorStore"):
#     """
#     Upload files to OpenAI and associate them with a vector store, checking for existing metadata.

#     Args:
#         file_paths (list of str): Paths of files to upload.
#         vector_store_name (str): The name of the vector store.

#     Returns:
#         dict: Metadata about the vector store and uploaded files.
#     """
#     try:
#         # Load existing metadata
#         metadata = load_metadata(VECTOR_STORE_META_FILE)
#         if metadata:
#             logging.info(f"Loaded existing metadata: {metadata}")

#             # Check if the vector store and files match
#             if (
#                 metadata.get("vector_store_name") == vector_store_name
#                 and set(metadata.get("uploaded_files", [])) == set(file_paths)
#             ):
#                 logging.info(f"Vector store '{vector_store_name}' and files already uploaded.")
#                 return metadata

#         # No matching metadata; proceed with upload
#         logging.info(f"Creating vector store: {vector_store_name}")
#         vector_store = client.beta.vector_stores.create(name=vector_store_name)
#         logging.info(f"Vector store created with ID: {vector_store.id}")

#         # Prepare file streams
#         file_streams = [open(path, "rb") for path in file_paths]
#         logging.info(f"Uploading files to vector store '{vector_store_name}'...")

#         # Upload files and associate them with the vector store
#         file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
#             vector_store_id=vector_store.id,
#             files=file_streams
#         )

#         # Safely extract file counts if available
#         file_counts = {}
#         if hasattr(file_batch, 'file_counts'):
#             file_counts = {
#                 "processed_files": getattr(file_batch.file_counts, 'processed', None),
#                 "failed_files": getattr(file_batch.file_counts, 'failed', None),
#                 "pending_files": getattr(file_batch.file_counts, 'pending', None),
#             }

#         # Close file streams
#         for stream in file_streams:
#             stream.close()

#         # Prepare and save metadata
#         metadata = {
#             "vector_store_name": vector_store_name,
#             "vector_store_id": vector_store.id,
#             "file_batch_status": file_batch.status,
#             "file_counts": file_counts,
#             "uploaded_files": file_paths,
#         }
#         save_metadata(VECTOR_STORE_META_FILE, metadata)

#         # Log the result
#         logging.info(f"File batch upload completed with status: {file_batch.status}")
#         logging.info(f"File counts: {file_counts}")

#         return metadata

#     except Exception as e:
#         logging.error(f"Error uploading files to vector store: {e}")
#         raise RuntimeError("Failed to upload files to vector store.")

# # Metadata File for Assistants
# ASSISTANT_META_FILE = "assistants_meta.json"

# def load_assistant_metadata():
#     """Load assistant metadata from a local file."""
#     if os.path.exists(ASSISTANT_META_FILE):
#         with open(ASSISTANT_META_FILE, "r") as f:
#             return json.load(f)
#     return {}

# def save_assistant_metadata(data):
#     """Save assistant metadata to a local file."""
#     with open(ASSISTANT_META_FILE, "w") as f:
#         json.dump(data, f)

# def get_or_create_function_assistant():
#     """Retrieve or create a function assistant."""
#     metadata = load_assistant_metadata()
#     if "function_assistant_id" in metadata:
#         logging.info(f"Using existing Function Assistant ID: {metadata['function_assistant_id']}")
#         return metadata["function_assistant_id"]

#     try:
#         # Create the function assistant
#         assistant = client.beta.assistants.create(
#             name="FunctionAssistant",
#             instructions=SYSTEM_PROMPT,
#             model="gpt-3.5-turbo",
#             tools=eastc_functions,
#         )
#         logging.info(f"Function assistant created successfully with ID: {assistant.id}")

#         # Save the assistant ID
#         metadata["function_assistant_id"] = assistant.id
#         save_assistant_metadata(metadata)
#         return assistant.id

#     except Exception as e:
#         logging.error(f"Failed to create function assistant: {e}")
#         raise RuntimeError("Failed to create the function assistant.")

# def get_or_create_retrieval_assistant(vector_store_id):
#     """Retrieve or create a retrieval assistant."""
#     metadata = load_assistant_metadata()
#     if "retrieval_assistant_id" in metadata:
#         logging.info(f"Using existing Retrieval Assistant ID: {metadata['retrieval_assistant_id']}")
#         return metadata["retrieval_assistant_id"]

#     try:
#         # Create the retrieval assistant
#         assistant = client.beta.assistants.create(
#             name="RetrievalAssistant",
#             instructions=SYSTEM_PROMPT,
#             model="gpt-3.5-turbo",
#             tools=[{"type": "file_search"}],
#         )
#         updated_assistant = client.beta.assistants.update(
#             assistant_id=assistant.id,
#             tool_resources={"file_search": {"vector_store_ids": [vector_store_id]}},
#         )
#         logging.info(f"Retrieval assistant created successfully with ID: {updated_assistant.id}")

#         # Save the assistant ID
#         metadata["retrieval_assistant_id"] = updated_assistant.id
#         save_assistant_metadata(metadata)
#         return updated_assistant.id

#     except Exception as e:
#         logging.error(f"Failed to create retrieval assistant: {e}")
#         raise RuntimeError("Failed to create the retrieval assistant.")

# # Initialize Assistants
# def initialize_assistants():
#     """Initialize vector store and assistants."""
#     metadata = upload_file_with_vector_store(FILE_PATHS, VECTOR_STORE_NAME)
#     vector_store_id = metadata["vector_store_id"]

#     retrieval_assistant_id = get_or_create_retrieval_assistant(vector_store_id)
#     function_assistant_id = get_or_create_function_assistant()

#     logging.info(f"Retrieval Assistant ID: {retrieval_assistant_id}")
#     logging.info(f"Function Assistant ID: {function_assistant_id}")

#     return retrieval_assistant_id, function_assistant_id


# # Example: Usage
# retrieval_assistant_id, function_assistant_id = initialize_assistants()
# # Run assistants
# # --- Functionality-Specific Logic ---
# def handle_function_call(function_call):
#     """Handle function calls from the assistant."""
#     function_name = function_call.name
#     function_args = json.loads(function_call.arguments or "{}")
    
#     # Define function mapping
#     function_map = {
#         "get_contact_info": lambda args: f"Contact info for department {args['department']}.",
#         "process_payment": lambda args: f"Processed payment of {args['amount']} {args['currency']} using {args['method']}.",
#     }

#     # Execute the function if it exists
#     if function_name in function_map:
#         return function_map[function_name](function_args)
#     else:
#         return f"Function {function_name} is not implemented."

# def run_assistant(thread_id, name, message, assistant_id, is_retrieval=False):
#     """Run assistant and handle responses."""
#     try:
#         user_message = client.beta.threads.messages.create(
#             thread_id=thread_id,
#             role="user",
#             content=message+name,
#         )

#         run = client.beta.threads.runs.create(
#             thread_id=thread_id,
#             assistant_id=assistant_id,
#         )

#         while run.status != "completed":
#             time.sleep(0.5)
#             run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)

#         # Retrieve and process responses
#         messages = client.beta.threads.messages.list(thread_id=thread_id)
#         for msg in messages.data:
#             if msg.role == "assistant":
#                 if hasattr(msg, "function_call") and not is_retrieval:
#                     return handle_function_call(msg.function_call)
#                 return msg.content

#     except Exception as e:
#         logging.error(f"Error running assistant: {e}")
#         return "An error occurred. Please try again."

# def cancel_active_runs(thread_id):
#     """Cancel any active runs for the given thread, ignoring expired runs."""
#     try:
#         # List all runs for the thread
#         runs = client.beta.threads.runs.list(thread_id=thread_id)
#         for run in runs.data:
#             if run.status in ["in_progress", "queued"]:  # Only cancel actionable runs
#                 try:
#                     logging.info(f"Cancelling active run {run.id}.")
#                     client.beta.threads.runs.cancel(thread_id=thread_id, run_id=run.id)
#                 except Exception as cancel_error:
#                     logging.error(f"Error cancelling run {run.id}: {cancel_error}")
#             elif run.status == "expired":
#                 logging.warning(f"Run {run.id} is expired and cannot be cancelled.")
#     except Exception as e:
#         logging.error(f"Error cancelling active runs: {e}")

# def reset_thread(thread_id):
#     """Reset a thread by creating a new one or reinitializing it."""
#     try:
#         logging.info(f"Resetting thread {thread_id}.")
#         # Fetch the thread's messages
#         original_messages = client.beta.threads.messages.list(thread_id=thread_id).data

#         # Ensure all messages have valid string content
#         cleaned_messages = []
#         for msg in original_messages:
#             # Flatten content to a single string if necessary
#             if isinstance(msg.content, list):  # Handle cases where content is a list
#                 msg_content = " ".join([str(item.text) for item in msg.content if isinstance(item, dict) and "text" in item])
#             elif isinstance(msg.content, str):  # If it's already a string
#                 msg_content = msg.content
#             else:
#                 logging.warning(f"Unexpected message content format: {msg.content}")
#                 msg_content = str(msg.content)  # Fallback to string conversion

#             cleaned_messages.append({"role": msg.role, "content": msg_content})

#         # Create a new thread with the cleaned messages
#         new_thread = client.beta.threads.create(messages=cleaned_messages)
#         logging.info(f"Thread {thread_id} reset successfully to {new_thread.id}.")
#         return new_thread.id

#     except Exception as e:
#         logging.error(f"Error resetting thread {thread_id}: {e}")
#         raise RuntimeError("Failed to reset thread.")


# processing_threads = set()  # Track active threads to prevent duplicates

# def process_message(message_body, wa_id, name):
#     global processing_threads
#     if wa_id in processing_threads:
#         logging.warning(f"Message from {wa_id} is already being processed. Ignoring duplicate request.")
#         return "Your request is already being processed."

#     processing_threads.add(wa_id)
#     try:
#         response = generate_response(message_body, wa_id, name)
#     finally:
#         processing_threads.remove(wa_id)  # Ensure thread is removed after processing
#     return response




# def run_function_assistant(thread_id, name, message):
#     return run_assistant(thread_id, name, message, function_assistant_id)

# def run_retrieval_assistant(thread_id, name, message):
#     return run_assistant(thread_id, name, message, retrieval_assistant_id)

# # Generate response
# def generate_response(message_body, wa_id, name):
#     thread_id = get_or_create_thread(wa_id)
    
#     try:
#         cancel_active_runs(thread_id)  # Cancel active runs if necessary
#     except Exception as e:
#         logging.error(f"Error during run cancellation: {e}")

#     # Check for expired runs and reset thread if necessary
#     runs = client.beta.threads.runs.list(thread_id=thread_id)
#     expired_runs = [run for run in runs.data if run.status == "expired"]

#     if expired_runs:
#         try:
#             logging.warning(f"Thread {thread_id} has expired runs. Resetting the thread.")
#             thread_id = reset_thread(thread_id)
#         except RuntimeError:
#             logging.error("Failed to reset thread. Aborting message processing.")
#             return "Sorry, your request could not be processed due to a system issue. Please try again later."

#     # Determine which assistant to use
#     assistant_type = determine_assistant(message_body)
#     if assistant_type == "function":
#         return run_function_assistant(thread_id, name, message_body)
#     else:
#         return run_retrieval_assistant(thread_id, name, message_body)

# # # Setup Process
# # file_paths = ["../Hybrid_whatsap_bot/app/Bot_Data/EASTC.txt"]
# # upload_result = upload_file_with_vector_store(file_paths)
# # retrieval_assistant_id = create_retrieval_assistant(upload_result["vector_store_id"])
# # function_assistant_id = create_function_assistant()

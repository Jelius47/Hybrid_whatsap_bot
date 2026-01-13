# eastc_functions = [
#     {
#         "type": "function",
#         "function": {
#             "name": "get_contact_info",
#             "description": "Provide contact information for EASTC.",
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "department": {
#                         "type": "string",
#                         "description": "The specific department to get contact info for (e.g., 'admissions', 'finance')."
#                     }
#                 },
#                 "required": ["department"]
#             }
#         }
#     },
#     {
#         "type": "function",
#         "function": {
#             "name": "process_payment",
#             "description": "Process a payment with specified details.",
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "amount": {
#                         "type": "number",
#                         "description": "The amount to be paid."
#                     },
#                     "currency": {
#                         "type": "string",
#                         "description": "The currency in which the payment is made (e.g., 'USD', 'EUR')."
#                     },
#                     "method": {
#                         "type": "string",
#                         "description": "The payment method to use, e.g., 'credit card', 'bank transfer'."
#                     }
#                 },
#                 "required": ["amount", "currency", "method"]
#             }
#         }
#     },
#     {
#         "type": "function",
#         "function": {
#             "name": "check_payment_status",
#             "description": "Check the status of a specific payment.",
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "transaction_id": {
#                         "type": "string",
#                         "description": "The transaction ID of the payment to check."
#                     }
#                 },
#                 "required": ["transaction_id"]
#             }
#         }
#     },
#     {
#         "type": "function",
#         "function": {
#             "name": "provide_payment_instructions",
#             "description": "Provide instructions for making a payment.",
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "method": {
#                         "type": "string",
#                         "description": "The method of payment, e.g., 'credit card', 'bank transfer'."
#                     }
#                 },
#                 "required": ["method"]
#             }
#         }
#     }
# ]
eastc_functions = [
    {
        "type": "function",
        "function": {
            "name": "register_user",
            "description": "Registers a user by sending their phone number and car plate number to an external registration service.",
            "parameters": {
                "type": "object",
                "properties": {
                    "phone_number": {
                        "type": "string",
                        "description": "The phone number of the user to be registered.",
                    },
                    "car_plate_no": {
                        "type": "string",
                        "description": "The car plate number of the user's vehicle.",
                    },
                },
                "required": ["phone_number", "car_plate_no"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "confirm_booking",
            "description": "Allows a user to confirm or cancel their booking for a gas station.",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "integer",
                        "description": "The unique ID of the user confirming or canceling the booking.",
                    },
                    "confirmation": {
                        "type": "boolean",
                        "description": "The user's confirmation status. Set to 'true' for confirmation or 'false' for cancellation.",
                    },
                },
                "required": ["user_id", "confirmation"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "request_filling_station",
            "description": "Provides a list of nearby gas filling stations based on the user's location.",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "integer",
                        "description": "The unique ID of the user requesting nearby filling stations.",
                    }
                },
                "required": ["user_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "payment_options",
            "description": "Allows a user to select a payment method (cash or electronic) for their gas station booking.",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "integer",
                        "description": "The unique ID of the user selecting a payment option.",
                    },
                    "payment_option": {
                        "type": "string",
                        "description": "The payment method chosen by the user. Must be either 'cash' or 'electronic'.",
                    },
                },
                "required": ["user_id", "payment_option"],
            },
        },
    },
]

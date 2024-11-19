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
                            "name": "get_contact_info",
                            "description": "Provide contact information for EASTC.",
                            "parameters": {
                                "type": "object",
                                "properties": {
                                    "department": {
                                        "type": "string",
                                        "description": "The specific department to get contact info for (e.g., 'admissions', 'finance')."
                                    }
                                },
                                "required": ["department"]
                            }
                        },
                        {
                            "name": "process_payment",
                            "description": "Process a payment with specified details.",
                            "parameters": {
                                "type": "object",
                                "properties": {
                                    "amount": {
                                        "type": "number",
                                        "description": "The amount to be paid."
                                    },
                                    "currency": {
                                        "type": "string",
                                        "description": "The currency in which the payment is made (e.g., 'USD', 'EUR')."
                                    },
                                    "method": {
                                        "type": "string",
                                        "description": "The payment method to use, e.g., 'credit card', 'bank transfer'."
                                    }
                                },
                                "required": ["amount", "currency", "method"]
                            }
                        }
                    ]
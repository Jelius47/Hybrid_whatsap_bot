# ticketing_custom_functions = [
#     {
#         'name': 'greetings_what_is_our_business',
#         'description': 'Send a welcome message explaining the business and its purpose.',
#         'parameters': {
#             'type': 'object',
#             'properties': {
#                 'wa_id': {
#                     'type': 'string',
#                     'description': 'WhatsApp ID of the user.'
#                 },
#                 'name': {
#                     'type': 'string',
#                     'description': 'Name of the user to personalize the greeting.'
#                 }
#             },
#             'required': ['wa_id', 'name']
#         }
#     },
#     {
#         'name': 'provide_event_details',
#         'description': 'Provide details of the specified event, including date, time, and location.',
#         'parameters': {
#             'type': 'object',
#             'properties': {
#                 'event_name': {
#                     'type': 'string',
#                     'description': 'Name of the event for which details are requested.'
#                 },
#                 'wa_id': {
#                     'type': 'string',
#                     'description': 'WhatsApp ID of the user.'
#                 },
#                 'name': {
#                     'type': 'string',
#                     'description': 'Name of the user making the request.'
#                 }
#             },
#             'required': ['event_name', 'wa_id', 'name']
#         }
#     },
#     {
#         'name': 'process_payment_provide_response',
#         'description': 'Process payment for an event and provide a confirmation response.',
#         'parameters': {
#             'type': 'object',
#             'properties': {
#                 'event_name': {
#                     'type': 'string',
#                     'description': 'The name of the event being paid for.'
#                 },
#                 'wa_id': {
#                     'type': 'string',
#                     'description': 'WhatsApp ID of the user making the payment.'
#                 },
#                 'name': {
#                     'type': 'string',
#                     'description': 'Name of the user making the payment.'
#                 }
#             },
#             'required': ['event_name', 'wa_id', 'name']
#         }
#     },
#     {
#         'name': 'ticket_cutting_ticket_generation',
#         'description': 'Generate a ticket for the user and provide a confirmation message with a unique ticket ID.',
#         'parameters': {
#             'type': 'object',
#             'properties': {
#                 'event_name': {
#                     'type': 'string',
#                     'description': 'The name of the event for which the ticket is being generated.'
#                 },
#                 'wa_id': {
#                     'type': 'string',
#                     'description': 'WhatsApp ID of the user receiving the ticket.'
#                 },
#                 'name': {
#                     'type': 'string',
#                     'description': 'Name of the user for the ticket confirmation.'
#                 }
#             },
#             'required': ['event_name', 'wa_id', 'name']
#         }
#     },
#     {
#         'name': 'retrieve_tickets_details',
#         'description': 'Retrieve and provide ticket details if they exist in the database.',
#         'parameters': {
#             'type': 'object',
#             'properties': {
#                 'event_name': {
#                     'type': 'string',
#                     'description': 'The name of the event for which the ticket details are requested.'
#                 },
#                 'wa_id': {
#                     'type': 'string',
#                     'description': 'WhatsApp ID of the user requesting ticket details.'
#                 },
#                 'name': {
#                     'type': 'string',
#                     'description': 'Name of the user requesting ticket details.'
#                 }
#             },
#             'required': ['event_name', 'wa_id', 'name']
#         }
#     }
# ]
ona_functions = [
    {
        'name': 'what_is_ona_stories',
        'description': 'Provide a description of Ona Stories.',
        'parameters': {
            'type': 'object',
            'properties': {}
        }
    },
    {
        'name': 'provide_contact_and_location',
        'description': 'Provide contact information and location for Ona Stories.',
        'parameters': {
            'type': 'object',
            'properties': {}
        }
    },
    {
        'name': 'provide_sample_works',
        'description': 'List sample works created by Ona Stories.',
        'parameters': {
            'type': 'object',
            'properties': {}
        }
    }
]
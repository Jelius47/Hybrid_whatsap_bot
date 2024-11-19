# Informational Functions (aligned with descriptions)
# def get_eastc_history(start_date, end_date):
#     """Retrieve EASTC historical information within a specified date range."""
#     # Here, simulate retrieval with mock data or database query.
#     return [
#         {"title": "EASTC Founded", "description": f"EASTC was founded on {start_date}."},
#         {"title": "Expansion Phase", "description": f"Major expansions occurred up to {end_date}."}
#     ]

def get_contact_info(department):
    """Retrieve contact information for a specified EASTC department."""
    contacts = {
        "admissions": {"title": "Admissions Office", "description": "Contact admissions at admissions@eastc.org"},
        "finance": {"title": "Finance Department", "description": "Contact finance at finance@eastc.org"},
    }
    return contacts.get(department.lower(), {"title": "Department Not Found", "description": f"No contact info for {department}."})

# Payment Processing Functions (development category)
def process_payment(amount, currency, method):
    """Process a payment transaction based on provided details."""
    # Simulate payment processing
    return f"Payment of {amount} {currency} processed using {method}."

def check_payment_status(transaction_id):
    """Check the status of a payment based on transaction ID."""
    # Simulate checking payment status
    return f"Payment status for transaction ID {transaction_id} is: completed."

def provide_payment_instructions(method):
    """Provide instructions for making a payment using a specified method."""
    instructions = {
        "credit card": "Use your credit card number and CVV to complete the payment.",
        "bank transfer": "Transfer to our account at Bank XYZ, Account Number 123456789."
    }
    return instructions.get(method.lower(), "No instructions available for this payment method.")

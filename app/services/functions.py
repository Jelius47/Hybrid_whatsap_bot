import requests
from flask import Flask, request, jsonify
from flask import Blueprint, request, jsonify, current_app

webhook_blueprint = Blueprint("webhook", __name__)

REGISTRATION_URL = "https://9a83-197-250-226-222.ngrok-free.app/registration"
# In-memory database for demonstration purposes

users_db = {}
bookings_db = []


# @webhook_blueprint.route("/register", methods=["POST"])

def register_user():
    data = request.json
    phone_number = data.get('phone_number')
    car_plate_no = data.get('car_plate_no')

    if not phone_number or not car_plate_no:
        return jsonify({"error": "Phone number and car plate number are required"}), 400

    # Send data to the external registration endpoint
    try:
        response = requests.post(REGISTRATION_URL, json=data)
        if response.status_code == 201:
            user_id = len(users_db) + 1
            users_db[user_id] = {
                "phone_number": phone_number,
                "car_plate_no": car_plate_no
            }
            return jsonify({"message": "User registered successfully", "user_id": user_id}), 201
        else:
            return jsonify({"error": "Failed to register user", "details": response.json()}), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Could not connect to registration service", "details": str(e)}), 500

# Payment options endpoint

# @app.route('/payment', methods=['POST'])
# @webhook_blueprint.route("/payment", methods=["POST"])

def payment_options():
    data = request.json
    user_id = data.get('user_id')
    payment_option = data.get('payment_option')

    if not user_id or not payment_option:
        return jsonify({"error": "User ID and payment option are required"}), 400

    if payment_option not in ["cash", "electronic"]:
        return jsonify({"error": "Invalid payment option"}), 400

    bookings_db.append({
        "user_id": user_id,
        "payment_option": payment_option,
        "status": "Pending"
    })
    return jsonify({"message": "Payment option selected successfully"}), 200


# Nearby filling stations endpoint
# @webhook_blueprint.route("/filling-stations", methods=["POST"])

def request_filling_station():
    data = request.json
    user_id = data.get('user_id')

    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    # Mock data for nearby filling stations
    filling_stations = [
        {"name": "Station A", "location": "Kinondoni", "distance": "2.5 km"},
        {"name": "Station B", "location": "Mikocheni", "distance": "3.0 km"},
        {"name": "Station C", "location": "Kijitonyama", "distance": "4.2 km"}
    ]
    return jsonify({"message": "Nearby filling stations", "stations": filling_stations}), 200


# Booking confirmation endpoint
# @webhook_blueprint.route("/confirmation-", methods=["POST"])

def confirm_booking():
    data = request.json
    user_id = data.get('user_id')
    confirmation = data.get('confirmation')

    if not user_id or confirmation is None:
        return jsonify({"error": "User ID and confirmation status are required"}), 400

    for booking in bookings_db:
        if booking['user_id'] == user_id:
            if confirmation:
                booking['status'] = "Confirmed"
                return jsonify({"message": "Booking confirmed"}), 200
            else:
                booking['status'] = "Cancelled"
                return jsonify({"message": "Booking cancelled"}), 200

    return jsonify({"error": "Booking not found for the user"}), 404

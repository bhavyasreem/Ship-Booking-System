from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .db import (
    passengers_col, ships_col, schedules_col, bookings_col, payments_col,
    get_next_passenger_id, get_next_ship_id, get_next_schedule_id,
    get_next_booking_id, get_next_payment_id
)

def clean_doc(doc):
    if doc and '_id' in doc:
        del doc['_id']
    return doc

def safe_int(val, default=0):
    try:
        if val is None:
            return default
        return int(val)
    except (ValueError, TypeError):
        return default

def safe_float(val, default=0.0):
    try:
        if val is None:
            return default
        return float(val)
    except (ValueError, TypeError):
        return default

# ==================== PASSENGER MANAGEMENT ====================

@api_view(['POST'])
def add_passenger(request):
    data = request.data.copy()
    data['passenger_id'] = get_next_passenger_id()
    # Ensure fields are strings
    data['full_name'] = str(data.get('full_name', ''))
    data['email'] = str(data.get('email', '')).lower().strip()
    data['phone'] = str(data.get('phone', ''))
    data['nationality'] = str(data.get('nationality', ''))
    data['passport_number'] = str(data.get('passport_number', ''))
    data['password'] = str(data.get('password', ''))
    
    passengers_col.insert_one(data)
    return Response(clean_doc(data), status=status.HTTP_201_CREATED)

@api_view(['GET'])
def get_passengers(request):
    passengers = list(passengers_col.find({}, {'_id': 0}))
    return Response(passengers, status=status.HTTP_200_OK)

@api_view(['PUT'])
def update_passenger(request, id):
    try:
        pid = int(id)
    except ValueError:
        return Response({"error": "Invalid passenger ID"}, status=status.HTTP_400_BAD_REQUEST)
    
    data = request.data.copy()
    if 'passenger_id' in data:
        del data['passenger_id']
    
    # Cast fields if they are present in update request
    if 'full_name' in data: data['full_name'] = str(data['full_name'])
    if 'email' in data: data['email'] = str(data['email']).lower().strip()
    if 'phone' in data: data['phone'] = str(data['phone'])
    if 'nationality' in data: data['nationality'] = str(data['nationality'])
    if 'passport_number' in data: data['passport_number'] = str(data['passport_number'])
    if 'password' in data: data['password'] = str(data['password'])

    result = passengers_col.update_one({"passenger_id": pid}, {"$set": data})
    if result.matched_count == 0:
        return Response({"error": "Passenger not found"}, status=status.HTTP_404_NOT_FOUND)
    
    updated = passengers_col.find_one({"passenger_id": pid}, {'_id': 0})
    return Response(updated, status=status.HTTP_200_OK)

@api_view(['DELETE'])
def delete_passenger(request, id):
    try:
        pid = int(id)
    except ValueError:
        return Response({"error": "Invalid passenger ID"}, status=status.HTTP_400_BAD_REQUEST)
    
    result = passengers_col.delete_one({"passenger_id": pid})
    if result.deleted_count == 0:
        return Response({"error": "Passenger not found"}, status=status.HTTP_404_NOT_FOUND)
    return Response({"message": "Passenger deleted successfully"}, status=status.HTTP_200_OK)


# ==================== SHIP MANAGEMENT ====================

@api_view(['POST'])
def add_ship(request):
    data = request.data.copy()
    data['ship_id'] = get_next_ship_id()
    data['ship_name'] = str(data.get('ship_name', ''))
    data['ship_type'] = str(data.get('ship_type', 'Cruise Ship'))
    data['capacity'] = safe_int(data.get('capacity', 0))
    data['operator_name'] = str(data.get('operator_name', ''))
    data['status'] = str(data.get('status', 'Active'))
    
    ships_col.insert_one(data)
    return Response(clean_doc(data), status=status.HTTP_201_CREATED)

@api_view(['GET'])
def get_ships(request):
    ships = list(ships_col.find({}, {'_id': 0}))
    return Response(ships, status=status.HTTP_200_OK)

@api_view(['PUT'])
def update_ship(request, id):
    try:
        sid = int(id)
    except ValueError:
        return Response({"error": "Invalid ship ID"}, status=status.HTTP_400_BAD_REQUEST)
    
    data = request.data.copy()
    if 'ship_id' in data:
        del data['ship_id']
        
    if 'ship_name' in data: data['ship_name'] = str(data['ship_name'])
    if 'ship_type' in data: data['ship_type'] = str(data['ship_type'])
    if 'capacity' in data: data['capacity'] = safe_int(data['capacity'])
    if 'operator_name' in data: data['operator_name'] = str(data['operator_name'])
    if 'status' in data: data['status'] = str(data['status'])

    result = ships_col.update_one({"ship_id": sid}, {"$set": data})
    if result.matched_count == 0:
        return Response({"error": "Ship not found"}, status=status.HTTP_404_NOT_FOUND)
        
    updated = ships_col.find_one({"ship_id": sid}, {'_id': 0})
    return Response(updated, status=status.HTTP_200_OK)

@api_view(['DELETE'])
def delete_ship(request, id):
    try:
        sid = int(id)
    except ValueError:
        return Response({"error": "Invalid ship ID"}, status=status.HTTP_400_BAD_REQUEST)
        
    result = ships_col.delete_one({"ship_id": sid})
    if result.deleted_count == 0:
        return Response({"error": "Ship not found"}, status=status.HTTP_404_NOT_FOUND)
    return Response({"message": "Ship deleted successfully"}, status=status.HTTP_200_OK)


# ==================== ROUTE & SCHEDULE MANAGEMENT ====================

@api_view(['POST'])
def add_schedule(request):
    data = request.data.copy()
    data['schedule_id'] = get_next_schedule_id()
    data['ship_name'] = str(data.get('ship_name', ''))
    data['source_port'] = str(data.get('source_port', ''))
    data['destination_port'] = str(data.get('destination_port', ''))
    data['departure_date'] = str(data.get('departure_date', ''))
    data['departure_time'] = str(data.get('departure_time', ''))
    data['arrival_date'] = str(data.get('arrival_date', ''))
    data['arrival_time'] = str(data.get('arrival_time', ''))
    data['fare'] = safe_float(data.get('fare', 0.0))
    
    schedules_col.insert_one(data)
    return Response(clean_doc(data), status=status.HTTP_201_CREATED)

@api_view(['GET'])
def get_schedules(request):
    schedules = list(schedules_col.find({}, {'_id': 0}))
    return Response(schedules, status=status.HTTP_200_OK)

@api_view(['PUT'])
def update_schedule(request, id):
    try:
        sid = int(id)
    except ValueError:
        return Response({"error": "Invalid schedule ID"}, status=status.HTTP_400_BAD_REQUEST)
        
    data = request.data.copy()
    if 'schedule_id' in data:
        del data['schedule_id']
        
    if 'ship_name' in data: data['ship_name'] = str(data['ship_name'])
    if 'source_port' in data: data['source_port'] = str(data['source_port'])
    if 'destination_port' in data: data['destination_port'] = str(data['destination_port'])
    if 'departure_date' in data: data['departure_date'] = str(data['departure_date'])
    if 'departure_time' in data: data['departure_time'] = str(data['departure_time'])
    if 'arrival_date' in data: data['arrival_date'] = str(data['arrival_date'])
    if 'arrival_time' in data: data['arrival_time'] = str(data['arrival_time'])
    if 'fare' in data: data['fare'] = safe_float(data['fare'])

    result = schedules_col.update_one({"schedule_id": sid}, {"$set": data})
    if result.matched_count == 0:
        return Response({"error": "Schedule not found"}, status=status.HTTP_404_NOT_FOUND)
        
    updated = schedules_col.find_one({"schedule_id": sid}, {'_id': 0})
    return Response(updated, status=status.HTTP_200_OK)

@api_view(['DELETE'])
def delete_schedule(request, id):
    try:
        sid = int(id)
    except ValueError:
        return Response({"error": "Invalid schedule ID"}, status=status.HTTP_400_BAD_REQUEST)
        
    result = schedules_col.delete_one({"schedule_id": sid})
    if result.deleted_count == 0:
        return Response({"error": "Schedule not found"}, status=status.HTTP_404_NOT_FOUND)
    return Response({"message": "Schedule deleted successfully"}, status=status.HTTP_200_OK)


# ==================== CABIN/TICKET BOOKING MANAGEMENT ====================

@api_view(['POST'])
def add_booking(request):
    data = request.data.copy()
    data['booking_id'] = get_next_booking_id()
    data['passenger_name'] = str(data.get('passenger_name', ''))
    data['ship_name'] = str(data.get('ship_name', ''))
    data['cabin_type'] = str(data.get('cabin_type', 'Economy'))
    data['journey_date'] = str(data.get('journey_date', ''))
    data['source_port'] = str(data.get('source_port', ''))
    data['destination_port'] = str(data.get('destination_port', ''))
    data['total_amount'] = safe_float(data.get('total_amount', 0.0))
    data['booking_status'] = str(data.get('booking_status', 'Waiting'))
    
    bookings_col.insert_one(data)
    return Response(clean_doc(data), status=status.HTTP_201_CREATED)

@api_view(['GET'])
def get_bookings(request):
    bookings = list(bookings_col.find({}, {'_id': 0}))
    return Response(bookings, status=status.HTTP_200_OK)

@api_view(['PUT'])
def update_booking(request, id):
    try:
        bid = int(id)
    except ValueError:
        return Response({"error": "Invalid booking ID"}, status=status.HTTP_400_BAD_REQUEST)
        
    data = request.data.copy()
    if 'booking_id' in data:
        del data['booking_id']
        
    if 'passenger_name' in data: data['passenger_name'] = str(data['passenger_name'])
    if 'ship_name' in data: data['ship_name'] = str(data['ship_name'])
    if 'cabin_type' in data: data['cabin_type'] = str(data['cabin_type'])
    if 'journey_date' in data: data['journey_date'] = str(data['journey_date'])
    if 'source_port' in data: data['source_port'] = str(data['source_port'])
    if 'destination_port' in data: data['destination_port'] = str(data['destination_port'])
    if 'total_amount' in data: data['total_amount'] = safe_float(data['total_amount'])
    if 'booking_status' in data: data['booking_status'] = str(data['booking_status'])

    result = bookings_col.update_one({"booking_id": bid}, {"$set": data})
    if result.matched_count == 0:
        return Response({"error": "Booking not found"}, status=status.HTTP_404_NOT_FOUND)
        
    updated = bookings_col.find_one({"booking_id": bid}, {'_id': 0})
    return Response(updated, status=status.HTTP_200_OK)

@api_view(['DELETE'])
def delete_booking(request, id):
    try:
        bid = int(id)
    except ValueError:
        return Response({"error": "Invalid booking ID"}, status=status.HTTP_400_BAD_REQUEST)
        
    result = bookings_col.delete_one({"booking_id": bid})
    if result.deleted_count == 0:
        return Response({"error": "Booking not found"}, status=status.HTTP_404_NOT_FOUND)
    return Response({"message": "Booking deleted successfully"}, status=status.HTTP_200_OK)


# ==================== PAYMENT MANAGEMENT ====================

@api_view(['POST'])
def add_payment(request):
    data = request.data.copy()
    data['payment_id'] = get_next_payment_id()
    data['booking_id'] = safe_int(data.get('booking_id', 0))
    data['passenger_name'] = str(data.get('passenger_name', ''))
    data['amount'] = safe_float(data.get('amount', 0.0))
    data['payment_method'] = str(data.get('payment_method', 'UPI'))
    data['payment_status'] = str(data.get('payment_status', 'Pending'))
    data['transaction_id'] = str(data.get('transaction_id', ''))
    data['payment_date'] = str(data.get('payment_date', ''))
    
    payments_col.insert_one(data)
    return Response(clean_doc(data), status=status.HTTP_201_CREATED)

@api_view(['GET'])
def get_payments(request):
    payments = list(payments_col.find({}, {'_id': 0}))
    return Response(payments, status=status.HTTP_200_OK)

@api_view(['PUT'])
def update_payment(request, id):
    try:
        pid = int(id)
    except ValueError:
        return Response({"error": "Invalid payment ID"}, status=status.HTTP_400_BAD_REQUEST)
        
    data = request.data.copy()
    if 'payment_id' in data:
        del data['payment_id']
        
    if 'booking_id' in data: data['booking_id'] = safe_int(data['booking_id'])
    if 'passenger_name' in data: data['passenger_name'] = str(data['passenger_name'])
    if 'amount' in data: data['amount'] = safe_float(data['amount'])
    if 'payment_method' in data: data['payment_method'] = str(data['payment_method'])
    if 'payment_status' in data: data['payment_status'] = str(data['payment_status'])
    if 'transaction_id' in data: data['transaction_id'] = str(data['transaction_id'])
    if 'payment_date' in data: data['payment_date'] = str(data['payment_date'])

    result = payments_col.update_one({"payment_id": pid}, {"$set": data})
    if result.matched_count == 0:
        return Response({"error": "Payment not found"}, status=status.HTTP_404_NOT_FOUND)
        
    updated = payments_col.find_one({"payment_id": pid}, {'_id': 0})
    return Response(updated, status=status.HTTP_200_OK)

@api_view(['DELETE'])
def delete_payment(request, id):
    try:
        pid = int(id)
    except ValueError:
        return Response({"error": "Invalid payment ID"}, status=status.HTTP_400_BAD_REQUEST)
        
    result = payments_col.delete_one({"payment_id": pid})
    if result.deleted_count == 0:
        return Response({"error": "Payment not found"}, status=status.HTTP_404_NOT_FOUND)
    return Response({"message": "Payment deleted successfully"}, status=status.HTTP_200_OK)

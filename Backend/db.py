import pymongo
from pymongo import ReturnDocument

# MongoDB Atlas connection details
CONNECTION_STRING = "mongodb+srv://Doremon_12:RRobertR%408908@cluster0.zx7ka0h.mongodb.net/"
client = pymongo.MongoClient(CONNECTION_STRING)
db = client["ship_booking_db"]

# Collection references
passengers_col = db["passengers"]
ships_col = db["ships"]
schedules_col = db["schedules"]
bookings_col = db["bookings"]
payments_col = db["payments"]

def get_next_id(collection_name, start_id):
    """
    Atomically increments and returns the next ID for the given collection name.
    If the sequence doesn't exist, it initializes to start_id.
    """
    result = db['counters'].find_one_and_update(
        {'_id': collection_name},
        {'$inc': {'sequence_value': 1}},
        upsert=True,
        return_document=ReturnDocument.AFTER
    )
    if result.get('sequence_value', 0) < start_id:
        db['counters'].update_one({'_id': collection_name}, {'$set': {'sequence_value': start_id}})
        return start_id
    return result['sequence_value']

def get_next_passenger_id():
    return get_next_id("passengers", 101)

def get_next_ship_id():
    return get_next_id("ships", 201)

def get_next_schedule_id():
    return get_next_id("schedules", 301)

def get_next_booking_id():
    return get_next_id("bookings", 401)

def get_next_payment_id():
    return get_next_id("payments", 501)

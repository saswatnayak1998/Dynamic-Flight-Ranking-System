from flask import Flask, request, jsonify
import mysql.connector
from datetime import datetime, timedelta
import decimal
from flask_cors import CORS  

app = Flask(__name__)
CORS(app) 

db_config = {
    'host': '127.0.0.1',
    'port': '3306',
    'user': 'root',
    'password': '9436068918',  
    'database': 'flight_db',  
}

def calculate_user_preference_score(flight, preferences):
    score = 0

    user_dep_time = datetime.strptime(preferences['departure_time'], '%H:%M')

    if isinstance(flight['departure_time'], timedelta):
        flight_dep_time = (datetime.min + flight['departure_time']).time()
    elif isinstance(flight['departure_time'], datetime):
        flight_dep_time = flight['departure_time'].time()
    else:
        flight_dep_time = datetime.strptime(flight['departure_time'], '%H:%M').time()

    time_diff = abs((user_dep_time - datetime.combine(datetime.min, flight_dep_time)).total_seconds() / 60)
    score += (120 - time_diff) / 120  # Score based on closeness

    user_arrival_time = datetime.strptime(preferences['arrival_time'], '%H:%M')

    if isinstance(flight['arrival_time'], timedelta):
        flight_arrival_time = (datetime.min + flight['arrival_time']).time()
    elif isinstance(flight['arrival_time'], datetime):
        flight_arrival_time = flight['arrival_time'].time()
    else:
        flight_arrival_time = datetime.strptime(flight['arrival_time'], '%H:%M').time()

    arrival_diff = abs((user_arrival_time - datetime.combine(datetime.min, flight_arrival_time)).total_seconds() / 60)
    score += (120 - arrival_diff) / 120

    preferred_airline = preferences['preferred_airline']
    score += 1 if flight['airline'] == preferred_airline else 0

    preferred_class = preferences['cabin_class']
    score += 1 if flight['cabin_class'] == preferred_class else 0

    return score/4

def calculate_enterprise_preference_score(flight, enterprise_preferences, min_price, max_price):
    score = 0

    enterprise_airline = enterprise_preferences['preferred_airline']
    score += 1 if flight['airline'] == enterprise_airline else 0

    score += (max_price - flight['price']) / (max_price - min_price) if max_price != min_price else 0
    print(score)
    return score/2


def fetch_flights_from_db(preferred_time, dep_city, dest_city, flight_date, buffer_hours=2):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    preferred_time_dt = datetime.strptime(preferred_time, '%H:%M')
    start_time = (preferred_time_dt - timedelta(hours=buffer_hours)).time()
    end_time = (preferred_time_dt + timedelta(hours=buffer_hours)).time()

    flight_date_formatted = datetime.strptime(flight_date, '%Y-%m-%d').strftime('%Y-%m-%d')

    query = """
    SELECT 
        f.*, 
        a.name AS airline,
        cc.class_name AS cabin_class,
        ao.name AS origin_airport,
        ad.name AS destination_airport
    FROM Flights f
    JOIN Airlines a ON f.airline_id = a.id
    JOIN CabinClasses cc ON f.cabin_class_id = cc.id
    JOIN Airports ao ON f.origin_id = ao.id
    JOIN Airports ad ON f.destination_id = ad.id
    WHERE 
        f.departure_time BETWEEN %s AND %s
        AND ao.code = %s
        AND ad.code = %s
        AND f.date = %s
    """
    cursor.execute(query, (start_time, end_time, dep_city, dest_city, flight_date_formatted))
    flights = cursor.fetchall()
    conn.close()
    print(len(flights))

    return flights


# Main ranking logic
def rank_flights(flights, user_weight, enterprise_weight, inventory_weight, user_preferences, enterprise_preferences):
    prices = [flight['price'] for flight in flights]
    min_price = min(prices)
    max_price = max(prices)

    ranked_flights = []
    for flight in flights:
        user_score = calculate_user_preference_score(flight, user_preferences)
        enterprise_score = calculate_enterprise_preference_score(flight, enterprise_preferences, min_price, max_price)
        user_score = float(user_score) if isinstance(user_score, decimal.Decimal) else user_score
        enterprise_score = float(enterprise_score) if isinstance(enterprise_score, decimal.Decimal) else enterprise_score
        inventory_score = 0  
        inventory_score = float(inventory_score) if isinstance(inventory_score, decimal.Decimal) else inventory_score
        print(user_weight, enterprise_weight)

        total_score = (user_weight * user_score) + (enterprise_weight * enterprise_score) + (inventory_weight * inventory_score)
        total_score = (user_weight * user_score) + (enterprise_weight * enterprise_score) + (inventory_weight * inventory_score)

        flight['total_score'] = total_score
        ranked_flights.append(flight)

    ranked_flights = sorted(ranked_flights, key=lambda x: x['total_score'], reverse=True)[:3]
    return ranked_flights

def timedelta_to_string(td):
    total_minutes = int(td.total_seconds() / 60)
    hours, minutes = divmod(total_minutes, 60)
    return f"{hours:02}:{minutes:02}"

def make_flights_json_serializable(flights):
    for flight in flights:
        if isinstance(flight.get('departure_time'), timedelta):
            flight['departure_time'] = timedelta_to_string(flight['departure_time'])
        if isinstance(flight.get('arrival_time'), timedelta):
            flight['arrival_time'] = timedelta_to_string(flight['arrival_time'])
    return flights

@app.route('/rank_flightss', methods=['POST'])
def rank_flights_endpoint():
    preferences = request.json
    user_preferences = preferences['user_preferences']
    enterprise_preferences = preferences['enterprise_preferences']
    user_weight = user_preferences.get('weight', 0.5)
    enterprise_weight = enterprise_preferences.get('weight', 0.5)
    inventory_weight = preferences.get('inventory_weight', 0)

    flights = fetch_flights_from_db(
        preferred_time=user_preferences['departure_time'],
        dep_city=user_preferences['departure_city'],
        dest_city=user_preferences['destination_city'],
        flight_date=user_preferences['date']
    )

    ranked_flights = rank_flights(
        flights, 
        user_weight, 
        enterprise_weight, 
        inventory_weight, 
        user_preferences, 
        enterprise_preferences
    )

    serializable_flights = make_flights_json_serializable(ranked_flights)

    return jsonify(serializable_flights)


if __name__ == '__main__':
    app.run(debug=True)

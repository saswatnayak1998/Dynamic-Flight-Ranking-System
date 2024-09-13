import mysql.connector
from mysql.connector import errorcode
import pandas as pd
import random
import datetime

db_config = {
    'user': 'root',  
    'password': '9436068918', 
    'host': '127.0.0.1',
    'port': 3306,
    'database': 'flight_db'
}

def connect_to_db(config):
    try:
        conn = mysql.connector.connect(**config)
        print("Successfully connected to the database.")
        return conn
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
        return None

def create_tables(cursor):
    table_statements = {
        'Airlines': """
        CREATE TABLE IF NOT EXISTS Airlines (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) UNIQUE
        );
        """,
        'Airports': """
        CREATE TABLE IF NOT EXISTS Airports (
            id INT AUTO_INCREMENT PRIMARY KEY,
            code VARCHAR(10) UNIQUE,
            name VARCHAR(255)
        );
        """,
        'CabinClasses': """
        CREATE TABLE IF NOT EXISTS CabinClasses (
            id INT AUTO_INCREMENT PRIMARY KEY,
            class_name VARCHAR(50) UNIQUE
        );
        """,
        'Flights': """
        CREATE TABLE IF NOT EXISTS Flights (
            id INT AUTO_INCREMENT PRIMARY KEY,
            airline_id INT,
            origin_id INT,
            destination_id INT,
            cabin_class_id INT,
            date DATE,
            departure_time TIME,
            arrival_time TIME,
            flight_duration FLOAT,
            price DECIMAL(10, 2),
            FOREIGN KEY (airline_id) REFERENCES Airlines(id),
            FOREIGN KEY (origin_id) REFERENCES Airports(id),
            FOREIGN KEY (destination_id) REFERENCES Airports(id),
            FOREIGN KEY (cabin_class_id) REFERENCES CabinClasses(id)
        );
        """
    }
    
    for table_name, create_statement in table_statements.items():
        try:
            cursor.execute(create_statement)
            print(f"Table {table_name} created successfully.")
        except mysql.connector.Error as err:
            print(f"Error creating table {table_name}: {err}")

def populate_lookup_tables(cursor):
    airlines = ['United', 'Air Canada', 'American Airlines', 'Delta', 'Lufthansa']
    airports = [
        ('JFK', 'John F. Kennedy International Airport'),
        ('LAX', 'Los Angeles International Airport'),
        ('ORD', 'Chicago O\'Hare International Airport'),
        ('DFW', 'Dallas/Fort Worth International Airport'),
        ('SFO', 'San Francisco International Airport')
    ]
    cabin_classes = ['Economy', 'Business', 'First']

    for airline in airlines:
        cursor.execute("INSERT IGNORE INTO Airlines (name) VALUES (%s)", (airline,))
    
    for code, name in airports:
        cursor.execute("INSERT IGNORE INTO Airports (code, name) VALUES (%s, %s)", (code, name))
    
    for cabin_class in cabin_classes:
        cursor.execute("INSERT IGNORE INTO CabinClasses (class_name) VALUES (%s)", (cabin_class,))

def generate_and_insert_flights(cursor, num_flights=100):
    airlines = ['United', 'Air Canada', 'American Airlines', 'Delta', 'Lufthansa']
    airports = ['JFK', 'LAX', 'ORD', 'DFW', 'SFO']
    cabin_classes = ['Economy', 'Business', 'First']
    
    for _ in range(num_flights):
        airline = random.choice(airlines)
        origin = random.choice(airports)
        destination = random.choice([airport for airport in airports if airport != origin])
        cabin_class = random.choice(cabin_classes)
        date = datetime.date.today() + datetime.timedelta(days=random.randint(0, 6))
        departure_time = datetime.time(random.randint(0, 23), random.randint(0, 59))
        flight_duration = round(random.uniform(1, 10), 2)
        arrival_time = (datetime.datetime.combine(datetime.date.today(), departure_time) +
                        datetime.timedelta(hours=flight_duration)).time()
        price = round(random.uniform(100, 1000), 2)

        cursor.execute("""
            INSERT INTO Flights (airline_id, origin_id, destination_id, cabin_class_id, date, 
                departure_time, arrival_time, flight_duration, price)
            VALUES (
                (SELECT id FROM Airlines WHERE name = %s),
                (SELECT id FROM Airports WHERE code = %s),
                (SELECT id FROM Airports WHERE code = %s),
                (SELECT id FROM CabinClasses WHERE class_name = %s),
                %s, %s, %s, %s, %s
            )
        """, (airline, origin, destination, cabin_class, date, departure_time, arrival_time, flight_duration, price))

def main():
    conn = connect_to_db(db_config)
    if conn:
        cursor = conn.cursor()
        create_tables(cursor)
        populate_lookup_tables(cursor)
        generate_and_insert_flights(cursor, num_flights=10000)  
        conn.commit()  
        cursor.close()
        conn.close()
        print("Data generation and insertion completed successfully.")

if __name__ == "__main__":
    main()

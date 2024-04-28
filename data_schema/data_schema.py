import sqlite3

DB_FILE = 'nyctransit_hub.db'

def create_tables(cursor):
    # Users
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id VARCHAR PRIMARY KEY,
            email VARCHAR UNIQUE,
            password HASH,
            profile_desc VARCHAR,
            alert_preferences VARCHAR
        )
    ''')

    # Favorites Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Favorites (
            user_id VARCHAR,
            RouteID NUMERIC,
            PRIMARY KEY (user_id, RouteID),
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    ''')

    # Routes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS routes (
            route_id NUMERIC PRIMARY KEY,
            route_short_name VARCHAR,
            route_name VARCHAR,
            route_type NUMERIC,
            route_url VARCHAR,
            route_color VARCHAR,
            route_text_color VARCHAR
        )
    ''')

    # Stops
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stops (
            stop_id VARCHAR PRIMARY KEY,
            stop_name VARCHAR,
            stop_lat NUMERIC,
            stop_lon NUMERIC,
            location_type NUMERIC,
            parent_station NUMERIC
        )
    ''')

    # Trips
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS trips (
            trip_id VARCHAR PRIMARY KEY,
            route_id NUMERIC,
            service_id VARCHAR,
            trip_headsign VARCHAR,
            direction_id VARCHAR,
            shape_id VARCHAR,
            FOREIGN KEY (route_id) REFERENCES routes(route_id)
        )
    ''')

    # Stop Times
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stop_times (
            trip_id VARCHAR,
            stop_id VARCHAR,
            arrival_time TIME,
            departure_time TIME,
            stop_sequence NUMERIC,
            PRIMARY KEY (trip_id, stop_id),
            FOREIGN KEY (trip_id) REFERENCES trips(trip_id),
            FOREIGN KEY (stop_id) REFERENCES stops(stop_id)
        )
    ''')

    # Shapes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS shapes (
            shape_id NUMERIC PRIMARY KEY,
            shape_pt_sequence NUMERIC,
            shape_pt_lat NUMERIC,
            shape_pt_lon NUMERIC
        )
    ''')

    # Calendar
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS calendar (
            service_id VARCHAR PRIMARY KEY,
            monday BOOLEAN,
            tuesday BOOLEAN,
            wednesday BOOLEAN,
            thursday BOOLEAN,
            friday BOOLEAN,
            saturday BOOLEAN,
            sunday BOOLEAN,
            start_date NUMERIC,
            end_date NUMERIC
        )
    ''')

    # Calendar Dates
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS calendar_dates (
            service_id VARCHAR,
            date NUMERIC,
            exception_type NUMERIC,
            FOREIGN KEY (service_id) REFERENCES calendar(service_id)
        )
    ''')

    # Vehicle Positions
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vehicle_positions (
            position_id VARCHAR PRIMARY KEY,
            vehicle_id VARCHAR,
            trip_id VARCHAR,
            current_stop_sequence NUMERIC,
            current_status NUMERIC,
            latitude NUMERIC,
            longitude NUMERIC,
            timestamp TIME,
            FOREIGN KEY (trip_id) REFERENCES trips(trip_id)
        )
    ''')

    # Service Alerts
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS service_alerts (
            alert_id VARCHAR PRIMARY KEY,
            alert_text VARCHAR,
            start_time TIME,
            end_time TIME,
            timestamp TIME
        )
    ''')

    # Transfers
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transfers (
            from_stop_id NUMERIC,
            to_stop_id NUMERIC,
            transfer_type NUMERIC,
            min_transfer_time NUMERIC,
            PRIMARY KEY (from_stop_id, to_stop_id),
            FOREIGN KEY (from_stop_id) REFERENCES stops(stop_id),
            FOREIGN KEY (to_stop_id) REFERENCES stops(stop_id)
        )
    ''')

    # Trip Updates
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS trip_updates (
            update_id VARCHAR PRIMARY KEY,
            trip_id VARCHAR,
            start_time TIME,
            delay NUMERIC,
            schedule_type NUMERIC,
            FOREIGN KEY (trip_id) REFERENCES trips(trip_id)
        )
    ''')

def main():
    # Establish a database connection
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Create tables
    create_tables(cursor)

    # Commit changes and close the connection
    conn.commit()
    conn.close()

if __name__ == "__main__":
    main

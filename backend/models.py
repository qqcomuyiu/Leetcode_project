import sqlite3
import csv

def connect_db():
    return sqlite3.connect('db/database.db')

def create_tables(conn):
    cursor = conn.cursor()
    
    # Agency Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS agency (
            agency_id TEXT PRIMARY KEY,
            agency_name TEXT,
            agency_url TEXT,
            agency_timezone TEXT,
            agency_lang TEXT,
            agency_phone TEXT
        )
    ''')

    # Calendar Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS calendar (
            service_id TEXT PRIMARY KEY,
            monday INTEGER,
            tuesday INTEGER,
            wednesday INTEGER,
            thursday INTEGER,
            friday INTEGER,
            saturday INTEGER,
            sunday INTEGER,
            start_date TEXT,
            end_date TEXT
        )
    ''')

    # Calendar Dates Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS calendar_dates (
            service_id TEXT,
            date TEXT,
            exception_type INTEGER,
            PRIMARY KEY (service_id, date)
        )
    ''')

    # Routes Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS routes (
            route_id TEXT PRIMARY KEY,
            agency_id TEXT,
            route_short_name TEXT,
            route_long_name TEXT,
            route_type INTEGER,
            route_desc TEXT,
            route_url TEXT,
            route_color TEXT,
            route_text_color TEXT,
            FOREIGN KEY (agency_id) REFERENCES agency(agency_id)
        )
    ''')

    # Shapes Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS shapes (
            shape_id TEXT,
            shape_pt_sequence INTEGER,
            shape_pt_lat REAL,
            shape_pt_lon REAL,
            PRIMARY KEY (shape_id, shape_pt_sequence)
        )
    ''')

    # Stop Times Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stop_times (
            trip_id TEXT,
            stop_id TEXT,
            arrival_time TEXT,
            departure_time TEXT,
            stop_sequence INTEGER,
            PRIMARY KEY (trip_id, stop_sequence),
            FOREIGN KEY (stop_id) REFERENCES stops(stop_id)
        )
    ''')

    # Stops Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stops (
            stop_id TEXT PRIMARY KEY,
            stop_name TEXT,
            stop_lat REAL,
            stop_lon REAL,
            location_type INTEGER,
            parent_station TEXT
        )
    ''')

    # Transfers Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transfers (
            from_stop_id TEXT,
            to_stop_id TEXT,
            transfer_type INTEGER,
            min_transfer_time INTEGER,
            PRIMARY KEY (from_stop_id, to_stop_id)
        )
    ''')

    # Trips Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS trips (
            trip_id TEXT PRIMARY KEY,
            route_id TEXT,
            service_id TEXT,
            trip_headsign TEXT,
            direction_id TEXT,
            shape_id TEXT,
            FOREIGN KEY (route_id) REFERENCES routes(route_id),
            FOREIGN KEY (service_id) REFERENCES calendar(service_id)
        )
    ''')

    conn.commit()

def import_file(conn, table_name, file_path, columns):
    cursor = conn.cursor()
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        placeholders = ', '.join(['?'] * len(columns))
        sql = f'INSERT OR REPLACE INTO {table_name} ({", ".join(columns)}) VALUES ({placeholders})'
        for row in reader:
            values = [row[column] for column in columns]
            cursor.execute(sql, values)
    conn.commit()

def main():
    conn = connect_db()  
    create_tables(conn)  

    import_file(conn, 'agency', 'static_data/agency.csv', [
        'agency_id', 'agency_name', 'agency_url', 'agency_timezone', 'agency_lang', 'agency_phone'
    ])
    import_file(conn, 'calendar', 'static_data/calendar.csv', [
        'service_id', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'start_date', 'end_date'
    ])
    import_file(conn, 'calendar_dates', 'static_data/calendar_dates.csv', [
        'service_id', 'date', 'exception_type'
    ])
    import_file(conn, 'routes', 'static_data/routes.csv', [
        'agency_id', 'route_id', 'route_short_name', 'route_long_name', 'route_type', 'route_desc', 'route_url', 'route_color', 'route_text_color'
    ])
    import_file(conn, 'shapes', 'static_data/shapes.csv', [
        'shape_id', 'shape_pt_sequence', 'shape_pt_lat', 'shape_pt_lon'
    ])
    import_file(conn, 'stop_times', 'static_data/stop_times.csv', [
        'trip_id', 'stop_id', 'arrival_time', 'departure_time', 'stop_sequence'
    ])
    import_file(conn, 'stops', 'static_data/stops.csv', [
        'stop_id', 'stop_name', 'stop_lat', 'stop_lon', 'location_type', 'parent_station'
    ])
    import_file(conn, 'transfers', 'static_data/transfers.csv', [
        'from_stop_id', 'to_stop_id', 'transfer_type', 'min_transfer_time'
    ])
    import_file(conn, 'trips', 'static_data/trips.csv', [
        'route_id', 'service_id', 'trip_id', 'trip_headsign', 'direction_id', 'shape_id'
    ])

    conn.close()  # 关闭数据库连接

if __name__ == "__main__":
    main()

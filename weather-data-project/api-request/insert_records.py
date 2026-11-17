import psycopg2
from api_request import mock_fetch_data

def connect_to_db():
    print("Connecting to the postgreSQL database...")
    try:
        conn = psycopg2.connect(
            host="db",
            port=5432,
            dbname="db",
            user="db_user",
            password="db_password"
        )
        return conn
    except psycopg2.Error as e:
        print(f"Database connection failed: {e}")
        raise
    
def create_table(conn):
    print("Creating table if not exist...")
    try:
        cursor = conn.cursor()
        cursor.execute("""
            create schema if not exists dev;
            create table if not exists dev.raw_weather_data(
                id serial primary key,
                city text,
                temperature float,
                weather_description text,
                wind_speed float,
                time timestamp,
                insert_at timestamp default now(),
                utc_offset text
            );
            """)
        conn.commit()
        print("Table was creatred.")
    except psycopg2.Error as e:
        print(f"Failed to create table: {e}")
        raise

def insert_records(conn, data):
    print("Inserting weather data into the database...")
    try:
        weather = data['current']
        location = data['location']
        cursor = conn.cursor()
        cursor.execute("""
            insert into dev.raw_weather_data(
                city,
                temperature,
                weather_description,
                wind_speed,
                time,
                insert_at,
                utc_offset
            )values(%s, %s, %s, %s, %s, now(), %s)
                       """,(
                           location['name'],
                           weather['temperature'],
                           weather['weather_descriptions'][0],
                           weather['wind_speed'],
                           location['localtime'],
                           location['utc_offset']
                       ))
        conn.commit()
        print("Data successfully inserted..")
    except psycopg2.Error as e:
        print(f"error inserting data into the database: {e}")
        raise

def main():
    try:
        data = mock_fetch_data()
        conn = connect_to_db()
        create_table(conn)
        insert_records(conn,data)
    except Exception as e:
        print(f"an error occured during execution: {e}")
    finally:
        if 'conn' in locals():
            conn.close()
            print("Database connection closed.")

main()
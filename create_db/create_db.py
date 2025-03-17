from dotenv import load_dotenv
import os
import psycopg2

load_dotenv()

POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_DB = os.getenv('POSTGRES_DB')
POSTGRES_HOST = os.getenv('POSTGRES_HOST')

conn = psycopg2.connect(
    dbname = POSTGRES_DB,
    user = POSTGRES_USER,
    password = POSTGRES_PASSWORD,
    host = POSTGRES_HOST,
    port = "5432"
)

with conn:
    with conn.cursor() as cursor:
        
        cursor.execute("DROP TABLE IF EXISTS passengers")
        cursor.execute("DROP TABLE IF EXISTS bookings")
        
        cursor.execute("CREATE TYPE gender_enum AS ENUM ('male', 'female', 'others')")
        cursor.execute("CREATE TYPE berth_type_enum AS ENUM ('confirmed', 'rac', 'wl')")
        
        cursor.execute(
            """
            CREATE TABLE bookings (
                pnr VARCHAR(8) PRIMARY KEY,
                booked_by VARCHAR(16) NOT NULL,
                source VARCHAR(5) NOT NULL,
                destination VARCHAR(5) NOT NULL,
                travel_date TIMESTAMP NOT NULL,
                is_cancelled BOOLEAN NOT NULL DEFAULT false,
                cancelled_at TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        
        cursor.execute(
            """
            CREATE TABLE passengers (
                id SERIAL PRIMARY KEY,
                pnr VARCHAR(8) references bookings(pnr) ON DELETE CASCADE,
                name VARCHAR(50) NOT NULL,
                age INTEGER CHECK( age > 0 ),
                gender gender_enum NOT NULL,
                gaurdian_id INTEGER references passengers(id),
                berth_type berth_type_enum NOT NULL,
                berth_no VARCHAR(4),
                is_cancelled BOOLEAN DEFAULT false,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        
        cursor.execute(
            """
            CREATE TABLE berth_map (
                id SERIAL PRIMARY KEY,
                berth_type berth_type_enum NOT NULL,
                berth_no VARCHAR(4),
                occupied BOOLEAN DEFAULT false
            )
            """
        )
        
        
        confirmed_seat_map = [("confirmed", f"L{num}") for num in range(1, 33)] + [("confirmed", f"L{num}") for num in range(1, 32)]
        rac_map = [("rac", f"RAC{num}") for num in range(1, 10)]
        wl_map = [("wl", None) for num in range(1, 11)]
        cursor.executemany(
            "INSERT INTO berth_map (berth_type, berth_no) VALUES (%s, %s)",
            confirmed_seat_map + rac_map + wl_map
        )
        

from dotenv import load_dotenv
import os
import psycopg2

load_dotenv()

POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_DB = os.getenv('POSTGRES_DB')
# POSTGRES_URI = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@localhost:5432/{POSTGRES_DB}"

print(POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB)

conn = psycopg2.connect(
    dbname = POSTGRES_DB,
    user = POSTGRES_USER,
    password = POSTGRES_PASSWORD,
    host = "db",
    port = "5432"
)

with conn:
    with conn.cursor() as cursor:
        
        cursor.execute("DROP TABLE IF EXISTS passengers")
        cursor.execute("DROP TABLE IF EXISTS bookings")
        cursor.execute("DROP TABLE IF EXISTS trains")
        
        cursor.execute("CREATE TYPE gender_enum AS ENUM ('Male', 'Female', 'Others')")
        cursor.execute("CREATE TYPE berth_type_enum AS ENUM ('Confirmed', 'RAC', 'WL')")

        cursor.execute(
            """
            CREATE TABLE trains (
                train_no INTEGER PRIMARY KEY,
                confirmed INTEGER NOT NULL,
                rac INTEGER NOT NULL,
                wl INTEGER NOT NULL
            )
            """
        )
        
        cursor.execute(
            """
            INSERT INTO trains (train_no, confirmed, rac, wl) VALUES (22501, 63, 9, 10)
            """
        )
        
        cursor.execute(
            """
            CREATE TABLE bookings (
                train_no INTEGER references trains(train_no) NOT NULL,
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
                berth_type berth_type_enum NOT NULL,
                berth_no VARCHAR(4),
                is_cancelled BOOLEAN DEFAULT false,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )


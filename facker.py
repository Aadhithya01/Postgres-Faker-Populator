import psycopg2
from faker import Faker
import random
import os

fake = Faker()

# Function to create tables
def create_tables():
    try:
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            name TEXT,
            email TEXT PRIMARY KEY,
            address TEXT,
            product TEXT,
            quantity INTEGER,
            price REAL,
            order_date DATE
        )
        ''')
        conn.commit()
        print("Tables created successfully.")
    except Exception as e:
        print(f"Error creating tables: {e}")

# Generate and insert data
def generate_customers(n):
    try:
        for _ in range(n):
            name = fake.name()
            email = fake.email()
            address = fake.address()
            product = fake.word()
            quantity = random.randint(1, 5)
            price = round(random.uniform(10.0, 100.0), 2)
            order_date = fake.date_this_year()

            cursor.execute('''
                INSERT INTO customers (name, email, address, product, quantity, price, order_date)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ''', (name, email, address, product, quantity, price, order_date))
        conn.commit()
        print(f"{n} customers inserted successfully.")
    except Exception as e:
        print(f"Error inserting customers: {e}")

# Connect to PostgreSQL database
try:
    conn = psycopg2.connect(
        dbname=os.getenv("NAME"),  
        user=os.getenv('USER'),         
        password=os.getenv("PASSWORD"),     
        host=os.getenv("HOST"),             
        port=os.getenv("PORT")               
    )
    cursor = conn.cursor()
    print("Connected to the database.")
except Exception as e:
    print(f"Error connecting to the database: {e}")
    exit(1)

# Create the customers table and populate it with data
create_tables()
generate_customers(100)

# Close connection
conn.close()

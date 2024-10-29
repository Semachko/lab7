from faker import Faker
import psycopg2

conn = psycopg2.connect(
    host="db",
    database="supply_department",
    user="user",
    password="pass",
    port="5432",
)
cur = conn.cursor()

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS suppliers (
        supplier_id SERIAL PRIMARY KEY,
        company_name VARCHAR(255) NOT NULL,
        contact_person VARCHAR(255),
        phone VARCHAR(40),
        account_number VARCHAR(50) NOT NULL
    );
"""
)

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS materials (
        material_id SERIAL PRIMARY KEY,
        material_name VARCHAR(255) NOT NULL,
        price NUMERIC(10, 2) NOT NULL CHECK (price > 0)
    );
"""
)

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS deliveries (
        delivery_id SERIAL PRIMARY KEY,
        delivery_date DATE NOT NULL,
        supplier_id INT REFERENCES suppliers(supplier_id),
        material_id INT REFERENCES materials(material_id),
        delivery_days INT NOT NULL CHECK (delivery_days BETWEEN 1 AND 7),
        material_quantity INT NOT NULL CHECK (material_quantity > 0)
    );
"""
)


conn.commit()
cur.close()
conn.close()

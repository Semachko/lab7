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
fake = Faker("uk_UA")

for _ in range(4):
    cur.execute(
        f"""
        INSERT INTO suppliers (company_name, contact_person, phone, account_number)
        VALUES ('{fake.company()}', '{fake.name()}', '{fake.phone_number()}', {fake.bban()});
        """
    )

for material in ("деревина", "лак", "сталеві деталі"):
    cur.execute(
        f"""
        INSERT INTO materials (material_name, price)
        VALUES ('{material}', {round(fake.random_number(digits=3), 2)});
        """
    )

for _ in range(22):
    cur.execute("SELECT supplier_id FROM suppliers ORDER BY RANDOM() LIMIT 1;")
    supplier_id = cur.fetchone()[0]

    cur.execute("SELECT material_id FROM materials ORDER BY RANDOM() LIMIT 1;")
    material_id = cur.fetchone()[0]

    cur.execute(
        """
    INSERT INTO deliveries (delivery_date, supplier_id, material_id, delivery_days, material_quantity)
    VALUES (%s, %s, %s, %s, %s);
    """,
        (
            fake.date_this_year(),
            supplier_id,
            material_id,
            fake.random_int(min=1, max=7),
            fake.random_int(min=1, max=100),
        ),
    )


conn.commit()
cur.close()
conn.close()

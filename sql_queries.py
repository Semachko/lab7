import psycopg2
from prettytable import PrettyTable


queries = [
    """
    SELECT d.*, s.company_name
    FROM deliveries d
    JOIN suppliers s ON d.supplier_id = s.supplier_id
    WHERE d.delivery_days <= 3
    ORDER BY s.company_name;
""",
    """
    SELECT d.*, (m.price * d.material_quantity) AS total_payment
    FROM deliveries d
    JOIN materials m ON d.material_id = m.material_id;
""",
    """
    SELECT d.*, s.company_name
    FROM deliveries d
    JOIN suppliers s ON d.supplier_id = s.supplier_id
    WHERE d.material_id = %s;
""",
    """
    SELECT s.company_name, m.material_name, SUM(d.material_quantity) AS total_quantity
    FROM deliveries d
    JOIN suppliers s ON d.supplier_id = s.supplier_id
    JOIN materials m ON d.material_id = m.material_id
    GROUP BY s.company_name, m.material_name
    ORDER BY s.company_name;
""",
    """
    SELECT m.material_name, SUM(d.material_quantity) AS total_quantity
    FROM deliveries d
    JOIN materials m ON d.material_id = m.material_id
    GROUP BY m.material_name;
""",
    """
    SELECT s.company_name, COUNT(d.delivery_id) AS total_deliveries
    FROM deliveries d
    JOIN suppliers s ON d.supplier_id = s.supplier_id
    GROUP BY s.company_name;
""",
]


def print_table(data, columns):
    table = PrettyTable()
    table.field_names = columns
    for row in data:
        table.add_row(row)
    print(table)


try:
    connection_params = {
        "dbname": "supply_department",
        "user": "user",
        "password": "pass",
        "host": "localhost",
        "port": "5544",
    }
    conn = psycopg2.connect(**connection_params)
    cur = conn.cursor()

    cur.execute(
        "SELECT table_name FROM information_schema.tables WHERE table_schema='public';"
    )
    tables = cur.fetchall()

    for table in tables:
        table_name = table[0]
        cur.execute(f"SELECT * FROM {table_name};")
        data = cur.fetchall()
        columns = [desc[0] for desc in cur.description]

        print(f"\nТаблиця '{table_name}':")
        print_table(data, columns)

    for query in queries:
        print(f"\nЗапит:\n{query.strip()}")
        if "%s" in query:
            cur.execute(query, (1,))
        else:
            cur.execute(query)

        results = cur.fetchall()
        columns = [desc[0] for desc in cur.description]
        print_table(results, columns)

except Exception as e:
    print(f"ERROR: {e}")

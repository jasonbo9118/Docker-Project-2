import psycopg2
import pandas as pd

# Connect to PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    port=5432,
    dbname="shop_db",
    user="admin",
    password="admin"
)

cur = conn.cursor()

# Example: Query users
cur.execute("SELECT * FROM users;")
users = cur.fetchall()
print("Users:")
print(users)

# Example: Query orders and join with users/products
query = """
SELECT o.id, u.name as user_name, p.name as product_name, o.quantity
FROM orders o
JOIN users u ON o.user_id = u.id
JOIN products p ON o.product_id = p.id;
"""
df = pd.read_sql(query, conn)
print("\nOrders DataFrame:")
print(df)

# Example: Clean data (remove orders with quantity = 0)
cur.execute("DELETE FROM orders WHERE quantity = 0;")
conn.commit()

cur.close()
conn.close()
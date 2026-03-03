import psycopg2
import pandas as pd

# --------------------------
# 1️⃣ Connect to PostgreSQL
# --------------------------
conn = psycopg2.connect(
    host="localhost",
    port=5432,
    dbname="shop_db",
    user="admin",
    password="admin"
)
cur = conn.cursor()
print("Connected to PostgreSQL successfully!")

# --------------------------
# 2️⃣ Query existing users
# --------------------------
cur.execute("SELECT * FROM users;")
users = cur.fetchall()
print("\nExisting Users:")
for u in users:
    print(u)

# --------------------------
# 3️⃣ Insert new users
# --------------------------
new_users = [
    ('Charlie', 'charlie@example.com'),
    ('Diana', 'diana@example.com'),
    ('Eve', 'eve@example.com'),
    ('Frank', 'frank@example.com'),
    ('Grace', 'grace@example.com'),
    ('Hannah', 'hannah@example.com'),
    ('Ian', 'ian@example.com')
]

for name, email in new_users:
    cur.execute("INSERT INTO users (name, email) VALUES (%s, %s) ON CONFLICT DO NOTHING;", (name, email))

# --------------------------
# 4️⃣ Insert new products
# --------------------------
new_products = [
    ('Keyboard', 45.00),
    ('Monitor', 220.00),
    ('Webcam', 75.00),
    ('Headphones', 150.25),
    ('USB-C Cable', 10.50),
    ('External Hard Drive', 99.99),
    ('Desk Lamp', 35.00)
]

for name, price in new_products:
    cur.execute("INSERT INTO products (name, price) VALUES (%s, %s) ON CONFLICT DO NOTHING;", (name, price))

# Commit so we can safely query IDs
conn.commit()
print("\nNew users and products added successfully!")

# --------------------------
# 5️⃣ Retrieve IDs for orders
# --------------------------
# Get user IDs
cur.execute("SELECT id, name FROM users;")
user_map = {name: uid for uid, name in cur.fetchall()}

# Get product IDs
cur.execute("SELECT id, name FROM products;")
product_map = {name: pid for pid, name in cur.fetchall()}

# --------------------------
# 6️⃣ Insert orders safely
# --------------------------
orders = [
    ('Charlie', 'Keyboard', 2),
    ('Diana', 'Monitor', 1),
    ('Eve', 'Webcam', 1),
    ('Frank', 'Headphones', 2),
    ('Grace', 'USB-C Cable', 3),
    ('Hannah', 'External Hard Drive', 1),
    ('Ian', 'Desk Lamp', 2)
]

for user_name, product_name, quantity in orders:
    user_id = user_map[user_name]
    product_id = product_map[product_name]
    cur.execute("""
        INSERT INTO orders (user_id, product_id, quantity)
        VALUES (%s, %s, %s);
    """, (user_id, product_id, quantity))

conn.commit()
print("\nOrders added successfully!")

# --------------------------
# 7️⃣ Query orders with joins
# --------------------------
query = """
SELECT o.id, u.name AS user_name, p.name AS product_name, o.quantity
FROM orders o
JOIN users u ON o.user_id = u.id
JOIN products p ON o.product_id = p.id;
"""
df_orders = pd.read_sql(query, conn)
print("\nOrders DataFrame:")
print(df_orders)

# --------------------------
# 8️⃣ Example data cleaning
# --------------------------
# Remove orders with quantity > 2
cur.execute("DELETE FROM orders WHERE quantity > 2;")
conn.commit()
print("\nOrders with quantity > 2 have been removed.")

df_cleaned = pd.read_sql(query, conn)
print("\nCleaned Orders DataFrame:")
print(df_cleaned)

# --------------------------
# 9️⃣ Close connection
# --------------------------
cur.close()
conn.close()
print("\nPostgreSQL connection closed.")
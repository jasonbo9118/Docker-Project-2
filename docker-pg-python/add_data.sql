-- add_data.sql
-- Add new users
INSERT INTO users (name, email) VALUES
('Charlie', 'charlie@example.com'),
('Diana', 'diana@example.com');

-- Add new products
INSERT INTO products (name, price) VALUES
('Keyboard', 45.00),
('Monitor', 220.00);

-- Add new orders
INSERT INTO orders (user_id, product_id, quantity) VALUES
(3, 3, 2),  -- Charlie buys 2 Keyboards
(4, 4, 1);  -- Diana buys 1 Monitor
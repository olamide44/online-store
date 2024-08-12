-- Create Users Table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    email VARCHAR(255) UNIQUE,
    password VARCHAR(255),
    address VARCHAR(255)
);

-- Create Products Table
CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    description TEXT,
    price FLOAT,
    stock INT
);

-- Create Orders Table
CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id),
    total_amount FLOAT,
    date_of_order DATE,
    status VARCHAR(50)
);

-- Create Order Items Table
CREATE TABLE IF NOT EXISTS order_items (
    id SERIAL PRIMARY KEY,
    order_id INT REFERENCES orders(id),
    product_id INT REFERENCES products(id),
    quantity INT,
    price FLOAT
);

-- Insert Users
INSERT INTO users (name, email, password, address)
VALUES
('John Doe', 'john.doe2@example.com', 'password123', '123 Main St, Anytown, Ireland'),
('Jane Smith', 'jane.smith2@example.com', 'password456', '456 Elm St, Anytown, Ireland'),
('Alice Johnson', 'alice.johnson2@example.com', 'password789', '789 Oak St, Anytown, Ireland');

-- Insert Products
INSERT INTO products (name, description, price, stock)
VALUES
('Yoga Mat', 'High-density yoga mat for comfortable workouts.', 25.99, 100),
('Dumbbells Set', 'Adjustable dumbbells set for strength training.', 49.99, 200),
('Treadmill', 'Folding treadmill with LCD display.', 299.99, 50);

-- Insert Orders
INSERT INTO orders (user_id, total_amount, date_of_order, status)
VALUES
(1, 101.97, '2024-01-27', 'Completed'),
(2, 49.99, '2024-04-02', 'Pending'),
(3, 299.99, '2024-06-18', 'Shipped');

-- Insert Order Items
INSERT INTO order_items (order_id, product_id, quantity, price)
VALUES
(1, 1, 2, 25.99),
(1, 2, 1, 49.99),
(2, 2, 1, 49.99),
(3, 3, 1, 299.99);

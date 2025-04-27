-- Create tables
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    description TEXT,
    price DECIMAL(10,2),
    stock INTEGER
);

CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    order_date TIMESTAMP DEFAULT NOW(),
    status VARCHAR(50)
);

CREATE TABLE order_items (
    id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders(id),
    product_id INTEGER REFERENCES products(id),
    quantity INTEGER,
    price DECIMAL(10,2)
);

-- Insert sample data
INSERT INTO users (name, email) VALUES
('Alice Smith', 'alice@example.com'),
('Bob Johnson', 'bob@example.com'),
('Charlie Lee', 'charlie@example.com'),
('Diana Ross', 'diana@example.com'),
('Edward King', 'edward@example.com');

INSERT INTO products (name, description, price, stock) VALUES
('Laptop', 'High-performance laptop', 1200.00, 10),
('Smartphone', 'Latest model smartphone', 800.00, 25),
('Headphones', 'Noise-cancelling headphones', 150.00, 50),
('Camera', 'DSLR camera for photography', 500.00, 15),
('Smartwatch', 'Waterproof smartwatch', 200.00, 30),
('Tablet', 'Lightweight tablet', 300.00, 20),
('Printer', 'Wireless printer', 100.00, 12),
('Monitor', '4K UHD Monitor', 400.00, 8),
('Keyboard', 'Mechanical keyboard', 80.00, 40),
('Mouse', 'Wireless mouse', 40.00, 60);

INSERT INTO orders (user_id, order_date, status) VALUES
(1, NOW(), 'Pending'),
(2, NOW(), 'Shipped'),
(3, NOW(), 'Delivered'),
(4, NOW(), 'Cancelled'),
(5, NOW(), 'Processing');

INSERT INTO order_items (order_id, product_id, quantity, price) VALUES
(1, 1, 1, 1200.00),
(1, 9, 2, 80.00),
(2, 2, 1, 800.00),
(3, 4, 1, 500.00),
(3, 5, 2, 200.00),
(4, 3, 1, 150.00),
(5, 6, 1, 300.00),
(5, 10, 2, 40.00);

# models.py - структуры таблиц

# Таблица пользователей
USERS_TABLE = """
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    surname VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

# Таблица кредитов
CREDIT_TABLE = """
CREATE TABLE IF NOT EXISTS credit (
    id SERIAL PRIMARY KEY,
    amount DECIMAL(10,2) NOT NULL,
    remaining_amount DECIMAL(10,2) NOT NULL,
    user_id INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_payment_date TIMESTAMP,
    status VARCHAR(20) DEFAULT 'active'
);
"""

PAYMENTS_TABLE = """
CREATE TABLE IF NOT EXISTS payments (
    id SERIAL PRIMARY KEY,
    credit_id INTEGER REFERENCES credit(id),
    payment_amount DECIMAL(10,2) NOT NULL,
    payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""


"""
# Список всех таблиц для создания
ALL_TABLES = [
    USERS_TABLE,
    CREDIT_TABLE,
    PAYMENTS_TABLE
]
"""
import psycopg2
from psycopg2 import OperationalError
import os
from dotenv import load_dotenv
# from DbConfig.tables.tableModels import USERS_TABLE, CREDIT_TABLE, PAYMENTS_TABLE
load_dotenv()

def create_connection():
    try:
        connection = psycopg2.connect(
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT'),
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD')
        )
        print("✅ Подключение к PostgreSQL успешно установлено")
        return connection
    except OperationalError as e:
        print(f"❌ Ошибка подключения: {e}")
        return None

if __name__ == "__main__":
    create_connection()
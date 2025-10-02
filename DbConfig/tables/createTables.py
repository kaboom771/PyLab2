import sys
import os
# Добавляем корневую директорию проекта в путь Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from DbConfig.databaseCn import create_connection
from tableModels import USERS_TABLE, CREDIT_TABLE, PAYMENTS_TABLE

def createTablesFunc():
    conn = create_connection()
    if conn is None:
        return  
    try:
        cursor = conn.cursor()

        # Создание таблицы users
        cursor.execute(USERS_TABLE)
        # Создание таблицы credit
        cursor.execute(CREDIT_TABLE)
        # Создание таблицы Payments
        cursor.execute(PAYMENTS_TABLE)

        conn.commit()
        print("✅ Таблицы созданы успешно")     
    except Exception as e:
        print(f"❌ Ошибка создания таблиц: {e}")
    finally:
        if conn:
            conn.close()

createTablesFunc()

if __name__ == "__main__":
    createTablesFunc()
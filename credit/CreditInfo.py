from DbConfig.databaseCn import create_connection

def get_credit_info(credit_id):
    """Получает информацию о кредите"""
    conn = create_connection()
    if not conn:
        return None
    
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT c.*, u.name, u.surname 
            FROM credit c 
            JOIN users u ON c.user_id = u.id 
            WHERE c.id = %s
        """, (credit_id,))
        credit_info = cursor.fetchone()
        return credit_info
    except Exception as e:
        print(f"❌ Ошибка получения информации о кредите: {e}")
        return None
    finally:
        conn.close()

def get_payment_history(credit_id):
    """Получает историю платежей по кредиту"""
    conn = create_connection()
    if not conn:
        return []
    
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM payments 
            WHERE credit_id = %s 
            ORDER BY payment_date DESC
        """, (credit_id,))
        payments = cursor.fetchall()
        return payments
    except Exception as e:
        print(f"❌ Ошибка получения истории платежей: {e}")
        return []
    finally:
        conn.close()
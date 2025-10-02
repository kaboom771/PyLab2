import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from DbConfig.databaseCn import create_connection

class DatabaseService:
    def get_all_users(self):
        """Получить всех пользователей"""
        conn = create_connection()
        if not conn:
            return []
        
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, surname FROM users ORDER BY id")
            return cursor.fetchall()
        except Exception as e:
            print(f"❌ Ошибка получения пользователей: {e}")
            return []
        finally:
            conn.close()
    
    def get_user_credits(self, user_id):
        """Получить кредиты пользователя"""
        conn = create_connection()
        if not conn:
            return []
        
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, amount, remaining_amount, status 
                FROM credit 
                WHERE user_id = %s AND status = 'active'
                ORDER BY id
            """, (user_id,))
            return cursor.fetchall()
        except Exception as e:
            print(f"❌ Ошибка получения кредитов: {e}")
            return []
        finally:
            conn.close()
    
    def make_payment(self, credit_id, amount):
        """Внести платеж по кредиту"""
        conn = create_connection()
        if not conn:
            return False, "Ошибка подключения"
        
        try:
            cursor = conn.cursor()
            
            # Получаем текущий остаток
            cursor.execute("SELECT remaining_amount FROM credit WHERE id = %s", (credit_id,))
            result = cursor.fetchone()
            
            if not result:
                return False, "Кредит не найден"
            
            remaining = result[0]
            
            if amount <= 0:
                return False, "Сумма платежа должна быть положительной"
            
            if amount > remaining:
                return False, f"Сумма платежа превышает остаток долга ({remaining:.2f})"
            
            # Вносим платеж
            cursor.execute("""
                INSERT INTO payments (credit_id, payment_amount) 
                VALUES (%s, %s)
            """, (credit_id, amount))
            
            # Обновляем остаток
            cursor.execute("""
                UPDATE credit 
                SET remaining_amount = remaining_amount - %s,
                    last_payment_date = CURRENT_TIMESTAMP
                WHERE id = %s
            """, (amount, credit_id))
            
            # Проверяем полное погашение
            cursor.execute("SELECT remaining_amount FROM credit WHERE id = %s", (credit_id,))
            new_remaining = cursor.fetchone()[0]
            
            if new_remaining <= 0:
                cursor.execute("UPDATE credit SET status = 'paid' WHERE id = %s", (credit_id,))
            
            conn.commit()
            return True, f"✅ Платеж {amount:.2f} успешно внесен!"
            
        except Exception as e:
            conn.rollback()
            return False, f"❌ Ошибка платежа: {e}"
        finally:
            conn.close()
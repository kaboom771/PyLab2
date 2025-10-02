import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from DbConfig.database_service import DatabaseService

class BankingCore:
    def __init__(self):
        self.db = DatabaseService()
        self.current_user = None
        self.current_credit = None
    
    def select_user(self):
        """Выбор пользователя"""
        users = self.db.get_all_users()
        if not users:
            print("❌ Нет пользователей в базе")
            return
        
        print("\n👥 ВЫБЕРИТЕ ПОЛЬЗОВАТЕЛЯ:")
        for i, (user_id, name, surname) in enumerate(users, 1):
            print(f"{i}. {name} {surname} (ID: {user_id})")
        print("0. ↩️ Назад")
        
        try:
            choice = int(input("\nВыберите номер: "))
            if choice == 0:
                return
            if 1 <= choice <= len(users):
                self.current_user = users[choice - 1]
                self.current_credit = None  # Сбрасываем выбранный кредит
                print(f"✅ Выбран пользователь: {self.current_user[1]} {self.current_user[2]}")
            else:
                print("❌ Неверный выбор")
        except ValueError:
            print("❌ Введите число")
    
    def select_credit(self):
        """Выбор кредита"""
        if not self.current_user:
            print("❌ Сначала выберите пользователя")
            return
        
        credits = self.db.get_user_credits(self.current_user[0])
        if not credits:
            print(f"❌ У пользователя {self.current_user[1]} нет активных кредитов")
            return
        
        print(f"\n💳 КРЕДИТЫ {self.current_user[1]} {self.current_user[2]}:")
        for i, (credit_id, amount, remaining, status) in enumerate(credits, 1):
            print(f"{i}. Кредит #{credit_id}: {amount:.2f} ₽ (остаток: {remaining:.2f} ₽)")
        print("0. ↩️ Назад")
        
        try:
            choice = int(input("\nВыберите номер кредита: "))
            if choice == 0:
                return
            if 1 <= choice <= len(credits):
                self.current_credit = credits[choice - 1]
                print(f"✅ Выбран кредит #{self.current_credit[0]}")
            else:
                print("❌ Неверный выбор")
        except ValueError:
            print("❌ Введите число")
    
    def make_payment_menu(self):
        """Меню внесения платежа"""
        if not self.current_credit:
            print("❌ Сначала выберите кредит")
            return
        
        credit_id, amount, remaining, status = self.current_credit
        
        print(f"\n💰 ВНЕСЕНИЕ ПЛАТЕЖА:")
        print(f"Кредит #{credit_id}")
        print(f"Сумма кредита: {amount:.2f} ₽")
        print(f"Остаток долга: {remaining:.2f} ₽")
        
        try:
            payment_amount = float(input("\nВведите сумму платежа: "))
            success, message = self.db.make_payment(credit_id, payment_amount)
            print(message)
            
            if success:
                # Обновляем информацию о кредите
                credits = self.db.get_user_credits(self.current_user[0])
                for credit in credits:
                    if credit[0] == credit_id:
                        self.current_credit = credit
                        break
                
                # Если кредит погашен, сбрасываем выбор
                if self.current_credit[2] <= 0:
                    print("🎉 Кредит полностью погашен!")
                    self.current_credit = None
                    
        except ValueError:
            print("❌ Введите корректную сумму")
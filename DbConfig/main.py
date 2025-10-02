import signal
import sys
import os
import sys

# Добавляем корневую директорию в путь для импортов
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from credit.CreditClass import BankingCore




class BankingApp:
    def __init__(self):
        self.running = True
        self.core = BankingCore()
        
    def shutdown_handler(self, signum, frame):
        """Обработчик сигнала завершения"""
        print("\n\n🛑 Получен сигнал завершения...")
        self.running = False
        sys.exit(0)
    
    def display_main_menu(self):
        """Главное меню"""
        print("\n" + "="*50)
        print("🏦 БАНКОВСКАЯ СИСТЕМА")
        print("="*50)
        print("1. 👥 Выбрать пользователя")
        if self.core.current_user:
            print("2. 💳 Выбрать кредит")
        if self.core.current_credit:
            print("3. 💰 Внести платеж")
        print("0. ❌ Выход")
        print("="*50)
    
    def run(self):
        """Запуск основного цикла"""
        # Настройка обработчика сигналов
        signal.signal(signal.SIGINT, self.shutdown_handler)
        signal.signal(signal.SIGTERM, self.shutdown_handler)
        
        print("🚀 Банковская система запущена")
        print("💡 Для выхода нажмите Ctrl+C")
        
        while self.running:
            try:
                self.display_main_menu()
                
                choice = input("Выберите действие: ").strip()
                
                if choice == "1":
                    self.core.select_user()
                elif choice == "2" and self.core.current_user:
                    self.core.select_credit()
                elif choice == "3" and self.core.current_credit:
                    self.core.make_payment_menu()
                elif choice == "0":
                    print("👋 До свидания!")
                    break
                else:
                    print("❌ Неверный выбор или действие недоступно")
                    
            except KeyboardInterrupt:
                print("\n\n🛑 Завершение работы...")
                break
            except Exception as e:
                print(f"❌ Произошла ошибка: {e}")

def main():
    app = BankingApp()
    app.run()

if __name__ == "__main__":
    main()
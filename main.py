import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont
from database import db
from ui.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    app.setFont(QFont("Constantia", 10))
    
    try:
        db.connect()  # Явное подключение к БД
        window = MainWindow()
        window.show()
        ret = app.exec_()
    except Exception as e:
        print(f"Application error: {e}")
        ret = 1
    finally:
        db.close()  # Закрытие соединения при выходе
    
    sys.exit(ret)

if __name__ == "__main__":
    main()
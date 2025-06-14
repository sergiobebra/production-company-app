from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QPushButton, QTableWidget, QTableWidgetItem, 
                            QComboBox, QDateEdit, QMessageBox, QHeaderView)
from PyQt5.QtCore import Qt, QDate
from database import db 
class ProductionTab(QWidget):
    def __init__(self):
        super().__init__()
        self.orders_data = []
        self.initUI()
    
    def initUI(self):
        main_layout = QVBoxLayout()
        
        # Форма управления производством
        form_layout = QVBoxLayout()
        
        # Фильтры
        filter_layout = QHBoxLayout()
        filter_label = QLabel("Фильтр:")
        self.filter_combo = QComboBox()
        self.filter_combo.addItems(["Все заказы", "В производстве", "Готовые", "Просроченные"])
        filter_layout.addWidget(filter_label)
        filter_layout.addWidget(self.filter_combo)
        
        # Кнопки управления
        buttons_layout = QHBoxLayout()
        self.start_button = QPushButton("Запустить в производство")
        self.complete_button = QPushButton("Завершить производство")
        self.delay_button = QPushButton("Отметить задержку")
        buttons_layout.addWidget(self.start_button)
        buttons_layout.addWidget(self.complete_button)
        buttons_layout.addWidget(self.delay_button)
        
        # Таблица производственных заказов
        self.orders_table = QTableWidget()
        self.orders_table.setColumnCount(6)
        self.orders_table.setHorizontalHeaderLabels([
            "ID", "Продукция", "Количество", "Срок", "Статус", "Цех"
        ])
        self.orders_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.orders_table.setSelectionBehavior(QTableWidget.SelectRows)
        
        form_layout.addLayout(filter_layout)
        form_layout.addLayout(buttons_layout)
        main_layout.addLayout(form_layout)
        main_layout.addWidget(self.orders_table)
        
        self.setLayout(main_layout)
        
        # Подключаем сигналы
        self.filter_combo.currentTextChanged.connect(self.filter_orders)
        self.start_button.clicked.connect(self.start_production)
        self.complete_button.clicked.connect(self.complete_production)
        self.delay_button.clicked.connect(self.mark_delay)
        
        # Загрузка тестовых данных
        self.load_test_data()
    
    def load_test_data(self):
        self.orders_data = [
            ["1001", "Стол офисный", "5", "15.06.2023", "В ожидании", "Цех 1"],
            ["1002", "Стул офисный", "10", "10.06.2023", "В производстве", "Цех 2"],
            ["1003", "Шкаф для документов", "3", "20.06.2023", "Готов", "Цех 1"]
        ]
        self.update_orders_table()
    
    def update_orders_table(self, data=None):
        self.orders_table.setRowCount(0)
        data = data or self.orders_data
        for row_data in data:
            row = self.orders_table.rowCount()
            self.orders_table.insertRow(row)
            for col, value in enumerate(row_data):
                item = QTableWidgetItem(value)
                item.setFlags(item.flags() ^ Qt.ItemIsEditable)
                self.orders_table.setItem(row, col, item)
    
    def filter_orders(self):
        filter_text = self.filter_combo.currentText()
        if filter_text == "Все заказы":
            self.update_orders_table()
        else:
            filtered = [order for order in self.orders_data if filter_text in order[4]]
            self.update_orders_table(filtered)
    
    def start_production(self):
        selected_row = self.orders_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите заказ")
            return
        
        if self.orders_data[selected_row][4] != "В ожидании":
            QMessageBox.warning(self, "Ошибка", "Можно запускать только заказы в статусе 'В ожидании'")
            return
        
        self.orders_data[selected_row][4] = "В производстве"
        self.update_orders_table()
        QMessageBox.information(self, "Успех", "Заказ запущен в производство")
    
    def complete_production(self):
        selected_row = self.orders_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите заказ")
            return
        
        if self.orders_data[selected_row][4] != "В производстве":
            QMessageBox.warning(self, "Ошибка", "Можно завершать только заказы в статусе 'В производстве'")
            return
        
        self.orders_data[selected_row][4] = "Готов"
        self.update_orders_table()
        QMessageBox.information(self, "Успех", "Производство заказа завершено")
    
    def mark_delay(self):
        selected_row = self.orders_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите заказ")
            return
        
        self.orders_data[selected_row][4] = "Просрочен"
        self.update_orders_table()
        QMessageBox.information(self, "Информация", "Заказ отмечен как просроченный")
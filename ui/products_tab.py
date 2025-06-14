from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QLineEdit, QPushButton, QTableWidget, 
                            QTableWidgetItem, QComboBox, QSpinBox, 
                            QDoubleSpinBox, QMessageBox, QHeaderView)
from PyQt5.QtCore import Qt
from database import db 
class ProductsTab(QWidget):
    def __init__(self):
        super().__init__()
        self.products_data = []
        
        self.initUI()
        self.load_products()
    
    def initUI(self):
        main_layout = QVBoxLayout()
        
        # Форма добавления/редактирования продукции
        form_layout = QVBoxLayout()
        
        # Артикул
        article_layout = QHBoxLayout()
        article_label = QLabel("Артикул:")
        self.article_edit = QLineEdit()
        article_layout.addWidget(article_label)
        article_layout.addWidget(self.article_edit)
        
        # Тип продукции
        type_layout = QHBoxLayout()
        type_label = QLabel("Тип продукции:")
        self.type_combo = QComboBox()
        self.type_combo.addItems(["Стол", "Стул", "Шкаф", "Полка", "Тумба"])
        type_layout.addWidget(type_label)
        type_layout.addWidget(self.type_combo)
        
        # Наименование
        name_layout = QHBoxLayout()
        name_label = QLabel("Наименование:")
        self.name_edit = QLineEdit()
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_edit)
        
        # Описание
        description_layout = QHBoxLayout()
        description_label = QLabel("Описание:")
        self.description_edit = QLineEdit()
        description_layout.addWidget(description_label)
        description_layout.addWidget(self.description_edit)
        
        # Минимальная стоимость
        price_layout = QHBoxLayout()
        price_label = QLabel("Мин. стоимость:")
        self.price_edit = QDoubleSpinBox()
        self.price_edit.setRange(0, 1000000)
        self.price_edit.setPrefix("₽ ")
        price_layout.addWidget(price_label)
        price_layout.addWidget(self.price_edit)
        
        # Габариты
        dimensions_layout = QHBoxLayout()
        dimensions_label = QLabel("Размеры (Д×Ш×В):")
        self.length_edit = QSpinBox()
        self.length_edit.setRange(0, 1000)
        self.length_edit.setSuffix(" см")
        self.width_edit = QSpinBox()
        self.width_edit.setRange(0, 1000)
        self.width_edit.setSuffix(" см")
        self.height_edit = QSpinBox()
        self.height_edit.setRange(0, 1000)
        self.height_edit.setSuffix(" см")
        dimensions_layout.addWidget(dimensions_label)
        dimensions_layout.addWidget(self.length_edit)
        dimensions_layout.addWidget(self.width_edit)
        dimensions_layout.addWidget(self.height_edit)
        
        # Вес
        weight_layout = QHBoxLayout()
        weight_label = QLabel("Вес:")
        self.weight_edit = QSpinBox()
        self.weight_edit.setRange(0, 1000)
        self.weight_edit.setSuffix(" кг")
        weight_layout.addWidget(weight_label)
        weight_layout.addWidget(self.weight_edit)
        
        # Кнопки управления
        buttons_layout = QHBoxLayout()
        self.add_button = QPushButton("Добавить")
        self.edit_button = QPushButton("Редактировать")
        self.delete_button = QPushButton("Удалить")
        self.clear_button = QPushButton("Очистить")
        buttons_layout.addWidget(self.add_button)
        buttons_layout.addWidget(self.edit_button)
        buttons_layout.addWidget(self.delete_button)
        buttons_layout.addWidget(self.clear_button)
        
        # Добавляем все в форму
        form_layout.addLayout(article_layout)
        form_layout.addLayout(type_layout)
        form_layout.addLayout(name_layout)
        form_layout.addLayout(description_layout)
        form_layout.addLayout(price_layout)
        form_layout.addLayout(dimensions_layout)
        form_layout.addLayout(weight_layout)
        form_layout.addLayout(buttons_layout)
        
        # Таблица продукции
        self.products_table = QTableWidget()
        self.products_table.setColumnCount(8)
        self.products_table.setHorizontalHeaderLabels([
            "Артикул", "Тип", "Наименование", "Описание", "Стоимость", "Размеры", "Вес", "Время изготовления"
        ])
        self.products_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.products_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.products_table.setSelectionMode(QTableWidget.SingleSelection)
        
        main_layout.addLayout(form_layout)
        main_layout.addWidget(self.products_table)
        
        self.setLayout(main_layout)
        
        # Подключаем сигналы
        self.add_button.clicked.connect(self.add_product)
        self.edit_button.clicked.connect(self.edit_product)
        self.delete_button.clicked.connect(self.delete_product)
        self.clear_button.clicked.connect(self.clear_form)
        self.products_table.itemSelectionChanged.connect(self.load_product_data)
        
        # Загрузка тестовых данных
        self.load_test_data()
    
    def load_test_data(self):
        test_data = [
            ["STL-001", "Стол", "Стол офисный", "Деревянный стол с металлическими ножками", "12000", "120×80×75", "15", "2 дня"],
            ["STL-002", "Стул", "Стул офисный", "Эргономичный офисный стул", "4500", "50×50×90", "5", "1 день"],
        ]
        
        for data in test_data:
            self.products_data.append(data)
            row = self.products_table.rowCount()
            self.products_table.insertRow(row)
            for col, value in enumerate(data):
                item = QTableWidgetItem(value)
                item.setFlags(item.flags() ^ Qt.ItemIsEditable)
                self.products_table.setItem(row, col, item)
    
    def add_product(self):
        if not self.article_edit.text() or not self.name_edit.text():
            QMessageBox.warning(self, "Ошибка", "Заполните обязательные поля: Артикул и Наименование")
            return
        
        try:
            with db.conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO products 
                    (article, type, name, description, price, 
                     length, width, height, weight, production_time)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    self.article_edit.text(),
                    self.type_combo.currentText(),
                    self.name_edit.text(),
                    self.description_edit.text(),
                    self.price_edit.value(),
                    self.length_edit.value(),
                    self.width_edit.value(),
                    self.height_edit.value(),
                    self.weight_edit.value(),
                    "1 день"  # Значение по умолчанию
                ))
                db.conn.commit()
                self.load_products()
                self.clear_form()
                QMessageBox.information(self, "Успех", "Продукция добавлена")
        except Exception as e:
            db.conn.rollback()
            QMessageBox.critical(self, "Ошибка", f"Не удалось добавить продукцию: {e}")

    def load_products(self):
        try:
            with db.conn.cursor() as cur:
                cur.execute("""
                    SELECT article, type, name, description, price, 
                           length, width, height, weight, production_time 
                    FROM products
                """)
                self.products_data = cur.fetchall()
                self.update_products_table()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить продукцию: {e}")

    def update_products_table(self):
        self.products_table.setRowCount(0)
        for product in self.products_data:
            row = self.products_table.rowCount()
            self.products_table.insertRow(row)
            
            # Преобразуем размеры в строку
            dimensions = f"{product[5]}×{product[6]}×{product[7]}"
            
            # Подготавливаем данные для таблицы
            table_data = [
                product[0],  # Артикул
                product[1],  # Тип
                product[2],  # Наименование
                product[3],  # Описание
                f"{product[4]:.2f}",  # Цена
                dimensions,  # Размеры
                f"{product[8]} кг",  # Вес
                product[9]   # Время изготовления
            ]
            
            for col, data in enumerate(table_data):
                item = QTableWidgetItem(str(data))
                item.setFlags(item.flags() ^ Qt.ItemIsEditable)
                self.products_table.setItem(row, col, item)

    def edit_product(self):
        selected_row = self.products_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите продукцию для редактирования")
            return
        
        # Проверка заполнения обязательных полей
        if not self.article_edit.text() or not self.name_edit.text():
            QMessageBox.warning(self, "Ошибка", "Заполните обязательные поля: Артикул и Наименование")
            return
        
        dimensions = f"{self.length_edit.value()}×{self.width_edit.value()}×{self.height_edit.value()}"
        
        product_data = [
            self.article_edit.text(),
            self.type_combo.currentText(),
            self.name_edit.text(),
            self.description_edit.text(),
            f"{self.price_edit.value():.2f}",
            dimensions,
            f"{self.weight_edit.value()}",
            self.products_table.item(selected_row, 7).text()  # Сохраняем время изготовления
        ]
        
        self.products_data[selected_row] = product_data
        
        for col, value in enumerate(product_data):
            item = QTableWidgetItem(value)
            item.setFlags(item.flags() ^ Qt.ItemIsEditable)
            self.products_table.setItem(selected_row, col, item)
        
        QMessageBox.information(self, "Успех", "Данные продукции успешно обновлены")
    
    def delete_product(self):
        selected_row = self.products_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите продукцию для удаления")
            return
        
        reply = QMessageBox.question(
            self, 
            "Подтверждение", 
            f"Вы уверены, что хотите удалить продукцию {self.products_table.item(selected_row, 2).text()}?", 
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.products_table.removeRow(selected_row)
            self.products_data.pop(selected_row)
            self.clear_form()
    
    def load_product_data(self):
        selected_row = self.products_table.currentRow()
        if selected_row >= 0:
            product_data = self.products_data[selected_row]
            
            self.article_edit.setText(product_data[0])
            self.type_combo.setCurrentText(product_data[1])
            self.name_edit.setText(product_data[2])
            self.description_edit.setText(product_data[3])
            self.price_edit.setValue(float(product_data[4]))
            
            # Парсим размеры
            dimensions = product_data[5].split("×")
            if len(dimensions) == 3:
                self.length_edit.setValue(int(dimensions[0]))
                self.width_edit.setValue(int(dimensions[1]))
                self.height_edit.setValue(int(dimensions[2]))
            
            # Парсим вес (удаляем " кг" если есть)
            weight = product_data[6].replace(" кг", "")
            self.weight_edit.setValue(int(weight))
    
    def clear_form(self):
        self.article_edit.clear()
        self.type_combo.setCurrentIndex(0)
        self.name_edit.clear()
        self.description_edit.clear()
        self.price_edit.setValue(0)
        self.length_edit.setValue(0)
        self.width_edit.setValue(0)
        self.height_edit.setValue(0)
        self.weight_edit.setValue(0)
        self.products_table.clearSelection()
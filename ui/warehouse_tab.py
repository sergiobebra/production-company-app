from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QLineEdit, QPushButton, QTableWidget, 
                            QTableWidgetItem, QComboBox, QSpinBox, 
                            QMessageBox, QHeaderView, QTabWidget)
from PyQt5.QtCore import Qt
from database import db 
class WarehouseTab(QWidget):
    def __init__(self):
        super().__init__()
        self.materials_data = []
        self.products_data = []
        self.initUI()
    
    def initUI(self):
        main_layout = QVBoxLayout()
        
        # Создаем вкладки для склада
        self.tabs = QTabWidget()
        
        # Вкладка материалов
        self.materials_tab = QWidget()
        self.setup_materials_tab()
        
        # Вкладка готовой продукции
        self.products_tab = QWidget()
        self.setup_products_tab()
        
        self.tabs.addTab(self.materials_tab, "Материалы")
        self.tabs.addTab(self.products_tab, "Готовая продукция")
        
        main_layout.addWidget(self.tabs)
        self.setLayout(main_layout)
        
        # Загрузка тестовых данных
        self.load_test_data()
    
    def setup_materials_tab(self):
        layout = QVBoxLayout()
        
        # Форма добавления/редактирования материалов
        form_layout = QVBoxLayout()
        
        # Тип материала
        type_layout = QHBoxLayout()
        type_label = QLabel("Тип материала:")
        self.material_type_combo = QComboBox()
        self.material_type_combo.addItems(["Дерево", "Металл", "Пластик", "Ткань", "Фурнитура"])
        type_layout.addWidget(type_label)
        type_layout.addWidget(self.material_type_combo)
        
        # Наименование
        name_layout = QHBoxLayout()
        name_label = QLabel("Наименование:")
        self.material_name_edit = QLineEdit()
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.material_name_edit)
        
        # Единица измерения
        unit_layout = QHBoxLayout()
        unit_label = QLabel("Единица измерения:")
        self.material_unit_combo = QComboBox()
        self.material_unit_combo.addItems(["шт", "кг", "м", "м²", "л"])
        unit_layout.addWidget(unit_label)
        unit_layout.addWidget(self.material_unit_combo)
        
        # Количество
        quantity_layout = QHBoxLayout()
        quantity_label = QLabel("Количество:")
        self.material_quantity_edit = QSpinBox()
        self.material_quantity_edit.setRange(0, 100000)
        quantity_layout.addWidget(quantity_label)
        quantity_layout.addWidget(self.material_quantity_edit)
        
        # Минимальный запас
        min_layout = QHBoxLayout()
        min_label = QLabel("Мин. запас:")
        self.material_min_edit = QSpinBox()
        self.material_min_edit.setRange(0, 100000)
        min_layout.addWidget(min_label)
        min_layout.addWidget(self.material_min_edit)
        
        # Кнопки управления
        buttons_layout = QHBoxLayout()
        self.material_add_button = QPushButton("Добавить")
        self.material_edit_button = QPushButton("Редактировать")
        self.material_delete_button = QPushButton("Удалить")
        self.material_clear_button = QPushButton("Очистить")
        buttons_layout.addWidget(self.material_add_button)
        buttons_layout.addWidget(self.material_edit_button)
        buttons_layout.addWidget(self.material_delete_button)
        buttons_layout.addWidget(self.material_clear_button)
        
        # Добавляем все в форму
        form_layout.addLayout(type_layout)
        form_layout.addLayout(name_layout)
        form_layout.addLayout(unit_layout)
        form_layout.addLayout(quantity_layout)
        form_layout.addLayout(min_layout)
        form_layout.addLayout(buttons_layout)
        
        # Таблица материалов
        self.materials_table = QTableWidget()
        self.materials_table.setColumnCount(6)
        self.materials_table.setHorizontalHeaderLabels([
            "Тип", "Наименование", "Ед. изм.", "Количество", "Мин. запас", "Статус"
        ])
        self.materials_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.materials_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.materials_table.setSelectionMode(QTableWidget.SingleSelection)
        
        layout.addLayout(form_layout)
        layout.addWidget(self.materials_table)
        
        self.materials_tab.setLayout(layout)
        
        # Подключаем сигналы
        self.material_add_button.clicked.connect(self.add_material)
        self.material_edit_button.clicked.connect(self.edit_material)
        self.material_delete_button.clicked.connect(self.delete_material)
        self.material_clear_button.clicked.connect(self.clear_material_form)
        self.materials_table.itemSelectionChanged.connect(self.load_material_data)
    
    def setup_products_tab(self):
        layout = QVBoxLayout()
        
        # Форма работы с готовой продукцией
        form_layout = QVBoxLayout()
        
        # Поиск продукции
        search_layout = QHBoxLayout()
        search_label = QLabel("Поиск:")
        self.product_search_edit = QLineEdit()
        self.product_search_button = QPushButton("Найти")
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.product_search_edit)
        search_layout.addWidget(self.product_search_button)
        
        # Кнопки управления
        buttons_layout = QHBoxLayout()
        self.product_in_button = QPushButton("Приход")
        self.product_out_button = QPushButton("Расход")
        self.product_move_button = QPushButton("Перемещение")
        buttons_layout.addWidget(self.product_in_button)
        buttons_layout.addWidget(self.product_out_button)
        buttons_layout.addWidget(self.product_move_button)
        
        # Добавляем в форму
        form_layout.addLayout(search_layout)
        form_layout.addLayout(buttons_layout)
        
        # Таблица готовой продукции
        self.products_table = QTableWidget()
        self.products_table.setColumnCount(5)
        self.products_table.setHorizontalHeaderLabels([
            "Артикул", "Наименование", "Количество", "Место хранения", "Статус"
        ])
        self.products_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.products_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.products_table.setSelectionMode(QTableWidget.SingleSelection)
        
        layout.addLayout(form_layout)
        layout.addWidget(self.products_table)
        
        self.products_tab.setLayout(layout)
        
        # Подключаем сигналы
        self.product_search_button.clicked.connect(self.search_product)
        self.product_in_button.clicked.connect(self.product_in)
        self.product_out_button.clicked.connect(self.product_out)
        self.product_move_button.clicked.connect(self.product_move)
    
    def load_test_data(self):
        # Тестовые данные для материалов
        materials_test_data = [
            ["Дерево", "Доска сосновая", "шт", "150", "50", "Достаточно"],
            ["Металл", "Труба стальная", "м", "75", "30", "Достаточно"],
            ["Фурнитура", "Ручка для шкафа", "шт", "320", "100", "Достаточно"],
        ]
        
        for data in materials_test_data:
            self.materials_data.append(data)
            row = self.materials_table.rowCount()
            self.materials_table.insertRow(row)
            for col, value in enumerate(data):
                item = QTableWidgetItem(value)
                item.setFlags(item.flags() ^ Qt.ItemIsEditable)
                self.materials_table.setItem(row, col, item)
        
        # Тестовые данные для готовой продукции
        products_test_data = [
            ["STL-001", "Стол офисный", "12", "Секция A", "Готов"],
            ["STL-002", "Стул офисный", "24", "Секция B", "Готов"],
        ]
        
        for data in products_test_data:
            self.products_data.append(data)
            row = self.products_table.rowCount()
            self.products_table.insertRow(row)
            for col, value in enumerate(data):
                item = QTableWidgetItem(value)
                item.setFlags(item.flags() ^ Qt.ItemIsEditable)
                self.products_table.setItem(row, col, item)
    
    def add_material(self):
        if not self.material_name_edit.text():
            QMessageBox.warning(self, "Ошибка", "Заполните обязательное поле: Наименование")
            return
        
        if self.material_min_edit.value() > self.material_quantity_edit.value():
            QMessageBox.warning(self, "Ошибка", "Минимальный запас не может быть больше текущего количества")
            return
        
        status = "Достаточно" if self.material_quantity_edit.value() >= self.material_min_edit.value() else "Недостаточно"
        
        material_data = [
            self.material_type_combo.currentText(),
            self.material_name_edit.text(),
            self.material_unit_combo.currentText(),
            str(self.material_quantity_edit.value()),
            str(self.material_min_edit.value()),
            status
        ]
        
        self.materials_data.append(material_data)
        self.update_materials_table()
        self.clear_material_form()
        QMessageBox.information(self, "Успех", "Материал успешно добавлен")
    
    def edit_material(self):
        selected_row = self.materials_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите материал для редактирования")
            return
        
        if not self.material_name_edit.text():
            QMessageBox.warning(self, "Ошибка", "Заполните обязательное поле: Наименование")
            return
        
        status = "Достаточно" if self.material_quantity_edit.value() >= self.material_min_edit.value() else "Недостаточно"
        
        self.materials_data[selected_row] = [
            self.material_type_combo.currentText(),
            self.material_name_edit.text(),
            self.material_unit_combo.currentText(),
            str(self.material_quantity_edit.value()),
            str(self.material_min_edit.value()),
            status
        ]
        
        self.update_materials_table()
        QMessageBox.information(self, "Успех", "Данные материала обновлены")
    
    def delete_material(self):
        selected_row = self.materials_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите материал для удаления")
            return
        
        reply = QMessageBox.question(
            self, "Подтверждение", 
            f"Удалить материал {self.materials_data[selected_row][1]}?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.materials_data.pop(selected_row)
            self.update_materials_table()
            self.clear_material_form()
    
    def update_materials_table(self):
        self.materials_table.setRowCount(0)
        for data in self.materials_data:
            row = self.materials_table.rowCount()
            self.materials_table.insertRow(row)
            for col, value in enumerate(data):
                item = QTableWidgetItem(value)
                item.setFlags(item.flags() ^ Qt.ItemIsEditable)
                self.materials_table.setItem(row, col, item)
    
    def clear_material_form(self):
        self.material_name_edit.clear()
        self.material_quantity_edit.setValue(0)
        self.material_min_edit.setValue(0)
        self.materials_table.clearSelection()
    
    def search_product(self):
        search_text = self.product_search_edit.text().lower()
        if not search_text:
            self.update_products_table()
            return
        
        filtered_data = [
            data for data in self.products_data 
            if search_text in data[0].lower() or search_text in data[1].lower()
        ]
        
        self.products_table.setRowCount(0)
        for data in filtered_data:
            row = self.products_table.rowCount()
            self.products_table.insertRow(row)
            for col, value in enumerate(data):
                item = QTableWidgetItem(value)
                item.setFlags(item.flags() ^ Qt.ItemIsEditable)
                self.products_table.setItem(row, col, item)
    
    def product_in(self):
        QMessageBox.information(self, "Информация", "Функция прихода продукции в разработке")
    
    def product_out(self):
        QMessageBox.information(self, "Информация", "Функция расхода продукции в разработке")
    
    def product_move(self):
        QMessageBox.information(self, "Информация", "Функция перемещения продукции в разработке")
    
    def update_products_table(self):
        self.products_table.setRowCount(0)
        for data in self.products_data:
            row = self.products_table.rowCount()
            self.products_table.insertRow(row)
            for col, value in enumerate(data):
                item = QTableWidgetItem(value)
                item.setFlags(item.flags() ^ Qt.ItemIsEditable)
                self.products_table.setItem(row, col, item)
    
    def load_material_data(self):
        selected_row = self.materials_table.currentRow()
        if selected_row >= 0:
            material = self.materials_data[selected_row]
            self.material_type_combo.setCurrentText(material[0])
            self.material_name_edit.setText(material[1])
            self.material_unit_combo.setCurrentText(material[2])
            self.material_quantity_edit.setValue(int(material[3]))
            self.material_min_edit.setValue(int(material[4]))
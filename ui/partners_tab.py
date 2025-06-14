from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QLineEdit, QPushButton, QTableWidget, 
                            QTableWidgetItem, QComboBox, QDateEdit, 
                            QMessageBox, QHeaderView)
from PyQt5.QtCore import Qt
from database import db

class PartnersTab(QWidget):
    def __init__(self):
        super().__init__()
        self.partners_data = [] 
        self.initUI()
        self.load_partners()
    
    def initUI(self):
        main_layout = QVBoxLayout()
        
        # Форма добавления/редактирования партнера
        form_layout = QVBoxLayout()
        
        # Тип партнера
        type_layout = QHBoxLayout()
        type_label = QLabel("Тип партнера:")
        self.type_combo = QComboBox()
        self.type_combo.addItems(["Розничный магазин", "Оптовый магазин", "Интернет-магазин", "Другая компания"])
        type_layout.addWidget(type_label)
        type_layout.addWidget(self.type_combo)
        
        # Наименование компании
        name_layout = QHBoxLayout()
        name_label = QLabel("Наименование:")
        self.name_edit = QLineEdit()
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_edit)
        
        # Юридический адрес
        address_layout = QHBoxLayout()
        address_label = QLabel("Юридический адрес:")
        self.address_edit = QLineEdit()
        address_layout.addWidget(address_label)
        address_layout.addWidget(self.address_edit)
        
        # ИНН
        inn_layout = QHBoxLayout()
        inn_label = QLabel("ИНН:")
        self.inn_edit = QLineEdit()
        inn_layout.addWidget(inn_label)
        inn_layout.addWidget(self.inn_edit)
        
        # ФИО директора
        director_layout = QHBoxLayout()
        director_label = QLabel("ФИО директора:")
        self.director_edit = QLineEdit()
        director_layout.addWidget(director_label)
        director_layout.addWidget(self.director_edit)
        
        # Контактные данные
        contacts_layout = QHBoxLayout()
        contacts_label = QLabel("Контактные данные:")
        self.phone_edit = QLineEdit()
        self.phone_edit.setPlaceholderText("Телефон")
        self.email_edit = QLineEdit()
        self.email_edit.setPlaceholderText("Email")
        contacts_layout.addWidget(contacts_label)
        contacts_layout.addWidget(self.phone_edit)
        contacts_layout.addWidget(self.email_edit)
        
        # Рейтинг
        rating_layout = QHBoxLayout()
        rating_label = QLabel("Рейтинг:")
        self.rating_combo = QComboBox()
        self.rating_combo.addItems(["A", "B", "C", "D"])
        rating_layout.addWidget(rating_label)
        rating_layout.addWidget(self.rating_combo)
        
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
        form_layout.addLayout(type_layout)
        form_layout.addLayout(name_layout)
        form_layout.addLayout(address_layout)
        form_layout.addLayout(inn_layout)
        form_layout.addLayout(director_layout)
        form_layout.addLayout(contacts_layout)
        form_layout.addLayout(rating_layout)
        form_layout.addLayout(buttons_layout)
        
        # Таблица партнеров
        self.partners_table = QTableWidget()
        self.partners_table.setColumnCount(8)
        self.partners_table.setHorizontalHeaderLabels([
            "Тип", "Наименование", "ИНН", "Директор", "Телефон", "Email", "Рейтинг", "Объем продаж"
        ])
        self.partners_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.partners_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.partners_table.setSelectionMode(QTableWidget.SingleSelection)
        
        main_layout.addLayout(form_layout)
        main_layout.addWidget(self.partners_table)
        
        self.setLayout(main_layout)
        
        # Подключаем сигналы
        self.add_button.clicked.connect(self.add_partner)
        self.edit_button.clicked.connect(self.edit_partner)
        self.delete_button.clicked.connect(self.delete_partner)
        self.clear_button.clicked.connect(self.clear_form)
        self.partners_table.itemSelectionChanged.connect(self.load_partner_data)
        
        # Загрузка тестовых данных
        self.load_test_data()
    
    def load_test_data(self):
        test_data = [
            ["Розничный магазин", "МебельОфис", "1234567890", "Иванов И.И.", "+79991234567", "office@example.com", "A", "1 250 000"],
            ["Оптовый магазин", "ОфисГрад", "0987654321", "Петров П.П.", "+79998765432", "grad@example.com", "B", "890 000"],
        ]
        
        for data in test_data:
            self.partners_data.append(data)
            row = self.partners_table.rowCount()
            self.partners_table.insertRow(row)
            for col, value in enumerate(data):
                item = QTableWidgetItem(value)
                item.setFlags(item.flags() ^ Qt.ItemIsEditable)
                self.partners_table.setItem(row, col, item)
    
    def add_partner(self):
        # Проверка заполнения обязательных полей
        if not self.name_edit.text() or not self.inn_edit.text():
            QMessageBox.warning(self, "Ошибка", "Заполните обязательные поля: Наименование и ИНН")
            return
        
        partner_data = [
            self.type_combo.currentText(),
            self.name_edit.text(),
            self.inn_edit.text(),
            self.director_edit.text(),
            self.phone_edit.text(),
            self.email_edit.text(),
            self.rating_combo.currentText(),
            "0"  # Начальный объем продаж
        ]
        
        self.partners_data.append(partner_data)
        
        row = self.partners_table.rowCount()
        self.partners_table.insertRow(row)
        for col, value in enumerate(partner_data):
            item = QTableWidgetItem(value)
            item.setFlags(item.flags() ^ Qt.ItemIsEditable)
            self.partners_table.setItem(row, col, item)
        
        self.clear_form()
        QMessageBox.information(self, "Успех", "Партнер успешно добавлен")
    
    def edit_partner(self):
        selected_row = self.partners_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите партнера для редактирования")
            return
        
        # Проверка заполнения обязательных полей
        if not self.name_edit.text() or not self.inn_edit.text():
            QMessageBox.warning(self, "Ошибка", "Заполните обязательные поля: Наименование и ИНН")
            return
        
        partner_data = [
            self.type_combo.currentText(),
            self.name_edit.text(),
            self.inn_edit.text(),
            self.director_edit.text(),
            self.phone_edit.text(),
            self.email_edit.text(),
            self.rating_combo.currentText(),
            self.partners_table.item(selected_row, 7).text()  # Сохраняем объем продаж
        ]
        
        self.partners_data[selected_row] = partner_data
        
        for col, value in enumerate(partner_data):
            item = QTableWidgetItem(value)
            item.setFlags(item.flags() ^ Qt.ItemIsEditable)
            self.partners_table.setItem(selected_row, col, item)
        
        QMessageBox.information(self, "Успех", "Данные партнера успешно обновлены")
    
    def delete_partner(self):
        selected_row = self.partners_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите партнера для удаления")
            return
        
        reply = QMessageBox.question(
            self, 
            "Подтверждение", 
            f"Вы уверены, что хотите удалить партнера {self.partners_table.item(selected_row, 1).text()}?", 
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.partners_table.removeRow(selected_row)
            self.partners_data.pop(selected_row)
            self.clear_form()
    
    def load_partners(self):
        try:
            with db.conn.cursor() as cur:
                cur.execute("SELECT * FROM partners")
                partners = cur.fetchall()
                
                self.partners_table.setRowCount(0)
                for row_num, partner in enumerate(partners):
                    self.partners_table.insertRow(row_num)
                    for col_num, data in enumerate(partner[1:]):  # Пропускаем id
                        item = QTableWidgetItem(str(data))
                        item.setFlags(item.flags() ^ Qt.ItemIsEditable)
                        self.partners_table.setItem(row_num, col_num, item)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить партнеров: {e}")
    
    def add_partner(self):
        if not self.name_edit.text() or not self.inn_edit.text():
            QMessageBox.warning(self, "Ошибка", "Заполните обязательные поля: Наименование и ИНН")
            return
        
        try:
            with db.conn.cursor() as cur:
                cur.execute("""
                INSERT INTO partners (type, name, address, inn, director, phone, email, rating)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    self.type_combo.currentText(),
                    self.name_edit.text(),
                    self.address_edit.text(),
                    self.inn_edit.text(),
                    self.director_edit.text(),
                    self.phone_edit.text(),
                    self.email_edit.text(),
                    self.rating_combo.currentText()
                ))
                db.conn.commit()
                self.load_partners()
                self.clear_form()
                QMessageBox.information(self, "Успех", "Партнер успешно добавлен")
        except Exception as e:
            db.conn.rollback()
            QMessageBox.critical(self, "Ошибка", f"Не удалось добавить партнера: {e}")
    
    def edit_partner(self):
        selected_row = self.partners_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите партнера для редактирования")
            return
        
        partner_id = self.get_partner_id(selected_row)
        
        try:
            with db.conn.cursor() as cur:
                cur.execute("""
                UPDATE partners 
                SET type = %s, name = %s, address = %s, inn = %s, 
                    director = %s, phone = %s, email = %s, rating = %s
                WHERE id = %s
                """, (
                    self.type_combo.currentText(),
                    self.name_edit.text(),
                    self.address_edit.text(),
                    self.inn_edit.text(),
                    self.director_edit.text(),
                    self.phone_edit.text(),
                    self.email_edit.text(),
                    self.rating_combo.currentText(),
                    partner_id
                ))
                db.conn.commit()
                self.load_partners()
                QMessageBox.information(self, "Успех", "Данные партнера обновлены")
        except Exception as e:
            db.conn.rollback()
            QMessageBox.critical(self, "Ошибка", f"Не удалось обновить данные: {e}")
    
    def delete_partner(self):
        selected_row = self.partners_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите партнера для удаления")
            return
        
        partner_id = self.get_partner_id(selected_row)
        partner_name = self.partners_table.item(selected_row, 1).text()
        
        reply = QMessageBox.question(
            self, "Подтверждение", 
            f"Вы уверены, что хотите удалить партнера {partner_name}?", 
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                with db.conn.cursor() as cur:
                    cur.execute("DELETE FROM partners WHERE id = %s", (partner_id,))
                    db.conn.commit()
                    self.load_partners()
                    self.clear_form()
            except Exception as e:
                db.conn.rollback()
                QMessageBox.critical(self, "Ошибка", f"Не удалось удалить партнера: {e}")
    
    def get_partner_id(self, row):
        try:
            with db.conn.cursor() as cur:
                partner_name = self.partners_table.item(row, 1).text()
                cur.execute("SELECT id FROM partners WHERE name = %s", (partner_name,))
                return cur.fetchone()[0]
        except Exception as e:
            print(f"Error getting partner id: {e}")
            return None
    
    def load_partner_data(self):
        selected_row = self.partners_table.currentRow()
        if selected_row >= 0:
            partner_id = self.get_partner_id(selected_row)
            try:
                with db.conn.cursor() as cur:
                    cur.execute("SELECT * FROM partners WHERE id = %s", (partner_id,))
                    partner = cur.fetchone()
                    
                    if partner:
                        self.type_combo.setCurrentText(partner[1])
                        self.name_edit.setText(partner[2])
                        self.address_edit.setText(partner[3])
                        self.inn_edit.setText(partner[4])
                        self.director_edit.setText(partner[5])
                        self.phone_edit.setText(partner[6])
                        self.email_edit.setText(partner[7])
                        self.rating_combo.setCurrentText(partner[8])
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить данные: {e}")
    
    def clear_form(self):
        self.type_combo.setCurrentIndex(0)
        self.name_edit.clear()
        self.address_edit.clear()
        self.inn_edit.clear()
        self.director_edit.clear()
        self.phone_edit.clear()
        self.email_edit.clear()
        self.rating_combo.setCurrentIndex(0)
        self.partners_table.clearSelection()
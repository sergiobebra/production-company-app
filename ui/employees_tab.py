from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QLineEdit, QPushButton, QTableWidget, 
                            QTableWidgetItem, QDateEdit, QComboBox, 
                            QMessageBox, QHeaderView)
from PyQt5.QtCore import Qt, QDate
from database import db 

class EmployeesTab(QWidget):
    def __init__(self):
        super().__init__()
        self.employees_data = []
        self.initUI()
        self.load_employees()

    def initUI(self):
        main_layout = QVBoxLayout()
        
        # Форма добавления сотрудников
        form_layout = QVBoxLayout()
        
        # ФИО
        name_layout = QHBoxLayout()
        name_label = QLabel("ФИО:")
        self.name_edit = QLineEdit()
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_edit)
        
        # Дата рождения
        birth_layout = QHBoxLayout()
        birth_label = QLabel("Дата рождения:")
        self.birth_edit = QDateEdit()
        self.birth_edit.setDate(QDate.currentDate())
        self.birth_edit.setCalendarPopup(True)
        birth_layout.addWidget(birth_label)
        birth_layout.addWidget(self.birth_edit)
        
        # Должность
        position_layout = QHBoxLayout()
        position_label = QLabel("Должность:")
        self.position_combo = QComboBox()
        self.position_combo.addItems(["Менеджер", "Мастер", "Рабочий", "Аналитик", "Кладовщик"])
        position_layout.addWidget(position_label)
        position_layout.addWidget(self.position_combo)
        
        # Цех/отдел
        department_layout = QHBoxLayout()
        department_label = QLabel("Цех/Отдел:")
        self.department_edit = QLineEdit()
        department_layout.addWidget(department_label)
        department_layout.addWidget(self.department_edit)
        
        # Кнопки управления
        buttons_layout = QHBoxLayout()
        self.add_button = QPushButton("Добавить")
        self.edit_button = QPushButton("Редактировать")
        self.delete_button = QPushButton("Удалить")
        buttons_layout.addWidget(self.add_button)
        buttons_layout.addWidget(self.edit_button)
        buttons_layout.addWidget(self.delete_button)
        
        # Добавляем элементы в форму
        form_layout.addLayout(name_layout)
        form_layout.addLayout(birth_layout)
        form_layout.addLayout(position_layout)
        form_layout.addLayout(department_layout)
        form_layout.addLayout(buttons_layout)
        
        # Таблица сотрудников
        self.employees_table = QTableWidget()
        self.employees_table.setColumnCount(5)
        self.employees_table.setHorizontalHeaderLabels([
            "ID", "ФИО", "Дата рождения", "Должность", "Цех/Отдел"
        ])
        self.employees_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.employees_table.setSelectionBehavior(QTableWidget.SelectRows)
        
        main_layout.addLayout(form_layout)
        main_layout.addWidget(self.employees_table)
        
        self.setLayout(main_layout)
        
        # Подключаем сигналы
        self.add_button.clicked.connect(self.add_employee)
        self.edit_button.clicked.connect(self.edit_employee)
        self.delete_button.clicked.connect(self.delete_employee)
        self.employees_table.itemSelectionChanged.connect(self.load_employee_data)

    def load_employees(self):
        try:
            with db.conn.cursor() as cur:
                cur.execute("""
                    SELECT id, full_name, TO_CHAR(birth_date, 'DD.MM.YYYY'), 
                           position, department 
                    FROM employees
                    ORDER BY id
                """)
                self.employees_data = cur.fetchall()
                self.update_employees_table()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить сотрудников: {e}")

    def add_employee(self):
        if not self.name_edit.text():
            QMessageBox.warning(self, "Ошибка", "Введите ФИО сотрудника")
            return
        
        try:
            with db.conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO employees 
                    (full_name, birth_date, position, department)
                    VALUES (%s, %s, %s, %s)
                    RETURNING id
                """, (
                    self.name_edit.text(),
                    self.birth_edit.date().toString("yyyy-MM-dd"),
                    self.position_combo.currentText(),
                    self.department_edit.text()
                ))
                db.conn.commit()
                self.load_employees()
                self.clear_form()
                QMessageBox.information(self, "Успех", "Сотрудник добавлен")
        except Exception as e:
            db.conn.rollback()
            QMessageBox.critical(self, "Ошибка", f"Не удалось добавить сотрудника: {e}")

    def edit_employee(self):
        selected_row = self.employees_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите сотрудника")
            return
        
        employee_id = self.employees_table.item(selected_row, 0).text()
        if not employee_id:
            QMessageBox.warning(self, "Ошибка", "Не удалось определить ID сотрудника")
            return
        
        try:
            with db.conn.cursor() as cur:
                cur.execute("""
                    UPDATE employees SET
                    full_name = %s,
                    birth_date = %s,
                    position = %s,
                    department = %s
                    WHERE id = %s
                """, (
                    self.name_edit.text(),
                    self.birth_edit.date().toString("yyyy-MM-dd"),
                    self.position_combo.currentText(),
                    self.department_edit.text(),
                    employee_id
                ))
                db.conn.commit()
                self.load_employees()
                QMessageBox.information(self, "Успех", "Данные сотрудника обновлены")
        except Exception as e:
            db.conn.rollback()
            QMessageBox.critical(self, "Ошибка", f"Не удалось обновить данные: {e}")

    def delete_employee(self):
        selected_row = self.employees_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите сотрудника")
            return
        
        employee_id = self.employees_table.item(selected_row, 0).text()
        employee_name = self.employees_table.item(selected_row, 1).text()
        
        reply = QMessageBox.question(
            self, "Подтверждение", 
            f"Удалить сотрудника {employee_name}?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                with db.conn.cursor() as cur:
                    cur.execute("DELETE FROM employees WHERE id = %s", (employee_id,))
                    db.conn.commit()
                    self.load_employees()
                    self.clear_form()
            except Exception as e:
                db.conn.rollback()
                QMessageBox.critical(self, "Ошибка", f"Не удалось удалить сотрудника: {e}")

    def update_employees_table(self):
        self.employees_table.setRowCount(0)
        for data in self.employees_data:
            row = self.employees_table.rowCount()
            self.employees_table.insertRow(row)
            for col, value in enumerate(data):
                item = QTableWidgetItem(str(value))
                item.setFlags(item.flags() ^ Qt.ItemIsEditable)
                self.employees_table.setItem(row, col, item)
    
    def load_employee_data(self):
        selected_row = self.employees_table.currentRow()
        if selected_row >= 0:
            employee = self.employees_data[selected_row]
            self.name_edit.setText(employee[1])
            self.birth_edit.setDate(QDate.fromString(employee[2], "dd.MM.yyyy"))
            self.position_combo.setCurrentText(employee[3])
            self.department_edit.setText(employee[4])
    
    def clear_form(self):
        self.name_edit.clear()
        self.birth_edit.setDate(QDate.currentDate())
        self.position_combo.setCurrentIndex(0)
        self.department_edit.clear()
        self.employees_table.clearSelection()
from PyQt5.QtWidgets import (QMainWindow, QTabWidget, QWidget, QVBoxLayout, 
                            QLabel, QStatusBar)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from database import db 
from ui.partners_tab import PartnersTab
from ui.products_tab import ProductsTab
from ui.warehouse_tab import WarehouseTab
from ui.production_tab import ProductionTab
from ui.employees_tab import EmployeesTab

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Образ плюс - Управление производством")
        self.setGeometry(100, 100, 1200, 800)
        
        self.setup_ui()
        self.setup_styles()
        
    def setup_ui(self):
        # Логотип компании
        self.logo_label = QLabel(self)
        # self.logo_label.setPixmap(QPixmap("resources/logo.png").scaled(300, 150, Qt.KeepAspectRatio))
        self.logo_label.setAlignment(Qt.AlignCenter)
        
        # Создаем вкладки
        self.tabs = QTabWidget()
        
        # Инициализация вкладок
        self.partners_tab = PartnersTab()
        self.products_tab = ProductsTab()
        self.warehouse_tab = WarehouseTab()
        self.production_tab = ProductionTab()
        self.employees_tab = EmployeesTab()
        
        # Добавляем вкладки
        self.tabs.addTab(self.partners_tab, "Партнеры")
        self.tabs.addTab(self.products_tab, "Продукция")
        self.tabs.addTab(self.warehouse_tab, "Склад")
        self.tabs.addTab(self.production_tab, "Производство")
        self.tabs.addTab(self.employees_tab, "Сотрудники")
        
        # Основной layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.logo_label)
        main_layout.addWidget(self.tabs)
        
        # Центральный виджет
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
        
        # Статус бар
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Готово", 3000)
    
    def setup_styles(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #FFFFFF;
            }
            QTabWidget::pane {
                border: 1px solid #BFD6F6;
                background: #BFD6F6;
                margin-top: 5px;
            }
            QTabBar::tab {
                background: #BFD6F6;
                border: 1px solid #405C73;
                padding: 8px;
                font-family: Constantia;
                min-width: 100px;
            }
            QTabBar::tab:selected {
                background: #405C73;
                color: white;
            }
            QPushButton {
                background-color: #BFD6F6;
                border: 1px solid #405C73;
                padding: 5px 10px;
                font-family: Constantia;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #405C73;
                color: white;
            }
            QLineEdit, QComboBox, QDateEdit, QSpinBox, QTextEdit {
                border: 1px solid #BFD6F6;
                padding: 3px;
                font-family: Constantia;
            }
            QTableWidget {
                gridline-color: #BFD6F6;
                font-family: Constantia;
            }
            QHeaderView::section {
                background-color: #405C73;
                color: white;
                padding: 5px;
                border: none;
                font-family: Constantia;
            }
            QStatusBar {
                font-family: Constantia;
                color: #405C73;
            }
        """)
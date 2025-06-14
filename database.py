import psycopg2
from psycopg2 import sql

class Database:
    def __init__(self):
        self.conn = None
        
    def connect(self):
        try:
            self.conn = psycopg2.connect(
                dbname="production_company",
                user="postgres",
                password="postgres",
                host="localhost",
                port="5432"
            )
            print("Connected to PostgreSQL database")
        except Exception as e:
            print(f"Error connecting to PostgreSQL: {e}")
    
    def create_tables(self):
        try:
            with self.conn.cursor() as cur:
                # Таблица партнеров
                cur.execute("""
                CREATE TABLE IF NOT EXISTS partners (
                    id SERIAL PRIMARY KEY,
                    type VARCHAR(50) NOT NULL,
                    name VARCHAR(100) NOT NULL,
                    address TEXT,
                    inn VARCHAR(20) UNIQUE NOT NULL,
                    director VARCHAR(100),
                    phone VARCHAR(20),
                    email VARCHAR(100),
                    rating VARCHAR(1),
                    sales_volume DECIMAL(12, 2) DEFAULT 0
                )
                """)
                
                # Таблица продукции
                cur.execute("""
                CREATE TABLE IF NOT EXISTS products (
                    id SERIAL PRIMARY KEY,
                    article VARCHAR(20) UNIQUE NOT NULL,
                    type VARCHAR(50) NOT NULL,
                    name VARCHAR(100) NOT NULL,
                    description TEXT,
                    price DECIMAL(12, 2) NOT NULL,
                    length INTEGER,
                    width INTEGER,
                    height INTEGER,
                    weight INTEGER,
                    production_time VARCHAR(50)
                )
                """)
                
                # Таблица материалов
                cur.execute("""
                CREATE TABLE IF NOT EXISTS materials (
                    id SERIAL PRIMARY KEY,
                    type VARCHAR(50) NOT NULL,
                    name VARCHAR(100) NOT NULL,
                    unit VARCHAR(10) NOT NULL,
                    quantity INTEGER NOT NULL,
                    min_stock INTEGER NOT NULL
                )
                """)
                cur.execute("""
                CREATE TABLE IF NOT EXISTS employees (
                    id SERIAL PRIMARY KEY,
                    full_name VARCHAR(100) NOT NULL,
                    birth_date DATE,
                    position VARCHAR(50),
                    department VARCHAR(50),
                    status VARCHAR(20) DEFAULT 'Активен'
                )
                """)
                cur.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id SERIAL PRIMARY KEY,
                article VARCHAR(20) UNIQUE NOT NULL,
                type VARCHAR(50) NOT NULL,
                name VARCHAR(100) NOT NULL,
                description TEXT,
                price DECIMAL(12, 2) NOT NULL,
                length INTEGER,
                width INTEGER,
                height INTEGER,
                weight INTEGER,
                production_time VARCHAR(50)
            )
            """)
                self.conn.commit()
        except Exception as e:
            print(f"Error creating tables: {e}")
            self.conn.rollback()
    
    def close(self):
        if self.conn:
            self.conn.close()
            print("Database connection closed")

# Создаем глобальный экземпляр для использования в приложении
db = Database()
db.connect()
db.create_tables()
print("Таблицы созданы успешно!")
db.close()
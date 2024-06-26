import pyodbc
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
import sys

sys.path.append(os.path.join(sys.path[0], 'dbcon'))

load_dotenv()

username = os.environ.get("USNAME")
password = os.environ.get("PASS")
hostname = os.environ.get("HOST")
database = os.environ.get("DBNAME")

# Создание подключения к базе данных
engine = create_engine(
    f"mssql+pyodbc://{username}:{password}@{hostname}/{database}?driver=ODBC+Driver+18+for+SQL+Server"
    f"&TrustServerCertificate=yes")

# Создание сессии
Session = sessionmaker(bind=engine)
session = Session()

REDIS_HOST = os.environ.get("REDIS_HOST")
REDIS_PASS = os.environ.get("REDIS_PASS")


def test_conn():
    connection = engine.raw_connection()

    # Получение информации о драйвере
    driver_info = connection.getinfo(pyodbc.SQL_DRIVER_NAME)
    driver_version = connection.getinfo(pyodbc.SQL_DRIVER_VER)

    print(f"Driver Name: {driver_info}")
    print(f"Driver Version: {driver_version}")

    # Закрытие подключения
    connection.close()


if __name__ == '__main__':
    pass

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
database_name = os.environ.get("DBNAME")


# Создание подключения к базе данных
# engine = create_engine(f'mssql+pyodbc://{username}:{password}@{hostname}/{database_name}?driver=SQL+Server')
engine = create_engine("mssql+pyodbc://{username}:{password}@{hostname}/{database_name}?driver=ODBC+Driver+18+for+SQL+Server")


# Создание сессии
Session = sessionmaker(bind=engine)
session = Session()

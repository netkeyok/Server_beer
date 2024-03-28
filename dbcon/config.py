from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
import sys

sys.path.append(os.path.join(sys.path[0], 'dbcon'))

load_dotenv()

username = os.environ.get("usname")
password = os.environ.get("pass")
hostname = os.environ.get("host")
database_name = os.environ.get("dbname")


# Создание подключения к базе данных
engine = create_engine(f'mssql+pyodbc://{username}:{password}@{hostname}/{database_name}?driver=SQL+Server')

# Создание сессии
Session = sessionmaker(bind=engine)
session = Session()

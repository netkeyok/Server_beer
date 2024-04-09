# Используем официальный образ Python как базовый
FROM python:3.11.9-slim

# Установка переменных окружения для немедленного вывода логов в консоль
ENV PYTHONUNBUFFERED 1

# Установка необходимых утилит и зависимостей для pyodbc
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        g++ \
        unixodbc-dev \
        gnupg \
        curl \
    && curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/ubuntu/22.04/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql17 \
    # Очистка кэша apt
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Установка SQLAlchemy и pyodbc


# Команды, выполняемые при запуске контейнера
COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD python3 -m uvicorn main:app --reload --host 0.0.0.0 --port 8081

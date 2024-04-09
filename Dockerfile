# Используем официальный образ Python как базовый
FROM python:3.11.9-slim-bullseye

# Установка переменных окружения для немедленного вывода логов в консоль
ENV PYTHONUNBUFFERED=1

# Добавление ключа Microsoft GPG и репозитория
RUN curl https://packages.microsoft.com/keys/microsoft.asc | tee /etc/apt/trusted.gpg.d/microsoft.asc \
    && curl https://packages.microsoft.com/config/debian/12/prod.list | tee /etc/apt/sources.list.d/mssql-release.list

# Обновление списка пакетов и установка необходимых пакетов
RUN apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql18 \
    # optional: for bcp and sqlcmd
    && ACCEPT_EULA=Y apt-get install -y mssql-tools18 \
    && echo 'export PATH="$PATH:/opt/mssql-tools18/bin"' >> ~/.bashrc \
    # optional: for unixODBC development headers
    && apt-get install -y unixodbc-dev \
    # optional: kerberos library for debian-slim distributions
    && apt-get install -y libgssapi-krb5-2

# Установка SQLAlchemy и pyodbc, копирование файлов проекта и установка зависимостей
COPY . .
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Команды, выполняемые при запуске контейнера
CMD ["python3", "-m", "uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8081"]
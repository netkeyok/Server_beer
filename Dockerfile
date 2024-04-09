# Используем официальный образ Python как базовый
FROM python:3.11.9-alpine3.19

# Установка переменных окружения для немедленного вывода логов в консоль
ENV PYTHONUNBUFFERED=1

# Установка необходимых утилит и зависимостей для Microsoft ODBC 18
RUN apk update \
    && apk add --no-cache gcc g++ unixodbc-dev gnupg curl

# Определение архитектуры для скачивания правильного пакета
RUN case $(uname -m) in \
        x86_64) architecture="amd64" ;; \
        arm64) architecture="arm64" ;; \
        *) echo "Alpine architecture $(uname -m) is not currently supported." && exit 1 ;; \
    esac \
    && curl -O https://download.microsoft.com/download/3/5/5/355d7943-a338-41a7-858d-53b259ea33f5/msodbcsql18_18.3.2.1-1_$architecture.apk \
    && curl -O https://download.microsoft.com/download/3/5/5/355d7943-a338-41a7-858d-53b259ea33f5/mssql-tools18_18.3.1.1-1_$architecture.apk \
    # (Optional) Проверка подписи, если требуется
    && apk add --no-cache gnupg \
    && curl https://packages.microsoft.com/keys/microsoft.asc | gpg --import - \
    && gpg --verify msodbcsql18_18.3.2.1-1_$architecture.sig msodbcsql18_18.3.2.1-1_$architecture.apk \
    && gpg --verify mssql-tools18_18.3.1.1-1_$architecture.sig mssql-tools18_18.3.1.1-1_$architecture.apk \
    # Установка пакетов
    && apk add --allow-untrusted msodbcsql18_18.3.2.1-1_$architecture.apk \
    && apk add --allow-untrusted mssql-tools18_18.3.1.1-1_$architecture.apk

# Установка SQLAlchemy и pyodbc
# Команды, выполняемые при запуске контейнера
COPY . .
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

CMD ["python3", "-m", "uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8081"]
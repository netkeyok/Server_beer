Временный мини сервер для утилиты печати пивных QR кодов

# Для запуска:
docker build . --tag server_beer --no-cache && docker run --name server_beer -p 8081:8081 -p 5557:5557 --env-file ./.env server_beer
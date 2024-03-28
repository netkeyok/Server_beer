FROM python:3.11-slim

COPY . .

RUN pip install -r requirements.txt
RUN apt-get install unixodbc-dev

CMD python3 -m uvicorn main:app --reload --host 0.0.0.0 --port 8081

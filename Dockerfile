FROM laudio/pyodbc:3.0.0

COPY . .

# install FreeTDS and dependencies

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD python3 -m uvicorn main:app --reload --host 0.0.0.0 --port 8081

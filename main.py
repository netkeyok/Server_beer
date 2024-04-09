from datetime import datetime

from fastapi import FastAPI
from dbcon.pydantic_models import Package
from dbcon.config import username, password, hostname, database

from dbcon.functions import request_docs, organization_list

app = FastAPI()


@app.get("/documents/")
async def get_documents(start_date: datetime, end_date: datetime, number: int) -> Package:
    documents = request_docs(start_date, end_date, number)
    return documents


@app.get("/orgs/")
async def get_org_list():
    items = organization_list()
    return items

# test_conn()
print(username, password, hostname, database)
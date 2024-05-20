from uuid import UUID

import uvicorn
from fastapi import FastAPI, Body

from service import Service

app = FastAPI()
service = Service()


@app.get("/select")
def select():
    return service.select()


@app.post("/insert")
def insert(
    value: str = Body(),
    transaction_id: UUID = Body(),
):
    result = service.insert(value, transaction_id)
    return {"id": result}


@app.delete("/delete")
def delete(
    item_id: UUID = Body(),
    transaction_id: UUID = Body(),
):
    service.delete(item_id, transaction_id)
    return {"status": "success"}


@app.post("/begin")
def begin(parent_id: UUID | None = Body(default=None, embed=True)):
    transaction_id = service.begin(parent_id)
    return {"transaction_id": transaction_id}


@app.post("/commit")
def commit(
    transaction_id: UUID = Body(embed=True),
):
    service.commit(transaction_id)
    return {"status": "success"}


@app.post("/rollback")
def rollback(
    transaction_id: UUID = Body(embed=True),
):
    service.rollback(transaction_id)
    return {"status": "success"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

from http.client import HTTPMessage
from typing import List
from uuid import uuid4
from fastapi import FastAPI, Depends, HTTPException
from models import *
from database import engine, SessionLocal
import models 
from sqlalchemy.orm import Session
from prometheus_client import start_http_server, Counter
import http.server

METRICS_PORT = 8001
REQUEST_COUNT = Counter('app_request_count', 'Total / http request count')
REQUEST_COUNT_INTERNS = Counter('app_request_count_users', 'Total /api/v1/interns http request count')

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

start_http_server(METRICS_PORT)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

@app.get("/")
def create_database():
    REQUEST_COUNT.inc()
    return {"Hello": "Interns!"}

@app.get("/api/v1/interns")
async def fetch_users(db: Session = Depends(get_db)):
    REQUEST_COUNT_INTERNS.inc()
    return db.query(models.Intern).all()

@app.post("/api/v1/interns")
async def register_user(intern: InternModel, db: Session = Depends(get_db)):
    intern_model = models.Intern()
    intern_model.id_intern = intern.id_intern
    intern_model.first_name = intern.first_name
    intern_model.last_name = intern.last_name
    db.add(intern_model)
    db.commit()
    return {"id": intern.id }

@app.delete("/api/v1/interns/{intern_id}")
async def delete_user(id_intern: int, db: Session = Depends(get_db)):
    intern_model = db.query(models.Intern)
    for intern in intern_model:
        print(id_intern)
        print(intern.id_intern)
        if intern.id_intern == id_intern:
            db.delete(intern)
            db.commit()
            return { f"user with id: {id_intern} was deleted" }

    raise HTTPException(
        status_code=404,
        detail=f"user with id: {id_intern} does not exist"
    )

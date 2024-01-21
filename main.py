from app.models.dbmodels import Base  # Update the import
from app.config.dbconfig import sqlalchemy_engine
from fastapi import FastAPI

Base.metadata.create_all(bind=sqlalchemy_engine)

app = FastAPI()

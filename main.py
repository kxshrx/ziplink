from fastapi import FastAPI
from routers import urls
import models
from database import engine
app = FastAPI()

app.include_router(urls.router)

models.Base.metadata.create_all(bind=engine)


from fastapi import FastAPI
from routers import urls, users, auth
import models
from database import engine
app = FastAPI()

app.include_router(urls.router)
app.include_router(users.router)
app.include_router(auth.router)
models.Base.metadata.create_all(bind=engine)


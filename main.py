from fastapi import FastAPI
from routers import urls, users, auth, admin
import models
from database import engine
app = FastAPI()

app.include_router(urls.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(admin.router)
models.Base.metadata.create_all(bind=engine)


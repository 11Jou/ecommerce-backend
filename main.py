from fastapi import FastAPI, Depends, HTTPException
from Modules.Auth.Controller import router as AuthRouter
from Core.Database import Base, engine


app = FastAPI()

Base.metadata.create_all(bind=engine)
app.include_router(AuthRouter)
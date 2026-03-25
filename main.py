from fastapi import FastAPI, Depends, HTTPException
from Modules.Auth.Controller import router as AuthRouter
from Modules.UserProfile.Controller import router as UserProfileRouter
from Core.Database import Base, engine


app = FastAPI()

app.include_router(AuthRouter)
app.include_router(UserProfileRouter)
import uvicorn
import os
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from App.api import user_API, Image_API, Student_API, Mydata_API

app = FastAPI()

"""
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
"""

app.include_router(user_API.app, tags=["user"])
app.include_router(Image_API.app, tags=["webui"])
app.include_router(Student_API.app, tags=["student"])
app.include_router(Mydata_API.app, tags=["mydata"])

@app.get("/")
async def root():
    return {"message": "Hello FastAPI"}

@app.get("/home")
async def home():
    return {"message": "Home"}

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=50000)
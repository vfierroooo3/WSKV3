from database import db
from fastapi import FastAPI, Request
from pymongo import MongoClient
from schemas import ProjectCreate
from fastapi.responses import JSONResponse
from pymongo.errors import PyMongoError

app = FastAPI()

projects_collection = db["projects"]

@app.post("/projects", status_code=201)
def create_project(project: ProjectCreate):
    projects_collection.insert_one(project.model_dump())

    return {
        "success": True,
        "errorMessage": ""
    }

# Error Handler
@app.exception_handler(PyMongoError)
async def mongodb_exception_handler(
    request: Request,
    exc: PyMongoError
):
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "errorMessage": str(exc)
        }
    )
from sys import prefix

import uvicorn
from fastapi import FastAPI
from src.routers.users import router as users_router

app = FastAPI(prefix="api/")
app.include_router(users_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
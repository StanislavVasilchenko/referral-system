import uvicorn
from fastapi import FastAPI
from src.routers.users import router as users_router
from src.routers.referral_code import router as ref_code_router

app = FastAPI(prefix="api/")
app.include_router(users_router)
app.include_router(ref_code_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

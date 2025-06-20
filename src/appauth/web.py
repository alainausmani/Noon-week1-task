from fastapi import FastAPI
from .views import router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.include_router(router, prefix="/auth") 

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


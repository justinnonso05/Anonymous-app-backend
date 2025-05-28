from fastapi import FastAPI
from sqlalchemy.orm import Session
from app.database import init_db
from app.routes import message_routes, user_routes
from fastapi.security import APIKeyHeader, OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Define allowed origins (Frontend URL)
origins = [
    "https://justinnonso05.github.io",
    "https://url-insights.vercel.app/",
    "http://127.0.0.1:5500" # Alternative localhost URL
]
# Enable CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows only specific origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)


@app.on_event("startup")
def startup():
    init_db()

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI with SQLite!"}

# Include routers
app.include_router(user_routes.router, prefix="/users", tags=["Users"])
app.include_router(message_routes.router, prefix="/api", tags=["messages"])

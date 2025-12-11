import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI Image Upload Service"
    UPLOAD_DIR: str = "app/static/uploads"
    # Railway sẽ cung cấp biến DATABASE_URL nếu bạn add plugin Postgres
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./sql_app.db")

settings = Settings()

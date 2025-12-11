import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI Image Upload Service"
    UPLOAD_DIR: str = "app/static/uploads"
    
    @property
    def DATABASE_URL(self) -> str:
        # 1. Lấy biến từ hệ thống
        url = os.getenv("DATABASE_URL")
        
        # 2. Log kiểm tra (Sẽ hiện trong Deploy Logs của Railway)
        if not url:
            print("⚠️ DATABASE_URL is EMPTY! Using SQLite as fallback.")
            return "sqlite:///./sql_app.db"
        
        # 3. Fix lỗi prefix cho Postgres
        if url.startswith("postgres://"):
            url = url.replace("postgres://", "postgresql://", 1)
        
        return url

settings = Settings()

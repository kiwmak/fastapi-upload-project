import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI Image Upload Service"
    UPLOAD_DIR: str = "app/static/uploads"
    
    # Lấy DATABASE_URL từ Railway (mặc định là SQLite nếu chạy ở local)
    _db_url: str = os.getenv("DATABASE_URL", "sqlite:///./sql_app.db")
    
    @property
    def DATABASE_URL(self) -> str:
        # Sửa lỗi 'postgres://' thành 'postgresql://' cho SQLAlchemy
        if self._db_url and self._db_url.startswith("postgres://"):
            return self._db_url.replace("postgres://", "postgresql://", 1)
        return self._db_url

settings = Settings()

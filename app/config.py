import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI Image Upload Service"
    UPLOAD_DIR: str = "app/static/uploads"
    
    # Sử dụng property để xử lý chuỗi URL
    @property
    def DATABASE_URL(self) -> str:
        url = os.getenv("DATABASE_URL")
        if not url:
            # Trả về SQLite mặc định nếu không tìm thấy biến môi trường
            return "sqlite:///./sql_app.db"
        
        # Sửa lỗi format cho SQLAlchemy
        if url.startswith("postgres://"):
            url = url.replace("postgres://", "postgresql://", 1)
        return url

settings = Settings()

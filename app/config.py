import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI Image Upload Service"
    UPLOAD_DIR: str = "app/static/uploads"
    # Dùng os.environ.get để lấy trực tiếp từ hệ thống Railway
    DATABASE_URL: str = os.environ.get("DATABASE_URL", "sqlite:///./sql_app.db")

    def get_sqlalchemy_url(self) -> str:
        # Xử lý chuỗi để SQLAlchemy không báo lỗi parse
        url = self.DATABASE_URL
        if url.startswith("postgres://"):
            url = url.replace("postgres://", "postgresql://", 1)
        return url

settings = Settings()

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI Image Upload Service"
    # Đường dẫn nơi ảnh sẽ được lưu trữ (tương đối với gốc dự án)
    UPLOAD_DIR: str = "app/static/uploads"
    # Cấu hình Database (dùng SQLite cho đơn giản)
    DATABASE_URL: str = "sqlite:///./sql_app.db"

settings = Settings()
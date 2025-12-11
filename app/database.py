from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# 1. Lấy chuỗi kết nối đã được xử lý từ config
SQLALCHEMY_DATABASE_URL = settings.get_sqlalchemy_url()

# 2. In ra log để bạn kiểm tra trên Railway (chỉ in phần đuôi để bảo mật)
print(f"DEBUG: Connecting to DB: {SQLALCHEMY_DATABASE_URL.split('@')[-1] if '@' in SQLALCHEMY_DATABASE_URL else 'SQLite'}")

# 3. Tạo Engine
if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
else:
    # Đối với Postgres (Railway)
    engine = create_engine(SQLALCHEMY_DATABASE_URL)

# 4. Tạo Session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 5. KHAI BÁO BASE (Dòng này cực kỳ quan trọng, lỗi của bạn là do thiếu dòng này)
Base = declarative_base()

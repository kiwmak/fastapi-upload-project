from sqlalchemy import create_engine
from .config import settings

# Gọi hàm xử lý URL đã fix postgresql://
SQLALCHEMY_DATABASE_URL = settings.get_sqlalchemy_url()

if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
else:
    # Đối với Postgres trên Railway
    engine = create_engine(SQLALCHEMY_DATABASE_URL)

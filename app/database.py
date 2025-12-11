from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# Lấy URL từ property chúng ta vừa viết ở config.py
db_url = settings.DATABASE_URL

# In ra log để debug trên Railway
print(f"🚀 Connecting to: {db_url.split('@')[-1] if '@' in db_url else db_url}")

if db_url.startswith("sqlite"):
    engine = create_engine(db_url, connect_args={"check_same_thread": False})
else:
    engine = create_engine(db_url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

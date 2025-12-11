#!/bin/bash

# Lệnh này dùng Gunicorn để quản lý tiến trình (process management) 
# và sử dụng Uvicorn workers để xử lý ứng dụng FastAPI (app.main:app)
#
# Cấu hình:
# --workers 4: Sử dụng 4 worker (số lượng worker thường bằng 2 * số core CPU + 1, nhưng 4 là giá trị an toàn)
# --worker-class uvicorn.workers.UvicornWorker: Chỉ định worker type là Uvicorn
# app.main:app: Chỉ định vị trí ứng dụng của bạn (từ file app/main.py)

gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
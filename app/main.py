import os
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Depends, Request
from fastapi.responses import JSONResponse, FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session # Đã bỏ comment
from pathlib import Path
from datetime import datetime
import shutil
import uuid

# Import các file bạn đã tạo
from . import models, crud
from .database import engine
from .deps import get_db
from .config import settings

# Khởi tạo DB và tạo bảng nếu chưa có
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME)

# Đảm bảo thư mục upload tồn tại
Path(settings.UPLOAD_DIR).mkdir(parents=True, exist_ok=True)

# Static files (để phục vụ ảnh đã upload)
# Lưu ý: '/static/' là đường dẫn URL, 'app/static' là thư mục vật lý
app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")

# --- ENDPOINTS QUẢN LÝ DỮ LIỆU ---

@app.post("/orders", response_model=dict)
def create_order_endpoint(order_no: str = Form(...), db: Session = Depends(get_db)):
    existing = crud.get_order_by_no(db, order_no)
    if existing:
        raise HTTPException(status_code=400, detail="Order already exists")
    o = crud.create_order(db, order_no)
    return {"id": o.id, "order_no": o.order_no}


@app.post("/items", response_model=dict)
def create_item_endpoint(order_no: str = Form(...), item_code: str = Form(...), db: Session = Depends(get_db)):
    # 1. Lấy hoặc tạo Order
    order = crud.get_order_by_no(db, order_no)
    if not order:
        order = crud.create_order(db, order_no)

    # 2. Kiểm tra Item đã tồn tại chưa
    existing = crud.get_item_by_code(db, item_code)
    if existing:
        raise HTTPException(status_code=400, detail="Item code already exists")

    # 3. Tạo Item mới
    it = crud.create_item(db, order, item_code)
    return {"id": it.id, "item_code": it.item_code, "order_no": order_no}


# --- ENDPOINT UPLOAD ẢNH (CHÍNH) ---

@app.post("/items/{item_code}/images", response_model=dict)
async def upload_item_image(item_code: str, file: UploadFile = File(...), db: Session = Depends(get_db)):
    item = crud.get_item_by_code(db, item_code)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    # 1. Xử lý tên file và đường dẫn
    ext = file.filename.split(".")[-1]
    # Tạo tên file duy nhất: Mã hàng_Timestamp_UUID_Ngắn.đuôi
    unique_filename = f"{item_code}_{int(datetime.utcnow().timestamp())}_{uuid.uuid4().hex[:8]}.{ext}"

    # Đường dẫn vật lý để lưu file
    save_path = Path(settings.UPLOAD_DIR) / unique_filename

    # 2. Lưu file vật lý
    try:
        # Mở file mới để ghi binary (wb)
        with save_path.open("wb") as buffer:
            # Sao chép dữ liệu từ file upload vào file trên server
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        print(f"Error saving file: {e}")
        raise HTTPException(status_code=500, detail="Could not save file")


    # 3. Lưu metadata vào DB
    # Đường dẫn URL công khai (từ thư mục static/uploads)
    url_path = f"/static/uploads/{unique_filename}"
    img = crud.create_item_image(db, item, unique_filename, url_path)

    return {"id": img.id, "file_name": img.file_name, "url": img.file_path, "item_code": item_code}


@app.get("/items/{item_code}/images", response_model=list)
def list_item_images(item_code: str, db: Session = Depends(get_db)):
    item = crud.get_item_by_code(db, item_code)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    imgs = crud.list_images_for_item(db, item)
    # Trả về các trường cần thiết để hiển thị trên client
    return [
        {"id": i.id, "file_name": i.file_name, "url": i.file_path, "uploaded_at": i.uploaded_at}
        for i in imgs
    ]


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    # Đường dẫn ảnh mẫu để kiểm tra kết nối static
    test_image_url = "/static/uploads/fastapi_icon.png"
    return templates.TemplateResponse(
        "index.html", 
        {
            "request": request,
            "test_image": test_image_url
        }
    )

# --- ENDPOINTS GET DANH SÁCH ---

@app.get("/api/orders", response_model=list)
def list_orders(db: Session = Depends(get_db)):
    """Trả về danh sách tất cả đơn hàng"""
    orders = db.query(models.Order).all()
    return [{"order_no": o.order_no, "created_at": o.created_at} for o in orders]

@app.get("/api/items", response_model=list)
def list_items(db: Session = Depends(get_db)):
    """Trả về danh sách tất cả mã hàng"""
    items = db.query(models.Item).all()
    # Lấy thêm thông tin order_no để hiển thị
    return [
        {"item_code": i.item_code, "order_no": i.order.order_no, "created_at": i.created_at} 
        for i in items
    ]

# ... (các endpoint khác)

@app.get("/api/orders/{order_no}/items", response_model=list)
def list_items_by_order(order_no: str, db: Session = Depends(get_db)):
    """Trả về danh sách Mã hàng thuộc một Đơn hàng cụ thể"""
    order = crud.get_order_by_no(db, order_no)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
        
    # Lấy danh sách item từ mối quan hệ đã định nghĩa trong models.py
    items = order.items 
    return [
        {"item_code": i.item_code, "order_no": order_no} 
        for i in items
    ]
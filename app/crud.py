from sqlalchemy.orm import Session
from . import models

# Order CRUD
def get_order_by_no(db: Session, order_no: str):
    return db.query(models.Order).filter(models.Order.order_no == order_no).first()

def create_order(db: Session, order_no: str):
    db_order = models.Order(order_no=order_no)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

# Item CRUD
def get_item_by_code(db: Session, item_code: str):
    return db.query(models.Item).filter(models.Item.item_code == item_code).first()

def create_item(db: Session, order: models.Order, item_code: str):
    db_item = models.Item(order_id=order.id, item_code=item_code)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

# Image CRUD
def create_item_image(db: Session, item: models.Item, file_name: str, file_path: str):
    db_image = models.ItemImage(
        item_id=item.id,
        file_name=file_name,
        file_path=file_path
    )
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image

def list_images_for_item(db: Session, item: models.Item):
    return db.query(models.ItemImage).filter(models.ItemImage.item_id == item.id).all()
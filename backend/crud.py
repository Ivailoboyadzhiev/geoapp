from sqlalchemy.orm import Session
import models
import schemas

def get_points(db: Session):
    return db.query(models.GeoPoint).all()


def get_next_available_id(db: Session):
    used_ids = db.query(models.GeoPoint.id).order_by(models.GeoPoint.id).all()
    used_ids = {id for (id,) in used_ids}
    current = 1
    while current in used_ids:
        current += 1
    return current

def create_point(db: Session, point: schemas.PointCreate):
    next_id = get_next_available_id(db)
    db_point = models.GeoPoint(id=next_id, **point.dict())
    db.add(db_point)
    db.commit()
    db.refresh(db_point)
    return db_point

def update_point(db: Session, point_id: int, point: schemas.PointUpdate):
    db_point = db.query(models.GeoPoint).filter(models.GeoPoint.id == point_id).first()
    if not db_point:
        return None
    db_point.latitude = point.latitude
    db_point.longitude = point.longitude
    db_point.description = point.description
    db.commit()
    db.refresh(db_point)
    return db_point

def delete_point(db: Session, point_id: int):
    db_point = db.query(models.GeoPoint).filter(models.GeoPoint.id == point_id).first()
    if not db_point:
        return None
    db.delete(db_point)
    db.commit()
    return True




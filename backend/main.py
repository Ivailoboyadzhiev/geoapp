from fastapi import FastAPI, Depends, Request, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
import models
import schemas
import crud
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from dotenv import load_dotenv
import os


load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)
#models.Base.metadata.create_all(bind=engine) #comment this for a test
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR.parent.parent / "frontend" / "templates"))


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/points", response_model=list[schemas.Point])
def read_points(db: Session = Depends(get_db)):
    return crud.get_points(db)

@app.post("/add_point", response_model=schemas.Point)
def add_point(point: schemas.PointCreate, db: Session = Depends(get_db)):
    return crud.create_point(db, point)

@app.put("/update_point/{point_id}", response_model=schemas.Point)
def update_point(point_id: int, updated: schemas.PointUpdate, db: Session = Depends(get_db)):
    db_point = crud.update_point(db, point_id, updated)
    if db_point is None:
        raise HTTPException(status_code=404, detail="Point not found")
    return db_point

@app.delete("/delete_point/{point_id}")
def delete_point(point_id: int, db: Session = Depends(get_db)):
    success = crud.delete_point(db, point_id)
    if not success:
        raise HTTPException(status_code=404, detail="Point not found")
    return {"message": "Point deleted"}


@app.get("/", response_class=HTMLResponse)
async def serve_points_page(request: Request):
    return templates.TemplateResponse("points.html", {"request": request})

@app.get("/add", response_class=HTMLResponse)
async def serve_add_page(request: Request):
    return templates.TemplateResponse("add_points.html", {"request": request})

@app.get("/map", response_class=HTMLResponse)
async def serve_map_page(request: Request):
    return templates.TemplateResponse("leafletDemo.html", {"request": request})

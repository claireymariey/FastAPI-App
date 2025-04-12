from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, ToDo
import crud, schemas

Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ROUTES

@app.get("/todos", response_model=list[schemas.ToDoOut])
def read_todos(db: Session = Depends(get_db)):
    return crud.get_all_todos(db)

@app.get("/todos/{todo_id}", response_model=schemas.ToDoOut)
def read_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = crud.get_todo(db, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="ToDo not found")
    return todo

@app.post("/todos", response_model=schemas.ToDoOut)
def create_todo(todo: schemas.ToDoCreate, db: Session = Depends(get_db)):
    return crud.create_todo(db, todo)

@app.put("/todos/{todo_id}", response_model=schemas.ToDoOut)
def update_todo(todo_id: int, todo: schemas.ToDoUpdate, db: Session = Depends(get_db)):
    db_todo = crud.update_todo(db, todo_id, todo)
    if not db_todo:
        raise HTTPException(status_code=404, detail="ToDo not found")
    return db_todo

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = crud.delete_todo(db, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="ToDo not found")
    return {"message": "ToDo deleted"}

@app.get("/todos/status/{completed}", response_model=list[schemas.ToDoOut])
def filter_todos(completed: bool, db: Session = Depends(get_db)):
    return crud.get_todos_by_status(db, completed)

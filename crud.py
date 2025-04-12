from sqlalchemy.orm import Session
from . import models, schemas

def get_all_todos(db: Session):
    return db.query(models.ToDo).all()

def get_todo(db: Session, todo_id: int):
    return db.query(models.ToDo).filter(models.ToDo.id == todo_id).first()

def create_todo(db: Session, todo: schemas.ToDoCreate):
    db_todo = models.ToDo(title=todo.title, completed=todo.completed)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

def update_todo(db: Session, todo_id: int, todo_data: schemas.ToDoUpdate):
    todo = db.query(models.ToDo).filter(models.ToDo.id == todo_id).first()
    if todo:
        todo.title = todo_data.title
        todo.completed = todo_data.completed
        db.commit()
        db.refresh(todo)
    return todo

def delete_todo(db: Session, todo_id: int):
    todo = db.query(models.ToDo).filter(models.ToDo.id == todo_id).first()
    if todo:
        db.delete(todo)
        db.commit()
    return todo

def get_todos_by_status(db: Session, completed: bool):
    return db.query(models.ToDo).filter(models.ToDo.completed == completed).all()

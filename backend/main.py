from fastapi import FastAPI, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session

from backend.config import SessionLocal
from schemas import Model
from backend.models import ModelsDB


app = FastAPI()


def get_session():
    with SessionLocal() as session:
        return session


@app.get('/')
def root():
    """
    Корневой get-запрос
    """
    return "root"


@app.get('/prompts', response_model=List[Model])
def get_prompts(db: Session = Depends(get_session)):

    """
    Получить список prompts
    """

    result = db.query(ModelsDB).all()
    return result
    # return db.query(DogDB).filter(DogDB.kind == kind).all()


@app.get('/prompt/{id}', response_model=Model)
def get_prompt_id(id: int, db: Session = Depends(get_session)):
    """
    Получение prompt по id
    """

    result = db.query(ModelsDB).filter(ModelsDB.id == id).all()
    return result


@app.post('/prompt/{id}', response_model=Model)
def post_update_prompt(id: int, score: int, comment: str, db: Session = Depends(get_session)):
    """
    Обновление оценки и комментария для конкретной комбинации Prompt + LLM
    """

    model = db.query(ModelsDB).filter(ModelsDB.id == id).first()

    if model is None:
        raise HTTPException(status_code=404, detail='Dog not found')

    model.score = score
    model.comment = comment


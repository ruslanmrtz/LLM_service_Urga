from fastapi import FastAPI, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session

from backend.config import SessionLocal
from backend.schemas import Model, UpdatePromptRequest
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


@app.get('/get_prompt/{project_name}/{func_name}/{prompt}/{llm_name}', response_model=Model)
def get_prompt(project_name: str, func_name: str,
                  prompt: str, llm_name: str, db: Session = Depends(get_session)):
    """
    Получение prompt по параметрам
    """
    try:
        result = db.query(ModelsDB).filter(
            ModelsDB.project_name == project_name,
            ModelsDB.func_name == func_name,
            ModelsDB.prompt == prompt,
            ModelsDB.llm_name == llm_name
        ).first()

        if result is None:
            raise HTTPException(status_code=404, detail="Prompt not found")
        return result

    except Exception as e:
        import logging
        logging.exception(f"Ошибка при получении prompt: {e}")
        raise HTTPException(status_code=500, detail="Ошибка базы данных")


@app.put("/update_prompt", response_model=Model)
def update_prompt(request: UpdatePromptRequest, db: Session = Depends(get_session)):
    """
    Обновление оценки и комментария для конкретной комбинации Prompt + LLM по идентификатору
    """
    try:
        model = db.query(ModelsDB).filter(ModelsDB.id == request.id).first()

        if model is None:
            raise HTTPException(status_code=404, detail='Prompt not found')

        model.prompt = request.prompt
        model.score = request.score
        model.comment = request.comment
        db.commit()

        return model
    except Exception as e:
        db.rollback()  # Важно: откат транзакции при ошибке
        raise HTTPException(status_code=500, detail=f"Ошибка базы данных: {e}")



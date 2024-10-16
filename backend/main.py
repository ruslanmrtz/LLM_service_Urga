from fastapi import FastAPI

# from backend.config import SessionLocal
# from schemas import Dog, DogType, Timestamp
# from backend.models import ModelsDB


app = FastAPI()


# def get_session():
#     with SessionLocal() as session:
#         return session


@app.get('/')
def root():
    """
    Корневой get-запрос
    """
    return "root"



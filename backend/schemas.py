from pydantic import BaseModel


class Model(BaseModel):

    id: int
    project_name: str
    func_name: str
    prompt: str
    llm_name: str
    comment: str
    score: int
    path: str


# Определяем модель данных для тела запроса
class UpdatePromptRequest(BaseModel):
    id: int
    prompt: str
    score: float
    comment: str
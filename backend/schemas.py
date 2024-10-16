from pydantic import BaseModel


class Model(BaseModel):

    id: int
    project_name: str
    func_name: str
    prompt: str
    llm_name: str
    score: int
    comment: str
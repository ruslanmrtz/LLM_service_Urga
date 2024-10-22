from sqlalchemy import Column, String, Integer

from backend.config import Base


class ModelsDB(Base):
    __tablename__ = "models_table"

    id = Column(Integer, primary_key=True, autoincrement=True)
    project_name = Column(String)
    func_name = Column(String)
    prompt = Column(String)
    llm_name = Column(String)
    comment = Column(String)
    score = Column(Integer)
    path = Column(String)
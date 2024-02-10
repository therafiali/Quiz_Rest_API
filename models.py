from typing import Optional,List
from sqlalchemy import JSON
from sqlmodel import SQLModel, Field,Column
from database import engine

class Student(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    pin : int
    

    
class Quiz_Question(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    question: str
    choices: List[str] = Field(sa_column=Column(JSON))
    correct_answer: str
    
    
class Answer(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    question_id: int
    correct_answer: str    
    
    

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    
if __name__ == "__main__":
    create_db_and_tables()

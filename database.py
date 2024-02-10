from sqlmodel import SQLModel, create_engine,Session 


database_connection_str = "postgresql://postgres:rootadmin@localhost:5432/quizfastapi"    
#echo true only development env not for production
engine = create_engine(database_connection_str, echo=True)
    
    
    
    
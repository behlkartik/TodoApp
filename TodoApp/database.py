from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# SQLALCHEMY_DATABASE_URL = "sqlite:///./todos.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost:5433/todoapp"
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:root@0.0.0.0:13306/todos"
# Engine to open connection to database on database uri string
# engine = create_engine(url=SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
engine = create_engine(url=SQLALCHEMY_DATABASE_URL)
# Each instance of SessionLocal will create a database session
SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)
# Object to control the database (to interact and create tables etc)
Base = declarative_base()

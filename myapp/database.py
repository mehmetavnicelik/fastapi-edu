from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .config import settings

#'postgresql://username:password@hostname:portnumber/databasename'
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

##Since sqlalchemy is used the code below is not necessary
#while True:
#    try:
#        conn=psycopg2.connect(host='localhost',database='fastapi-edu',user='postgres',password='2323',cursor_factory=RealDictCursor)
#        cursor=conn.cursor()
#        print("databasee connection is succesfull!")
#        break
#    except Exception as error:
#        print("database connection is failed")
#        print("Error: ",error)
#        time.sleep(2)
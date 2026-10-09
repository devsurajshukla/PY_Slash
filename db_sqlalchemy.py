import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

load_dotenv()

db_HOST = os.getenv("DB_HOST")
db_PORT = os.getenv("DB_PORT")
db_USER = os.getenv("DB_USER")
db_PASSWORD = os.getenv("DB_PASSWORD")
db_NAME = os.getenv("DB_NAME")

DATABASE_URL = ( f"mysql+mysqlconnector://{db_USER}:{db_PASSWORD}@{db_HOST}:{db_PORT}/{db_NAME}" )

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    bind=engine
)

print(f"Database connection established to {db_NAME} at {db_HOST}:{db_PORT} as user {db_USER}")
print("SQLAlchemy engine and session created successfully!")

db = SessionLocal()

print("Session created successfully!")

db.close()

print("Session closed successfully!")

# with engine.connect() as connection:

#     result = connection.execute(
#         text("SELECT DATABASE()")
#     )

#     database_name = result.scalar()

#  print("Connected database:", database_name)

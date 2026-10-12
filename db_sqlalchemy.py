import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")


DATABASE_URL = (
    f"mysql+mysqlconnector://"
    f"{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
)

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    bind=engine
)


def get_db_session():
    return SessionLocal()

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

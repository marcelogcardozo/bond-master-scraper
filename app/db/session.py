from sqlalchemy import URL, create_engine
from sqlalchemy.orm import sessionmaker

from app.config import (
    MASTER_DB_CONNECTION,
    MASTER_DB_DATABASE,
    MASTER_DB_DRIVER,
    MASTER_DB_HOST,
    MASTER_DB_PASSWORD,
    MASTER_DB_PORT,
    MASTER_DB_USERNAME,
)

SQL_URL_MASTER_DB = URL.create(
    MASTER_DB_CONNECTION,
    query={"driver": MASTER_DB_DRIVER},
    username=MASTER_DB_USERNAME,
    password=MASTER_DB_PASSWORD,
    host=MASTER_DB_HOST,
    port=MASTER_DB_PORT,
    database=MASTER_DB_DATABASE,
)


engine = create_engine(
    SQL_URL_MASTER_DB,
    connect_args={"check_same_thread": False, "connect_timeout": 30},
)

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

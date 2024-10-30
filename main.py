from urllib.parse import quote_plus
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()


username = os.getenv("DB_USERNAME")
password = quote_plus(os.getenv("DB_PASSWORD"))
host = os.getenv("DB_HOST")
database = os.getenv("DB_NAME")


DATABASE_URL = f"mssql+pyodbc://{username}:{password}@{host}/{database}?driver=ODBC+Driver+17+for+SQL+Server"


engine = create_engine(DATABASE_URL)


with engine.connect() as connection:
    result = connection.execute(text("SELECT TOP 5 codigo, descricao FROM dbo.Produtos"))
    for row in result:
        print(row)


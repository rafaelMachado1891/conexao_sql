from urllib.parse import quote_plus
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os
import pandas as pd

# Carregar variáveis de ambiente
load_dotenv()

# Configurações do banco de dados
username = os.getenv("DB_USERNAME")
password = quote_plus(os.getenv("DB_PASSWORD"))
host = os.getenv("DB_HOST")
database = os.getenv("DB_NAME")

# URL de conexão com o banco de dados
DATABASE_URL = f"mssql+pyodbc://{username}:{password}@{host}/{database}?driver=ODBC+Driver+17+for+SQL+Server"

# Criar o engine de conexão
engine = create_engine(DATABASE_URL)

# Consulta SQL
query = """
SELECT TOP 1000
    a.Numero,
    a.Data_EM,
    a.Codigo_OPF,
    a.Descricao_OPF,
    a.Codigo_Terceiro,
    a.Razao,
    b.Codigo,
    b.Descricao,
    b.Preco,
    b.Quantidade,
    a.VProdutos
FROM NotaS1 a
JOIN NotaS2 b ON b.Numero = a.Numero
WHERE a.Codigo_OPF NOT IN ('5.901')
"""

# Conectar ao banco e executar a consulta
with engine.connect() as connection:
    result = connection.execute(text(query))
    
    # Carregar os resultados em um DataFrame
    df = pd.DataFrame(result.fetchall(), columns=result.keys())

# Exportar para JSON ou CSV
output_format = "json"  # Defina para "csv" se desejar CSV

if output_format == "json":
    df.to_json("output_data.json", orient="records", lines=True, force_ascii=False)
    print("Dados exportados para output_data.json")
else:
    df.to_csv("output_data.csv", index=False)
    print("Dados exportados para output_data.csv")

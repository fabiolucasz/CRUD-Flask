import pandas as pd
from sqlalchemy import create_engine

# Exportar banco de dados como .xlsx
def converter_para_excel():
    engine = create_engine('sqlite:///cadastro.db')
    df = pd.read_sql_table('usuario', engine)
    df.to_excel('usuarios.xlsx', index=False)


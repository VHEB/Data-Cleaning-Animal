import pandas as pd
from sqlalchemy import create_engine

# Caminho do arquivo tratado
csv_path = "FichaAnimal_tratado.csv"

# Carregar o CSV tratado
df = pd.read_csv(csv_path, encoding="utf-8-sig")

# Remover colunas extras que não fazem parte do model
cols_to_drop = ["Altitude_min_max_", "Barimetria_min_max_"]
df.drop(columns=cols_to_drop, inplace=True, errors='ignore')

# Converter os nomes das colunas para minúsculas (para padronização)
df.columns = [col.lower() for col in df.columns]

# Renomear colunas para que correspondam ao model Animal do Django
rename_mapping = {
    "possivemente_extinta": "possivelmente_extinta",
    "consta_em_lista_nacional_oficial": "consta_lista_nacional_oficial",
    "unidade_de_conservacao_federal": "uc_federal",
    "unidade_de_conservacao_estadual": "uc_estadual",
    "plano_de_acao": "plano_acao",
    "listas_e_convencoes": "listas_convencoes"
}
df.rename(columns=rename_mapping, inplace=True)


if 'cadastrado_por_id' in df.columns:
    df.drop(columns=['cadastrado_por_id'], inplace=True)

# Opcional: Verifique as colunas após a renomeação
print("Colunas finais do DataFrame:")
print(df.columns.tolist())


# Crie a conexão com o MySQL
# Substitua 'VHEB', '753100', 'localhost' e 'biomap' pelos seus dados de conexão
engine = create_engine("mysql+pymysql://VHEB:753100@localhost/biomap")

# Exportar os dados para a tabela "core_animal" do MySQL
# Se a tabela já existir, os dados serão acrescentados (if_exists='append')
df.to_sql(name="core_animal", con=engine, if_exists="append", index=False, chunksize=1000)

print("✅ Dados exportados para o banco de dados com sucesso!")

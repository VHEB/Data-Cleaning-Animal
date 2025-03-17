

import pandas as pd
import chardet

# Caminho do arquivo CSV
csv_path = "FichaAnimal.csv"

# Detectar codificação automaticamente
with open(csv_path, 'rb') as f:
    result = chardet.detect(f.read())
encoding = result['encoding']

try:
    df = pd.read_csv(csv_path, encoding=encoding, sep=None, engine="python", on_bad_lines="skip")
    print("✅ Arquivo carregado com sucesso!")
except Exception as e:
    print(f"❌ Erro ao carregar CSV: {e}")
    exit()

# Exibir amostra dos dados
print("\n Primeiras linhas do arquivo:")
print(df.head())

# Mostrar estrutura do DataFrame
print("\n Informações da base de dados:")
print(df.info())

# Verificar valores nulos
print("\n Contagem de valores nulos por coluna:")
print(df.isnull().sum())

# Remover espaços extras e normalizar texto
df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

# Substituir nulos por "Desconhecido"
df.fillna("Desconhecido", inplace=True)

# Converter booleanos
bool_columns = ["Possivemente_Extinta", "Endemica_Brasil", "Consta_em_Lista_Nacional_Oficial", "Migratoria"]
for col in bool_columns:
    if col in df.columns:
        df[col] = df[col].apply(lambda x: 1 if str(x).strip().lower() == "sim" else 0)

# Salvar arquivo tratado
output_path = "FichaAnimal_tratado.csv"
df.to_csv(output_path, index=False, encoding="utf-8-sig")

print(f"\n✅ Arquivo tratado salvo em: {output_path}")
# train.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import joblib

# 1. Carregar o dataset
df = pd.read_csv('OLX_cars_dataset00.csv') 

# --- TRATAMENTO DOS DADOS PARA O FUTURO ---
ano_atual = 2026
df['Idade_Carro'] = ano_atual - df['Year']
df['Idade_Carro'] = df['Idade_Carro'].apply(lambda x: 1 if x <= 0 else x)

# Calcula a média e cria o alvo (KM daqui a 4 anos)
df['KM_por_Ano'] = df["KM's driven"] / df['Idade_Carro']
df['KM_daqui_4_anos'] = df["KM's driven"] + (df['KM_por_Ano'] * 4)
# ------------------------------------------

# 2. Selecionar as variáveis corretas do seu CSV
colunas_relevantes = ['Year', 'Price', 'Make', 'Fuel'] 

X = df[colunas_relevantes]
y = df['KM_daqui_4_anos']

# 3. Separar as colunas (Ajustado de 'Brand' para 'Make')
colunas_texto = ['Make', 'Fuel'] 
colunas_numericas = ['Year', 'Price'] 

# Criar um transformador que converte texto em número
transformador_categorias = OneHotEncoder(handle_unknown='ignore')

# Criar o processador dos dados
preprocessor = ColumnTransformer(
    transformers=[
        ('num', 'passthrough', colunas_numericas),
        ('cat', transformador_categorias, colunas_texto)
    ])

# 4. Criar um PIPELINE
modelo_pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', RandomForestRegressor(random_state=42, n_estimators=100))
])

# 5. Dividir em treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 6. Treinar o Pipeline completo
print("Treinando o modelo com Pipeline... Aguarde um momento.")
modelo_pipeline.fit(X_train, y_train)

# 7. Salvar o Pipeline completo
joblib.dump(modelo_pipeline, 'modelo_olx.pkl')

print("Sucesso! O arquivo 'modelo_olx.pkl' foi gerado.")
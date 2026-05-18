import streamlit as st
import pandas as pd
import joblib

@st.cache_resource
def load_model():
    return joblib.load("modelo_olx_v2.pkl")

@st.cache_data
def load_data():
    return pd.read_csv('OLX_cars_dataset00.csv') # só pra ter valores exatos nos dropdowns

model = load_model()
df = load_data()

unique_makes = sorted(df['Make'].dropna().unique())
unique_models = sorted(df['Model'].dropna().unique())
unique_cities = sorted(df['Registration city'].dropna().unique())
unique_fuels = sorted(df['Fuel'].dropna().unique())

st.title("Kars - Prevendo a kilometragem de veículos usados")
st.write("""
    Este app realiza a previsão da kilometragem de veículos usados em **4 anos** com base em seus detalhes atuais e perfil de mercado.
""")

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    year = st.number_input("Ano do veículo", min_value=1980, max_value=2026, value=2018, step=1)
    fuel = st.selectbox("Tipo de combustível", unique_fuels)
    city = st.selectbox("Cidade de registro", unique_cities)
    transmission = st.selectbox("Tipo de transmissão", ["Manual", "Automatic"])

with col2:
    price = st.number_input("Preço", min_value=0, max_value=100_000_000, value=50_000, step=1000)
    make = st.selectbox("Marca", unique_makes)
    carModel = st.selectbox("Modelo", unique_models)
    kmDriven = st.number_input("Quilometragem atual", min_value=0, max_value=1_000_000, value=50_000, step=1000)

st.markdown("---")

if st.button("Prever Kilometragem", type="primary"):
    input_data = pd.DataFrame([{
        'Year': year,
        'Price': price,
        'Make': make,
        'Model': carModel,
        'Fuel': fuel,
        'Registration city': city,
        'Transmission': transmission,
        "KM's driven": kmDriven
    }])

    try:
        prediction = model.predict(input_data)[0]

        st.success(f"A previsão da kilometragem em 4 anos é: **{prediction:.2f} km**")
        st.metric(label="Previsão de Kilometragem", value=f"{int(prediction):,}".replace(",", ".") + " Km")

    except Exception as e:
        st.error(f"Erro ao realizar a previsão: {e}")
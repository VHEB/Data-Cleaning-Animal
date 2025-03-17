import streamlit as st
import pandas as pd

st.title("Visualização de Dados do CSV")

df = pd.read_csv("FichaAnimal_tratado.csv")
st.dataframe(df)
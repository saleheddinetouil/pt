import streamlit as st
import requests
from PIL import Image
import google.generativeai as genai
import PIL.Image
import pathlib
import tqdm
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY");

genai.configure(api_key = API_KEY);
model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])


st.set_page_config(layout='wide')
st.title("Chat Bot 🤖🔍🌎 ")

st.markdown("teste");

aba1, aba2, aba3, aba4, aba5 = st.tabs(['Chat Bot Geral','Análise de Imagens','Análise de PDFs', 'Bot Personalizado', 'Sobre']);

with aba1:
  st.write("### Chat Bot Geral:")
  st.write("- **Pergunte o que quiser**: Diga um oi, pergunte qual a origem da roupa branca no reveillon, por que o céu é azul?, deixe a criatividade rolar solta (não use o bot para consultas de pesquisas, vá atrás para confiar as informações, sempre bom ter uma fonte confiável);")

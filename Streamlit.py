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


aba1, aba2, aba3, aba4, aba5 = st.tabs(['Chat Bot Geral','Análise de Imagens','Análise de PDFs', 'Bot Personalizado', 'Sobre']);

with aba1:
  st.write("### Chat Bot Geral:")
  st.write("- **Pergunte o que quiser**: Diga um oi, pergunte qual a origem da roupa branca no reveillon, por que o céu é azul?, deixe a criatividade rolar solta (não use o bot para consultas de pesquisas, vá atrás para confiar as informações, sempre bom ter uma fonte confiável);")

  if 'messages' not in st.session_state:
          st.session_state.messages = []

  user_input = st.text_input("Você: ", "")
  if st.button("Enviar", key="chat"):
          if user_input:
              response = chat.send_message(user_input)
              st.session_state.messages.append(("Você", user_input))
              st.session_state.messages.append(("Gemini", response.text))
          else:
              st.write("Por favor, digite uma pergunta.")

  if st.session_state.messages:
          for user, message in st.session_state.messages:
              st.write(f"**{user}**: {message}")
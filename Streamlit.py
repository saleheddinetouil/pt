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

# Incluindo estilos CSS do arquivo styles.css
def local_css(file_name):
    with open(file_name) as f:
        
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Chamando a função local_css com o nome do arquivo styles.css
local_css("./styles.css");

############# FUNÇÕES
# Função para processar o envio de mensagem do chat
def process_chat_message(user_input):
    if user_input:
        response = chat.send_message(user_input)
        st.session_state.messages.append(("Você", user_input))
        st.session_state.messages.append(("Gemini", response.text))
        st.rerun()
    else:
        st.markdown('<span id="empty-input-error">Por favor, digite uma pergunta.</span>', unsafe_allow_html=True)



#st.set_page_config(layout='wide')
st.title("Chat Bot 🤖🔍🌎 ")


aba1, aba2, aba3, aba4, aba5 = st.tabs(['Chat Bot Geral','Análise de Imagens','Análise de PDFs', 'Bot Personalizado', 'Sobre']);

with aba1:
    st.write("### Chat Bot Geral:")
    st.write("- **Pergunte o que quiser**: Diga um oi, pergunte qual a origem da roupa branca no reveillon, por que o céu é azul?, deixe a criatividade rolar solta (não use o bot para consultas de pesquisas, vá atrás para confiar as informações, sempre bom ter uma fonte confiável);")

    # Container para exibir as mensagens do chat
    chat_container = st.container()

    if 'messages' not in st.session_state:
        st.session_state.messages = []

    # Exibindo as mensagens do chat
    with chat_container:
        for user, message in st.session_state.messages:
            st.write(f"**{user}**: {message}")

    # Input do usuário
    user_input = st.text_input("Você: ", "")

    # Botão "Enviar"
    if st.button("Enviar", key="chat"):
        process_chat_message(user_input)
        user_input = "";

with aba2:
    st.write("### Análise de Imagens com IA");
    st.write("- **Envie uma imagem!**: Envie uma imagem e pergunte o que quiser sobre ela para a IA!)")

with aba3:
  st.write("### Análise de PDFs com IA");
  st.write("- **Envie um arquivo PDF!**: Envie seu currículo, um livro, revista, e pergunte sobre ele para a IA, quer um resumo? um conselho? Teste agora!")

with aba4:
  st.write("### Faça seu bot");
  st.write("- **Instrua seu bot!**: Aqui você pode costumizar seu bot instruindo o que você quer que ele incorpore, de instruções a ele. Ex: Quer que ele seja um barman? escrevas para ele o cardápio, como atender os clientes e etc. Após isso o chat ficará customizado.")

with aba5:
  st.write("### Sobre");
  st.write("- **Informações sobre o site**: Esse site foi feito através do uso da biblioteca python Streamit, usando a API do Gemini para incorporar o uso dos Bots.")
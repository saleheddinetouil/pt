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

messages = []

# Global state variable for language
if "selected_language" not in st.session_state:
    st.session_state["selected_language"] = "English"

if "selected_font_size" not in st.session_state:
    st.session_state["selected_font_size"] = "Medium"

# Incluindo estilos CSS do arquivo styles.css
def local_css(file_name):
    with open(file_name) as f:
        
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Chamando a função local_css com o nome do arquivo styles.css
local_css("./styles.css");

############# FUNÇÕES
def set_language(language):
    st.session_state["selected_language"] = language
    st.rerun()

# Função para atualizar o container
def update_chat_container():
    chat_message_html = f"""<div id="chat-area">{''.join([f'<div class="message {message_class}"><b>{user}:</b> {message}</div>' for user, message in messages])}</div>"""
    # Exibe as mensagens no Streamlit
    st.markdown(chat_message_html, unsafe_allow_html=True)

        
# Função para processar o envio de mensagem do chat
def process_chat_message(user_input):
    if user_input:
        response = chat.send_message(user_input)

        # Get the selected language
        selected_language = st.session_state["selected_language"]

        # Determine the pronoun based on language
        if selected_language == "Português": 
            pronome = "Você"
        else:
            pronome = "You"
        st.session_state.messages.append((pronome, user_input))
        st.session_state.messages.append(("Gemini", response.text))
        update_chat_container()
        st.rerun()
    else:
        st.markdown('<span id="erro">Por favor, digite alguma coisa.</span>', unsafe_allow_html=True)

def set_font_size(font_size):
    if font_size == "Small":
        st.markdown('<style>body { font-size: small; } p { font-size: small; } h1,h3 {font-size: 22px;}</style>', unsafe_allow_html=True)
    elif font_size == "Medium":
        st.markdown('<style>body { font-size: medium; } p,li,h3,ul,h1 { font-size: medium; }</style>', unsafe_allow_html=True)
    elif font_size == "Large":
        st.markdown('<style>body { font-size: large; } h3,h1 { font-size: 45px; } p {font-size: 30px;}</style>', unsafe_allow_html=True)

# Languages
with st.sidebar:
    language_options = ["English", "Português"]
    st.sidebar.title('OPTIONS 📌')
    selected_language = st.selectbox("LINGUAGEM 🌎", language_options)

    if selected_language != st.session_state["selected_language"]:
        set_language(selected_language)

# Fonts
with st.sidebar:
    font_size_options = ["Medium", "Small", "Large"]
    selected_font_size = st.selectbox("Font Size 🔍", font_size_options)
    st.image('./img/gemini.png', caption='Powered by Gemini AI')

    if selected_font_size != st.session_state["selected_font_size"]:
        set_font_size(selected_font_size)


#st.set_page_config(layout='wide')
st.title("Chat Bot 🤖💭 ")


if selected_language == "Português":
        aba1, aba2, aba3, aba4, aba5 = st.tabs(['Chat Bot Geral','Análise de Imagens','Análise de PDFs', 'Bot Personalizado', 'Sobre']);
elif selected_language == "English":
        aba1, aba2, aba3, aba4, aba5 = st.tabs(['Chat Bot Geral','Image Review','PDFs Review', 'Custom Bot', 'About']);

with aba1:
    if selected_language == "Português":
        st.write("### Chat Bot:")
        st.write("- **Pergunte o que quiser**: Diga um oi, pergunte qual a origem da roupa branca no reveillon, por que o céu é azul?, deixe a criatividade rolar solta (não use o bot para consultas de pesquisas, vá atrás para confiar as informações, sempre bom ter uma fonte confiável);")

        # Container para exibir as mensagens do chat
        chat_container = st.container()

        if 'messages' not in st.session_state:
            st.session_state.messages = []

        # Exibindo as mensagens do chat
        with chat_container:
            st.markdown('<div class="chat-container">', unsafe_allow_html=True)
            for user, message in st.session_state.messages:
                message_class = "user" if user == "Você" else "bot"
                st.markdown(f'<div class="message {message_class}"><b>{user}:</b> {message}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # Input do usuário
        user_input = st.chat_input("Diga alguma coisa... ", key = "user_input")
        if user_input:
            process_chat_message(user_input);

        
        st.markdown("<div id='chat-area' style='overflow-y: auto; max-height: 500px;'></div>", unsafe_allow_html=True)
    elif selected_language == "English":
        st.write("### Chat Bot:")
        st.write("- **Ask anything you want**: Say hello, ask where the white clothes come from on New Year's Eve, why the sky is blue, let your creativity run wild (don't use the bot for research queries, go back and trust the information, it's always good to have a reliable source).")

        # Container para exibir as mensagens do chat
        chat_container = st.container()

        if 'messages' not in st.session_state:
            st.session_state.messages = []

        # Exibindo as mensagens do chat
        with chat_container:
            st.markdown('<div class="chat-container">', unsafe_allow_html=True)
            for user, message in st.session_state.messages:
                message_class = "user" if user == "You" else "bot"
                st.markdown(f'<div class="message {message_class}"><b>{user}:</b> {message}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # Input do usuário
        user_input = st.chat_input("Write something... ", key = "user_input")
        if user_input:
            process_chat_message(user_input);
        
        st.markdown("<div id='chat-area' style='overflow-y: auto; max-height: 500px;'></div>", unsafe_allow_html=True)

with aba2:
 if selected_language == "Português":
    st.write("### Análise de Imagens com IA");
    st.write("- **Envie uma imagem!**: Envie uma imagem e pergunte o que quiser sobre ela para a IA!)")
 elif selected_language == "English":
    st.write("### XXX")
    st.write("xxx")






with aba3:
  if selected_language == "Português":
    st.write("### Análise de PDFs com IA");
    st.write("- **Envie um arquivo PDF!**: Envie seu currículo, um livro, revista, e pergunte sobre ele para a IA, quer um resumo? um conselho? Teste agora!")
  elif selected_language == "English":
    st.write("### XXX")
    st.write("xxx")








with aba4:
  if selected_language == "Português":
    st.write("### Faça seu bot");
    st.write("- **Instrua seu bot!**: Aqui você pode costumizar seu bot instruindo o que você quer que ele incorpore, de instruções a ele. Ex: Quer que ele seja um barman? escrevas para ele o cardápio, como atender os clientes e etc. Após isso o chat ficará customizado.")
  elif selected_language == "English":
    st.write("### XXX")
    st.write("xxx")









with aba5:
  # Conteúdo Dinâmico com Base no Idioma
  if selected_language == "Português":
    st.write("### Sobre");
    st.write("- **Informações sobre o site**: Esse site foi feito através do uso da biblioteca python Streamit, usando a API do Gemini para incorporar o uso dos Bots.")
    
    st.write("Esse site...")

    # Gemini
    st.image('./img/gemini.png', caption='Gemini AI')
  elif selected_language == "English":
    st.write("### About");
    st.write("- **xxxxxx**: This website was podereb by gemini")
    
    st.write("This website...")

    #Gemini
    st.image('./img/gemini.png', caption='Gemini AI')

# Necessary imports for streamlit, google api, json reading, lottie, etc.
import streamlit as st
import requests
from PIL import Image
import google.generativeai as genai
import PIL.Image
import pathlib
import tqdm
import os
import time
import json
import fitz
import tempfile
import PyPDF2
from io import BytesIO
from streamlit_lottie import st_lottie # Import for animated lottie files
from dotenv import load_dotenv

# Page layout as centered
st.set_page_config(layout="centered")

# Loading .env file (environment variables) and getting our API KEY
load_dotenv()

API_KEY = os.getenv("API_KEY");
genai.configure(api_key = API_KEY);
model = genai.GenerativeModel('gemini-1.5-flash')
chat = model.start_chat(history=[])

messages = []
image_messages = []
pdf_messages = []

### Global State Variables
if "selected_language" not in st.session_state:
    st.session_state["selected_language"] = "English"

if "selected_font_size" not in st.session_state:
    st.session_state["selected_font_size"] = "Medium"

if "selected_background" not in st.session_state:
    st.session_state["selected_background"] = "Default"

if "selected_background_messages" not in st.session_state:
    st.session_state["selected_background_messages"] = "Default"

# Importing CSS folder for global styling
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("./styles.css");

############# FUNCTIONS 
def set_language(language):
    st.session_state["selected_language"] = language

# Function to update the container
def update_chat_container():
    chat_message_html = f"""<div id="chat-area">{''.join([f'<div class="message {message_class}"><b>{user}:</b> {message}</div>' for user, message in messages])}</div>"""
    # Displays the messages in Streamlit
    st.markdown(chat_message_html, unsafe_allow_html=True)

# Function to process sending chat messages
def process_chat_message(user_input):
    if user_input:
        response = chat.send_message(user_input)

        # Selected language
        selected_language = st.session_state["selected_language"]

        if selected_language == "French":
            pronoun = "Vous"
        elif selected_language == "Darija":
            pronoun = "Nta"
        else:
            pronoun = "You"

        st.session_state.messages.append((pronoun, user_input))
        st.session_state.messages.append(("Gemini", response.text))
        update_chat_container()
        st.rerun()
    else:
        # Display error message based on selected language
        if selected_language == "French":
            error_message = "Veuillez saisir quelque chose."
        elif selected_language == "Darija":
            error_message = "Aji ktèb chi haja."
        else:
            error_message = "Please type something."
        st.markdown(f'<span id="erro">{error_message}</span>', unsafe_allow_html=True)

# Function to change the font size of the site, useful for accessibility
def set_font_size(font_size):
    if font_size == "Small":
        st.markdown('<style>body { font-size: small; } p { font-size: small; } h1,h3 {font-size: 22px;}</style>', unsafe_allow_html=True)
    elif font_size == "Medium":
        st.markdown('<style>body { font-size: medium; } p,li,h3,ul,h1 { font-size: medium; }</style>', unsafe_allow_html=True)
    elif font_size == "Large":
        st.markdown('<style>body { font-size: large; } h3,h1 { font-size: 45px; } p {font-size: 30px;} p.aviso {font-size: 27px}</style>', unsafe_allow_html=True)

# Function to change the background color of the site, useful for accessibility
def set_background(color):
    if color == "White":
        st.markdown('''<style> [data-testid="stSidebarContent"] { background-color: #D7D5CD; } [data-testid="stAppViewContainer"] { background-color: white;} 
                    [data-testid="stHeader"] { background-color: white;}  [data-testid="stSidebarCollapseButton"] { background-color: #D7D5CD;} [data-testid="stMainMenu"] { background-color: #D7D5CD;} 
                    [data-testid="main-menu-list"] { background-color: #D7D5CD;} [data-testid="stImageCaption"] {color: black} p,li,ul,h3,h1,h2,button { color: black; }</style>''', unsafe_allow_html=True)
        
    elif color == "Default": 
        st.markdown('<style></style>', unsafe_allow_html=True)

# Function to change the background color of messages, useful for accessibility
def set_background_messages(color_message):
    if color_message == "Black and White":
        st.markdown('<style> div.message.user { background-color: white; color: black} div.message.bot{ background-color: black;}</style>', unsafe_allow_html=True)
        
    elif color_message == "Default": 
        st.markdown('<style></style>', unsafe_allow_html=True)

    elif color_message == "Light Blue and Purple":
        st.markdown('<style> div.message.user { background-color: #85D4FD; color: black} div.message.bot{ background-color: purple;} </style>', unsafe_allow_html=True)
    
    elif color_message == "Light Blue and Gray":
        st.markdown('<style> div.message.user { background-color: #3797f0; color: white} div.message.bot{ background-color: gray;} </style>', unsafe_allow_html=True)

# Function to process the sent audio
def process_audio(audio_file_path, user_prompt):
        model = genai.GenerativeModel("models/gemini-1.5-pro-latest")
        audio_file = genai.upload_file(path=audio_file_path)
        response = model.generate_content(
            [
                user_prompt,
                audio_file
            ]
        )
        return response.text

# Function to temporarily save the audio file
def save_uploaded_file(uploaded_file):
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.' + uploaded_file.name.split('.')[-1]) as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                return tmp_file.name
        except Exception as e:
            st.error(f"Error: {e}")
            return None

######## Sidebars - Filters

#Language
with st.sidebar:
    language_options = ["English", "French", "Darija"]
    st.markdown('''<style> [data-testid="stMarkdownContainer"] h1 { font-size: 45px; text-shadow: 2px -2px #466EFF; }</style>''', unsafe_allow_html=True)
    st.sidebar.title('SETTINGS ⚙️')

    with open('./img/Animation.json') as f:
        lottie_animation = json.load(f)
    
    st_lottie(lottie_animation)

    selected_language = st.selectbox("LANGUAGE 🌎", language_options)

    if selected_language != st.session_state["selected_language"]:
        set_language(selected_language)

#Fonts
with st.sidebar:
    font_size_options = ["Medium", "Small", "Large"]
    selected_font_size = st.selectbox("Font Size 🔍", font_size_options)
    st.sidebar.markdown("---")
    
    if selected_font_size != st.session_state["selected_font_size"]:
        set_font_size(selected_font_size)

#Background Color
with st.sidebar:
    background_options = ["Default", "White"]
    selected_background = st.radio(" Background 🎨", background_options)

    if selected_background != st.session_state["selected_background"]:
        set_background(selected_background)

#Message-Colors
with st.sidebar:
    background_options_messages = ["Default", "Black and White", "Light Blue and Purple", "Light Blue and Gray"]
    selected_background_messages = st.radio(" Background Messages 🎨", background_options_messages)
    st.sidebar.markdown("---")
    st.image('./img/gemini.png', caption='Powered by Gemini AI')

    if selected_background_messages != st.session_state["selected_background_messages"]:
        set_background_messages(selected_background_messages)

#### Beginning of pages and use of the Bot

# stSidebarContent
st.title("Chat Bot 🤖💭 ")

# Changing the tab language according to the filter
if selected_language == "French":
    aba1, aba2, aba3, aba4, aba5 = st.tabs(['Chat Bot Général','Analyse d\'Images','Analyse de PDFs', 'Analyse Audio', 'À Propos']);
elif selected_language == "Darija":
    aba1, aba2, aba3, aba4, aba5 = st.tabs(['Chat Bot عام','تحليل الصور','تحليل PDF', 'تحليل الصوت', 'حول']);
else:
    aba1, aba2, aba3, aba4, aba5 = st.tabs(['General Chat Bot','Image Review','PDFs Review', 'Audio Review', 'About']);

with aba1:
    if selected_language == "French":
        st.write("### Chat Bot:")
        st.write(" 📍 **Demandez ce que vous voulez !** Dites bonjour, demandez d'où viennent les vêtements blancs du Nouvel An, pourquoi le ciel est bleu ?, laissez libre cours à votre créativité (n'utilisez pas le bot pour des requêtes de recherche, allez-y pour faire confiance aux informations, il est toujours bon d'avoir une source fiable) ;")
        st.markdown('<p class = aviso>Avertissement : Selon la question, le bot peut ajouter beaucoup de texte et ne pas envoyer la réponse. Soyez ponctuel. Si le bot donne une erreur, demandez-lui de résumer la réponse, cela devrait fonctionner.</p>', unsafe_allow_html=True);
        user_input_placeholder = "Dites quelque chose..."
    elif selected_language == "Darija":
        st.write("### Chat Bot:")
        st.write(" 📍 **Swel chi haja بغيتي!**  Goul salam, swel 3la asl l7wayej lbyad f l3am jdid, 3lach ssema zerga?, khali l'imagination ديالك tkhdem (ma tsta3mlsh lbot bach tchof l'information, sir chouf l'information mn source fiable, dima mezyan tkon andek source fiable);")
        st.markdown('<p class = aviso>Avis: Imken lbot izej chi text bezzaf w ma yb3atsh ljawwab. Koun précis. Ila lbot 3ta chi erreur, goul lih ykhtasar ljawwab, khas ykhdem.</p>', unsafe_allow_html=True);
        user_input_placeholder = "كتب شي حاجة..."
    else:
        st.write("### Chat Bot:")
        st.write(" 📍 **Ask anything you want!** Say hello, ask where the white clothes come from on New Year's Eve, why the sky is blue, let your creativity run wild (don't use the bot for research queries, go back and trust the information, it's always good to have a reliable source).")
        st.markdown('<p class = aviso>Note: Depending on the question, the bot may add a lot of text and not send the answer. Be punctual. If the bot gives an error, ask it to summarise the answer, it should works.</p>', unsafe_allow_html=True);
        user_input_placeholder = "Write something..."

    chat_container = st.container()

    if 'messages' not in st.session_state:
        st.session_state.messages = []

    with chat_container:
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        for user, message in st.session_state.messages:
            message_class = "user" if user == "You" or user == "Vous" or user == "Nta" else "bot"
            st.markdown(f'<div class="message {message_class}"><b>{user}:</b> {message}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    user_input = st.chat_input(user_input_placeholder, key = "user_input")
    if user_input:
        with st.spinner('Processing...'):
            process_chat_message(user_input);

    st.markdown("<div id='chat-area' style='overflow-y: auto; max-height: 500px;'></div>", unsafe_allow_html=True)

with aba2:  
    if selected_language == "French":
        st.write("### Analyse d'Images avec IA")
        st.write("📍 **Envoyez une image !**: Envoyez une image et demandez ce que vous voulez à l'IA à son sujet !")
        st.markdown("<p class = aviso >Avertissement : L'IA lit les images jusqu'à 20 Mo.</p>", unsafe_allow_html=True);
        file_uploader_label = "Choisissez une image..."
        image_caption = "Image Envoyée"
        user_input_placeholder = "Posez une question sur l'image..."
    elif selected_language == "Darija":
        st.write("### تحليل الصور بالذكاء الاصطناعي")
        st.write("📍 **أرسل صورة!**: أرسل صورة واسأل الذكاء الاصطناعي أي شيء عنها!")
        st.markdown("<p class = aviso >ملاحظة: يدعم الذكاء الاصطناعي التحميل حتى 20 ميغابايت</p>", unsafe_allow_html=True);
        file_uploader_label = "ختار صورة..."
        image_caption = "الصورة المرسلة"
        user_input_placeholder = "سؤال حول الصورة..."
    else:
        st.write("### Image Review with AI")
        st.write("📍 **Upload an image!**: Upload an image and ask the AI anything about it!")
        st.markdown("<p class = aviso>Note: IA supports up to 20MB upload</p>", unsafe_allow_html=True);
        file_uploader_label = "Choose an image..."
        image_caption = "Uploaded Image"
        user_input_placeholder = "Ask something about the image..."

    model = genai.GenerativeModel('gemini-1.5-flash') 
    uploaded_file = st.file_uploader(file_uploader_label, type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption=image_caption, use_column_width=True)
        st.write("Analyzing the image...")

        if 'image_messages' not in st.session_state:
            st.session_state.image_messages = []

        if len(st.session_state.image_messages) == 0:
            if selected_language == "French":
                st.session_state.image_messages.append(("Vous", f"Analysez cette image : {uploaded_file.name}"))
                initial_prompt = "Analysez cette image"
            elif selected_language == "Darija":
                st.session_state.image_messages.append(("Nta", f"حلل هاد الصورة: {uploaded_file.name}"))
                initial_prompt = "حلل هاد الصورة"
            else:
                st.session_state.image_messages.append(("You", f"Analyze this image: {uploaded_file.name}"))
                initial_prompt = "Analyze this image"
            response = model.generate_content([initial_prompt, image])
            response.resolve()
            st.session_state.image_messages.append(("Gemini", response.text))

        chat_container = st.container()
        with chat_container:
            st.markdown('<div class="chat-container">', unsafe_allow_html=True)
            for user, message in st.session_state.image_messages:
                message_class = "user" if user == "You" or user == "Vous" or user == "Nta" else "bot"
                st.markdown(f'<div class="message {message_class}"><b>{user}:</b> {message}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        user_input = st.chat_input(user_input_placeholder, key="image_user_input")
        if user_input:
            st.session_state.image_messages.append((user, user_input))
            response = model.generate_content([user_input, image])
            response.resolve()
            st.session_state.image_messages.append(("Gemini", response.text))
            st.rerun()

with aba3:
  if selected_language == "French":
    st.write("### Analyse de PDFs avec IA");
    st.write("📍 **Envoyez un fichier PDF !**: Envoyez votre CV, un livre, un magazine, et interrogez l'IA à ce sujet, vous voulez un résumé ? un conseil ? Testez maintenant !")
    st.markdown("<p class = aviso> En cas d'erreur de lecture, assurez-vous que votre fichier PDF est correctement formaté. L'IA lira le contenu de votre PDF, en ignorant les images. </p>", unsafe_allow_html=True);
    file_uploader_label = "Choisissez un fichier PDF..."
    user_input_placeholder = "Posez une question sur le PDF..."
  elif selected_language == "Darija":
    st.write("### تحليل ملفات PDF بالذكاء الاصطناعي");
    st.write("📍 **أرسل ملف PDF!**: أرسل سيرتك الذاتية، كتابًا، مجلة، واسأل الذكاء الاصطناعي عنها، هل تريد ملخصًا؟ نصيحة؟ جرب الآن!")
    st.markdown("<p class = aviso> في حالة وجود خطأ أثناء القراءة، تأكد من تنسيق ملف PDF بشكل صحيح. سيقرأ الذكاء الاصطناعي محتوى ملف PDF الخاص بك، متجاهلاً الصور. </p>", unsafe_allow_html=True);
    file_uploader_label = "ختار ملف PDF..."
    user_input_placeholder = "سؤال حول ملف PDF..."
  else:
    st.write("### PDF's Review with an IA");
    st.write("📍 **Send a PDF file!**: Send your resume/curriculum, a magazine, a book, ask about it to the IA, wants a summary? an advice? Try it now!")
    st.markdown("<p class = aviso> If there is an error when reading PDF file, make sure your file is correctly formatted. The AI will read the content of your PDF, ignoring images. </p>", unsafe_allow_html=True);
    file_uploader_label = "Choose a PDF File..."
    user_input_placeholder = "Ask something about the PDF..."

  uploaded_file_pdf = st.file_uploader(file_uploader_label, type=["pdf"])
    
  if uploaded_file_pdf is not None:
        pdf_bytes = BytesIO(uploaded_file_pdf.read())
        
        leitor_pdf = PyPDF2.PdfReader(pdf_bytes)

        num_paginas = len(leitor_pdf.pages)
        texto_completo = ""

        for num_pagina in range(num_paginas):
            pagina = leitor_pdf.pages[num_pagina]

            texto_pagina = pagina.extract_text()
            texto_completo += texto_pagina + "\n"

        model = genai.GenerativeModel('gemini-1.5-pro-latest')

        if 'pdf_messages' not in st.session_state:
            st.session_state.pdf_messages = []

        if len(st.session_state.pdf_messages) == 0:
            if selected_language == "French":
                st.session_state.pdf_messages.append(("Vous", f"Analysez ce PDF : {uploaded_file_pdf.name}"))
                initial_prompt = "Analysez ce PDF"
            elif selected_language == "Darija":
                st.session_state.pdf_messages.append(("Nta", f"حلل هاد PDF: {uploaded_file_pdf.name}"))
                initial_prompt = "حلل هاد PDF"
            else:
                st.session_state.pdf_messages.append(("You", f"Analyze this PDF: {uploaded_file_pdf.name}"))
                initial_prompt = "Analyze this PDF"
            response = model.generate_content([initial_prompt, texto_completo])
            response.resolve()
            st.session_state.pdf_messages.append(("Gemini", response.text))

        chat_container = st.container()
        with chat_container:
            st.markdown('<div class="chat-container">', unsafe_allow_html=True)
            for user, message in st.session_state.pdf_messages:
                message_class = "user" if user == "You" or user == "Vous" or user == "Nta" else "bot"
                st.markdown(f'<div class="message {message_class}"><b>{user}:</b> {message}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        user_input = st.chat_input(user_input_placeholder, key="pdf_user_input")
        if user_input:
            st.session_state.pdf_messages.append((user, user_input))
            response = model.generate_content([user_input, texto_completo])
            response.resolve()
            st.session_state.pdf_messages.append(("Gemini", response.text))
            st.rerun()

with aba4:
  if selected_language == "French":
    st.write("### Analyse Audio");
    st.write("📍 **Envoyez un audio !**:  Envoyez un audio et posez une question à son sujet, vous voulez un résumé d'un audio de 10 minutes ? Testez !")
    st.markdown("<p class = aviso> L'audio doit contenir des paroles, le bot analysera principalement les paroles (qui ne contiennent pas de langage explicite/obscénités !). Les audios contenant du bruit/de la musique sont susceptibles de générer une erreur. </p>", unsafe_allow_html=True);
    user_prompt_placeholder = "Que diriez-vous de... 'Résumez-moi cet audio'"
    file_uploader_label = "Envoyez votre fichier"
    button_label = "Traiter!"
    response_label = "Réponse: "
  elif selected_language == "Darija":
    st.write("### تحليل الصوت");
    st.write("📍 **أرسل مقطعًا صوتيًا!**:  أرسل مقطعًا صوتيًا واطرح سؤالًا عنه، هل تريد ملخصًا لمقطع صوتي مدته 10 دقائق؟ جرب!")
    st.markdown("<p class = aviso> يجب أن يحتوي الصوت على كلام، سيقوم البوت بتحليل الكلام بشكل أساسي (الذي لا يحتوي على لغة صريحة/فحش!). من المحتمل أن تتسبب المقاطع الصوتية التي تحتوي على ضوضاء/موسيقى في حدوث خطأ. </p>", unsafe_allow_html=True);
    user_prompt_placeholder = "شنو رأيك ف... 'لخص ليا هاد الصوت'"
    file_uploader_label = "أرسل ملفك"
    button_label = "معالجة!"
    response_label = "الجواب: "
  else:
    st.write("### Audio Review")
    st.write("📍 **Send an audio!**: Send an audio and ask a question about it, want a summary of a 10-minute audio? Try it out!")
    st.markdown("<p class = aviso> The audio must contain speech, the bot will mainly analyse speech (that doesn't contain explicit language/obscenities!). Audio that contains noise/music is likely to give an error. </p>", unsafe_allow_html=True);
    user_prompt_placeholder = "E.g., 'Please summarize the audio:'"
    file_uploader_label = "Upload Audio File"
    button_label = "Process Audio"
    response_label = "Processed Output"

  user_prompt = st.text_input("Enter your custom AI prompt:", placeholder=user_prompt_placeholder)

  audio_file = st.file_uploader(file_uploader_label, type=['wav', 'mp3'])
  if audio_file is not None:
        audio_path = save_uploaded_file(audio_file)
        st.audio(audio_path)

        if st.button(button_label):
            with st.spinner('Processing...'):
                processed_text = process_audio(audio_path, user_prompt)
                st.text_area(response_label, processed_text, height=300)

with aba5:
  if selected_language == "French":
    st.write("### À Propos");
    st.write("Ce site a été construit en utilisant la bibliothèque Streamlit de python via l'API Google Gemini, l'intelligence artificielle de Google.")
  elif selected_language == "Darija":
    st.write("### حول");
    st.write("تم بناء هذا الموقع باستخدام مكتبة Streamlit من python عبر واجهة برمجة تطبيقات Google Gemini، وهي تقنية الذكاء الاصطناعي من Google.")
  else:
    st.write("### About");
    st.write("This site was built using the Streamlit python library via the Google Gemini API, Google's artificial intelligence.")

  #Gemini
  st.image('./img/gemini.png', caption='Gemini AI')

  #Streamlit
  st.image('./img/Streamlit.png', caption='Streamlit Logo')

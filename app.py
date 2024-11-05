import streamlit as st
import ollama
from streamlit_chat import message

# Configuración de la página
st.set_page_config(
    page_title="CHAT BOT OMNISSIAH",
    page_icon="🐉",
    layout="wide"
)

# Estilo personalizado
st.markdown("""
<style>
    .stTextInput > div > div > input {
        background-color: #f0f2f6;
        color: black;
    }
    .stTextArea > div > div > textarea {
        background-color: #f0f2f6;
        color: black;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
    }
    .chat-message {
        padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex
    }
    .chat-message.user {
        background-color: #2b313e
    }
    .chat-message.bot {
        background-color: #475063
    }
    .chat-message .avatar {
      width: 20%;
    }
    .chat-message .avatar img {
      max-width: 78px;
      max-height: 78px;
      border-radius: 50%;
      object-fit: cover;
    }
    .chat-message .message {
      width: 80%;
      padding: 0 1.5rem;
      color: #fff;
    }
</style>
""", unsafe_allow_html=True)

# Título con icono de dragón
st.title("🐉 The Omnissiah")

# Inicializar el historial de chat en la sesión si no existe
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Sidebar para configuración
with st.sidebar:
    st.header("Configuración del Chatbot")
    user_defined_prompt = st.text_area(
        "Define el rol del chatbot:",
        "Eres un asistente amigable y servicial que ayuda a los usuarios con sus preguntas.",
        help="Este texto definirá cómo se comportará el chatbot."
    )

def chat_with_llama(user_input, prompt):
    full_prompt = f"{prompt}\nUser: {user_input}\nOmnissiah:"
    response = ollama.generate(model="llama3", prompt=full_prompt)
    return response.get('response', "Error: No se encontró la respuesta generada.")

# Área principal de chat
st.header("Conversa con la IA")

# Mostrar el historial de chat
for i, chat in enumerate(st.session_state.chat_history):
    if i % 2 == 0:
        message(chat, is_user=True, key=f"user_msg_{i}")
    else:
        message(chat, is_user=False, key=f"bot_msg_{i}")

# Función para manejar el envío del mensaje
def handle_send():
    if st.session_state.user_input:
        user_message = st.session_state.user_input
        st.session_state.chat_history.append(user_message)

        with st.spinner('El Omnissiah está pensando...'):
            response = chat_with_llama(user_message, user_defined_prompt)

        st.session_state.chat_history.append(response)
        st.session_state.user_input = ""  # Limpiar el campo de texto después de enviar

# Campo de entrada del usuario con la tecla Enter para enviar
user_input = st.text_input("Escribe tu mensaje aquí:", key="user_input", on_change=handle_send)

# Botón para limpiar el historial
if st.button("Limpiar Conversación"):
    st.session_state.chat_history = []  # Limpiar el historial sin recargar la página

# Mensaje de salida
st.markdown("---")
st.info("Escribe 'salir' para terminar la conversación.")

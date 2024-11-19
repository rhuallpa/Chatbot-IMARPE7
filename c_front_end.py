import streamlit as st
import b_backend  # Importar el backend actualizado

# Configuración de la página
st.set_page_config(page_title="IMARPE Chatbot y Excel Analyzer", layout="centered")

# Estilo CSS personalizado para centrar el contenido
st.markdown(
    """
    <style>
    .main-title {
        text-align: center;
        font-size: 32px;
        color: #028090;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .footer {
        text-align: center;
        font-size: 12px;
        color: #666665;
        margin-top: 20px;
    }
    .st-chat {
        max-width: 800px;
        margin: auto;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Título de la aplicación
st.markdown("<h2 class='main-title'>🤖 E.M.A.i-iMAR-1 Bot - Análisis y Consultas Especializadas - IMARPE ⛵🐟 🐬</h2>", unsafe_allow_html=True)

# Inicializar el historial de mensajes en la sesión
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {
            "role": "assistant",
            "content": "👋 ¡Hola! Soy **E.M.A.i-iMAR-1 Bot**, un asistente experto en **análisis científico y tecnológico del mar** para IMARPE 🌊. Estoy aquí para ofrecerte **información precisa, educativa y basada en datos relevantes** sobre temas relacionados con los estudios marinos y acuícolas. ¿En qué puedo ayudarte hoy?"
        }
    ]

# Mostrar el historial de mensajes en una sección centrada
st.markdown("<hr>", unsafe_allow_html=True)  # Línea divisoria para estilo
with st.container():
    for msg in st.session_state["messages"]:
        if msg["role"] == "assistant":
            # Respuesta del asistente con formato Markdown
            st.chat_message("assistant").markdown(msg["content"], unsafe_allow_html=True)
        else:
            # Pregunta del usuario como texto simple
            st.chat_message("user").write(msg["content"])

# Entrada del usuario
user_input = st.chat_input("Escribe tu consulta aquí...")
if user_input:
    # Añadir la consulta del usuario al historial
    st.session_state["messages"].append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    # Llamar al backend para procesar la consulta
    with st.spinner("Procesando..."):
        try:
            respuesta = b_backend.consulta(user_input, st.session_state["messages"])
        except Exception as e:
            respuesta = f"⚠️ **Error:** {str(e)}"

    # Añadir la respuesta del asistente al historial
    st.session_state["messages"].append({"role": "assistant", "content": respuesta})
    st.chat_message("assistant").markdown(respuesta, unsafe_allow_html=True)

# Pie de página con información
st.markdown(
    """
    <div class='footer'>
        © 2024 E.M.A.i-iMAR-1 Bot - Todos los derechos reservados.
    </div>
    """,
    unsafe_allow_html=True
)

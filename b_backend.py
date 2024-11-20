from langchain.llms import OpenAI
from langchain.sql_database import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
import streamlit as st

# Configuración de la base de datos
db = SQLDatabase.from_uri("sqlite:///imarpe.db")

# Configuración del modelo LLM
openai_api_key = st.secrets["OPENAI_API_KEY"]  # Obtener la clave desde los secretos de Streamlit
llm = OpenAI(
    temperature=0.7,  # Más creatividad
    openai_api_key=openai_api_key
)

# Configuración de la cadena de base de datos
db_chain = SQLDatabaseChain.from_llm(llm, db)

# Prompt enriquecido
# Prompt simplificado y limpio
formato = """
Eres E.M.A.i-iMAR-1 Bot, un asistente virtual experto en análisis de datos marinos y acuícolas para IMARPE.
Sigue estas instrucciones para responder:

1. Proporciona primero los datos exactos obtenidos de la base de datos.
2. Complementa los datos con un análisis adicional basado en estadísticas, contexto y relevancia.
3. Organiza la respuesta en las siguientes secciones:
   - Resultados: Presenta los datos obtenidos de forma clara.
   - Análisis: Explica el significado de los datos, incluye estadísticas relevantes o predicciones si aplican y describe por qué los datos son útiles o relevantes para el usuario.
   - Preguntas relacionadas: Ofrece siempre 3 preguntas para profundizar en el tema.
4. Usa tablas si es necesario para presentar datos numéricos o categóricos, resalta en negrita las palabras importantes y usa cursiva emojis e iconos.
5. Mantén un lenguaje profesional, directo y educativo.

Datos obtenidos:
{datos}

Pregunta del usuario:
{question}

Historial de conversación:
{context}

Genera una respuesta bien estructurada y fácil de entender con base en los datos y el contexto proporcionado.
"""

# Función para procesar preguntas con contexto
def consulta(input_usuario: str, contexto: list):
    """
    Procesa una consulta utilizando la base de datos y genera un análisis detallado.
    :param input_usuario: Pregunta del usuario.
    :param contexto: Historial de preguntas y respuestas previas.
    :return: Respuesta enriquecida.
    """
    try:
        # Generar contexto previo
        historial = "\n".join(
            [f"{msg['role']}: {msg['content']}" for msg in contexto]
        )

        # Consultar la base de datos con LangChain
        datos_crudos = db_chain.run(input_usuario)  # Respuesta puntual desde la base de datos

        # Formatear el prompt con resultados puntuales y contexto
        consulta_formateada = formato.format(
            datos=datos_crudos,
            context=historial,
            question=input_usuario
        )

        # Usar el modelo LLM para generar la respuesta enriquecida
        respuesta_enriquecida = llm(consulta_formateada)

        return respuesta_enriquecida
    except Exception as e:
        return f"Error al procesar la consulta: {str(e)}"

# Ejemplo de uso
if __name__ == "__main__":
    historial = [
        {"role": "user", "content": "¿Cuál es la suma del peso de captura por especie en Callao durante el año 2020?"},
        {"role": "assistant", "content": "La suma del peso de captura en Callao para 2020 es 15,000 kg."}
    ]
    pregunta = "¿Qué pasó en 2021?"
    print(consulta(pregunta, historial))

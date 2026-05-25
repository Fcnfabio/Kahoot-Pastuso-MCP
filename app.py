import streamlit as st
from embeddings import EmbeddingIndex
from rag import QuizRAG
from llm import call_llm

st.set_page_config(page_title="Juego Pastuso 🎮")

# 🔧 Panel de desarrollo (solo visible en modo debug)
with st.sidebar:
    st.header("🔧 Desarrollo")
    debug_llm = st.checkbox("🤖 Forzar LLM en feedback", value=False, help="Activa para usar siempre el LLM y ver logs")
    
    3if debug_llm:
        st.info("💡 Modo debug: Cada feedback usará el LLM")
        st.caption("Revisa la terminal para ver respuestas y errores del LLM")

@st.cache_resource
def load_game():
    index = EmbeddingIndex("data.json")
    return QuizRAG(index, call_llm)

game = load_game()

# 🧠 estado inicial
if "pregunta" not in st.session_state:
    st.session_state.pregunta = game.generar_pregunta()
    st.session_state.score = 0
    st.session_state.respondido = False

pregunta = st.session_state.pregunta

st.title("🎮 Adivina la palabra pastusa")

st.write("### Definición:")
st.info(pregunta["definicion"])

opcion = st.radio(
    "Elige la correcta:",
    pregunta["opciones"],
    key="opcion_actual"
)

# 🎯 BOTÓN RESPONDER
if not st.session_state.respondido:
    if st.button("Responder"):
        correcta = opcion == pregunta["respuesta"]
        
        st.session_state.respondido = True
        
        if correcta:
            st.session_state.score += 10
            st.success("✅ Correcto!")
        else:
            st.session_state.score -= 5
            st.error(f"❌ Era: {pregunta['respuesta']}")
        
        # 🔥 Generar feedback con soporte para modo debug
        feedback = game.generar_feedback(
            correcta, 
            pregunta["respuesta"],
            debug=debug_llm  # ← Pasar flag de debug
        )
        st.write(feedback)

# 👉 MOSTRAR RESULTADO SI YA RESPONDIÓ
if st.session_state.respondido:
    st.write("---")
    
    if st.button("➡️ Siguiente"):
        st.session_state.pregunta = game.generar_pregunta()
        st.session_state.respondido = False
        st.rerun()

st.write(f"### 🏆 Puntaje: {st.session_state.score}")
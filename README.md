# 🎮 Kahoot Pastuso - Juego con RAG + LLM

Un juego interactivo tipo Kahoot construido con **Streamlit**, usando **RAG (Retrieval-Augmented Generation)** para generar preguntas y distractores inteligentes a partir de un dataset de palabras pastusas.

---

## 🚀 Características

- 🎮 Modo Kahoot con temporizador en tiempo real
- 🧠 Generación de preguntas usando RAG
- 🎯 Distractores inteligentes (mezcla de similares + aleatorios)
- 🤖 Integración con LLM vía OpenRouter (modelos gratuitos)
- ⚡ Sistema de puntuación basado en velocidad
- 🔄 Flujo automático entre preguntas
- 🔐 API Key segura con `.env`

---

## 🧱 Arquitectura del proyecto

```
/project
├── app.py              # Interfaz Streamlit (juego)
├── rag.py              # Lógica de preguntas y feedback
├── embeddings.py       # RAG + FAISS + fastembed
├── llm.py              # Cliente OpenRouter
├── data.json           # Dataset de palabras
├── requirements.txt
├── .env                # API Key (no subir a git)
└── README.md
```

---

## ⚙️ Instalación

### 1. Clonar el proyecto

```bash
git clone <repo>
cd <repo>
```

### 2. Crear entorno virtual

```bash
python -m venv venv
source venv/bin/activate  # Linux / Mac
venv\Scripts\activate     # Windows
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

---

## 🔑 Configuración de API Key

Crea un archivo `.env` en la raíz del proyecto:

```env
OPENROUTER_API_KEY=sk-or-v1-xxxxxxxxxxxxxxxx
```

---

## ▶️ Ejecutar la aplicación

```bash
streamlit run app.py
```

---

## 🎮 Cómo funciona

1. Se selecciona una palabra aleatoria del dataset
2. Se usa RAG (FAISS + embeddings) para encontrar palabras similares
3. Se generan opciones:
   - ✅ 1 correcta
   - 🎯 1 similar (difícil)
   - 🎲 2 aleatorias (balance)
4. El usuario responde antes de que se acabe el tiempo
5. Se asignan puntos según rapidez

---

## 🧠 Tecnologías usadas

| Tecnología | Uso |
|---|---|
| **Streamlit** | Interfaz de usuario |
| **FAISS** | Búsqueda vectorial |
| **fastembed** | Embeddings rápidos |
| **OpenRouter** | LLM (modelos gratuitos) |
| **python-dotenv** | Manejo de variables de entorno |

---

## ⚡ Modo Kahoot

- ⏱️ Temporizador dinámico
- 📊 Barra de progreso
- ⚡ Puntos por velocidad
- 🔄 Auto-siguiente pregunta
- 🎯 Feedback inmediato

---

## 🛠️ Posibles mejoras

- 🏆 Leaderboard global
- 👥 Multiplayer
- 🎨 UI tipo Kahoot (botones grandes y colores)
- 🔊 Sonidos
- 🧠 Dificultad progresiva
- 📱 Versión móvil

---

## ⚠️ Notas

- No subir `.env` al repositorio
- Modelos LLM gratuitos pueden tener rate limit (429)
- Se implementa fallback automático de modelos

---

## 📦 Deploy

Se puede desplegar fácilmente en:

- Streamlit Cloud
- Railway
- VPS (Ubuntu recomendado)

---

## 👨‍💻 Autor

Proyecto construido como sistema RAG aplicado a un juego interactivo educativo.

---

## ⭐ Licencia

MIT

---
## 👨‍💻 Autor

**Ing. Cristian Díaz**

<p align="center">
  <img width="300" src="https://i.imgur.com/a7YBcsp.png">
</p>
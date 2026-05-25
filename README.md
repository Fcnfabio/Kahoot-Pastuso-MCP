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
- 🔗 **NUEVO:** Conexión MCP con GitHub para automatización

---

## 🧱 Arquitectura del proyecto

```
/project
├── app.py              # Interfaz Streamlit (juego)
├── rag.py              # Lógica de preguntas y feedback
├── embeddings.py       # RAG + FAISS + fastembed
├── llm.py              # Cliente OpenRouter
├── mcp_github_client.py # Cliente MCP para conexión con GitHub
├── data.json           # Dataset de palabras
├── mcp.json            # Configuración MCP (no subir a git)
├── requirements.txt
├── .env                # API Keys (no subir a git)
├── README.md
└── README_MCP.md       # Documentación de MCP
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
GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxxxxxxx
```

> **Nota:** El `GITHUB_TOKEN` es opcional, solo necesario si quieres usar las funcionalidades MCP con GitHub.

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

## 🔗 MCP con GitHub

Este proyecto incluye integración con **Model Context Protocol (MCP)** para conectar con GitHub. Esto permite:

- Usar herramientas de GitHub directamente desde clientes MCP compatibles (como Claude Desktop)
- Automatizar tareas de repositorio
- Crear issues, pull requests, y más

Para más detalles, ver [README_MCP.md](README_MCP.md).

## ⚠️ Notas

- No subir `.env` ni `mcp.json` al repositorio
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
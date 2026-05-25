import requests
import json
import time
import os
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# 🔥 Validar que la API key esté configurada
if not OPENROUTER_API_KEY:
    print("⚠️  WARNING: OPENROUTER_API_KEY no está configurada en .env")
    print("   El LLM no funcionará hasta que agregues tu clave de OpenRouter")

MODELOS = [
    "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free", # 🔥 principal (rápido)
    "meta-llama/llama-3-8b-instruct:free",   # 🔁 fallback
    "nvidia/nemotron-3-super-120b-a12b:free" # 🧠 último recurso
]

def call_llm(prompt, max_retries=5):
    # 🔥 Validar API key antes de intentar llamada
    if not OPENROUTER_API_KEY:
        print("❌ call_llm: OPENROUTER_API_KEY no configurada")
        return "😅 Configura tu API key de OpenRouter en .env"
    
    url = "https://openrouter.ai/api/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/tu-usuario/kahoot-pastuso",  # 🔥 Requerido por OpenRouter
        "X-Title": "Kahoot Pastuso",  # 🔥 Requerido por OpenRouter
    }
    
    for attempt in range(max_retries):
        model = MODELOS[attempt % len(MODELOS)]
        
        payload = {
            "model": model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7
        }
        
        try:
            response = requests.post(
                url,
                headers=headers,
                data=json.dumps(payload)
            )
            
            # 🔥 manejo de rate limit
            if response.status_code == 429:
                print(f"⚠️ Rate limit con {model}")
                time.sleep(2 + attempt * 2)
                continue
            
            if response.status_code != 200:
                error_msg = response.text[:200] if len(response.text) > 200 else response.text
                print(f"❌ HTTP {response.status_code} con {model}: {error_msg}")
                
                # 🔥 Log específico para errores de autenticación
                if response.status_code in [401, 403]:
                    print("💡 Verifica que tu OPENROUTER_API_KEY sea válida")
                continue
            
            res_json = response.json()
            
            if "error" in res_json:
                print("❌ OpenRouter error:", res_json)
                continue
            
            return res_json["choices"][0]["message"]["content"]
        
        except requests.exceptions.ConnectionError:
            print("❌ Error de conexión: verifica tu internet o que openrouter.ai esté disponible")
            time.sleep(2)
        except requests.exceptions.Timeout:
            print("❌ Timeout: la API tardó mucho en responder")
            time.sleep(2)
        except Exception as e:
            print(f"❌ Exception inesperada ({type(e).__name__}): {str(e)}")
            time.sleep(1)
    
    # 🔥 fallback final (NUNCA romper la app)
    return "😅 El pastuso se quedó pensando... intenta otra vez"
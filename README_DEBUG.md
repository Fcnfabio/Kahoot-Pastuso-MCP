# 🔧 Guía de Debug para el LLM

Este documento te ayuda a diagnosticar y solucionar problemas con la conexión al LLM en tu proyecto Kahoot-Pastuso.

---

## 🚀 Cambios Recientes Aplicados

### 1. `rag.py` - Feedback con modo debug
- ✅ Nuevo parámetro `debug=False` en `generar_feedback()`
- ✅ Logs detallados cuando falla la llamada al LLM
- ✅ Captura de excepciones específicas (no genéricas)

### 2. `llm.py` - Conexión robusta
- ✅ Validación temprana de `OPENROUTER_API_KEY`
- ✅ Headers adicionales requeridos por OpenRouter (`HTTP-Referer`, `X-Title`)
- ✅ Manejo específico de errores de conexión y timeout
- ✅ Logs más informativos con códigos de estado HTTP

### 3. `app.py` - Panel de debug en Streamlit
- ✅ Checkbox "🤖 Forzar LLM en feedback" en la barra lateral
- ✅ Cuando está activo: 100% de los feedbacks usan el LLM
- ✅ Mensajes informativos en la UI

### 4. `test_llm.py` - Script de prueba independiente
- ✅ Ejecutable desde terminal: `python test_llm.py`
- ✅ Prueba 3 escenarios diferentes con el LLM
- ✅ Muestra errores claramente si la API no responde

---

## 🛠️ Cómo Diagnosticar Problemas

### Paso 1: Verificar tu `.env`

Asegúrate de tener esto en `C:\Users\crist\OneDrive\Documentos\Campus\D3\Kahoot-Pastuso\.env`:

```env
OPENROUTER_API_KEY=sk-or-v1-tu-clave-real-aqui
```

⚠️ **Importante**: 
- Sin comillas alrededor de la clave
- Sin espacios antes o después del `=`
- La clave debe ser válida y activa en [openrouter.ai/keys](https://openrouter.ai/keys)

### Paso 2: Probar con el script independiente

```bash
cd C:\Users\crist\OneDrive\Documentos\Campus\D3\Kahoot-Pastuso
python test_llm.py
```

**Resultados esperados:**
- ✅ Si ves respuestas en dialecto pastuso → **Todo funciona** 🎉
- ❌ Si ves "Configura tu API key" → Revisa tu `.env`
- ❌ Si ves errores HTTP 401/403 → Tu clave es inválida o expiró
- ❌ Si ves errores de conexión → Verifica tu internet o firewall

### Paso 3: Probar en Streamlit con modo debug

1. Ejecuta la app:
   ```bash
   streamlit run app.py
   ```

2. En la barra lateral (izquierda), activa:
   ```
   ☑️ 🤖 Forzar LLM en feedback
   ```

3. Responde una pregunta del juego

4. **Revisa la terminal** donde ejecutaste Streamlit:
   - Deberías ver logs como: `🤖 LLM Response: [respuesta del modelo]`
   - Si hay errores, verás: `⚠️ Error al llamar LLM: [detalles]`

### Paso 4: Interpretar los logs

| Mensaje en terminal | Significado | Solución |
|---------------------|-------------|----------|
| `⚠️ WARNING: OPENROUTER_API_KEY no está configurada` | Falta la variable en `.env` | Agrega tu clave al archivo `.env` |
| `❌ HTTP 401` o `❌ HTTP 403` | Clave inválida o sin permisos | Regenera tu clave en OpenRouter |
| `❌ HTTP 429` | Rate limit (muchas peticiones) | Espera unos segundos, el código ya hace retry automático |
| `❌ Error de conexión` | Problema de red o DNS | Verifica internet, firewall, o que openrouter.ai esté online |
| `❌ Timeout` | La API tardó mucho | El código ya hace retry, pero verifica tu conexión |
| `🤖 LLM Response: ...` | ✅ Todo funcionando | ¡Disfruta tu app! |

---

## 🔁 Flujo Normal de Ejecución

```
Usuario responde pregunta
        ↓
rag.py: generar_feedback(correcta, palabra, debug=False)
        ↓
¿debug=True o random >= 0.8?
        ↓
   ┌────┴────┐
   ↓         ↓
[80%]      [20% o debug]
Local       LLM
   ↓         ↓
Frases    call_llm(prompt)
predefinidas   ↓
   ↓     ¿API Key válida?
Retorno   ↓
inmediato  Sí → Llama a OpenRouter
              ↓
           ¿Respuesta 200?
              ↓
        ┌─────┴─────┐
        ↓           ↓
      [Sí]        [No]
        ↓           ↓
   Retorna     Reintenta con
   respuesta   siguiente modelo
   del LLM         ↓
              ¿Agotó retries?
                 ↓
           ┌─────┴─────┐
           ↓           ↓
         [Sí]        [No]
           ↓           ↓
   Retorna fallback  Continúa retry
   "😅 El pastuso..."
```

---

## 💡 Tips para Desarrollo

### Forzar 100% LLM temporalmente

Edita `rag.py` línea ~55:
```python
# Cambia esto:
usar_llm = debug or (random.random() >= 0.8)

# Por esto (solo para testing):
usar_llm = True  # ← Fuerza siempre el LLM
```

### Ver logs en tiempo real

Ejecuta Streamlit y mantén abierta la terminal:
```bash
streamlit run app.py
```

Los prints de `llm.py` y `rag.py` aparecerán ahí, no en la interfaz web.

### Limpiar caché de Streamlit

Si haces cambios y no se reflejan:
```bash
# Cierra Streamlit y elimina caché
rm -r .streamlit/cache  # o borra la carpeta manualmente
streamlit run app.py
```

---

## ❓ Preguntas Frecuentes

**¿Por qué a veces no veo la respuesta del LLM en la web?**
> Porque el 80% del tiempo usa frases locales predefinidas. Activa el checkbox de debug para forzar el LLM.

**¿Los `print()` se ven en Streamlit?**
> No, solo en la terminal donde ejecutaste `streamlit run`. Por eso agregamos logs específicos.

**¿Puedo usar esto en producción?**
> Sí, pero considera:
> - Guardar logs en archivo en lugar de solo print()
> - Implementar métricas de uso del LLM
> - Agregar un sistema de cache para respuestas repetidas

**¿Qué hago si OpenRouter cambia su API?**
> Revisa [su documentación](https://openrouter.ai/docs) y actualiza `llm.py` según sea necesario.

---

## 🆘 ¿Sigue sin funcionar?

1. Ejecuta `python test_llm.py` y copia el output completo
2. Verifica que tu clave de OpenRouter tenga créditos o esté en modo free
3. Revisa que tu firewall/antivirus no bloquee `openrouter.ai`
4. Si usas proxy/VPN, asegúrate de que permita conexiones HTTPS

Si necesitas más ayuda, comparte:
- El output de `test_llm.py`
- Tu versión de Python (`python --version`)
- El contenido de tu `.env` (ocultando la clave real: `OPENROUTER_API_KEY=sk-or-v1-***`)

#!/usr/bin/env python3
"""
🔍 Script de prueba para verificar la conexión con el LLM
Ejecutar: python test_llm.py
"""

from llm import call_llm
import sys

def test_llm_connection():
    print("🔍 Probando conexión con OpenRouter API...\n")
    
    # Test 1: Saludo básico
    print("📝 Test 1: Saludo en pastuso")
    respuesta = call_llm("Saluda como pastuso en una frase muy corta")
    print(f"✅ Respuesta: {respuesta}\n")
    
    # Test 2: Felicitación
    print("📝 Test 2: Felicitación por acierto")
    respuesta = call_llm("Responde como pastuso, corto y gracioso felicitando por acertar 'chimba'")
    print(f"✅ Respuesta: {respuesta}\n")
    
    # Test 3: Burla amigable
    print("📝 Test 3: Burla amigable por error")
    respuesta = call_llm("Responde como pastuso, gracioso burlándote por fallar 'guayabo'")
    print(f"✅ Respuesta: {respuesta}\n")
    
    print("✨ ¡Pruebas completadas!")
    print("\n💡 Si ves respuestas en dialecto pastuso, tu conexión con el LLM funciona correctamente.")
    print("💡 Si ves el mensaje de fallback, revisa tu OPENROUTER_API_KEY en .env")

if __name__ == "__main__":
    try:
        test_llm_connection()
    except KeyboardInterrupt:
        print("\n⚠️  Cancelado por usuario")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error inesperado: {type(e).__name__}: {e}")
        sys.exit(1)

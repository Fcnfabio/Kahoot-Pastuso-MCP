import random

class QuizRAG:
    def __init__(self, embedding_index, llm_fn):
        self.index = embedding_index
        self.llm = llm_fn
        self.data = embedding_index.data
    
    def generar_pregunta(self):
        correcta = random.choice(self.data)
        
        definicion = correcta["definicion"]
        
        # 🔥 1. similares (difícil)
        similares = self.index.buscar_similares(definicion, k=10)
        
        distractores_similares = [
            item["palabra"]
            for item in similares
            if item["palabra"] != correcta["palabra"]
        ]
        
        # 🔥 2. aleatorios (fácil / control)
        aleatorios = [
            item["palabra"]
            for item in self.data
            if item["palabra"] != correcta["palabra"]
        ]
        
        random.shuffle(aleatorios)
        
        # 🔥 mezcla inteligente
        distractores = []
        
        # 1 similar + 2 random → balance perfecto
        if distractores_similares:
            distractores.append(distractores_similares[0])
        
        distractores += aleatorios[:2]
        
        opciones = [correcta["palabra"]] + distractores
        random.shuffle(opciones)
        
        return {
            "definicion": definicion,
            "opciones": opciones,
            "respuesta": correcta["palabra"]
        }
    
    def generar_feedback(self, correcto, palabra, debug=False):
        """
        Genera feedback para el usuario.
        
        Args:
            correcto: bool - si la respuesta fue correcta
            palabra: str - la palabra correcta
            debug: bool - si True, fuerza uso del LLM para testing
        """
        # 🔥 Modo debug: forzar LLM para testing
        usar_llm = debug or (random.random() >= 0.8)
        
        if not usar_llm:
            # 🔥 80% local (rápido y gratis)
            if correcto:
                return random.choice([
                    "😄 ¡Bien ahí pues!",
                    "🔥 ¡Ese sí sabe!",
                    "👏 ¡Correcto, mi llave!",
                    "💯 ¡De una!"
                ])
            else:
                return f"😅 Era {palabra}, pilas pues"
        
        # 🔥 20% LLM (variedad) o 100% si debug=True
        try:
            if correcto:
                prompt = f"Responde como pastuso, corto y gracioso felicitando por acertar '{palabra}'"
            else:
                prompt = f"Responde como pastuso, gracioso burlándote por fallar '{palabra}'"
            
            respuesta = self.llm(prompt)
            
            # 🔥 Log para desarrollo (se ve en terminal)
            if debug:
                print(f"🤖 LLM Response: {respuesta}")
            
            return respuesta
        
        except Exception as e:
            # 🔥 Muestra error en consola para debugging
            print(f"⚠️ Error al llamar LLM: {type(e).__name__}: {str(e)}")
            
            # 🔥 Retorna fallback sin romper la app
            return "😄 ¡Bien!" if correcto else f"😅 Era {palabra}"
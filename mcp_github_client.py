#!/usr/bin/env python3
"""
Cliente MCP para conectar con GitHub.
Este script permite usar el Model Context Protocol para interactuar con GitHub.
"""

import json
import os
import subprocess
import sys
import time
from typing import Optional

class MCPGitHubClient:
    """Cliente para interactuar con GitHub a través de MCP."""
    
    def __init__(self, token: str):
        """
        Inicializa el cliente MCP de GitHub.
        
        Args:
            token: Token personal de GitHub (ghp_...)
        """
        self.token = token
        self.process: Optional[subprocess.Popen] = None
        self.request_id = 0
        
    def start_server(self):
        """Inicia el servidor MCP de GitHub."""
        print("🚀 Iniciando servidor MCP de GitHub...")
        
        env = os.environ.copy()
        env["GITHUB_PERSONAL_TOKEN"] = self.token
        
        self.process = subprocess.Popen(
            ["npx", "-y", "@modelcontextprotocol/server-github"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env,
            text=True
        )
        
        print("✅ Servidor MCP de GitHub iniciado")
        return self.process
    
    def _next_id(self) -> int:
        """Genera un ID único para la solicitud."""
        self.request_id += 1
        return self.request_id
    
    def send_request(self, method: str, params: dict) -> dict:
        """
        Envía una solicitud al servidor MCP.
        
        Args:
            method: Nombre del método a llamar
            params: Parámetros del método
            
        Returns:
            Respuesta del servidor
        """
        if not self.process:
            raise RuntimeError("El servidor no está iniciado. Llama a start_server() primero.")
        
        request = {
            "jsonrpc": "2.0",
            "id": self._next_id(),
            "method": method,
            "params": params
        }
        
        request_str = json.dumps(request) + "\n"
        self.process.stdin.write(request_str)
        self.process.stdin.flush()
        
        response_str = self.process.stdout.readline()
        if not response_str:
            raise RuntimeError("No se recibió respuesta del servidor")
        
        return json.loads(response_str)
    
    def list_tools(self) -> dict:
        """Lista todas las herramientas disponibles."""
        print("🔍 Obteniendo lista de herramientas disponibles...")
        return self.send_request("tools/list", {})
    
    def call_tool(self, name: str, arguments: dict) -> dict:
        """
        Llama a una herramienta específica.
        
        Args:
            name: Nombre de la herramienta
            arguments: Argumentos para la herramienta
            
        Returns:
            Resultado de la herramienta
        """
        print(f"🔧 Llamando herramienta: {name}")
        return self.send_request("tools/call", {
            "name": name,
            "arguments": arguments
        })
    
    def test_connection(self):
        """Prueba la conexión con GitHub."""
        print("\n🔍 Probando conexión con GitHub...")
        
        try:
            # Listar herramientas disponibles
            tools_result = self.list_tools()
            
            if "result" in tools_result and "tools" in tools_result["result"]:
                tools = tools_result["result"]["tools"]
                print(f"✅ Servidor MCP conectado exitosamente!")
                print(f"\n📝 Herramientas disponibles ({len(tools)}):")
                
                for tool in tools:
                    name = tool.get("name", "desconocida")
                    description = tool.get("description", "Sin descripción")
                    print(f"   • {name}: {description}")
                
                return True
            else:
                print(f"❌ Error en la conexión: {tools_result}")
                return False
                
        except Exception as e:
            print(f"❌ Error al probar conexión: {e}")
            return False
    
    def test_github_api(self):
        """Prueba una llamada real a la API de GitHub."""
        print("\n🔍 Probando llamada a API de GitHub...")
        
        try:
            # Listar herramientas primero para verificar autenticación
            result = self.call_tool("list_repositories", {"username": ""})
            
            if "result" in result:
                print("✅ Llamada a API de GitHub exitosa!")
                return True
            else:
                print(f"❌ Error en llamada: {result}")
                return False
                
        except Exception as e:
            print(f"❌ Error al llamar API: {e}")
            return False
    
    def stop_server(self):
        """Detiene el servidor MCP."""
        if self.process:
            self.process.terminate()
            self.process.wait()
            print("\n🛑 Servidor MCP detenido")


def main():
    """Función principal para probar la conexión MCP con GitHub."""
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        print("❌ Error: La variable de entorno GITHUB_TOKEN no está configurada.")
        print("   Configura tu token en el archivo .env o exporta la variable:")
        print("   export GITHUB_TOKEN='tu_token_aqui'")
        sys.exit(1)
    
    print("🎮 Kahoot Pastuso - Cliente MCP GitHub")
    print("=" * 50)
    
    client = MCPGitHubClient(token)
    
    try:
        client.start_server()
        
        # Pequeña pausa para que el servidor se inicialice
        time.sleep(2)
        
        if client.test_connection():
            print("\n🎉 ¡Conexión MCP con GitHub establecida exitosamente!")
            print("\n💡 El archivo mcp.json está configurado para usar este servidor.")
            print("   Puedes usar clientes MCP compatibles (como Claude Desktop) para conectar.")
            
            # Preguntar si quiere probar una llamada real
            print("\n" + "=" * 50)
            response = input("¿Quieres probar una llamada real a GitHub? (s/n): ").lower()
            
            if response == 's':
                client.test_github_api()
        else:
            print("\n❌ No se pudo establecer la conexión con GitHub.")
            
    except KeyboardInterrupt:
        print("\n\n👋 Interrumpido por el usuario")
    except Exception as e:
        print(f"\n❌ Error: {e}")
    finally:
        client.stop_server()


if __name__ == "__main__":
    main()
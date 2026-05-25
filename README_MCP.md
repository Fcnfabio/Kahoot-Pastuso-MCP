# 🔗 Configuración MCP con GitHub

Este documento explica cómo configurar y usar el Model Context Protocol (MCP) para conectar con GitHub.

## 📋 Requisitos Previos

1. **Node.js** instalado (para usar `npx`)
2. **Token de GitHub** (Personal Access Token)
3. **Python 3.7+** (para el script cliente)

## 🚀 Instalación del Servidor MCP de GitHub

El servidor MCP de GitHub ya está instalado globalmente:

```bash
npm install -g @modelcontextprotocol/server-github
```

## 🔑 Configuración de Credenciales

### Opción 1: Usando el archivo `.env` (Recomendado)

1. Crea un archivo `.env` en la raíz del proyecto:

```bash
cp .env.example .env
```

2. Edita `.env` y agrega tu token de GitHub:

```env
OPENROUTER_API_KEY=tu_api_key_aqui
GITHUB_TOKEN=ghp_tu_token_personal_aqui
```

### Opción 2: Usando variables de entorno

```bash
export GITHUB_TOKEN="ghp_tu_token_personal_aqui"
```

## 📁 Archivos de Configuración

### `mcp.json`

Este archivo configura el servidor MCP para que clientes compatibles (como Claude Desktop) puedan conectarse:

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_TOKEN": "ghp_tu_token_aqui"
      }
    }
  }
}
```

**⚠️ Importante:** Este archivo contiene el token y está en `.gitignore` para no subirse al repositorio.

### `.gitignore`

Los siguientes archivos están protegidos y no se suben al repositorio:
- `.env` - Contiene credenciales sensibles
- `mcp.json` - Contiene el token de GitHub

## 🧪 Probando la Conexión

### Usando el script cliente Python

1. Asegúrate de tener el token en el `.env` o exportado:

```bash
export GITHUB_TOKEN="ghp_tu_token_aqui"
```

2. Ejecuta el script de prueba:

```bash
python3 mcp_github_client.py
```

3. El script mostrará:
   - Lista de herramientas MCP disponibles
   - Opción de probar una llamada real a GitHub

### Herramientas MCP Disponibles

El servidor MCP de GitHub proporciona las siguientes herramientas:

- `list_repositories` - Lista repositorios de un usuario
- `search_repositories` - Busca repositorios
- `get_repository` - Obtiene información de un repositorio
- `create_issue` - Crea un issue
- `list_issues` - Lista issues
- `get_issue` - Obtiene un issue específico
- `create_pull_request` - Crea un pull request
- `list_pull_requests` - Lista pull requests
- Y muchas más...

## 🔧 Uso con Claude Desktop

Para usar MCP con Claude Desktop:

1. Copia el archivo `mcp.json` a la configuración de Claude Desktop:
   - **Linux/Mac:** `~/.config/claude-desktop/mcp.json`
   - **Windows:** `%APPDATA%\Claude\Desktop\mcp.json`

2. Asegúrate de que el token en `mcp.json` sea válido

3. Reinicia Claude Desktop

4. Ahora puedes usar las herramientas de GitHub directamente desde Claude

## 🛡️ Seguridad

### Buenas Prácticas

1. **Nunca compartas tu token de GitHub**
2. **No subas archivos `.env` o `mcp.json` al repositorio**
3. **Usa tokens con permisos mínimos necesarios**
4. **Regenera tokens comprometidos inmediatamente**

### Permisos del Token

El token debe tener al menos estos permisos:
- `repo` - Acceso completo a repositorios (para repositorios privados)
- `public_repo` - Solo para repositorios públicos
- `user` - Información del usuario

## 📝 Ejemplos de Uso

### Ejemplo 1: Listar tus repositorios

```python
from mcp_github_client import MCPGitHubClient
import os

token = os.getenv("GITHUB_TOKEN")
client = MCPGitHubClient(token)
client.start_server()

# Listar repositorios
result = client.call_tool("list_repositories", {"username": ""})
print(result)

client.stop_server()
```

### Ejemplo 2: Crear un issue

```python
result = client.call_tool("create_issue", {
    "owner": "Fcnfabio",
    "repo": "Kahoot-Pastuso-MCP",
    "title": "Nuevo issue de prueba",
    "body": "Este es un issue creado vía MCP"
})
```

## 🔍 Solución de Problemas

### Error: "Method not found"

- Verifica que el servidor MCP esté instalado: `npm list -g @modelcontextprotocol/server-github`
- Asegúrate de que el token sea válido

### Error: "GITHUB_TOKEN no está configurada"

- Verifica que el archivo `.env` exista y tenga el token
- O exporta la variable: `export GITHUB_TOKEN="tu_token"`

### Error: "Push protection" de GitHub

- GitHub detectó un token en el código y bloqueó el push
- Elimina el token del código y usa variables de entorno
- O permite el token en: `https://github.com/{usuario}/{repo}/security/secret-scanning/unblock-secret/...`

## 📚 Recursos Adicionales

- [Documentación oficial de MCP](https://modelcontextprotocol.io/)
- [Servidor MCP de GitHub en npm](https://www.npmjs.com/package/@modelcontextprotocol/server-github)
- [API de GitHub](https://docs.github.com/es/rest)
- [Working with Secret Scanning](https://docs.github.com/code-security/secret-scanning/working-with-secret-scanning-and-push-protection)

## 🎮 Proyecto Relacionado

Este proyecto es parte de **Kahoot Pastuso**, un juego interactivo que usa RAG + LLM. Para más información, ver el [README.md](README.md) principal.
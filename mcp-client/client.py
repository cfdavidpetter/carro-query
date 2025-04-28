import os
import json
import aiohttp
from datetime import datetime
from typing import List, Dict, Any
from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from contextlib import AsyncExitStack

load_dotenv()

class MCPClient:
    def __init__(self):
        self.session = None
        self.exit_stack = AsyncExitStack()
        
        # Ensure we're using the correct Ollama URL
        self.ollama_url = os.getenv("OLLAMA_BASE_URL", "http://ollama:11434")
        print(f"Using Ollama URL: {self.ollama_url}")
        
        self.tool_selection_prompt = """Você é um assistente especializado em ajudar a escolher a ferramenta correta para consultas sobre carros.
        Sua tarefa é analisar a pergunta do usuário e determinar qual ferramenta do servidor deve ser usada.
        
        Ferramentas disponíveis:
        - get_all_cars: Buscar todos os carros.
        - filter_cars: Filtrar carros com critérios (ano, cor, preço etc.).
        - create_car: Criar um carro novo.
        - update_car: Atualizar dados de um carro existente.
        - delete_car: Deletar um carro.
        - count_cars_by_attribute: Contar carros agrupados por algum atributo (ex: year, color, kilometers, doors, accents, price, ame, engine_displacement, fuel_type, consumption, transmission).
        
        Pergunta do usuário: {query}
        
        Qual das ferramentas disponíveis é mais adequada para responder a pergunta do usuário?
        Responda APENAS com o nome da ferramenta mais apropriada, sem explicações adicionais!
        """
    
    async def connect_to_server(self):
        server_params = StdioServerParameters(
            command="uv",
            args=["run", "--with", "mcp", "mcp", "run", "mcp-server/server.py"],
            env={"PYTHONPATH": "."}
        )

        stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
        self.stdio, self.write = stdio_transport
        self.session = await self.exit_stack.enter_async_context(ClientSession(self.stdio, self.write))

        await self.session.initialize()

    async def ask_ollama(self, prompt: str) -> str:
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(
                    f"{self.ollama_url}/api/generate",
                    json={
                        "model": os.getenv("OLLAMA_MODEL", "deepseek-r1:1.5b"),
                        "prompt": prompt,
                        "stream": False
                    }
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        return result.get("response", "").strip()
                    else:
                        raise Exception(f"Ollama API returned status {response.status}")
            except Exception as e:
                print(f"Erro ao consultar o Ollama: {str(e)}")
                return ""

    async def process_query(self, query: str) -> str:
        if not self.session:
            return "Erro ao se conectar ao servidor!"

        try:
            response = await self.session.list_tools()
            available_tools = [tool.name for tool in response.tools]

            prompt = self.tool_selection_prompt.format(query=query)
            tool_name = await self.ask_ollama(prompt)

            if not tool_name:
                return "Desculpe, não consegui processar sua pergunta. Tente novamente."
                
            tool_name = tool_name.strip().lower()

            if tool_name not in available_tools:
                return f"Desculpe, não consegui encontrar uma ferramenta apropriada para sua pergunta."

            result = await self.session.call_tool(tool_name, {})
            # Convert CallToolResult to dictionary
            return {
                "tool_name": tool_name,
                "result": result.result
            }

        except Exception as e:
            return f"Erro ao processar a consulta: {str(e)}"

    async def cleanup(self):
        await self.exit_stack.aclose()

async def main():
    client = MCPClient()
    
    print("\n\nBem-vindo ao Chat de Consulta de Carros!")
    print("--------------------------------------------")
    print("Para sair do programa, digite 'sair/quit'")
    print("--------------------------------------------")
    
    try:
        os.makedirs("mcp-client/results", exist_ok=True)
        
        while True:
            user_input = input("\nSua pergunta: ").strip()

            if user_input.lower() == 'quit' or user_input.lower() == 'sair':
                print("Obrigado por usar o Chat.\nEspero que tenha sido útil!\nAté logo!")
                break
            
            try:
                await client.connect_to_server()
            except Exception as e:
                print(f"Erro ao conectar ao servidor: {str(e)}")
            
            print("\nResposta:")
            response = await client.process_query(user_input)
            print(response)

            # Save response to file
            timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M')
            with open(f"mcp-client/results/{timestamp}_{user_input}.json", "w") as f:
                f.write(response)
    finally:
        await client.cleanup()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

# CarroQuery

CarroQuery é um sistema de chat com IA sobre carros, permitindo que usuários obtenham informações detalhadas sobre veículos através de uma interface conversacional.

## 🛠️ Requisitos

- Docker
- Docker Compose
- Git

## 📋 Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/carro-query.git
cd carro-query
```

2. Inicie os containers Docker:
```bash
docker-compose up -d --build
```

3. Baixe o modelo de linguagem necessário para o Ollama:
```bash
docker exec ollama ollama pull gemma3:1b
```

4. Aguarde todos os containers estarem online e execute o script de boot:
```bash
docker exec carro-query-app ./setup.sh
```

5. Iniciar Chat:
```bash
docker-compose exec app python mcp-client/client.py
```

# Loja Virtual API - (Projeto Teste Backend)

## Descrição
Este projeto é uma aplicação backend desenvolvida para gerenciar uma loja virtual. A aplicação foi construída utilizando Python e FastAPI, juntamente com PostgreSQL para armazenamento de dados e RabbitMQ para processamento assíncrono de pedidos. O objetivo principal é fornecer uma API robusta e eficiente para gerenciar usuários, produtos e pedidos, garantindo uma experiência fluida e confiável.

## Funcionalidades Principais
- **Gerenciamento de Usuários**: 
  - Criar, listar e obter detalhes de usuários.
- **Gerenciamento de Produtos**: 
  - Criar, listar e obter detalhes de produtos.
- **Gerenciamento de Pedidos**: 
  - Criar e listar pedidos por usuário.
- **Processamento Assíncrono de Pedidos**: 
  - Uso de RabbitMQ para enfileirar pedidos.
  - Uso de Celery para processamento assíncrono de pedidos.
    
## Tecnologias Utilizadas
- Python
- FastAPI
- PostgreSQL
- RabbitMQ
- Celery
- Docker e Docker Compose

## Pré-requisitos
Certifique-se de ter os seguintes itens instalados em seu sistema:
- [Python](https://www.python.org/downloads/)
- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Instalação
1. Clone o repositório:
   ```bash
   git clone https://github.com/vribeirodev/backend-fastapi.git
   cd backend-fastapi

2. Configure o ambiente virtual:
   ```bash
   python -m venv env
   source env/bin/activate # Linux/macOS
   env\scripts\activate # Windows

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt

4. Configure o Docker e rode os containers:
   ```bash
   docker-compose up -d --remove-orphans --build

5. Execute os testes:
   ```bash
   docker-compose run --rm test

## Documentação da API
A documentação completa da API pode ser acessada através do Swagger/OpenAPI quando o servidor está em execução, disponível em [http://localhost:8000/docs](http://localhost:8000/docs).

![image](https://github.com/vribeirodev/backend-fastapi/assets/98496942/9346ea71-82fb-4385-a8fd-3d14e12b5de2)

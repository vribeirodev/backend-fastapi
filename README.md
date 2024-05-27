# Backend FastAPI

## Descrição
Este projeto é uma aplicação backend para gerenciar uma loja virtual, utilizando FastAPI, PostgreSQL e RabbitMQ para processamento assíncrono de pedidos.

## Tecnologias Utilizadas
- Python 3.9
- FastAPI
- PostgreSQL
- RabbitMQ
- Celery
- Docker e Docker Compose

## Pré-requisitos
Certifique-se de ter os seguintes itens instalados em seu sistema:
- [Python 3.8+](https://www.python.org/downloads/)
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

## Uso
Com o container web em execução acesse a documentação interativa da API no navegador:
http://localhost:8000/docs

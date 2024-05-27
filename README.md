# Loja Virtual API - (Projeto Teste Backend)

## Descrição
Este projeto é uma aplicação backend desenvolvida para gerenciar uma loja virtual. A aplicação foi construída utilizando Python e FastAPI, juntamente com PostgreSQL para armazenamento de dados e RabbitMQ para processamento assíncrono de pedidos.

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

## Estrutura do Projeto
```plaintext
.
├── alembic                     # Ferramenta de migração de banco de dados
│   ├── versions                # Arquivos de migração
├── app
│   ├── api                     # Definição das rotas da API
│   ├── core                    # Configurações principais e inicialização
│   ├── db                      # Configurações e modelos do banco de dados
│   ├── models                  # Definições dos modelos do banco de dados
│   ├── schemas                 # Esquemas de validação dos dados
│   ├── services                # Lógica de negócios e serviços
│   ├── worker                  # Configuração do Celery
│   ├── initial_data.py         # Script para inicialização de dados
│   └── main.py                 # Ponto de entrada da aplicação
├── tests                       # Testes automatizados
├── .gitignore                  # Arquivos a serem ignorados pelo Git
├── alembic.ini                 # Configurações do Alembic
├── docker-compose.yml          # Arquivo de configuração do Docker Compose
├── Dockerfile                  # Arquivo de configuração do Docker
├── README.md                   # Documentação do projeto
├── requirements.txt            # Dependências do projeto

```

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

## Contêineres
Ao executar `docker-compose up`, os seguintes contêineres serão iniciados:
- **web**: Servidor FastAPI rodando a aplicação web.
- **db**: Servidor PostgreSQL para armazenamento de dados.
- **rabbitmq**: Servidor RabbitMQ para enfileiramento de mensagens.
- **celery**: Worker Celery para processamento assíncrono de tarefas.
- **test**: Contêiner para execução de testes automatizados.

## Documentação da API
A documentação completa da API pode ser acessada através do Swagger/OpenAPI quando o servidor está em execução, disponível em [http://localhost:8000/docs](http://localhost:8000/docs) ou em [http://localhost:8000/redoc](http://localhost:8000/redoc).

![image](https://github.com/vribeirodev/backend-fastapi/assets/98496942/9346ea71-82fb-4385-a8fd-3d14e12b5de2)

## Exemplos de Uso

### Criar um novo usuário
```bash
curl -X 'POST' \
  'http://localhost:8000/api/v1/users/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "João da Silva",
  "email": "joao.silva@example.com",
  "password": "minhasenha123"
}'
```

### Obter detalhes de um usuário por ID
```bash
curl -X 'GET' \
  'http://localhost:8000/api/v1/users/1' \
  -H 'accept: application/json'
```

### Criar um novo produto
```bash
curl -X 'POST' \
  'http://localhost:8000/api/v1/products/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "Celular",
  "description": "Smartphone com 64GB de armazenamento.",
  "price": 1999.99,
  "quantity_in_stock": 50
}'
```

### Criar um novo pedido
```bash
curl -X 'POST' \
  'http://localhost:8000/api/v1/orders/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "user_id": 1,
  "items": [
    {
      "product_id": 1,
      "quantity": 2
    }
  ]
}'
```

# FastAPI Delivery API

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/sqlalchemy-%23D71F00.svg?style=for-the-badge&logo=sqlalchemy&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)

API REST de um sistema de delivery desenvolvida com Python e FastAPI, permitindo gerenciamento de produtos, categorias e pedidos, com autenticação JWT e controle de acesso baseado em permissões.

# Tecnologias utilizadas

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- Docker & Docker Compose
- Pytest

# Autenticação e Autorização

A API utiliza autenticação baseada em JWT (JSON Web Token).
- Login com geração de token
- Controle de acesso por perfil:
    - Usuário comum: pode criar pedidos e visualizar produtos
    - Administrador: pode gerenciar produtos e categorias
- Proteção de rotas para impedir que um usuário acesse ou modifique recursos de outro usuário
- Validação de permissões via dependências do FastAPI

# Funcionalidades

- Usuários
    - Registro e autenticação
    - Perfis com níveis de permissão (admin e comum)

- Categorias
    - Listar categorias
    - Criar, deletar e atualizar 
    - Upload e armazenamento local de imagens

- Produtos
    - Listar produtos por categoria
    - Visualizar produto específico
    - Criar, desativar, ativar e atualizar 
    - Upload e armazenamento local de imagens

- Pedidos
    - Criar pedidos
    - Listar pedidos do próprio usuário
    - Visualizar pedido específico
    - Alterar status do pedido (somente dono do pedido ou admin)
    - Restrições para impedir acesso a pedidos de outros usuários

- Testes
    - Testes de integração utilizando Pytest
    - Cobertura de testes na camada de serviços
    - Ambiente isolado para testes com banco dedicado

**OBS**: Para criar admins basta atualizar o campo is_admin de um usuario ja existente na base de dados para true

# Como rodar o projeto

1 - Clone o repositório
```bash
git clone https://github.com/gabrielferreira02/fastapi-delivery-api.git
cd fastapi-delivery-api
```

2 - Crie um arquivo .env na raiz com o seguinte conteúdo
```env
DB_URL=postgresql://postgres:postgres@db:5432/deliveryapi
UPLOAD_DIR=app/uploads/images
JWT_EXPIRATION_TIME=30
SECRET_KEY=sua chave secreta
ALGORITHM=HS256
```

3 - Inicie o projeto com docker e execute as migrações
```bash
docker compose up -d
docker compose exec api alembic upgrade head
```

Após iniciar o projeto acesse: http://localhost:8000/docs

4 - Para verificar os testes da camada serviço
```bash
docker compose exec api pytest --cov=app.services
```

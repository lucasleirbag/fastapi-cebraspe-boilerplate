# FastAPI Cebraspe Boilerplate

Template de produção FastAPI otimizado para projetos da Cebraspe, com SQL Server, autenticação JWT e arquitetura modular.

## 🚀 Features

- **FastAPI** com suporte completo a async/await
- **SQL Server** como banco de dados principal
- **Autenticação JWT** com OAuth2 Password Flow
- **SQLAlchemy 2.0** com suporte assíncrono (aioodbc)
- **Alembic** para migrações de banco
- **Pytest** com cobertura de testes completa
- **Arquitetura modular** com Repository Pattern
- **Docker** ready para desenvolvimento e produção
- **Pydantic** para validação de dados
- **Celery** para processamento de tarefas assíncronas

## 📋 Pré-requisitos

- Python 3.11+
- SQL Server 2019+ (ou SQL Server Developer Edition)
- ODBC Driver 17+ for SQL Server
- Git

## 🛠️ Configuração Inicial

### 1. Clone o repositório
```bash
git clone https://github.com/lucasleirbag/fastapi-cebraspe-boilerplate.git
cd fastapi-cebraspe-boilerplate
```

### 2. Configurar ambiente virtual
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
# ou
source .venv/bin/activate  # Linux/Mac
```

### 3. Instalar dependências
```bash
pip install -e .
```

### 4. Configurar variáveis de ambiente
Copie o arquivo `.env.example` para `.env` e configure:

```env
# Banco de dados SQL Server
DB_SERVER=localhost
DB_PORT=1433
DB_NAME_PRODUCTION=fastapi_production_db
DB_NAME_TEST=fastapi_test_db
DB_DRIVER=ODBC Driver 17 for SQL Server
DB_TRUSTED_CONNECTION=yes
DB_TRUST_SERVER_CERTIFICATE=yes
DB_ENCRYPT=yes

# Aplicação
ENVIRONMENT=development
SECRET_KEY=your-secret-key-here
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=1440

# Redis (opcional)
REDIS_URL=redis://localhost:6379/7
```

### 5. Executar migrações
```bash
alembic upgrade head
```

### 6. Executar testes
```bash
pytest -v
```

### 7. Iniciar aplicação
```bash
uvicorn core.server:app --reload --host 0.0.0.0 --port 8000
```

## 📚 Estrutura do Projeto

```
fastapi-cebraspe-boilerplate/
├── api/                    # Endpoints da API
│   └── v1/                # Versão 1 da API
│       ├── users/         # Endpoints de usuários
│       ├── tasks/         # Endpoints de tarefas
│       └── monitoring/    # Health checks
├── app/                   # Modelos e schemas
│   ├── models/           # Modelos SQLAlchemy
│   └── schemas/          # Schemas Pydantic
├── core/                 # Configurações e utilitários
│   ├── config.py         # Configurações da aplicação
│   ├── database/         # Configuração do banco
│   ├── security/         # JWT e autenticação
│   ├── repository/       # Repository pattern
│   └── controller/       # Controllers
├── tests/                # Testes automatizados
├── alembic/              # Migrações do banco
└── requirements/         # Dependências
```

## 🔐 Autenticação

O template usa JWT com OAuth2 Password Flow:

### Registrar usuário
```bash
POST /v1/users/register
{
  "email": "user@cebraspe.org.br",
  "username": "usuario",
  "password": "SenhaForte123!"
}
```

### Login
```bash
POST /v1/users/login
{
  "username": "usuario",
  "password": "SenhaForte123!"
}
```

### Usar token
```bash
GET /v1/users/
Authorization: Bearer <seu-jwt-token>
```

## 🧪 Testes

```bash
# Executar todos os testes
pytest -v

# Executar com cobertura
pytest --cov=app --cov=core --cov-report=html

# Executar testes específicos
pytest tests/api/v1/users/ -v
```

## 🐳 Docker

```bash
# Desenvolvimento
docker-compose up -d

# Produção
docker build -t fastapi-cebraspe .
docker run -p 8000:8000 fastapi-cebraspe
```

## 📖 Documentação da API

Após iniciar a aplicação, acesse:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔧 Desenvolvimento

### Adicionar nova funcionalidade
1. Criar modelo em `app/models/`
2. Criar schema em `app/schemas/`
3. Criar repository em `core/repository/`
4. Criar controller em `core/controller/`
5. Criar endpoints em `api/v1/`
6. Adicionar testes em `tests/`

### Criar migração
```bash
alembic revision --autogenerate -m "Descrição da migração"
alembic upgrade head
```

## 🚀 Deploy

### Variáveis de ambiente para produção
```env
ENVIRONMENT=production
DEBUG=0
SECRET_KEY=<chave-secreta-forte>
DB_SERVER=<servidor-producao>
DB_NAME_PRODUCTION=<banco-producao>
```

### Comandos de deploy
```bash
# Build
docker build -t fastapi-cebraspe:latest .

# Deploy
docker run -d \
  --name fastapi-cebraspe \
  -p 8000:8000 \
  --env-file .env.production \
  fastapi-cebraspe:latest
```

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto é propriedade da Cebraspe e destinado ao uso interno.

## 📞 Suporte

Para dúvidas ou suporte, entre em contato com a equipe de desenvolvimento da Cebraspe.

---

**Desenvolvido com ❤️ para a Cebraspe**

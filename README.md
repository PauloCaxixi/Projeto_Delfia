# 🔐 Encrypted Document Management API

> API REST desenvolvida em Python utilizando **FastAPI** para
> gerenciamento seguro de documentos PDF criptografados.

------------------------------------------------------------------------

# Índice

-   Visão Geral
-   Objetivo
-   Funcionalidades
-   Arquitetura
-   Estrutura do Projeto
-   Tecnologias
-   Instalação
-   Configuração
-   Executando a Aplicação
-   Fluxo de Funcionamento
-   Endpoints
-   Segurança
-   Criptografia
-   Banco de Dados
-   Logs
-   Testes
-   Estrutura das Camadas
-   Decisões Técnicas
-   Melhorias Futuras

------------------------------------------------------------------------

# Visão Geral

Este projeto implementa uma API REST para armazenamento seguro de
documentos PDF.

Todos os arquivos enviados são:

-   validados;
-   criptografados;
-   armazenados no sistema de arquivos;
-   registrados no banco de dados apenas com seus metadados.

O download realiza a descriptografia apenas em memória.

------------------------------------------------------------------------

# Objetivo

Este projeto foi desenvolvido para demonstrar conhecimentos em:

-   Python
-   FastAPI
-   SQLAlchemy
-   Criptografia
-   Arquitetura em Camadas
-   Repository Pattern
-   Service Layer
-   Segurança
-   Testes Automatizados
-   Clean Code

------------------------------------------------------------------------

# Funcionalidades

-   Upload de PDF
-   Listagem de documentos
-   Download seguro
-   Criptografia Fernet
-   HTTP Basic Authentication
-   SQLite
-   Logs
-   Testes automatizados

------------------------------------------------------------------------

# Arquitetura

``` text
                Cliente

                   │
                   ▼

              FastAPI Router

                   │
                   ▼

          Authentication Layer

                   │
                   ▼

            Document Service

        ┌──────────┴──────────┐

        ▼                     ▼

 EncryptionService     Repository

        │                     │

        ▼                     ▼

   Arquivos .enc         SQLite
```

------------------------------------------------------------------------

# Estrutura do Projeto

``` text
app/
│
├── api/
│   └── documents.py
│
├── core/
│   ├── authentication.py
│   ├── config.py
│   ├── encryption.py
│   └── logging_config.py
│
├── database/
│   ├── database.py
│   ├── init_db.py
│   └── session.py
│
├── models/
│   └── document.py
│
├── repositories/
│   └── document_repository.py
│
├── schemas/
│   └── document.py
│
├── services/
│   └── document_service.py
│
└── main.py

tests/
scripts/
storage/
logs/
```

------------------------------------------------------------------------

# Tecnologias

| Tecnologia | Utilização |
|------------|------------|
| Python | Linguagem de programação |
| FastAPI | Framework para API REST |
| SQLAlchemy | ORM |
| SQLite | Banco de dados |
| Cryptography | Criptografia de arquivos |
| Pydantic | Validação de dados e configurações |
| Uvicorn | Servidor ASGI |
| Pytest | Testes automatizados |

------------------------------------------------------------------------

# Instalação

``` bash
git clone <URL_DO_REPOSITORIO>

cd Projeto_Delfia
```

Crie o ambiente virtual.

Windows

``` powershell
python -m venv .venv

.venv\Scripts\activate
```

Linux

``` bash
python3 -m venv .venv

source .venv/bin/activate
```

Instale as dependências.

``` bash
pip install -r requirements.txt
```

------------------------------------------------------------------------

# Configuração

Gere uma chave.

``` bash
python scripts/generate_key.py
```

Crie um arquivo `.env`.

``` env
ENCRYPTION_KEY=SUA_CHAVE

API_USERNAME=admin

API_PASSWORD=senha
```

------------------------------------------------------------------------

# Executando

``` bash
uvicorn app.main:app --reload
```

Swagger

``` text
http://127.0.0.1:8000/docs
```

------------------------------------------------------------------------

# Fluxo de Upload

``` text
Cliente

   │

   ▼

Recebe PDF

   │

   ▼

Validação

   │

   ▼

SHA256

   │

   ▼

Criptografia

   │

   ▼

storage/*.enc

   │

   ▼

SQLite
```

------------------------------------------------------------------------

# Fluxo de Download

``` text
Autenticação

    │

    ▼

Consulta Banco

    │

    ▼

Lê Arquivo .enc

    │

    ▼

Descriptografa

    │

    ▼

Retorna PDF
```

------------------------------------------------------------------------

# Endpoints

## Health

``` http
GET /health
```

## Upload

``` http
POST /documents
```

## Listagem

``` http
GET /documents
```

## Download

``` http
GET /documents/{document_id}/download
```

------------------------------------------------------------------------

# Segurança

Foram implementadas as seguintes medidas:

-   HTTP Basic Authentication
-   compare_digest()
-   SQLAlchemy
-   UUID para nomes internos
-   Validação da extensão
-   Validação do Content-Type
-   Validação da assinatura `%PDF-`
-   Limite de tamanho
-   Criptografia Fernet
-   Variáveis de ambiente
-   Logs sem informações sensíveis

------------------------------------------------------------------------

# Criptografia

Foi utilizada a biblioteca **cryptography** com algoritmo **Fernet**.

O Fernet fornece:

-   Confidencialidade
-   Integridade
-   Autenticação do conteúdo

Os documentos nunca permanecem descriptografados no armazenamento.

------------------------------------------------------------------------

# Banco de Dados

Foi utilizado SQLite para facilitar a execução do projeto.

O banco armazena somente:

-   ID
-   Nome original
-   Nome interno
-   Tipo
-   Checksum
-   Tamanho
-   Data de criação

------------------------------------------------------------------------

# Logs

São registrados:

-   Upload
-   Download
-   Tentativas inválidas
-   Listagem
-   Erros controlados

Arquivo:

``` text
logs/application.log
```

------------------------------------------------------------------------

# Testes

Executar

``` bash
python -m pytest
```

Cobertura

``` bash
python -m pytest --cov=app --cov-report=term-missing
```

Resultado atual

-   17 testes aprovados
-   92% de cobertura

------------------------------------------------------------------------

# Exemplos de Uso

## Upload de Documento

### Requisição

```http
POST /documents
Authorization: Basic <base64>

Content-Type: multipart/form-data
```

Arquivo enviado:

```text
contrato.pdf
```

### Resposta

```json
{
  "id": "d3fb5c9d-f6ef-4b3d-bd7e-89db68ef66b3",
  "original_name": "contrato.pdf",
  "content_type": "application/pdf",
  "size": 48215,
  "checksum": "bc4bcad857b5cf6e99...",
  "created_at": "2026-07-16T16:48:21"
}
```

------------------------------------------------------------------------

## Listagem

### Requisição

```http
GET /documents
```

### Resposta

```json
[
    {
        "id": "d3fb5c9d-f6ef-4b3d-bd7e-89db68ef66b3",
        "original_name": "contrato.pdf",
        "content_type": "application/pdf",
        "size": 48215,
        "checksum": "bc4bcad857b5cf6e99...",
        "created_at": "2026-07-16T16:48:21"
    }
]
```

------------------------------------------------------------------------

## Download

### Requisição

```http
GET /documents/{document_id}/download
```

Resposta:

```text
application/pdf
```

------------------------------------------------------------------------

# Códigos HTTP

| Código | Descrição |
|---------|-----------|
| 200 | Requisição realizada com sucesso |
| 201 | Documento criado |
| 400 | Arquivo inválido |
| 401 | Credenciais inválidas |
| 404 | Documento não encontrado |
| 500 | Erro interno |

------------------------------------------------------------------------

# Decisões Técnicas

Durante o desenvolvimento foram adotadas algumas decisões para manter o projeto organizado, seguro e de fácil manutenção.

### FastAPI

Escolhido pela alta produtividade, tipagem nativa e documentação automática.

### SQLAlchemy

Evita consultas SQL construídas manualmente, reduzindo riscos de SQL Injection.

### Fernet

Oferece criptografia autenticada, garantindo confidencialidade e integridade.

### Repository Pattern

Centraliza o acesso ao banco de dados e desacopla a regra de negócio da persistência.

### Service Layer

Toda a regra de negócio foi centralizada na camada de serviços.

Isso torna os endpoints mais simples e facilita testes e manutenção.

------------------------------------------------------------------------

# Estrutura das Camadas

```text
API
│
├── Recebe requisições HTTP
├── Valida parâmetros
└── Chama Services

Services
│
├── Regras de negócio
├── Valida arquivos
├── Criptografa documentos
└── Utiliza Repository

Repositories
│
└── Comunicação com SQLite

Models
│
└── Estrutura das tabelas

Core
│
├── Configurações
├── Autenticação
├── Criptografia
└── Logs
```

------------------------------------------------------------------------

# Escalabilidade

Embora o projeto tenha sido desenvolvido para um desafio técnico, sua arquitetura permite evolução sem grandes mudanças estruturais.

Possíveis melhorias:

- PostgreSQL
- Amazon S3
- Docker
- Kubernetes
- Redis
- RabbitMQ
- Celery
- OAuth2
- JWT
- Rate Limiting
- Auditoria
- Versionamento de API
- CI/CD
- AWS Secrets Manager
- Hashicorp Vault

------------------------------------------------------------------------

# 🚀 Melhorias Futuras

## Funcionalidades

- Exclusão de documentos
- Versionamento de documentos
- Histórico de alterações
- Múltiplos usuários
- Controle de permissões (RBAC)
- Dashboard administrativo
- Upload assíncrono
- Compressão de arquivos

## Infraestrutura e Escalabilidade

- Migração do banco de dados para PostgreSQL
- Containerização com Docker
- Pipeline de CI/CD (GitHub Actions)
- Cache com Redis
- Armazenamento de documentos no Amazon S3
- Rate Limiting para proteção da API

## Segurança

- Autenticação JWT e OAuth2
- Rotação automática das chaves de criptografia
- Integração com Secret Manager para gerenciamento seguro de credenciais
- Integração com antivírus para validação dos arquivos enviados
- Auditoria completa das operações realizadas

------------------------------------------------------------------------

# Licença

Este projeto foi desenvolvido exclusivamente para fins de avaliação técnica em um processo seletivo.

------------------------------------------------------------------------

# Decisões Técnicas

-   FastAPI pela produtividade e documentação automática.
-   SQLAlchemy para evitar SQL Injection.
-   Fernet por oferecer criptografia autenticada.
-   SQLite para simplificar a execução local.
-   Repository Pattern para desacoplar acesso ao banco.
-   Service Layer para centralizar regras de negócio.
-   Variáveis de ambiente para remover segredos do código.

------------------------------------------------------------------------

# Autor

Projeto desenvolvido como solução para um desafio técnico utilizando
boas práticas de arquitetura, segurança, organização de código e testes
automatizados.
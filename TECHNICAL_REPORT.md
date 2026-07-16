# Relatório Técnico

## Sistema de Gestão de Documentos Criptografados

**Autor:** Paulo Caxixi Pereira Fernandes

**Tecnologias Principais:**

- Python 3.14
- FastAPI
- SQLAlchemy
- SQLite
- Cryptography (Fernet)
- Pytest

---

# 1. Introdução

Este documento apresenta as decisões técnicas adotadas durante o desenvolvimento do Sistema de Gestão de Documentos Criptografados.

O objetivo do projeto foi desenvolver uma API REST capaz de realizar upload, armazenamento, listagem e recuperação de documentos PDF de forma segura, garantindo que os arquivos permanecessem criptografados no sistema de arquivos e que somente usuários autenticados pudessem acessá-los.

Além da implementação funcional, foram considerados aspectos relacionados à arquitetura, organização do código, segurança, testes automatizados e facilidade de manutenção.

---

# 2. Objetivo

O principal objetivo foi construir uma aplicação organizada, segura e de fácil manutenção que atendesse integralmente aos requisitos propostos no desafio técnico.

Durante o desenvolvimento buscou-se aplicar boas práticas de engenharia de software, como:

- Clean Code;
- Separação de responsabilidades;
- Arquitetura em camadas;
- Testes automatizados;
- Configuração por variáveis de ambiente;
- Segurança no tratamento de arquivos;
- Código de fácil manutenção.

---

# 3. Requisitos Atendidos

Durante o desenvolvimento foram implementados todos os requisitos solicitados.

| Requisito | Status |
|-----------|--------|
| API REST | ✅ |
| Upload de PDF | ✅ |
| Listagem | ✅ |
| Download | ✅ |
| Criptografia | ✅ |
| Autenticação HTTP Basic | ✅ |
| Logs | ✅ |
| Variáveis de ambiente | ✅ |
| Testes automatizados | ✅ |
| README | ✅ |
| Relatório Técnico | ✅ |

---

# 4. Arquitetura Escolhida

Foi adotada uma arquitetura em camadas para separar responsabilidades e facilitar futuras evoluções do sistema.

A aplicação foi organizada da seguinte forma:

```text
Cliente

    │

    ▼

FastAPI

    │

    ▼

Authentication

    │

    ▼

Document Service

    │

    ├──────────────┐

    ▼              ▼

Encryption     Repository

                    │

                    ▼

                SQLite

```

Cada camada possui uma única responsabilidade.

Essa organização reduz o acoplamento entre componentes e facilita testes e manutenção.

---

# 5. Estrutura do Projeto

```text
app/

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

Essa estrutura foi escolhida para manter o projeto organizado conforme aplicações Python modernas.

---

# 6. Fluxo da Aplicação

## Upload

```text
Cliente

    │

    ▼

Recebe Arquivo

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

Storage

    │

    ▼

SQLite
```

## Download

```text
Cliente

    │

    ▼

Autenticação

    │

    ▼

Busca Metadados

    │

    ▼

Lê Arquivo Criptografado

    │

    ▼

Descriptografa

    │

    ▼

Retorna PDF
```

---

# 7. Escolhas Técnicas

## FastAPI

Foi escolhido FastAPI pelos seguintes motivos:

- Excelente desempenho.
- Tipagem nativa.
- Documentação automática (Swagger/OpenAPI).
- Facilidade na criação de APIs REST.
- Integração simples com testes automatizados.

Além disso, a documentação automática facilita tanto o desenvolvimento quanto a validação da API.

---

## SQLAlchemy

Foi utilizado SQLAlchemy como ORM.

Principais benefícios:

- Evita construção manual de consultas SQL.
- Reduz riscos de SQL Injection.
- Facilita manutenção.
- Permite migração futura para outros bancos de dados.

---

## SQLite

SQLite foi escolhido devido ao escopo do desafio.

Vantagens:

- Não necessita instalação.
- Fácil configuração.
- Arquivo único.
- Ideal para testes técnicos.

Caso a aplicação fosse utilizada em produção, PostgreSQL seria uma escolha mais adequada.

---

## Cryptography (Fernet)

Foi utilizada a biblioteca Cryptography com Fernet.

Essa biblioteca oferece:

- Criptografia autenticada.
- Integridade dos dados.
- Facilidade de implementação.
- API consolidada e amplamente utilizada.

O Fernet garante que qualquer alteração no arquivo criptografado seja detectada automaticamente.

---

## Repository Pattern

O acesso ao banco de dados foi isolado em uma camada Repository.

Essa abordagem permite:

- Centralizar consultas.
- Facilitar manutenção.
- Reduzir duplicação.
- Melhorar testes.

---

## Service Layer

Toda regra de negócio foi centralizada na camada Services.

Isso evita que regras fiquem distribuídas entre controllers e banco de dados.

A camada Service ficou responsável por:

- validar arquivos;
- calcular checksum;
- criptografar documentos;
- descriptografar documentos;
- persistir informações.

---

# 8. Configuração

As configurações da aplicação são carregadas através do arquivo `.env`.

São utilizadas variáveis para:

- chave de criptografia;
- usuário da API;
- senha da API.

Essa abordagem evita que informações sensíveis fiquem armazenadas diretamente no código-fonte.

Além disso, o arquivo `.env` foi incluído no `.gitignore`, impedindo seu versionamento.

---

# 9. Organização do Código

Durante o desenvolvimento foram seguidos princípios de Clean Code.

As principais práticas adotadas foram:

- funções pequenas;
- nomes descritivos;
- responsabilidade única;
- separação entre camadas;
- reutilização de código;
- tratamento explícito de erros;
- tipagem com type hints.

Essas práticas tornam o projeto mais legível e mais simples de evoluir.

---

# 10. Segurança

Durante o desenvolvimento, a segurança foi considerada um dos principais requisitos do projeto.

Embora o escopo da aplicação seja reduzido, foram implementadas diversas medidas para minimizar riscos comuns em aplicações web.

## Autenticação

Foi utilizada autenticação HTTP Basic.

As credenciais são carregadas por meio de variáveis de ambiente e comparadas utilizando `secrets.compare_digest()`.

Essa abordagem evita comparações diretas de strings, reduzindo riscos de ataques baseados em tempo de resposta (Timing Attack).

Em ambientes de produção, essa autenticação deve ser utilizada somente sobre HTTPS.

---

## Proteção contra SQL Injection

Toda comunicação com o banco de dados é realizada através do SQLAlchemy.

Nenhuma consulta SQL é construída manualmente utilizando concatenação de strings.

Dessa forma, a aplicação utiliza consultas parametrizadas automaticamente pelo ORM.

---

## Proteção contra Path Traversal

O nome enviado pelo usuário nunca é utilizado como nome físico do arquivo.

Sempre é gerado um UUID para representar o documento armazenado.

Exemplo:

```text
storage/

2f04ab4d-f26f-49a2-b65c-a73df90dcab9.enc
```

Isso impede que usuários tentem acessar caminhos como:

```text
../../windows/system32
```

---

## Upload Seguro

Antes do armazenamento são realizadas diversas validações.

- Extensão `.pdf`
- Content-Type
- Assinatura `%PDF-`
- Arquivo vazio
- Limite máximo de tamanho

Essas verificações reduzem significativamente o risco de armazenamento de arquivos inválidos.

---

## Gerenciamento de Segredos

Nenhuma informação sensível permanece no código.

As seguintes configurações são carregadas através do arquivo `.env`:

- ENCRYPTION_KEY
- API_USERNAME
- API_PASSWORD

O arquivo `.env` também foi incluído no `.gitignore`.

---

# 11. Criptografia

Foi utilizada a biblioteca **Cryptography**, através da implementação Fernet.

A escolha foi realizada pelos seguintes motivos:

- Implementação consolidada.
- API simples.
- Criptografia autenticada.
- Verificação automática de integridade.

Sempre que um documento é recebido ocorre o seguinte fluxo:

```text
Documento Original

        │

        ▼

SHA-256

        │

        ▼

Criptografia Fernet

        │

        ▼

Arquivo .enc
```

Durante o download:

```text
Arquivo .enc

        │

        ▼

Descriptografia

        │

        ▼

PDF Original
```

Os documentos permanecem criptografados durante todo o período em que ficam armazenados.

---

# 12. Banco de Dados

Foi utilizado SQLite devido ao escopo do desafio.

O banco armazena apenas metadados.

Campos armazenados:

- ID
- Nome original
- Nome interno
- Tipo
- Checksum
- Tamanho
- Data de criação

O conteúdo do documento nunca é salvo no banco de dados.

Os arquivos permanecem exclusivamente no diretório `storage`.

---

# 13. Tratamento de Erros

Foram criadas exceções específicas para representar diferentes situações.

Exemplos:

- EncryptionError
- InvalidDocumentError
- DocumentNotFoundError

Essas exceções permitem separar erros esperados de falhas inesperadas.

A API converte essas exceções em respostas HTTP apropriadas.

Exemplo:

| Exceção | HTTP |
|----------|------|
| InvalidDocumentError | 400 |
| DocumentNotFoundError | 404 |
| Credenciais inválidas | 401 |

---

# 14. Logs

As operações consideradas sensíveis geram registros.

Eventos registrados:

- Upload
- Download
- Listagem
- Upload inválido
- Documento inexistente

Os logs são gravados em:

```text
logs/application.log
```

Nenhuma informação sensível é registrada.

Exemplos de informações omitidas:

- senha
- chave Fernet
- conteúdo do documento

---

# 15. Testes Automatizados

Foram implementados testes unitários e testes de integração.

## Criptografia

Os testes validam:

- criptografia do conteúdo;
- descriptografia correta;
- rejeição de chave inválida;
- rejeição de conteúdo alterado;
- conteúdo vazio;
- chave vazia.

---

## Configuração

Foram criados testes para validar:

- leitura do `.env`;
- configurações obrigatórias.

---

## Autenticação

Os testes verificam:

- acesso sem credenciais;
- usuário inválido;
- senha inválida;
- autenticação válida.

---

## Documentos

Foram implementados testes para:

- upload;
- listagem;
- download;
- arquivo inválido;
- documento inexistente.

---

# 16. Cobertura dos Testes

Resultado obtido:

```text
17 testes executados

17 testes aprovados

92% de cobertura
```

Os testes foram desenvolvidos utilizando:

- Pytest
- FastAPI TestClient
- SQLite em memória

Essa abordagem permite que os testes sejam rápidos, isolados e independentes do ambiente local.

---

# 17. Escalabilidade

Embora o projeto tenha sido desenvolvido para um desafio técnico, sua arquitetura permite evolução sem mudanças significativas.

Possíveis evoluções:

## Banco

Substituir SQLite por PostgreSQL.

---

## Armazenamento

Migrar arquivos para:

- Amazon S3
- Azure Blob Storage
- Google Cloud Storage

---

## Processamento

Executar criptografia de arquivos grandes utilizando filas assíncronas.

Exemplos:

- Celery
- RabbitMQ
- Redis Queue

---

## Balanceamento

Executar múltiplas instâncias da API utilizando Load Balancer.

---

## Cache

Adicionar Redis para reduzir consultas repetidas.

---

## Auditoria

Persistir logs em soluções centralizadas.

Exemplos:

- Elasticsearch
- Grafana Loki
- Splunk

---

# 18. Melhorias Futuras

Caso o projeto fosse evoluído, poderiam ser adicionadas funcionalidades como:

- múltiplos usuários;
- perfis de acesso;
- JWT;
- OAuth2;
- versionamento de documentos;
- exclusão lógica;
- histórico de versões;
- upload assíncrono;
- antivírus;
- Docker;
- Kubernetes;
- CI/CD;
- monitoramento;
- métricas;
- rotação automática de chaves;
- integração com Secret Manager.

---

# 19. Dificuldades Encontradas

Durante o desenvolvimento alguns desafios precisaram ser resolvidos.

Entre eles:

- organização da arquitetura;
- definição da separação entre Services e Repository;
- configuração dos testes automatizados;
- gerenciamento da chave de criptografia;
- tratamento adequado de exceções;
- armazenamento seguro dos arquivos.

Todos esses pontos foram solucionados mantendo o foco em simplicidade e facilidade de manutenção.

---

# 20. Lições Aprendidas

O desenvolvimento permitiu reforçar diversos conceitos importantes.

Entre eles:

- arquitetura em camadas;
- organização de APIs REST;
- testes automatizados;
- criptografia de arquivos;
- boas práticas de segurança;
- separação de responsabilidades;
- configuração por variáveis de ambiente;
- tratamento de erros.

---

# 21. Conclusão

O projeto atende aos requisitos propostos no desafio técnico.

Durante o desenvolvimento foram priorizados aspectos relacionados à organização, segurança, qualidade de código e facilidade de manutenção.

A solução implementada fornece uma base sólida para gerenciamento seguro de documentos criptografados e pode evoluir futuramente para ambientes de produção com poucas alterações estruturais.

Além de atender aos requisitos funcionais, o projeto demonstra a aplicação de boas práticas de desenvolvimento, arquitetura em camadas, testes automatizados e princípios de Clean Code, proporcionando uma solução organizada, extensível e preparada para futuras evoluções.
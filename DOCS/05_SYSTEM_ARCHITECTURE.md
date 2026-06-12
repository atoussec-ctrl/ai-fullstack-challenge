# Arquitetura do Sistema

## Diagrama lógico

```txt
User
 ↓
React/Vite Frontend
 ↓ REST/SSE
Flask API
 ↓
Application Services
 ↓
Domain
 ↓
Infrastructure
 ├── SQLite
 ├── OpenAI
 ├── LangChain
 ├── LangSmith
 └── FAISS/Milvus
```

## Fronteiras

### Frontend

Responsável por:

- interface de chat;
- tema claro/escuro;
- upload de arquivos;
- gravação de áudio;
- preview de imagens/documentos;
- estado de tela;
- cache de dados;
- consumo da API Flask;
- testes de UI.

Não deve:

- guardar chave OpenAI;
- executar lógica sensível de IA;
- persistir dados críticos sem backend;
- acoplar componentes à implementação HTTP.

### Backend Flask

Responsável por:

- autenticação futura;
- endpoints REST;
- validação server-side;
- persistência SQLite;
- integração com LangChain/OpenAI;
- busca semântica;
- upload seguro;
- streaming de respostas;
- logging e tracing.

### Pacotes de domínio

Responsáveis por:

- entidades;
- regras de negócio;
- casos de uso;
- portas/interfaces;
- erros de domínio.

## Clean Architecture aplicada

```txt
Presentation
  React Components / Flask Blueprints
Application
  Use Cases / Services
Domain
  Entities / Value Objects / Ports
Infrastructure
  SQLite / OpenAI / FAISS / File Storage
```

## SOLID

### Single Responsibility

Cada componente e serviço deve ter uma única razão para mudar.

Exemplo:

- `ChatComposer` renderiza composição.
- `useSendMessage` envia mensagem.
- `chatApi` conhece HTTP.
- `Message` representa entidade.

### Open/Closed

Novos tipos de attachment devem ser adicionados sem reescrever o composer.

### Liskov Substitution

Implementações de repositório devem respeitar interfaces.

### Interface Segregation

Separar portas:

- `ChatCompletionGateway`;
- `TranscriptionGateway`;
- `AttachmentStorage`;
- `VectorSearchGateway`.

### Dependency Inversion

Casos de uso dependem de abstrações, não de Flask, OpenAI ou FAISS diretamente.

## DRY e KISS

- Contratos compartilhados por OpenAPI.
- Tipos TypeScript gerados a partir do schema.
- Componentes pequenos.
- Sem abstração prematura.
- Um fluxo claro para mensagem, upload e streaming.

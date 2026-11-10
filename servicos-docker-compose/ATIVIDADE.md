# Atividade: aplicação do projeto integrador com FastAPI, HTML e MySQL

## 1. Objetivo

Em equipes de **até três integrantes**, adaptar a aplicação de [MeuProjeto](MeuProjeto/) a uma temática do **projeto integrador** ou a uma **atividade desenvolvida na disciplina de Engenharia de Software**. A aplicação deverá permitir cadastrar, listar, visualizar, atualizar e excluir dados pelo navegador, com armazenamento no MySQL.

**Valor total: 5,0 pontos.**

O trabalho consiste em atualizar `MeuProjeto/backend/main.py` e acrescentar as páginas necessárias em `MeuProjeto/frontend/`. A pasta [MeuProjeto-Com-BD](MeuProjeto-Com-BD/) fornece as alterações iniciais de conexão com o banco e um exemplo de CRUD de **usuários**, com os campos `nome` e `senha` do exemplo original. A equipe poderá copiar essas alterações para sua versão de `MeuProjeto` ou trabalhar a partir de uma cópia de `MeuProjeto-Com-BD`.

Mantenha a organização e o nível de complexidade do exemplo: um arquivo Python com conexão, classes e rotas; páginas HTML simples com JavaScript e `fetch`. Não é necessário separar o backend em módulos, criar schemas Pydantic próprios, utilizar templates Jinja2, frameworks de frontend ou bibliotecas adicionais de formulários.

## 2. Conhecer o exemplo antes de alterar

### 2.1. Exemplo original: `MeuProjeto`

- `backend/main.py`: CRUD de usuários armazenados em uma lista Python.
- `frontend/index.html`: menu principal.
- `frontend/usuarios.html`: cadastro de usuários com `POST` e JSON.
- `frontend/listarusuarios.html`: consulta dos usuários com `GET`.
- `frontend/atualizarusuario.html`: atualização com `PUT`.
- `frontend/deletarusuario.html`: exclusão com `DELETE`.
- `Dockerfile`: preparação do backend Python.
- `docker-compose.yml`: serviços `backend` e `frontend` (Nginx).

Os dados da lista desaparecem quando o backend é reiniciado. O objetivo desta atividade é aplicar o mesmo fluxo de requisições a registros armazenados em banco de dados.

### 2.2. Exemplo inicial com banco: `MeuProjeto-Com-BD`

```text
MeuProjeto-Com-BD/
├── Dockerfile
├── docker-compose.yml
├── backend/
│   ├── main.py
│   └── requirements.txt
└── frontend/
    ├── index.html
    ├── usuarios.html
    ├── listarusuarios.html
    ├── atualizarusuario.html
    └── deletarusuario.html
```

Esta pasta mantém **os mesmos cinco arquivos HTML e a mesma estrutura do original**, com pequenos ajustes para usar o ID gerado pelo MySQL nos seletores e na listagem e corrigir o evento `click` do botão de atualizar a lista.

O `backend/main.py` acrescenta:

1. Conexão com o MySQL usando SQLAlchemy e variáveis de ambiente.
2. Classe `Usuario`, representando a tabela `usuarios`, com `id`, `nome` e `senha`.
3. Criação da tabela com `Base.metadata.create_all(engine)`.
4. Rota `POST /usuarios`, que recebe JSON e insere um usuário.
5. Rotas de listagem, consulta individual, atualização e exclusão de usuários no MySQL.

O exemplo com banco substitui a lista em memória pelo MySQL em todas as operações de usuários. As telas existentes já permitem cadastrar, listar, atualizar e excluir usuários. A equipe deverá adaptar esse fluxo e criar as páginas das entidades do tema escolhido.

As dependências são FastAPI e Uvicorn, já presentes no original, mais SQLAlchemy e `PyMySQL[rsa]`. O SQLAlchemy representa as tabelas e executa as operações; o PyMySQL é o driver necessário para estabelecer a conexão com o MySQL. O extra `rsa` permite a autenticação utilizada pelo MySQL 8. Não é necessário instalar `python-dotenv`: o Compose fornece as variáveis ao backend.

## 3. Definir a temática e os dados

Escolha um tema vinculado ao trabalho já realizado no projeto integrador ou em Engenharia de Software. Explique essa relação e defina **pelo menos quatro entidades** relevantes para a aplicação.

| Temática | Exemplos de entidades |
|---|---|
| Gestão de demandas de software | Demandas, projetos, equipes e entregas |
| Controle de laboratório | Equipamentos, materiais, setores e chamados |
| Organização de eventos | Eventos, participantes, espaços e atividades |
| Controle de estoque | Produtos, categorias, fornecedores e movimentações |

Quatro registros de uma mesma tabela não correspondem a quatro entidades. O cadastro de usuários original só poderá contar como uma entidade se fizer sentido no tema e for utilizado com persistência no MySQL.

Para cada entidade, defina os campos e seus tipos. Utilize um `id` inteiro como chave primária, gerado pelo banco. Comece com campos simples, como nome, descrição, quantidade ou situação. Relacionamentos com chaves estrangeiras são opcionais nesta atividade; o foco é compreender o caminho entre a tela, a API e o banco.

## 4. Executar e compreender o cadastro de usuários

Na raiz deste repositório:

```bash
cd MeuProjeto-Com-BD
docker compose up -d --build
docker compose ps
```

Utilize:

- Menu HTML: <http://127.0.0.1:8001>.
- Backend: <http://127.0.0.1:8000>.
- Documentação para experimentar a API: <http://127.0.0.1:8000/docs>.

Encerre a versão original antes de iniciar a versão com banco, caso ela esteja usando as mesmas portas. Se acessar por outra máquina, substitua `127.0.0.1` nos endereços dos `fetch` pelo IP ou nome da máquina que executa o backend.

No Compose fornecido, o MySQL cria o banco `meuprojeto` e o usuário didático `aluno`. O backend conecta ao endereço `db`, que é o nome do serviço MySQL na rede interna. O serviço aguarda a verificação de disponibilidade do banco antes de iniciar. O SQLAlchemy cria as tabelas que ainda não existem; `create_all` não altera colunas de tabelas já criadas.

O frontend é servido pelo Nginx e o JavaScript do navegador acessa diretamente a porta `8000` do backend, como no original. Por isso, o backend mantém a configuração de CORS. Nesta atividade, o Nginx serve os arquivos estáticos; não é necessário configurá-lo como proxy.

### 4.1. Fazer a primeira inserção

Utilize `/docs` ou o terminal para enviar:

```bash
curl -X POST http://127.0.0.1:8000/usuarios \
  -H 'Content-Type: application/json' \
  -d '{"nome":"Ana", "senha":"senha_didatica"}'
```

A resposta contém uma mensagem e o `id` gerado pelo MySQL. Para listar:

```bash
curl http://127.0.0.1:8000/usuarios
```

No `main.py`, acompanhe as etapas:

```python
with Sessao() as banco:
    usuario = Usuario(nome=nome, senha=senha)
    banco.add(usuario)
    banco.commit()
    banco.refresh(usuario)
```

- `Usuario(...)` cria o objeto Python com os dados recebidos.
- `banco.add(...)` inclui o objeto na sessão.
- `banco.commit()` confirma a inserção no MySQL.
- `banco.refresh(...)` carrega os valores gerados pelo banco, como o `id`.
- O bloco `with` fecha a sessão ao terminar; cada requisição abre sua própria sessão.

As rotas de cadastro e atualização mantêm `request: Request`, como no exemplo original. A função usa `async def` para ler o JSON com `await request.json()`, sem criar uma classe de entrada separada:

```python
@app.post("/usuarios", status_code=201)
async def cad_usuario(request: Request):
    dados = await request.json()
    nome, senha = validar_usuario(dados)
    # Criar o objeto Usuario e gravar com a sessão, conforme main.py.
```

Na atualização, a assinatura é `async def alterar_usuario(usuario_id: int, request: Request)`, com a mesma leitura do JSON. As classes SQLAlchemy representam as tabelas.

### 4.2. Compreender a tela de cadastro

O arquivo `frontend/usuarios.html` envia os campos `nome` e `senha` para `/usuarios`. O mesmo JSON utilizado no exemplo original agora é gravado no MySQL:

```javascript
const usuario = {
    nome: formulario.elements.nome.value,
    senha: formulario.elements.senha.value
};

const resposta = await fetch("http://127.0.0.1:8000/usuarios", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(usuario)
});

const dados = await resposta.json();
mensagem.textContent = resposta.ok ? dados.mensagem : dados.detail;
```

Ao adaptar as páginas, trate também falhas de conexão com `try/catch`. A API valida nome e senha obrigatórios, com até 100 caracteres, e retorna o ID no cadastro. As consultas retornam `id` e `nome`; a senha não é incluída nas respostas. A tela de edição recebe uma nova senha, como no original.

Depois de compreender o exemplo, adapte os nomes da classe, tabela, campos, rotas e telas à primeira entidade do tema. Não é obrigatório manter usuários na entrega final. Duplique as páginas existentes para criar as telas das demais entidades e acrescente links no menu.

## 5. Implementar o sistema da equipe

### 5.1. Backend e MySQL

Concentre a conexão, as classes e as rotas em `backend/main.py`. Para cada entidade, implemente o CRUD completo seguindo esta organização:

| Método | Exemplo de rota | Operação |
|---|---|---|
| POST | `/usuarios` | Cadastrar um registro |
| GET | `/usuarios` | Listar os registros |
| GET | `/usuarios/{usuario_id}` | Consultar um registro pelo ID |
| PUT | `/usuarios/{usuario_id}` | Atualizar um registro |
| DELETE | `/usuarios/{usuario_id}` | Excluir um registro |

O CRUD de usuários já está implementado como referência. Para as entidades do tema, siga as mesmas operações e consulte os objetos pelo ID real do banco:

```python
with Sessao() as banco:
    usuario = banco.get(Usuario, usuario_id)
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")

    # Atualizar: atribuir os novos valores aos campos e chamar banco.commit().
    # Excluir: chamar banco.delete(usuario) e depois banco.commit().
```

Todas as entidades exigidas deverão utilizar o MySQL. Valide campos obrigatórios, tamanhos de texto e valores numéricos no backend, mesmo que a tela também faça validações. Operações sobre IDs inexistentes devem responder com `404`; dados inválidos devem receber uma resposta compreensível. Não devolva diretamente objetos da sessão: siga a listagem fornecida e monte dicionários com os campos da resposta.

### 5.2. Frontend

Mantenha os arquivos em `frontend/` e siga as páginas do exemplo:

- Acrescente links no `index.html` para as entidades do tema.
- Crie páginas para cadastro, listagem, atualização e exclusão de cada entidade.
- Permita consultar os dados de um registro; essa consulta pode preencher a tela de edição usando `GET /entidade/{id}`.
- Envie e receba JSON com `fetch`, usando os métodos HTTP da tabela anterior.
- Mostre mensagens de sucesso e erro, verifique `resposta.ok` e trate falhas de conexão.
- Use `textContent` para exibir dados recebidos e peça confirmação antes de excluir.
- Inclua um link de retorno ao menu nas páginas.

**O ID agora vem do banco.** Nos seletores de edição e exclusão, use `opcao.value = usuario.id`, e não o índice do `forEach`. IDs não precisam ser consecutivos e não mudam quando outro registro é excluído.

Na versão com banco, os seletores já utilizam `usuario.id`, a listagem mostra esse ID e o botão de atualizar a lista usa o evento `click`. Preserve esses ajustes ao criar as páginas das entidades do tema.

### 5.3. Docker Compose

Mantenha três serviços, como em `MeuProjeto-Com-BD/docker-compose.yml`:

- `frontend`: Nginx servindo os arquivos de `frontend/`, publicado na porta `8001`.
- `backend`: FastAPI, construído pelo Dockerfile fornecido, publicado na porta `8000`.
- `db`: MySQL, acessado pelo backend pela rede interna, sem publicar a porta do banco no hospedeiro.

Preserve as variáveis de conexão, o usuário da aplicação diferente de `root`, o `healthcheck`, a dependência do backend em relação ao banco e o volume nomeado de dados. O Dockerfile existente é suficiente para o backend; não é necessário criar outro para o frontend.

## 6. Verificar a persistência

Após cadastrar um registro de uma entidade armazenada no MySQL:

```bash
docker compose down
docker compose up -d
```

Acesse a listagem e confirme que o registro permanece disponível. Use a mesma pasta e o mesmo projeto Compose no teste.

**Não utilize `docker compose down -v` nesse teste:** a opção `-v` remove o volume com os dados do banco.

## 7. Avaliação

| Critério | Valor |
|---|---:|
| Tema vinculado ao projeto integrador ou a Engenharia de Software, com definição das quatro entidades e seus campos | 0,5 |
| Docker Compose: três serviços, construção do backend, comunicação, portas, variáveis, healthcheck e volume | 1,5 |
| Backend: CRUD das quatro entidades no MySQL, classes SQLAlchemy, validações e uso correto dos IDs | 1,0 |
| Frontend: telas e menu do tema, operações com fetch e mensagens de retorno | 1,0 |
| Documentação e demonstração, incluindo persistência após recriar os contêineres | 1,0 |
| **Total** | **5,0** |

Será considerada a cobertura das quatro entidades e das operações exigidas. Apenas executar o cadastro de usuários fornecido não conclui a atividade.

## 8. Entrega e demonstração

Entregue:

1. Código-fonte organizado como `MeuProjeto`: `backend/main.py`, `backend/requirements.txt`, arquivos de `frontend/`, `Dockerfile` e `docker-compose.yml`.
2. README com integrantes, tema, vínculo com o projeto integrador ou Engenharia de Software, entidades/campos e comandos para executar e acessar a aplicação.
3. Relatório em PDF com arquitetura (serviços, portas e comunicação), tabelas/campos, capturas do CRUD e evidência da persistência.

Na apresentação, todos os integrantes deverão explicar a solução. Mostrem os três serviços em execução, as operações das quatro entidades pelas telas, uma validação de dados, o tratamento de um ID inexistente e a permanência dos registros depois de `docker compose down` e `docker compose up -d`.

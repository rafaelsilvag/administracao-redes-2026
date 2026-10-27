# Atividade de Administração de Redes: aplicação web com Docker Compose, FastAPI, MySQL e Nginx

## Visão geral

Nesta atividade, os alunos trabalharão em equipes de **até três integrantes** para desenvolver e implantar uma aplicação web utilizando contêineres Docker.

Cada equipe escolherá um tema e implementará uma aplicação composta por **três serviços**, executados em contêineres separados e gerenciados pelo Docker Compose:

- **Backend:** aplicação em Python com FastAPI, responsável pelas regras de negócio, pelo acesso aos dados e pela renderização das telas HTML com Jinja2.
- **Banco de dados:** MySQL, responsável pelo armazenamento persistente.
- **Frontend/proxy:** Nginx, responsável por receber o acesso do navegador e encaminhar as requisições para o FastAPI.

A interface será formada por templates HTML com formulários, seguindo o exemplo fornecido. Não é necessário implementar JavaScript para consumir uma API JSON.

**Valor total: 5,0 pontos.**

## 1. Tema e funcionalidades da aplicação

Cada equipe deverá escolher um tema e definir **pelo menos quatro entidades distintas**, relacionadas ao funcionamento da aplicação.

Exemplos:

| Tema | Exemplos de entidades |
|---|---|
| Biblioteca | Livros, autores, leitores e empréstimos |
| Loja | Produtos, categorias, clientes e pedidos |
| Clínica veterinária | Tutores, animais, veterinários e consultas |
| Gestão de eventos | Eventos, participantes, espaços e inscrições |
| Administração de redes | Equipamentos, setores, serviços e chamados |

As entidades devem fazer sentido dentro do tema escolhido. Quatro registros de uma mesma entidade não atendem ao requisito de quatro entidades.

Para **cada uma das quatro entidades**, a aplicação deverá permitir:

1. **Cadastrar:** inserir um novo registro.
2. **Consultar:** listar os registros e visualizar os detalhes de um registro específico.
3. **Atualizar:** editar os dados de um registro existente.
4. **Excluir:** remover um registro, respeitando os relacionamentos e as regras do sistema.

Todas essas operações deverão estar disponíveis na interface web e utilizar dados armazenados no MySQL.

### 1.1. Aplicação inicial fornecida

Utilize a pasta [esqueleto](esqueleto/) como ponto de partida. Consulte o [guia de instalação](GUIA-INSTALACAO.md) para executar o exemplo localmente antes de adaptá-lo ao Docker Compose.

A estrutura principal do exemplo é:

```text
esqueleto/
├── main.py
├── requirements.txt
├── banco.sql
└── templates/
    ├── menu.html
    └── tela_usuarios.html
```

- `main.py`: conexão com o banco, classes das tabelas, validações e rotas, reunidas em um único arquivo Python.
- `templates/menu.html`: menu principal, exibido na rota `/`.
- `templates/tela_usuarios.html`: formulário de cadastro/edição e listagem de usuários.
- `requirements.txt`: dependências da aplicação.
- `banco.sql`: preparação inicial do banco e do usuário MySQL para execução local.

O exemplo já permite gerenciar usuários. Cada equipe deverá adaptá-lo ao tema escolhido e completar o CRUD das quatro entidades. A entidade usuário poderá fazer parte das quatro, se fizer sentido no tema.

Para cada entidade, mantenha uma tela HTML própria em `templates`, seguindo `tela_usuarios.html`, e adicione um link no menu principal. Todas as telas de gerenciamento deverão oferecer um link para retornar ao menu. Mantenha o código Python no `main.py`, sem exigir separação em módulos.

## 2. Arquitetura obrigatória

A aplicação deverá seguir o fluxo:

```text
Navegador do usuário
        |
        | HTTP — porta publicada no hospedeiro (ex.: 8080)
        v
Frontend/proxy — Nginx
        |
        | encaminha as rotas e os formulários
        v
Backend — FastAPI + templates Jinja2
        |
        | conexão interna pelo nome do serviço db
        v
Banco de dados — MySQL
```

O navegador deverá acessar a aplicação pelo Nginx. O Nginx encaminhará as requisições ao FastAPI, que renderizará os templates e devolverá as páginas HTML pelo mesmo caminho.

Os links e formulários deverão usar caminhos relativos ao site, como `/`, `/usuarios` e `/usuarios/1/editar`. O proxy deverá preservar esses caminhos, sem exigir o prefixo `/api/`.

O backend deverá acessar o MySQL pela rede do Docker Compose, utilizando o nome do serviço `db` como endereço (`DB_HOST=db`).

## 3. Requisitos de infraestrutura

### 3.1. Docker Compose

A equipe deverá entregar um arquivo `compose.yaml` ou `docker-compose.yml` com os três serviços: `frontend`, `backend` e `db`.

O ambiente deverá ser construído e iniciado com:

```bash
docker compose up -d --build
```

A configuração deverá contemplar:

- Rede para comunicação entre os serviços.
- Volume nomeado para persistência dos dados do MySQL.
- Variáveis de ambiente para configurar a conexão com o banco.
- Verificação de disponibilidade do MySQL com `healthcheck`.
- Dependência do backend em relação à disponibilidade do banco, utilizando `depends_on` com `condition: service_healthy`.
- Publicação da porta HTTP do Nginx no hospedeiro, por exemplo, `8080:80`.

O banco de dados não deverá ter sua porta publicada no hospedeiro. O backend também deverá ser acessado pela interface por meio do Nginx.

Será permitida a utilização de imagens oficiais do Python, MySQL e Nginx. A equipe deverá criar um Dockerfile para o backend e outro para o frontend, incorporando os arquivos e as configurações necessários.

### 3.2. Backend com FastAPI

O backend deverá:

- Ser desenvolvido em Python com FastAPI.
- Executar em um servidor ASGI, como o Uvicorn, escutando em `0.0.0.0` dentro do contêiner (por exemplo, `uvicorn main:app --host 0.0.0.0 --port 8000`).
- Manter a conexão, as classes das tabelas e as rotas no arquivo `main.py`.
- Renderizar os arquivos HTML do diretório `templates` com Jinja2.
- Disponibilizar a rota `/` com um menu de acesso às quatro entidades.
- Disponibilizar as rotas necessárias ao CRUD das quatro entidades.
- Receber os dados por formulários HTML, usando `Form`, e retornar páginas HTML.
- Após cadastrar, editar ou excluir, redirecionar para a listagem da entidade, seguindo o exemplo com `RedirectResponse` e status `303`.
- Validar campos obrigatórios e tipos de dados.
- Retornar respostas adequadas para operações bem-sucedidas, dados inválidos e registros inexistentes.
- Utilizar um usuário próprio do banco de dados, diferente de `root`.
- Manter os valores fornecidos pelo usuário com escape HTML, como na configuração Jinja2 do exemplo.

Para uma entidade chamada `produtos`, siga a organização do CRUD de usuários:

| Método | Rota | Operação |
|---|---|---|
| GET | `/` | Mostrar o menu principal |
| GET | `/produtos` | Listar e mostrar o formulário de cadastro |
| POST | `/produtos` | Cadastrar |
| GET | `/produtos/{id}` | Visualizar os dados e preencher o formulário de edição |
| POST | `/produtos/{id}/editar` | Atualizar |
| POST | `/produtos/{id}/excluir` | Excluir |

A listagem e o formulário poderão ficar na mesma página, como no template fornecido. Os formulários usam `POST` também para editar e excluir; não é necessário criar rotas `PUT`, `PATCH` ou `DELETE`, nem uma API JSON separada.

### 3.3. Banco de dados MySQL

O banco deverá conter:

- Pelo menos quatro tabelas principais, correspondentes às entidades.
- Chaves primárias em todas as tabelas.
- Pelo menos dois relacionamentos entre entidades, implementados com chaves estrangeiras.
- Restrições coerentes com os dados, como campos obrigatórios e valores únicos, quando aplicável.
- Um mecanismo de criação inicial da estrutura, pelas classes SQLAlchemy com `Base.metadata.create_all(engine)`, como no exemplo, ou por script SQL. No contêiner MySQL, configure também a criação do banco e do usuário da aplicação.

A aplicação deverá tratar exclusões que afetem registros relacionados, apresentando uma mensagem compreensível ao usuário.

Os dados deverão permanecer disponíveis após a remoção e recriação dos contêineres, desde que o volume seja preservado.

### 3.4. Interface HTML e Nginx

A interface deverá utilizar templates HTML renderizados pelo FastAPI e apresentar:

- Menu principal na rota `/`, com links para gerenciar as quatro entidades.
- Listagem dos registros de cada entidade.
- Visualização dos dados de um registro, podendo usar o próprio formulário de edição.
- Formulários de cadastro e edição.
- Ação de exclusão com confirmação, como no exemplo fornecido.
- Mensagens compreensíveis para erros de validação e operações não permitidas.
- Campos apropriados para selecionar registros relacionados, como escolher o cliente de um pedido.
- Link para retornar ao menu principal em cada tela de gerenciamento.

As operações deverão ser executadas pelos links e formulários das telas. A documentação automática do FastAPI não substituirá a interface exigida.

O Nginx deverá encaminhar todas as rotas da aplicação ao serviço `backend`, incluindo `/`, as listagens e os envios de formulários. Os templates deverão ser incluídos na imagem do backend, pois o FastAPI é responsável por renderizá-los. Não é necessário copiar esses templates para a imagem do Nginx.

O CSS poderá permanecer nos próprios templates, como no exemplo. Não é necessário adicionar JavaScript além da confirmação de exclusão já fornecida.

## 4. Etapas e pontuação

| Etapa | Critérios | Valor |
|---|---|---:|
| Planejamento e modelagem | Tema, definição das quatro entidades, campos, relacionamentos e diagrama da arquitetura | 0,5 |
| Infraestrutura com Docker Compose | Três serviços, Dockerfiles, rede, portas, variáveis de ambiente, volume e inicialização coordenada | 1,5 |
| Backend e banco de dados | CRUD das quatro entidades, validações, relacionamentos e persistência no MySQL | 1,0 |
| Frontend e integração | Telas das quatro entidades, CRUD pela interface e encaminhamento das requisições pelo Nginx | 1,0 |
| Relatório e demonstração | Documentação, evidências de funcionamento e explicação da solução | 1,0 |
| **Total** | | **5,0** |

Nos itens de backend e frontend, será considerada a cobertura das quatro entidades e das operações exigidas. Funcionalidades incompletas poderão receber pontuação parcial.

## 5. Entrega

A equipe deverá entregar o código-fonte e os arquivos necessários para executar o ambiente, incluindo:

- Arquivo do Docker Compose.
- Dockerfiles do backend e do frontend.
- Arquivo `main.py` e arquivo de dependências.
- Diretório `templates` com `menu.html` e as telas das quatro entidades.
- Configuração do Nginx.
- Definição das tabelas no SQLAlchemy ou scripts SQL, além da configuração de criação do banco e do usuário MySQL.
- Arquivo `.env.example` com as variáveis necessárias e valores fictícios.
- README com as instruções de configuração, execução, acesso e encerramento.
- Relatório final em PDF.

O relatório deverá apresentar:

1. Identificação dos integrantes e tema escolhido.
2. Descrição das quatro entidades e de suas funcionalidades.
3. Diagrama da arquitetura, com serviços, portas e comunicação.
4. Modelo do banco, com tabelas e relacionamentos.
5. Explicação das redes, volumes e variáveis de ambiente.
6. Capturas de tela que comprovem o CRUD das quatro entidades.
7. Evidência da persistência dos dados após a recriação dos contêineres.
8. Dificuldades encontradas e soluções adotadas.

## 6. Demonstração prática

Durante a apresentação, a equipe deverá:

1. Construir e iniciar o ambiente com Docker Compose.
2. Mostrar os três serviços em execução.
3. Acessar a aplicação pelo endereço publicado pelo Nginx.
4. Acessar o menu principal e demonstrar cadastro, listagem, visualização, edição e exclusão nas quatro entidades, utilizando as telas HTML.
5. Demonstrar uma validação de dados e o tratamento de um registro relacionado.
6. Cadastrar um registro e encerrar o ambiente com `docker compose down`.
7. Iniciar novamente o ambiente e comprovar que o registro permanece disponível.

**Atenção:** o comando `docker compose down -v` remove os volumes nomeados declarados no Compose e não deverá ser utilizado no teste de persistência.

Todos os integrantes deverão participar da apresentação e ser capazes de explicar a arquitetura e o funcionamento da solução.

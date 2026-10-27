# Guia inicial: FastAPI, HTML e MySQL

O FastAPI recebe os formulários, acessa o MySQL com SQLAlchemy e devolve páginas HTML. A conexão, a classe que representa a tabela e as rotas ficam no mesmo arquivo Python.

## 1. Estrutura

```text
esqueleto/
├── main.py                  # Conexão, tabela e todas as rotas
├── templates/
│   └── usuarios.html        # Formulário e listagem
├── requirements.txt        # Bibliotecas Python
├── banco.sql               # Criação do banco e usuário MySQL
├── .env.example            # Exemplo de configuração
├── .gitignore
└── README.md
```

## 2. Instalar os programas

Em Ubuntu 22.04/24.04, para uma máquina de estudo com MySQL local:

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip mysql-server
sudo systemctl enable --now mysql
```

Se o laboratório já tem um servidor MySQL, use o endereço e as credenciais fornecidos pelo professor em vez de instalar outro servidor.

## 3. Criar o ambiente Python

No terminal, entre na pasta `esqueleto` da sua cópia do projeto:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Repita `source .venv/bin/activate` sempre que abrir um novo terminal para trabalhar no projeto.

| Biblioteca | Para que serve |
|---|---|
| FastAPI | Receber as requisições e executar as funções das rotas |
| Uvicorn | Executar o servidor da aplicação |
| SQLAlchemy | Representar a tabela como classe Python e consultar/gravar dados |
| PyMySQL com extra rsa | Conectar o Python ao MySQL, incluindo autenticação do MySQL 8 |
| Jinja2 | Preencher o HTML com dados enviados pelo Python |
| python-multipart | Ler campos enviados por formulários HTML |
| python-dotenv | Ler as configurações do arquivo `.env` |

## 4. Preparar o MySQL e a configuração

Na pasta `esqueleto`, execute o script como administrador do MySQL:

```bash
sudo mysql < banco.sql
cp .env.example .env
```

O script cria o banco `atividade` e o usuário `aluno`, com a senha didática `senha_didatica`. Se alterar a senha no script, altere também `DB_PASSWORD` no `.env`. Se esse usuário já existir, `CREATE USER IF NOT EXISTS` não troca sua senha.

Conteúdo de `.env` para o exemplo local:

```dotenv
DB_HOST=localhost
DB_PORT=3306
DB_NAME=atividade
DB_USER=aluno
DB_PASSWORD=senha_didatica
```

Não envie o `.env` para o Git. O script é para o MySQL local; em servidor remoto, o administrador precisa fornecer um usuário autorizado a conectar a partir da sua máquina.

## 5. Iniciar

Com o ambiente virtual ativo, na pasta `esqueleto`:

```bash
uvicorn main:app --reload
```

Abra <http://127.0.0.1:8000>. Para encerrar, pressione `Ctrl+C` no terminal.

Ao iniciar, o SQLAlchemy cria a tabela `usuarios` se ela ainda não existir. O banco precisa estar disponível antes de iniciar a aplicação.

## 6. Entender o exemplo

Leia `main.py` na ordem dos comentários numerados:

1. **Conexão:** lê `.env`, cria o endereço de conexão e configura as sessões do banco.
2. **Tabela:** a classe `Usuario` representa `usuarios`, com `id`, `nome` e `email` único.
3. **Inicialização:** cria a tabela e configura o HTML.
4. **Listagem:** consulta os usuários e passa os dados para `usuarios.html`.
5. **Cadastro:** recebe `nome` e `email` por `Form`, cria um objeto e faz `commit`.
6. **Visualização:** busca um usuário pelo identificador e preenche o formulário.
7. **Edição:** altera os campos do objeto e confirma a transação.
8. **Exclusão:** remove o objeto e confirma a transação.

`with Sessao() as db` abre uma sessão e garante seu fechamento. `commit()` confirma alterações; `rollback()` desfaz a transação quando ocorre um erro, como e-mail repetido.

No HTML, `{{ item.nome }}` imprime um dado, `{% for item in usuarios %}` repete as linhas da tabela e `{% if usuario %}` permite usar a mesma tela para cadastro e edição. O Jinja2 escapa o conteúdo exibido nos campos HTML.

Os formulários usam `method="post"` e enviam os dados diretamente para as rotas Python. Após gravar, o FastAPI redireciona para a listagem. Não é necessário escrever chamadas `fetch` ou trabalhar com JSON nesta etapa.

| Caminho | Método | Função |
|---|---|---|
| `/` | GET | Listar e mostrar formulário de cadastro |
| `/usuarios` | POST | Cadastrar |
| `/usuarios/{id}` | GET | Visualizar e abrir edição |
| `/usuarios/{id}/editar` | POST | Salvar edição |
| `/usuarios/{id}/excluir` | POST | Excluir |

A escolha de POST para edição e exclusão acompanha o funcionamento de formulários HTML comuns. O CRUD continua completo, sem exigir uma API REST separada neste momento.

## 7. Testar

1. Cadastre um usuário com nome e e-mail.
2. Confira o registro na listagem.
3. Clique em **Visualizar / editar**, altere o nome e salve.
4. Tente cadastrar outro usuário com o mesmo e-mail: a tela deve informar a duplicidade.
5. Pare o FastAPI e inicie novamente: os dados devem continuar na listagem.
6. Exclua o usuário, confirme a ação e confira que ele saiu da listagem.

Para conferir a tabela diretamente:

```bash
mysql -h localhost -u aluno -p atividade
```

Informe a senha do exemplo e execute:

```sql
SHOW TABLES;
SELECT * FROM usuarios;
exit
```

## 8. Adaptar para o trabalho

Cada grupo pode acrescentar as classes e as rotas das suas entidades no próprio `main.py` e criar outros arquivos HTML na pasta `templates`. Comece adaptando `Usuario` para uma entidade do tema e repita o fluxo para as demais.

Concentre-se em cadastrar, listar, visualizar, editar e excluir. Acrescente as entidades e os relacionamentos conforme a orientação do professor.

`create_all()` cria tabelas ausentes, mas não altera colunas de tabelas existentes. Mudanças na estrutura devem ser acompanhadas de alterações no banco. Não é necessário introduzir ferramentas de migração nesta etapa.

Este exemplo cadastra pessoas com nome e e-mail; não implementa login. A validação do e-mail no Python é básica, para fins didáticos.

## Problemas comuns

- **Comando uvicorn não encontrado:** ative `.venv` e instale `requirements.txt`.
- **Access denied:** confira o usuário, a senha e as permissões no MySQL.
- **Can't connect:** confira se o MySQL está ativo e se o endereço e a porta estão corretos.
- **Unknown database:** execute `banco.sql` antes de iniciar.
- **Porta 8000 ocupada:** use `uvicorn main:app --reload --port 8001` e abra a porta 8001.

## Referências

- [Formulários no FastAPI](https://fastapi.tiangolo.com/tutorial/request-forms/)
- [HTML com templates no FastAPI](https://fastapi.tiangolo.com/advanced/templates/)
- [Conexão com SQLAlchemy](https://docs.sqlalchemy.org/en/20/core/engines.html)

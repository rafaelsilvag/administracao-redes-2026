# Aplicação de exemplo: FastAPI, HTML e MySQL

Esqueleto inicial para os grupos desenvolverem uma aplicação web com cadastro, listagem, visualização, edição e exclusão de dados.

Consulte o [enunciado da atividade](ATIVIDADE.md).

A aplicação reúne em um único arquivo Python a conexão com o MySQL, a classe `Usuario` e as rotas. O HTML é servido pelo próprio FastAPI.

## Arquivos

- `esqueleto/main.py`: aplicação e CRUD de usuários.
- `esqueleto/templates/menu.html`: menu principal.
- `esqueleto/templates/tela_usuarios.html`: formulário e listagem de usuários.
- `esqueleto/requirements.txt`: bibliotecas necessárias.
- `esqueleto/banco.sql`: preparação do banco e do usuário MySQL.
- `esqueleto/.env.example`: exemplo de configuração da conexão.

## Como começar

Siga o [guia de instalação](GUIA-INSTALACAO.md) para preparar Python e MySQL. As instruções resumidas estão no [README do esqueleto](esqueleto/README.md).

Depois de preparar o banco, na pasta `esqueleto`:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn main:app --reload
```

Confira os dados da conexão no `.env` antes de iniciar. Acesse <http://127.0.0.1:8000>.

Cada grupo deverá adaptar o exemplo ao seu tema e implementar as entidades e os relacionamentos solicitados pelo professor.

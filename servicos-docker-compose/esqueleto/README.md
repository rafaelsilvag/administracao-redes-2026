# Aplicação inicial do grupo

Uma única aplicação FastAPI com HTML e SQLAlchemy, usando MySQL.

1. Configure o banco executando `banco.sql` como administrador.
2. Copie `.env.example` para `.env` e confira os dados da conexão.
3. Crie e ative um ambiente virtual.
4. Instale as dependências e inicie:

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

Abra <http://127.0.0.1:8000> para acessar o menu principal. A opção **Gerenciar usuários** abre o CRUD em `/usuarios`.

As rotas ficam no `main.py` e o HTML nos arquivos `templates/menu.html` e `templates/tela_usuarios.html`. Para incluir outro CRUD no menu, adicione um link `<li><a href="/sua-rota">Gerenciar ...</a></li>` em `templates/menu.html` e implemente as rotas correspondentes no `main.py`.

Veja o [guia completo](../GUIA-INSTALACAO.md) para os comandos de instalação e as explicações. Se copiar somente esta pasta, leve também o guia.

Identifique aqui o tema e os integrantes do grupo. Adapte o exemplo de usuário às entidades do seu trabalho.

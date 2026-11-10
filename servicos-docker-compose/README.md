# Aplicação de exemplo: FastAPI, HTML e MySQL

Material para adaptar uma aplicação ao projeto integrador ou a uma atividade da disciplina de Engenharia de Software. Consulte o [enunciado da atividade](ATIVIDADE.md).

## Exemplos

- [MeuProjeto](MeuProjeto/): exemplo original, com CRUD de usuários em uma lista Python e páginas HTML que acessam a API com `fetch`.
- [MeuProjeto-Com-BD](MeuProjeto-Com-BD/): mesma estrutura e mesmos nomes de arquivos HTML, acrescentando MySQL, SQLAlchemy e CRUD de usuários em `backend/main.py`.

Na versão com banco, **os usuários persistem no MySQL**, com os campos `nome` e `senha` do exemplo original. Os seletores de edição/exclusão e a listagem utilizam o ID gerado pelo banco. O evento do botão de atualizar a lista também foi corrigido. As consultas retornam `id` e `nome`.

## Executar a versão com banco

Com Docker e Docker Compose instalados, na raiz deste repositório:

```bash
cd MeuProjeto-Com-BD
docker compose up -d --build
```

- Frontend: <http://127.0.0.1:8001>.
- Backend e documentação da API: <http://127.0.0.1:8000/docs>.
- Usuários cadastrados: <http://127.0.0.1:8000/usuarios>.

O Compose cria o banco `meuprojeto`, configura o usuário didático `aluno`, aguarda o MySQL e inicia o backend. O SQLAlchemy cria a tabela `usuarios` automaticamente. A primeira inicialização pode demorar enquanto as imagens são baixadas e o banco é preparado.

Para encerrar, execute `docker compose down`. Os usuários permanecem no volume nomeado; `docker compose down -v` remove esse volume e seus dados.

As duas versões usam as mesmas portas: encerre uma antes de iniciar a outra. O navegador acessa o backend diretamente na porta `8000`; se usar outra máquina, ajuste o endereço nos `fetch` dos HTML.

Veja no [enunciado](ATIVIDADE.md) o primeiro cadastro de usuários, as orientações para as novas telas e os requisitos de entrega. O antigo [guia de instalação](GUIA-INSTALACAO.md) descreve uma estrutura anterior com templates e não é o roteiro desta versão.

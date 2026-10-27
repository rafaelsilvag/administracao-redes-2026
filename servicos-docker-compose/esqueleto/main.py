import os
from contextlib import asynccontextmanager
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import Column, Integer, String, URL, create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import declarative_base, sessionmaker

# 1. Conexão com o banco de dados.
PASTA = Path(__file__).resolve().parent
load_dotenv(PASTA / ".env")
url = URL.create(
    "mysql+pymysql",
    username=os.environ["DB_USER"],
    password=os.environ["DB_PASSWORD"],
    host=os.environ.get("DB_HOST", "localhost"),
    port=int(os.environ.get("DB_PORT", "3306")),
    database=os.environ["DB_NAME"],
    query={"charset": "utf8mb4"},
)
engine = create_engine(url, pool_pre_ping=True)
Sessao = sessionmaker(bind=engine)
Base = declarative_base()

# 2. Classe que representa a tabela usuarios no MySQL.
class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(254), nullable=False, unique=True)

# 3. Inicialização da aplicação e criação da tabela, caso não exista.
@asynccontextmanager
async def iniciar(app: FastAPI):
    Base.metadata.create_all(engine)
    yield
    engine.dispose()

app = FastAPI(title="Cadastro de usuários", lifespan=iniciar)
templates = Jinja2Templates(directory=str(PASTA / "templates"))

# As telas enviam formulários HTML; não é necessário JavaScript nem schemas.
def mostrar(request, db, usuario=None, mensagem="", status=200):
    usuarios = db.query(Usuario).order_by(Usuario.id).all()
    return templates.TemplateResponse(
        request=request,
        name="usuarios.html",
        context={"usuarios": usuarios, "usuario": usuario, "mensagem": mensagem},
        status_code=status,
    )

def validar(nome, email):
    # Validação básica didática. O navegador também valida o formulário.
    if not 2 <= len(nome) <= 100:
        return "O nome deve ter entre 2 e 100 caracteres."
    if len(email) > 254 or email.count("@") != 1 or not all(email.split("@")) or any(c.isspace() for c in email):
        return "Informe um e-mail válido."
    return ""

# 4. Listar usuários e mostrar o formulário de cadastro.
@app.get("/")
def inicio(request: Request):
    with Sessao() as db:
        return mostrar(request, db)

# 5. Gravar um novo usuário.
@app.post("/usuarios")
def cadastrar(request: Request, nome: str = Form(...), email: str = Form(...)):
    nome, email = nome.strip(), email.strip()
    with Sessao() as db:
        erro = validar(nome, email)
        if erro:
            return mostrar(request, db, mensagem=erro, status=422)
        db.add(Usuario(nome=nome, email=email))
        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            return mostrar(request, db, mensagem="E-mail já cadastrado.", status=409)
    return RedirectResponse(url="/", status_code=303)

# 6. Visualizar os dados de um usuário e preencher o formulário de edição.
@app.get("/usuarios/{usuario_id}")
def visualizar(request: Request, usuario_id: int):
    with Sessao() as db:
        usuario = db.get(Usuario, usuario_id)
        if usuario is None:
            return mostrar(request, db, mensagem="Usuário não encontrado.", status=404)
        return mostrar(request, db, usuario=usuario)

# 7. Atualizar os dados de um usuário.
@app.post("/usuarios/{usuario_id}/editar")
def editar(request: Request, usuario_id: int, nome: str = Form(...), email: str = Form(...)):
    nome, email = nome.strip(), email.strip()
    with Sessao() as db:
        usuario = db.get(Usuario, usuario_id)
        if usuario is None:
            return mostrar(request, db, mensagem="Usuário não encontrado.", status=404)
        erro = validar(nome, email)
        if erro:
            return mostrar(request, db, usuario=usuario, mensagem=erro, status=422)
        usuario.nome = nome
        usuario.email = email
        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            return mostrar(request, db, usuario=usuario, mensagem="E-mail já cadastrado.", status=409)
    return RedirectResponse(url="/", status_code=303)

# 8. Excluir um usuário.
@app.post("/usuarios/{usuario_id}/excluir")
def excluir(request: Request, usuario_id: int):
    with Sessao() as db:
        usuario = db.get(Usuario, usuario_id)
        if usuario is None:
            return mostrar(request, db, mensagem="Usuário não encontrado.", status=404)
        db.delete(usuario)
        db.commit()
    return RedirectResponse(url="/", status_code=303)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

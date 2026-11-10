import os

from fastapi import Body, FastAPI, HTTPException
from sqlalchemy import Column, Integer, String, create_engine, select
from sqlalchemy.engine import URL
from sqlalchemy.orm import declarative_base, sessionmaker
import uvicorn

from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 1. Conexão. No Compose, o endereço do MySQL é o nome do serviço: db.
endereco_banco = URL.create(
    "mysql+pymysql",
    username=os.getenv("DB_USER", "aluno"),
    password=os.getenv("DB_PASSWORD", "senha_didatica"),
    host=os.getenv("DB_HOST", "db"),
    port=int(os.getenv("DB_PORT", "3306")),
    database=os.getenv("DB_NAME", "meuprojeto"),
    query={"charset": "utf8mb4"},
)
engine = create_engine(endereco_banco, pool_pre_ping=True)
Sessao = sessionmaker(bind=engine)
Base = declarative_base()


# 2. A classe representa a tabela; cada objeto representa um usuário.
class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    senha = Column(String(100), nullable=False)


# Cria as tabelas que ainda não existem. O banco é criado pelo MySQL/Compose.
Base.metadata.create_all(engine)


def validar_usuario(dados):
    nome = dados.get("nome")
    senha = dados.get("senha")
    if not isinstance(nome, str) or not nome.strip() or len(nome.strip()) > 100:
        raise HTTPException(status_code=400, detail="Informe um nome com até 100 caracteres.")
    if not isinstance(senha, str) or not senha.strip() or len(senha.strip()) > 100:
        raise HTTPException(status_code=400, detail="Informe uma senha com até 100 caracteres.")
    return nome.strip(), senha.strip()


@app.get("/")
def inicio():
    return {"mensagem": "Bem vindo a FastAPI!"}


# 3. Receber JSON, criar um objeto e gravar no banco.
@app.post("/usuarios", status_code=201)
def cad_usuario(dados: dict = Body(...)):
    nome, senha = validar_usuario(dados)
    with Sessao() as banco:
        usuario = Usuario(nome=nome, senha=senha)
        banco.add(usuario)
        banco.commit()
        banco.refresh(usuario)
        return {"mensagem": f"Usuário {usuario.nome} cadastrado com sucesso!", "id": usuario.id}


# 4. Consultar os objetos e devolver uma lista de dicionários em JSON.
@app.get("/usuarios")
def listar_usuarios():
    with Sessao() as banco:
        usuarios = banco.scalars(select(Usuario).order_by(Usuario.id)).all()
        return [{"id": usuario.id, "nome": usuario.nome} for usuario in usuarios]


# 5. Buscar pela chave primária, em vez da posição em uma lista.
@app.get("/usuarios/{usuario_id}")
def visualizar_usuario(usuario_id: int):
    with Sessao() as banco:
        usuario = banco.get(Usuario, usuario_id)
        if usuario is None:
            raise HTTPException(status_code=404, detail="Usuário não encontrado.")
        return {"id": usuario.id, "nome": usuario.nome}


# 6. Alterar os campos do objeto e confirmar a alteração.
@app.put("/usuarios/{usuario_id}")
def alterar_usuario(usuario_id: int, dados: dict = Body(...)):
    nome, senha = validar_usuario(dados)
    with Sessao() as banco:
        usuario = banco.get(Usuario, usuario_id)
        if usuario is None:
            raise HTTPException(status_code=404, detail="Usuário não encontrado.")
        usuario.nome = nome
        usuario.senha = senha
        banco.commit()
        return {"mensagem": f"Usuário {nome} alterado com sucesso!"}


# 7. Remover o objeto do banco e confirmar a exclusão.
@app.delete("/usuarios/{usuario_id}")
def deletar_usuario(usuario_id: int):
    with Sessao() as banco:
        usuario = banco.get(Usuario, usuario_id)
        if usuario is None:
            raise HTTPException(status_code=404, detail="Usuário não encontrado.")
        banco.delete(usuario)
        banco.commit()
        return {"mensagem": f"Usuário ID {usuario_id} removido com sucesso!"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

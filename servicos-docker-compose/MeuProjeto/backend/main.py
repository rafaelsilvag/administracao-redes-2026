from fastapi import FastAPI, Request
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

lista_usuarios = []

@app.get("/")
def inicio():
    return {"mensagem": "Bem vindo a FastAPI!"}

@app.post("/usuarios")
async def cad_usuario(request: Request):
    dados = await request.json()
    nome = dados.get("nome").strip()
    senha = dados.get("senha").strip()

    lista_usuarios.append({ "nome": nome, "senha": senha })

    return {"mensagem": f"Usuário {nome}/{senha} cadastrado com sucesso!"}

@app.get("/usuarios")
async def listar_usuarios():
    return lista_usuarios

@app.get("/usuarios/{usuario_id}")
async def visualizar_usuario(usuario_id: int):
    return lista_usuarios[usuario_id]

@app.put("/usuarios/{usuario_id}")
async def alterar_usuario(usuario_id: int, request: Request):
    dados = await request.json()
    nome = dados.get("nome").strip()
    senha = dados.get("senha").strip()
    lista_usuarios[usuario_id] = {"nome": nome, "senha": senha}
    return {"mensagem": f"Usuário {nome} alterado com sucesso!"}

@app.delete("/usuarios/{usuario_id}")
async def deletar_usuario(usuario_id: int):
    lista_usuarios.pop(usuario_id)
    return {"mensagem": f"Usuário ID {usuario_id} removido com sucesso!"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
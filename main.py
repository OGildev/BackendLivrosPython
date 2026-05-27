
# API de Livros

# Métodos HTTP: GET, POST, PUT, DELETE

# POST - Adicionar novos livros (Create)
# GET - Buscar os dados dos livros (Read)
# PUT - Atualizar informações dos livros (Update)
# DELETE - Deletar informações dos livros (Delete)

# CRUD

# Create
# Read
# Update
# Delete

# Query Strings

# Comando para inicializar servidor: fastapi dev .\Aula1.py

# Documentação Swagger -> Documentar os endpoints da nossa aplicação da nossa API

from tracemalloc import start

from fastapi import FastAPI, HTTPException, Depends # type: ignore
from fastapi.security import HTTPBasic, HTTPBasicCredentials # type: ignore
from pydantic import BaseModel # type: ignore
from typing import Optional
import secrets
import os

app = FastAPI(
    title="API de Livros",
    description="API para gerenciar catálogo de livros",
    version="1.0.0",
    contact={
        "name":"Gilberto Lima",
        "email":"ogildev@gmail.com"
    }
)

USUARIO = "admin"
SENHA = "admin"

security = HTTPBasic()

def autenticacao(credentials: HTTPBasicCredentials = Depends(security)):
    is_username_correct = secrets.compare_digest(credentials.username, USUARIO)
    is_password_correct = secrets.compare_digest(credentials.password, SENHA)

    if not (is_username_correct and is_password_correct):
        raise HTTPException(
            status_code=401,
            detail="Usuário ou senha incorretos",
            headers={"WWW-Authenticate": "Basic"},
        )

livros = {}

class Livro(BaseModel):
    nome_livro: str
    autor_livro: str
    ano_livro: int

@app.get("/")
def hello_world():
    return {"Hello": "World!"}

@app.get("/livros")
def get_livros(page: int = 1, limit: int = 10, credentials: HTTPBasicCredentials = Depends(autenticacao)):
    if page < 1 or limit < 1:
        raise HTTPException(status_code=300, detail="Page e limit estão incorretos! Eles devem ser maiores que 0!")

    if not livros:
        return {"message": "Não existe nenhum livro"} 
        
    start = (page - 1) * limit
    end = start + limit
    
    livros_paginados = [
        {"id": id_livro, "nome_livro": livro_data["nome_livro"], "autor_livro": livro_data["autor_livro"], "ano_livro": livro_data["ano_livro"]}
        for id_livro, livro_data in list(livros.items())[start:end]
    ]
    return {
        "page": page,
        "limit": limit,
        "total_livros": len(livros),
        "livros": livros_paginados
        } 

# id do livro
# nome do livro
# autor do livro
# ano de lançamento do livro

@app.post("/adicionar")
def post_livros(id_livro: int, livro: Livro, credentials: HTTPBasicCredentials = Depends(autenticacao)): # Alteração feita para referenciar a classe Livro a fim de não precisarmos utilizar Query Strings nas chamadas do método POST
    if id_livro in livros:
        raise HTTPException(status_code=400, detail="Esse livro já existe!")
    else:
        livros[id_livro] = livro.dict() # Alteração feita pois não estamos mais passando como parametro os campos. Eles estão referenciados na classe. Código antigo: {"nome_livro": nome_livro, "autor_livro": autor_livro, "ano_livro": ano_livro}
        return {"message": "O livro foi criado com sucesso"}
    
@app.put("/atualizar/{id_livro}")
def put_livros(id_livro: int, livro: Livro, credentials: HTTPBasicCredentials = Depends(autenticacao)): # Alteração feita para referenciar a classe Livro a fim de não precisarmos utilizar Query Strings nas chamadas do método POST
    meu_livro = livros.get(id_livro)
    if not meu_livro:
        raise HTTPException(status_code=404, detail="Esse livro não foi encontrado!")
    else:
        livros[id_livro] = livro.dict() 
        return {"message": "As informações do seu livro foram atualizados com sucesso!"}
    
@app.delete("/deletar/{id_livro}")
def delete_livro(id_livro: int, credentials: HTTPBasicCredentials = Depends(autenticacao)):
    if id_livro not in livros:
        raise HTTPException(status_code=404, detail="Esse livro não foi encontrado!")
    else:
        del livros[id_livro]

        return {"message": "Seu livro foi deletado com sucesso!"}

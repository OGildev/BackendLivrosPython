
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

from fastapi import FastAPI, HTTPException # type: ignore
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

livros = {}

class Livro(BaseModel):
    nome_livro: str
    autor_livro: str
    ano_livro: int

@app.get("/livros")
def get_livros():
    if not livros:
        return {"message": "Não existe nenhum livro"} 
    else:
        return {"livros": livros} 

# id do livro
# nome do livro
# autor do livro
# ano de lançamento do livro

@app.post("/adicionar")
def post_livros(id_livro: int, livro: Livro): # Alteração feita para referenciar a classe Livro a fim de não precisarmos utilizar Query Strings nas chamadas do método POST
    if id_livro in livros:
        raise HTTPException(status_code=400, detail="Esse livro já existe!")
    else:
        livros[id_livro] = livro.dict() # Alteração feita pois não estamos mais passando como parametro os campos. Eles estão referenciados na classe. Código antigo: {"nome_livro": nome_livro, "autor_livro": autor_livro, "ano_livro": ano_livro}
        return {"message": "O livro foi criado com sucesso"}
    
@app.put("/atualizar/{id_livro}")
def put_livros(id_livro: int, livro: Livro): # Alteração feita para referenciar a classe Livro a fim de não precisarmos utilizar Query Strings nas chamadas do método POST
    meu_livro = livros.get(id_livro)
    if not meu_livro:
        raise HTTPException(status_code=404, detail="Esse livro não foi encontrado!")
    else:
        livros[id_livro] = livro.dict() 
        return {"message": "As informações do seu livro foram atualizados com sucesso!"}
    
@app.delete("/deletar/{id_livro}")
def delete_livro(id_livro: int):
    if id_livro not in livros:
        raise HTTPException(status_code=404, detail="Esse livro não foi encontrado!")
    else:
        del livros[id_livro]

        return {"message": "Seu livro foi deletado com sucesso!"}

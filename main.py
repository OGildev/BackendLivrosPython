

from fastapi import FastAPI, HTTPException  # type: ignore

app = FastAPI()

tarefas = [
    {"nome":"Tarefa1", "descricao":"Lavar louça", "concluida": False},
    {"nome":"Tarefa 2", "descricao":"Estudar Python", "concluida": False},    
    {"nome":"Tarefa 3", "descricao":"2hrs de games para curtição", "concluida": False}
]

@app.get("/tarefas")
def get_tarefas():
    if not tarefas:
        return {"message": "Não existe essa tarefa."}
    else:
        return {"tarefas": tarefas}
    
@app.post("/adicionar/{nome}/{descricao}")
def post_tarefas(nome: str, descricao: str):
    for tarefa in tarefas:
        if tarefa["nome"] == nome:
            raise HTTPException(status_code = 400, detail = "Essa tarefa já existe!")
        
    nova_tarefa = {"nome": nome, "descricao": descricao, "concluida": False}    
    tarefas.append(nova_tarefa)

    return{"message": "A tarefa foi adicionada com sucesso!"}

@app.put("/atualizar/{nome}")
def put_tarefa(nome: str):
    for tarefa in tarefas:
        if tarefa["nome"] == nome:
            tarefa["concluida"] = True
            return{"message": "A tarefa foi alterada com sucesso!"}
        
    raise HTTPException(status_code = 400, detail = "Essa tarefa não existe para ser atualizada!")    

@app.delete("/deletar/{nome}")
def delete_tarefa(nome: str):
    for tarefa in tarefas:
        if tarefa["nome"] == nome:
            tarefas.remove(tarefa)
            return {"message": "Tarefa deletada com sucesso!"}    
        
    raise HTTPException(status_code=404, detail="Não existe tarefa para ser excluída!")

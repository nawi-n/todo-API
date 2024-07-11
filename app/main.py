from fastapi import FastAPI, HTTPException, Query, Path
from pymongo import MongoClient
from app.schema import TodoModel,ObjectId

app = FastAPI()

uri = "mongodb+srv://admin:pass@cluster0.akmxuag.mongodb.net/?appName=Cluster0"
client = MongoClient(uri)
db = client.todo_db
collection = db["To-do"]

@app.get("/")
async def all_todos():
    todos=[]
    for todo in collection.find():
        todos.append(todo)
    return todos

@app.post("/")
def post_todo(todo: TodoModel):
    todo_dict = todo.dict(by_alias=True)
    result=collection.insert_one(todo_dict)
    return {"meassage" : "todo created successfully",
            "id" : str(result.inserted_id),
            "task" : todo.task,
            "status": todo.done }


@app.put("/{key}")
async def update_todo(key: str, todo: TodoModel):
    todo_dict = todo.dict(by_alias=True)
    result = collection.update_one({"_id": ObjectId(key)}, {"$set": todo_dict})
    if result.modified_count == 1:
        return {"message": "Todo updated successfully"}
    else:
        raise HTTPException(status_code=404, detail=f"Todo with id {key} not found")

@app.delete("/{key}")
async def delete_todo(key: str):
    result = collection.delete_one({"_id": ObjectId(key)})
    if result.deleted_count == 1:
        return {"message": "Todo deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail=f"Todo with id {key} not found")












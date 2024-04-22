from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from model import vector_search, generate_sql, embeddings, index, table_descriptions
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

class Query(BaseModel):
    text: str

@app.post("/generate-sql/")
def generate_sql_endpoint(query: Query):
    table_names = list(table_descriptions.keys())
    best_tables = vector_search(query.text, embeddings, index, table_names)
    if not best_tables:
        raise HTTPException(status_code=404, detail="No relevant tables found")
    sql_query = generate_sql(query.text, best_tables)
    return {"query": query.text, "sql_query": sql_query}

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_root():
    return {"message": "Hello World, visit /static/index.html to see the SQL query generator"}
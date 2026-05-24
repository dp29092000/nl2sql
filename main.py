from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.schema_retriever import SchemaRetriever
from src.prompt_builder import build_prompt, generate_sql
from src.sql_executor import execute_sql
from pydantic import BaseModel

retriever = SchemaRetriever()

@asynccontextmanager
async def lifespan(app: FastAPI):
    retriever.build_index()
    yield

app = FastAPI(lifespan=lifespan)

class QueryRequest(BaseModel):
    question: str

@app.post("/query")
def query(request: QueryRequest):
    db_id,schema = retriever.retrieve_schema(request.question)
    print(f"db_id: {db_id}")
    print(f"file path: database/{db_id}/{db_id}.sqlite")
    print(f"schema: {schema}") 
    prompt = build_prompt(request.question,schema)
    sql = generate_sql(prompt)
    print(sql)
    result = execute_sql(db_id,sql)
    return {"sql": sql, "result": result}
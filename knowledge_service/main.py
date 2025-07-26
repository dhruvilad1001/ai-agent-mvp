# # from fastapi import FastAPI
# # from pydantic import BaseModel
# # from chromadb import Client
# # from chromadb.config import Settings
# # from sentence_transformers import SentenceTransformer

# # app = FastAPI()

# # client = Client(Settings(chroma_db_impl="duckdb+parquet", persist_directory="./db"))
# # collection = client.get_or_create_collection("knowledge")
# # model = SentenceTransformer("all-MiniLM-L6-v2")

# # class IngestRequest(BaseModel):
# #     documents: list[str]

# # class SearchQuery(BaseModel):
# #     query: str

# # @app.post("/ingest")
# # def ingest_data(req: IngestRequest):
# #     ids = [f"doc_{i}" for i in range(len(req.documents))]
# #     embeddings = model.encode(req.documents).tolist()
# #     collection.add(documents=req.documents, embeddings=embeddings, ids=ids)
# #     return {"status": "success", "count": len(req.documents)}

# # @app.post("/query")
# # def query_kb(req: SearchQuery):
# #     query_embedding = model.encode([req.query]).tolist()[0]
# #     results = collection.query(query_embeddings=[query_embedding], n_results=1)
# #     if results and results.get("documents") and results["documents"][0]:
# #         return {"result": results["documents"][0][0]}
# #     return {"result": None}



# from fastapi import FastAPI
# from pydantic import BaseModel
# import chromadb
# from sentence_transformers import SentenceTransformer

# app = FastAPI()

# client = chromadb.PersistentClient(path="./db")
# collection = client.get_or_create_collection("knowledge")
# model = SentenceTransformer("all-MiniLM-L6-v2")

# class IngestRequest(BaseModel):
#     documents: list[str]

# class SearchQuery(BaseModel):
#     query: str

# @app.post("/ingest")
# def ingest_data(req: IngestRequest):
#     ids = [f"doc_{i}" for i in range(len(req.documents))]
#     embeddings = model.encode(req.documents).tolist()
#     collection.add(documents=req.documents, embeddings=embeddings, ids=ids)
#     return {"status": "success", "count": len(req.documents)}

# @app.post("/query")
# def query_kb(req: SearchQuery):
#     query_embedding = model.encode([req.query]).tolist()[0]
#     results = collection.query(query_embeddings=[query_embedding], n_results=1)
#     if results and results.get("documents") and results["documents"][0]:
#         return {"result": results["documents"][0][0]}
#     return {"result": None}



from fastapi import FastAPI
from pydantic import BaseModel
import chromadb
from sentence_transformers import SentenceTransformer

app = FastAPI()

# Initialize ChromaDB and embedding model
client = chromadb.PersistentClient(path="./db")
collection = client.get_or_create_collection("knowledge")
model = SentenceTransformer("all-MiniLM-L6-v2")

# Request models
class IngestRequest(BaseModel):
    documents: list[str]

class SearchQuery(BaseModel):
    query: str

# Ingest endpoint
@app.post("/ingest")
def ingest_data(req: IngestRequest):
    ids = [f"doc_{i}" for i in range(len(req.documents))]
    embeddings = model.encode(req.documents).tolist()
    collection.add(documents=req.documents, embeddings=embeddings, ids=ids)
    return {"status": "success", "count": len(req.documents)}

# Query endpoint with similarity check
@app.post("/query")
def query_kb(req: SearchQuery):
    query_embedding = model.encode([req.query]).tolist()[0]
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=1,
        include=["distances"]
    )

    if (
        results and
        results.get("documents") and results["documents"][0] and
        results.get("distances") and results["distances"][0][0] < 0.5  # Adjust threshold as needed
    ):
        return {"result": results["documents"][0][0]}
    
    return {"result": None}

# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# import requests
# import uuid

# app = FastAPI()

# # -------- Data Models -------- #
# class QueryRequest(BaseModel):
#     chat_id: str = None
#     query: str

# class QueryResponse(BaseModel):
#     chat_id: str
#     response: str

# # -------- Endpoint -------- #
# @app.post("/chat", response_model=QueryResponse)
# def chat(query_req: QueryRequest):
#     chat_id = query_req.chat_id or str(uuid.uuid4())
#     query = query_req.query

#     # 1. Try Knowledge Base
#     kb_response = requests.post("http://localhost:8001/query", json={"query": query})
#     if kb_response.status_code == 200 and kb_response.json().get("result"):
#         answer = kb_response.json()["result"]
#     else:
#         # 2. Fallback to Search
#         search_response = requests.get(f"http://localhost:8002/search?query={query}")
#         if search_response.status_code != 200:
#             raise HTTPException(status_code=500, detail="Search service failed")
#         answer = search_response.json()["result"]

#     # 3. Save to History
#     requests.post("http://localhost:8003/history", json={
#         "chat_id": chat_id,
#         "query": query,
#         "response": answer
#     })

#     return {"chat_id": chat_id, "response": answer}


# @app.get("/chat/{chat_id}")
# def get_chat(chat_id: str):
#     history_response = requests.get(f"http://localhost:8003/history/{chat_id}")
#     if history_response.status_code != 200:
#         raise HTTPException(status_code=404, detail="Chat not found")
#     return history_response.json()


from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import uuid
import logging

# -------- Logging -------- #
logging.basicConfig(level=logging.INFO)

# -------- FastAPI App -------- #
app = FastAPI()

# -------- Data Models -------- #
class QueryRequest(BaseModel):
    chat_id: str = None
    query: str

class QueryResponse(BaseModel):
    chat_id: str
    response: str

# -------- Endpoint: Chat -------- #
@app.post("/chat", response_model=QueryResponse)
def chat(query_req: QueryRequest):
    chat_id = query_req.chat_id or str(uuid.uuid4())
    query = query_req.query

    # 1. Try Knowledge Base
    kb_response = requests.post("http://localhost:8001/query", json={"query": query})
    if kb_response.status_code == 200 and kb_response.json().get("result"):
        answer = kb_response.json()["result"]
        logging.info("Answer from Knowledge Base")
    else:
        # 2. Fallback to Search
        search_response = requests.get(f"http://localhost:8002/search?query={query}")
        if search_response.status_code != 200:
            raise HTTPException(status_code=500, detail="Search service failed")
        answer = search_response.json()["result"]
        logging.info("Answer from Search Service")

    # 3. Save to History
    try:
        requests.post("http://localhost:8003/history", json={
            "chat_id": chat_id,
            "query": query,
            "response": answer
        })
    except Exception as e:
        logging.warning(f"Failed to store chat history: {e}")

    return {"chat_id": chat_id, "response": answer}

# -------- Endpoint: Get Chat History -------- #
@app.get("/chat/{chat_id}")
def get_chat(chat_id: str):
    history_response = requests.get(f"http://localhost:8003/history/{chat_id}")
    if history_response.status_code != 200:
        raise HTTPException(status_code=404, detail="Chat not found")
    return history_response.json()

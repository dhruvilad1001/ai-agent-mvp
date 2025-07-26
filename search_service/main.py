from fastapi import FastAPI, HTTPException
from duckduckgo_search import DDGS

app = FastAPI()

@app.get("/search")
def search(query: str):
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, region='wt-wt', safesearch='Moderate', timelimit='y'))
            if results:
                top_result = results[0]
                return {"result": top_result["body"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"result": "No results found"}

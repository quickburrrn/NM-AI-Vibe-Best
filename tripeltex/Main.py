from fastapi import FastAPI
from pydantic import BaseModel
from app.agent.pipeline import run_pipeline

# Define the request schema
class SolveRequest(BaseModel):
    prompt: str
    credentials: dict  # e.g., {"token": "...", "proxy_url": "..."}
    files: list | None = None  # optional PDF/image attachments

app = FastAPI()

@app.post("/solve")
async def solve(req: SolveRequest):
    """
    Entrypoint for AI accounting agent.
    Delegates parsing, planning, execution, and validation to the pipeline.
    """
    try:
        await run_pipeline(req.prompt, req.credentials, req.files)
        return {"status": "completed"}
    except Exception as e:
        return {"status": "failed", "error": str(e)}
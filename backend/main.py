
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from backend.research_agent import conduct_research

app = FastAPI(
    title="Multi-Agent AI Research Assistant",
    description="Research questions using web search and AI.",
    version="1.0.0",
)


class ResearchRequest(BaseModel):
    question: str = Field(
        min_length=3,
        max_length=1000,
        description="The topic or question to research.",
    )


@app.get("/health")
def health_check():
    return {"status": "ok", "message": "Research API is running."}


@app.post("/research")
def research(request: ResearchRequest):
    try:
        return conduct_research(request.question)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))
    except Exception:
        raise HTTPException(
            status_code=502,
            detail="Research failed. Check the backend terminal logs.",
        )

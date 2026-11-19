from fastapi import FastAPI, HTTPException
from app.schemas import LinkAnalysisRequest, LinkAnalysisResponse
from app.services.analysis_service import run_link_analysis
from app.services.llm_service import LLMServiceError
from app.services.website_extractor import WebsiteExtractionError
from app.utils.validators import URLValidationError

app = FastAPI(
    title="AI-Powered Website Link Analysis API",
    description="Extracts website content and generates competitive, SEO, search query, service, and audience insights using an LLM.",
    version="1.0.0",
)


@app.get("/", tags=["Health"])
async def health_check():
    return {"status": "ok", "docs": "/docs", "endpoint": "POST /link-analysis"}


@app.post("/link-analysis", response_model=LinkAnalysisResponse, tags=["Analysis"])
async def link_analysis(payload: LinkAnalysisRequest):
    try:
        return await run_link_analysis(payload.url)
    except URLValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except WebsiteExtractionError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except LLMServiceError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Unexpected server error: {str(exc)}") from exc
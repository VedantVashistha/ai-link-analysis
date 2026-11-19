import asyncio
from app.schemas import LinkAnalysisResponse
from app.services.competitor_service import enrich_competitor_analysis
from app.services.llm_service import analyze_content_with_llm
from app.services.website_extractor import fetch_and_extract_website
from app.utils.validators import validate_public_url


async def run_link_analysis(raw_url: str) -> LinkAnalysisResponse:
    # 1. Validate URL & SSRF protection
    safe_url = validate_public_url(raw_url)

    # 2. Fetch & clean HTML
    extracted = await fetch_and_extract_website(safe_url)

    # 3. Run LLM analysis in worker thread so FastAPI event loop stays non-blocking
    llm_result = await asyncio.to_thread(analyze_content_with_llm, extracted)

    # 4. Post-process competitor transparency flags
    llm_result.analysis.competitor_analysis = enrich_competitor_analysis(
        llm_result.analysis.competitor_analysis
    )

    return LinkAnalysisResponse(
        success=True,
        website=extracted["url"],
        brand=llm_result.brand,
        analysis=llm_result.analysis,
    )
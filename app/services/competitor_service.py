from app.schemas import CompetitorAnalysis


def enrich_competitor_analysis(comp_analysis: CompetitorAnalysis) -> CompetitorAnalysis:
    """Ensures every competitor entry explicitly discloses AI-assisted market inference."""
    for comp in comp_analysis.competitors:
        comp.is_ai_suggested = True
    return comp_analysis
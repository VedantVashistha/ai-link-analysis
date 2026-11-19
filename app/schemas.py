from typing import List, Optional
from pydantic import BaseModel, Field


# --- Request Schema ---
class LinkAnalysisRequest(BaseModel):
    url: str = Field(..., example="https://example.com", description="Public website URL to analyze")


# --- Section 1: Competitor vs Your Brand Details ---
class CompetitorDetail(BaseModel):
    name: str
    main_service: str
    target_market: str
    strengths: List[str]
    weaknesses_or_gaps: List[str]
    is_ai_suggested: bool = Field(
        default=True,
        description="Marks whether competitor info is AI-inferred rather than directly scraped",
    )


class CompetitorAnalysis(BaseModel):
    brand_overview: str
    main_products_and_services: List[str]
    competitors: List[CompetitorDetail] = Field(..., min_length=1)
    strengths: List[str] = Field(..., description="Your brand's competitive advantages")
    opportunities: List[str] = Field(..., description="Opportunities to improve market positioning")


# --- Section 2: Top 5 Target Search Queries ---
class TargetSearchQuery(BaseModel):
    query: str
    platforms: List[str] = Field(..., description="Suitable platforms: Google Search, Facebook, Instagram, LinkedIn, X")
    intent: str
    business_relevance: str
    target_audience: str


# --- Section 3: SEO Improvement ---
class SEOImprovements(BaseModel):
    primary_keyword: str
    secondary_keywords: List[str]
    long_tail_keywords: List[str]
    relevant_business_keywords: List[str]
    recommended_title: str
    title_structure_notes: str
    meta_description: str
    supporting_content: List[str]


# --- Section 4: Top 5 Services ---
class ServiceItem(BaseModel):
    service_name: str
    description: str
    target_industry: str
    target_customer: str
    main_benefit: str
    source_type: str = Field(..., description="'Extracted from website' or 'Inferred recommendation'")


# --- Section 5: Target Audience Identification ---
class AudienceSegment(BaseModel):
    audience_label: str
    business_type: str
    requirement: str


class TargetAudience(BaseModel):
    primary_audience: List[str]
    secondary_audience: List[str]
    industries: List[str]
    business_types: List[str]
    customer_profiles: List[str]
    geographical_focus: Optional[str] = None
    customer_needs: List[str]
    customer_interests: List[str]
    recommended_marketing_segments: List[AudienceSegment]


# --- Brand & Combined LLM Output Schema ---
class BrandInfo(BaseModel):
    name: str
    category: str
    summary: str


class AnalysisSections(BaseModel):
    competitor_analysis: CompetitorAnalysis
    target_search_queries: List[TargetSearchQuery]
    seo_improvements: SEOImprovements
    top_services: List[ServiceItem]
    target_audience: TargetAudience


class LLMWebsiteAnalysisPayload(BaseModel):
    brand: BrandInfo
    analysis: AnalysisSections


# --- Final API Response Schema ---
class LinkAnalysisResponse(BaseModel):
    success: bool = True
    website: str
    brand: BrandInfo
    analysis: AnalysisSections
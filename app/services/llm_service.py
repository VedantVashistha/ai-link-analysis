import json
import re
import time
from typing import Dict
from google import genai
from google.genai import types
from app.config import settings
from app.schemas import LLMWebsiteAnalysisPayload


class LLMServiceError(Exception):
    pass


def _extract_json_text(raw_text: str) -> str:
    cleaned = raw_text.strip()
    match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", cleaned)
    if match:
        return match.group(1).strip()
    return cleaned


def analyze_content_with_llm(extracted_data: Dict[str, str]) -> LLMWebsiteAnalysisPayload:
    if not settings.gemini_api_key:
        raise LLMServiceError("GEMINI_API_KEY is not configured in environment variables.")

    client = genai.Client(
        api_key=settings.gemini_api_key,
        http_options=types.HttpOptions(timeout=30000),
    )

    schema_hint = json.dumps(LLMWebsiteAnalysisPayload.model_json_schema(), indent=2)

    base_prompt = f"""
You are a senior digital strategy, competitive intelligence, and SEO analyst.
Analyze the following extracted website content and produce a comprehensive, grounded structured analysis.

STRICT RULES:
1. Base all brand, product, service, and audience insights directly on the provided website content. Do NOT invent generic placeholder companies.
2. Identify at least 3 realistic competitors in the same industry/niche. Clearly mark `is_ai_suggested: true` when competitor details are derived from market knowledge rather than explicitly stated on the page.
3. Generate exactly 5 target search queries mapped across Google Search, Facebook, Instagram, LinkedIn, and X (Twitter). Do NOT invent search volume numbers or ranking metrics.
4. Provide actionable SEO improvements (primary, secondary, long-tail keywords, improved SEO title, meta description, and supporting content ideas).
5. Identify up to 5 top services from the website content; if fewer than 5 are explicitly listed, clearly label additional ones with `source_type: "Inferred recommendation"`.
6. Provide thorough Target Audience segmentation.

--- WEBSITE DATA ---
URL: {extracted_data['url']}
Page Title: {extracted_data['title']}
Meta Description: {extracted_data['meta_description']}

Headings:
{extracted_data['headings']}

Cleaned Body Content:
{extracted_data['body_text']}
"""

    models_to_try = [settings.gemini_model, "gemini-3.5-flash-lite"]
    last_error = None

    for model_name in models_to_try:
        for attempt in range(2):
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=base_prompt,
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                        response_schema=LLMWebsiteAnalysisPayload,
                        temperature=0.2,
                    ),
                )
                if not response.text:
                    raise LLMServiceError("Empty response received from LLM.")

                return LLMWebsiteAnalysisPayload.model_validate_json(_extract_json_text(response.text))
            except Exception as exc:
                last_error = exc
                err_str = str(exc)

                if "503" in err_str or "UNAVAILABLE" in err_str or "429" in err_str:
                    time.sleep(2)
                    continue

                # If 400 INVALID_ARGUMENT is caused by response_schema constraints, retry once with JSON mime type + schema prompt
                if "400" in err_str or "INVALID_ARGUMENT" in err_str:
                    try:
                        fallback_prompt = (
                            f"{base_prompt}\n\nReturn ONLY valid JSON matching this JSON Schema:\n{schema_hint}"
                        )
                        fb_response = client.models.generate_content(
                            model=model_name,
                            contents=fallback_prompt,
                            config=types.GenerateContentConfig(
                                response_mime_type="application/json",
                                temperature=0.2,
                            ),
                        )
                        if fb_response.text:
                            return LLMWebsiteAnalysisPayload.model_validate_json(
                                _extract_json_text(fb_response.text)
                            )
                    except Exception as fb_exc:
                        last_error = fb_exc
                break

    raise LLMServiceError(f"LLM analysis failed: {str(last_error)}")
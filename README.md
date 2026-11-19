# AI-Powered Website Link Analysis API

A FastAPI and Python 3.x REST service (`POST /link-analysis`) that accepts a public website URL, validates it against Server-Side Request Forgery (SSRF) risks, extracts and cleans its HTML content, and generates structured business, competitor, target search query, SEO, service, and target audience insights using Google Gemini[cite: 1, 10, 12].

## Live Deployment & API Links

- **Live Base URL:** `https://ai-link-analysis-s9lq.onrender.com`[cite: 10]
- **Analysis Endpoint:** `POST https://ai-link-analysis-s9lq.onrender.com/link-analysis`[cite: 10, 11]
- **Interactive Swagger UI (`/docs`):** `https://ai-link-analysis-s9lq.onrender.com/docs`[cite: 10, 11]
- **Local Endpoint:** `http://localhost:4000/link-analysis` (Docs: `http://localhost:4000/docs`)

> **Note on Free Hosting:** On Render's free tier, the service may spin down during inactivity and take up to ~50 seconds on the initial cold request[cite: 10].

---

## Key Features & Functional Coverage

The `POST /link-analysis` endpoint returns structured JSON organized around brand metadata and **five core analysis sections**:

1. **Competitor vs. Your Brand Details:** Brand name, business overview, main category, core products/services, at least 3 relevant competitors (explicitly flagged with `is_ai_suggested` when inferred via model market knowledge), competitor strengths/weaknesses, brand advantages, and market positioning opportunities.
2. **Top 5 Target Search Queries:** Five customer search queries mapped across **Google Search**, **Facebook**, **Instagram**, **LinkedIn**, and **X (Twitter)** with search intent, business relevance, and target audience context (without fabricated search volumes).
3. **SEO Improvements:** Primary, secondary, and long-tail keywords, recommended SEO title, meta description, and supporting content ideas (landing pages, FAQs, blogs, industry/location pages).
4. **Top 5 Services:** Up to five key services with service name, description, target industry, target customer, main benefit, and source attribution (distinguishing explicit website offerings from inferred recommendations).
5. **Target Audience Identification:** Primary and secondary audiences, industry segments, business types, customer profiles, geographical focus (when present), needs/challenges, interests, and recommended marketing segments[cite: 5, 12].

---

## Project Structure

```text
ai-link-analysis/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── schemas.py
│   ├── services/
│   │   ├── website_extractor.py
│   │   ├── llm_service.py
│   │   ├── analysis_service.py
│   │   └── competitor_service.py
│   └── utils/
│       └── validators.py
├── tests/
│   └── test_link_analysis.py
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md

# AI-Powered Website Link Analysis API

A FastAPI and Python 3.x REST service (`POST /link-analysis`) that validates a public website URL, extracts and cleans its HTML content, and generates structured business, competitor, target search query, SEO, service, and target audience insights using Gemini[cite: 1, 2, 7, 9].

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
├── requirements.txt
└── README.md
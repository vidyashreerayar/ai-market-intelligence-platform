# Cutting Reporting Lag: AI-Powered Market Intelligence for Trusted Decisions

An AI-powered market intelligence platform for Intersnack — built to bridge data architecture and business users across procurement, manufacturing, and sales, replacing slow manual reporting with fast, explainable, cited answers.

## Problem & Context

Intersnack operates 35–40+ production sites across 30+ countries, generating ~€4.5–4.6bn in sales (2025) with a workforce of ~15,000. Intersnack's procurement, manufacturing, and sales teams face volatile commodity costs (potatoes, oils, energy), demanding retailer negotiations, and complex multi-country demand planning — yet decision-relevant data stays scattered and manual to access. This slows reaction to price swings, weakens forecasting accuracy, and erodes negotiating leverage with retailers.

**Estimated annual cost of this gap:** €1.9M–5.5M (headcount × hours lost to manual reporting × hourly cost — see Research Insights below for the full calculation).

## Goal

Cut reporting lag with a trustworthy, explainable AI-grounded analytics platform bridging data architecture and business users across procurement, manufacturing, and sales.

## Users

Procurement, Manufacturing, Sales — the exact functions named in the AI Engineer, Analytics & End-User Insights job posting. Every feature has one clear owner: the pricing agent serves Procurement, the market agent serves Sales, and so on.

## Solution Overview

- **Intent-based routing** — an LLM classifier (not keyword matching) determines which specialist agent should handle each question, with a confidence threshold and fallback
- **True RAG pipeline** — news is ingested (NewsAPI), cleaned, embedded, and indexed into a PostgreSQL/pgvector store, replacing raw unstructured lookups
- **Explainable, cited answers** — every factual claim is tied to a numbered source, shown to the user with a relevance score
- **Structured pricing data** — German potato prices from Eurostat, queried directly (no embedding needed for numeric time series)
- **Prove Impact dashboard** — live KPIs (routing confidence, retrieval relevance, citation rate) shown against baseline manual-reporting estimates

## Architecture

![Architecture diagram](docs/architecture_diagram.svg)

```
Sources (NewsAPI, Eurostat)
        ↓
ETL: extract → transform → load
        ↓
Storage: PostgreSQL (news_articles, potato_prices) + news_embeddings (vector index)
        ↓
AI layer: supervisor.py (intent routing) → 4 specialist agents
        ↓
UI: Streamlit app — answer + sources + Prove Impact dashboard
```

Full file-level breakdown:
| Layer | File | Role |
|---|---|---|
| Extract | `scrapers/news_api.py`, `etl/extract.py` | Fetch from NewsAPI, Eurostat |
| Transform | `etl/transform.py` | Clean, dedupe, structure |
| Load | `etl/load.py` | Write to PostgreSQL, dedup by url/year |
| Index | `etl/indexer.py` | Embed news into pgvector (`news_embeddings`) |
| Orchestrate | `etl/pipeline.py` | Runs the full ETL + indexing flow |
| Route | `agents/supervisor.py` | Classifies intent, logs KPIs per query |
| Answer | `agents/news_agent.py`, `market_agent.py`, `trend_agent.py`, `pricing_agent.py` | Retrieve + answer with citations |
| Metrics | `etl/metrics.py` | Logs and aggregates KPIs |
| UI | `app.py` | Streamlit — Q&A tab + Prove Impact tab |

## KPIs (Prove Impact)

**Business KPIs:** decision cycle time, report trust score, negotiation leverage — measure whether people actually use and benefit from the tool.

**Technical KPIs (computed live):** routing confidence, retrieval relevance (similarity score), citation rate, source coverage, data freshness — measure whether the tool is accurate and honest, which is what makes the business KPIs credible.

| Metric | Before (manual) | After (AI) |
|---|---|---|
| Report cycle time | 5–10 days | Seconds |
| Analyst time on reporting | 20–30% | Query-driven, on-demand |
| Routing confidence | N/A | Live, see Prove Impact tab |
| Retrieval relevance | N/A | Live, see Prove Impact tab |
| Citation rate | N/A | Live, see Prove Impact tab |

## Research Insights

Full categorized research (company facts, job description, industry PESTLE analysis) with sources and whose point of view each insight serves — see [`docs/research_insights.md`](docs/research_insights.md).

**Cost impact formula:** headcount (~150–225, estimated from ~15,000 employees × 1–1.5% analytical-role ratio) × hours lost/year (360–540, from 20–30% manual-reporting benchmark) × hourly cost (€35–45, German analyst salary proxy) = **€1.9M–5.5M/year**. All assumptions are stated explicitly; this is a directional estimate, not Intersnack's actual figures.

## Primary Sources
- [Intersnack Group Overview](https://www.intersnackgroup.com/about-us/overview)
- [Intersnack Careers](https://www.intersnackgroup.com/careers/career-opportunities)
- [Intersnack Sustainability Approach](https://www.intersnack.de/en/sustainability/our-approach-to-sustainability)
- [Job Posting — AI Engineer, Analytics & End-User Insights](https://joinus.intersnack-it.com/o/ai-engineer-analytics-end-user-insights)

## How to Run

1. Install dependencies: `pip install -r requirements.txt`
2. Set environment variables in `.env`: `GROQ_API_KEY`, `NEWS_API_KEY`, database connection string
3. Run the ETL pipeline to populate data: `python -m etl.pipeline`
4. Launch the app: `streamlit run app.py`

## Limitations & Next Steps

- No real Intersnack user interviews — problem framing is validated via public company research and the job description instead
- Cost/impact figures are directional estimates from public benchmarks, not Intersnack's internal data
- Factory visit insights (planned per the original project roadmap) are not yet incorporated — pending access
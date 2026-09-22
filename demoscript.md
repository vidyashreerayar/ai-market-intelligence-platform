
# Demo Script — Intersnack Market Intelligence Platform

~8-10 minute walkthrough for the interview.

## 1. Problem walkthrough (1-2 min)

"Intersnack operates 35-40+ sites across 30+ countries. Procurement, manufacturing, and sales teams deal with volatile commodity costs, demanding retailer negotiations, and complex multi-country planning — but the data they need is scattered and manual to pull together. I estimated this costs somewhere between €1.9M and 5.5M a year in lost analyst time and delayed decisions, based on public benchmarks.

This maps directly to the AI Engineer, Analytics & End-User Insights role — the JD specifically calls for decoupled data pipelines, explainable KPIs, and RAG-driven analytics that extend existing BI. I built a working version of that."

## 2. Live end-to-end demo (3-4 min)

Open the app and ask, in order:

1. **"How have potato prices changed from 2000 to 2024?"**
   → Shows structured data path — pricing agent queries Eurostat data directly, renders the line chart with min/max/latest metrics.

2. **"What recent product launches have competitors announced?"**
   → Shows the RAG path — intent routed to market_agent, retrieves from the vector index, answer includes numbered citations. Open the Sources expander to show the actual articles and relevance scores.

3. **"What are the emerging consumer trends in the snack industry?"**
   → Same RAG path, different category (trend_agent) — demonstrates the intent router correctly distinguishing between competitor and trend questions.

**Narrate while it runs:** "Every claim in the answer is cited — you can click through to the actual article. This isn't the model guessing; it's grounded in real indexed data."

## 3. Key scenarios (1-2 min)

- **Low-confidence routing:** ask something ambiguous (e.g. "tell me about snacks") and show it falls back gracefully instead of guessing wrong.
- **Prove Impact tab:** switch tabs, show the before/after table — 5-10 days manual reporting vs seconds, plus live routing confidence and citation rate numbers pulled from actual usage.

## 4. Before vs. after (1 min)

| | Before | After |
|---|---|---|
| Report cycle | 5-10 days | Seconds |
| Trust | No visibility into sourcing | Every claim cited, relevance-scored |
| Routing | N/A (manual) | LLM-classified with confidence + fallback |

## 5. Q&A / next steps (1-2 min)

Be ready for:
- **"Where did your numbers come from?"** → Public company research (Intersnack's own site + job posting = primary; industry PESTLE reports = secondary, clearly flagged in the README).
- **"What would you do with real access?"** → Validate the cost-impact estimate with real headcount/time data, connect to actual internal BI (Qlik/Power BI) instead of public APIs, incorporate factory visit insights per the original plan.
- **"How does this scale?"** → Landing-zone → transform → load → index pattern is the same regardless of data volume; swapping NewsAPI/Eurostat for internal data sources doesn't change the architecture.

**Close:** "This was built in [X days] as a demonstration of the exact architecture pattern the role asks for — I'd want to validate the assumptions with real Intersnack data and users next."
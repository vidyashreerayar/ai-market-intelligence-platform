import re
import logging
from datetime import datetime

from sqlalchemy import text
from database.connection import engine

logger = logging.getLogger(__name__)


def ensure_schema():
    with engine.connect() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS query_metrics (
                id SERIAL PRIMARY KEY,
                question TEXT NOT NULL,
                category TEXT,
                routing_confidence FLOAT,
                avg_retrieval_similarity FLOAT,
                num_sources INT,
                citation_rate FLOAT,
                latency_seconds FLOAT,
                logged_at TIMESTAMP DEFAULT NOW()
            );
        """))
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS prompt_logs (
                id SERIAL PRIMARY KEY,
                question TEXT NOT NULL,
                category TEXT,
                system_prompt TEXT,
                prompt_version TEXT,
                logged_at TIMESTAMP DEFAULT NOW()
            );
        """))
        conn.commit()


def _citation_rate(answer_text: str, num_sources: int) -> float:
    """% of available sources that were actually cited at least once in the answer."""
    if num_sources == 0:
        return 0.0
    cited = set(re.findall(r"\[Source (\d+)\]", answer_text))
    return round(len(cited) / num_sources, 3)


def log_query_metrics(question: str, category: str, routing_confidence: float,
                       sources: list, answer_text: str, latency_seconds: float = None):
    """
    Call this after every route_question() call in supervisor.py.
    sources: the list of source dicts returned by the agent (each has 'similarity').
    """
    similarities = [s["similarity"] for s in sources if "similarity" in s]
    avg_similarity = round(sum(similarities) / len(similarities), 3) if similarities else None
    citation_rate = _citation_rate(answer_text, len(sources))

    with engine.connect() as conn:
        conn.execute(
            text("""
                INSERT INTO query_metrics
                    (question, category, routing_confidence, avg_retrieval_similarity,
                     num_sources, citation_rate, latency_seconds, logged_at)
                VALUES (:question, :category, :routing_confidence, :avg_similarity,
                        :num_sources, :citation_rate, :latency_seconds, :logged_at)
            """),
            {
                "question": question,
                "category": category,
                "routing_confidence": routing_confidence,
                "avg_similarity": avg_similarity,
                "num_sources": len(sources),
                "citation_rate": citation_rate,
                "latency_seconds": latency_seconds,
                "logged_at": datetime.utcnow(),
            },
        )
        conn.commit()

    logger.info(
        f"Logged metrics: confidence={routing_confidence:.2f}, "
        f"avg_similarity={avg_similarity}, citation_rate={citation_rate}, "
        f"latency={latency_seconds}"
    )


# Bump this manually whenever a system prompt's wording changes materially.
PROMPT_VERSION = "v1"


def log_prompt(question: str, category: str, system_prompt: str):
    """Call this from each agent right before invoking the LLM, to track prompt versions over time."""
    with engine.connect() as conn:
        conn.execute(
            text("""
                INSERT INTO prompt_logs (question, category, system_prompt, prompt_version, logged_at)
                VALUES (:question, :category, :system_prompt, :prompt_version, :logged_at)
            """),
            {
                "question": question,
                "category": category,
                "system_prompt": system_prompt,
                "prompt_version": PROMPT_VERSION,
                "logged_at": datetime.utcnow(),
            },
        )
        conn.commit()


def get_summary_stats():
    """Aggregate stats for the dashboard — averages across all logged queries."""
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT
                COUNT(*) as total_queries,
                AVG(routing_confidence) as avg_confidence,
                AVG(avg_retrieval_similarity) as avg_similarity,
                AVG(citation_rate) as avg_citation_rate,
                AVG(num_sources) as avg_num_sources,
                AVG(latency_seconds) as avg_latency
            FROM query_metrics
        """))
        row = result.fetchone()

    if not row or row[0] == 0:
        return None

    stats = {
        "total_queries": row[0],
        "avg_confidence": round(row[1], 3) if row[1] else None,
        "avg_similarity": round(row[2], 3) if row[2] else None,
        "avg_citation_rate": round(row[3], 3) if row[3] else None,
        "avg_num_sources": round(row[4], 1) if row[4] else None,
        "avg_latency": round(row[5], 2) if row[5] else None,
    }

    # Source coverage and data freshness come from news_embeddings, not query_metrics
    with engine.connect() as conn:
        coverage = conn.execute(text("SELECT COUNT(DISTINCT source) FROM news_embeddings")).scalar()
        freshness = conn.execute(text(
            "SELECT AVG(EXTRACT(EPOCH FROM (NOW() - published_at)) / 86400) FROM news_embeddings"
        )).scalar()

    stats["source_coverage"] = coverage or 0
    stats["avg_freshness_days"] = round(freshness, 1) if freshness else None

    return stats
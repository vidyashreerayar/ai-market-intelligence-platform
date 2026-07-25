# 🥔 Intersnack Market Intelligence Platform

<p align="center">

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-Live_App-red?logo=streamlit)
![LangChain](https://img.shields.io/badge/LangChain-Agentic_AI-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Neon-blue?logo=postgresql)
![Groq](https://img.shields.io/badge/Groq-Llama_3.3-orange)
![License](https://img.shields.io/badge/Status-Portfolio-success)

</p>

An AI-powered **Market Intelligence Platform** for the snack industry that combines **Agentic AI, Retrieval-Augmented Generation (RAG), PostgreSQL, and interactive analytics** to deliver business insights from industry news, competitor activity, consumer trends, and commodity prices.

🌐 **Live Demo:** https://intersnack-market-intel.streamlit.app

---

# 📸 Live Application

<p align="center">
<img src="assets/live_page.png" width="1000">
</p>

---

# ✨ Features

- 🤖 Multi-agent AI architecture
- 📰 Latest snack industry news summarisation
- 🏪 Competitor & brand intelligence
- 📈 Consumer trend analysis
- 🥔 Historical potato price analytics
- 📊 Interactive Plotly visualisations
- 🧠 LLM-powered business insights using **Groq Llama 3.3 70B**
- 🎯 Automatic query routing to specialised AI agents

---

# 🏗️ Architecture

```mermaid
flowchart LR

User --> Streamlit

Streamlit --> Supervisor

Supervisor --> NewsAgent
Supervisor --> MarketAgent
Supervisor --> TrendAgent
Supervisor --> PricingAgent

NewsAgent --> PostgreSQL
MarketAgent --> PostgreSQL
TrendAgent --> PostgreSQL
PricingAgent --> PostgreSQL

NewsAgent --> Groq
MarketAgent --> Groq
TrendAgent --> Groq
PricingAgent --> Groq

PricingAgent --> Plotly

Groq --> Streamlit
Plotly --> Streamlit
```

---

# 🛠 Tech Stack

| Category | Technologies |
|-----------|--------------|
| Frontend | Streamlit |
| AI | Groq Llama 3.3 70B, LangChain |
| Backend | Python, SQLAlchemy |
| Database | PostgreSQL (Neon) |
| Visualisation | Plotly |
| APIs | SerpAPI (Google News) |

---

# 📊 Data Sources

- 📰 Google News (via SerpAPI)
- 🗄 PostgreSQL / Neon
- 🥔 Historical Potato Price Dataset
- 🤖 Groq Llama 3.3 70B

---

# 📸 Application Demo

### Dashboard

Users interact with multiple specialised AI agents through a single conversational interface.

<p align="center">
<img src="assets/demo.png" width="1000">
</p>

---

### Pricing Intelligence

The Pricing Agent combines structured potato price data with LLM reasoning to generate business insights alongside interactive Plotly visualisations.

<p align="center">
<img src="assets/demo_01.png" width="1000">
</p>

---

# 💬 Example Questions

```text
What are the latest snack industry news?

Compare Lay's and Pringles.

What consumer trends are emerging?

Show historical potato prices.

Why have potato prices increased?

What opportunities exist in premium snacks?
```

---

# 🚀 Run Locally

```bash
git clone https://github.com/vidyashreerayar/intersnack-market-intelligence-demo.git

cd intersnack-market-intelligence-demo

pip install -r requirements.txt

streamlit run app.py
```

Create a `.env` file:

```env
GROQ_API_KEY=

SERPAPI_API_KEY=

DB_HOST=

DB_PORT=

DB_NAME=

DB_USER=

DB_PASSWORD=
```

---

# 👩‍💻 Author

**Vidyashree Rayar**

M.Sc. Artificial Intelligence  
BTU Cottbus–Senftenberg

---

⭐ If you found this project interesting, consider giving the repository a star.
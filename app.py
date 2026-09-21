# Load libraries and connect the Streamlit app to the AI supervisor and metrics
import pandas as pd
import plotly.express as px
import streamlit as st

from agents.supervisor import route_question
from etl.metrics import get_summary_stats

# Configure the Streamlit page layout, title, and Intersnack logo
st.set_page_config(
    page_title="Intersnack Market Intelligence Platform",
    page_icon="assets/intersnack_logo.png",
    layout="wide"
)

# --------------------- Styling --------------------- #
# Define the visual style of the dashboard
st.markdown("""
<style>

.block-container{
    padding-top:6rem;
    padding-left:4rem;
    padding-right:4rem;
    max-width:1450px;
}

[data-testid="stAppViewContainer"]{
    background:#ffffff;
}

h1,h2,h3,p,li,label{
    color:#222222;
}

.main-title{
    font-size:42px;
    font-weight:700;
    color:#222222;
    margin-bottom:0;
}

.subtitle{
    color:#666666;
    font-size:18px;
    margin-top:4px;
}

.section-title{
    color:#C62828;
    font-weight:700;
    font-size:24px;
    margin-bottom:15px;
}

.stButton>button{
    background:#C62828;
    color:white;
    border:none;
    border-radius:6px;
    padding:10px 28px;
    font-weight:600;
}

.stButton>button:hover{
    background:#B71C1C;
    color:white;
}

div[data-testid="stTextInput"] input{
    border-radius:8px;
}

</style>
""", unsafe_allow_html=True)

# --------------------- Header --------------------- #
# Display the Intersnack logo, platform title, and description
logo_col, title_col = st.columns([1,5])

with logo_col:
    st.image("assets/intersnack_logo.png", width=150)

with title_col:

    st.markdown(
        "<div class='main-title'>Market Intelligence Platform</div>",
        unsafe_allow_html=True,
    )

    st.markdown(
        "<div class='subtitle'>AI-powered market, competitor, trend and pricing intelligence for Intersnack.</div>",
        unsafe_allow_html=True,
    )

st.divider()

# --------------------- Tabs --------------------- #
# Create the two main sections of the dashboard
tab1, tab2 = st.tabs(["AI Assistant", "Prove Impact"])

# ==================== TAB 1: AI Assistant ==================== #
# Display the AI question-answering interface
with tab1:
    # Split the assistant tab into an example-question area and answer area
    left, right = st.columns([1,2], gap="large")

    # --------------------- Left --------------------- #

    with left:
        # Display example business questions users can ask
        st.markdown(
        "<div class='section-title'>Example Questions</div>",
        unsafe_allow_html=True,
    )

    st.markdown("""
**📰 News**
- Summarize the latest snack industry news.
- What are the latest news articles related to the snack industry?

**🏢 Competitor Intelligence**
- Which competitors are mentioned most frequently in recent news?
- What recent product launches have competitors announced?
- What market opportunities for Intersnack are highlighted in recent news?
- What business risks to Intersnack are mentioned in recent news?

**📈 Market Trends**
- What are the key trends in the snack industry?
- What emerging consumer trends are mentioned in recent news?
- Which industry trends could impact Intersnack?

**💰 Raw Material Pricing**
- How have potato prices changed from 2000 to 2024?
- Which year recorded the highest potato price?
- Which year recorded the lowest potato price?
- How could potato price fluctuations affect Intersnack's manufacturing costs?
""")

    # --------------------- Right --------------------- #

    with right:
        # Display the question input area
        st.markdown(
            "<div class='section-title'>Ask the AI Assistant</div>",
            unsafe_allow_html=True,
        )
        # Capture the user's business question
        question = st.text_input(
        "Question",
        placeholder="Ask about competitors, market trends, news or potato prices...",
        label_visibility="collapsed"
        )
        # Create the button that starts the analysis
        ask = st.button("Analyze")
        # Process the question when the user clicks Analyze
        if ask and question:
            # Show a loading message while the supervisor processes the question
            with st.spinner("Analyzing..."):
                answer = route_question(question)

            st.markdown("---")
            # Display the AI-generated answer
            st.subheader("Answer")
            st.write(answer["text"])

            # ---------------- Sources ---------------- #
            # Display the supporting sources returned by the selected agent
            if answer.get("sources"):
                with st.expander(f"📚 Sources ({len(answer['sources'])})"):
                    for s in answer["sources"]:
                        st.markdown(
                            f"**[{s['label']}]** [{s['title']}]({s['url']})  \n"
                            f"*{s['source']} · relevance: {s['similarity']:.0%}*"
                        )
            # Display a chart when the selected agent returns chart data
            if answer["chart_data"]:

                st.markdown("---")
                st.subheader(answer["chart_title"])
                # Convert the returned chart data into a DataFrame
                df = pd.DataFrame(answer["chart_data"])

                # ---------------- Line Chart ---------------- #
                # Create a line chart for time-series data such as potato prices
                if answer["chart_type"] == "line":
                    # Check that the required year and price columns are available
                    if {"year", "price_eur_per_100kg"}.issubset(df.columns):
                        # Convert chart columns to numeric values
                        df["year"] = pd.to_numeric(df["year"])
                        df["price_eur_per_100kg"] = pd.to_numeric(df["price_eur_per_100kg"])
                        # Sort the data chronologically
                        df = df.sort_values("year")
                        # Create the historical potato-price line chart
                        fig = px.line(
                            df,
                            x="year",
                            y="price_eur_per_100kg",
                            markers=True,
                            title="Historical Potato Prices (2000–2024)"
                        )
                        # Format the chart line, markers, and hover information
                        fig.update_traces(
                            line=dict(
                                color="#C62828",
                                width=4
                            ),
                            marker=dict(
                                color="#C62828",
                                size=9,
                                line=dict(
                                    color="white",
                                    width=2
                                )
                            ),
                            hovertemplate="<b>Year:</b> %{x}<br><b>Price:</b> €%{y:.2f}<extra></extra>"
                        )
                         # Configure the chart layout and axes
                        fig.update_layout(
                            template="simple_white",
                            height=500,
                            hovermode="x unified",
                            title=dict(
                                x=0.5,
                                font=dict(size=24)
                            ),
                            margin=dict(l=20,r=20,t=70,b=20),
                            xaxis=dict(
                                title="Year",
                                tickmode="linear",
                                dtick=2,
                                showgrid=True,
                                gridcolor="#E8E8E8",
                                zeroline=False
                            ),
                            yaxis=dict(
                                title="Price (€ per 100 kg)",
                                showgrid=True,
                                gridcolor="#E8E8E8",
                                zeroline=False
                            )
                        )

                        # Display the potato-price chart
                        st.plotly_chart(fig, width="stretch")

                        c1, c2, c3 = st.columns(3)

                        with c1:
                            st.metric(
                                "Latest Price",
                                f"€{df.iloc[-1]['price_eur_per_100kg']:.2f}"
                            )

                        with c2:
                            st.metric(
                                "Highest Price",
                                f"€{df['price_eur_per_100kg'].max():.2f}"
                            )

                        with c3:
                            st.metric(
                                "Lowest Price",
                                f"€{df['price_eur_per_100kg'].min():.2f}"
                            )

                # ---------------- Bar Chart ---------------- #
                # Create a bar chart when competitor mention data is returned
                elif answer["chart_type"] == "bar":
                    # Check that competitor and mention-count columns are available
                    if {"competitor", "mentions"}.issubset(df.columns):
                        # Sort competitors from most to least mentions
                        df = df.sort_values(
                            "mentions",
                            ascending=False
                        )
                        # Create the competitor-mentions bar chart
                        fig = px.bar(
                            df,
                            x="competitor",
                            y="mentions",
                            text="mentions",
                            title="Competitor Mentions in Recent News",
                            color="mentions",
                            color_continuous_scale=["#F9D5D3", "#C62828"]
                        )
                        # Display mention counts and configure hover information
                        fig.update_traces(
                            textposition="outside",
                            hovertemplate="<b>%{x}</b><br>Mentions: %{y}<extra></extra>"
                        )
                        # Configure the bar-chart layout and axes
                        fig.update_layout(
                            template="simple_white",
                            height=500,
                            title=dict(
                                x=0.5,
                                font=dict(size=24)
                            ),
                            margin=dict(l=20,r=20,t=70,b=20),
                            xaxis_title="Competitor",
                            yaxis_title="Mentions",
                            coloraxis_showscale=False,
                            xaxis=dict(
                                showgrid=False
                            ),
                            yaxis=dict(
                                gridcolor="#E8E8E8"
                            )
                        )
                        # Display the competitor-mentions chart
                        st.plotly_chart(fig, width="stretch")

                        

# ==================== TAB 2: Prove Impact ==================== #
# Display the system performance and business-impact metrics
with tab2:
    # Display the Prove Impact section title
    st.markdown(
        "<div class='section-title'>Prove Impact — Before vs After</div>",
        unsafe_allow_html=True,
    )
    # Get aggregated performance metrics from metrics.py
    stats = get_summary_stats()
    # Show a message if no queries have been logged yet
    if not stats:
        st.info("No queries logged yet — ask a few questions in the AI Assistant tab first.")
    else:
        # Build a table comparing the manual process with the AI system
        before_after = pd.DataFrame([
            {"Metric": "Report cycle time", "Before (manual)": "5–10 days", "After (AI)": f"{stats['avg_latency']}s" if stats['avg_latency'] else "Seconds"},
            {"Metric": "Analyst time on reporting", "Before (manual)": "20–30%", "After (AI)": "Query-driven, on-demand"},
            {"Metric": "Routing confidence (avg)", "Before (manual)": "N/A", "After (AI)": f"{stats['avg_confidence']:.0%}" if stats['avg_confidence'] else "N/A"},
            {"Metric": "Retrieval relevance (avg)", "Before (manual)": "N/A", "After (AI)": f"{stats['avg_similarity']:.0%}" if stats['avg_similarity'] else "N/A"},
            {"Metric": "Citation rate (avg)", "Before (manual)": "N/A", "After (AI)": f"{stats['avg_citation_rate']:.0%}" if stats['avg_citation_rate'] else "N/A"},
            {"Metric": "Source coverage", "Before (manual)": "N/A", "After (AI)": f"{stats['source_coverage']} publishers"},
            {"Metric": "Data freshness (avg)", "Before (manual)": "N/A", "After (AI)": f"{stats['avg_freshness_days']} days old" if stats['avg_freshness_days'] else "N/A"},
        ])
        # Display the before-and-after comparison table
        st.table(before_after)
        # Create four columns for key performance metrics
        c1, c2, c3, c4 = st.columns(4)
        # Show the total number of queries answered
        with c1:
            st.metric("Total queries answered", stats["total_queries"])
        # Show the average number of sources used per answer
        with c2:
            st.metric("Avg sources per answer", stats["avg_num_sources"])
        # Show the average response time
        with c3:
            st.metric("Avg response time", f"{stats['avg_latency']}s" if stats['avg_latency'] else "N/A")
        # Show the number of publishers represented in the indexed news
        with c4:
            st.metric("Source coverage", f"{stats['source_coverage']} publishers")
        # Explain the source and limitations of the displayed metrics
        st.caption(
            "Before-state figures are estimates from public benchmarks (see README research insights). "
            "After-state figures are live, computed from actual system usage. "
            "System uptime is not tracked in this demo (no production deployment to monitor)."
        )
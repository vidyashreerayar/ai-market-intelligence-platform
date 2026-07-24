import pandas as pd
import plotly.express as px
import streamlit as st

from agents.supervisor import route_question

st.set_page_config(
    page_title="Intersnack Market Intelligence Platform",
    page_icon="assets/intersnack_logo.png",
    layout="wide"
)

# --------------------- Styling --------------------- #

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

# --------------------- Layout --------------------- #

left, right = st.columns([1,2], gap="large")

# --------------------- Left --------------------- #

with left:

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

    st.markdown(
        "<div class='section-title'>Ask the AI Assistant</div>",
        unsafe_allow_html=True,
    )

    question = st.text_input(
    "Question",
    placeholder="Ask about competitors, market trends, news or potato prices...",
    label_visibility="collapsed"
    )
    ask = st.button("Analyze")

    if ask and question:

        with st.spinner("Analyzing..."):
            answer = route_question(question)

        st.markdown("---")

        st.subheader("Answer")
        st.write(answer["text"])

        if answer["chart_data"]:

            st.markdown("---")
            st.subheader(answer["chart_title"])

            df = pd.DataFrame(answer["chart_data"])

            # ---------------- Line Chart ---------------- #

            if answer["chart_type"] == "line":

                if {"year", "price_eur_per_100kg"}.issubset(df.columns):

                    df["year"] = pd.to_numeric(df["year"])
                    df["price_eur_per_100kg"] = pd.to_numeric(df["price_eur_per_100kg"])

                    df = df.sort_values("year")

                    fig = px.line(
                        df,
                        x="year",
                        y="price_eur_per_100kg",
                        markers=True,
                        title="Historical Potato Prices (2000–2024)"
                    )

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

                    #st.plotly_chart(fig, use_container_width=True)
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

            elif answer["chart_type"] == "bar":

                if {"competitor", "mentions"}.issubset(df.columns):

                    df = df.sort_values(
                        "mentions",
                        ascending=False
                    )

                    fig = px.bar(
                        df,
                        x="competitor",
                        y="mentions",
                        text="mentions",
                        title="Competitor Mentions in Recent News",
                        color="mentions",
                        color_continuous_scale=["#F9D5D3", "#C62828"]
                    )

                    fig.update_traces(
                        textposition="outside",
                        hovertemplate="<b>%{x}</b><br>Mentions: %{y}<extra></extra>"
                    )

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

                    st.plotly_chart(fig, width="stretch")

                    #st.plotly_chart(fig, use_container_width=True)
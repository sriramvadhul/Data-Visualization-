import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Clinical Analytics Dashboard",
    page_icon="🏥",
    layout="wide"
)

# ---------------- LOAD DATA ----------------
FILE_PATH = "data/medical_data.csv"
df = pd.read_csv(FILE_PATH)

# ---------------- SIDEBAR STYLE ----------------
st.markdown("""
<style>
[data-testid="stSidebar"] {
    background-color: #0B1F3B;
}
[data-testid="stSidebar"] * {
    color: white;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR MENU ----------------
with st.sidebar:
    st.markdown("## 🏥 Clinical Dashboard")

    selected = option_menu(
        menu_title=None,
        options=[
            "Overview",
            "Demographics",
            "Vitals",
            "Labs",
            "Risk Factors",
            "Trends"
        ],
        icons=[
            "house",
            "people",
            "heart-pulse",
            "flask",
            "shield-exclamation",
            "graph-up"
        ],
        default_index=0,
        styles={
            "container": {"background-color": "#0B1F3B"},
            "icon": {"color": "#5DA9E9", "font-size": "20px"},
            "nav-link": {"font-size": "16px"},
            "nav-link-selected": {
                "background-color": "#1F3B73"
            }
        }
    )

# ---------------- OVERVIEW ----------------
if selected == "Overview":
    st.markdown("## 🏥 Clinical Data Analytics & Visualization Dashboard")

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Total Patients", f"{len(df):,}")
    k2.metric("Average Age", f"{df.age.mean():.1f}")
    k3.metric("Avg Oxygen Saturation", f"{df.oxygen_saturation.mean():.1f}%")
    k4.metric("Avg CRP Level", f"{df.crp.mean():.1f}")

    st.markdown("---")

    fig = px.pie(
        df,
        names="diagnosis",
        title="Diagnosis Distribution",
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    st.plotly_chart(fig, use_container_width=True)

# ---------------- DEMOGRAPHICS ----------------
elif selected == "Demographics":
    st.markdown("## 👥 Patient Demographics")

    col1, col2 = st.columns(2)

    with col1:
        fig = px.histogram(
            df,
            x="age",
            nbins=30,
            title="Age Distribution",
            color_discrete_sequence=["#5DA9E9"]
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.bar(
            df,
            x="gender",
            title="Gender Distribution",
            color="gender",
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        st.plotly_chart(fig, use_container_width=True)

# ---------------- VITALS ----------------
elif selected == "Vitals":
    st.markdown("## ❤️ Vitals Analysis")

    vitals = [
        "temperature",
        "heart_rate",
        "respiratory_rate",
        "oxygen_saturation"
    ]

    for v in vitals:
        fig = px.box(
            df,
            x="diagnosis",
            y=v,
            title=f"{v.replace('_',' ').title()} by Diagnosis",
            color="diagnosis",
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        st.plotly_chart(fig, use_container_width=True)

# ---------------- LABS ----------------
elif selected == "Labs":
    st.markdown("## 🧪 Laboratory Indicators")

    fig1 = px.scatter(
        df,
        x="wbc",
        y="crp",
        color="diagnosis",
        opacity=0.7,
        title="WBC vs CRP (Inflammation Markers)",
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    st.plotly_chart(fig1, use_container_width=True)

    fig2 = px.bar(
        df.groupby("diagnosis")[["wbc", "crp"]].mean().reset_index(),
        x="diagnosis",
        y=["wbc", "crp"],
        barmode="group",
        title="Average Lab Values by Diagnosis",
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    st.plotly_chart(fig2, use_container_width=True)

# ---------------- RISK FACTORS ----------------
elif selected == "Risk Factors":
    st.markdown("## ⚠️ Risk Factors")

    risk_cols = ["diabetes", "hypertension", "asthma", "smoker"]
    risk_data = df[risk_cols].mean().reset_index()
    risk_data.columns = ["Risk Factor", "Prevalence"]

    fig = px.bar(
        risk_data,
        x="Risk Factor",
        y="Prevalence",
        title="Prevalence of Clinical Risk Factors",
        color="Risk Factor",
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    st.plotly_chart(fig, use_container_width=True)

# ---------------- TRENDS ----------------
elif selected == "Trends":
    st.markdown("## 📈 Clinical Trends")

    fig = px.line(
        df.sort_values("age"),
        x="age",
        y="oxygen_saturation",
        title="Oxygen Saturation Trend Across Age",
        color_discrete_sequence=["#5DA9E9"]
    )
    st.plotly_chart(fig, use_container_width=True)

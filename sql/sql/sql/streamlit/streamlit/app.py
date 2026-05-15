import streamlit as st
import pandas as pd
import plotly.express as px
from snowflake.snowpark.context import get_active_session

st.set_page_config(page_title="LinkedIn Jobs", page_icon="💼", layout="wide")
session = get_active_session()

@st.cache_data(ttl=600)
def run_query(query):
    return session.sql(query).to_pandas()

st.title("💼 Analyse des Offres d'Emploi LinkedIn")
st.markdown("**ESME — Architecture Big Data 2026**")
st.divider()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Offres d'emploi", f"{run_query('SELECT COUNT(*) AS N FROM linkedin.public.job_postings')['N'][0]:,}")
col2.metric("Entreprises", f"{run_query('SELECT COUNT(DISTINCT name) AS N FROM linkedin.public.companies')['N'][0]:,}")
col3.metric("Secteurs", f"{run_query('SELECT COUNT(DISTINCT industry) AS N FROM linkedin.public.company_industries')['N'][0]:,}")
sal = run_query("SELECT ROUND(AVG(max_salary),0) AS N FROM linkedin.public.job_postings WHERE max_salary IS NOT NULL AND pay_period='YEARLY'")
col4.metric("Salaire max moyen", f"${int(sal['N'][0]):,}")

st.divider()

st.header("1️⃣ Top 10 titres les plus publiés par industrie")
df1 = run_query("""
SELECT ji.industry_id AS INDUSTRY, jp.title AS JOB_TITLE, COUNT(*) AS NB_POSTINGS
FROM linkedin.public.job_postings jp
JOIN linkedin.public.job_industries ji ON jp.job_id = ji.job_id
WHERE jp.title IS NOT NULL
GROUP BY ji.industry_id, jp.title
QUALIFY ROW_NUMBER() OVER (PARTITION BY ji.industry_id ORDER BY COUNT(*) DESC) <= 10
ORDER BY INDUSTRY, NB_POSTINGS DESC
""")
if len(df1) > 0:
    ind1 = st.selectbox("Sélectionner une industrie", sorted(df1["INDUSTRY"].unique()), key="s1")
    df1f = df1[df1["INDUSTRY"] == ind1]
    fig1 = px.bar(df1f.sort_values("NB_POSTINGS"), x="NB_POSTINGS", y="JOB_TITLE",
        orientation="h", color="NB_POSTINGS", color_continuous_scale="Blues",
        text="NB_POSTINGS", title=f"Top 10 titres — {ind1}",
        labels={"NB_POSTINGS": "Nombre d'offres", "JOB_TITLE": "Titre"})
    fig1.update_layout(height=450, coloraxis_showscale=False)
    st.plotly_chart(fig1, use_container_width=True)

st.divider()

st.header("2️⃣ Top 10 postes les mieux rémunérés par industrie")
df2 = run_query("""
SELECT ji.industry_id AS INDUSTRY, jp.title AS JOB_TITLE,
    ROUND(AVG(jp.max_salary),0) AS AVG_MAX_SALARY
FROM linkedin.public.job_postings jp
JOIN linkedin.public.job_industries ji ON jp.job_id = ji.job_id
WHERE jp.max_salary IS NOT NULL AND jp.pay_period = 'YEARLY'
GROUP BY ji.industry_id, jp.title
QUALIFY ROW_NUMBER() OVER (PARTITION BY ji.industry_id ORDER BY AVG(jp.max_salary) DESC) <= 10
ORDER BY INDUSTRY, AVG_MAX_SALARY DESC
""")
if len(df2) > 0:
    ind2 = st.selectbox("Sélectionner une industrie", sorted(df2["INDUSTRY"].unique()), key="s2")
    df2f = df2[df2["INDUSTRY"] == ind2]
    fig2 = px.bar(df2f.sort_values("AVG_MAX_SALARY"), x="AVG_MAX_SALARY", y="JOB_TITLE",
        orientation="h", color="AVG_MAX_SALARY", color_continuous_scale="Greens",
        text="AVG_MAX_SALARY", title=f"Top 10 salaires — {ind2}",
        labels={"AVG_MAX_SALARY": "Salaire max moyen ($/an)", "JOB_TITLE": "Titre"})
    fig2.update_layout(height=450, coloraxis_showscale=False)
    st.plotly_chart(fig2, use_container_width=True)

st.divider()

st.header("3️⃣ Répartition par taille d'entreprise")
df3 = run_query("""
SELECT
    CASE c.company_size
        WHEN 0 THEN '0 - Tres petite'
        WHEN 1 THEN '1 - Petite'
        WHEN 2 THEN '2 - Petite-moyenne'
        WHEN 3 THEN '3 - Moyenne'
        WHEN 4 THEN '4 - Moyenne-grande'
        WHEN 5 THEN '5 - Grande'
        WHEN 6 THEN '6 - Tres grande'
        WHEN 7 THEN '7 - Entreprise'
        ELSE 'Non renseigne'
    END AS COMPANY_SIZE_LABEL,
    COUNT(jp.job_id) AS NB_OFFRES
FROM linkedin.public.job_postings jp
LEFT JOIN linkedin.public.companies c ON jp.company_name = c.name
GROUP BY c.company_size, COMPANY_SIZE_LABEL
ORDER BY NB_OFFRES DESC
""")
col_a, col_b = st.columns(2)
with col_a:
    fig3a = px.pie(df3, names="COMPANY_SIZE_LABEL", values="NB_OFFRES",
        title="Camembert", hole=0.4,
        color_discrete_sequence=px.colors.sequential.Teal)
    st.plotly_chart(fig3a, use_container_width=True)
with col_b:
    fig3b = px.bar(df3, x="COMPANY_SIZE_LABEL", y="NB_OFFRES",
        color="NB_OFFRES", color_continuous_scale="Teal", text="NB_OFFRES",
        title="Barres", labels={"COMPANY_SIZE_LABEL": "Taille", "NB_OFFRES": "Offres"})
    fig3b.update_layout(coloraxis_showscale=False, xaxis_tickangle=-30)
    st.plotly_chart(fig3b, use_container_width=True)

st.divider()

st.header("4️⃣ Répartition par secteur d'activité (Top 20)")
df4 = run_query("""
SELECT ji.industry_id AS INDUSTRY, COUNT(DISTINCT jp.job_id) AS NB_OFFRES
FROM linkedin.public.job_postings jp
JOIN linkedin.public.job_industries ji ON jp.job_id = ji.job_id
GROUP BY ji.industry_id
ORDER BY NB_OFFRES DESC
LIMIT 20
""")
fig4 = px.bar(df4.sort_values("NB_OFFRES"), x="NB_OFFRES", y="INDUSTRY",
    orientation="h", color="NB_OFFRES", color_continuous_scale="Purples",
    text="NB_OFFRES", title="Top 20 secteurs",
    labels={"NB_OFFRES": "Nombre d'offres", "INDUSTRY": "Secteur"})
fig4.update_layout(height=600, coloraxis_showscale=False)
st.plotly_chart(fig4, use_container_width=True)

st.divider()

st.header("5️⃣ Répartition par type d'emploi")
df5 = run_query("""
SELECT COALESCE(formatted_work_type, 'Non renseigne') AS WORK_TYPE,
    COUNT(*) AS NB_OFFRES,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS POURCENTAGE
FROM linkedin.public.job_postings
GROUP BY formatted_work_type
ORDER BY NB_OFFRES DESC
""")
col_c, col_d = st.columns(2)
with col_c:
    fig5 = px.pie(df5, names="WORK_TYPE", values="NB_OFFRES",
        title="Répartition par type d'emploi", hole=0.35,
        color_discrete_sequence=px.colors.qualitative.Set2)
    st.plotly_chart(fig5, use_container_width=True)
with col_d:
    st.dataframe(df5.rename(columns={"WORK_TYPE": "Type", "NB_OFFRES": "Nb offres", "POURCENTAGE": "%"}).reset_index(drop=True))

st.divider()
st.markdown("<div style='text-align:center;color:gray;'>ESME — Big Data 2026</div>", unsafe_allow_html=True)

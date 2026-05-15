# 🧊 Analyse des Offres d'Emploi LinkedIn avec Snowflake

**ESME — Evaluation Architecture Big Data 2026**  
**Binôme** : Joshua Maarek & Harold Malherbe  
**Soumission** : axel@logbrain.fr | Objet : ESME_EVALUATION_ARCHITECTURE_BIGDATA_2026

---

## 📁 Structure du projet
ESME_EVALUATION_ARCHITECTURE_BIGDATA_2026/
├── README.md
├── sql/
│   ├── 01_setup.sql
│   ├── 02_create_tables.sql
│   ├── 03_load_data.sql
│   └── 04_analyses.sql
└── streamlit/
└── app.py
---

## 🎯 Objectif

Ce projet analyse plusieurs milliers d'offres d'emploi LinkedIn en utilisant **Snowflake** comme base de données cloud et **Streamlit** pour les visualisations. Les données sont chargées depuis un bucket S3 public.

---

## 📊 Dataset

| Fichier | Format | Lignes |
|---|---|---|
| job_postings.csv | CSV | 13 546 |
| benefits.csv | CSV | 13 761 |
| companies.json | JSON | 6 063 |
| employee_counts.csv | CSV | 15 907 |
| job_skills.csv | CSV | 27 899 |
| job_industries.json | JSON | 21 993 |
| company_industries.json | JSON | 31 760 |
| company_specialities.json | JSON | 128 355 |

---

## 🔧 Étapes d'exécution

### Étape 1 — Création de la base et du stage

On crée la base linkedin, un stage externe pointant vers S3, et deux formats de fichiers csv_format et json_format.

### Étape 2 — Création des tables

8 tables créées. Ajustements : zip_code en VARCHAR(200) et speciality en TEXT car certaines valeurs dépassaient la taille initiale.

### Étape 3 — Chargement des données

CSV via COPY INTO direct. JSON via table temporaire VARIANT puis INSERT INTO avec parsing des champs.

---

## 📊 Analyses réalisées

### Analyse 1 — Top 10 titres les plus publiés par industrie
Jointure job_postings et job_industries. QUALIFY ROW_NUMBER() pour garder le top 10 par industrie.

### Analyse 2 — Top 10 postes les mieux rémunérés
Même jointure, filtrage pay_period = YEARLY, moyenne de max_salary.

### Analyse 3 — Répartition par taille d'entreprise
Jointure avec companies via company_name. Mapping company_size 0-7 vers libellés lisibles.

### Analyse 4 — Répartition par secteur d'activité
Top 20 secteurs via job_industries.industry_id.

### Analyse 5 — Répartition par type d'emploi
82.57% Full-time, 8.84% Contract, 6.81% Part-time.

---

## ⚠️ Problèmes rencontrés et solutions

| Problème | Solution |
|---|---|
| zip_code trop courte | ALTER TABLE MODIFY COLUMN zip_code VARCHAR(200) |
| speciality trop courte | ALTER TABLE MODIFY COLUMN speciality TEXT |
| job_industries vide | Rechargement via table VARIANT temporaire |
| plotly absent dans Snowflake | Ajout via bouton Packages de l'éditeur Streamlit |
| Streamlit version incompatible | Passage en mode Run on warehouse legacy |
| industry_id numerique ne matche pas industry texte | Utilisation de industry_id directement comme label |
| Harold sans accès à la base | GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA linkedin.public TO ROLE ACCOUNTADMIN |

---

## 🚀 Déploiement Streamlit

1. Snowflake > Projects > Streamlit > + Streamlit App
2. App location : LINKEDIN / PUBLIC
3. Mode : Run on warehouse legacy
4. Coller le contenu de streamlit/app.py
5. Ajouter plotly via le bouton Packages
6. Cliquer Run

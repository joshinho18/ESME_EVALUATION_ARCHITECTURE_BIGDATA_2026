USE DATABASE linkedin;
USE SCHEMA public;

-- Analyse 1 : Top 10 titres les plus publiés par industrie
SELECT ji.industry_id AS INDUSTRY, jp.title AS JOB_TITLE, COUNT(*) AS NB_POSTINGS
FROM job_postings jp
JOIN job_industries ji ON jp.job_id = ji.job_id
WHERE jp.title IS NOT NULL
GROUP BY ji.industry_id, jp.title
QUALIFY ROW_NUMBER() OVER (PARTITION BY ji.industry_id ORDER BY COUNT(*) DESC) <= 10
ORDER BY INDUSTRY, NB_POSTINGS DESC;

-- Analyse 2 : Top 10 postes les mieux rémunérés par industrie
SELECT ji.industry_id AS INDUSTRY, jp.title AS JOB_TITLE,
    ROUND(AVG(jp.max_salary),0) AS AVG_MAX_SALARY
FROM job_postings jp
JOIN job_industries ji ON jp.job_id = ji.job_id
WHERE jp.max_salary IS NOT NULL AND jp.pay_period = 'YEARLY'
GROUP BY ji.industry_id, jp.title
QUALIFY ROW_NUMBER() OVER (PARTITION BY ji.industry_id ORDER BY AVG(jp.max_salary) DESC) <= 10
ORDER BY INDUSTRY, AVG_MAX_SALARY DESC;

-- Analyse 3 : Répartition par taille d'entreprise
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
FROM job_postings jp
LEFT JOIN companies c ON jp.company_name = c.name
GROUP BY c.company_size, COMPANY_SIZE_LABEL
ORDER BY NB_OFFRES DESC;

-- Analyse 4 : Répartition par secteur d'activité
SELECT ji.industry_id AS INDUSTRY, COUNT(DISTINCT jp.job_id) AS NB_OFFRES
FROM job_postings jp
JOIN job_industries ji ON jp.job_id = ji.job_id
GROUP BY ji.industry_id
ORDER BY NB_OFFRES DESC
LIMIT 20;

-- Analyse 5 : Répartition par type d'emploi
SELECT COALESCE(formatted_work_type, 'Non renseigne') AS WORK_TYPE,
    COUNT(*) AS NB_OFFRES,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS POURCENTAGE
FROM job_postings
GROUP BY formatted_work_type
ORDER BY NB_OFFRES DESC;

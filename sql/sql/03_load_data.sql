USE DATABASE linkedin;
USE SCHEMA public;

COPY INTO job_postings
FROM @linkedin_stage/job_postings.csv
FILE_FORMAT = (FORMAT_NAME = 'csv_format')
ON_ERROR = 'CONTINUE';

COPY INTO benefits
FROM @linkedin_stage/benefits.csv
FILE_FORMAT = (FORMAT_NAME = 'csv_format')
ON_ERROR = 'CONTINUE';

COPY INTO employee_counts
FROM @linkedin_stage/employee_counts.csv
FILE_FORMAT = (FORMAT_NAME = 'csv_format')
ON_ERROR = 'CONTINUE';

COPY INTO job_skills
FROM @linkedin_stage/job_skills.csv
FILE_FORMAT = (FORMAT_NAME = 'csv_format')
ON_ERROR = 'CONTINUE';

CREATE OR REPLACE TEMP TABLE companies_raw (v VARIANT);
COPY INTO companies_raw
FROM @linkedin_stage/companies.json
FILE_FORMAT = (FORMAT_NAME = 'json_format');

INSERT INTO companies
SELECT
    v:company_id::VARCHAR, v:name::VARCHAR, v:description::VARCHAR,
    v:company_size::INTEGER, v:state::VARCHAR, v:country::VARCHAR,
    v:city::VARCHAR, v:zip_code::VARCHAR(200), v:address::VARCHAR, v:url::VARCHAR
FROM companies_raw;

CREATE OR REPLACE TEMP TABLE company_industries_raw (v VARIANT);
COPY INTO company_industries_raw
FROM @linkedin_stage/company_industries.json
FILE_FORMAT = (FORMAT_NAME = 'json_format');

INSERT INTO company_industries
SELECT v:company_id::VARCHAR, v:industry::VARCHAR
FROM company_industries_raw;

CREATE OR REPLACE TEMP TABLE company_specialities_raw (v VARIANT);
COPY INTO company_specialities_raw
FROM @linkedin_stage/company_specialities.json
FILE_FORMAT = (FORMAT_NAME = 'json_format');

ALTER TABLE company_specialities MODIFY COLUMN speciality TEXT;
INSERT INTO company_specialities
SELECT v:company_id::VARCHAR, v:speciality::VARCHAR
FROM company_specialities_raw;

CREATE OR REPLACE TEMP TABLE job_industries_raw (v VARIANT);
COPY INTO job_industries_raw
FROM @linkedin_stage/job_industries.json
FILE_FORMAT = (FORMAT_NAME = 'json_format');

INSERT INTO job_industries
SELECT v:job_id::VARCHAR, v:industry_id::VARCHAR
FROM job_industries_raw;

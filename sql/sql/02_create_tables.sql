USE DATABASE linkedin;
USE SCHEMA public;

CREATE OR REPLACE TABLE job_postings (
    job_id                    VARCHAR(50),
    company_name              VARCHAR(255),
    title                     VARCHAR(500),
    description               TEXT,
    max_salary                FLOAT,
    med_salary                FLOAT,
    min_salary                FLOAT,
    pay_period                VARCHAR(50),
    formatted_work_type       VARCHAR(100),
    location                  VARCHAR(255),
    applies                   INTEGER,
    original_listed_time      BIGINT,
    remote_allowed            BOOLEAN,
    views                     INTEGER,
    job_posting_url           VARCHAR(1000),
    application_url           VARCHAR(1000),
    application_type          VARCHAR(100),
    expiry                    BIGINT,
    closed_time               BIGINT,
    formatted_experience_level VARCHAR(100),
    skills_desc               TEXT,
    listed_time

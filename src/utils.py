import psycopg2

def create_database(database_name: str, params: dict):
    """Создание базы данных и таблиц для сохранения данных об организациях и вакансиях"""
    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"DROP DATABASE  IF EXISTS {database_name}")
    cur.execute(f"CREATE DATABASE  {database_name}")

    conn.close()

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        cur.execute("""
        CREATE TABLE employers (
            employer_id VARCHAR(20) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            number_of_vacancy INTEGER,
            url VARCHAR(255)
            )
        """)

    with conn.cursor() as cur:
        cur.execute("""
        CREATE TABLE vacancies (
            vacancy_id VARCHAR(20) PRIMARY KEY,
            employer_id VARCHAR(20) REFERENCES employers(employer_id),
            title VARCHAR(255) NOT NULL,
            description TEXT,
            salary_from INTEGER,
            salary_to INTEGER,
            currency VARCHAR(20),
            url VARCHAR(255)
            )
        """)

    conn.commit()
    conn.close()

from typing import Any

import psycopg2

from src.hh_api import HeadHunterAPI


def create_database(database_name: str, params: dict) -> None:
    """Создание базы данных и таблиц для сохранения данных об организациях и вакансиях"""
    admin_params = params.copy()
    admin_params["database"] = "postgres"

    conn = psycopg2.connect(**admin_params)
    conn.autocommit = True

    with conn.cursor() as cur:
        cur.execute(f"DROP DATABASE IF EXISTS {database_name}")
        cur.execute(f"CREATE DATABASE {database_name}")

    conn.close()

    conn = psycopg2.connect(**params)

    with conn.cursor() as cur:
        cur.execute(
            """
        CREATE TABLE employers (
            employer_id VARCHAR(20) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            url VARCHAR(255)
            )
        """
        )

    with conn.cursor() as cur:
        cur.execute(
            """
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
        """
        )

    conn.commit()
    conn.close()


def save_data_to_database(employers: list[dict[str, Any]], database_name: str, params: dict) -> None:
    """Сохранение данных о компаниях и вакансиях в базу данных"""
    conn = psycopg2.connect(**params)

    with conn.cursor() as cur:
        for employer in employers:
            cur.execute(
                """
                INSERT INTO employers (employer_id, name, url)
                VALUES (%s, %s, %s)
                ON CONFLICT (employer_id) DO NOTHING
                """,
                (employer["id"], employer["name"], employer["alternate_url"]),
            )

            api = HeadHunterAPI()
            vacancies_data = api.get_vacancies(employer["id"])
            for vacancy in vacancies_data:
                salary = vacancy.get("salary") or {}
                cur.execute(
                    """
                    INSERT INTO vacancies (
                        vacancy_id, employer_id, title, description,
                        salary_from, salary_to, currency, url
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (vacancy_id) DO NOTHING
                """,
                    (
                        vacancy["id"],
                        employer["id"],
                        vacancy.get("name", ""),
                        vacancy.get("snippet", {}).get("requirement", ""),
                        salary.get("from"),
                        salary.get("to"),
                        salary.get("currency"),
                        vacancy.get("alternate_url", ""),
                    ),
                )

    conn.commit()
    conn.close()

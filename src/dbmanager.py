from src.base_dbmanager import BaseDBManager
import psycopg2


class DBManager(BaseDBManager):
    """Класс для работы с базой данных PostgreSQL"""

    def __init__(self, params: dict) -> None:
        """Инициализация подключение к БД"""
        self.conn = psycopg2.connect(**params)

    def close(self):
        """Закрыть соединение с БД"""
        self.conn.close()

    def get_companies_and_vacancies_count(self):
        """Получает список всех компаний и количество вакансий у каждой компании"""
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT employers.name, COUNT(vacancies.vacancy_id) AS number_of_vacancies
                FROM employers
                LEFT JOIN vacancies ON employers.employer_id = vacancies.employer_id
                GROUP BY employers.employer_id, employers.name
                ORDER BY number_of_vacancies DESC
            """)
            return cur.fetchall()

    def get_all_vacancies(self):
        """Получает список всех вакансий с названием компании, вакансией, зарплатой и ссылкой"""
        with self.conn.cursor() as cur:
            cur.execute(""" 
                SELECT 
                    employers.name AS company_name,
                    vacancies.title AS vacancy_title,
                    vacancies.salary_from,
                    vacancies.salary_to,
                    vacancies.currency, 
                    vacancies.url AS vacancy_url
                FROM vacancies
                INNER JOIN employers ON vacancies.employer_id = employers.employer_id
                ORDER BY company_name, vacancy_title 
            """)
            return cur.fetchall()

    def get_avg_salary(self):
        """Получает среднюю зарплату по всем вакансиям"""
        with self.conn.cursor() as cur:
            cur.execute(""" 
                SELECT AVG((COALESCE(salary_from, salary_to) + 
                            COALESCE(salary_to, salary_from)) / 2) 
                FROM vacancies
                WHERE salary_from IS NOT NULL OR salary_to IS NOT NULL
            """)
            return cur.fetchone()[0]  # возвращаем одно число

    def get_vacancies_with_higher_salary(self):
        """Получает список вакансий, у которых зарплата выше средней"""
        average_salary = self.get_avg_salary()
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT
                    employers.name AS company_name,
                    vacancies.title AS vacancy_title,
                    vacancies.salary_from,
                    vacancies.salary_to,
                    vacancies.currency,
                    vacancies.url AS vacancy_url
                FROM vacancies
                INNER JOIN employers ON vacancies.employer_id = employers.employer_id
                WHERE ((COALESCE(vacancies.salary_from, vacancies.salary_to) + 
                        COALESCE(vacancies.salary_to, vacancies.salary_from)) / 2) > %s
                ORDER BY ((COALESCE(vacancies.salary_from, vacancies.salary_to) + 
                           COALESCE(vacancies.salary_to, vacancies.salary_from)) / 2) DESC
            """, (average_salary,))
            return cur.fetchall()

    def get_vacancies_with_keyword(self, keyword: str):
        """Получает список вакансий, в названии которых содержится переданное слово"""
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT
                    employers.name AS company_name,
                    vacancies.title AS vacancy_title,
                    vacancies.salary_from,
                    vacancies.salary_to,
                    vacancies.currency,
                    vacancies.url AS vacancy_url
                FROM vacancies
                INNER JOIN employers ON vacancies.employer_id = employers.employer_id
                WHERE LOWER(vacancies.title) LIKE LOWER(%s)
                ORDER BY company_name, vacancy_title
            """, (f'%{keyword}%',))
            return cur.fetchall()


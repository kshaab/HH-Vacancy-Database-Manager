from src.config import config
from src.dbmanager import DBManager
from typing import Optional


def print_vacancies(vacancies: list[tuple]) -> None:
    """Функция для вывода информации пользователю"""
    def format_salary(salary_from: Optional[str], salary_to: Optional[str], currency: str) -> str:
        if salary_from or salary_to:
            return f"{salary_from or 'не указана'} - {salary_to or 'не указана'} {currency}"
        return "Зарплата не указана"

    for company, title, salary_from, salary_to, currency, url in vacancies:
        salary = format_salary(salary_from, salary_to, currency)
        print(f"{company}, {title}, {salary}, {url}")


def user_interaction() -> None:
    """Функция взаимодействия с пользователем"""
    db_params = config()
    db_manager = DBManager(db_params)

    while True:
        print("""Выберите действие:
        1. Список компаний и количества вакансий
        2. Список всех вакансий 
        3. Средняя зарплата по вакансиям 
        4. Вакансии с зарплатой выше средней
        5. Поиск по ключевому слову
        6. Выйти """)

        answer = input().strip()

        if answer == "1":
            companies = db_manager.get_companies_and_vacancies_count()
            for company, count in companies:
                print(f"{company}: {count} вакансий.")

        elif answer == "2":
            vacancies = db_manager.get_all_vacancies()
            print_vacancies(vacancies)


        elif answer == "3":
            avg_salary = db_manager.get_avg_salary()
            print(f"Средняя зарплата по вакансиям: {avg_salary}")


        elif answer == "4":
            higher_salary = db_manager.get_vacancies_with_higher_salary()
            print_vacancies(higher_salary)

        elif answer == "5":
            keyword = input("Введите слово для поиска: ").strip()
            vacancies = db_manager.get_vacancies_with_keyword(keyword)
            print_vacancies(vacancies)


        elif answer == "6":
            break

        else:
            print("Неверный ввод. Попробуйте еще раз.")




from abc import ABC, abstractmethod
from typing import List, Tuple


class BaseDBManager(ABC):
    """Абстрактный класс для работы с БД"""

    @abstractmethod
    def get_companies_and_vacancies_count(self) -> List[Tuple]:
        """Получает список всех компаний и количество вакансий у каждой компании"""
        ...

    @abstractmethod
    def get_all_vacancies(self) -> List[Tuple]:
        """Получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию"""
        ...

    @abstractmethod
    def get_avg_salary(self) -> float:
        """Получает среднюю зарплату по вакансиям"""
        ...

    @abstractmethod
    def get_vacancies_with_higher_salary(self) -> List[Tuple]:
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям"""
        ...

    @abstractmethod
    def get_vacancies_with_keyword(self, keyword: str) -> List[Tuple]:
        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова"""
        ...

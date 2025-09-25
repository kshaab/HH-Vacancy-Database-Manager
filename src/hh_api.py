import json
from typing import Any, Dict, List, cast

import requests

from src.base_hh_api import BaseClassAPI


class HeadHunterAPI(BaseClassAPI):
    """Класс для работы с API hh.ru"""

    def __init__(self) -> None:
        """Инициализация приватного атрибута класса"""
        self.__base_url = "https://api.hh.ru"

    def _connect_api(self, endpoint: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Метод подключения к API"""
        try:
            response = requests.get(
                f"{self.__base_url}{endpoint}",
                params=params,
                headers={"User-Agent": "HH-User-Agent"},
                timeout=10,
            )
            response.raise_for_status()
            data = response.json()
            if isinstance(data, dict):
                return data
            return {}
        except requests.RequestException as e:
            print(f"Ошибка при подключении к API: {e}")
            return {}

    def get_companies(self, company_names: list[str]) -> List[Dict[str, Any]]:
        """Метод получения компаний по названию"""
        results: List[Dict[str, Any]] = []

        for name in company_names:
            params = {"text": name, "per_page": 10, "only_with_vacancies": True}
            data = self._connect_api("/employers", params)

            if isinstance(data, dict):
                items = data.get("items", [])
                for item in items:
                    if item.get("name") == name:
                        results.append(item)
                        break

        return results

    def get_vacancies(self, employer_id: str) -> List[Dict[str, Any]]:
        """Метод получения вакансий работодателя по его ID"""
        params = {"employer_id": employer_id, "per_page": 50}
        data = self._connect_api("/vacancies", params)
        return cast(List[Dict[str, Any]], data.get("items", []))


if __name__ == "__main__":
    api = HeadHunterAPI()

    companies = [
        "VK",
        "Газпром недра",
        "Skyeng",
        "Лаборатория Касперского",
        "Four Seasons Hotel Moscow",
        "СБЕР",
        "Яндекс",
        "Солар",
        "ЛУКОЙЛ",
        "STARS COFFEE",
    ]

    json_data_emp = api.get_companies(companies)
    # all_vacancies = {}
    # for company in json_data_emp:
    #     employer_id = company['id']
    #     vacancies = api.get_vacancies(employer_id)
    #     all_vacancies[employer_id] = vacancies

    print("Компании:")
    print(json.dumps(json_data_emp, ensure_ascii=False, indent=4))

    # print("\nВакансии:")
    # print(json.dumps(all_vacancies, ensure_ascii=False, indent=4))

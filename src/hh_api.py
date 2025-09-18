from typing import Any, Dict, List, cast
import requests
from base_class_hh_api import BaseClassAPI


class HeadHunterAPI(BaseClassAPI):
    """Класс для работы с API hh.ru"""

    def __init__(self) -> None:
        "Инициализация приватного атрибута класса"
        self.__base_url = "https://api.hh.ru"

    def _connect_api(self, endpoint: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Метод подключения к API"""
        try:
            response = requests.get(
                f"{self.__base_url}{endpoint}", #endpoint для получения и компаний, и вакансий
                params=params,
                headers={"User-Agent": "HH-User-Agent"},
                timeout=10,
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Ошибка при подключении к API: {e}")
            return {}

    def get_company(self, company_name: str) -> List[Dict[str, Any]]:
        """Метод получения компаний по названию"""
        params = {"text": company_name, "per_page": 10, "only_with_vacancies": True}
        data = self._connect_api("/employers", params)
        return cast(List[Dict[str, Any]], data.get("items", []))

    def get_vacancies(self, employer_id: str) -> List[Dict[str, Any]]:
        """Метод получения вакансий работодателя по его ID"""
        params = {"employer_id": employer_id, "per_page": 50}
        data = self._connect_api("/vacancies", params)
        return cast(List[Dict[str, Any]], data.get("items", []))


if __name__ == "__main__":
    api = HeadHunterAPI()

    companies = api.get_company("Skyeng")
    for company in companies:
        print(f"Работодатель: {company['name']} (id={company['id']})")

        vacancies = api.get_vacancies(company["id"])
        for v in vacancies[:5]:
            print(f"  - {v['name']} ({v['area']['name']})")


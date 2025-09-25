from src.config import config
from src.hh_api import HeadHunterAPI
from src.interaction_function import user_interaction
from src.utils import create_database, save_data_to_database


def main() -> None:
    """Главная функция для запуска проекта"""
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
    companies_data = api.get_companies(companies)
    db_params = config()
    create_database("hh_database", db_params)
    save_data_to_database(companies_data, "hh_database", db_params)
    user_interaction()


if __name__ == "__main__":
    main()

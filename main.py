from src.utils import create_database
from src.hh_api import HeadHunterAPI
from src.config import config


def main():
    api = HeadHunterAPI()
    companies = ["VK", "Газпром недра",
                 "Skyeng", "Лаборатория Касперского",
                 "Four Seasons Hotel Moscow", "СБЕР",
                 "Яндекс", "Солар",
                 "ЛУКОЙЛ", "Полюс"]
    data = api.get_companies(companies)
    params = config()
    create_database("hh_database", params)


if __name__ == "__main__":
    main()


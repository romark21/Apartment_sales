import os
import json
from get_data_from_web import get_data
from database_utils import update_ads_table
# from get_data_from_web import get_ads_list


def fetch_new_ads():
    """
    Функция для парсинга новых объявлений.
    """
    print("Начинаем сбор новых данных...")
    # Собираем данные через get_data
    ads_data = get_data()
    file_path = r'D:\Phyton_programs\apartment_sales_data\data\new_ads.json'
    # file_path = os.path.join(os.getcwd(), 'data', 'new_ads.json')

    # Сохраняем данные в JSON-файл
    # os.makedirs(os.path.dirname(file_path), exist_ok=True)  # Создаём папку, если её нет
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(ads_data, file, ensure_ascii=False, indent=4)

    print(f"Данные сохранены в файл {file_path}")
    print(ads_data)


def update_database():
    """
    Функция для обновления базы данных.
    """
    print("Начинаем обновление базы данных...")
    file_path = r'D:\Phyton_programs\apartment_sales_data\data\new_ads.json'
    # file_path = os.path.join(os.getcwd(), 'data', 'new_ads.json')

    # Загружаем данные из файла
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Файл {file_path} не найден. Сначала выполните fetch_new_ads.")

    with open(file_path, 'r', encoding='utf-8') as file:
        new_ads = json.load(file)

    # Обновляем данные в PostgreSQL
    update_ads_table(new_ads)
    print("Обновление базы данных завершено.")


fetch_new_ads()
update_database()

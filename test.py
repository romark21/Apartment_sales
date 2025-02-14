# from dotenv import load_dotenv
# import os
#
# # Загружаем переменные из .env
# load_dotenv()
#
# # Читаем параметры из переменных окружения
# DB_HOST = os.getenv('DB_HOST')
# DB_PORT = os.getenv('DB_PORT')
# DB_NAME = os.getenv('DB_NAME')
# DB_USER = os.getenv('DB_USER')
# DB_PASSWORD = os.getenv('DB_PASSWORD')
#
# # Используем эти параметры, например, для подключения к PostgreSQL
# DB_CONN_STRING = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
#
#
# # Тестируем вывод переменных
# print(f"DB_HOST: {os.getenv('DB_HOST')}")
# print(f"DB_PORT: {os.getenv('DB_PORT')}")
# print(f"DB_NAME: {os.getenv('DB_NAME')}")
# print(f"DB_USER: {os.getenv('DB_USER')}")
# print(f"DB_PASSWORD: {os.getenv('DB_PASSWORD')}")
# import os
# import json
#
#
# def fetch_new_ads():
#     """
#     Функция для парсинга новых объявлений.
#     """
#     print("Начинаем сбор новых данных...")
#     # Собираем данные через get_data
#     ads_data = [
#         {'city': 'Riga', 'district': 'Purvciems', 'street': 'Marsa g. 6', 'rooms': '1', 'area': '28', 'floor': '5/5',
#          'series': 'Lit pr.', 'house_type': 'Panel', 'facilities': '', 'price': '31 000', 'price_m2': '1 107.14',
#          'ads_date': '20.01.2025 21:53'},
#         {'city': 'Riga', 'district': 'Centre', 'street': 'Rupniecibas 20', 'rooms': '4', 'area': '90', 'floor': '2/4',
#          'series': 'Recon.', 'house_type': 'Brick', 'facilities': 'Balcony, Parking', 'price': '256 000',
#          'price_m2': '2 844.44', 'ads_date': '20.01.2025 21:22'},
#         {'city': 'Riga', 'district': 'Dzeguzhkalns', 'street': 'Daugavgrivas 56', 'rooms': '3', 'area': '58',
#          'floor': '6/9/elevator', 'series': '467-th', 'house_type': 'Panel', 'facilities': 'Loggia, Parking',
#          'price': '65 000', 'price_m2': '1 120.69', 'ads_date': '20.01.2025 21:50'}]
#     file_path = os.path.join(os.getcwd(), 'data', 'new_ads.json')
#
#     # Сохраняем данные в JSON-файл
#     os.makedirs(os.path.dirname(file_path), exist_ok=True)  # Создаём папку, если её нет
#     with open(file_path, 'w', encoding='utf-8') as f:
#         json.dump(ads_data, f, ensure_ascii=False, indent=4)
#
#     print(f"Данные сохранены в файл {file_path}")
#     print(ads_data)
#
#
# fetch_new_ads()


num_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]

k = 5


result = num_list[-abs(k):]
del num_list[-abs(k):]
result.extend(num_list)
print(result)


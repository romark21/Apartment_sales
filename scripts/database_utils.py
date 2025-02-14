import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv
import os


load_dotenv(override=True, encoding='utf-8')


DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')


def create_tables():
    create_cities_table = """
    CREATE TABLE IF NOT EXISTS cities (
        city_id SERIAL PRIMARY KEY,
        city_name TEXT NOT NULL UNIQUE
    );
    """

    create_districts_table = """
    CREATE TABLE IF NOT EXISTS districts (
        district_id SERIAL PRIMARY KEY,
        district_name TEXT NOT NULL UNIQUE
    );
    """

    create_deals_types_table = """
        CREATE TABLE IF NOT EXISTS deals_types(
            deal_type_id SERIAL PRIMARY KEY,
            deal_type_name TEXT NOT NULL UNIQUE
        );
        """

    create_houses_types_table = """
            CREATE TABLE IF NOT EXISTS houses_types(
                house_type_id SERIAL PRIMARY KEY,
                house_type_name TEXT NOT NULL UNIQUE
            );
            """

    create_ads_table = """
    CREATE TABLE IF NOT EXISTS ads (
        ad_id SERIAL PRIMARY KEY,
        posted_date TIMESTAMP NOT NULL,
        street_name TEXT NOT NULL,
        rooms INT,
        area_m2 NUMERIC,
        price NUMERIC,
        price_m2 NUMERIC,
        house_type_id INT REFERENCES houses_types(house_type_id),
        deal_type_id INT REFERENCES deals_types(deal_type_id),
        ads_url VARCHAR,
        city_id INT REFERENCES cities(city_id),
        district_id INT REFERENCES districts(district_id)
    );
    """

    conn = None
    cursor = None
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = conn.cursor()
        cursor.execute(create_cities_table)
        cursor.execute(create_districts_table)
        cursor.execute(create_deals_types_table)
        cursor.execute(create_houses_types_table)
        cursor.execute(create_ads_table)
        conn.commit()
        print("Таблицы успешно созданы.")
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def restart_identity_cascade():
    ads_table = """
        TRUNCATE TABLE ads RESTART IDENTITY CASCADE;
        """

    cities_table = """
        TRUNCATE TABLE cities RESTART IDENTITY CASCADE;
        """

    districts_table = """
        TRUNCATE TABLE cities RESTART IDENTITY CASCADE;
        """

    houses_types_table = """
         TRUNCATE TABLE houses_types RESTART IDENTITY CASCADE;
         """

    transactions_table = """
         TRUNCATE TABLE deals_types RESTART IDENTITY CASCADE;
         """

    conn = None
    cursor = None
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = conn.cursor()
        cursor.execute(ads_table)
        cursor.execute(cities_table)
        cursor.execute(districts_table)
        cursor.execute(houses_types_table)
        cursor.execute(transactions_table)
        conn.commit()
        print("ID успешно обнулены.")
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# def update_ads_table(data: list[dict]):
#     """
#     Добавляет новые объявления в таблицу ads.
#     :param data: Список словарей, где каждый словарь представляет объявление.
#     """
#     insert_sql = """
#     INSERT INTO ads (posted_date, street_name, price, price_m2, city_id, district_id)
#     VALUES (%s, %s, %s, %s, %s, %s)
#     ON CONFLICT (ad_id) DO NOTHING;
#     """
#
#     conn = None
#     cursor = None
#     try:
#         conn = psycopg2.connect(
#             host=DB_HOST,
#             port=DB_PORT,
#             dbname=DB_NAME,
#             user=DB_USER,
#             password=DB_PASSWORD
#         )
#         cursor = conn.cursor()
#
#         # Преобразуем данные в формат для вставки
#         values = [
#             (item['posted_date'], item['street_name'], item['price'],
#              item['price_m2'], item['city_id'], item['district_id'])
#             for item in data
#         ]
#
#         cursor.executemany(insert_sql, values)
#         conn.commit()
#         print(f"{cursor.rowcount} новых объявлений добавлено.")
#     except Exception as e:
#         print(f"Ошибка: {e}")
#     finally:
#         cursor.close()
#         conn.close()


def update_ads_table(data: list[dict]):
    """
    Добавляет новые объявления в таблицу ads и обновляет таблицы cities и districts.
    :param data: Список словарей, где каждый словарь представляет объявление.
    """
    conn = None
    cursor = None
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = conn.cursor()

        # Вставка новых городов
        insert_city_sql = """
        INSERT INTO cities (city_name)
        VALUES (%s)
        ON CONFLICT (city_name) DO NOTHING;
        """
        cities = {item['city'] for item in data if item['city']}
        cursor.executemany(insert_city_sql, [(city,) for city in cities])

        # Вставка новых районов
        insert_district_sql = """
        INSERT INTO districts (district_name)
        VALUES (%s)
        ON CONFLICT (district_name) DO NOTHING;
        """
        districts = {item['district'] for item in data if item['district']}
        cursor.executemany(insert_district_sql, [(district,) for district in districts])

        # Вставка новых типов сделки
        insert_deal_type_sql = """
                INSERT INTO deals_types(deal_type_name)
                VALUES (%s)
                ON CONFLICT (deal_type_name) DO NOTHING;
                """
        deals_types = {item['deal_type'] for item in data if item['deal_type']}
        cursor.executemany(insert_deal_type_sql, [(deal_type,) for deal_type in deals_types])

        # Вставка новых типов сделки
        insert_house_type_sql = """
                        INSERT INTO houses_types (house_type_name)
                        VALUES (%s)
                        ON CONFLICT (house_type_name) DO NOTHING;
                        """
        houses_types = {item['house_type'] for item in data if item['house_type']}
        cursor.executemany(insert_house_type_sql, [(houses_type,) for houses_type in houses_types])

        # Вставка объявлений
        insert_ads_sql = """
        INSERT INTO ads (posted_date, street_name, rooms, area_m2, price, price_m2,
                         house_type_id, deal_type_id, ads_url, city_id, district_id)
        VALUES (
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            (SELECT house_type_id FROM houses_types WHERE house_type_name = %s),
            (SELECT deal_type_id FROM deals_types WHERE deal_type_name = %s),
            %s,
            (SELECT city_id FROM cities WHERE city_name = %s),
            (SELECT district_id FROM districts WHERE district_name = %s)
        );
        """
        values = [
            (
                item['ads_date'], item['street'], item['rooms'], item['area'], item['price'], item['price_m2'], item['house_type'], item['deal_type'],
                item['ads_url'], item['city'], item['district']
            )
            for item in data
        ]
        cursor.executemany(insert_ads_sql, values)

        conn.commit()
        print(f"{cursor.rowcount} новых объявлений добавлено.")
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


# create_tables()
# restart_identity_cascade()

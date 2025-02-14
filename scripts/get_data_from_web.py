import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from time import sleep
import random

# proxies = {
#     'http': 'http://123.45.67.89:8080',
#     'https': 'https://123.45.67.89:8080'}

url = 'https://www.ss.com/en/real-estate/flats/riga/all/'
ads_list = []


def get_headers():
    ua = UserAgent()
    headers = {
        'User-Agent': ua.random,
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': random.choice([
            'https://www.google.com/',
            'https://www.bing.com/',
            'https://www.yahoo.com/'
        ])
    }
    return headers


def safe_request(url, headers):
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None


def get_url():
    response = safe_request(url, headers=get_headers())
    sleep(random.randint(3, 5))
    if response.status_code == 200:
        print(f'Ok. Status code is: {response.status_code}')
        soup = BeautifulSoup(response.text, 'lxml')
        datas = soup.find_all('div', class_="d1")
        if not datas:
            print("No ads found on the page.")
            return
        for data in datas:
            ads_data = data.find('a')
            ads_url = f'https://www.ss.com/' + ads_data.get('href')
            yield ads_url
    else:
        print(f'Not ok. Status code is: {response.status_code}')


def get_data():
    urls = get_url()
    if not urls:
        print("No URLs to process. Exiting...")
        return
    for url in urls:
        d = dict()
        response = requests.get(url, headers=get_headers())
        print(f"Processing URL: {url}")
        # sleep(random.randint(3, 5))
        if response.status_code != 200:
            print(f"Failed to fetch ad. Status code: {response.status_code}")
            continue
        soup = BeautifulSoup(response.text, 'lxml')
        # print(soup)
        d['ads_url'] = url

        try:
            city = soup.find('td', {'id': 'tdo_20'}).text.strip()
        except AttributeError:
            city = ''
        d['city'] = city

        try:
            district = soup.find('td', {'id': 'tdo_856'}).text.strip()
        except AttributeError:
            district = ''
        d['district'] = district

        try:
            street = soup.find('td', {'id': 'tdo_11'}).text.replace('[Map]', '').strip()
        except AttributeError:
            street = ''
        d['street'] = street

        try:
            rooms = soup.find('td', {'id': 'tdo_1'}).text.strip()
        except AttributeError:
            rooms = ''
        d['rooms'] = rooms

        try:
            area = soup.find('td', {'id': 'tdo_3'}).text.replace('m²', '').strip()
        except AttributeError:
            area = ''
        d['area'] = area

        try:
            floor = soup.find('td', {'id': 'tdo_4'}).text.strip()
        except AttributeError:
            floor = ''
        d['floor'] = floor

        try:
            series = soup.find('td', {'id': 'tdo_6'}).text.strip()
        except AttributeError:
            series = ''
        d['series'] = series

        try:
            house_type = soup.find('td', {'id': 'tdo_2'}).text.strip()
        except AttributeError:
            house_type = ''
        d['house_type'] = house_type

        try:
            facilities = soup.find('td', {'id': 'tdo_1734'}).text.strip()
        except AttributeError:
            facilities = ''
        d['facilities'] = facilities

        try:
            price_value = soup.find('td', {'id': 'tdo_8'}).text.strip().split('€')
            if price_value[1].startswith('/mon.'):
                deal_type = 'rent_month'
                price_m2 = price_value[1].replace('(', '').strip().replace(' ', '').replace('/mon.', '')
            elif price_value[1].startswith('/day'):
                deal_type = 'rent_day'
                price_m2 = price_value[1].replace('(', '').strip().replace(' ', '').replace('/day', '')
            else:
                deal_type = 'sell'
                price_m2 = price_value[1].replace('(', '').strip().replace(' ', '')
            price = price_value[0].strip().replace(' ', '')
        except AttributeError:
            price = 0
            price_m2 = 0
            deal_type = ''
        d['price'] = price
        d['price_m2'] = price_m2
        d['deal_type'] = deal_type

        try:
            date_value = (soup.find_all('div', {'class': "ads_contacts_name em9"}) or
                          soup.find_all('td', {'class': "msg_footer"}))
            print(date_value)
            if len(date_value) > 3:
                ads_date = date_value[2].text.replace('Date:', '').strip()
            elif len(date_value) == 2:
                ads_date = date_value[1].text.replace('Date:', '').strip()
            else:
                ads_date = "Date not found"
        except AttributeError:
            ads_date = ''
        d['ads_date'] = ads_date

        print(f'City: {city}, District: {district}, Street: {street}, '
              f'Rooms: {rooms}, Area: {area}m², Floor: {floor}, '
              f'Series: {series}, House type: {house_type}, Facilities: {facilities}, '
              f'ADS url: {url}, Price: {price}€, Price per m2: {price_m2}€, ADS date: {ads_date}')
        print(d)
        if price not in ('Other', 0):
            ads_list.append(d)
        else:
            continue
        print(ads_list)
    return ads_list


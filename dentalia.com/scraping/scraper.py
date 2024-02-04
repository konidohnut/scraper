import json
import re
import requests
from bs4 import BeautifulSoup


def scrape_clinics(url):
    data = {
        'action': 'jet_engine_ajax',
        'handler': 'get_listing',
        'page_settings[post_id]': '5883',
        'page_settings[queried_id]': '344706|WP_Post',
        'page_settings[element_id]': 'c1b6043',
        'page_settings[page]': '1',
        'listing_type': 'elementor',
        'isEditMode': 'false',
    }

    response = requests.post(url, data=data)
    response_data = json.loads(response.text)
    html_data = response_data['data']['html']
    soup = BeautifulSoup(html_data, 'lxml')
    clinics = soup.find_all('div', class_='jet-engine-listing-overlay-wrap')

    data = []

    for clinic in clinics:
        name = clinic.find('h3', class_='elementor-heading-title elementor-size-default').text
        address = clinic.find('div', class_='jet-listing-dynamic-field__content').text

        latlon_matches = clinic.find('a', class_='elementor-button-link elementor-button elementor-size-md').get('href')
        latlon = re.findall(r'@(-?\d+\.\d+),(-?\d+\.\d+),\d+', latlon_matches)

        phone_numbers = clinic.find_all('div', class_='jet-listing jet-listing-dynamic-field display-inline')[
            1].text.replace(
            'Teléfono(s):', '')
        phones = re.findall(r'\(\d{2}\) \d{4}-\d{4}', phone_numbers)

        working_hours_schedule = (
            clinic.find_all('div', class_='jet-listing jet-listing-dynamic-field display-inline')[2].text).replace(
            'Horario:',
            '')
        working_hours = [line.strip() for line in working_hours_schedule.split('\n') if 'a' in line]

        data.append(
            {'name': name, 'address': address, 'latlon': latlon, 'phones': phones, 'working_hours': working_hours})

    return data

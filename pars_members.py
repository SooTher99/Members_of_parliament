import requests
from bs4 import BeautifulSoup
import json
from const import HEADERS
from time import sleep

# Load json file
with open('all_members.json', encoding='utf-8') as file:
    all_members = json.load(file)

# Creating a counter
iteration_count = int(len(all_members)) - 1
count = 0
print(f'Total iterations: {iteration_count}')

# We create a list, in the future we will upload data there
data_list = []

for person_name, person_href in all_members.items():
    req = requests.get(url=person_href, headers=HEADERS)
    src = req.text

    # Save page html file
    with open(f'data/{count}_{person_name}.html', 'w', encoding='utf-8') as file:
        file.write(src)

    # Reading this file
    with open(f'data/{count}_{person_name}.html', encoding='utf-8') as file:
        src = file.read()

    soup = BeautifulSoup(src, 'lxml')

    # Parse biography
    biographies = soup.find(class_='bt-collapse-padding-bottom').find_all('p')
    biographies_text = []
    for item in biographies:
        if len(item.text.strip()) != 0:
            biographies_text.append(item.text.strip())

    # Parse links
    links_text = {}
    links = soup.find(class_='bt-linkliste').find_all('a')
    for item in links:
        if len(item.text.strip()) != 0:
            links_text[item.text.strip()] = item.get('href')

    # Parse names and places of work
    person_name_and_work = soup.find(class_='col-xs-8 col-md-9 bt-biografie-name')
    person_name_ = person_name_and_work.find('h3').text.strip()
    person_work = person_name_and_work.find('p').text.strip()

    # Parse photo
    person_photo = 'https://www.bundestag.de' + \
                   soup.find(class_='bt-bild-standard pull-left').find('img').get('data-img-md-retina')

    # Loading data into a list
    members_info = (
        {
            'Name': person_name_,
            'Work': person_work,
            'Photo': person_photo,
            'Links': links_text,
            'Biography': biographies_text
        }
    )

    data_list.append(members_info)

    # Loading data into json file
    with open('members_info.json', 'w', encoding='utf-8') as file:
        json.dump(data_list, file, indent=4, ensure_ascii=False)

    count += 1
    print(f'# Итераций {count}. {person_name} записан...')
    iteration_count = iteration_count - 1
    if iteration_count == 0:
        print('Работа завершена')
        break
    print(f'Осталось итераций: {iteration_count}')
    sleep(2)

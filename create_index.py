import requests
from bs4 import BeautifulSoup
import json
from const import URL, HEADERS

# Function to create index.html
def get_index(url, headers):
    req = requests.get(url, headers=headers)
    src = req.text

    with open('index.html', 'w', encoding='utf-8') as file:
        file.write(src)


# Uncomment to create index.html
get_index(URL, HEADERS)

# Open index.html
with open('index.html', encoding="utf-8") as file:
    src = file.read()

# Let's convert html into a soup object and look for the class we need
soup = BeautifulSoup(src, 'lxml')
members = soup.find_all(class_='bt-open-in-overlay')

# Fill the dictionary with the found data
all_person_dict = {}
for person in members:
    person_name = person.get('title')
    person_href = person.get('href')
    all_person_dict[person_name] = person_href

# Saving data in json
with open('all_members.json', 'w', encoding='utf-8') as file:
    json.dump(all_person_dict, file, indent=4, ensure_ascii=False)



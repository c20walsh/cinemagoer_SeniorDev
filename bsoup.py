import requests
from bs4 import BeautifulSoup

url = "https://www.imdb.com/name/nm0005458/"
headers = {"User-Agent": "Mozilla/5.0"}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

elements = soup.find_all(True)
movies = []

valid_roles = {"Actor", "Producer", "Director", "Writer", "Editor", "Stunts"}

for elem in elements:
    if elem.name == "a" and "ipc-metadata-list-summary-item__t" in elem.get("class", []):
        movies.append(elem.text.strip())
    elif "ipc-title__text" in elem.get("class", []):
        role_text = elem.text.strip()
        if role_text in valid_roles:
            movies.append("")
            movies.append(role_text.upper())
    elif elem.name == "li" and "credits-total" in elem.get("class", []):
        parent_ul = elem.find_parent("ul")
        if parent_ul and "ipc-inline-list--show-dividers" in parent_ul.get("class", []):
            list_items = parent_ul.find_all("li")
            for i, li in enumerate(list_items):
                if li == elem and i > 0:
                    label = list_items[i - 1].text.strip()
                    movies.append("")
                    movies.append(label.upper())
                    break

for item in movies:
    print(item)

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
import os
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = Options()
options.add_argument("--headless") # remove for demo

driver_path = os.path.join(os.getcwd(), 'geckodriver.exe')
service = Service(driver_path)
driver = webdriver.Firefox(service=service, options=options)

url = "https://www.imdb.com/name/nm0005458/"
driver.get(url)

button = WebDriverWait(driver, 5).until(
    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'All credits')]"))
)
driver.execute_script("arguments[0].scrollIntoView(true);", button)
time.sleep(1)
button.click()

WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "ipc-metadata-list-summary-item__t"))
)

time.sleep(5)
movies = []
valid_roles = {"Actor", "Producer", "Director", "Writer", "Editor", "Stunts", "Thanks", "Self", "Archive Footage"}
elements = driver.find_elements(By.XPATH, "//*")

for elem in elements:
    class_name = elem.get_attribute("class")
    if elem.tag_name == "a" and class_name and "ipc-metadata-list-summary-item__t" in class_name:
        title = elem.text.strip()
        if title:
            movies.append(title)
    elif class_name and "ipc-title__text" in class_name:
        role = elem.text.strip()
        if role in valid_roles:
            movies.append("")
            movies.append(role.upper())
    elif class_name and "credits-total" in class_name:
        parent = elem.find_element(By.XPATH, "..")
        if parent and "ipc-inline-list--show-dividers" in parent.get_attribute("class"):
            items = parent.find_elements(By.TAG_NAME, "li")
            for i, li in enumerate(items):
                if li == elem and i > 0:
                    label = items[i - 1].text.strip()
                    movies.append("")
                    movies.append(label.upper())
                    break


for movie in movies:
    print(movie)
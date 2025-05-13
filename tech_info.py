from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os


def get_full_tech_info(imdb_id):
    options = Options()
    options.add_argument("--headless")

    driver_path = os.path.join(os.getcwd(), 'geckodriver.exe')
    service = Service(driver_path)
    driver = webdriver.Firefox(service=service, options=options)

    url = f"https://www.imdb.com/title/tt{imdb_id}/technical/"
    driver.get(url)

    technical_info = {}

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "ipc-metadata-list"))
        )

        items = driver.find_elements(By.CLASS_NAME, "ipc-metadata-list__item")

        for item in items:
            try:
                label = item.find_element(By.CLASS_NAME, "ipc-metadata-list-item__label").text.strip()
                content = item.find_element(By.CLASS_NAME, "ipc-metadata-list-item__content-container").text.strip()
                technical_info[label] = content
            except:
                continue
    finally:
        driver.quit()

    return technical_info


the_dark_knight_info = get_full_tech_info("0468569")
print("The Dark Knight Technical Info:")
for key, value in the_dark_knight_info.items():
    print(f"{key}: {value}")
print("-" * 20)

the_matrix_info = get_full_tech_info("0133093")
print("The Matrix Technical Info:")
for key, value in the_matrix_info.items():
    print(f"{key}: {value}")
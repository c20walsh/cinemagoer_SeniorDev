from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

def get_all_release_dates(imdb_id):
    options = Options()
    options.add_argument("--headless")

    driver_path = os.path.join(os.getcwd(), 'geckodriver.exe')
    service = Service(driver_path)
    driver = webdriver.Firefox(service=service, options=options)

    url = f"https://www.imdb.com/title/tt{imdb_id}/releaseinfo/"
    driver.get(url)

    release_dates = []

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "ipc-metadata-list"))
        )

        items = driver.find_elements(By.CLASS_NAME, "ipc-metadata-list__item")

        for item in items:
            try:
                country = item.find_element(By.CLASS_NAME, "ipc-metadata-list-item__label").text.strip()
                date = item.find_element(By.CLASS_NAME, "ipc-metadata-list-item__content-container").text.strip()
                release_dates.append({"country": country, "date": date})
            except Exception:
                continue  # skip if any part is missing

    finally:
        driver.quit()

    return release_dates

print(get_all_release_dates("0468569"))

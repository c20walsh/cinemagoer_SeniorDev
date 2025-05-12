from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import re

def get_full_aspect_ratios(imdb_id):
    options = Options()
    options.add_argument("--headless")

    driver_path = os.path.join(os.getcwd(), 'geckodriver.exe')
    service = Service(driver_path)
    driver = webdriver.Firefox(service=service, options=options)

    url = f"https://www.imdb.com/title/tt{imdb_id}/technical/"
    driver.get(url)

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "ipc-metadata-list"))
        )

        items = driver.find_elements(By.CLASS_NAME, "ipc-metadata-list__item")

        for item in items:
            try:
                label = item.find_element(By.CLASS_NAME, "ipc-metadata-list-item__label").text.strip()
                if label.lower() == "aspect ratio":
                    content = item.find_element(By.CLASS_NAME, "ipc-metadata-list-item__content-container").text.strip()
                    return content
            except:
                continue
    finally:
        driver.quit()

    return "Aspect Ratio not found"

# Example usage
raw_text = get_full_aspect_ratios("0468569")
the_dark_knight_ratios = re.findall(r'\d+\.\d+\s*:\s*\d+(?:\s*\([^)]*\))?', raw_text)

print("THE DARK KNIGHT")
for ratio in the_dark_knight_ratios:
    print(ratio)

raw_text = get_full_aspect_ratios("0133093")
the_matrix_ratios = re.findall(r'\d+\.\d+\s*:\s*\d+(?:\s*\([^)]*\))?', raw_text)

print("THE MATRIX")
for ratio in the_matrix_ratios:
    print(ratio)


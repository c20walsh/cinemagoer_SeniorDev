from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import re


def get_full_list(chart):
    # Setup options and driver
    options = Options()
    options.add_argument("--headless")

    driver_path = os.path.join(os.getcwd(), 'geckodriver.exe')
    service = Service(driver_path)
    driver = webdriver.Firefox(service=service, options=options)

    # get current valid chart. I may add some more in the future
    valid_charts = {"top", "bottom", "toptv", "moviemeter"}
    if chart not in valid_charts:
        return "Invalid movie list"

    # Load IMDb page
    url = f"https://www.imdb.com/chart/{chart}/"
    driver.get(url)


    try:
        # Wait for the table of movies to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "ipc-metadata-list-summary-item"))
        )

        # Find all metadata items
        movie_elements = driver.find_elements(By.CLASS_NAME, "ipc-metadata-list-summary-item")

        top_movies = []
        for item in movie_elements:
            title_element = item.find_element(By.CLASS_NAME, "ipc-title__text")
            raw_title = title_element.text.strip()

            # Remove leading rank number like "1. " using regex
            title = re.sub(r"^\d+\.\s*", "", raw_title)

            if title:
                top_movies.append(title)

    finally:
        driver.quit()

    return top_movies


def get_top250_movies():
    return get_full_list("top")


def get_bottom100_movies():
    return get_full_list("bottom")


def get_top250_tv():
    return get_full_list("toptv")


def get_popular100_movies():
    return get_full_list("moviemeter")


print(get_top250_movies())
print(get_bottom100_movies())
print(get_top250_tv())
print(get_popular100_movies())

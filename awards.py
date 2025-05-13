from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

def get_movie_awards(imdb_id):
    options = Options()
    options.add_argument("--headless")
    driver_path = os.path.join(os.getcwd(), 'geckodriver.exe')
    service = Service(driver_path)
    driver = webdriver.Firefox(service=service, options=options)
    url = f"https://www.imdb.com/title/{imdb_id}/awards/"
    driver.get(url)

    awards = []

    try:
        # Wait until at least one award section is present
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "section.ipc-page-section"))
        )

        # Scroll to load all elements
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "section.ipc-page-section"))
        )

        # Find all award sections
        award_sections = driver.find_elements(By.CSS_SELECTOR, "section.ipc-page-section")

        for section in award_sections:
            # Get the category title
            try:
                category_elem = section.find_element(By.CSS_SELECTOR, "h3.ipc-title__text")
                category = category_elem.text.strip()
                # Skip non-award sections
                if any(x in category.lower() for x in ["contribute", "recently viewed", "editorial", "user lists", "user polls"]):
                    continue
            except:
                continue

            # Click all "more" buttons
            for _ in range(2):  # Retry twice
                try:
                    more_buttons = section.find_elements(By.CSS_SELECTOR, "button.ipc-see-more__button")
                    for button in more_buttons:
                        driver.execute_script("arguments[0].click();", button)
                        WebDriverWait(driver, 5).until(
                            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li.ipc-metadata-list-summary-item"))
                        )
                except:
                    break

            # Find the award list
            try:
                award_list = section.find_element(By.XPATH, ".//ul[contains(@class, 'metadata-list') or contains(@class, 'award')]")
            except:
                continue

            # Find all award items
            award_items = award_list.find_elements(By.XPATH, ".//li[contains(@class, 'metadata-list-summary-item')]")
            if not award_items:
                continue

            for item in award_items:
                try:
                    # Find title and result elements
                    title_elem = item.find_element(By.XPATH, ".//span[contains(@class, 'awardCategoryName') or contains(@class, 'ipc-metadata-list-summary-item__li')]")
                    result_elem = item.find_element(By.XPATH, ".//a[contains(@class, 'ipc-metadata-list-summary-item__t') or contains(text(), 'Winner') or contains(text(), 'Nominee')]")
                    award_title = title_elem.text.strip()
                    result = result_elem.text.strip().split(' ', 2)[1]  # Extract "Winner" or "Nominee"

                    awards.append({
                        "category": category,
                        "award": award_title,
                        "result": result
                    })
                except Exception as e:
                    continue

    finally:
        driver.quit()

    return awards

# # Example: Gladiator
# awards = get_movie_awards("tt0133093")  # OR "tt0133093" for The Matrix
# for award in awards:
#     print(award)
import os

import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

DOWNLOAD_LOCATION = "/Users/russell/discordBot/downloads"
SERVICE = Service(ChromeDriverManager().install())

options = Options()
options.headless = True
prefs = {'download.default_directory' : DOWNLOAD_LOCATION}
options.add_experimental_option('prefs', prefs)


def download_link_from_moxfield(moxfield_link):
    try:
        driver = webdriver.Chrome(service=SERVICE, options=options)
        driver.get(moxfield_link)
        more_button = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "subheader-more"))
        )
        more_button.click()
        export_button = driver.find_element(By.XPATH, "// a[contains(text(),'Export')]")
        export_button.click()
        download_button = driver.find_element(By.XPATH, "// a[contains(text(),'Download for MTGO')]")
        return download_button.get_attribute("href")
    except Exception as error:
        print('cannot open')
        return "Broken"
    finally:
        driver.quit()


def download_link_from_manabox(manabox_link):
    try:
        driver = webdriver.Chrome(service=SERVICE, options=options)
        driver.get(manabox_link)
        download_button = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[aria-label="Download deck file"]'))
        )
        download_button.click()
        time.sleep(3)
        return DOWNLOAD_LOCATION + "/" + os.listdir(DOWNLOAD_LOCATION)[0]
    except Exception as error:
        print('cannot open')
        return "Broken"
    finally:
        driver.quit()

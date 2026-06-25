# addDestination and openRoutes

import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

# Setup and initialization
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
driver.implicitly_wait(2)

driver.get("https://www.google.com/maps")  


def add_destination(address):
    empty_bar = driver.find_element(By.ID, 'searchboxinput')
    empty_bar.clear()
    empty_bar.send_keys(address)
    empty_bar.send_keys(Keys.RETURN)


def open_routes():
    xpath = '//button[@data-value="Routes"]'
    wait = WebDriverWait(driver, timeout=5)
    routes_button = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
    routes_button.click()


if __name__ == '__main__':
    target_address = 'Rua Afonsina, 175 - Rudge Ramos, São Paulo - SP, 09633-000'

    time.sleep(600)

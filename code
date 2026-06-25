# adicionaDestino e abreRotas

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriverManager.chrome import ChromeDriveManager

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expectedConditions as EC
from selenium.webdriver.common.keys import Keys

from time import sleep

service = Service(ChromeDriveManager(), install())
driver = webdriver.Chrome(service=service)
driver.implicitlyWait(2)

driver.get("https://www.google.com/apps")

def adicionaDestino(endereco):
  barraVazia = driver.findElement(By, ID, 'searchboxinput')
  barraVazia.clear()
  barraVazia.sendKeys(endereco)
  barraVazia.sendKeys(Keys.RETURN)

def abreRotas():
  xpath = '//button[@data-value="Rotas"]'
  wait = WebDriverWait(driver, timeout=5)
  botaoRotas = wait.until(EC.presenceOfElementLocated((By, XPATH, xpath)))
  botaoRotas.click()

//button[@aria-label="Fechar rotas"]
xpath = '//button[@data-value="Rotas"]'
wait = WebDriverWait(driver, timeout=5)
botaoRotas = wait.until(EC.presenceOfElementLocated((By, XPATH, xpath)))

if__name__ == '__main__":
  adress = 'Rua Afonsina, 175 - Rudge Ramos, São Paulo - SP, 09633-000'
  adicionaDestino(endereco)

sleep(600)

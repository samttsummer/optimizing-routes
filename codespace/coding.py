# IMPORTS

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from time import sleep
import pulp
import itertools


# DRIVER SETUP 

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
driver.implicitly_wait(2)
driver.get("https://www.google.com/maps")


# HELPER FUNCTIONS 

def isOnRoutesTab():
    xpath = '//button[@aria-label="Close directions"]'
    closeRoutesButton = driver.find_elements(By.XPATH, xpath)
    return len(closeRoutesButton) > 0


def addDestination(address, boxNumber=1):
    if not isOnRoutesTab():
        emptySearchBar = driver.find_element(By.ID, 'searchboxinput')
        emptySearchBar.clear()
        emptySearchBar.send_keys(address)
        emptySearchBar.send_keys(Keys.RETURN)
    else:
        xpath = '//div[contains(@id, "directions-searchbox")]//input'
        addressBoxes = driver.find_elements(By.XPATH, xpath)
        addressBoxes = [box for box in addressBoxes if box.is_displayed()]

        if len(addressBoxes) >= boxNumber:
            addressBox = addressBoxes[boxNumber - 1]
            addressBox.send_keys(Keys.CONTROL + 'a')
            addressBox.send_keys(Keys.DELETE)
            addressBox.send_keys(address)
            addressBox.send_keys(Keys.RETURN)
        else:
            print(f'Could not add the address {len(addressBoxes)} | {boxNumber}')


def openDirections():
    xpath = '//button[@data-value="Directions"]'
    wait = WebDriverWait(driver, timeout=5)
    directionsButton = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
    directionsButton.click()

    xpath = '//button[@aria-label="Close directions"]'
    wait = WebDriverWait(driver, timeout=5)
    wait.until(EC.presence_of_element_located((By.XPATH, xpath)))


def addDestinationBox():
    xpath = '//span[text()="Add destination"]'
    wait = WebDriverWait(driver, timeout=3)
    wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))

    addDestinationButton = driver.find_element(By.XPATH, xpath)
    addDestinationButton.click()


def selectTravelMode(travelMode="Driving"):
    xpath = f'//img[@aria-label="{travelMode}"]'
    wait = WebDriverWait(driver, timeout=3)
    travelModeButton = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
    travelModeButton.click()


def getTotalTravelTime():
    xpath = '//div[@id="section-directions-trip-0"]//div[contains(text(),"min")]'
    wait = WebDriverWait(driver, timeout=3)
    travelTimeElement = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
    return int(travelTimeElement.text.replace(' min', ''))


def getTotalDistance():
    xpath = '//div[@id="section-directions-trip-0"]//div[contains(text(),"km")]'
    wait = WebDriverWait(driver, timeout=3)
    distanceElement = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
    return float(distanceElement.text.replace(' km', '').replace(',', '.'))


# MAIN FUNCTIONS 

def generateDistancePairs(addresses):
    distancePairs = {}

    driver.get("https://www.google.com/maps")
    addDestination(addresses[0], 1)
    openDirections()
    selectTravelMode(travelMode="Driving")

    for i, address1 in enumerate(addresses):
        addDestination(address1, 1)

        for j, address2 in enumerate(addresses):
            if i != j:
                addDestination(address2, 2)
                travelTime = getTotalTravelTime()
                distancePairs[f'{i}_{j}'] = travelTime

    return distancePairs


def generateOptimization(addresses, distancePairs):

    def getDistance(address1, address2):
        return distancePairs[f'{address1}_{address2}']

    problem = pulp.LpProblem('TSP', pulp.LpMinimize)

    x = pulp.LpVariable.dicts(
        'x',
        [(i, j) for i in range(len(addresses)) for j in range(len(addresses)) if i != j],
        cat='Binary'
    )

    problem += pulp.lpSum([
        getDistance(i, j) * x[(i, j)]
        for i in range(len(addresses))
        for j in range(len(addresses))
        if i != j
    ])

    for i in range(len(addresses)):
        problem += pulp.lpSum([x[(i, j)] for j in range(len(addresses)) if i != j]) == 1
        problem += pulp.lpSum([x[(j, i)] for j in range(len(addresses)) if i != j]) == 1

    for k in range(len(addresses)):
        for subsetSize in range(2, len(addresses)):
            for subset in itertools.combinations(
                [i for i in range(len(addresses)) if i != k],
                subsetSize
            ):
                problem += pulp.lpSum([
                    x[(i, j)]
                    for i in subset
                    for j in subset
                    if i != j
                ]) <= len(subset) - 1

    problem.solve(pulp.PULP_CBC_CMD())

    solution = []
    startCity = 0
    nextCity = startCity

    while True:
        for j in range(len(addresses)):
            if j != nextCity and x[(nextCity, j)].value() == 1:
                solution.append((nextCity, j))
                nextCity = j
                break

        if nextCity == startCity:
            break

    print('Route:')
    for origin, destination in solution:
        print(origin, ' -> ', destination)

    return solution


def showOptimizedRoute(addresses, solution):
    driver.get("https://www.google.com/maps")

    addDestination(addresses[0], 1)
    openDirections()

    for i, (origin, destination) in enumerate(solution):
        addDestination(addresses[origin], i + 1)
        addDestinationBox()

    addDestination(addresses[0], len(addresses) + 1)


if __name__ == '__main__':

    addresses = [
        "Av. José Bonifácio, 245 - Farroupilha, Porto Alegre - RS, 90040-130",
        "AVENIDA EDVALDO PEREIRA PAIVA 3001 - Praia de Belas, Porto Alegre - RS, 91110-060",
        "Av. Guaíba, 544 - Ipanema, Porto Alegre - RS, 91760-740",
        "Av. Padre Cacique, 2000 - Praia de Belas, Porto Alegre - RS, 90810-180",
        "R. Dr. Salvador França, 1427 - Jardim Botânico, Porto Alegre - RS, 90690-000",
    ]

    distancePairs = generateDistancePairs(addresses)
    solution = generateOptimization(addresses, distancePairs)
    showOptimizedRoute(addresses, solution)

    sleep(600)

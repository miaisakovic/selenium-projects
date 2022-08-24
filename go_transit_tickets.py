from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import selenium.webdriver.support.expected_conditions as ExpectedCondition
import time

service = ChromeService(executable_path=ChromeDriverManager().install())
try:
    driver = webdriver.Chrome(service=service)
except WebDriverException:
    assert False, "Check if Google Chrome is installed"

wait = WebDriverWait(driver, 30)

driver.get("https://www.gotransit.com/en/")

try:
    wait.until(ExpectedCondition.visibility_of_element_located((By.ID, "input-id1")))
    initial_location = driver.find_element(By.ID, "input-id1")
    initial_location.send_keys("Kitchener GO, Kitchener", Keys.DOWN, Keys.RETURN)
    # Wait for the options to load 
    time.sleep(5)
    initial_location.send_keys(Keys.DOWN, Keys.RETURN)
except Exception:
    assert False, "Can't input an initial location"

try:
    wait.until(ExpectedCondition.element_to_be_clickable((By.NAME, "time")))
    time_menu = driver.find_element(By.NAME, "time")
    time_menu.click()
except Exception:
    assert False, "Can't view the available departure times"

try:
    wait.until(ExpectedCondition.element_to_be_clickable((By.XPATH, "//*[text()='17:00']")))
    select_time = driver.find_element(By.XPATH, "//*[text()='17:00']")
    select_time.click()
except Exception:
    assert False, "Can't input 5:00 PM as the departure time"

try:
    wait.until(ExpectedCondition.visibility_of_element_located((By.NAME, "date")))
    date = driver.find_element(By.NAME, "date")
    date.send_keys(Keys.RIGHT, Keys.RETURN)
except Exception:
    assert False, "Can't input a date or submit trip details"

try:
    wait.until(ExpectedCondition.visibility_of_element_located((By.ID, "input-id2")))
    final_destination = driver.find_element(By.ID, "input-id2")
    final_destination.send_keys("Union Station GO, Toronto")
    # Wait for the options to load
    time.sleep(5)
    # Sending the return key submits the final destination and trip details
    final_destination.send_keys(Keys.DOWN, Keys.RETURN)
    wait.until(ExpectedCondition.visibility_of_element_located((By.ID, "TRIP_PLANNER_RESULTS")))
except Exception:
    assert False, "Can't input a final destination"

try:
    wait.until(ExpectedCondition.visibility_of_element_located((By.CLASS_NAME, "trip-details-cta")))
    trip_results = driver.find_elements(By.CLASS_NAME, "trip-details-cta")
except Exception:
    assert False, "Can't locate the top three trip results"

counter = 0
for trip in trip_results:
    try:
        wait.until(ExpectedCondition.visibility_of_element_located((By.CLASS_NAME, "station-text")))
        station_lst = trip.find_elements(By.CLASS_NAME, "station-text")
    except Exception:
        assert False, "Can't find route info"

    print("\nRoute: ", end = "")
    for station in station_lst:
        print(station.text, end = "")
        if station != station_lst[-1]:
            print(" --> ", end = "")

    try:
        wait.until(ExpectedCondition.visibility_of_element_located((By.CLASS_NAME, "columns.text")))
        info_lst = trip.find_elements(By.CLASS_NAME, "columns.text")
    except Exception:
        assert False, "Can't find the departure, arrival, and trip time info"
    
    i = 0
    categories = ["Departs", "Arrives", "Trip Time"]
    while i < len(info_lst):
        print("\n" + categories[i] + ": ", end = "")
        info = info_lst[i].find_element(By.XPATH, "dd[1]")
        print(info.text, end="")
        i = i + 1

    print("\nBuy E-ticket: ", end = "")
    try:
        wait.until(ExpectedCondition.element_to_be_clickable((By.CLASS_NAME, "trip-item-popup-button")))
        ticket_popup = trip.find_element(By.CLASS_NAME, "trip-item-popup-button")
        ticket_popup.click()
    except Exception:
        assert False, "Can't click 'Details / E-tickets' popup"

    try:
        wait.until(ExpectedCondition.element_to_be_clickable((By.XPATH, "//*[text()='Buy E-tickets Now']")))
        ticket = driver.find_element(By.XPATH, "//*[text()='Buy E-tickets Now']")
        ticket.click()
    except Exception:
        assert False, "Can't click 'Buy E-tickets Now' button"

    print(driver.current_url)

    driver.back()

    try:
        wait.until(ExpectedCondition.element_to_be_clickable((By.CLASS_NAME, "close-button.modal-close-button")))
        close_popup = driver.find_element(By.CLASS_NAME, "close-button.modal-close-button")
        close_popup.click()
    except Exception:
        assert False, "Can't close the 'Details / E-tickets' popup"

    counter = counter + 1

driver.quit()

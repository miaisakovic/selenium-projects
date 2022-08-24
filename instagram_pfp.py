from dotenv import load_dotenv
import os
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import selenium.webdriver.support.expected_conditions as ExpectedCondition
import time

load_dotenv()

service = ChromeService(executable_path=ChromeDriverManager().install())
try:
    driver = webdriver.Chrome(service=service)
except WebDriverException:
    assert False, "Check if Google Chrome is installed"

wait = WebDriverWait(driver, 30)

driver.get("https://www.instagram.com/")

try:
    user_username = os.getenv("INSTAGRAM_USERNAME")
    wait.until(ExpectedCondition.visibility_of_element_located((By.NAME, "username")))
    username = driver.find_element(By.NAME, "username")
    username.send_keys(user_username)
except Exception:
    assert False, "Can't input username"

try:
    user_password = os.getenv("INSTAGRAM_PASSWORD")
    wait.until(ExpectedCondition.visibility_of_element_located((By.NAME, "password")))
    password = driver.find_element(By.NAME, "password")
    password.send_keys(user_password)
except Exception:
    assert False, "Can't input password"

try:
    wait.until(ExpectedCondition.element_to_be_clickable((By.XPATH, "//*[text()='Log In']")))
    login = driver.find_element(By.XPATH, "//*[text()='Log In']")
    login.click()
except Exception:
    assert False, "Can't submit credentials"

# Wait for credentials to be submitted 
time.sleep(5)

# If user has 2FA enabled, enter a 6-digit code
if driver.current_url == "https://www.instagram.com/accounts/login/two_factor?next=%2F":
    security_code = input("\nEnter your 6-digit code generated by an authentication app:\n")
    try:
        wait.until(ExpectedCondition.visibility_of_element_located((By.NAME, "verificationCode")))
        password = driver.find_element(By.NAME, "verificationCode")
        password.send_keys(security_code)
    except Exception:
        assert False, "Can't input security code"

    try:
        wait.until(ExpectedCondition.element_to_be_clickable((By.XPATH, "//*[text()='Confirm']")))
        confirm = driver.find_element(By.XPATH, "//*[text()='Confirm']")
        confirm.click()
        # Wait for the security code to be submitted
        time.sleep(5)
    except Exception:
        assert False, "Can't submit security code"

# If prompted to save password, select the "Not Now" option
if driver.current_url == "https://www.instagram.com/accounts/onetap/?next=%2F":
    try:
        wait.until(ExpectedCondition.element_to_be_clickable((By.XPATH, "//*[text()='Not Now']")))
        dont_save_info = driver.find_element(By.XPATH, "//*[text()='Not Now']")
        dont_save_info.click()
    except Exception:
        assert False, "Can't select the 'Not Now' option when asked about saving login info"

# If prompted to turn on notifications, select the "Not Now" option
try:
    wait.until(ExpectedCondition.element_to_be_clickable((By.XPATH, "//*[text()='Not Now']")))
    notifications = driver.find_element(By.XPATH, "//*[text()='Not Now']")
    notifications.click()
except Exception:
    # If the popup for notifications is not present, proceed to view the user's Instagram profile
    pass

driver.get("https://www.instagram.com/" + user_username)

try:
    # If user already has a profile photo
    photo = True
    wait.until(ExpectedCondition.element_to_be_clickable((By.CSS_SELECTOR, "button[title='Change profile photo']")))
    profile_pic = driver.find_element(By.CSS_SELECTOR, "button[title='Change profile photo']")
    profile_pic.click()
except Exception:
    try:
        # If user does not have a profile photo yet
        photo = False
        wait.until(ExpectedCondition.element_to_be_clickable((By.CSS_SELECTOR, "button[title='Add a profile photo']")))
        profile_pic = driver.find_element(By.CSS_SELECTOR, "button[title='Add a profile photo']")
        profile_pic.click()
    except:
        assert False, "Can't click profile picture"

if photo:
    try:
        wait.until(ExpectedCondition.element_to_be_clickable((By.XPATH, "//*[text()='Upload Photo']")))
        upload_profile = driver.find_element(By.XPATH, "//*[text()='Upload Photo']")
        upload_profile.click()
    except:
        assert False, "Can't click the 'Upload Photo' option"

try:
    photo_path = os.getenv("INSTAGRAM_PROFILE_PICTURE")
    wait.until(ExpectedCondition.presence_of_element_located((By.XPATH, "//input[@accept = 'image/jpeg,image/png']")))
    input = driver.find_element(By.XPATH, "//input[@accept = 'image/jpeg,image/png']")
    input.send_keys(photo_path)
    # Wait for the profile photo to change
    time.sleep(10)
except Exception:
    assert False, "Can't upload a new profile picture"

driver.quit() 
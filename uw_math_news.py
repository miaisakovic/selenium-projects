from dotenv import load_dotenv
import os
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import selenium.webdriver.support.expected_conditions as ExpectedCondition
import ssl
from urllib import request
from webdriver_manager.chrome import ChromeDriverManager

load_dotenv()

service = ChromeService(executable_path=ChromeDriverManager().install())
options = Options()
options.add_argument("--window-size=500,500")

try:
    driver = webdriver.Chrome(service=service, options=options)
except WebDriverException:
    assert False, "Check if Google Chrome is installed"

wait = WebDriverWait(driver, 30)

driver.get("https://mathnews.uwaterloo.ca/")

# Click the link of the most recent Math NEWS article
try:
    wait.until(ExpectedCondition.element_to_be_clickable((By.PARTIAL_LINK_TEXT,
                                                          "mathNEWS-")))
    article_link = driver.find_elements(By.PARTIAL_LINK_TEXT, "mathNEWS-")
    text = article_link[0].text
    article_link[0].click()
except Exception:
    assert False, "Can't click the link of the most recent Math NEWS article"

# Override SSL certificate validation
ssl._create_default_https_context = ssl._create_unverified_context

# Retrieve the URL of the article
article_url = driver.current_url

# The relative path to a folder where the article should be saved
# This folder does not need to exist
local_folder = os.getenv('LOCAL_FOLDER_FOR_ARTICLE')

if local_folder[-1] != "/":
    local_folder = local_folder + "/"

# If the folder does not exist, create it
if not os.path.isdir(local_folder):
    os.makedirs(local_folder)

# The file name of the saved article
local_file = text + "-copy.pdf"

# Download the article and save it in the local folder
#   under the specified file name
request.urlretrieve(article_url, local_folder + local_file)

driver.quit()

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import yaml
import logging as log
import random

log.basicConfig(
    filename="log.txt",
    filemode="a",
    level=log.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s: %(message)s',
    datefmt="%Y-%m-%d %H:%M:%S"
)

MAX_TIMEOUT = 7

def driver_init():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get("https://www.swagbucks.com/p/login")

    log.info("Directed to swagbucks.com login page")
    return driver

def read_files():
    log.info("Run started")
    with open("user_config.yaml", "r") as user_stream:
        try: 
            user_config = yaml.safe_load(user_stream)
            log.info("User config loaded")
            return user_config
        except yaml.YAMLError as exc:
            log.error(exc)
            exit(1)

def login(driver, user_config):
    email = user_config["email"]
    password = user_config["password"]

    email_input = WebDriverWait(driver, MAX_TIMEOUT).until(EC.element_to_be_clickable((By.XPATH, "//input[@id='sbxJxRegEmail']")))
    email_input.send_keys(email)

    password_input = WebDriverWait(driver, MAX_TIMEOUT).until(EC.element_to_be_clickable((By.XPATH, "//input[@id='sbxJxRegPswd']")))
    password_input.send_keys(password)

    login_button = WebDriverWait(driver, MAX_TIMEOUT).until(EC.element_to_be_clickable((By.XPATH, "//button[@id='loginBtn']")))
    login_button.click()

    log.info("Successfully logged in")

def redirect_to_polls(driver):
    WebDriverWait(driver, MAX_TIMEOUT).until(EC.invisibility_of_element((By.XPATH, "//button[@id='loginBtn']")))
    driver.get("https://www.swagbucks.com/polls")

def get_table_size(driver):
    poll_table_element = WebDriverWait(driver, MAX_TIMEOUT).until(EC.presence_of_element_located((By.XPATH, "//table[@id='contPollAnswers']")))

    rows = poll_table_element.find_elements(By.TAG_NAME, "tr")
    if rows == []:
        log.warning("You already answered today's poll\n\n")
        exit(0)
    return len(rows) / 4

def click_on_random(driver, size):
    log.info("Answer " + str(random.randint(1, size)) + " was selected")
    chosen_element = WebDriverWait(driver, MAX_TIMEOUT).until(EC.element_to_be_clickable((By.XPATH, "//td[@id='answer" + str(random.randint(1, size)) + "']")))
    chosen_element.click()

def vote(driver):
    vote_button = WebDriverWait(driver, MAX_TIMEOUT).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='btnVote']")))
    vote_button.click()

def complete_daily(driver):
    click_on_random(driver, get_table_size(driver))
    vote(driver)
    log.info("Voting complete\n\n")

if __name__ == "__main__":
    user_config = read_files()
    driver = driver_init()
    login(driver, user_config)
    redirect_to_polls(driver)
    complete_daily(driver)
    driver.close()
import time
import random
import threading

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

chrome_options = Options()
chrome_options.add_extension('./src/Sui-Wallet.crx')

# Because I use M1 Mac it has error
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

driver = webdriver.Chrome(service=Service('./src/chromedriver'), options=chrome_options)

password = '12Testing34'

driver.maximize_window()
wait = WebDriverWait(driver, 5)
parent = driver.window_handles[0]


def switch_tab():
    windows = driver.window_handles
    for w in windows:
        if w != parent:
            driver.switch_to.window(w)


def setup_sui_wallet():
    driver.get('https://www.google.com')

    switch_tab()

    sui_wallet_get_started_btn = wait.until(
        ec.visibility_of_element_located(
            (By.XPATH, '/html/body/div/div/div/div/div/div[2]/a')))
    sui_wallet_get_started_btn.click()

    sui_wallet_create_new_wallet_btn = wait.until(
        ec.visibility_of_element_located(
            (By.XPATH, '/html/body/div/div/div/div[1]/a')))
    sui_wallet_create_new_wallet_btn.click()

    sui_wallet_create_password_input = wait.until(
        ec.visibility_of_element_located(
            (By.XPATH, '/html/body/div/div/div/form/div/fieldset/label[1]/input')))
    sui_wallet_create_password_input.send_keys(password)

    sui_wallet_confirm_password_input = wait.until(
        ec.visibility_of_element_located(
            (By.XPATH, '/html/body/div/div/div/form/div/fieldset/label[2]/input')))
    sui_wallet_confirm_password_input.send_keys(password)

    sui_wallet_create_password_check_box = wait.until(
        ec.visibility_of_element_located(
            (By.XPATH, '/html/body/div/div/div/form/div/fieldset/label[3]/span[1]')))
    sui_wallet_create_password_check_box.click()

    sui_wallet_create_wallet_btn = wait.until(
        ec.visibility_of_element_located(
            (By.XPATH, '/html/body/div/div/div/form/button')))
    sui_wallet_create_wallet_btn.click()

    time.sleep(2)

    sui_wallet_seed_phrase = wait.until(
        ec.visibility_of_element_located(
            (By.XPATH, '/html/body/div/div/div/div[2]')))

    with open(f'wallets/wallet-{int(random.random() * 10 ** 16)}', 'w') as wallet_file:
        wallet_file.write(sui_wallet_seed_phrase.text.split('\nCOPY')[0])

    sui_wallet_open_sui_wallet_btn = wait.until(
        ec.visibility_of_element_located(
            (By.XPATH, '/html/body/div/div/div/button')))
    sui_wallet_open_sui_wallet_btn.click()


setup_sui_wallet()

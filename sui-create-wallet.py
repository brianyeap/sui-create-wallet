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

password = '12Testing34'


def setup_sui_wallet():
    try:
        # Because I use M1 Mac it has error
        # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        chrome_options = Options()
        chrome_options.add_extension('./src/Sui-Wallet.crx')
        driver = webdriver.Chrome(service=Service('./src/chromedriver'), options=chrome_options)
        driver.maximize_window()
        wait = WebDriverWait(driver, 5)
        parent = driver.window_handles[0]

        def switch_tab():
            windows = driver.window_handles
            for w in windows:
                if w != parent:
                    driver.switch_to.window(w)

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

        return 1
    except Exception as e:
        # print(e)
        return 0


count = 0
total_needed = 100
thread_times = 3


def temp_func():
    while True:
        start_time = time.time()
        if setup_sui_wallet():
            print(f'Executed in: {round(time.time() - start_time)}S')
            break
        else:
            print('Retrying...')


while count < total_needed:
    thread_list = []
    temp_count = 0

    if (total_needed - count) < thread_times:
        thread_times = total_needed - count

    while temp_count < thread_times:
        t = threading.Thread(target=temp_func)
        thread_list.append(t)

        count += 1
        temp_count += 1
        print(f'Count: {count}/{total_needed}')

    for thread in thread_list:
        thread.start()

    for thread in thread_list:
        thread.join()

    print(f'Finished: {count}/{total_needed}')

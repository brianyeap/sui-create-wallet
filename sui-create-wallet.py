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
total_amount = 0

def setup_sui_wallet(amount):

    global total_amount
    try:
        chrome_options = Options()
        chrome_options.add_extension('./src/suiet-sui-wallet.crx')
        driver = webdriver.Chrome(service=Service('./src/chromedriver'), options=chrome_options)
        driver.maximize_window()
        wait = WebDriverWait(driver, 20)
        driver.get('chrome-extension://khpkpbbcccdmmclmpigdgddabeilkdpd/index.html')

        sui_wallet_create = wait.until(
            ec.visibility_of_element_located(
                (By.XPATH, '/html/body/div/div/div[1]/section/button[1]')))
        sui_wallet_create.click()

        wallet_password_field = wait.until(
            ec.visibility_of_element_located(
                (By.XPATH, '/html/body/div/div/div[1]/div/section/form/div[1]/div/div/input')))
        wallet_password_field.click()
        wallet_password_field.send_keys(password)

        wallet_password_field = wait.until(
            ec.visibility_of_element_located(
                (By.XPATH, '/html/body/div/div/div[1]/div/section/form/div[2]/div/div/input')))
        wallet_password_field.click()
        wallet_password_field.send_keys(password)
        next_step = wait.until(
            ec.visibility_of_element_located(
                (By.XPATH, '/html/body/div/div/div[1]/div/section/form/button')))
        next_step.click()
        
        pass_phrase = wait.until(
            ec.visibility_of_element_located(
                (By.XPATH, '/html/body/div/div/div[1]/div/section/div/div[1]')))
                
        seed_phrase = pass_phrase.text
        seed_phrase = seed_phrase.split('\n')
        clean_phrase = []
        for word in seed_phrase:
            word = str(word)
            if not word.isnumeric():
                clean_phrase.append(word)
        with open(f'seeds/{random.randint(0, 999999999)}', 'w+') as f:
            f.write(str(clean_phrase))
            
        done = wait.until(
            ec.visibility_of_element_located(
                (By.XPATH, '/html/body/div/div/div[1]/div/section/button')))
        done.click()
        view_wallets = wait.until(
            ec.visibility_of_element_located(
                (By.XPATH, '/html/body/div/div/div[1]/div[1]/div[2]/span')))
        view_wallets.click()
            
        for i in range(amount):
            start_time = time.time()
            creat_wallet = wait.until(
                ec.visibility_of_element_located(
                    (By.XPATH, '/html/body/div[2]/div/section[2]/button[1]')))
            creat_wallet.click()
            pass_phrase = wait.until(
                ec.visibility_of_element_located(
                (By.XPATH, '/html/body/div/div/div[1]/div/section/div/div[1]')))
                
            seed_phrase = pass_phrase.text
            seed_phrase = seed_phrase.split('\n')
            clean_phrase = []
            for word in seed_phrase:
                word = str(word)
                if not word.isnumeric():
                    clean_phrase.append(word)
            with open(f'seeds/{random.randint(0, 999999999)}', 'w+') as f:
                f.write(str(clean_phrase))
                done = wait.until(
                ec.visibility_of_element_located(
                    (By.XPATH, '/html/body/div/div/div[1]/div/section/button')))
            done.click()
            total_amount += 1
            print(f'#{total_amount} Executed in: {round(time.time() - start_time)}S')
    except Exception as e:
        print(e)
        return 0


total_needed = 100
thread_times = 3


def temp_func():
    amount = int(total_needed / thread_times)
    setup_sui_wallet(amount)
count = 0
thread_list = []
while count < thread_times:
    t = threading.Thread(target=temp_func)
    thread_list.append(t)
    count += 1
    print(f'created thread: {count}/{thread_times}')

for thread in thread_list:
    thread.start()

for thread in thread_list:
    thread.join()
    print(f'Finished: {count}/{total_needed}')
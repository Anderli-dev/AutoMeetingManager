import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument("start-maximized")

driver = webdriver.Chrome(options=chrome_options)

driver.get("https://classroom.google.com")

wait = WebDriverWait(driver, 2)

main_menu = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@role='menu']")))

actions = ActionChains(driver)
actions.move_to_element(main_menu).perform()

submenu_option = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@role='menuitem'][.//span[text()='Google Classroom']]")))

submenu_option.click()

next_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@id='identifierNext']//button")))

driver.switch_to.active_element.send_keys(email)

next_btn.click()
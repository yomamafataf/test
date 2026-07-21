import os
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1")
ARTIFACTS = Path("artifacts")
ARTIFACTS.mkdir(exist_ok=True)

options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)

try:
    wait = WebDriverWait(driver, 10)

    # Test an invalid common password.
    driver.get(BASE_URL)
    driver.find_element(By.ID, "password").send_keys("password")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    wait.until(
        lambda browser:
        "common-password list" in browser.page_source
    )

    # Test a valid password.
    driver.get(BASE_URL)
    driver.find_element(By.ID, "password").send_keys(
        "Correct-Horse-Battery-Staple-2026!"
    )
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    wait.until(
        lambda browser:
        "Welcome" in browser.page_source
    )

    print("Selenium UI tests passed.")

except Exception:
    driver.save_screenshot(ARTIFACTS / "ui-test-failure.png")
    raise

finally:
    driver.quit()
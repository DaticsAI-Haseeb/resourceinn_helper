from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def login_to_portal(username, password):
    # Setup the Chrome WebDriver
    driver = webdriver.Chrome()

    # Open the portal login page
    driver.get("https://datics.resourceinn.com/#/core/login")

    # Wait for the login elements to be loaded
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='username']"))
    )

    # Input the username and password
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@id='username']"))
    ).send_keys(username)
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@id='password']"))
    ).send_keys(password)

    # Click the login button
    # Instead of using the button's inner HTML, we find it by its class and action (assuming it's unique)
    login_button = driver.find_element(By.XPATH, "//button[contains(@class,'btn-submit-full') and @ng-click='login()']")
    login_button.click()

    return driver


def do_check_in(driver):
    # Wait and click the Check In button
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.mark_button:nth-child(1)"))
    ).click()


def do_check_out(driver):
    # Wait and click the Check Out button
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.mark_button:nth-child(2)"))
    ).click()
    time.sleep(5)  # Wait for the confirmation modal to appear
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.confirm"))
    ).click()


def toggle_break(driver):
    # Click the Break Out/Break In toggle button
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".mark_break_button"))
    ).click()


# # Example usage
# if __name__ == "__main__":
#     username = "hehe@gmail.com"
#     password = "hehe"
#     driver = login_to_portal(username, password)
#
#     time.sleep(10)  # Adjust based on page load times
#
#     toggle_break(driver)
#
#     time.sleep(10)  # Adjust based on page load times
#
#     # Remember to close the browser when done
#     driver.quit()

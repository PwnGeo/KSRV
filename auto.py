from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Initialize the browser
driver = webdriver.Chrome()  # or webdriver.Firefox()

try:
    # Open the login page
    driver.get("http://192.168.10.2:81/login.php")

    # Perform login
    username = "admin"
    password = "admin"

    # Fill in login information and submit the form
    input_username = driver.find_element(By.ID, "uname")
    input_password = driver.find_element(By.ID, "pwd")

    input_username.send_keys(username)
    input_password.send_keys(password)
    input_password.send_keys(Keys.ENTER)  # Submit using Enter key (or click button)

    # Wait for 5 seconds for the page to load and retrieve cookies
    time.sleep(5)

    # Get cookies
    cookies = driver.get_cookies()

    # Write PHPSESSID value to cookie.txt file
    with open("cookie.txt", "w") as cookie_file:
        for cookie in cookies:
            if cookie['name'] == 'PHPSESSID':
                cookie_file.write(cookie['value'] + "\n")
                break  # Once found PHPSESSID, break the loop

finally:
    # Close the browser when done
    driver.quit()

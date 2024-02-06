import time
from selenium import webdriver
from selenium.webdriver.common.by import By


def get_public_ip_with_selenium():
    global public_ip

    # Set up Selenium webdriver (make sure you have the webdriver installed and in your PATH)
    driver = webdriver.Chrome()  # You can use other webdrivers like Firefox, Edge, etc.

    # Navigate to the httpbin IP address endpoint
    driver.get('https://ipinfo.io/')

    # Find the element containing the IP address
    ip_element = driver.find_element(By.XPATH, '//*[@id="search-widget"]/input').get_attribute('value')
    # Extract the IP address text
    public_ip = ip_element.strip()
    # Close the webdriver
    driver.quit()

    return public_ip


if __name__ == "__main__":
    public_ip = get_public_ip_with_selenium()
    if public_ip:
        print("Your public IP address is:", public_ip)

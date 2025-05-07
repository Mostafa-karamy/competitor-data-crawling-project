from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--headless")  # optional, makes Chrome invisible

# Create a Service object with the chromedriver path
driver_path = r"C:\Users\admin\MicroModern\chromedriver\chromedriver.exe"
service = Service(executable_path=driver_path)

# Use the Service object when initializing the WebDriver
driver = webdriver.Chrome(service=service, options=options)

driver.get("https://www.google.com")
print(driver.title)
driver.quit()

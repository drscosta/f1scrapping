#scrapping the driver standings from the F1 website and writing them to a CSV file

import csv
from selenium import webdriver
#chrome options below
#from selenium.webdriver.chrome.service import Service
#from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager

#use for Chrome
#driver = webdriver.Chrome(service=Service(ChromeDriverManager.install()), options=options)

#logging options
import logging
from webdriver_manager.core.logger import set_logger

logger = logging.getLogger("custom_logger")
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())
logger.addHandler(logging.FileHandler("custom.log"))

set_logger(logger)

#use for Firefox
driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))

#fetch the URL
driver.get("https://www.formula1.com/en/results.html/2023/drivers.html")
#start a maximized window
driver.maximize_window()
#wait for elements to load. To improve in the future as this is not the safest load strategy
driver.implicitly_wait(0.5)

print("###########################")
print("website loaded...")

rows = driver.find_elements(by="xpath", value='//table[@class="resultsarchive-table"]/tbody/tr')

csv_file = "driver_positions.csv"

#open the CSV file in write mode
with open(csv_file, "w", newline="") as file:
    writer = csv.writer(file)

    #write the table headers to the CSV file
    headers = ["Position", "Driver", "Nationality", "Car", "Points"]
    writer.writerow(headers)

    for row in rows:
        #extract the data from each column using XPath
        position = row.find_element(by="xpath", value='./td[2]').text
        driver_name = row.find_element(by="xpath", value='./td[3]/a').text
        nationality = row.find_element(by="xpath", value='./td[4]').text
        car = row.find_element(by="xpath", value='./td[5]/a').text
        points = row.find_element(by="xpath", value='./td[6]').text
        #write the extracted data to the CSV file
        writer.writerow([position, driver_name, nationality, car, points])

print("\n###########################")
print(csv_file + " written!")
driver.quit()
import os
import re
import time
import logging
from datetime import datetime
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException

print(
    "======================================= START ======================================="
)
print("Ensure all instances of 'Data.csv' are closed to prevent data lose.")

# Initialize logger.
logging.basicConfig(
    filename="log.txt", level=logging.ERROR, format="%(asctime)s - %(message)s"
)
# logging.disable(logging.CRITICAL) # <====== REMEMBER TO COMMENT THIS.

# Get location of workign directory.
working_dir = os.getcwd()

# Create empty list variables that will contain scraped data.
parsed_data = []
car_type = []
car_make = []
price = []
total_price = []
mileage = []
year = []
engine = []
transmition = []
location = []
model_code = []
engine_code = []
steering = []
color = []
fuel = []
drive = []
seats = []
doors = []

# Declare chromedriver options.
chrome_options = webdriver.ChromeOptions()

window_vis = int(
    input(" Press 1: To show window.\n Press 2: To hide window.\n")
)  # Hide window option

if window_vis != (1 or 2):
    raise Exception("You didn't pick either one of the specified options")

try:
    if window_vis == 1:
        pass
    elif window_vis == 2:
        chrome_options.add_argument("--headless")
except Exception as e:
    print(e)

chrome_options.add_argument("--no-zygote")
chrome_options.add_argument("--mute-audio")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--log-level=3")
chrome_options.add_argument("--disable-breakpad")
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--ignore-ssl-errors")
chrome_options.add_argument("--disable-web-security")
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--allow-running-insecure-content")
chrome_options.add_argument("--ignore-certificate-errors-spki-list")
chrome_options.add_argument("--disable-features=VizDisplayCompositor")
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

# Set desired capabilities to ignore SSL stuff.
desired_capabilities = chrome_options.to_capabilities()
desired_capabilities["acceptInsecureCerts"] = True
desired_capabilities["acceptSslCerts"] = True

# Set up Chromedriver.
url = r"https://www.beforward.jp//"
driver_location = os.path.join(working_dir, r"chromedriver.exe")

driver = webdriver.Chrome(
    driver_location,
    options=chrome_options,
    desired_capabilities=desired_capabilities,
)

# Check for next Page function.
def check_next_page():
    try:
        check = driver.find_element(By.CSS_SELECTOR(".pagination-next"))
        return True
    except (NoSuchElementException):
        return False


# Getting Start datetime.
start_time = datetime.now()

# Run Chromedriver.
print("Starting chromedriver")

try:
    driver.maximize_window()
    print("Loading URL")
    driver.get(url)

    # Scraper code.
    print("Starting scraping process")
    # Locate Shop by type element.
    shop_by_type = driver.find_element_by_xpath("//ul[@id='shop-by-type']")
    car_types = shop_by_type.find_elements_by_tag_name("li")  # Get car type elements.

    for item in car_types:  # Iterate through Each car type.
        print("Selecting car element")
        car_t = item.text
        car_final = re.sub("[(\d, )]", "", car_t)
        item.click()
        time.sleep(3)

        # Toggle 100 results button.
        print("Attempting to toggle result button")
        try:
            select = driver.find_element_by_xpath(
                "//div[@class='results results-bottom']//select[@name='view_cnt']"
            )
            select.find_element_by_css_selector(
                "div[class='results results-bottom'] option[value='100']"
            ).click()
            print("Result button toggled successfully")
        except (NoSuchElementException):
            print("Didn't find result button")
            pass

        page_count = 1

        while check_next_page != False:
            time.sleep(2)
            # Delete login element.
            print(("Attempting to delete login element"))
            attempts = 0
            while attempts < 2:
                try:
                    driver.execute_script(
                        """var element = document.getElementsByClassName("stocklist-row login-banner-table")[0];
                        element.parentNode.removeChild(element);"""
                    )
                    print("Login element deleted")
                    attempts = 2
                except:
                    attempts += 1
                    if attempts == 2:
                        print("Didn't find login element")
                    else:
                        pass

            # Get car row wrapper.
            time.sleep(2)
            print("Getting car row wrapper...")
            car_container = driver.find_element_by_xpath(
                "//table[@class='stocklist-row-wrap']"
            )
            # Get list of cars in stock within car row wrapper.
            print("Getting cars in stock row wrapper")
            cars = car_container.find_elements_by_class_name("stocklist-row")
            count = 0

            # Loop through cars in car wrapper.
            print(f"Attempting to scrape car type {car_final} data")
            for car in cars:
                try:
                    count += 1
                    if (count == 15) or (count == 23):
                        pass
                    else:
                        car_type.append(car_final)
                        try:
                            car_make.append(
                                car.find_element_by_class_name("make-model").text
                            )
                        except (NoSuchElementException):
                            car_make.append(None)
                        try:
                            price.append(car.find_element_by_class_name("price").text)
                        except (NoSuchElementException):
                            price.append(None)
                        try:
                            total_price.append(
                                car.find_element_by_class_name("total-price").text
                            )
                        except (NoSuchElementException):
                            total_price.append(None)
                        try:
                            mileage.append(
                                driver.find_element(
                                    By.CSS_SELECTOR,
                                    f".stocklist-row:nth-child({count}) .mileage > .val",
                                ).text
                            )
                        except (NoSuchElementException):
                            mileage.append(None)
                        try:
                            year.append(
                                driver.find_element(
                                    By.CSS_SELECTOR,
                                    f".stocklist-row:nth-child({count}) .year > .val",
                                ).text
                            )
                        except (NoSuchElementException):
                            year.append(None)
                        try:
                            engine.append(
                                driver.find_element(
                                    By.CSS_SELECTOR,
                                    f".stocklist-row:nth-child({count}) .engine > .val",
                                ).text
                            )
                        except (NoSuchElementException):
                            engine.append(None)
                        try:
                            transmition.append(
                                driver.find_element(
                                    By.CSS_SELECTOR,
                                    f".stocklist-row:nth-child({count}) .trans > .val",
                                ).text
                            )
                        except (NoSuchElementException):
                            transmition.append(None)
                        try:
                            location.append(
                                driver.find_element(
                                    By.CSS_SELECTOR,
                                    f".stocklist-row:nth-child({count}) .val > span",
                                ).text
                            )
                        except (NoSuchElementException):
                            location.append(None)
                        try:
                            model_code.append(
                                driver.find_element(
                                    By.CSS_SELECTOR,
                                    f".stocklist-row:nth-child({count}) tr:nth-child(1) > .td-1st",
                                ).text
                            )
                        except (NoSuchElementException):
                            model_code.append(None)
                        try:
                            engine_code.append(
                                driver.find_element(
                                    By.CSS_SELECTOR,
                                    f".stocklist-row:nth-child({count}) tr:nth-child(2) > .td-1st",
                                ).text
                            )
                        except (NoSuchElementException):
                            engine_code.append(None)
                        try:
                            steering.append(
                                driver.find_element(
                                    By.CSS_SELECTOR,
                                    f".stocklist-row:nth-child({count}) tr:nth-child(1) > .td-2nd",
                                ).text
                            )
                        except (NoSuchElementException):
                            steering.append(None)
                        try:
                            color.append(
                                driver.find_element(
                                    By.CSS_SELECTOR,
                                    f".stocklist-row:nth-child({count}) tr:nth-child(2) > .td-2nd",
                                ).text
                            )
                        except (NoSuchElementException):
                            color.append(None)
                        try:
                            fuel.append(
                                driver.find_element(
                                    By.CSS_SELECTOR,
                                    f".stocklist-row:nth-child({count}) tr:nth-child(1) > .td-3rd",
                                ).text
                            )
                        except (NoSuchElementException):
                            fuel.append(None)
                        try:
                            drive.append(
                                driver.find_element(
                                    By.CSS_SELECTOR,
                                    f".stocklist-row:nth-child({count}) tr:nth-child(2) > .td-3rd",
                                ).text
                            )
                        except (NoSuchElementException):
                            drive.append(None)
                        try:
                            seats.append(
                                driver.find_element(
                                    By.CSS_SELECTOR,
                                    f".stocklist-row:nth-child({count}) tr:nth-child(1) > .td-4th",
                                ).text
                            )
                        except (NoSuchElementException):
                            seats.append(None)
                        try:
                            doors.append(
                                driver.find_element(
                                    By.CSS_SELECTOR,
                                    f".stocklist-row:nth-child({count}) tr:nth-child(2) > .td-4th",
                                ).text
                            )
                        except (NoSuchElementException):
                            doors.append(None)

                    if count > 100:
                        pass
                    else:
                        print(
                            f"Done getting data for car number {count} of type {car_final} on page {page_count}"
                        )
                except Exception as e:
                    logging.error(e)
                    pass

            # Attempt to remove popup if present.
            attempts = 0
            while attempts < 2:
                try:
                    driver.execute_script(
                        """var element = document.getElementsByClassName("not-operation-popup active")[0];
                        element.parentNode.removeChild(element);"""
                    )
                    print("Found popup and removed it")
                    attempts = 2
                except (NoSuchElementException):
                    attempts += 1
                    pass

            print(f"Done scraping data for all {car_final} cars on page {page_count}\n")

            # Next page.
            attempts = 0
            while attempts < 3:
                try:
                    print("Attempting to go to next Page")
                    pagination = driver.find_element_by_class_name("results-pagination")
                    pagination.find_element_by_xpath(
                        "//a[normalize-space()='Next Page']"
                    ).click()
                    attempts = 3
                    time.sleep(2)
                except:
                    attempts += 1
                    pass

            page_count += 1

        print(f"Done scraping data for all {car_final}\n")

    print("Done Scrapping data for all cars\n")

except (TimeoutException):
    logging.error("Took too long to load webpage. Check your internet connection")
except Exception as e:
    logging.error(e)
    pass

finally:
    # Teardown window.
    end_time = datetime.now()  # Get end datetime.
    time_taken = end_time - start_time  # Get time taken.

    print("Terminating chromedriver...")
    driver.quit()

# Print time taken.
print("Started at: ", start_time)
print("Finished at: ", end_time)
print("Time taken: ", time_taken)

# Create data frame and add data to it.
data = {
    "car type": car_type,
    "car make": car_make,
    "price": price,
    "total price": total_price,
    "mileage": mileage,
    "engine": engine,
    "transmition": transmition,
    "location": location,
    "model code": model_code,
    "engine code": engine_code,
    "steering": steering,
    "color": color,
    "fuel": fuel,
    "drive": drive,
    "seats": seats,
    "doors": doors,
}

print("Creating data frame")
data_frame = pd.DataFrame(data)

print("Showing data frame head\n")
print(data_frame.head(10))

# Save dataframe to CSV file.
try:
    data_frame.to_csv(os.path.join(working_dir, "Data.csv"), index=False, header=True)
except:
    print("Unable to save csv file")

print("End of program.")

print(
    "======================================== END ========================================"
)

import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup

# Initialize WebDriver
driver = webdriver.Chrome()

# Open the website
driver.get("https://voterlist.election.gov.np/")

time.sleep(3)  # Allow page to load

# Prepare CSV file
csv_filename = "voter_data.csv"
with open(csv_filename, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["State", "District", "VDC/Municipality", "Ward", "Reg Centre", "Voter Data"])  # Adjust columns

# Select dropdowns
state_dropdown = Select(driver.find_element(By.ID, "state"))
district_dropdown = Select(driver.find_element(By.ID, "district"))
vdc_dropdown = Select(driver.find_element(By.ID, "vdc_mun"))
ward_dropdown = Select(driver.find_element(By.ID, "ward"))
reg_centre_dropdown = Select(driver.find_element(By.ID, "reg_centre"))

# Get all dropdown options (excluding the first empty option)

state_options = []
for option in state_dropdown.options:
    text = option.text.strip()
    if text:
        state_options.append(text)

# Loop through each state
for state in state_options:
    state_dropdown.select_by_visible_text(state)
    time.sleep(2)  # Allow the district dropdown to update

    district_options = []
    for option in district_dropdown.options:
        text = option.text.strip()
        if text:
            district_options.append(text)

    for district in district_options:
        district_dropdown.select_by_visible_text(district)
        time.sleep(2)  # Allow VDC dropdown to update

        vdc_options = []
        for option in vdc_dropdown.options:
            text = option.text.strip()
            if text:
                vdc_options.append(text)

        for vdc in vdc_options:
            vdc_dropdown.select_by_visible_text(vdc)
            time.sleep(2)  # Allow ward dropdown to update

            ward_options = []
            for option in ward_dropdown.options:
                text = option.text.strip()
                if text:
                    ward_options.append(text)

            for ward in ward_options:
                ward_dropdown.select_by_visible_text(ward)
                time.sleep(2)  # Allow reg centre dropdown to update

                reg_centre_options = []
                for option in reg_centre_dropdown.options:
                    text = option.text.strip()
                    if text:
                        reg_centre_options.append(text)

                for reg_centre in reg_centre_options:
                    reg_centre_dropdown.select_by_visible_text(reg_centre)
                    time.sleep(2)

                    # Click submit button
                    submit_button = driver.find_element(By.ID, "btnSubmit")
                    submit_button.click()
                    time.sleep(5)  # Wait for table to load

                    
                        
                    try:
                        dataLength_dropdown = Select(driver.find_element(By.NAME, "tbl_data_length"))
                        dataLength_dropdown.select_by_value("100")
                        time.sleep(2)
                        table = driver.find_element(By.ID, "tbl_data")
                        table_html = table.get_attribute('outerHTML')  # Get the full HTML of the table
                    except:
                        table_html = None  # If table is not found, set to None

                    if table_html:
                        # Parse the HTML table with BeautifulSoup
                        soup = BeautifulSoup(table_html, "html.parser")

                        # Extract all rows from the table
                        rows = soup.find_all("tr")
                        for row in rows:
                            cols = row.find_all("td")
                            cols = [col.text.strip() for col in cols]  # Clean text from each column
                            if cols:
                                with open(csv_filename, "a", newline="", encoding="utf-8") as file:
                                    writer = csv.writer(file)
                                    writer.writerow([state, district, vdc, ward, reg_centre] + cols)

print(f"Data saved to {csv_filename}")

# Close the browser
driver.quit()

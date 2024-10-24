import os
import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image
from io import BytesIO

# Directory to save logos
LOGO_DIR = "logos"
if not os.path.exists(LOGO_DIR):
    os.makedirs(LOGO_DIR)

# Path to your ChromeDriver from an environment variable
CHROME_DRIVER_PATH = os.getenv(
    "CHROME_DRIVER_PATH"
)  # Set this environment variable to the ChromeDriver path


def setup_driver():
    """Set up the Selenium web driver with options."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run headless (no GUI)
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    service = Service(CHROME_DRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver


def search_website(driver, entity_code):
    """
    Search for the school's website using the MI School Data Education Map.

    Parameters:
        driver: Selenium WebDriver instance.
        entity_code (str): The entity code for the school.

    Returns:
        str: The website URL if found, otherwise None.
    """
    try:
        # Navigate to the MI School Data Education Map page
        driver.get("https://mischooldata.org/education-map/")

        # Wait for the search box to be available and enter the entity code
        wait = WebDriverWait(driver, 10)
        search_box = wait.until(
            EC.presence_of_element_located((By.ID, "insertMapSearch"))
        )
        search_box.clear()
        search_box.send_keys(entity_code)
        search_box.send_keys(Keys.RETURN)

        # Wait for the 'map-info-container' to be present and visible
        info_container = wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "map-info-container"))
        )

        # Find all divs with class 'row' inside 'map-info-container'
        row_divs = info_container.find_elements(By.CLASS_NAME, "row")

        # Ensure there are at least two 'row' divs as expected
        if len(row_divs) < 2:
            print(
                f"Warning: Expected at least 2 'row' divs for entity code {entity_code}, but found {len(row_divs)}."
            )
            return None

        # Access the second 'row' div
        second_row_div = row_divs[1]

        # Find the div with class 'col-md-12' inside the second 'row' div
        col_div = second_row_div.find_element(By.CLASS_NAME, "col-md-12")

        # Find the first div inside 'col-md-12'
        first_div = col_div.find_element(By.XPATH, "./div[1]")

        # Find the <a> tag containing the website link
        website_element = first_div.find_element(By.TAG_NAME, "a")
        return website_element.get_attribute("href")

    except Exception as e:
        print(f"Error finding website for entity code {entity_code}: {e}")
    return None

    """
    Search for the school's website using the MI School Data Education Map.
    
    Parameters:
        driver: Selenium WebDriver instance.
        entity_code (str): The entity code for the school.
    
    Returns:
        str: The website URL if found, otherwise None.
    """
    try:
        # Navigate to the MI School Data Education Map page
        driver.get("https://mischooldata.org/education-map/")

        # Wait for the search box to be available and enter the entity code
        wait = WebDriverWait(driver, 10)
        search_box = wait.until(
            EC.presence_of_element_located((By.ID, "insertMapSearch"))
        )
        search_box.clear()
        search_box.send_keys(entity_code)
        search_box.send_keys(Keys.RETURN)

        # Wait for the 'map-info-container' to be present and visible
        info_container = wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "map-info-container"))
        )

        # Find all divs with class 'row' inside 'map-info-container'
        row_divs = info_container.find_elements(By.CLASS_NAME, "row")[1]

        # Check if there are any 'row' divs
        if len(row_divs) == 0:
            print(
                f"Warning: No 'row' divs found for entity code {entity_code}. Retrying with an alternative approach."
            )
            # Alternative approach: check for links directly in 'map-info-container'
            website_element = info_container.find_elements(By.TAG_NAME, "a")
            if website_element:
                return website_element[0].get_attribute("href")
            else:
                print(
                    f"No website link found directly in 'map-info-container' for entity code {entity_code}."
                )
                return None

        # Find the <a> tag containing the website link in the second 'row' div
        if len(row_divs) >= 2:
            website_element = row_divs[1].find_element(By.TAG_NAME, "a")
            return website_element.get_attribute("href")
        else:
            print(
                f"Warning: Expected at least 2 'row' divs for entity code {entity_code}, but found {len(row_divs)}."
            )
            return None

    except Exception as e:
        print(f"Error finding website for entity code {entity_code}: {e}")
    return None


def find_logo(url):
    """
    Find the logo image on the school's website.

    Parameters:
        url (str): The school's website URL.

    Returns:
        str: The logo image URL if found, otherwise None.
    """
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        logo = (
            soup.find("img", {"alt": "logo"})
            or soup.find("img", {"class": "logo"})
            or soup.find("img", src=True)
        )
        if logo:
            logo_url = logo["src"]
            if not logo_url.startswith("http"):
                logo_url = requests.compat.urljoin(url, logo_url)
            return logo_url
    except Exception as e:
        print(f"Error finding logo on {url}: {e}")
    return None


def download_image(url, save_path):
    """
    Download the image from the given URL and save it as a PNG.

    Parameters:
        url (str): The URL of the image to download.
        save_path (str): The local path where the image will be saved.
    """
    try:
        response = requests.get(url)
        image = Image.open(BytesIO(response.content))
        image.save(save_path, "PNG")
    except Exception as e:
        print(f"Error downloading image from {url}: {e}")


def process_schools(input_csv, output_csv):
    """
    Process each school in the CSV and save logos while updating the CSV file.

    Parameters:
        input_csv (str): The path to the input CSV file containing school names and entity codes.
        output_csv (str): The path to the output CSV file that will include the school name, entity code, and website information.
    """
    # Read the CSV file and ensure 'Entity Code' is treated as a string
    df = pd.read_csv(input_csv, dtype={"Entity Code": str})

    # Ensure entity codes are formatted with leading zeros to be exactly 5 digits
    df["Entity Code"] = df["Entity Code"].apply(lambda x: x.zfill(5))

    # Add a new column for storing the website URLs
    df["Website"] = ""

    # Set up the Selenium driver
    driver = setup_driver()

    for index, row in df.iterrows():
        school_name = row["School Name"].strip()
        entity_code = row["Entity Code"].strip()

        # Search for the school's website using the entity code
        website = search_website(driver, entity_code)
        if website:
            df.at[index, "Website"] = website
            print(f"Found website for {school_name}: {website}")

            # Find the logo on the website
            logo_url = find_logo(website)
            if logo_url:
                print(f"Found logo for {school_name}: {logo_url}")

                # Save the logo as PNG
                formatted_name = "_".join(school_name.split())
                logo_path = os.path.join(LOGO_DIR, f"{formatted_name}.png")
                download_image(logo_url, logo_path)
            else:
                print(f"No logo found for {school_name}")
        else:
            print(f"No website found for {school_name}")

    # Save the updated CSV with the school name, entity code, and website information
    df.to_csv(output_csv, index=False)
    print(f"Updated CSV saved as {output_csv}")

    # Close the Selenium driver
    driver.quit()


# Run the program
input_csv = "schools.csv"  # Input CSV file path
output_csv = "schools_with_websites.csv"  # Output CSV file path
process_schools(input_csv, output_csv)

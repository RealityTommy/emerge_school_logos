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
import re
from tqdm import tqdm

# Set up the paths based on environment variables
OUTPUT_BASE_PATH = os.getenv(
    "OUTPUT_DIR_PATH"
)  # Set this environment variable to the desired base path for output
OUTPUT_DIR = os.path.join(OUTPUT_BASE_PATH, "output")
LOGO_DIR = os.path.join(OUTPUT_DIR, "logos")
INPUT_DIR = "input"

# Ensure the output and logos directories exist
if not os.path.exists(LOGO_DIR):
    os.makedirs(LOGO_DIR)

# Path to your ChromeDriver from an environment variable
CHROME_DRIVER_PATH = os.getenv(
    "CHROME_DRIVER_PATH"
)  # Set this environment variable to the ChromeDriver path


def setup_driver():
    """Set up the Selenium web driver with options."""
    chrome_options = Options()
    chrome_options.add_argument(
        "--headless"
    )  # Comment out this line to see the browser while debugging
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
        driver.get("https://mischooldata.org/education-map/")
        wait = WebDriverWait(driver, 10)

        search_box = wait.until(
            EC.presence_of_element_located((By.ID, "insertMapSearch"))
        )
        search_box.clear()
        search_box.send_keys(entity_code)
        search_box.send_keys(Keys.RETURN)

        info_container = wait.until(
            EC.visibility_of_element_located((By.CLASS_NAME, "map-info-container"))
        )

        try:
            website_element = driver.find_element(
                By.XPATH,
                "/html/body/div[1]/div[3]/div[2]/div/div/div[1]/div/div[3]/div[2]/div[1]/div[1]/a",
            )
            return website_element.get_attribute("href")
        except Exception as e:
            print(
                f"Unable to find website link using the specified XPath for entity code {entity_code}: {e}"
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
        output_csv (str): The path to the output CSV file that will include the school name, entity code, website, and logo status.
    """
    df = pd.read_csv(input_csv, dtype={"Entity Code": str})

    df["Entity Code"] = df["Entity Code"].apply(lambda x: x.zfill(5))

    df["Website"] = ""
    df["Logo Status"] = ""

    driver = setup_driver()

    for index, row in tqdm(df.iterrows(), total=df.shape[0], desc="Processing schools"):
        school_name = row["School Name"].strip()
        entity_code = row["Entity Code"].strip()

        website = search_website(driver, entity_code)
        if website:
            df.at[index, "Website"] = website
            print(f"Found website for {school_name}: {website}")

            logo_url = find_logo(website)
            if logo_url:
                print(f"Found logo for {school_name}: {logo_url}")

                formatted_name = re.sub(
                    r"[^a-z0-9]+", "-", "_".join(school_name.split()).lower()
                )
                logo_path = os.path.join(LOGO_DIR, f"{formatted_name}.png")

                if not os.path.exists(logo_path):
                    download_image(logo_url, logo_path)
                    df.at[index, "Logo Status"] = "Found"
                else:
                    print(f"Logo for {school_name} already exists. Skipping download.")
                    df.at[index, "Logo Status"] = "Already Exists"
            else:
                print(f"No logo found for {school_name}")
                df.at[index, "Logo Status"] = "Not Found"
        else:
            print(f"No website found for {school_name}")
            df.at[index, "Website"] = ""
            df.at[index, "Logo Status"] = "No Website"

    output_csv_path = os.path.join(OUTPUT_DIR, output_csv)
    df.to_csv(output_csv_path, index=False)
    print(f"Updated CSV saved as {output_csv_path}")

    driver.quit()


# Example usage
input_csv = os.path.join(INPUT_DIR, "schools_input.csv")
output_csv = "schools_output.csv"
process_schools(input_csv, output_csv)

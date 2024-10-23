import os
import requests
import pandas as pd
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
from googleapiclient.discovery import build

# Load the API key and Search Engine ID from environment variables
API_KEY = os.getenv('GOOGLE_API_KEY')  # Make sure to set this environment variable
CX = os.getenv('SEARCH_ENGINE_ID')  # Make sure to set this environment variable

# Directory to save logos
LOGO_DIR = 'logos'
if not os.path.exists(LOGO_DIR):
    os.makedirs(LOGO_DIR)

def search_website(school_name, address):
    """
    Search for the school's website using Google Custom Search API.
    
    Parameters:
        school_name (str): The name of the school district.
        address (str): The address of the school district.

    Returns:
        str: The website URL if found, otherwise None.
    """
    # Initialize the Google Custom Search API service
    service = build("customsearch", "v1", developerKey=API_KEY)
    
    # Combine the school name and address into a search query
    query = f"{school_name} {address}"
    
    try:
        # Execute the search query
        res = service.cse().list(q=query, cx=CX).execute()
        
        # Loop through search results to find a suitable link
        for item in res.get('items', []):
            link = item['link']
            # Look for educational domains like ".edu" or "k12" to filter school websites
            if "edu" in link or "k12" in link:
                return link
    except Exception as e:
        print(f"Error searching for {school_name}: {e}")
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
        # Send a request to the school's website
        response = requests.get(url)
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Search for common patterns that logos use (e.g., <img> tags with 'logo' class or alt attribute)
        logo = soup.find('img', {'alt': 'logo'}) or soup.find('img', {'class': 'logo'}) or soup.find('img', src=True)
        
        if logo:
            logo_url = logo['src']
            # Make sure the URL is absolute (full URL)
            if not logo_url.startswith('http'):
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
        # Send a request to download the image
        response = requests.get(url)
        # Open the image using PIL (Python Imaging Library)
        image = Image.open(BytesIO(response.content))
        # Save the image in PNG format
        image.save(save_path, 'PNG')
    except Exception as e:
        print(f"Error downloading image from {url}: {e}")

def process_schools(input_csv, output_csv):
    """
    Process each school in the CSV and save logos while updating the CSV file.
    
    Parameters:
        input_csv (str): The path to the input CSV file containing school names and addresses.
        output_csv (str): The path to the output CSV file that will include the website information.
    """
    # Read the CSV file into a DataFrame using pandas
    df = pd.read_csv(input_csv)
    # Add a new column for storing the website URLs
    df['Website'] = ''  

    # Loop through each row in the DataFrame
    for index, row in df.iterrows():
        school_name = row['School Name'].strip()  # Get the school name
        address = row['Address'].strip()  # Get the address

        # Format the school name to be used as a file name (e.g., replace spaces with underscores)
        formatted_name = '_'.join(school_name.split())

        # Search for the school's website using the API
        website = search_website(school_name, address)
        if website:
            # Update the DataFrame with the found website
            df.at[index, 'Website'] = website
            print(f"Found website for {school_name}: {website}")

            # Try to find the logo on the website
            logo_url = find_logo(website)
            if logo_url:
                print(f"Found logo for {school_name}: {logo_url}")

                # Save the logo image as PNG with the school's formatted name
                logo_path = os.path.join(LOGO_DIR, f"{formatted_name}.png")
                download_image(logo_url, logo_path)
            else:
                print(f"No logo found for {school_name}")
        else:
            print(f"No website found for {school_name}")

    # Save the updated DataFrame as a new CSV file
    df.to_csv(output_csv, index=False)
    print(f"Updated CSV saved as {output_csv}")

# Run the program
input_csv = 'schools.csv'  # Input CSV file path
output_csv = 'schools_with_websites.csv'  # Output CSV file path
process_schools(input_csv, output_csv)

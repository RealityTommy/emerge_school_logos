# School Logo Scraper

This Python program takes a CSV file containing school district names and addresses, searches the internet for each school’s website using the Google Custom Search API, finds the school’s logo, and saves it as a PNG file. The program also updates the CSV file to include the school’s website.

## Features
- Searches for each school’s official website based on its name and address.
- Scrapes the website to find the school’s logo.
- Saves the logo image as a PNG file in a specified directory.
- Updates the CSV file with the found website URLs.

## Requirements
Before running the program, ensure you have the following Python libraries installed:
- `requests`
- `beautifulsoup4`
- `pandas`
- `google-api-python-client`
- `Pillow`

You can install these libraries using pip:

```bash
pip install requests beautifulsoup4 pandas google-api-python-client Pillow
```

## Setup
1. **API Setup**:
   - Set up the Google Custom Search API by creating a project in the [Google Cloud Console](https://console.cloud.google.com/).
   - Enable the **Custom Search API**.
   - Generate an **API Key**.
   - Create a **Custom Search Engine** [here](https://cse.google.com/) and restrict it to educational domains (like `.edu` or `k12` if applicable). Copy the **Search Engine ID**.

2. **Set Environment Variables**:
   - Set the following environment variables with your API Key and Search Engine ID:
     - `GOOGLE_API_KEY`: Your API Key from Google Custom Search.
     - `SEARCH_ENGINE_ID`: Your Custom Search Engine ID.
   
   - On **Windows**:
     ```bash
     set GOOGLE_API_KEY=your_api_key
     set SEARCH_ENGINE_ID=your_search_engine_id
     ```
   - On **Mac/Linux**:
     ```bash
     export GOOGLE_API_KEY=your_api_key
     export SEARCH_ENGINE_ID=your_search_engine_id
     ```

## Usage
1. Prepare your CSV file with the following columns:
   - **School Name**: The name of the school district.
   - **Address**: The address of the school district.

   You can use the provided template CSV file (`schools_template.csv`) as a starting point.

2. Run the program by executing the Python script:
   ```bash
   python school_logo_scraper.py
   ```

3. The program will:
   - Read the input CSV file.
   - Search for each school’s website.
   - Scrape the website for the school logo.
   - Save the logo as a PNG in the `logos` directory.
   - Update the CSV file to include the website URL for each school.

4. The output CSV file (`schools_with_websites.csv`) will be saved in the same directory, containing the original information plus a new column for the website.

## Files
- **school_logo_scraper.py**: The main Python script that processes the CSV file and saves logos.
- **schools_template.csv**: A template CSV file you can use to input school names and addresses.
- **logos/**: A directory where the program saves the logos as PNG files.

## Troubleshooting
- **API Quota Limit**: Ensure you have sufficient quota for Google’s Custom Search API. The free tier has a limited number of searches per day.
- **Logo Not Found**: The program uses common patterns (like `<img>` tags with specific classes or attributes) to locate logos. If the logo is not found, it may be due to a different HTML structure on the school’s website.

## Dependencies
- Python 3.x
- Google Custom Search API access

## Notes
- Make sure to keep your API Key secure and not expose it in public code repositories.
- The program includes error handling to continue processing even if errors occur (e.g., if a school website or logo is not found).

## License
This project is licensed under the MIT License - see the LICENSE file for details.
```

### Explanation:
- The `README.md` explains the purpose of the program, setup instructions, usage, and troubleshooting tips.
- It provides a step-by-step guide on setting up the environment variables and running the script.
- Additional information about dependencies and file organization is included to help users understand the program's structure.

Feel free to adjust the file based on your preferences or further customizations!
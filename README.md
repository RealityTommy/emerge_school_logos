# School Logo Scraper

This Python program takes a CSV file containing school district names and their entity codes, searches the MI School Data Education Map for each school’s website, finds the school’s logo, and saves it as a PNG file. The program also updates the CSV file to include the school’s website.

## Features
- Searches for each school’s official website based on its entity code using MI School Data's Education Map.
- Scrapes the school’s homepage for a logo and saves it as a PNG.
- Updates the CSV file to include the school’s website.

## Requirements
Before running the program, ensure you have the following Python libraries installed:
- `pandas`
- `requests`
- `beautifulsoup4`
- `selenium`
- `pillow`

You can install these libraries using pip:

```bash
pip install pandas requests beautifulsoup4 selenium pillow
```

Additionally, you need to download [ChromeDriver](https://chromedriver.chromium.org/downloads) and ensure it's in your PATH or specify its location in the script.

## Setup
1. **Web Driver Setup**:
   - Download the appropriate version of ChromeDriver that matches your Chrome browser version.
   - Place it in a directory and update the `CHROME_DRIVER_PATH` variable in the script with the correct path.

2. **Input CSV File**:
   - Prepare your CSV file with the following columns:
     - **School Name**: The name of the school district.
     - **Entity Code**: The entity code of the school.

   You can use the provided template CSV file (`schools_template_updated.csv`) as a starting point.

3. **Environment Configuration**:
   - Make sure your environment has ChromeDriver installed and the location set correctly in the script.
   
## Usage
1. Ensure your input CSV file (`schools.csv`) has the correct format (School Name and Entity Code columns).
2. Run the program by executing the Python script:
   ```bash
   python school_logo_scraper.py
   ```

3. The program will:
   - Read the input CSV file.
   - Search MI School Data Education Map for each school’s website using the entity code.
   - Scrape the website for the school logo.
   - Save the logo as a PNG in the `logos` directory.
   - Update the CSV file to include the school name, entity code, and website.

4. The output CSV file (`schools_with_websites.csv`) will be saved in the same directory, containing the updated information.

## Files
- **school_logo_scraper.py**: The main Python script that processes the CSV file and saves logos.
- **schools_template_updated.csv**: A template CSV file you can use to input school names and entity codes.
- **logos/**: A directory where the program saves the logos as PNG files.

## Troubleshooting
- **Class Names or XPath Issues**: If the program fails to locate elements on the MI School Data website, inspect the elements using the browser’s developer tools (`F12`) and adjust the class names or XPaths in the script accordingly.
- **WebDriver Errors**: Ensure that ChromeDriver matches the version of Chrome installed on your system and that the path is correctly set in the script.
- **Connection Issues**: If the website loads slowly, you may need to increase the waiting time (`WebDriverWait`) in the script.

## Dependencies
- Python 3.x
- ChromeDriver installed and configured in your PATH or specified in the script.

## Notes
- This program uses web scraping with Selenium; it may need updates if the MI School Data website changes its structure or element IDs/classes.
- Always ensure that your ChromeDriver version matches your Chrome browser version.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
```

### Summary of Changes
- Updated the program details to reflect the use of MI School Data Education Map for retrieving school websites based on entity codes.
- Modified the CSV structure and instructions to align with the new input format (school name and entity code).
- Added troubleshooting tips specific to Selenium and web scraping.
- Provided instructions on setting up and configuring ChromeDriver.

This `README.md` file should now accurately guide users in setting up and running the updated program. Let me know if you need further adjustments!
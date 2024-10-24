# School Website and Logo Scraper

This project is a Python application that uses Selenium and BeautifulSoup to search for school websites using their entity codes from the MI School Data Education Map and attempts to find and download the school's logo from their website. The program outputs a CSV file that includes information about the school, the website, and the logo status.

## Table of Contents
- [Requirements](#requirements)
- [Setup](#setup)
- [Usage](#usage)
- [Input CSV Format](#input-csv-format)
- [Output CSV Format](#output-csv-format)
- [Troubleshooting](#troubleshooting)
- [Notes](#notes)

## Requirements

Ensure you have the following Python packages installed:

- `pandas`
- `selenium`
- `beautifulsoup4`
- `requests`
- `Pillow`

You can install these dependencies using:

```bash
pip install pandas selenium beautifulsoup4 requests Pillow
```

### Additional Requirements

- **Google Chrome**: The program uses ChromeDriver, so Google Chrome must be installed.
- **ChromeDriver**: Download the ChromeDriver matching your Chrome version from [ChromeDriver Download](https://chromedriver.chromium.org/downloads) and set the `CHROME_DRIVER_PATH` environment variable to the path of the ChromeDriver executable.

## Setup

1. **Download and Set Up ChromeDriver**:
   - Download ChromeDriver matching your Chrome version.
   - Move the `chromedriver` file to a known location (e.g., `/usr/local/bin/`).
   - Set the environment variable for `CHROME_DRIVER_PATH`:
     ```bash
     export CHROME_DRIVER_PATH=/path/to/chromedriver
     ```

2. **Directory for Logos**:
   - The program saves logos in a directory called `logos`. Ensure that this directory exists in the same location as the script, or it will be created automatically.

## Usage

Run the program with the following command:

```bash
python main.py
```

Make sure to adjust the file paths in `main.py` to point to your input and output CSV files.

## Input CSV Format

The input CSV file should have the following columns:

| School Name           | Entity Code |
|-----------------------|-------------|
| Example High School   | 03535       |
| Another School        | 12345       |
| Sample Elementary     | 67890       |

- **School Name**: The name of the school.
- **Entity Code**: The 5-digit entity code for the school (leading zeros must be included).

## Output CSV Format

The output CSV file will have the following columns:

| School Name           | Entity Code | Website                       | Logo Status   |
|-----------------------|-------------|------------------------------|---------------|
| Example High School   | 03535       | https://examplehigh.edu      | Found         |
| Another School        | 12345       | https://anotherschool.org    | Not Found     |
| Sample Elementary     | 67890       |                              | No Website    |

- **Website**: The URL of the school's website (left empty if no website is found).
- **Logo Status**:
  - `"Found"`: If a logo is successfully located and downloaded.
  - `"Not Found"`: If a school’s website is found, but no logo is detected.
  - `"No Website"`: If no website is found for the school.

## Troubleshooting

- **Website not found**: If the program cannot find a website, ensure that the entity code is correct and that the MI School Data site is accessible.
- **Logo not found**: Not all websites have a clear pattern for logo identification. You may need to inspect the website manually if logos are frequently missed.
- **ChromeDriver Issues**: Ensure the ChromeDriver version matches your Google Chrome version and the `CHROME_DRIVER_PATH` is correctly set.

## Notes

- **Running the program in non-headless mode**: For debugging, you can run the program with a visible browser by commenting out the `"--headless"` option in the `setup_driver` function.
- **Rate Limiting**: Be mindful of accessing the MI School Data site too frequently, as excessive requests might lead to temporary IP bans.
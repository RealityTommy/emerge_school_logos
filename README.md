# School Logo Scraper

This Python program scrapes the MI School Data website to find school websites and download their logos. The program uses Selenium, BeautifulSoup, and requests to automate this process.

## Project Structure

```
project-directory/
│
├── input/
│   └── schools.csv         # Your input CSV file should be placed here
│
├── output/
│   ├── logos/              # This directory will contain downloaded logos
│   └── schools_with_websites.csv  # Output CSV with processed data
│
├── app/
│   └── main.py             # The main script to run the program
│
├── requirements.txt
├── README.md
└── .gitignore
```

## Setup Instructions

### Prerequisites

- Python 3.7+
- `pip` (Python package manager)
- Chrome browser and [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/)

### Installation

1. **Clone the repository**:

   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. **Set up a virtual environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

### Configuration

1. **Set Environment Variables**:
   
   - `OUTPUT_DIR_PATH`: The base directory for the output and logos (e.g., `/path/to/project/output`).
   - `CHROME_DRIVER_PATH`: Path to your ChromeDriver executable (e.g., `/path/to/chromedriver`).

   Example (Linux/macOS):

   ```bash
   export OUTPUT_DIR_PATH="/path/to/project/output"
   export CHROME_DRIVER_PATH="/path/to/chromedriver"
   ```

   Example (Windows):

   ```bash
   set OUTPUT_DIR_PATH="C:\path\to\project\output"
   set CHROME_DRIVER_PATH="C:\path\to\chromedriver.exe"
   ```

2. **Place your input CSV**:

   - Add your input CSV file (`schools.csv`) to the `input` directory.
   - The file should contain columns for "School Name" and "Entity Code".

### Usage

Run the program:

```bash
python main.py
```

- The program will process the input CSV, search for school websites, and download logos to the `output/logos` directory.
- The output CSV file (`schools_with_websites.csv`) will be saved in the `output` directory.

### Notes

- Ensure the ChromeDriver version matches your installed version of Chrome.
- The input CSV file should be correctly formatted and located in the `input` directory.

### Dependencies

- `Selenium`
- `requests`
- `pandas`
- `tqdm`
- `PIL (Pillow)`

### Troubleshooting

1. **Input CSV Not Found**:
   - Make sure the file is located in the `input` directory and is named correctly (e.g., `schools.csv`).

2. **WebDriver Errors**:
   - Ensure `CHROME_DRIVER_PATH` points to the correct ChromeDriver executable compatible with your Chrome version.

3. **Permissions Errors**:
   - Ensure that the script has permission to read and write files in the `input` and `output` directories.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.
# School Website Logo Scraper

This Python program scrapes the MI School Data website to find school websites and download their logos. The program uses Selenium, BeautifulSoup, and requests to automate this process. It provides real-time statistics, including the number of successes and failures and the time taken for each operation.

## Project Structure

```
project-directory/
│
├── input/
│   └── schools_input.csv   # Your input CSV file should be placed here
│
├── output/
│   ├── logos/              # This directory will contain downloaded logos
│   └── schools_output.csv  # Output CSV with processed data
│
├── main.py                 # The main script to run the program
├── .gitignore
└── README.md
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

   - Add your input CSV file (`schools_input.csv`) to the `input` directory.
   - The file should contain columns for "School Name" and "Entity Code".

### Usage

Run the program:

```bash
python main.py
```

- The program will process the input CSV, search for school websites, and download logos to the `output/logos` directory.
- The output CSV file (`schools_output.csv`) will be saved in the `output` directory.

### Program Features

- **Progress Bar**: Displays the progress as schools are processed.
- **Ongoing Stats**: Shows real-time counts of successes and failures.
- **Time Tracking**: Displays the time taken for each school and the total elapsed time since the program started.

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
   - Make sure the file is located in the `input` directory and is named correctly (e.g., `schools_input.csv`).

2. **WebDriver Errors**:
   - Ensure `CHROME_DRIVER_PATH` points to the correct ChromeDriver executable compatible with your Chrome version.

3. **Permissions Errors**:
   - Ensure that the script has permission to read and write files in the `input` and `output` directories.

4. **Slow Operations**:
   - The program sets a timeout for each operation (searching for the website and downloading the logo). If an operation exceeds the set timeout, it will move on to the next school.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.
# Government Website Scraper

This project is a web scraper designed to recursively scrape all government websites under the `.gov.bd` domain, starting from a specified root website. The scraper collects unique main website links and saves them in a SQLite database.

## Project Structure

```
govbd-scraper
├── src
│   ├── site_scrape.py   # Main logic for scraping government websites
│   └── db.py            # Database connection and operations
├── requirements.txt      # Project dependencies
└── README.md             # Project documentation
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd govbd-scraper
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Open `src/site_scrape.py` and set the `root_url` variable to the desired starting point for scraping (e.g., `https://www.mygov.bd/`).

2. Run the scraper:
   ```
   python src/site_scrape.py
   ```

3. After the scraping is completed, the unique URLs will be printed to the console and saved in the `gov_websites.db` SQLite database.

## Dependencies

This project requires the following Python libraries:
- `requests`
- `beautifulsoup4`
- `sqlite3` (included with Python standard library)

## Additional Information

- The scraper checks if a URL belongs to the `.gov.bd` domain before saving it to the database.
- It uses a recursive approach to follow links found on the pages it scrapes.
- Ensure that you comply with the website's `robots.txt` file and scraping policies before running the scraper.
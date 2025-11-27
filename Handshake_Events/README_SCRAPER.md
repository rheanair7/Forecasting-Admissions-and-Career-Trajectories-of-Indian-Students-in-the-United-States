# Handshake Employer and Jobs Scraper

A Python web scraper to extract employer information and job postings from ASU's Handshake platform.

## Features

- Scrapes employer details (name, industry, location, size, followers, etc.)
- Extracts job postings for each employer (title, salary, type, location, posted date)
- Handles pagination automatically
- Saves data in structured JSON format
- Configurable page ranges
- Logging for monitoring progress
- Error handling and retry logic

## Prerequisites

1. Python 3.7 or higher
2. Chrome browser installed
3. ChromeDriver (will be managed automatically by Selenium)

## Installation

1. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

Run the scraper with default settings (scrapes first 5 pages):
```bash
python scrape_handshake.py
```

### Customization

Edit the `main()` function in `scrape_handshake.py` to customize:

**Scrape all pages:**
```python
scraper.scrape_all()
```

**Scrape specific page range:**
```python
scraper.scrape_all(start_page=1, end_page=10)
```

**Scrape limited number of pages:**
```python
scraper.scrape_all(start_page=1, max_pages=5)
```

**Run in headless mode (no browser window):**
```python
scraper = HandshakeScraper(headless=True)
```

## Output

The scraper generates a JSON file named `handshake_employers_data.json` with the following structure:

```json
{
  "total_employers": 125,
  "total_jobs": 487,
  "scraped_at": "2025-11-25 14:30:00",
  "employers": [
    {
      "name": "Handshake AI",
      "link": "https://asu.joinhandshake.com/e/999894",
      "industry": "Internet & Software",
      "followers": "5.63K followers",
      "location": "San Francisco, CA",
      "size": "250-1,000 employees",
      "type": "Private",
      "total_jobs": 4,
      "jobs": [
        {
          "title": "AI Trainer (No experience required)",
          "employer": "Handshake AI",
          "salary": "$17/hr",
          "type": "Part-time job",
          "location": "United States (Remote)",
          "posted_date": "1 week ago",
          "link": ""
        }
      ]
    }
  ]
}
```

## Important Notes

### Authentication

**IMPORTANT:** This script assumes you're already logged into Handshake. You'll need to:

1. Log in to your ASU Handshake account manually in Chrome
2. The scraper uses the same Chrome session

OR

Modify the script to handle authentication:
- Add login credentials
- Implement login flow before scraping

### Rate Limiting

The script includes delays between requests to avoid rate limiting:
- 2 seconds between employer pages
- 2 seconds after navigating to employer detail pages

You may need to adjust these delays based on your network speed and Handshake's rate limits.

### Session Management

If you encounter authentication issues, you can save and reuse cookies:

```python
# After manual login, save cookies
import pickle
pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))

# Load cookies in scraper
cookies = pickle.load(open("cookies.pkl", "rb"))
for cookie in cookies:
    driver.add_cookie(cookie)
```

## Error Handling

The script handles common errors:
- Timeout exceptions
- Missing elements
- Page load failures
- Keyboard interrupts (saves data before exit)

Check the console logs for detailed error messages.

## Troubleshooting

### ChromeDriver Issues
If you get ChromeDriver errors:
```bash
pip install --upgrade selenium
```

### Timeout Errors
Increase wait times in the script:
```python
self.wait = WebDriverWait(self.driver, 20)  # Increase from 10 to 20
```

### Missing Elements
Some employers may not have all fields. The scraper handles missing data gracefully and logs warnings.

## Legal and Ethical Considerations

- Respect Handshake's Terms of Service
- Use reasonable rate limits
- Only scrape data you have permission to access
- Don't overload the server with requests
- This tool is for educational/research purposes

## Performance

- Scraping speed: ~25 employers per page, ~30-60 seconds per page
- Memory usage: Moderate (stores all data in memory before saving)
- For large scrapes (100+ pages), consider implementing batch saving

## Customization

### Change CSS Selectors
If Handshake updates their UI, update the CSS selectors in:
- `extract_employer_info()`
- `extract_job_info()`

### Add More Data Fields
Extend the extraction methods to capture additional information like:
- Company descriptions
- Benefits
- Required skills
- Application deadlines

## License

This script is provided as-is for educational purposes.

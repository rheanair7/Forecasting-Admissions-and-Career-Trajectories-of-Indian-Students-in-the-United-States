#!/usr/bin/env python3
"""
Handshake Employer List Scraper - Optimized Version
Scrapes employer information directly from search result cards
Efficiently scrapes all 400 pages (~10,000 employers) from Colorado Handshake
Extracts: name, industry, followers, location, size, type, and link
"""

import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.options import Options
import logging

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,  # Changed to DEBUG to see debug messages
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class HandshakeScraperFinal:
    def __init__(self, headless=False):
        """Initialize the scraper with Chrome driver"""
        chrome_options = Options()
        if headless:
            chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

        self.driver = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.driver, 15)
        self.base_url = "https://colorado.joinhandshake.com"
        self.employers_data = []

    def manual_login(self):
        """Open login page and wait for manual login"""
        logger.info("Opening Handshake login page...")
        self.driver.get(self.base_url)

        logger.info("=" * 60)
        logger.info("PLEASE LOG IN MANUALLY IN THE BROWSER WINDOW")
        logger.info("After logging in and seeing the main page, press Enter here...")
        logger.info("=" * 60)

        input("Press Enter after you've logged in...")
        logger.info("Continuing with scraping...")
        time.sleep(2)

    def extract_employer_info_from_card(self, employer_card):
        """Extract employer info directly from the employer card element"""
        try:
            # Extract employer link and all data
            link = ""
            try:
                link_elem = employer_card.find_element(By.CSS_SELECTOR, "a.sc-VJPgA")
                link = link_elem.get_attribute('href')
                if link and not link.startswith('http'):
                    link = self.base_url + link
            except NoSuchElementException:
                try:
                    # Fallback: try any <a> tag with href
                    link_elem = employer_card.find_element(By.CSS_SELECTOR, "a[href*='/e/']")
                    link = link_elem.get_attribute('href')
                    if link and not link.startswith('http'):
                        link = self.base_url + link
                except NoSuchElementException:
                    pass

            # Extract employer name - h3.sc-btuMWg
            name = ""
            try:
                name_elem = employer_card.find_element(By.CSS_SELECTOR, "h3.sc-btuMWg")
                name = name_elem.text.strip()
                # If text is empty, try getting textContent attribute
                if not name:
                    name = name_elem.get_attribute('textContent').strip()
            except NoSuchElementException:
                # Fallback: try any h3
                try:
                    name_elem = employer_card.find_element(By.TAG_NAME, "h3")
                    name = name_elem.text.strip() or name_elem.get_attribute('textContent').strip()
                except NoSuchElementException:
                    pass

            # Extract industry and followers - p.sc-fQkmEp (format: "Industry · X followers")
            industry = ""
            followers = ""
            try:
                info_elem = employer_card.find_element(By.CSS_SELECTOR, "p.sc-fQkmEp")
                info_text = info_elem.text.strip()
                if not info_text:
                    info_text = info_elem.get_attribute('textContent').strip()
                # Format: "Industry · XXX followers"
                if '·' in info_text:
                    parts = info_text.split('·')
                    industry = parts[0].strip()
                    followers = parts[1].strip() if len(parts) > 1 else ""
                else:
                    industry = info_text
            except NoSuchElementException:
                # Fallback: try any p tag
                try:
                    info_elem = employer_card.find_element(By.TAG_NAME, "p")
                    info_text = info_elem.text.strip() or info_elem.get_attribute('textContent').strip()
                    if '·' in info_text:
                        parts = info_text.split('·')
                        industry = parts[0].strip()
                        followers = parts[1].strip() if len(parts) > 1 else ""
                    else:
                        industry = info_text
                except NoSuchElementException:
                    pass

            # Extract location, size, and type using JavaScript
            # This is more reliable than Selenium's element finding methods
            location = ""
            size = ""
            company_type = ""
            try:
                # Use JavaScript to extract all text nodes next to SVG elements
                js_script = """
                var card = arguments[0];
                var results = [];

                // Find all divs with SVG children
                var allDivs = card.querySelectorAll('div');

                for (var i = 0; i < allDivs.length; i++) {
                    var div = allDivs[i];
                    // Check if this div has an SVG as direct child
                    var hasSvg = false;
                    for (var j = 0; j < div.children.length; j++) {
                        if (div.children[j].tagName.toLowerCase() === 'svg') {
                            hasSvg = true;
                            break;
                        }
                    }

                    if (hasSvg) {
                        // Get the text content, excluding nested divs
                        var text = '';
                        for (var k = 0; k < div.childNodes.length; k++) {
                            var node = div.childNodes[k];
                            if (node.nodeType === 3) {  // Text node
                                text += node.textContent;
                            }
                        }
                        text = text.trim();

                        // Only add if not empty and doesn't contain the industry separator
                        if (text && text.indexOf('·') === -1 && text.length < 100) {
                            results.push(text);
                        }
                    }
                }

                return results;
                """

                metadata_texts = self.driver.execute_script(js_script, employer_card)
                logger.debug(f"Found {len(metadata_texts)} metadata fields via JavaScript")

                for text in metadata_texts:
                    logger.debug(f"Metadata text: '{text}'")

                # Now classify each metadata text
                for i, text in enumerate(metadata_texts):
                    logger.debug(f"Processing metadata {i+1}: '{text}'")

                    # Location: Contains comma (e.g., "San Francisco, CA") OR common location words
                    if (',' in text or any(loc_word in text.lower() for loc_word in ['remote', 'united states', 'usa', 'street', 'avenue', 'road', 'city', 'county'])) and not location:
                        location = text
                        logger.debug(f"  -> Identified as location: {location}")
                    # Size: Contains dash or + with numbers (e.g., "250 - 1,000" or "25,000+")
                    elif (('-' in text or '+' in text) and any(char.isdigit() for char in text)) and not size:
                        size = text
                        logger.debug(f"  -> Identified as size: {size}")
                    # Type: Text like "Private", "Public", "Non-Profit", etc.
                    elif not company_type and text.lower() in ['private', 'public', 'non-profit', 'nonprofit', 'government', 'educational', 'public company', 'private company']:
                        company_type = text
                        logger.debug(f"  -> Identified as type: {company_type}")
                    # Fallback: if we haven't found location yet and this doesn't match other patterns
                    elif not location and not any(char.isdigit() for char in text) and '-' not in text and '+' not in text:
                        location = text
                        logger.debug(f"  -> Identified as location (fallback): {location}")
                    # Fallback for type - any text without numbers that we haven't classified
                    elif not company_type and not any(char.isdigit() for char in text) and text not in [location, size]:
                        company_type = text
                        logger.debug(f"  -> Identified as type (fallback): {company_type}")

            except Exception as e:
                logger.error(f"Error extracting location/size/type: {e}")
                import traceback
                logger.debug(traceback.format_exc())

            employer_info = {
                "name": name,
                "link": link,
                "industry": industry,
                "followers": followers,
                "location": location,
                "size": size,
                "type": company_type
            }

            if name:
                logger.info(f"  ✓ Extracted: {name}")
            else:
                logger.warning(f"  ✗ No name found! Link: {link}")
                # Debug: print card HTML snippet
                card_html = employer_card.get_attribute('outerHTML')
                logger.debug(f"Card HTML (first 500 chars): {card_html[:500]}")

            return employer_info

        except Exception as e:
            logger.error(f"Error extracting employer info from card: {e}")
            return None


    def scrape_page(self, page_num):
        """Scrape a single page of employers"""
        url = f"{self.base_url}/employer-search?page={page_num}&per_page=25"
        logger.info(f"\n{'='*60}")
        logger.info(f"Scraping page {page_num}")
        logger.info(f"{'='*60}")

        try:
            self.driver.get(url)
            time.sleep(3)

            # Wait for employer cards - div[data-test="employer-search-employer-card"]
            try:
                self.wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-test='employer-search-employer-card']"))
                )
            except TimeoutException:
                logger.error(f"Could not find any employer cards on page {page_num}")
                return []

            # Get all employer cards
            employer_cards = self.driver.find_elements(By.CSS_SELECTOR, "div[data-test='employer-search-employer-card']")
            logger.info(f"Found {len(employer_cards)} employer cards on page {page_num}")

            if not employer_cards:
                logger.error("No employer cards found!")
                return []

            page_employers = []

            for i, card in enumerate(employer_cards, 1):
                logger.info(f"[{i}/{len(employer_cards)}] Processing employer card...")

                # Extract employer info from card
                employer_info = self.extract_employer_info_from_card(card)

                if employer_info and employer_info['name']:
                    page_employers.append(employer_info)

            logger.info(f"\n✓ Page {page_num} complete: {len(page_employers)} employers scraped")
            return page_employers

        except Exception as e:
            logger.error(f"Error scraping page {page_num}: {e}")
            return []

    def scrape_all(self, start_page=1, end_page=None, max_pages=None):
        """Scrape all pages or a range of pages"""
        try:
            # Navigate to first page
            self.driver.get(f"{self.base_url}/employer-search?page=1&per_page=25")
            time.sleep(5)

            # Determine pages to scrape
            if max_pages:
                end_page = start_page + max_pages - 1
            elif end_page is None:
                end_page = 400  # Default to all 400 pages

            logger.info(f"\n{'='*60}")
            logger.info(f"Starting scrape: Pages {start_page} to {end_page}")
            logger.info(f"Expected total employers: ~{(end_page - start_page + 1) * 25}")
            logger.info(f"{'='*60}\n")

            # Scrape each page
            for page_num in range(start_page, end_page + 1):
                try:
                    page_employers = self.scrape_page(page_num)
                    self.employers_data.extend(page_employers)

                    # Save progress every 10 pages
                    if page_num % 10 == 0:
                        self.save_data(f"handshake_employers_data_progress_page{page_num}.json")
                        logger.info(f"\n💾 Progress saved at page {page_num}")

                    # Add delay between pages to avoid rate limiting
                    if page_num < end_page:
                        time.sleep(2)  # Reduced delay since we're not visiting individual pages

                except Exception as e:
                    logger.error(f"Error on page {page_num}: {e}")
                    # Continue with next page even if one fails
                    continue

            logger.info(f"\n{'='*60}")
            logger.info(f"SCRAPING COMPLETE!")
            logger.info(f"Total employers scraped: {len(self.employers_data)}")
            logger.info(f"{'='*60}\n")

        except KeyboardInterrupt:
            logger.info(f"\n\n⚠️  Scraping interrupted by user at page {page_num}")
            logger.info(f"Scraped {len(self.employers_data)} employers so far")
        except Exception as e:
            logger.error(f"Error during scraping: {e}")
        finally:
            self.save_data()

    def save_data(self, filename="handshake_employers_data.json"):
        """Save scraped data to JSON file"""
        try:
            output_data = {
                "total_employers": len(self.employers_data),
                "scraped_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                "employers": self.employers_data
            }

            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, indent=2, ensure_ascii=False)

            logger.info(f"✓ Data saved to {filename}")
            logger.info(f"  - Total employers: {output_data['total_employers']}")

        except Exception as e:
            logger.error(f"Error saving data: {e}")

    def close(self):
        """Close the browser"""
        self.driver.quit()


def main():
    """Main function to run the scraper"""
    scraper = HandshakeScraperFinal(headless=False)

    try:
        # Prompt for manual login
        scraper.manual_login()

        # Ask user how many pages to scrape
        logger.info("\n" + "="*60)
        logger.info("SCRAPING OPTIONS")
        logger.info("="*60)
        logger.info("Total pages available: 400")
        logger.info("Each page has ~25 employers (~10,000 total)")
        logger.info("To scrape ALL 400 pages, just press Enter")
        logger.info("Or enter a specific number of pages to scrape")
        logger.info("For testing, enter '1' to scrape just the first page")
        logger.info("="*60 + "\n")

        user_input = input("How many pages to scrape? (default: 400 - all pages): ").strip()

        if user_input:
            try:
                max_pages = int(user_input)
                scraper.scrape_all(start_page=1, max_pages=max_pages)
            except ValueError:
                logger.error("Invalid input. Defaulting to all 400 pages.")
                scraper.scrape_all(start_page=1, max_pages=400)
        else:
            # Default: scrape all 400 pages
            logger.info("No input provided. Scraping all 400 pages...")
            scraper.scrape_all(start_page=1, max_pages=400)

    except KeyboardInterrupt:
        logger.info("\n\nScraping interrupted by user")
        scraper.save_data()
    except Exception as e:
        logger.error(f"Error in main: {e}")
    finally:
        scraper.close()


if __name__ == "__main__":
    main()

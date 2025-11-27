#!/usr/bin/env python3
"""
Handshake Employer and Jobs Scraper V2 - Flexible selectors
Scrapes employer information and their job postings from Colorado Handshake
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
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class HandshakeScraperV2:
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

    def extract_employer_info(self, employer_card):
        """Extract employer information from employer card element using flexible selectors"""
        try:
            # Try multiple selectors for employer name
            name = ""
            for selector in ["h3", "h2", "[data-test*='employer-name']"]:
                try:
                    name_elem = employer_card.find_element(By.CSS_SELECTOR, selector)
                    name = name_elem.text.strip()
                    if name:
                        break
                except NoSuchElementException:
                    continue

            if not name:
                logger.warning("Could not find employer name")
                return None

            # Extract employer link
            link = ""
            try:
                link_elem = employer_card.find_element(By.CSS_SELECTOR, "a[href*='/e/']")
                link = link_elem.get_attribute('href')
            except NoSuchElementException:
                try:
                    link_elem = employer_card.find_element(By.CSS_SELECTOR, "a")
                    link = link_elem.get_attribute('href')
                except NoSuchElementException:
                    logger.warning(f"Could not find link for {name}")

            # Extract all text from the card
            card_text = employer_card.text

            # Try to extract industry and followers
            industry = ""
            followers = ""
            location = ""
            size = ""
            company_type = ""

            # Split card text into lines
            lines = [line.strip() for line in card_text.split('\n') if line.strip()]

            for line in lines:
                # Check for followers
                if 'follower' in line.lower():
                    followers = line
                # Check for location (contains comma or state abbreviation)
                elif ',' in line or any(state in line for state in [' CA', ' NY', ' TX', ' CO']):
                    location = line
                # Check for company size
                elif '-' in line and any(char.isdigit() for char in line):
                    size = line
                # Check for company type
                elif line in ['Private', 'Public', 'Nonprofit', 'Government']:
                    company_type = line
                # Check for industry (usually has & or "and")
                elif '&' in line or 'and' in line.lower():
                    industry = line

            employer_info = {
                "name": name,
                "link": link,
                "industry": industry,
                "followers": followers,
                "location": location,
                "size": size,
                "type": company_type,
                "jobs": []
            }

            logger.info(f"Extracted employer: {name}")
            return employer_info

        except Exception as e:
            logger.error(f"Error extracting employer info: {e}")
            return None

    def extract_job_info(self, job_card):
        """Extract job information from job card element"""
        try:
            # Get all text from job card
            card_text = job_card.text
            lines = [line.strip() for line in card_text.split('\n') if line.strip()]

            if len(lines) < 2:
                return None

            # First line is usually the company, second is job title
            # Or first line is title
            employer_name = ""
            title = ""

            # Try to find title
            for selector in ["[id*='title']", "[class*='title']", "div:first-child"]:
                try:
                    title_elem = job_card.find_element(By.CSS_SELECTOR, selector)
                    title = title_elem.text.strip()
                    if title:
                        break
                except:
                    continue

            if not title and len(lines) > 0:
                # Assume first non-empty line is the title
                title = lines[0]

            # Extract employer name
            if len(lines) > 1:
                employer_name = lines[1] if lines[1] != title else lines[0]

            # Extract salary, job type, location, posted date from remaining lines
            salary = ""
            job_type = ""
            location = ""
            posted_date = ""

            for line in lines:
                if '$' in line or '/hr' in line:
                    salary = line
                elif 'time' in line.lower():
                    job_type = line
                elif 'ago' in line.lower() or 'week' in line.lower() or 'month' in line.lower():
                    posted_date = line
                elif 'Remote' in line or ',' in line:
                    location = line

            job_info = {
                "title": title,
                "employer": employer_name,
                "salary": salary,
                "type": job_type,
                "location": location,
                "posted_date": posted_date,
                "link": ""
            }

            logger.info(f"Extracted job: {title}")
            return job_info

        except Exception as e:
            logger.error(f"Error extracting job info: {e}")
            return None

    def scrape_employer_jobs(self, employer_link):
        """Navigate to employer page and scrape job postings"""
        if not employer_link:
            return []

        try:
            logger.info(f"Scraping jobs from: {employer_link}")
            self.driver.get(employer_link)
            time.sleep(3)  # Wait for page load

            # Look for the Jobs tab - try multiple selectors
            try:
                jobs_tab = None
                for selector in [
                    "//button[contains(text(), 'Jobs')]",
                    "//a[contains(text(), 'Jobs')]",
                    "//*[contains(text(), 'Jobs') and (name()='button' or name()='a')]"
                ]:
                    try:
                        jobs_tab = self.wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
                        break
                    except:
                        continue

                if jobs_tab:
                    jobs_tab.click()
                    time.sleep(3)
                else:
                    logger.warning(f"Jobs tab not found for {employer_link}")
                    return []
            except TimeoutException:
                logger.warning(f"Jobs tab not clickable for {employer_link}")
                return []

            # Wait for job cards to load - try multiple selectors
            job_cards = []
            for selector in [
                "div[role='listitem']",
                "div[data-test*='job']",
                "[class*='job'][class*='card']"
            ]:
                try:
                    self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
                    job_cards = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if job_cards:
                        break
                except:
                    continue

            if not job_cards:
                logger.warning(f"No job cards found for {employer_link}")
                return []

            jobs = []
            for card in job_cards:
                job_info = self.extract_job_info(card)
                if job_info and job_info['title']:
                    jobs.append(job_info)

            logger.info(f"Found {len(jobs)} jobs")
            return jobs

        except Exception as e:
            logger.error(f"Error scraping employer jobs: {e}")
            return []

    def scrape_page(self, page_num):
        """Scrape a single page of employers"""
        url = f"{self.base_url}/employer-search?page={page_num}&per_page=25"
        logger.info(f"Scraping page {page_num}: {url}")

        try:
            self.driver.get(url)
            time.sleep(5)  # Wait for dynamic content to load

            # Try multiple selectors for employer cards
            employer_cards = []
            selectors = [
                "div[data-test='employer-search-employer-card']",
                "div[role='listitem']",
                "a[href*='/e/']"
            ]

            for selector in selectors:
                try:
                    self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
                    employer_cards = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if employer_cards:
                        logger.info(f"Found {len(employer_cards)} employers using selector: {selector}")
                        break
                except TimeoutException:
                    continue

            if not employer_cards:
                logger.error(f"Could not find employer cards on page {page_num}")
                # Save page source for debugging
                with open(f'page_{page_num}_debug.html', 'w', encoding='utf-8') as f:
                    f.write(self.driver.page_source)
                logger.error(f"Page source saved to page_{page_num}_debug.html for debugging")
                return []

            page_employers = []

            for i, card in enumerate(employer_cards):
                logger.info(f"Processing employer {i+1}/{len(employer_cards)}")
                employer_info = self.extract_employer_info(card)

                if employer_info:
                    # Scrape jobs for this employer
                    jobs = self.scrape_employer_jobs(employer_info['link'])
                    employer_info['jobs'] = jobs
                    employer_info['total_jobs'] = len(jobs)
                    page_employers.append(employer_info)

                    # Go back to the employer search page
                    self.driver.get(url)
                    time.sleep(3)

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

            # Default to scraping limited pages
            if max_pages:
                end_page = start_page + max_pages - 1
            elif end_page is None:
                end_page = start_page + 4  # Default to 5 pages

            logger.info(f"Scraping pages {start_page} to {end_page}")

            # Scrape each page
            for page_num in range(start_page, end_page + 1):
                logger.info(f"Processing page {page_num}/{end_page}")
                page_employers = self.scrape_page(page_num)
                self.employers_data.extend(page_employers)

                # Add delay between pages to avoid rate limiting
                time.sleep(3)

            logger.info(f"Scraping complete! Total employers: {len(self.employers_data)}")

        except Exception as e:
            logger.error(f"Error during scraping: {e}")
        finally:
            self.save_data()

    def save_data(self, filename="handshake_employers_data.json"):
        """Save scraped data to JSON file"""
        try:
            output_data = {
                "total_employers": len(self.employers_data),
                "total_jobs": sum(emp.get('total_jobs', 0) for emp in self.employers_data),
                "scraped_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                "employers": self.employers_data
            }

            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, indent=2, ensure_ascii=False)

            logger.info(f"Data saved to {filename}")
            logger.info(f"Total employers: {output_data['total_employers']}")
            logger.info(f"Total jobs: {output_data['total_jobs']}")

        except Exception as e:
            logger.error(f"Error saving data: {e}")

    def close(self):
        """Close the browser"""
        self.driver.quit()


def main():
    """Main function to run the scraper"""
    scraper = HandshakeScraperV2(headless=False)

    try:
        # Prompt for manual login
        scraper.manual_login()

        # Scrape first 2 pages as a test
        scraper.scrape_all(start_page=1, max_pages=2)

    except KeyboardInterrupt:
        logger.info("Scraping interrupted by user")
        scraper.save_data()
    except Exception as e:
        logger.error(f"Error in main: {e}")
    finally:
        scraper.close()


if __name__ == "__main__":
    main()

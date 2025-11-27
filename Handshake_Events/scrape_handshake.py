#!/usr/bin/env python3
"""
Handshake Employer and Jobs Scraper
Scrapes employer information and their job postings from ASU Handshake
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


class HandshakeScraper:
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
        self.wait = WebDriverWait(self.driver, 10)
        self.base_url = "https://colorado.joinhandshake.com"
        self.employers_data = []

    def extract_employer_info(self, employer_card):
        """Extract employer information from employer card element"""
        try:
            # Extract employer name
            name_elem = employer_card.find_element(By.CSS_SELECTOR, "h3.sc-dkdNSM")
            name = name_elem.text

            # Extract employer link
            link_elem = employer_card.find_element(By.CSS_SELECTOR, "a.sc-jAzaMR")
            link = link_elem.get_attribute('href')

            # Extract industry and followers
            industry_elem = employer_card.find_element(By.CSS_SELECTOR, "p.sc-csRcV")
            industry_text = industry_elem.text
            industry_parts = industry_text.split('·')
            industry = industry_parts[0].strip() if len(industry_parts) > 0 else ""
            followers = industry_parts[1].strip() if len(industry_parts) > 1 else ""

            # Extract location, company size, and type
            metadata_elems = employer_card.find_elements(By.CSS_SELECTOR, "div.sc-dDVwJj")
            location = ""
            size = ""
            company_type = ""

            for elem in metadata_elems:
                text = elem.text
                if text and "," in text:  # Likely location
                    location = text
                elif text and ("-" in text or "+" in text):  # Likely size
                    size = text
                elif text and text in ["Private", "Public", "Nonprofit"]:
                    company_type = text

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
            # Extract job title
            title_elem = job_card.find_element(By.CSS_SELECTOR, "div.sc-cnOiCc")
            title = title_elem.text

            # Extract employer name
            employer_elem = job_card.find_element(By.CSS_SELECTOR, "span.sc-goETIM")
            employer_name = employer_elem.text

            # Extract salary and job type
            salary = ""
            job_type = ""
            try:
                salary_elem = job_card.find_element(By.CSS_SELECTOR, "p.sc-khsrKC")
                salary = salary_elem.text
            except NoSuchElementException:
                pass

            try:
                job_details = job_card.find_elements(By.CSS_SELECTOR, "div.sc-fSRBKe")
                if job_details:
                    job_type_text = job_details[0].text
                    parts = job_type_text.split('·')
                    job_type = parts[-1].strip() if parts else ""
            except NoSuchElementException:
                pass

            # Extract location and posted date
            location = ""
            posted_date = ""
            try:
                metadata_elem = job_card.find_element(By.CSS_SELECTOR, "div.sc-ktnSBN")
                metadata_text = metadata_elem.text
                parts = metadata_text.split('·')
                if len(parts) >= 2:
                    location = parts[0].strip()
                    posted_date = parts[1].strip()
                elif len(parts) == 1:
                    location = parts[0].strip()
            except NoSuchElementException:
                pass

            # Extract job link
            job_link = ""
            # Note: Job links would need to be clicked to get actual URLs
            # This would require additional interaction with each job card

            job_info = {
                "title": title,
                "employer": employer_name,
                "salary": salary,
                "type": job_type,
                "location": location,
                "posted_date": posted_date,
                "link": job_link
            }

            logger.info(f"Extracted job: {title}")
            return job_info

        except Exception as e:
            logger.error(f"Error extracting job info: {e}")
            return None

    def scrape_employer_jobs(self, employer_link):
        """Navigate to employer page and scrape job postings"""
        try:
            logger.info(f"Scraping jobs from: {employer_link}")
            self.driver.get(employer_link)
            time.sleep(2)  # Wait for page load

            # Look for the Jobs tab and click it
            try:
                jobs_tab = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Jobs')]"))
                )
                jobs_tab.click()
                time.sleep(2)
            except TimeoutException:
                logger.warning(f"Jobs tab not found for {employer_link}")
                return []

            # Wait for job cards to load
            try:
                self.wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div.sc-jVQoqC"))
                )
            except TimeoutException:
                logger.warning(f"No job cards found for {employer_link}")
                return []

            # Extract all job cards
            job_cards = self.driver.find_elements(By.CSS_SELECTOR, "div.sc-jVQoqC.gBpPGL")
            jobs = []

            for card in job_cards:
                job_info = self.extract_job_info(card)
                if job_info:
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
            time.sleep(3)  # Wait for dynamic content to load

            # Wait for employer cards to load
            self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-test='employer-search-employer-card']"))
            )

            # Get all employer cards
            employer_cards = self.driver.find_elements(By.CSS_SELECTOR, "div[data-test='employer-search-employer-card']")
            logger.info(f"Found {len(employer_cards)} employers on page {page_num}")

            page_employers = []

            for card in employer_cards:
                employer_info = self.extract_employer_info(card)
                if employer_info:
                    # Scrape jobs for this employer
                    jobs = self.scrape_employer_jobs(employer_info['link'])
                    employer_info['jobs'] = jobs
                    employer_info['total_jobs'] = len(jobs)
                    page_employers.append(employer_info)

                    # Go back to the employer search page
                    self.driver.get(url)
                    time.sleep(2)

            return page_employers

        except TimeoutException:
            logger.error(f"Timeout waiting for page {page_num} to load")
            return []
        except Exception as e:
            logger.error(f"Error scraping page {page_num}: {e}")
            return []

    def get_total_pages(self):
        """Get total number of pages from pagination"""
        try:
            # Find the last page number in pagination
            last_page_elem = self.driver.find_element(By.CSS_SELECTOR, "a[data-test^='pagination-page-']:last-of-type")
            last_page_text = last_page_elem.text
            return int(last_page_text)
        except Exception as e:
            logger.warning(f"Could not determine total pages: {e}")
            return 400  # Default from the HTML you provided

    def scrape_all(self, start_page=1, end_page=None, max_pages=None):
        """Scrape all pages or a range of pages"""
        try:
            # Navigate to first page to get total pages
            self.driver.get(f"{self.base_url}/employer-search?page=1&per_page=25")
            time.sleep(3)

            total_pages = self.get_total_pages()
            logger.info(f"Total pages available: {total_pages}")

            # Determine pages to scrape
            if max_pages:
                end_page = min(start_page + max_pages - 1, total_pages)
            elif end_page is None:
                end_page = total_pages
            else:
                end_page = min(end_page, total_pages)

            logger.info(f"Scraping pages {start_page} to {end_page}")

            # Scrape each page
            for page_num in range(start_page, end_page + 1):
                logger.info(f"Processing page {page_num}/{end_page}")
                page_employers = self.scrape_page(page_num)
                self.employers_data.extend(page_employers)

                # Add delay between pages to avoid rate limiting
                time.sleep(2)

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
    scraper = HandshakeScraper(headless=False)

    try:
        # Scrape first 5 pages as a test (you can change this)
        # To scrape all pages, use: scraper.scrape_all()
        # To scrape specific range: scraper.scrape_all(start_page=1, end_page=10)
        scraper.scrape_all(start_page=1, max_pages=5)

    except KeyboardInterrupt:
        logger.info("Scraping interrupted by user")
        scraper.save_data()
    except Exception as e:
        logger.error(f"Error in main: {e}")
    finally:
        scraper.close()


if __name__ == "__main__":
    main()

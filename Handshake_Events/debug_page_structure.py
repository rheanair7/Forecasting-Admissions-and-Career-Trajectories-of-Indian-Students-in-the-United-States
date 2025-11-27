#!/usr/bin/env python3
"""
Debug script to inspect the HTML structure of Colorado Handshake
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# Set up Chrome
chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 10)

try:
    print("Opening Colorado Handshake...")
    driver.get("https://colorado.joinhandshake.com")

    print("\n" + "="*60)
    print("PLEASE LOG IN MANUALLY IN THE BROWSER")
    print("After logging in, press Enter here...")
    print("="*60)
    input("Press Enter after login...")

    # Navigate to employer search
    print("\nNavigating to employer search...")
    driver.get("https://colorado.joinhandshake.com/employer-search?page=1&per_page=25")
    time.sleep(5)

    # Save page source
    with open('page_source.html', 'w', encoding='utf-8') as f:
        f.write(driver.page_source)
    print("Page source saved to page_source.html")

    # Try to find employer cards with various selectors
    print("\n" + "="*60)
    print("SEARCHING FOR EMPLOYER CARDS...")
    print("="*60)

    selectors_to_try = [
        ("div[data-test='employer-search-employer-card']", "data-test attribute"),
        ("div[role='listitem']", "role=listitem"),
        ("div[class*='employer']", "class contains 'employer'"),
        ("a[href*='/e/']", "links to employer pages"),
    ]

    for selector, description in selectors_to_try:
        try:
            elements = driver.find_elements(By.CSS_SELECTOR, selector)
            print(f"\n✓ Found {len(elements)} elements with {description}: {selector}")
            if elements and len(elements) > 0:
                print(f"  First element HTML (truncated):")
                html = elements[0].get_attribute('outerHTML')[:500]
                print(f"  {html}...")
        except Exception as e:
            print(f"✗ Failed with {selector}: {e}")

    # Try to find employer names with various selectors
    print("\n" + "="*60)
    print("SEARCHING FOR EMPLOYER NAMES...")
    print("="*60)

    name_selectors = [
        ("h3", "h3 tags"),
        ("h2", "h2 tags"),
        ("[class*='name']", "class contains 'name'"),
        ("[class*='title']", "class contains 'title'"),
    ]

    for selector, description in name_selectors:
        try:
            elements = driver.find_elements(By.CSS_SELECTOR, selector)
            print(f"\n✓ Found {len(elements)} {description}: {selector}")
            if elements and len(elements) > 0:
                print(f"  First 3 text values:")
                for i, elem in enumerate(elements[:3]):
                    text = elem.text.strip()
                    if text:
                        print(f"    {i+1}. {text[:100]}")
        except Exception as e:
            print(f"✗ Failed with {selector}: {e}")

    print("\n" + "="*60)
    print("Check page_source.html to inspect the full HTML structure")
    print("Press Enter to close browser...")
    print("="*60)
    input()

finally:
    driver.quit()

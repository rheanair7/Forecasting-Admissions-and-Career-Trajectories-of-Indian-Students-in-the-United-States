#!/usr/bin/env python3
"""
Debug scraper to see what's actually in the live page
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 15)

print("Opening Handshake...")
driver.get("https://colorado.joinhandshake.com")

print("\n" + "="*60)
print("PLEASE LOG IN MANUALLY")
print("="*60)
input("Press Enter after login...")

print("\nNavigating to employer search page 1...")
driver.get("https://colorado.joinhandshake.com/employer-search?page=1&per_page=25")
time.sleep(5)

# Save current page HTML
with open('live_page_debug.html', 'w', encoding='utf-8') as f:
    f.write(driver.page_source)
print("✓ Saved current page HTML to live_page_debug.html")

# Find employer cards
cards = driver.find_elements(By.CSS_SELECTOR, "div[data-test='employer-search-employer-card']")
print(f"\n✓ Found {len(cards)} employer cards")

if cards:
    print("\n" + "="*60)
    print("Debugging FIRST card:")
    print("="*60)

    first_card = cards[0]

    # Print the entire card HTML
    print("\nCard HTML (first 2000 chars):")
    print(first_card.get_attribute('outerHTML')[:2000])

    print("\n" + "="*60)
    print("Testing selectors on FIRST card:")
    print("="*60)

    # Test each selector
    selectors = {
        'Link': 'a.sc-VJPgA',
        'Name': 'h3.sc-btuMWg',
        'Industry/Followers': 'p.sc-fQkmEp',
        'Info divs': 'div.sc-eRmoUn.sc-irfVpP',
        'All links': 'a',
        'All h3': 'h3',
        'All p': 'p',
        'All divs': 'div'
    }

    for name, selector in selectors.items():
        try:
            elements = first_card.find_elements(By.CSS_SELECTOR, selector)
            print(f"\n{name} ('{selector}'):")
            print(f"  Found: {len(elements)} elements")
            for i, elem in enumerate(elements[:3]):  # Show first 3
                text = elem.text.strip() if elem.text else ''
                if name == 'Link' or name == 'All links':
                    href = elem.get_attribute('href')
                    print(f"    [{i+1}] href={href}, text={text[:50]}")
                else:
                    print(f"    [{i+1}] {text[:100]}")
        except Exception as e:
            print(f"\n{name}: ERROR - {e}")

print("\n" + "="*60)
print("Debug complete! Check live_page_debug.html for full page source")
print("="*60)

input("Press Enter to close browser...")
driver.quit()

#!/usr/bin/env python3
"""
Test the updated CSS selectors against the saved HTML structure
"""

from bs4 import BeautifulSoup

# Read the HTML file
with open('pg_struct.txt', 'r', encoding='utf-8') as f:
    html_content = f.read()

soup = BeautifulSoup(html_content, 'html.parser')

# Find employer cards
cards = soup.find_all('div', attrs={'data-test': 'employer-search-employer-card'})

print(f"Found {len(cards)} employer cards\n")
print("="*80)
print("Testing selectors on all cards:")
print("="*80)

for i, card in enumerate(cards, 1):
    print(f"\n[Card {i}]")

    # Extract link
    link_elem = card.select_one('a.sc-VJPgA')
    link = link_elem.get('href', '') if link_elem else ''
    if link and not link.startswith('http'):
        link = 'https://colorado.joinhandshake.com' + link

    # Extract name
    name_elem = card.select_one('h3.sc-btuMWg')
    name = name_elem.get_text(strip=True) if name_elem else ''

    # Extract industry and followers
    info_elem = card.select_one('p.sc-fQkmEp')
    industry = ""
    followers = ""
    if info_elem:
        info_text = info_elem.get_text(strip=True)
        if '·' in info_text:
            parts = info_text.split('·')
            industry = parts[0].strip()
            followers = parts[1].strip() if len(parts) > 1 else ""
        else:
            industry = info_text

    # Extract location, size, type
    # Order: Location (with comma or state), Size (with dash/numbers/+), Type (text)
    location = ""
    size = ""
    company_type = ""
    info_divs = card.select('div.sc-eRmoUn.sc-irfVpP')

    for div in info_divs:
        div_text = div.get_text(strip=True)
        if not div_text:
            continue

        # Location contains comma (e.g., "San Francisco, CA")
        if ',' in div_text and not location:
            location = div_text
        # Size contains dash or + with numbers (e.g., "250 - 1,000" or "25,000+")
        elif (('-' in div_text or '+' in div_text) and any(char.isdigit() for char in div_text)) and not size:
            size = div_text
        # Type is text like "Private", "Public", "Non-Profit"
        elif not location and not any(char.isdigit() for char in div_text):
            # This might be a location without comma (e.g., "Remote", "United States")
            location = div_text
        elif not company_type and div_text not in [location, size]:
            company_type = div_text

    print(f"  Name: {name}")
    print(f"  Industry: {industry}")
    print(f"  Followers: {followers}")
    print(f"  Location: {location}")
    print(f"  Size: {size}")
    print(f"  Type: {company_type}")
    print(f"  Link: {link}")

    if i >= 5:  # Show first 5 cards
        print(f"\n... and {len(cards) - 5} more cards")
        break

print("\n" + "="*80)
print("Selector test complete!")
print("="*80)

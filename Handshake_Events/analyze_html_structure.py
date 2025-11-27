#!/usr/bin/env python3
"""
Analyze the HTML structure to find correct selectors for employer cards
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

if cards:
    # Analyze the first card in detail
    first_card = cards[0]
    print("\nFirst card structure:")
    print("="*80)
    print(first_card.prettify()[:3000])  # First 3000 chars

    print("\n\n" + "="*80)
    print("Extracting data from first card:")
    print("="*80)

    # Try to find company name
    name_tags = first_card.find_all(['h1', 'h2', 'h3', 'h4', 'a'])
    print("\nPotential name elements:")
    for tag in name_tags[:5]:
        print(f"  {tag.name}: {tag.get_text(strip=True)[:100]}")

    # Try to find all text content
    all_text = first_card.get_text(separator=' | ', strip=True)
    print("\n\nAll text in card:")
    print(all_text[:500])

    # Find all links
    links = first_card.find_all('a', href=True)
    print("\n\nLinks in card:")
    for link in links[:3]:
        print(f"  {link['href']}")
        print(f"    Text: {link.get_text(strip=True)}")

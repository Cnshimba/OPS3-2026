#!/usr/bin/env python3
"""
Add IDs to Glossary Terms
Parses glossary.html and adds id attributes to term-card elements 
matching the term title. This enables deep linking (e.g., glossary.html#Term-Name).
"""

from bs4 import BeautifulSoup
from pathlib import Path

def add_ids_to_glossary():
    base_dir = Path(__file__).parent.parent
    glossary_path = base_dir / "glossary.html"
    
    if not glossary_path.exists():
        print(f"❌ File not found: {glossary_path}")
        return

    print(f"Processing: {glossary_path.name}")
    
    with open(glossary_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    soup = BeautifulSoup(content, 'html.parser')
    
    # Find all term cards
    term_cards = soup.find_all('div', class_='term-card')
    count = 0
    
    for card in term_cards:
        # Find the title element
        title_elem = card.find('div', class_='term-title')
        if title_elem:
            term_text = title_elem.get_text().strip()
            # Generate ID: Replace spaces with dashes, generic sanitization
            # The tooltip script uses: term.replace(" ", "-")
            term_id = term_text.replace(" ", "-")
            
            # Add id to the card if not present
            if not card.get('id'):
                card['id'] = term_id
                count += 1
                
    # Write back
    with open(glossary_path, 'w', encoding='utf-8') as f:
        f.write(str(soup))
        
    print(f"✅ Added IDs to {count} glossary terms")

if __name__ == "__main__":
    add_ids_to_glossary()

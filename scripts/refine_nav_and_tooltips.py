#!/usr/bin/env python3
"""
Refine Navigation and Fix Tooltips
1. Removes legacy "Back to Course Index" links (top and bottom).
2. Fixes glossary path in tooltips (from 'glossary.html' to '../glossary.html').
"""

from bs4 import BeautifulSoup
from pathlib import Path
import re

def refine_files():
    base_dir = Path(__file__).parent.parent
    print("=" * 70)
    print("Refining Navigation & Fixing Tooltip Paths")
    print("=" * 70)
    
    processed = 0
    # Process all Student Notes
    for week_dir in base_dir.glob("Week *"):
        if week_dir.is_dir():
            notes_files = list(week_dir.glob("*Student_Notes.html"))
            for html_file in notes_files:
                print(f"Processing: {html_file.name}")
                
                with open(html_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 1. FIX TOOLTIP PATHS
                # Replace 'href="glossary.html#' with 'href="../glossary.html#'
                # But careful not to double-prefix if already correct (though current script wrote incorrect ones)
                # The current script wrote: href="glossary.html#..."
                # We want: href="../glossary.html#..."
                
                # Simple string replacement is safest here as the pattern is distinct
                content = content.replace('href="glossary.html#', 'href="../glossary.html#')
                
                # 2. REMOVE LEGACY "BACK TO COURSE INDEX" LINKS
                # Pattern: <p><a href="../index.html">← Back to Course Index</a></p>
                # The arrow might be unicode char, so usage of regex is better.
                
                # Regex for the specific paragraph containing the link
                # Matches <p> ... <a ...>...Back to Course Index...</a> ... </p>
                legacy_nav_pattern = r'<p>\s*<a href="\.\./index\.html">.*?Back to Course Index.*?</a>\s*</p>'
                
                # Remove all occurrences (top and bottom)
                content = re.sub(legacy_nav_pattern, '', content, flags=re.DOTALL | re.IGNORECASE)
                
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                processed += 1
                
    print(f"✅ Refined {processed} files")

if __name__ == "__main__":
    refine_files()

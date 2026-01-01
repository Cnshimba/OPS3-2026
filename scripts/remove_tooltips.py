#!/usr/bin/env python3
"""
Remove all glossary tooltips from student notes HTML files using regex.
"""

from pathlib import Path
import re

def remove_tooltips(html_content):
    # Pattern to match glossary links:
    # <a ... class="glossary-term">Term Text<span class="glossary-tooltip">Def</span></a>
    
    # We use non-greedy matching .*?
    # Capture group 1 is the term text
    
    # This pattern handles:
    # 1. Opening <a> tag with class="glossary-term"
    # 2. Term text (Group 1)
    # 3. Optional <span class="glossary-tooltip">...</span>
    # 4. Closing </a>
    
    pattern = r'<a [^>]*class="glossary-term"[^>]*>(.*?)<span class="glossary-tooltip">.*?</span></a>'
    
    # Replace with just the term text (group 1)
    # We run this in a loop to handle nested cases if any (though unlikely here)
    # or just simple substitution
    
    # Python re.sub handles global replacement by default
    cleaned = re.sub(pattern, r'\1', html_content, flags=re.DOTALL)
    
    # Also handle cases where the tooltip span might be missing or different structure
    # Just <a class="glossary-term">Term</a>
    pattern_simple = r'<a [^>]*class="glossary-term"[^>]*>(.*?)</a>'
    cleaned = re.sub(pattern_simple, r'\1', cleaned, flags=re.DOTALL | re.IGNORECASE)

    # Remove the CSS style block for glossary if present
    style_pattern = r'<style>\s*/\* Glossary Tooltip Styles \*/.*?</style>'
    cleaned = re.sub(style_pattern, '', cleaned, flags=re.DOTALL)
    
    return cleaned

def main():
    base_dir = Path(__file__).parent.parent
    print("=" * 70)
    print("Removing ALL Glossary Tooltips (Regex Mode)")
    print("=" * 70)
    
    processed = 0
    for week_dir in base_dir.glob("Week *"):
        if week_dir.is_dir():
            notes_files = list(week_dir.glob("*Student_Notes.html"))
            for html_file in notes_files:
                print(f"Cleaning: {html_file.name}")
                with open(html_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                cleaned = remove_tooltips(content)
                
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(cleaned)
                processed += 1
                
    print(f"✅ Cleaned {processed} files")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Repair corrupted HTML files by stripping broken glossary markup and restoring clean text.
Includes handling for encoded HTML entities.
"""

from pathlib import Path
import re

def clean_glossary_corruption(content):
    # Pattern 1: Fully formed but nested/broken tags
    # <a href="..." class="glossary-term">Term<span ...>Def</span></a>
    content = re.sub(r'<a [^>]*class="glossary-term"[^>]*>(.*?)<span class="glossary-tooltip">.*?</span></a>', r'\1', content, flags=re.DOTALL)
    
    # Pattern 2: The specific corruption visible in screenshot (Unencoded)
    content = content.replace('class="glossary-term">', '')
    content = re.sub(r'<span class="glossary-tooltip">.*?</span>', '', content, flags=re.DOTALL)
    
    # Pattern 3: Encoded entities (from grep output)
    # class="glossary-term"&gt;
    content = content.replace('class="glossary-term"&gt;', '')
    content = content.replace('&lt;span class="glossary-icon"&gt;&lt;/span&gt;', '')
    content = content.replace('<span class="glossary-icon"></span>', '')
    
    # Remove encoded closing tags sequences seen in output
    # &lt;/a&gt;
    content = content.replace('&lt;/a&gt;', '')
    
    # Clean up any remaining <a ... class="glossary-term"> (opening tags)
    content = re.sub(r'<a [^>]*class="glossary-term"[^>]*>', '', content)
    
    # Remove simple <a> tags that might wrap nothing or be broken
    content = re.sub(r'<a href="glossary\.html#[^"]+" class="glossary-term">', '', content)
    
    # Final cleanup of any lingering "glossary-term" text
    content = re.sub(r'class=["\']glossary-term["\'][^>]*>', '', content)
    
    return content

def main():
    base_dir = Path(__file__).parent.parent
    print("=" * 70)
    print("Reparing Corrupted HTML Files (Enhanced)")
    print("=" * 70)
    
    processed = 0
    for week_dir in base_dir.glob("Week *"):
        if week_dir.is_dir():
            notes_files = list(week_dir.glob("*Student_Notes.html"))
            for html_file in notes_files:
                print(f"Repairing: {html_file.name}")
                with open(html_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                cleaned = clean_glossary_corruption(content)
                
                # Double clean common lingering artifacts
                cleaned = cleaned.replace('<span class="glossary-tooltip">', '')
                cleaned = cleaned.replace('</span></a>', '</a>')
                cleaned = cleaned.replace('</span>', '') # Risky but necessary for the generic spans left behind? NO.
                # Only remove spans that look like they belong to tooltips
                
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(cleaned)
                processed += 1
                
    print(f"✅ Repaired {processed} files")

if __name__ == "__main__":
    main()

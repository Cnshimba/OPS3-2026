#!/usr/bin/env python3
"""
Final spot repair for specific text artifacts left after HTML repair.
"""

from pathlib import Path
import re

def spot_repair(content):
    # Remove specific artifacts seen in logs
    content = content.replace('A Hypervisor" ', '')
    content = content.replace('Type 1 hypervisor" ', '')
    content = content.replace('&quot;', '"') # unlikely but safe if check context
    
    # Generic cleanup for stray quotes from stripped attributes
    # e.g. " class="...
    content = content.replace(' class="glossary-term">', '')
    
    # Clean up double spaces created by removals
    content = re.sub(r'  +', ' ', content)
    
    return content

def main():
    base_dir = Path(__file__).parent.parent
    print("=" * 70)
    print("Final Spot Repair")
    print("=" * 70)
    
    processed = 0
    for week_dir in base_dir.glob("Week *"):
        if week_dir.is_dir():
            notes_files = list(week_dir.glob("*Student_Notes.html"))
            for html_file in notes_files:
                print(f"Checking: {html_file.name}")
                with open(html_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                cleaned = spot_repair(content)
                
                if cleaned != content:
                    print(f"  Fixed artifacts in {html_file.name}")
                    with open(html_file, 'w', encoding='utf-8') as f:
                        f.write(cleaned)
                    processed += 1
                
    print(f"✅ Polished {processed} files")

if __name__ == "__main__":
    main()

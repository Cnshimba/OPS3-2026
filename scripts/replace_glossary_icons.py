#!/usr/bin/env python3
"""
Replace Glossary Icons
Replaces emoji icons (📂, 📅) with accessible SVG icons in glossary.html and potentially quiz files.
"""

from bs4 import BeautifulSoup
from pathlib import Path

# VUT Theme Colors
COLOR_GOLD = "#c9984a"
COLOR_BLUE = "#002F6E"

# SVG Icons (VUT Gold)
ICON_FOLDER = f'''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="{COLOR_GOLD}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="inline-block mr-1"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"></path></svg>'''
ICON_CALENDAR = f'''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="{COLOR_GOLD}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="inline-block mr-1"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></svg>'''
ICON_MEMO = f'''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="{COLOR_GOLD}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="inline-block mr-2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>'''
ICON_ROCKET = f'''<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="{COLOR_GOLD}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="inline-block mr-2"><path d="M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 0 0-2.91-.09z"></path><path d="M12 15l-3-3a22 22 0 0 1 2-3.95A12.88 12.88 0 0 1 22 2c0 2.72-.78 7.5-6 11a22.35 22.35 0 0 1-4 2z"></path><path d="M9 12H4s.55-3.03 2-4c1.62-1.08 5 0 5 0"></path><path d="M12 15v5s3.03-.55 4-2c1.08-1.62 0-5 0-5"></path></svg>'''
ICON_CLIPBOARD = f'''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="{COLOR_GOLD}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="inline-block mr-1"><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"></path><rect x="8" y="2" width="8" height="4" rx="1" ry="1"></rect></svg>'''
ICON_PENCIL = f'''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="{COLOR_GOLD}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="inline-block mr-1"><path d="M17 3a2.828 2.828 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5L17 3z"></path></svg>'''
ICON_KEYBOARD = f'''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="{COLOR_GOLD}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="inline-block mr-1"><rect x="2" y="4" width="20" height="16" rx="2" ry="2"></rect><line x1="6" y1="8" x2="6" y2="8"></line><line x1="10" y1="8" x2="10" y2="8"></line><line x1="14" y1="8" x2="14" y2="8"></line><line x1="18" y1="8" x2="18" y2="8"></line><line x1="6" y1="12" x2="6" y2="12"></line><line x1="10" y1="12" x2="10" y2="12"></line><line x1="14" y1="12" x2="14" y2="12"></line><line x1="18" y1="12" x2="18" y2="12"></line><line x1="6" y1="16" x2="18" y2="16"></line></svg>'''
ICON_STAR = f'''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="{COLOR_GOLD}" stroke="{COLOR_GOLD}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="inline-block mr-1"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>'''
ICON_SPARKLES = f'''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="{COLOR_GOLD}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="inline-block mr-1"><path d="m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275L12 3Z"></path></svg>'''
ICON_BOOKS = f'''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="{COLOR_GOLD}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="inline-block mr-1"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path></svg>'''
ICON_RETRY = f'''<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="{COLOR_BLUE}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="inline-block mr-2"><path d="M23 4v6h-6"></path><path d="M1 20v-6h6"></path><path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"></path></svg>'''

def replace_icons(file_path):
    path = Path(file_path)
    if not path.exists():
        print(f"Skipping {path.name} (Not found)")
        return

    print(f"Processing {path.name}...")
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    new_content = content
    
    # Mapping
    replacements = {
        "📂": ICON_FOLDER,
        "📅": ICON_CALENDAR,
        "📝": ICON_MEMO,
        "🚀": ICON_ROCKET,
        "📋": ICON_CLIPBOARD,
        "✏️": ICON_PENCIL,
        "⌨️": ICON_KEYBOARD,
        "🌟": ICON_STAR,
        "✨": ICON_SPARKLES,
        "📚": ICON_BOOKS,
        "🔄": ICON_RETRY
    }

    count = 0
    for emoji, svg in replacements.items():
        if emoji in new_content:
            new_content = new_content.replace(emoji, svg)
            count += 1
    
    if content != new_content:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"✅ Replaced {count} types of icons in {path.name}")
    else:
        print(f"No icons found to replace in {path.name}")

def main():
    base_dir = Path(__file__).parent.parent
    
    # Target files
    files_to_check = [
        base_dir / "glossary.html",
        # Check Quizzes as well since user mentioned them
    ]
    
    # Add all quiz files
    # Note: glob("Week */*Quiz.html") matches folders starting with Week
    files_to_check.extend(base_dir.glob("Week */*Quiz.html"))
    
    print(f"Found {len(files_to_check)} files to check/replace.")
    
    for file_path in files_to_check:
        replace_icons(file_path)

if __name__ == "__main__":
    main()

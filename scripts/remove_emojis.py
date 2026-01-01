#!/usr/bin/env python3
"""
Remove all emoji icons from student notes HTML files
"""

from pathlib import Path
import re

def remove_emojis_from_html(html_content):
    """Remove common emoji icons from HTML content"""
    
    # List of emojis to remove
    emojis_to_remove = [
        '📚', '📖', '💻', '🖥️', '⚙️', '🔧', '🌐', '🔒', 
        '📊', '📈', '📉', '💾', '🗄️', '🔌', '📡', '🎯',
        '✨', '🚀', '⭐', '🔥', '💡', '📝', '✅', '❌',
        '🔍', '🎓', '📋', '📄', '📁', '🏗️', '🔑', '🌟',
        '⚡', '🛠️', '📦', '🔐', '🌍', '☁️', '💬', '📞'
    ]
    
    # Remove each emoji
    for emoji in emojis_to_remove:
        html_content = html_content.replace(emoji, '')
    
    # Also remove emoji pattern using regex (catches any remaining emojis)
    # This matches emoji unicode ranges
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F1E0-\U0001F1FF"  # flags
        "\U00002702-\U000027B0"
        "\U000024C2-\U0001F251"
        "]+", 
        flags=re.UNICODE
    )
    html_content = emoji_pattern.sub('', html_content)
    
    return html_content

def main():
    """Remove emojis from all student notes HTML files"""
    base_dir = Path(__file__).parent.parent
    
    print("=" * 70)
    print("Removing Emoji Icons from Student Notes")
    print("=" * 70)
    print()
    
    processed = 0
    
    # Find all student notes HTML files
    for week_dir in base_dir.glob("Week *"):
        if week_dir.is_dir():
            notes_files = list(week_dir.glob("*Student_Notes.html"))
            
            for html_file in notes_files:
                print(f"Processing: {html_file.name}")
                
                # Read file
                with open(html_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Count emojis before
                original_length = len(content)
                
                # Remove emojis
                cleaned_content = remove_emojis_from_html(content)
                
                # Count emojis removed
                removed_count = original_length - len(cleaned_content)
                
                # Write back
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(cleaned_content)
                
                processed += 1
                print(f"  ✅ Removed {removed_count} emoji characters")
    
    print()
    print("=" * 70)
    print(f"✅ Processed {processed} HTML files")
    print(f"   All emoji icons removed")
    print("=" * 70)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Add Navigation Buttons to Student Notes
Adds "Previous Chapter" and "Next Chapter" buttons to the bottom of each student notes file.
Includes deduplication to prevent repeated addition of navigation bars.
"""

from bs4 import BeautifulSoup
from pathlib import Path
import re

# Define the ordered list of weeks and their folder names
COURSE_SEQUENCE = [
    {"week": 1, "folder": "Week 1 - Introduction to Virtualization", "file": "Week_1_Student_Notes.html", "title": "Week 1: Introduction"},
    {"week": 2, "folder": "Week 2 - Virtual Machines", "file": "Week_2_Student_Notes.html", "title": "Week 2: Virtual Machines"},
    {"week": 3, "folder": "Week 3 - Virtual Networking and Linux Networking Fundamentals", "file": "Week_3_Student_Notes.html", "title": "Week 3: Networking"},
    {"week": 4, "folder": "Week 4 - Storage and Backup", "file": "Week_4_Student_Notes.html", "title": "Week 4: Storage"},
    {"week": 5, "folder": "Week 5 - Containers and Resource Management", "file": "Week_5_Student_Notes.html", "title": "Week 5: Containers"},
    {"week": 6, "folder": "Week 6 - Proxmox Cluster and High Availability", "file": "Week_6_Student_Notes.html", "title": "Week 6: Clustering"},
    {"week": 7, "folder": "Week 7 - Transition to Cloud Computing Concepts", "file": "Week_7_Student_Notes.html", "title": "Week 7: Cloud Concepts"},
    {"week": 8, "folder": "Week 8 - Cloud Foundation", "file": "Week_8_Student_Notes.html", "title": "Week 8: Cloud Foundation"},
    {"week": 9, "folder": "Week 9 - Compute Operations", "file": "Week_9_Student_Notes.html", "title": "Week 9: Compute Ops"},
    {"week": 10, "folder": "Week 10 - Storage and Persistence", "file": "Week_10_Student_Notes.html", "title": "Week 10: Persistence"},
    {"week": 11, "folder": "Week 11 - Automation and Cloud API", "file": "Week_11_Student_Notes.html", "title": "Week 11: Automation"},
    {"week": 12, "folder": "Week 12 - Final Project and Review", "file": "Week_12_Student_Notes.html", "title": "Week 12: Final Review"},
]

def create_nav_html(prev_item, next_item):
    """Generate the navigation HTML block."""
    
    html = '<div class="chapter-navigation flex justify-between items-center mt-12 pt-8 border-t border-gray-200 dark:border-gray-700">'
    
    # Previous Button
    if prev_item:
        path = f"../{prev_item['folder']}/{prev_item['file']}"
        html += f"""
        <a href="{path}" class="flex items-center text-blue-600 hover:text-blue-800 dark:text-blue-400 dark:hover:text-blue-300 transition-colors no-underline">
            <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path></svg>
            <span>Previous: {prev_item['title']}</span>
        </a>
        """
    else:
        html += '<div></div>' # Spacer

    # Index Button (Center)
    html += """
    <a href="../index.html" class="flex items-center font-semibold text-gray-700 hover:text-blue-600 dark:text-gray-300 dark:hover:text-blue-400 transition-colors no-underline">
        <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"></path></svg>
        Course Index
    </a>
    """

    # Next Button
    if next_item:
        path = f"../{next_item['folder']}/{next_item['file']}"
        html += f"""
        <a href="{path}" class="flex items-center text-blue-600 hover:text-blue-800 dark:text-blue-400 dark:hover:text-blue-300 transition-colors no-underline">
            <span>Next: {next_item['title']}</span>
            <svg class="w-5 h-5 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path></svg>
        </a>
        """
    else:
        html += '<div></div>' # Spacer

    html += '</div>'
    return html

def main():
    base_dir = Path(__file__).parent.parent
    print("=" * 70)
    print("Adding Chapter Navigation")
    print("=" * 70)
    
    for i, item in enumerate(COURSE_SEQUENCE):
        prev_item = COURSE_SEQUENCE[i-1] if i > 0 else None
        next_item = COURSE_SEQUENCE[i+1] if i < len(COURSE_SEQUENCE) - 1 else None
        
        file_path = base_dir / item['folder'] / item['file']
        
        if not file_path.exists():
            print(f"❌ File not found: {file_path}")
            continue
            
        print(f"Processing: {item['file']}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        soup = BeautifulSoup(content, 'html.parser')
        
        # Find article
        article = soup.find('article')
        if not article:
            print("  ⚠️ No article tag found")
            continue
            
        # Remove existing navigation if present (avoid duplicates)
        existing_nav = article.find('div', class_='chapter-navigation')
        if existing_nav:
            existing_nav.decompose()
        
        # Generate new nav
        nav_html = create_nav_html(prev_item, next_item)
        nav_soup = BeautifulSoup(nav_html, 'html.parser')
        
        # Append to end of article
        article.append(nav_soup)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(str(soup))
            
    print("✅ Navigation added to all files")

if __name__ == "__main__":
    main()

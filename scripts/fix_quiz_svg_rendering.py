import glob
import os

def fix_quiz_files():
    # Find all Week_X_Quiz.html files
    quiz_files = glob.glob("Week */Week_*_Quiz.html")
    print(f"Found {len(quiz_files)} quiz files to check.")

    target_line_part = "document.getElementById('gradeDisplay').textContent = `${percentage}% - ${grade}`;"
    replacement_line_part = "document.getElementById('gradeDisplay').innerHTML = `${percentage}% - ${grade}`;"

    for file_path in quiz_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if target_line_part in content:
                new_content = content.replace(target_line_part, replacement_line_part)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"✅ Fixed: {file_path}")
            else:
                if replacement_line_part in content:
                     print(f"ℹ️ Already fixed: {file_path}")
                else:
                    print(f"⚠️ Pattern not found in: {file_path}")
                    # Debug print to help identify mismatch if needed
                    # start_idx = content.find("document.getElementById('gradeDisplay')")
                    # if start_idx != -1:
                    #     print(f"Context: {content[start_idx:start_idx+100]}")

        except Exception as e:
            print(f"❌ Error processing {file_path}: {e}")

if __name__ == "__main__":
    fix_quiz_files()

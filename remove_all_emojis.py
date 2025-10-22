#!/usr/bin/env python3
"""
Remove All Emojis from Project Files
====================================
Comprehensive script to remove all emojis from all project files
and prepare for Git repository push.
"""

import os
import re
import glob
from pathlib import Path

def remove_emojis_from_text(text):
    """Remove all emojis from text"""
    # Comprehensive emoji regex pattern
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F1E0-\U0001F1FF"  # flags (iOS)
        "\U00002702-\U000027B0"  # dingbats
        "\U000024C2-\U0001F251"  # enclosed characters
        "\U0001F900-\U0001F9FF"  # supplemental symbols
        "\U0001FA70-\U0001FAFF"  # symbols and pictographs extended-A
        "\U00002600-\U000026FF"  # miscellaneous symbols
        "\U00002700-\U000027BF"  # dingbats
        "\U0001F018-\U0001F0F5"  # playing cards
        "\U0001F200-\U0001F2FF"  # enclosed CJK letters and months
        "]+", 
        flags=re.UNICODE
    )
    return emoji_pattern.sub('', text)

def should_skip_file(file_path):
    """Check if file should be skipped"""
    skip_patterns = [
        'venv/',
        '__pycache__/',
        '.git/',
        '.DS_Store',
        '*.pyc',
        '*.pyo',
        '*.pyd',
        '*.so',
        '*.egg',
        '*.egg-info/',
        'node_modules/',
        '.env',
        '*.log',
        '*.db',
        '*.sqlite',
        '*.sqlite3'
    ]
    
    file_path_str = str(file_path)
    for pattern in skip_patterns:
        if pattern in file_path_str:
            return True
    return False

def process_file(file_path):
    """Process a single file to remove emojis"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remove emojis
        cleaned_content = remove_emojis_from_text(content)
        
        # Only write if content changed
        if cleaned_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(cleaned_content)
            print(f" Cleaned: {file_path}")
            return True
        else:
            print(f" No emojis found: {file_path}")
            return False
            
    except Exception as e:
        print(f" Error processing {file_path}: {e}")
        return False

def main():
    """Main function to remove emojis from all project files"""
    print(" Starting emoji removal from all project files...")
    
    project_root = Path('.')
    processed_files = 0
    cleaned_files = 0
    
    # File extensions to process
    extensions = [
        '*.py', '*.md', '*.txt', '*.yml', '*.yaml', '*.json', 
        '*.sh', '*.sql', '*.html', '*.css', '*.js', '*.ts'
    ]
    
    for ext in extensions:
        for file_path in project_root.rglob(ext):
            if should_skip_file(file_path):
                continue
                
            if file_path.is_file():
                processed_files += 1
                if process_file(file_path):
                    cleaned_files += 1
    
    print(f"\n Summary:")
    print(f"   Files processed: {processed_files}")
    print(f"   Files cleaned: {cleaned_files}")
    print(f"   Files unchanged: {processed_files - cleaned_files}")
    print("\n Emoji removal completed!")

if __name__ == "__main__":
    main()

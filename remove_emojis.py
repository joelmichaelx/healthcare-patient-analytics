#!/usr/bin/env python3
"""
Remove all emojis from files in the healthcare project
"""

import os
import re
import glob

def remove_emojis_from_file(file_path):
    """Remove emojis from a single file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remove common emojis
        emoji_pattern = re.compile(
            "["
            "\U0001F600-\U0001F64F"  # emoticons
            "\U0001F300-\U0001F5FF"  # symbols & pictographs
            "\U0001F680-\U0001F6FF"  # transport & map symbols
            "\U0001F1E0-\U0001F1FF"  # flags (iOS)
            "\U00002702-\U000027B0"  # dingbats
            "\U000024C2-\U0001F251"  # enclosed characters
            "]+", flags=re.UNICODE)
        
        new_content = emoji_pattern.sub('', content)
        
        if new_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Removed emojis from: {file_path}")
            return True
        return False
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    """Remove emojis from all relevant files"""
    print("Removing emojis from healthcare project files...")
    
    # File patterns to process
    patterns = [
        "*.md",
        "*.py", 
        "*.sh",
        "*.yml",
        "*.yaml",
        "*.txt"
    ]
    
    files_processed = 0
    files_changed = 0
    
    for pattern in patterns:
        for file_path in glob.glob(pattern, recursive=True):
            if os.path.isfile(file_path):
                files_processed += 1
                if remove_emojis_from_file(file_path):
                    files_changed += 1
    
    print(f"\nEmoji removal complete!")
    print(f"Files processed: {files_processed}")
    print(f"Files changed: {files_changed}")

if __name__ == "__main__":
    main()

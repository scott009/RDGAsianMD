#!/usr/bin/env python3
"""
Fix chapter 18.2: Change title to "INQUIRY OF THE FIRST NOBLE TRUTH"
"""

import json

def main():
    # Read the workmaster.json file
    with open('workmaster.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Find and update chapter 18.2
    chapters = data.get('chapters', [])

    for chapter in chapters:
        if chapter.get('id') == '18.2':
            print(f"Found chapter {chapter['id']}")
            print(f"Old title: {chapter.get('title')}")

            # Update chapter title
            chapter['title'] = 'INQUIRY OF THE FIRST NOBLE TRUTH'

            print(f"New title: {chapter['title']}")
            print("\nChapter title updated successfully!")
            break
    else:
        print("Chapter 18.2 not found!")
        return

    # Write the updated data back to workmaster.json
    with open('workmaster.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print("\nworkmaster.json has been updated.")

if __name__ == '__main__':
    main()

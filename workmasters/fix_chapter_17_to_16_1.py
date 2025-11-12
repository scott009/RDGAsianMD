#!/usr/bin/env python3
"""
Fix chapter 17: Change it to chapter 16.1 and update all paragraph IDs
"""

import json

def update_paragraph_ids(obj, old_prefix, new_prefix):
    """Recursively update paragraph IDs from old_prefix to new_prefix"""
    if isinstance(obj, dict):
        if obj.get('type') == 'paragraph' and 'id' in obj:
            old_id = obj['id']
            if old_id.startswith(old_prefix):
                # Replace the prefix
                obj['id'] = old_id.replace(old_prefix, new_prefix, 1)
                print(f"Updated: {old_id} -> {obj['id']}")
        # Recursively update in all dict values
        for value in obj.values():
            update_paragraph_ids(value, old_prefix, new_prefix)
    elif isinstance(obj, list):
        # Recursively update in all list items
        for item in obj:
            update_paragraph_ids(item, old_prefix, new_prefix)

def main():
    # Read the workmaster.json file
    with open('workmaster.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Find and update chapter 17
    chapters = data.get('chapters', [])

    for chapter in chapters:
        if chapter.get('id') == '17' or chapter.get('id') == 17:
            print(f"Found chapter {chapter['id']}: {chapter.get('title')}")
            print(f"Changing chapter ID from 17 to '16.1'")

            # Update chapter ID
            chapter['id'] = '16.1'

            # Update all paragraph IDs within this chapter
            update_paragraph_ids(chapter, 'p17-', 'p16.1-')

            print("\nChapter updated successfully!")
            break
    else:
        print("Chapter 17 not found!")
        return

    # Write the updated data back to workmaster.json
    with open('workmaster.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print("\nworkmaster.json has been updated.")

if __name__ == '__main__':
    main()

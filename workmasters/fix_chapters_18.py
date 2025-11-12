#!/usr/bin/env python3
"""
1. Delete chapter 18.1
2. Rename chapter 18.2 to 16.2 and update paragraph IDs
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

    chapters = data.get('chapters', [])

    # Step 1: Delete chapter 18.1
    print("Step 1: Deleting chapter 18.1...")
    chapters_to_keep = []
    for chapter in chapters:
        if chapter.get('id') == '18.1':
            print(f"Deleting chapter {chapter['id']}: {chapter.get('title')}")
        else:
            chapters_to_keep.append(chapter)

    data['chapters'] = chapters_to_keep
    print(f"Chapter 18.1 deleted. Remaining chapters: {len(chapters_to_keep)}\n")

    # Step 2: Rename chapter 18.2 to 16.2
    print("Step 2: Renaming chapter 18.2 to 16.2...")
    for chapter in data['chapters']:
        if chapter.get('id') == '18.2':
            print(f"Found chapter {chapter['id']}: {chapter.get('title')}")
            print(f"Changing chapter ID from 18.2 to '16.2'")

            # Update chapter ID
            chapter['id'] = '16.2'

            # Update all paragraph IDs within this chapter
            # Need to handle both p18.22- and p18.2- prefixes
            update_paragraph_ids(chapter, 'p18.22-', 'p16.2-')
            update_paragraph_ids(chapter, 'p18.2-', 'p16.2-')

            print("\nChapter updated successfully!")
            break

    # Write the updated data back to workmaster.json
    with open('workmaster.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print("\nworkmaster.json has been updated.")

if __name__ == '__main__':
    main()

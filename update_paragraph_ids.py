#!/usr/bin/env python3
"""
Script to update all paragraph IDs in Section 5 to match their current chapter numbers
"""

import json
import re

def update_paragraph_ids_in_content(content_list, chapter_id, counter):
    """
    Recursively update paragraph IDs in a content list
    Returns the updated counter
    """
    for item in content_list:
        item_type = item.get('type', '')

        if item_type == 'paragraph':
            old_id = item.get('id', '')
            new_id = f"p{chapter_id}-{counter['count']}"

            if old_id != new_id:
                item['id'] = new_id
                counter['updates'].append({
                    'chapter': chapter_id,
                    'old': old_id,
                    'new': new_id
                })

            counter['count'] += 1

        elif item_type == 'subsection':
            # Process paragraphs within subsections
            subsection_content = item.get('content', [])
            update_paragraph_ids_in_content(subsection_content, chapter_id, counter)

    return counter

def main():
    # Load the JSON file
    print("Loading workmaster.json...")
    with open('/home/scott/gitrepos/RDGAsianMD/workmaster.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Find Section 5
    section5 = None
    section5_index = None
    for i, section in enumerate(data['content']):
        if section.get('type') == 'section' and section.get('id') == 5:
            section5 = section
            section5_index = i
            break

    if not section5:
        print("ERROR: Section 5 not found!")
        return

    print(f"Found Section 5: {section5['title']}")
    print(f"Processing {len(section5['chapters'])} chapters...\n")

    total_updates = []

    # Process each chapter
    for chapter in section5['chapters']:
        chapter_id = str(chapter.get('id', ''))
        chapter_title = chapter.get('title', '')

        # Counter for paragraphs in this chapter
        counter = {
            'count': 1,
            'updates': []
        }

        # Process all sections in the chapter
        for section in chapter.get('sections', []):
            content = section.get('content', [])
            update_paragraph_ids_in_content(content, chapter_id, counter)

        if counter['updates']:
            print(f"Chapter {chapter_id}: {chapter_title}")
            print(f"  Updated {len(counter['updates'])} paragraph IDs")
            total_updates.extend(counter['updates'])
        elif counter['count'] > 1:
            print(f"Chapter {chapter_id}: {chapter_title}")
            print(f"  {counter['count']-1} paragraphs - IDs already correct")

    # Update the data
    data['content'][section5_index] = section5

    # Save the updated JSON
    output_file = '/home/scott/gitrepos/RDGAsianMD/workmaster.json'
    print(f"\nSaving updated JSON to {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print("\nDone!")
    print(f"\nSummary:")
    print(f"  Total paragraph IDs updated: {len(total_updates)}")

    if total_updates and len(total_updates) <= 20:
        print(f"\nUpdates made:")
        for update in total_updates:
            print(f"  Chapter {update['chapter']}: {update['old']} -> {update['new']}")
    elif total_updates:
        print(f"\nFirst 10 updates:")
        for update in total_updates[:10]:
            print(f"  Chapter {update['chapter']}: {update['old']} -> {update['new']}")
        print(f"  ... and {len(total_updates)-10} more")

if __name__ == '__main__':
    main()

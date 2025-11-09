#!/usr/bin/env python3
"""
Script to renumber chapters in Section 5 of workmaster.json based on sec5workmaster.md
"""

import json
import re
from collections import OrderedDict

# Chapter structure from MD file (in order)
MD_CHAPTERS = [
    ("12", "AWAKENING: BUDDHA"),
    ("13", "THE STORY OF THE ORIGINAL BUDDHA"),
    ("14", "WALKING IN THE FOOTSTEPS OF THE BUDDHA"),
    ("15", "THE TRUTH: DHARMA"),
    ("16", "THE FIRST NOBLE TRUTH:"),
    ("17", "TRAUMA AND ATTACHMENT INJURY"),
    ("18", "INQUIRY OF THE FIRST NOBLE TRUTH:"),
    ("19", "THE SECOND NOBLE TRUTH:"),
    ("19.1", "INQUIRY OF THE SECOND NOBLE TRUTH:"),
    ("20", "THE THIRD NOBLE TRUTH:"),
    ("20.1", "INQUIRY OF THE THIRD NOBLE TRUTH:"),
    ("21", "THE FOURTH NOBLE TRUTH:"),  # Fixing 21. to 21
    ("21.1", "INQUIRY OF THE FOURTH NOBLE TRUTH:"),  # Fixing spacing
    ("22", "THE EIGHTFOLD PATH:"),
    ("23", "WISE UNDERSTANDING:"),
    ("23.1", "INQUIRY OF WISE UNDERSTANDING:"),
    ("24", "WISE INTENTION:"),
    ("24.1", "INQUIRY OF WISE INTENTION:"),
    ("24.2", "MAKING AMENDS:"),
    ("25", "WISE SPEECH"),
    ("25.1", "INQUIRY OF WISE SPEECH:"),
    ("26", "WISE ACTION"),
    ("26.1", "INQUIRY OF WISE ACTION:"),
    ("27", "WISE LIVLIHOOD:"),
    ("27.1", "INQUIRY OF WISE LIVLIHOOD:"),
    ("28", "WISE EFFORT:"),
    ("28.1", "INQUIRY OF WISE EFFORT:"),
    ("29", "WISE MINDFULNESS:"),
    ("29.1", "INQUIRY OF WISE MINDFULNESS:"),
    ("30", "WISE CONCENTRATION:"),
    ("30.1", "INQUIRY OF WISE CONCENTRATION:"),  # Assuming this should be 30.1
]

def create_empty_chapter(chapter_id, title):
    """Create an empty chapter structure"""
    return {
        "type": "chapter",
        "id": chapter_id,
        "status": "draft",
        "title": title,
        "thai_title": "",
        "vietnamese_title": "",
        "korean_title": "",
        "japanese_title": "",
        "Chinese_Tradition_title": "",
        "Chinese_Simplified_title": "",
        "tibetan_title": "",
        "sections": []
    }

def extract_chapter_number_from_paragraph(para_id):
    """Extract chapter number from paragraph ID like 'p12-1' -> '12'"""
    if not para_id:
        return None
    match = re.match(r'p(\d+)-', para_id)
    if match:
        return match.group(1)
    return None

def find_chapter_by_content(old_chapters, chapter_num):
    """Find a chapter in old structure by looking for paragraphs with matching IDs"""
    chapter_num_str = str(chapter_num).split('.')[0]  # Get base number (e.g., '19' from '19.1')

    for chapter in old_chapters:
        # Look through sections and paragraphs
        for section in chapter.get('sections', []):
            for content_item in section.get('content', []):
                if content_item.get('type') == 'paragraph':
                    para_id = content_item.get('id', '')
                    if para_id.startswith(f'p{chapter_num_str}-'):
                        return chapter
                # Check subsections
                if content_item.get('type') == 'subsection':
                    for sub_item in content_item.get('content', []):
                        if sub_item.get('type') == 'paragraph':
                            para_id = sub_item.get('id', '')
                            if para_id.startswith(f'p{chapter_num_str}-'):
                                return chapter
    return None

def main():
    # Load the JSON file
    print("Loading workmaster.json...")
    with open('/home/scott/gitrepos/RDGAsianMD/workmasters/workmaster.json', 'r', encoding='utf-8') as f:
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
    print(f"Current number of chapters: {len(section5['chapters'])}")

    # Store old chapters for reference
    old_chapters = section5['chapters']

    # Build mapping of old chapters by their IDs
    old_chapters_by_id = {}
    for chapter in old_chapters:
        old_id = str(chapter.get('id', ''))
        old_chapters_by_id[old_id] = chapter

    # Create new chapter list
    new_chapters = []

    print("\nProcessing chapters...")
    for chapter_id, chapter_title in MD_CHAPTERS:
        base_chapter_num = chapter_id.split('.')[0]

        # Check if we have an existing chapter with this exact ID
        if chapter_id in old_chapters_by_id:
            print(f"  Chapter {chapter_id}: Found existing - {chapter_title}")
            existing = old_chapters_by_id[chapter_id]
            # Update the title to match MD (in case of differences)
            existing['id'] = chapter_id  # Ensure ID is correct format
            existing['title'] = chapter_title
            new_chapters.append(existing)
        else:
            # Try to find by base number (for content matching)
            existing = find_chapter_by_content(old_chapters, base_chapter_num)

            if existing and '.' in chapter_id:
                # This is a sub-chapter (like 19.1) but content is in main chapter
                # Create empty placeholder for now
                print(f"  Chapter {chapter_id}: Creating placeholder - {chapter_title}")
                new_chapters.append(create_empty_chapter(chapter_id, chapter_title))
            elif existing and '.' not in chapter_id:
                # Main chapter with existing content
                print(f"  Chapter {chapter_id}: Found content - {chapter_title}")
                existing['id'] = chapter_id
                existing['title'] = chapter_title
                new_chapters.append(existing)
            else:
                # No existing content found - create placeholder
                print(f"  Chapter {chapter_id}: Creating placeholder - {chapter_title}")
                new_chapters.append(create_empty_chapter(chapter_id, chapter_title))

    # Update Section 5 with new chapters
    section5['chapters'] = new_chapters
    data['content'][section5_index] = section5

    print(f"\nNew number of chapters: {len(new_chapters)}")

    # Save the updated JSON
    output_file = '/home/scott/gitrepos/RDGAsianMD/workmasters/workmaster_updated.json'
    print(f"\nSaving updated JSON to {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print("Done!")
    print(f"\nSummary:")
    print(f"  - Total chapters in new structure: {len(new_chapters)}")
    print(f"  - Original chapters: {len(old_chapters)}")

if __name__ == '__main__':
    main()

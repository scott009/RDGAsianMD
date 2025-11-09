#!/usr/bin/env python3
"""
Script to add chapter_type and parent_chapter fields to all chapters in Section 5
"""

import json

def get_parent_chapter(chapter_id):
    """Extract parent chapter ID from decimal notation"""
    ch_id = str(chapter_id)

    if '.' in ch_id:
        # Extract base number (e.g., "24.1" → "24", "18.1" → "18")
        base = ch_id.split('.')[0]
        return base
    else:
        # Non-decimal chapters have no parent
        return None

def get_chapter_type(chapter_id):
    """Determine chapter type based on decimal notation"""
    ch_id = str(chapter_id)

    if '.' in ch_id:
        return "inquiry"
    else:
        return "narrative"

def main():
    json_file = 'workmaster.json'

    print("Loading JSON file...")
    with open(json_file, 'r', encoding='utf-8') as f:
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

    # Add fields to each chapter
    narrative_count = 0
    inquiry_count = 0
    has_parent_count = 0
    no_parent_count = 0

    for chapter in section5['chapters']:
        chapter_id = chapter.get('id')

        # Add chapter_type
        chapter_type = get_chapter_type(chapter_id)
        chapter['chapter_type'] = chapter_type

        # Add parent_chapter
        parent = get_parent_chapter(chapter_id)
        if parent:
            chapter['parent_chapter'] = parent
            has_parent_count += 1
        else:
            # Don't add the field if there's no parent (keeps JSON cleaner)
            # Or set to None/null if you prefer
            no_parent_count += 1

        # Count types
        if chapter_type == 'narrative':
            narrative_count += 1
        else:
            inquiry_count += 1

        # Display
        parent_str = f"parent: {parent}" if parent else "no parent"
        print(f"  Chapter {str(chapter_id):5} → {chapter_type:10} ({parent_str}) - {chapter['title'][:45]}")

    # Update the data
    data['content'][section5_index] = section5

    # Save updated JSON
    print(f"\nSaving updated JSON to {json_file}...")
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print("\n" + "="*80)
    print("SUMMARY:")
    print(f"  Narrative chapters: {narrative_count}")
    print(f"  Inquiry chapters: {inquiry_count}")
    print(f"  Chapters with parent: {has_parent_count}")
    print(f"  Chapters without parent: {no_parent_count}")
    print("="*80)
    print("\nDone!")

if __name__ == '__main__':
    main()

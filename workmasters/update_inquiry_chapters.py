#!/usr/bin/env python3
"""
Extract ONLY inquiry chapters from section5_truths_and_paths_english.md
and update them in workmaster.json
"""

import json
import re

def parse_inquiry_chapters(filename):
    """Parse and extract ONLY inquiry chapters"""
    with open(filename, 'r') as f:
        content = f.read()

    chapters = []
    lines = content.split('\n')

    current_chapter = None
    current_paragraphs = []
    seen_chapters = set()  # Track chapters we've already processed to avoid duplicates

    i = 0
    while i < len(lines):
        line = lines[i]

        # Check for inquiry chapter heading
        chapter_match = re.match(r'^## Chapter ([\d.]+)\s*:?\s*INQUIRY OF\s+(.+)$', line)
        if chapter_match:
            # Save previous chapter if exists and not already seen
            if current_chapter and current_paragraphs:
                ch_id = current_chapter['id']
                if ch_id not in seen_chapters:
                    current_chapter['paragraphs'] = current_paragraphs
                    chapters.append(current_chapter)
                    seen_chapters.add(ch_id)

            # Start new chapter
            chapter_id_str = chapter_match.group(1).strip()
            chapter_title_end = chapter_match.group(2).strip()

            # Keep ID as string
            chapter_id = chapter_id_str
            full_title = f"INQUIRY OF {chapter_title_end}"

            # Skip if we've already seen this chapter (duplicate)
            if chapter_id in seen_chapters:
                current_chapter = None
                current_paragraphs = []
                i += 1
                continue

            current_chapter = {
                'id': chapter_id,
                'title': full_title
            }
            current_paragraphs = []
            i += 1
            continue

        # Check for paragraph ID: ### ID: p18-1
        para_id_match = re.match(r'^### ID:\s*(p[\d.]+-\d+)$', line)
        if para_id_match and current_chapter:
            para_id = para_id_match.group(1)
            # Next line(s) contain the paragraph text
            i += 1
            para_text_lines = []
            while i < len(lines) and not lines[i].startswith('###') and not lines[i].startswith('##'):
                if lines[i].strip():  # Skip empty lines
                    para_text_lines.append(lines[i])
                i += 1

            para_text = ' '.join(para_text_lines).strip()
            if para_text:
                current_paragraphs.append({
                    'id': para_id,
                    'text': para_text
                })
            continue

        i += 1

    # Save last chapter if exists and not already seen
    if current_chapter and current_paragraphs:
        ch_id = current_chapter['id']
        if ch_id not in seen_chapters:
            current_chapter['paragraphs'] = current_paragraphs
            chapters.append(current_chapter)

    return chapters

def create_chapter_json(chapter_data):
    """Create a chapter in the workmaster.json format"""
    paragraphs = []

    for para in chapter_data['paragraphs']:
        paragraphs.append({
            "type": "paragraph",
            "id": para['id'],
            "text": para['text'],
            "thai_text": "",
            "vietnamese_text": "",
            "korean_text": "",
            "japanese_text": "",
            "Chinese_Tradition_text": "",
            "Chinese_Simplified_text": "",
            "tibetan_text": ""
        })

    # Create the full chapter structure
    chapter = {
        "type": "chapter",
        "id": chapter_data['id'],
        "status": "draft",
        "title": chapter_data['title'],
        "thai_title": "",
        "vietnamese_title": "",
        "korean_title": "",
        "japanese_title": "",
        "Chinese_Tradition_title": "",
        "Chinese_Simplified_title": "",
        "tibetan_title": "",
        "sections": [
            {
                "type": "section",
                "id": 1,
                "heading": "",
                "content": [
                    {
                        "type": "subsection",
                        "id": 1,
                        "heading": "",
                        "content": paragraphs
                    }
                ]
            }
        ]
    }

    return chapter

def main():
    print("Parsing section5_truths_and_paths_english.md for INQUIRY chapters...")
    chapters_data = parse_inquiry_chapters('/home/scott/gitrepos/RDGAsianMD/section5_truths_and_paths_english.md')

    print(f"Found {len(chapters_data)} unique inquiry chapters:")
    for ch in chapters_data:
        print(f"  Chapter {ch['id']}: {ch['title']} ({len(ch['paragraphs'])} paragraphs)")

    # Read existing workmaster.json
    print("\nReading workmaster.json...")
    with open('workmaster.json', 'r') as f:
        data = json.load(f)

    print(f"Current number of chapters: {len(data['chapters'])}")

    # Create a dict of new chapters by ID for easy lookup
    new_chapters_dict = {ch['id']: create_chapter_json(ch) for ch in chapters_data}

    # Update existing inquiry chapters by replacing them in place
    updated_count = 0

    for i in range(len(data['chapters'])):
        chapter_id = data['chapters'][i]['id']
        if chapter_id in new_chapters_dict:
            old_title = data['chapters'][i]['title']
            data['chapters'][i] = new_chapters_dict[chapter_id]
            print(f"  Updated Chapter {chapter_id}: {old_title}")
            updated_count += 1
            del new_chapters_dict[chapter_id]

    # Report any chapters from section5 that weren't in the JSON
    if new_chapters_dict:
        print(f"\n  Note: {len(new_chapters_dict)} inquiry chapters not found in workmaster.json:")
        for ch_id in sorted(new_chapters_dict.keys()):
            print(f"    Chapter {ch_id}: {new_chapters_dict[ch_id]['title']}")

    print(f"\nUpdated: {updated_count} inquiry chapters")
    print(f"Total chapters: {len(data['chapters'])}")

    # Write updated JSON back to file
    print("\nWriting updated workmaster.json...")
    with open('workmaster.json', 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print("✓ Successfully updated workmaster.json with inquiry chapters")

if __name__ == '__main__':
    main()

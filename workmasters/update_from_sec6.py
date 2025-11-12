#!/usr/bin/env python3
"""
Parse sec6WM.md and append Chapters 31-35 to workmaster.json
"""

import json
import re

def parse_sec6_md(filename):
    """Parse sec6WM.md and extract chapters with paragraphs"""
    with open(filename, 'r') as f:
        content = f.read()

    chapters = []
    lines = content.split('\n')

    current_chapter = None
    current_paragraphs = []

    i = 0
    while i < len(lines):
        line = lines[i]

        # Check for chapter heading: ## Chapter 31: TITLE
        chapter_match = re.match(r'^## Chapter (\d+):\s*(.+)$', line)
        if chapter_match:
            # Save previous chapter if exists
            if current_chapter and current_paragraphs:
                current_chapter['paragraphs'] = current_paragraphs
                chapters.append(current_chapter)

            # Start new chapter
            chapter_id = int(chapter_match.group(1))
            chapter_title = chapter_match.group(2).strip()
            current_chapter = {
                'id': chapter_id,
                'title': chapter_title
            }
            current_paragraphs = []
            i += 1
            continue

        # Check for paragraph ID: ### ID: p31-1
        para_id_match = re.match(r'^### ID:\s*(p\d+-\d+)$', line)
        if para_id_match:
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

    # Save last chapter
    if current_chapter and current_paragraphs:
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
    print("Parsing sec6WM.md...")
    chapters_data = parse_sec6_md('sec6WM.md')

    print(f"Found {len(chapters_data)} chapters:")
    for ch in chapters_data:
        print(f"  Chapter {ch['id']}: {ch['title']} ({len(ch['paragraphs'])} paragraphs)")

    # Read existing workmaster.json
    print("\nReading workmaster.json...")
    with open('workmaster.json', 'r') as f:
        data = json.load(f)

    # Work with flat structure
    print(f"Current number of chapters: {len(data['chapters'])}")

    # Convert parsed chapters to JSON format and append
    print("\nAdding chapters 31-35...")
    for chapter_data in chapters_data:
        chapter_json = create_chapter_json(chapter_data)
        data['chapters'].append(chapter_json)
        print(f"  Added Chapter {chapter_data['id']}: {chapter_data['title']}")

    print(f"\nNew total chapters: {len(data['chapters'])}")

    # Write updated JSON back to file
    print("\nWriting updated workmaster.json...")
    with open('workmaster.json', 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print("✓ Successfully updated workmaster.json")

    # Verify the addition
    print("\nVerification - Last 5 chapters:")
    for chapter in data['chapters'][-5:]:
        print(f"  Chapter {chapter['id']}: {chapter['title']}")

if __name__ == '__main__':
    main()

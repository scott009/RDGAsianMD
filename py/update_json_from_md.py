#!/usr/bin/env python3
"""
Script to update workmaster.json Section 5 content from sec5workmaster.md
"""

import json
import re

def parse_md_file(md_file):
    """Parse the MD file and extract chapters with their paragraphs"""

    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()

    chapters = {}

    # Split by chapter headers
    chapter_pattern = r'^## Chapter ([\d.]+): (.+)$'
    chapter_matches = list(re.finditer(chapter_pattern, content, re.MULTILINE))

    for i, match in enumerate(chapter_matches):
        chapter_id = match.group(1)
        chapter_title = match.group(2)
        start = match.end()

        # Find end of this chapter (start of next chapter or end of file)
        if i < len(chapter_matches) - 1:
            end = chapter_matches[i + 1].start()
        else:
            end = len(content)

        chapter_content = content[start:end]

        # Parse paragraphs within this chapter
        paragraphs = []
        para_pattern = r'^### ID: (p[\d.]+\-\d+)\n(.*?)(?=^### ID:|^## Chapter|\Z)'

        for para_match in re.finditer(para_pattern, chapter_content, re.MULTILINE | re.DOTALL):
            para_id = para_match.group(1)
            para_content = para_match.group(2).strip()

            # Check for Class line
            class_match = re.match(r'^#### Class: (.+)\n', para_content)
            para_class = None
            if class_match:
                para_class = class_match.group(1)
                # Remove class line from content
                para_content = para_content[class_match.end():].strip()

            paragraphs.append({
                'id': para_id,
                'text': para_content,
                'class': para_class
            })

        chapters[chapter_id] = {
            'title': chapter_title,
            'paragraphs': paragraphs
        }

    return chapters

def create_paragraph_json(para_id, text, para_class=None):
    """Create a paragraph JSON object"""
    para = {
        "type": "paragraph",
        "id": para_id,
        "text": text,
        "thai_text": "",
        "vietnamese_text": "",
        "korean_text": "",
        "japanese_text": "",
        "Chinese_Tradition_text": "",
        "Chinese_Simplified_text": "",
        "tibetan_text": ""
    }

    if para_class:
        para["class"] = para_class

    return para

def update_json_chapter(json_chapter, md_chapter_data):
    """Update a JSON chapter with MD content"""

    # Create a simple section structure with all paragraphs
    paragraphs = []
    for para in md_chapter_data['paragraphs']:
        paragraphs.append(create_paragraph_json(
            para['id'],
            para['text'],
            para.get('class')
        ))

    # Update chapter sections
    if not json_chapter.get('sections'):
        json_chapter['sections'] = []

    # Put all paragraphs in the first section
    if len(json_chapter['sections']) == 0:
        json_chapter['sections'].append({
            "type": "section",
            "id": 1,
            "heading": "",
            "content": []
        })

    json_chapter['sections'][0]['content'] = paragraphs

    # Clear any additional sections
    json_chapter['sections'] = json_chapter['sections'][:1]

def main():
    md_file = 'workmasters/sec5workmaster.md'
    json_file = 'workmasters/workmaster.json'

    print("Parsing MD file...")
    md_chapters = parse_md_file(md_file)
    print(f"Found {len(md_chapters)} chapters in MD file")

    print("\nLoading JSON file...")
    with open(json_file, 'r', encoding='utf-8') as f:
        json_data = json.load(f)

    # Find Section 5
    section5 = None
    section5_index = None
    for i, section in enumerate(json_data['content']):
        if section.get('type') == 'section' and section.get('id') == 5:
            section5 = section
            section5_index = i
            break

    if not section5:
        print("ERROR: Section 5 not found in JSON!")
        return

    print(f"Found Section 5 with {len(section5['chapters'])} chapters")

    # Update chapters
    print("\nUpdating chapters...")
    updated_count = 0
    empty_count = 0

    for json_chapter in section5['chapters']:
        chapter_id = str(json_chapter['id'])

        if chapter_id in md_chapters:
            md_data = md_chapters[chapter_id]

            # Update title to match MD
            json_chapter['title'] = md_data['title']

            # Update content
            if md_data['paragraphs']:
                update_json_chapter(json_chapter, md_data)
                updated_count += 1
                print(f"  Chapter {chapter_id}: Updated with {len(md_data['paragraphs'])} paragraphs")
            else:
                empty_count += 1
                print(f"  Chapter {chapter_id}: No content in MD (keeping empty)")
        else:
            empty_count += 1
            print(f"  Chapter {chapter_id}: Not found in MD (keeping empty)")

    # Save updated JSON
    json_data['content'][section5_index] = section5

    output_file = 'workmasters/workmaster.json'
    print(f"\nSaving updated JSON to {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)

    print("\n" + "="*80)
    print("SUMMARY:")
    print(f"  Chapters updated with content: {updated_count}")
    print(f"  Chapters remaining empty: {empty_count}")
    print(f"  Total chapters: {len(section5['chapters'])}")
    print("="*80)
    print("\nDone!")

if __name__ == '__main__':
    main()

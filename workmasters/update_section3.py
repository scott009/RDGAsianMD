#!/usr/bin/env python3
"""Update workmaster.json Section 3 with corrected content from sec3WM.md"""

import json
import re


def parse_markdown():
    """Parse sec3WM.md and return chapters with paragraphs"""
    with open('sec3WM.md', 'r') as f:
        content = f.read()

    chapters = {}
    chapter_sections = re.split(r'^## Chapter (\d+): (.+)$', content, flags=re.MULTILINE)

    for i in range(1, len(chapter_sections), 3):
        if i+2 > len(chapter_sections):
            break
        ch_num = chapter_sections[i]
        ch_title = chapter_sections[i+1]
        ch_content = chapter_sections[i+2]

        chapters[ch_num] = {'title': ch_title, 'paras': []}

        para_pattern = r'### ID: (p\d+-\d+)\s*\n(.*?)(?=\n### ID:|## Chapter |\Z)'
        for match in re.finditer(para_pattern, ch_content, re.DOTALL):
            para_id = match.group(1)
            para_text = ' '.join(match.group(2).strip().split())
            if para_text:
                chapters[ch_num]['paras'].append({
                    'id': para_id,
                    'text': para_text
                })

    return chapters


def create_paragraph_obj(para_id, text):
    """Create a standard paragraph object"""
    return {
        'type': 'paragraph',
        'id': para_id,
        'text': text,
        'thai_text': '',
        'vietnamese_text': '',
        'korean_text': '',
        'japanese_text': '',
        'Chinese_Tradition_text': '',
        'Chinese_Simplified_text': '',
        'tibetan_text': ''
    }


def replace_chapter_content(chapter, new_paras, title=None):
    """Replace entire chapter content with new paragraphs"""
    if title:
        chapter['title'] = title

    # Ensure sections exist
    if not chapter.get('sections'):
        chapter['sections'] = []
    if not chapter['sections']:
        chapter['sections'].append({
            'type': 'section',
            'id': 1,
            'heading': '',
            'content': []
        })

    section = chapter['sections'][0]

    # Find or create subsection
    subsection = None
    for item in section.get('content', []):
        if item.get('type') == 'subsection':
            subsection = item
            break

    if not subsection:
        subsection = {
            'type': 'subsection',
            'id': 1,
            'heading': '',
            'content': []
        }
        section['content'] = [subsection]

    # Replace all paragraphs
    subsection['content'] = [create_paragraph_obj(p['id'], p['text']) for p in new_paras]


def main():
    print("Parsing sec3WM.md...")
    md_chapters = parse_markdown()

    print("\nParsed chapters:")
    for ch_id, ch_data in md_chapters.items():
        ids = [p['id'] for p in ch_data['paras']]
        print(f"  Chapter {ch_id}: {len(ids)} paras - {', '.join(ids)}")

    print("\nLoading workmaster.json...")
    with open('workmaster.json', 'r') as f:
        data = json.load(f)

    # Find Section 3
    for section in data.get('content', []):
        if section.get('id') == 3:
            print("\nUpdating Section 3...")

            for chapter in section.get('chapters', []):
                ch_id = chapter.get('id')

                if ch_id == 8:
                    print("  Updating Chapter 8 (PREFACE)...")
                    if '8' in md_chapters:
                        replace_chapter_content(chapter, md_chapters['8']['paras'])
                        print(f"    Replaced with {len(md_chapters['8']['paras'])} paragraphs")
                        print(f"    Removed p8-5 (page number)")

    print("\nSaving workmaster.json...")
    with open('workmaster.json', 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print("✓ Done!")


if __name__ == '__main__':
    main()

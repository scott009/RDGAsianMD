#!/usr/bin/env python3
"""Update workmaster.json Section 1 with corrected content from sec1WM.md"""

import json
import re


def parse_markdown():
    """Parse sec1WM.md and return chapters with paragraphs"""
    with open('sec1WM.md', 'r') as f:
        content = f.read()

    chapters = {}

    # Split by chapter headers
    chapter_pattern = r'^## Chapter (\d+): (.+)$'
    parts = re.split(chapter_pattern, content, flags=re.MULTILINE)

    i = 1
    while i < len(parts):
        if i + 2 > len(parts):
            break

        ch_num = parts[i]
        ch_title = parts[i+1]
        ch_content = parts[i+2]

        # Check for subtitle
        subtitle_match = re.search(r'^### (.+?)(?:\n#### class subtitle)?(?=\n### ID:)', ch_content, re.MULTILINE)
        subtitle = subtitle_match.group(1).strip() if subtitle_match else None

        chapters[ch_num] = {
            'title': ch_title,
            'subtitle': subtitle,
            'paras': []
        }

        # Extract paragraphs
        para_pattern = r'### ID: (p\d+-\d+)\s*\n(.*?)(?=\n### ID:|## Chapter |\Z)'
        for match in re.finditer(para_pattern, ch_content, re.DOTALL):
            para_id = match.group(1)
            para_text = match.group(2).strip()
            # Remove any "class" directives
            para_text = re.sub(r'#### class \w+\s*\n?', '', para_text)
            para_text = ' '.join(para_text.split())

            if para_text:
                chapters[ch_num]['paras'].append({
                    'id': para_id,
                    'text': para_text
                })

        i += 3

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


def create_subsection_with_paras(paras, subsection_id=1, heading='', subtitle=None):
    """Create a subsection with paragraphs"""
    content = []

    # Add subtitle heading if present
    if subtitle:
        content.append({
            'type': 'subsection',
            'id': subsection_id,
            'heading': subtitle,
            'content': [create_paragraph_obj(p['id'], p['text']) for p in paras]
        })
    else:
        # Just add paragraphs directly as subsection content
        content.append({
            'type': 'subsection',
            'id': subsection_id,
            'heading': heading,
            'content': [create_paragraph_obj(p['id'], p['text']) for p in paras]
        })

    return content


def replace_chapter_content(chapter, new_paras, title=None, subtitle=None):
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

    # Create subsection with content
    section['content'] = create_subsection_with_paras(new_paras, subtitle=subtitle)


def main():
    print("Parsing sec1WM.md...")
    md_chapters = parse_markdown()

    print("\nParsed chapters:")
    for ch_id, ch_data in md_chapters.items():
        ids = [p['id'] for p in ch_data['paras']]
        subtitle_info = f" (subtitle: {ch_data['subtitle']})" if ch_data['subtitle'] else ""
        print(f"  Chapter {ch_id}: {ch_data['title']}{subtitle_info}")
        print(f"    {len(ids)} paras - {', '.join(ids)}")

    print("\nLoading workmaster.json...")
    with open('workmaster.json', 'r') as f:
        data = json.load(f)

    # Find Section 1
    for section in data.get('content', []):
        if section.get('id') == 1:
            print("\nUpdating Section 1...")
            new_chapters = []

            # Track if we've found chapters to update
            found_ch4 = False

            for chapter in section.get('chapters', []):
                ch_id = chapter.get('id')

                # Keep Chapter 1 and 2 as placeholders
                if ch_id in [1, 2]:
                    print(f"  Keeping Chapter {ch_id} as placeholder...")
                    new_chapters.append(chapter)

                # Update Chapter 3
                elif ch_id == 3:
                    print("  Updating Chapter 3...")
                    if '3' in md_chapters:
                        replace_chapter_content(
                            chapter,
                            md_chapters['3']['paras'],
                            md_chapters['3']['title'],
                            md_chapters['3']['subtitle']
                        )
                    new_chapters.append(chapter)

                # Check if Chapter 4 exists, update it
                elif ch_id == 4:
                    print("  Updating existing Chapter 4...")
                    found_ch4 = True
                    if '4' in md_chapters:
                        replace_chapter_content(
                            chapter,
                            md_chapters['4']['paras'],
                            md_chapters['4']['title']
                        )
                    new_chapters.append(chapter)

                # Skip Chapter 3a, it will become Chapter 5
                elif ch_id == '3a':
                    print("  Renaming Chapter 3a to Chapter 5...")
                    chapter['id'] = 5
                    if '5' in md_chapters:
                        replace_chapter_content(
                            chapter,
                            md_chapters['5']['paras'],
                            md_chapters['5']['title']
                        )
                    new_chapters.append(chapter)

                else:
                    new_chapters.append(chapter)

            # If Chapter 4 doesn't exist, create it
            if not found_ch4 and '4' in md_chapters:
                print("  Creating new Chapter 4...")
                new_chapter = {
                    'type': 'chapter',
                    'id': 4,
                    'status': 'draft',
                    'title': md_chapters['4']['title'],
                    'thai_title': '',
                    'vietnamese_title': '',
                    'korean_title': '',
                    'japanese_title': '',
                    'Chinese_Tradition_title': '',
                    'Chinese_Simplified_title': '',
                    'tibetan_title': '',
                    'sections': [{
                        'type': 'section',
                        'id': 1,
                        'heading': '',
                        'content': create_subsection_with_paras(md_chapters['4']['paras'])
                    }]
                }
                # Insert after Chapter 3
                insert_pos = 3  # After chapters 1, 2, 3
                new_chapters.insert(insert_pos, new_chapter)

            section['chapters'] = new_chapters
            print(f"  Section 1 now has {len(new_chapters)} chapters")

    print("\nSaving workmaster.json...")
    with open('workmaster.json', 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print("✓ Done!")


if __name__ == '__main__':
    main()

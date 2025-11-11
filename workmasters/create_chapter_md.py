#!/usr/bin/env python3
"""
Create markdown file for a specific chapter
"""

import json
import sys

def extract_chapter_content(chapter):
    """Extract all text content from a chapter"""
    lines = []

    # Add chapter title
    chapter_id = chapter.get('id', '')
    chapter_title = chapter.get('title', '')
    lines.append(f"# Chapter {chapter_id}: {chapter_title}\n")

    def process_content(content_list):
        for item in content_list:
            if isinstance(item, dict):
                item_type = item.get('type', '')

                if item_type == 'paragraph':
                    pid = item.get('id', '')
                    text = item.get('text', '')
                    class_name = item.get('class', '')

                    if class_name:
                        lines.append(f"### ID: {pid}")
                        lines.append(f"#### Class: {class_name}")
                        lines.append(text)
                        lines.append("")
                    else:
                        lines.append(f"### ID: {pid}")
                        lines.append(text)
                        lines.append("")

                elif item_type == 'section':
                    heading = item.get('heading', '')
                    if heading:
                        lines.append(f"## Section: {heading}\n")
                    if 'content' in item:
                        process_content(item['content'])

                elif item_type == 'subsection':
                    heading = item.get('heading', '')
                    if heading:
                        lines.append(f"### Subsection: {heading}\n")
                    if 'content' in item:
                        process_content(item['content'])

    # Process sections
    sections = chapter.get('sections', [])
    process_content(sections)

    return '\n'.join(lines)

def main(chapter_id, output_file):
    # Read the workmaster.json file
    with open('workmaster.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Find the chapter
    chapters = data.get('chapters', [])

    for chapter in chapters:
        if str(chapter.get('id')) == str(chapter_id):
            print(f"Found chapter {chapter_id}: {chapter.get('title')}")

            # Extract content
            content = extract_chapter_content(chapter)

            # Write to markdown file
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(content)

            print(f"Created {output_file}")
            return

    print(f"Chapter {chapter_id} not found!")

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python3 create_chapter_md.py <chapter_id> <output_file>")
        sys.exit(1)

    chapter_id = sys.argv[1]
    output_file = sys.argv[2]
    main(chapter_id, output_file)

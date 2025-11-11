#!/usr/bin/env python3
"""
Create markdown files for chapters 21 through 30.1
"""

import json

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

def main():
    # Read the workmaster.json file
    with open('workmaster.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Define the chapters we want to export
    chapter_ids = [
        '21', '21.1',
        '22',
        '23', '23.1',
        '24', '24.1', '24.2',
        '25', '25.1',
        '26', '26.1',
        '27', '27.1',
        '28', '28.1',
        '29', '29.1',
        '30', '30.1'
    ]

    chapters = data.get('chapters', [])
    created_files = []

    for chapter_id in chapter_ids:
        for chapter in chapters:
            if str(chapter.get('id')) == str(chapter_id):
                output_file = f"c{chapter_id}.md"

                print(f"Creating {output_file} for chapter {chapter_id}: {chapter.get('title')}")

                # Extract content
                content = extract_chapter_content(chapter)

                # Write to markdown file
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(content)

                created_files.append(output_file)
                break

    print(f"\nCreated {len(created_files)} files:")
    for f in created_files:
        print(f"  - {f}")

if __name__ == '__main__':
    main()

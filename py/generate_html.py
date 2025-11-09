#!/usr/bin/env python3
"""
Generate HTML file from workmaster.json Section 5 content
"""

import json
import sys

def is_inquiry_chapter(chapter_id):
    """Check if chapter ID indicates an inquiry chapter (has decimal)"""
    return '.' in str(chapter_id)

def remove_trailing_colon(title):
    """Remove trailing colon from title"""
    return title.rstrip(':')

def generate_html(json_file, output_file):
    """Generate HTML from JSON workmaster file"""

    # Load JSON
    print(f"Loading {json_file}...")
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Find Section 5
    section5 = None
    for section in data['content']:
        if section.get('type') == 'section' and section.get('id') == 5:
            section5 = section
            break

    if not section5:
        print("ERROR: Section 5 not found!")
        sys.exit(1)

    print(f"Found Section 5: {section5['title']}")
    print(f"Processing {len(section5['chapters'])} chapters...")

    # Start building HTML
    html = []
    html.append('<!DOCTYPE html>')
    html.append('<html lang="en">')
    html.append('<head>')
    html.append('  <meta charset="UTF-8">')
    html.append('  <meta name="viewport" content="width=device-width, initial-scale=1.0">')
    html.append(f'  <title>{section5["title"]}</title>')
    html.append('  <link rel="stylesheet" href="ada2.css">')
    html.append('</head>')
    html.append('<body>')
    html.append(f'  <h1>{section5["title"]}</h1>')
    html.append('')

    # Process each chapter
    for chapter in section5['chapters']:
        chapter_id = str(chapter.get('id', ''))
        chapter_title = chapter.get('title', '')
        is_inquiry = is_inquiry_chapter(chapter_id)

        # For main chapters, remove trailing colon
        if not is_inquiry:
            display_title = remove_trailing_colon(chapter_title)
            html.append(f'  <h2>{display_title}</h2>')
        else:
            # Inquiry chapters keep colon, use smaller heading with class
            html.append(f'  <h3 class="inquiry-chapter">{chapter_title}</h3>')

        # Process sections in chapter
        for section in chapter.get('sections', []):
            # Process content items
            for item in section.get('content', []):
                if item.get('type') == 'paragraph':
                    text = item.get('text', '')
                    item_class = item.get('class', '')
                    para_id = item.get('id', '')

                    # Build paragraph tag with optional class
                    if item_class:
                        html.append(f'  <p class="{item_class}" id="{para_id}">{text}</p>')
                    else:
                        html.append(f'  <p id="{para_id}">{text}</p>')

        html.append('')  # Blank line between chapters

    html.append('</body>')
    html.append('</html>')

    # Write HTML file
    print(f"\nWriting HTML to {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(html))

    print("Done!")

def main():
    json_file = 'workmasters/workmaster.json'
    output_file = 'workmasters/section5.html'

    generate_html(json_file, output_file)

if __name__ == '__main__':
    main()

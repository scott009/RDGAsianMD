#!/usr/bin/env python3
"""
Extract chapter information with all paragraph IDs from workmaster.json
Output format: Chapter [id]. [TITLE]: (p[id]-1, p[id]-2, ...)
"""

import json
import sys

def extract_paragraph_ids(obj, paragraph_ids):
    """Recursively extract all paragraph IDs from nested structure"""
    if isinstance(obj, dict):
        if obj.get('type') == 'paragraph' and 'id' in obj:
            paragraph_ids.append(obj['id'])
        # Recursively search in all dict values
        for value in obj.values():
            extract_paragraph_ids(value, paragraph_ids)
    elif isinstance(obj, list):
        # Recursively search in all list items
        for item in obj:
            extract_paragraph_ids(item, paragraph_ids)

def main():
    # Read the workmaster.json file
    with open('workmaster.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Process each chapter
    chapters = data.get('chapters', [])

    for chapter in chapters:
        chapter_id = chapter.get('id', 'unknown')
        chapter_title = chapter.get('title', 'NO TITLE')
        chapter_status = chapter.get('status', '')

        # Skip empty chapters if desired (but we'll show them with a note)
        if chapter_status == 'empty':
            print(f"Chapter {chapter_id}. [EMPTY]")
            continue

        # Extract all paragraph IDs from this chapter
        paragraph_ids = []
        extract_paragraph_ids(chapter, paragraph_ids)

        # Format paragraph IDs as a comma-separated list
        if paragraph_ids:
            para_list = ', '.join(paragraph_ids)
            print(f"Chapter {chapter_id}. {chapter_title}: ({para_list})")
        else:
            print(f"Chapter {chapter_id}. {chapter_title}: (no paragraphs)")

if __name__ == '__main__':
    main()

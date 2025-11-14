#!/usr/bin/env python3
"""
Create a translation template for a specific language and chapter range.
This extracts all paragraphs that need translation into a clean JSON format.

Usage:
    python create_translation_template.py --lang vietnamese --chapters 34-36
    python create_translation_template.py --lang japanese --chapters 34,35,36
"""

import json
import argparse
import sys
from pathlib import Path

def parse_chapter_range(chapters_str):
    """Parse chapter range like '34-36' or '34,35,36' into a list of chapter IDs."""
    chapter_ids = []

    if '-' in chapters_str:
        # Range format: 34-36
        start, end = chapters_str.split('-')
        chapter_ids = [str(i) for i in range(int(start), int(end) + 1)]
    else:
        # Comma-separated format: 34,35,36
        chapter_ids = [ch.strip() for ch in chapters_str.split(',')]

    return chapter_ids

def get_text_field_name(lang):
    """Get the appropriate text field name for the language."""
    lang_fields = {
        'thai': 'thai_text',
        'vietnamese': 'vietnamese_text',
        'japanese': 'japanese_text',
        'korean': 'korean_text',
        'simplified_chinese': 'simplified_chinese_text',
        'traditional_chinese': 'traditional_chinese_text',
        'tibetan': 'tibetan_text'
    }
    return lang_fields.get(lang.lower(), f'{lang.lower()}_text')

def get_title_field_name(lang):
    """Get the appropriate title field name for the language."""
    lang_fields = {
        'thai': 'thai_title',
        'vietnamese': 'vietnamese_title',
        'japanese': 'japanese_title',
        'korean': 'korean_title',
        'simplified_chinese': 'simplified_chinese_title',
        'traditional_chinese': 'traditional_chinese_title',
        'tibetan': 'tibetan_title'
    }
    return lang_fields.get(lang.lower(), f'{lang.lower()}_title')

def create_template(source_file, lang, chapter_ids, output_file):
    """Create a translation template from the source JSON file."""

    # Load source JSON
    try:
        with open(source_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: Source file '{source_file}' not found.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in source file: {e}")
        sys.exit(1)

    text_field = get_text_field_name(lang)
    title_field = get_title_field_name(lang)

    # Extract chapters to translate
    template = {}
    chapters_found = []

    for chapter in data.get('chapters', []):
        chapter_id = str(chapter.get('id'))

        if chapter_id in chapter_ids:
            chapters_found.append(chapter_id)

            template[chapter_id] = {
                'english_title': chapter.get('title', ''),
                'title': '',  # To be filled in
                'paragraphs': {}
            }

            # Extract paragraphs
            for para in chapter.get('content', []):
                para_id = para.get('id')
                if para_id:
                    template[chapter_id]['paragraphs'][para_id] = {
                        'english': para.get('text', ''),
                        'translation': '',  # To be filled in
                        'class': para.get('class', ''),  # Include class for poemlines, etc.
                    }

    # Check if all requested chapters were found
    missing_chapters = set(chapter_ids) - set(chapters_found)
    if missing_chapters:
        print(f"Warning: Chapters not found in source: {', '.join(sorted(missing_chapters))}")

    if not template:
        print(f"Error: No chapters found for IDs: {', '.join(chapter_ids)}")
        sys.exit(1)

    # Write template
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(template, f, ensure_ascii=False, indent=2)

    # Print statistics
    total_paragraphs = sum(len(ch['paragraphs']) for ch in template.values())
    print(f"\nTranslation template created: {output_file}")
    print(f"Language: {lang}")
    print(f"Chapters: {', '.join(sorted(chapters_found))}")
    print(f"Total paragraphs to translate: {total_paragraphs}")
    print(f"\nNext steps:")
    print(f"1. Edit {output_file} and fill in the 'title' and 'translation' fields")
    print(f"2. Run: python apply_translations.py --lang {lang} --file {output_file}")

def main():
    parser = argparse.ArgumentParser(
        description='Create a translation template for specific chapters',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('--lang', required=True,
                       help='Target language (e.g., vietnamese, japanese, korean)')
    parser.add_argument('--chapters', required=True,
                       help='Chapters to translate (e.g., "34-36" or "34,35,36")')
    parser.add_argument('--source', default='../RDGBook_English.json',
                       help='Source JSON file (default: ../RDGBook_English.json)')
    parser.add_argument('--output',
                       help='Output file (default: translations_{lang}_ch{chapters}.json)')

    args = parser.parse_args()

    # Parse chapter range
    chapter_ids = parse_chapter_range(args.chapters)

    # Determine output filename
    if args.output:
        output_file = args.output
    else:
        chapters_suffix = args.chapters.replace(',', '_').replace('-', '_')
        output_file = f"translations_{args.lang}_ch{chapters_suffix}.json"

    # Get absolute paths
    script_dir = Path(__file__).parent
    source_file = (script_dir / args.source).resolve()
    output_file = (script_dir / output_file).resolve()

    print(f"Creating translation template...")
    print(f"Source: {source_file}")
    print(f"Output: {output_file}")

    create_template(source_file, args.lang, chapter_ids, output_file)

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
Initialize a language file from RDGBook_English.json structure.
Creates a translation-only file with empty text/title fields ready for translation.

Usage:
    python initialize_language_file.py --lang thai
    python initialize_language_file.py --lang vietnamese --source ../RDGBook_English.json
"""

import json
import argparse
import sys
from pathlib import Path

def initialize_language_file(source_file, lang, output_file):
    """Create a language file with structure from English but empty text fields."""

    # Load English source
    try:
        with open(source_file, 'r', encoding='utf-8') as f:
            english_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: Source file '{source_file}' not found.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in source file: {e}")
        sys.exit(1)

    # Create new language structure
    lang_data = {
        'metadata': {
            'title': english_data.get('metadata', {}).get('title', 'Recovery Dharma'),
            'edition': english_data.get('metadata', {}).get('edition', '2.0'),
            'language': lang,
            'source_file': source_file.name,
            'base_language': 'english',
            'license': english_data.get('metadata', {}).get('license', 'CC BY-SA 4.0'),
            'json_version': english_data.get('metadata', {}).get('json_version', '3.1')
        },
        'chapters': []
    }

    # Copy chapter structure with empty text fields
    for chapter in english_data.get('chapters', []):
        new_chapter = {
            'type': chapter.get('type'),
            'id': chapter.get('id'),
            'status': chapter.get('status'),
            'title': '',  # Empty - to be filled with translation
            'content': []
        }

        # Copy content structure with empty text fields
        for content_item in chapter.get('content', []):
            new_content = {
                'type': content_item.get('type'),
                'id': content_item.get('id'),
                'class': content_item.get('class'),
                'text': ''  # Empty - to be filled with translation
            }
            new_chapter['content'].append(new_content)

        lang_data['chapters'].append(new_chapter)

    # Write language file
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(lang_data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Error writing output file: {e}")
        sys.exit(1)

    # Print statistics
    total_chapters = len(lang_data['chapters'])
    total_content = sum(len(ch['content']) for ch in lang_data['chapters'])

    print("\n" + "="*60)
    print("Language File Initialized")
    print("="*60)
    print(f"Source: {source_file}")
    print(f"Output: {output_file}")
    print(f"Language: {lang}")
    print()
    print(f"Total chapters: {total_chapters}")
    print(f"Total content items: {total_content}")
    print()
    print("Next steps:")
    print(f"1. Generate translation template:")
    print(f"   python create_translation_template.py --lang {lang} --chapters <range>")
    print(f"2. Fill in translations in the template file")
    print(f"3. Apply translations:")
    print(f"   python apply_translations.py --lang {lang} --file <template_file>")

def main():
    parser = argparse.ArgumentParser(
        description='Initialize a language file from English structure',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('--lang', required=True,
                       help='Target language (e.g., thai, vietnamese, korean)')
    parser.add_argument('--source', default='../RDGBook_English.json',
                       help='Source English JSON file (default: ../RDGBook_English.json)')
    parser.add_argument('--output',
                       help='Output file (default: ../RDGBook_{Lang}.json)')

    args = parser.parse_args()

    # Determine output filename
    if args.output:
        output_file = args.output
    else:
        # Capitalize first letter of language for filename
        lang_cap = args.lang.replace('_', ' ').title().replace(' ', '')
        output_file = f"../RDGBook_{lang_cap}.json"

    # Get absolute paths
    script_dir = Path(__file__).parent
    source_file = (script_dir / args.source).resolve()
    output_file = (script_dir / output_file).resolve()

    # Check if output file already exists
    if output_file.exists():
        response = input(f"\nWarning: {output_file} already exists. Overwrite? (yes/no): ")
        if response.lower() not in ['yes', 'y']:
            print("Aborted.")
            sys.exit(0)

    print(f"Initializing {args.lang} language file...")
    print(f"Source: {source_file}")
    print(f"Output: {output_file}")

    initialize_language_file(source_file, args.lang, output_file)

if __name__ == '__main__':
    main()

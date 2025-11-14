#!/usr/bin/env python3
"""
Apply translations from a translation file to the target JSON file.
This replaces the 'text' and 'title' fields with translations (translation-only files).

Usage:
    python apply_translations.py --lang vietnamese --file translations_vietnamese_ch34_36.json
    python apply_translations.py --lang thai --file translations_thai_ch34_36.json --target ../RDGBook_Thai.json

Note: Target files should contain only translated text in 'text' and 'title' fields.
English text is maintained separately in RDGBook_English.json.
"""

import json
import argparse
import sys
from pathlib import Path

def apply_translations(target_file, translation_file, lang, dry_run=False):
    """Apply translations from translation file to target JSON file."""

    # Use standard field names (translation-only files)
    text_field = 'text'
    title_field = 'title'

    # Load target JSON
    try:
        with open(target_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: Target file '{target_file}' not found.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in target file: {e}")
        sys.exit(1)

    # Load translations
    try:
        with open(translation_file, 'r', encoding='utf-8') as f:
            translations = json.load(f)
    except FileNotFoundError:
        print(f"Error: Translation file '{translation_file}' not found.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in translation file: {e}")
        sys.exit(1)

    # Statistics
    stats = {
        'chapters_updated': 0,
        'titles_updated': 0,
        'paragraphs_updated': 0,
        'paragraphs_skipped': 0,
        'chapters_not_found': [],
        'paragraphs_not_found': []
    }

    # Apply translations
    for chapter in data.get('chapters', []):
        chapter_id = str(chapter.get('id'))

        if chapter_id in translations:
            chapter_trans = translations[chapter_id]

            # Update chapter title
            if chapter_trans.get('title'):
                if dry_run:
                    print(f"Would update chapter {chapter_id} title: {chapter_trans['title'][:50]}...")
                else:
                    chapter[title_field] = chapter_trans['title']
                stats['titles_updated'] += 1

            # Update paragraphs
            for para in chapter.get('content', []):
                para_id = para.get('id')

                if para_id and para_id in chapter_trans.get('paragraphs', {}):
                    para_trans = chapter_trans['paragraphs'][para_id]
                    translation_text = para_trans.get('translation', '')

                    if translation_text:
                        if dry_run:
                            print(f"Would update {para_id}: {translation_text[:50]}...")
                        else:
                            para[text_field] = translation_text
                        stats['paragraphs_updated'] += 1
                    else:
                        stats['paragraphs_skipped'] += 1
                        if not dry_run:
                            print(f"Warning: Empty translation for {para_id}, skipping")

            stats['chapters_updated'] += 1

        elif chapter_id in [str(t) for t in translations.keys()]:
            # Chapter was in translation file but not found
            stats['chapters_not_found'].append(chapter_id)

    # Write updated JSON (if not dry run)
    if not dry_run:
        with open(target_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    # Print statistics
    print("\n" + "="*60)
    print(f"Translation Application {'(DRY RUN)' if dry_run else 'Complete'}")
    print("="*60)
    print(f"Target file: {target_file}")
    print(f"Translation file: {translation_file}")
    print(f"Language: {lang}")
    print(f"Text field: {text_field}")
    print(f"Title field: {title_field}")
    print()
    print(f"Chapters updated: {stats['chapters_updated']}")
    print(f"Titles updated: {stats['titles_updated']}")
    print(f"Paragraphs updated: {stats['paragraphs_updated']}")

    if stats['paragraphs_skipped'] > 0:
        print(f"Paragraphs skipped (empty translation): {stats['paragraphs_skipped']}")

    if stats['chapters_not_found']:
        print(f"\nWarning: Chapters in translation file but not found in target:")
        for ch_id in stats['chapters_not_found']:
            print(f"  - Chapter {ch_id}")

    if stats['paragraphs_not_found']:
        print(f"\nWarning: Paragraphs in translation file but not found in target:")
        for para_id in stats['paragraphs_not_found']:
            print(f"  - {para_id}")

    if not dry_run:
        print(f"\nSuccess! Updated {target_file}")
    else:
        print("\nThis was a dry run. Use --apply to actually update the file.")

def main():
    parser = argparse.ArgumentParser(
        description='Apply translations to target JSON file',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('--lang', required=True,
                       help='Target language (e.g., vietnamese, japanese, korean)')
    parser.add_argument('--file', required=True,
                       help='Translation file (e.g., translations_vietnamese_ch34_36.json)')
    parser.add_argument('--target',
                       help='Target JSON file (default: ../RDGBook_{Lang}.json)')
    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would be updated without actually updating')

    args = parser.parse_args()

    # Determine target filename
    if args.target:
        target_file = args.target
    else:
        # Capitalize first letter of language for filename
        lang_cap = args.lang.replace('_', ' ').title().replace(' ', '')
        target_file = f"../RDGBook_{lang_cap}.json"

    # Get absolute paths
    script_dir = Path(__file__).parent
    target_file = (script_dir / target_file).resolve()
    translation_file = (script_dir / args.file).resolve()

    print(f"Applying translations...")
    apply_translations(target_file, translation_file, args.lang, args.dry_run)

if __name__ == '__main__':
    main()

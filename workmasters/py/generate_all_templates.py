#!/usr/bin/env python3
"""
Generate translation templates for all remaining languages at once.

Usage:
    python generate_all_templates.py --chapters 34-36
    python generate_all_templates.py --chapters 34,35,36 --languages vietnamese,japanese
"""

import argparse
import subprocess
import sys
from pathlib import Path

# All supported languages
ALL_LANGUAGES = [
    'vietnamese',
    'japanese',
    'korean',
    'simplified_chinese',
    'traditional_chinese',
    'tibetan'
]

def generate_templates(chapters, languages):
    """Generate translation templates for specified languages."""

    script_dir = Path(__file__).parent
    create_script = script_dir / 'create_translation_template.py'

    if not create_script.exists():
        print(f"Error: create_translation_template.py not found at {create_script}")
        sys.exit(1)

    print("="*60)
    print("Generating Translation Templates")
    print("="*60)
    print(f"Chapters: {chapters}")
    print(f"Languages: {', '.join(languages)}")
    print()

    results = []

    for lang in languages:
        print(f"\n{'='*60}")
        print(f"Processing: {lang.upper()}")
        print(f"{'='*60}")

        cmd = [
            'python3',
            str(create_script),
            '--lang', lang,
            '--chapters', chapters
        ]

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            print(result.stdout)
            results.append({
                'language': lang,
                'status': 'success',
                'message': 'Template created successfully'
            })
        except subprocess.CalledProcessError as e:
            print(f"Error creating template for {lang}:")
            print(e.stderr)
            results.append({
                'language': lang,
                'status': 'error',
                'message': str(e)
            })

    # Print summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)

    success_count = sum(1 for r in results if r['status'] == 'success')
    error_count = len(results) - success_count

    print(f"Total languages: {len(results)}")
    print(f"Success: {success_count}")
    print(f"Errors: {error_count}")
    print()

    if success_count > 0:
        print("Successfully created templates for:")
        for r in results:
            if r['status'] == 'success':
                print(f"  ✓ {r['language']}")

    if error_count > 0:
        print("\nFailed to create templates for:")
        for r in results:
            if r['status'] == 'error':
                print(f"  ✗ {r['language']}: {r['message']}")

    print("\n" + "="*60)
    print("NEXT STEPS")
    print("="*60)
    print("1. Review and fill in translations in each template file")
    print("2. For each language, run:")
    print("   python apply_translations.py --lang <language> --file <template_file>")
    print()
    print("Example:")
    print("   python apply_translations.py --lang vietnamese --file translations_vietnamese_ch34_36.json")

def main():
    parser = argparse.ArgumentParser(
        description='Generate translation templates for multiple languages',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('--chapters', required=True,
                       help='Chapters to translate (e.g., "34-36" or "34,35,36")')
    parser.add_argument('--languages',
                       help=f'Comma-separated list of languages (default: all)\nAvailable: {", ".join(ALL_LANGUAGES)}')

    args = parser.parse_args()

    # Parse languages
    if args.languages:
        languages = [lang.strip() for lang in args.languages.split(',')]
        # Validate languages
        invalid = set(languages) - set(ALL_LANGUAGES)
        if invalid:
            print(f"Error: Invalid language(s): {', '.join(invalid)}")
            print(f"Available languages: {', '.join(ALL_LANGUAGES)}")
            sys.exit(1)
    else:
        languages = ALL_LANGUAGES

    generate_templates(args.chapters, languages)

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
Convert RDGBook JSON file to Markdown format.

Usage:
    python json_to_markdown.py --input ../RDGBook_English.json --output ../RDGBook_English.md
    python json_to_markdown.py --lang thai
"""

import json
import argparse
import sys
from pathlib import Path

def json_to_markdown(input_file, output_file):
    """Convert JSON book format to Markdown."""

    # Load JSON
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in input file: {e}")
        sys.exit(1)

    # Start building markdown
    markdown_lines = []

    # Add metadata header
    metadata = data.get('metadata', {})
    markdown_lines.append(f"# {metadata.get('title', 'Recovery Dharma')}")
    markdown_lines.append(f"")
    markdown_lines.append(f"**Edition:** {metadata.get('edition', '2.0')}")
    if metadata.get('language'):
        markdown_lines.append(f"**Language:** {metadata.get('language')}")
    markdown_lines.append(f"**License:** {metadata.get('license', 'CC BY-SA 4.0')}")
    markdown_lines.append(f"")
    markdown_lines.append("---")
    markdown_lines.append("")

    # Process chapters
    for chapter in data.get('chapters', []):
        chapter_id = chapter.get('id')
        chapter_title = chapter.get('title', '')

        # Skip chapters with no content
        if not chapter.get('content'):
            continue

        # Chapter heading
        if chapter_title:
            markdown_lines.append(f"## Chapter {chapter_id}: {chapter_title}")
        else:
            markdown_lines.append(f"## Chapter {chapter_id}")
        markdown_lines.append("")

        # Process content items
        for content_item in chapter.get('content', []):
            content_id = content_item.get('id')
            content_text = content_item.get('text', '')
            content_class = content_item.get('class', '')

            # Skip empty content
            if not content_text:
                continue

            # Add ID heading
            markdown_lines.append(f"### ID: {content_id}")

            # Add class info if present and notable
            if content_class and content_class not in ['', 'para']:
                markdown_lines.append(f"*[{content_class}]*")

            # Add text content
            markdown_lines.append(content_text)
            markdown_lines.append("")

    # Write markdown file
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(markdown_lines))
    except Exception as e:
        print(f"Error writing output file: {e}")
        sys.exit(1)

    # Statistics
    total_chapters = len([ch for ch in data.get('chapters', []) if ch.get('content')])
    total_content = sum(len(ch.get('content', [])) for ch in data.get('chapters', []))

    print("\n" + "="*60)
    print("Markdown Conversion Complete")
    print("="*60)
    print(f"Input: {input_file}")
    print(f"Output: {output_file}")
    print(f"Chapters: {total_chapters}")
    print(f"Content items: {total_content}")
    print(f"\nMarkdown file created successfully!")

def main():
    parser = argparse.ArgumentParser(
        description='Convert RDGBook JSON to Markdown',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('--input',
                       help='Input JSON file (default: ../RDGBook_English.json)')
    parser.add_argument('--output',
                       help='Output markdown file (default: ../RDGBook_{lang}.md)')
    parser.add_argument('--lang',
                       help='Language (if not using --input, will use RDGBook_{Lang}.json)')

    args = parser.parse_args()

    # Determine input filename
    if args.input:
        input_file = args.input
    elif args.lang:
        lang_cap = args.lang.replace('_', ' ').title().replace(' ', '')
        input_file = f"../RDGBook_{lang_cap}.json"
    else:
        input_file = "../RDGBook_English.json"

    # Determine output filename
    if args.output:
        output_file = args.output
    elif args.lang:
        lang_cap = args.lang.replace('_', ' ').title().replace(' ', '')
        output_file = f"../RDGBook_{lang_cap}.md"
    else:
        output_file = "../RDGBook_English.md"

    # Get absolute paths
    script_dir = Path(__file__).parent
    input_file = (script_dir / input_file).resolve()
    output_file = (script_dir / output_file).resolve()

    print(f"Converting JSON to Markdown...")
    json_to_markdown(input_file, output_file)

if __name__ == '__main__':
    main()

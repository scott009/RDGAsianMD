#!/usr/bin/env python3
"""
Script to fix duplicate paragraph IDs in the MD file by renumbering them sequentially
"""

import re

def main():
    input_file = 'sec5workmaster.md'

    print("Reading sec5workmaster.md...")
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Track current chapter
    current_chapter = None
    para_counter = 1
    changes = []

    print("\nProcessing paragraphs...")

    for i, line in enumerate(lines):
        # Detect chapter headers
        chapter_match = re.match(r'^## Chapter ([\d.]+):', line)
        if chapter_match:
            current_chapter = chapter_match.group(1)
            para_counter = 1
            print(f"\nChapter {current_chapter}:")

        # Detect paragraph IDs
        para_match = re.match(r'^### ID: (p[\d.]+)-(\d+)', line)
        if para_match and current_chapter:
            old_id = para_match.group(0).replace('### ID: ', '')
            expected_id = f"p{current_chapter}-{para_counter}"

            if old_id != expected_id:
                new_line = f"### ID: {expected_id}\n"
                lines[i] = new_line
                changes.append({
                    'line': i + 1,
                    'chapter': current_chapter,
                    'old': old_id,
                    'new': expected_id
                })
                print(f"  Line {i+1:4}: {old_id} → {expected_id}")

            para_counter += 1

    print(f"\n{'='*80}")
    print(f"SUMMARY:")
    print(f"  Total changes: {len(changes)}")

    if changes:
        print(f"\nSaving updated file...")
        with open(input_file, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        print(f"File saved successfully!")

        # Show summary by chapter
        from collections import defaultdict
        by_chapter = defaultdict(list)
        for change in changes:
            by_chapter[change['chapter']].append(change)

        print(f"\nChanges by chapter:")
        for chapter, ch_changes in sorted(by_chapter.items()):
            print(f"  Chapter {chapter}: {len(ch_changes)} changes")
    else:
        print("\nNo changes needed - all IDs are already sequential!")

if __name__ == '__main__':
    main()

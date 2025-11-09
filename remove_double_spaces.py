#!/usr/bin/env python3
"""
Script to remove double spaces between words in the MD file
"""

import re

def remove_double_spaces(text):
    """Remove multiple consecutive spaces, replacing with single space"""
    # Replace 2+ spaces with single space
    cleaned = re.sub(r' {2,}', ' ', text)
    return cleaned

def main():
    input_file = '/home/scott/gitrepos/RDGAsianMD/sec5workmaster.md'

    print("Reading sec5workmaster.md...")
    with open(input_file, 'r', encoding='utf-8') as f:
        original_text = f.read()

    print(f"Original file size: {len(original_text)} characters")

    # Find all instances of double spaces for reporting
    double_space_pattern = re.compile(r' {2,}')
    matches = double_space_pattern.findall(original_text)

    if matches:
        print(f"\nFound {len(matches)} instances of multiple spaces:")

        # Count by number of consecutive spaces
        from collections import Counter
        space_counts = Counter([len(m) for m in matches])
        for space_count, occurrences in sorted(space_counts.items()):
            print(f"  {space_count} spaces: {occurrences} occurrences")

        # Clean the text
        print("\nRemoving multiple spaces...")
        cleaned_text = remove_double_spaces(original_text)

        print(f"Cleaned file size: {len(cleaned_text)} characters")
        print(f"Characters removed: {len(original_text) - len(cleaned_text)}")

        # Save the cleaned text
        print(f"\nSaving cleaned file to {input_file}...")
        with open(input_file, 'w', encoding='utf-8') as f:
            f.write(cleaned_text)

        print("Done!")
    else:
        print("\nNo double spaces found. File is already clean!")

if __name__ == '__main__':
    main()

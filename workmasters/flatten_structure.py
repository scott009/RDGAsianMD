#!/usr/bin/env python3
"""
Flatten workmaster.json structure:
- Keep metadata as-is
- Remove nested section structure
- Create flat chapters array
"""

import json

def flatten_workmaster(input_file, output_file):
    """Flatten the nested section structure into a flat chapters array"""

    print(f"Reading {input_file}...")
    with open(input_file, 'r') as f:
        data = json.load(f)

    # Keep metadata
    new_structure = {
        "metadata": data.get("metadata", {})
    }

    # Extract all chapters from all sections into flat array
    all_chapters = []

    print("\nExtracting chapters from sections:")
    for section in data.get('content', []):
        section_title = section.get('title', 'unknown')
        chapters_in_section = section.get('chapters', [])

        if chapters_in_section:
            print(f"  {section_title}: {len(chapters_in_section)} chapters")
            all_chapters.extend(chapters_in_section)

    # Add flat chapters array to new structure
    new_structure['chapters'] = all_chapters

    print(f"\nTotal chapters extracted: {len(all_chapters)}")

    # Write flattened structure
    print(f"\nWriting to {output_file}...")
    with open(output_file, 'w') as f:
        json.dump(new_structure, f, indent=2, ensure_ascii=False)

    print("✓ Successfully flattened structure")

    # Verification
    print("\nVerification:")
    print(f"  Metadata fields: {list(new_structure['metadata'].keys())}")
    print(f"  Total chapters: {len(new_structure['chapters'])}")
    print(f"\n  First 3 chapters:")
    for ch in new_structure['chapters'][:3]:
        print(f"    {ch['id']}. {ch['title']}")
    print(f"\n  Last 3 chapters:")
    for ch in new_structure['chapters'][-3:]:
        print(f"    {ch['id']}. {ch['title']}")

if __name__ == '__main__':
    flatten_workmaster('workmaster.json', 'workmaster.json')

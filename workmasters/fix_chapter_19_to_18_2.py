#!/usr/bin/env python3
"""
Fix chapter 19: Change it to chapter 18.2 and replace all paragraphs with new content
"""

import json

def main():
    # Read the workmaster.json file
    with open('workmaster.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # New paragraph content
    new_paragraphs = [
        {
            "type": "paragraph",
            "id": "p18.22-1",
            "class": "inquirybullitt",
            "text": "Begin by making a list of the behaviors and actions associated with your addiction(s) that you consider harmful. Without exaggerating or minimizing, think about the things you have done that have created additional suffering to yourself and others.",
            "thai_text": "",
            "vietnamese_text": "",
            "korean_text": "",
            "japanese_text": "",
            "Chinese_Tradition_text": "",
            "Chinese_Simplified_text": "",
            "tibetan_text": ""
        },
        {
            "type": "paragraph",
            "id": "p18.2-2",
            "class": "inquirybullitt",
            "text": "For each behavior listed, write how you and others have suffered because of that behavior.",
            "thai_text": "",
            "vietnamese_text": "",
            "korean_text": "",
            "japanese_text": "",
            "Chinese_Tradition_text": "",
            "Chinese_Simplified_text": "",
            "tibetan_text": ""
        },
        {
            "type": "paragraph",
            "id": "p18.2-3",
            "class": "inquirybullitt",
            "text": "List any other costs or negative consequences you can think of, such as finances, health, relationships, sexual relations, or missed opportunities.",
            "thai_text": "",
            "vietnamese_text": "",
            "korean_text": "",
            "japanese_text": "",
            "Chinese_Tradition_text": "",
            "Chinese_Simplified_text": "",
            "tibetan_text": ""
        },
        {
            "type": "paragraph",
            "id": "p18.2-4",
            "class": "inquirybullitt",
            "text": "Do you notice any patterns? What are they? What are the ways that you might avoid or reduce suffering for yourself and others if you change these patterns?",
            "thai_text": "",
            "vietnamese_text": "",
            "korean_text": "",
            "japanese_text": "",
            "Chinese_Tradition_text": "",
            "Chinese_Simplified_text": "",
            "tibetan_text": ""
        },
        {
            "type": "paragraph",
            "id": "p18.2-5",
            "class": "inquirybullitt",
            "text": "How have your addictive behaviors been a response to trauma and pain? What are some ways you can respond to trauma and pain that nurture healing rather than avoidance?",
            "thai_text": "",
            "vietnamese_text": "",
            "korean_text": "",
            "japanese_text": "",
            "Chinese_Tradition_text": "",
            "Chinese_Simplified_text": "",
            "tibetan_text": ""
        },
        {
            "type": "paragraph",
            "id": "p18.2-6",
            "class": "inquirybullitt",
            "text": "If you have experienced trauma from discrimination, what are ways you can experience healing and practice self-care? Consider opportunities to support social justice while allowing yourself to heal and practice compassion for yourself and others.",
            "thai_text": "",
            "vietnamese_text": "",
            "korean_text": "",
            "japanese_text": "",
            "Chinese_Tradition_text": "",
            "Chinese_Simplified_text": "",
            "tibetan_text": ""
        }
    ]

    # Find and update chapter 19
    chapters = data.get('chapters', [])

    for chapter in chapters:
        if chapter.get('id') == '19' or chapter.get('id') == 19:
            print(f"Found chapter {chapter['id']}: {chapter.get('title')}")
            print(f"Changing chapter ID from 19 to '18.2'")

            # Update chapter ID
            chapter['id'] = '18.2'

            # Replace all content with new paragraphs
            # Assuming the paragraphs are in sections[0].content[0].content
            if chapter.get('sections') and len(chapter['sections']) > 0:
                section = chapter['sections'][0]
                if section.get('content') and len(section['content']) > 0:
                    subsection = section['content'][0]
                    subsection['content'] = new_paragraphs
                    print(f"Replaced paragraphs with {len(new_paragraphs)} new paragraphs")

            print("\nChapter updated successfully!")
            break
    else:
        print("Chapter 19 not found!")
        return

    # Write the updated data back to workmaster.json
    with open('workmaster.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print("\nworkmaster.json has been updated.")

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
Replace paragraphs in chapter 19.1 with new content
"""

import json

def main():
    # Read the workmaster.json file
    with open('workmaster.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # New paragraph content (with errors corrected)
    new_paragraphs = [
        {
            "type": "paragraph",
            "id": "p19.1-1",
            "class": "inquirybullitt",
            "text": "List situations, circumstances, and feelings that you have used harmful behavior to try to avoid.",
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
            "id": "p19.1-2",
            "class": "inquirybullitt",
            "text": "Name the emotions, sensations, and thoughts that come to mind when you abstain. Are there troubling memories, shame, grief, or unmet needs behind the craving? How can you meet these with compassion and patience?",
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
            "id": "p19.1-3",
            "class": "inquirybullitt",
            "text": "What things did you give up in your clinging to impermanent and unreliable solutions? For example, did you give up relationships, financial security, health, opportunities, legal standing, or other important things to maintain your addictive behaviors? What made the addiction more important to you than any of these things you gave up?",
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
            "id": "p19.1-4",
            "class": "inquirybullitt",
            "text": "Are you clinging to any beliefs that fuel craving and aversion, beliefs that deny the truth of impermanence, or beliefs about how things in life \"should\" be? What are they?",
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
            "id": "p19.1-5",
            "class": "inquirybullitt",
            "text": "If you have experienced discrimination-based trauma or social injustice, how can you meet the experience in a way that honors your true self, without creating more pain and suffering?",
            "thai_text": "",
            "vietnamese_text": "",
            "korean_text": "",
            "japanese_text": "",
            "Chinese_Tradition_text": "",
            "Chinese_Simplified_text": "",
            "tibetan_text": ""
        }
    ]

    # Find and update chapter 19.1
    chapters = data.get('chapters', [])

    for chapter in chapters:
        if chapter.get('id') == '19.1':
            print(f"Found chapter {chapter['id']}: {chapter.get('title')}")

            # Replace all content with new paragraphs
            if chapter.get('sections') and len(chapter['sections']) > 0:
                section = chapter['sections'][0]
                if section.get('content') and len(section['content']) > 0:
                    subsection = section['content'][0]
                    subsection['content'] = new_paragraphs
                    print(f"Replaced paragraphs with {len(new_paragraphs)} new paragraphs")

            print("\nChapter updated successfully!")
            break
    else:
        print("Chapter 19.1 not found!")
        return

    # Write the updated data back to workmaster.json
    with open('workmaster.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print("\nworkmaster.json has been updated.")

if __name__ == '__main__':
    main()

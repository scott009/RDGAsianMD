#!/usr/bin/env python3
"""
Add chapter 19 before chapter 19.1 with corrected text
"""

import json

def main():
    # Read the workmaster.json file
    with open('workmaster.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # New chapter 19 structure with corrected text
    new_chapter = {
        "type": "chapter",
        "id": "19",
        "status": "draft",
        "title": "THE SECOND NOBLE TRUTH:",
        "thai_title": "",
        "vietnamese_title": "",
        "korean_title": "",
        "japanese_title": "",
        "Chinese_Tradition_title": "",
        "Chinese_Simplified_title": "",
        "tibetan_title": "",
        "sections": [
            {
                "type": "section",
                "id": 1,
                "heading": "",
                "content": [
                    {
                        "type": "subsection",
                        "id": 1,
                        "heading": "",
                        "content": [
                            {
                                "type": "paragraph",
                                "id": "p19-1",
                                "class": "subtitle",
                                "text": "The Cause of Suffering",
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
                                "id": "p19-2",
                                "text": "As people who have become dependent on substances and behaviors, we've all experienced the sense of failure and hopelessness that comes from trying, and failing, to let go of our fixations. Addiction itself increases our suffering by creating a hope that both pleasure and escape can be permanent. We go through this suffering again and again because substances or behaviors can only give us temporary relief to our pain, our unhappiness, and our lost or damaged sense of self.",
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
                                "id": "p19-3",
                                "text": "Our refusal to accept the way things are leads to wanting, or craving, which is the cause of suffering. This excludes discrimination-based suffering and harm which do not need to be \"accepted\" but met with wise boundaries, wise action, and compassion. We don't suffer because of the way things are, but because we want — or think we \"need\" — those things to be different. We suffer because we cling to the idea that we can satisfy our own cravings, while ignoring the true nature of the world around us. Above all, we cling to the idea that we can hold on to impermanent and unreliable things, things that can't ever lead to real satisfaction or lasting happiness, without experiencing the suffering of one day losing them.",
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
                                "id": "p19-5",
                                "text": "Clinging to impermanent solutions for suffering results in craving. We experience craving like a thirst, an unsatisfied longing, and it can become a driving force in our lives. If craving goes beyond simple desire, which is a natural part of life, it often leads us to fixation, obsession, and the delusional belief that we can't be happy without getting what we crave. It warps our intentions so that we make choices that harm our selves and others. This repetitive craving and obsessive drive to satisfy it leads to what we now know as addiction. Addiction occupies the part of our mind that chooses — our will — and replaces compassion, kindness, generosity, honesty, and other intentions that might have been there.",
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
                                "id": "p19-7",
                                "text": "Many of us experience addiction as the loss of our freedom to choose; it's the addiction that seems to be making our choices for us. In the way we \"must have\" food, shelter, or water, our mind can tell us we \"must have\" some substance, buy or steal something, satisfy some lust, keep acting until we achieve some \"needed\" result; that we must protect ourselves at all cost and attack people with whom we disagree, or people who have something we want. This \"need\" also leads to an unsettled or agitated state of mind that tells us we'll only be happy if we get certain results or feel a certain way. We want to be someone we're not, or we don't want to be who we are.",
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
                                "id": "p19-8",
                                "text": "Conditions or circumstances in and of themselves don't cause suffering. They can cause pain or unpleasant experiences, but we add suffering on top of this when we think we \"need\" those circumstances to be different. We create even more suffering when we act out in ways that deny the reality of the circumstances and the reality of impermanence. Craving is the underlying motive that fuels unwise actions that create suffering.",
                                "thai_text": "",
                                "vietnamese_text": "",
                                "korean_text": "",
                                "japanese_text": "",
                                "Chinese_Tradition_text": "",
                                "Chinese_Simplified_text": "",
                                "tibetan_text": ""
                            }
                        ]
                    }
                ]
            }
        ]
    }

    # Find the position of chapter 19.1 and insert before it
    chapters = data.get('chapters', [])

    for i, chapter in enumerate(chapters):
        if chapter.get('id') == '19.1':
            print(f"Found chapter 19.1 at position {i}")
            print(f"Inserting new chapter 19 before it")
            chapters.insert(i, new_chapter)
            print("Chapter 19 inserted successfully!")
            break
    else:
        print("Chapter 19.1 not found!")
        return

    # Write the updated data back to workmaster.json
    with open('workmaster.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print("\nworkmaster.json has been updated.")
    print("\nCorrected errors:")
    print("- 'be haviors' → 'behaviors'")
    print("- 'crav ing' → 'craving' (multiple instances)")
    print("- 'dis agree' → 'disagree'")

if __name__ == '__main__':
    main()

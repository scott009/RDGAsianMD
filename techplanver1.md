# RDG Asian Translations Project Plan

## Project Overview

Transform the Recovery Dharma book into 6 Asian language editions, maintaining structural integrity and enabling efficient AI-assisted translation workflows.

---

## Target Languages (6)

1. **Thai** (English + Thai)
2. **Vietnamese** (English + Vietnamese)
3. **Korean** (English + Korean)
4. **Japanese** (English + Japanese)
5. **Chinese Traditional** (English + Traditional Chinese)
6. **Chinese Simplified** (English + Simplified Chinese)

**Note:** Tibetan has been eliminated from this phase.

---

## Document Structure

### Current Sections (8 total)

| Section | Title | Chapters | Paragraphs | Status |
|---------|-------|----------|------------|--------|
| 1 | Title and Legal and Dedication | 4 | 17 | ✓ Has content |
| 2 | Table of Contents | 4 | 19 | ✓ Has content |
| 3 | Preface | 1 | 5 | ✓ Has content |
| 4 | Introduction | 4 | 36 | ✓ Has content |
| **5** | **Truths and Paths** | **31** | **223** | **✓ Completed & Cleaned** |
| 6 | Community | 1 | 80 | ✓ Has content |
| 7 | Recovery is Possible | 1 | 25 | ✓ Has content |
| 8 | Personal Stories | 1 | 47 | ✓ Has content |

**Total:** 47 chapters, 452 paragraphs

---

## Work Completed (Section 5)

### Accomplishments ✓

1. **Chapter Renumbering**
   - Renumbered all chapters (12-30.1) to match source document
   - Fixed chapter IDs: 18→18.1, 21.→21, 21.1, 30→30.1

2. **MD File Cleaning**
   - Removed duplicate chapters (1500 → 753 lines)
   - Removed 518 instances of double spaces
   - Fixed 93 paragraph IDs to match new chapter numbers
   - All INQUIRY chapters properly designated with .x notation

3. **JSON Structure Enhancement**
   - Updated all 31 chapters with cleaned MD content (223 paragraphs)
   - Added `chapter_type` field: "narrative" or "inquiry"
   - Added `parent_chapter` field to link inquiry chapters to parent narratives
   - Maintained all translation field placeholders

4. **Documentation & Scripts**
   - Created transformation scripts for reproducibility:
     - `renumber_chapters.py`
     - `update_paragraph_ids.py`
     - `remove_double_spaces.py`
     - `fix_duplicate_paragraph_ids.py`
     - `update_json_from_md.py`
     - `add_chapter_type_fields.py`

5. **Git Management**
   - Committed to `scott` and `thomas` branches
   - Ready for pull request to `main` when appropriate

### Section 5 Structure Details

**Chapter Types:**
- **18 narrative chapters** - Core teaching content
- **13 inquiry chapters** - Reflection/practice exercises
  - 12 chapters with `.1` notation
  - 1 chapter with `.2` notation (24.2: Making Amends)

**Parent-Child Relationships:**
- All inquiry chapters linked to parent narratives via `parent_chapter` field
- Example: Chapter 24 (WISE INTENTION) has two inquiry children:
  - 24.1: INQUIRY OF WISE INTENTION
  - 24.2: MAKING AMENDS

---

## Project Roadmap

### Phase 1: Complete MD & JSON Integration

#### 1.1 Correct MD Files for Remaining Sections ☐
**Sections to process:** 1, 2, 3, 4, 6, 7, 8

**For each section:**
- Remove double spaces
- Verify/add paragraph IDs
- Check for duplicate content
- Ensure consistent formatting
- Validate chapter structure

**Existing MD files:**
```
section1_title_legal_dedication_english.md       (3.0K)
section2_table_of_contents_english.md           (3.1K)
section3_preface_english.md                     (2.3K)
section4_introduction_english.md                (13K)
section5_truths_and_paths_english.md            (174K) ✓ DONE
section6_community_english.md                   (28K)
section7_recovery_is_possible_english.md        (7.4K)
section8_personal_stories_english.md            (17K)
```

#### 1.2 Integrate Corrected MD into workmaster.json ☐
- Update all sections with corrected MD content
- Verify paragraph IDs match across all sections
- Add `chapter_type` and `parent_chapter` where applicable
- Maintain consistent structure across all sections

#### 1.3 Create Master MD File ☐
**Purpose:** Human-editable, readable version of entire document

**Structure:**
```markdown
# Recovery Dharma - Master Document

## Section 1: Title and Legal and Dedication
### Chapter 1: ...
#### ID: p1-1
[content]

## Section 2: Table of Contents
...

[continues through all 8 sections]
```

**Benefits:**
- Easy to read and review
- Version control friendly
- Can be used to regenerate JSON if needed
- Serves as authoritative source document

#### 1.4 Remove Tibetan Fields ☐
- Strip `tibetan_text` and `tibetan_title` from all paragraphs/chapters
- Update metadata to reflect 6 target languages
- Verify JSON structure integrity after removal

---

### Phase 2: Repository Setup & Language Split

#### 2.1 Prepare workmaster.json for Commit ☐
- Final validation of all sections
- Verify no duplicate IDs across entire document
- Confirm all 6 language fields present
- Generate summary statistics

#### 2.2 Commit to RDGBookAsian Repository ☐
- Location: `/RDGBookAsian` repo
- Create appropriate branch structure
- Document JSON structure in repo README
- Tag version for tracking

#### 2.3 Split into 6 Language-Specific Files ☐

**Output files:**
```
RDG_Thai.json
RDG_Vietnamese.json
RDG_Korean.json
RDG_Japanese.json
RDG_ChineseTraditional.json
RDG_ChineseSimplified.json
```

**Each file contains:**
- Full document structure (metadata, sections, chapters)
- English text (source + proofing reference)
- Target language text fields only (e.g., Thai file has only `english_text` + `thai_text`)
- All IDs, chapter_type, parent_chapter fields

**Benefits of splitting:**
- Smaller file sizes (faster loading/processing)
- Language-specific workflows
- Parallel translation work
- Easier to manage and version control
- Reduced merge conflicts

**File size estimate:**
- Current workmaster: ~435KB
- Per-language file: ~150-200KB (estimated)

---

### Phase 3: Translation Workflow

#### 3.1 Translation Process ☐

**For each language file:**

1. **AI-Assisted Translation**
   - Use LLM to translate English → target language
   - Preserve paragraph IDs and structure
   - Maintain chapter_type and hierarchy

2. **Human Proofing**
   - Native speaker review
   - Compare English source (included in file)
   - Verify cultural/spiritual context
   - Check technical terms

3. **Iteration**
   - Update based on feedback
   - Version control each iteration
   - Track translation progress per section

**Translation Fields:**
```json
{
  "id": "p12-1",
  "text": "English source text...",
  "thai_text": "ข้อความภาษาไทย...",
  "chapter_type": "narrative"
}
```

#### 3.2 Quality Assurance ☐
- Verify all paragraphs translated
- Check formatting consistency
- Validate JSON structure
- Test with sample readers

---

### Phase 4: Format Transformation

#### 4.1 Generate Output Formats ☐

**Target formats for each language:**
- **HTML** - Web viewing, interactive features
- **PDF** - Print-ready, distribution
- **EPUB** - E-readers
- **MOBI** - Kindle
- **Plain text** - Accessibility

#### 4.2 Format-Specific Features ☐
- Chapter navigation
- Inquiry exercises formatting
- Internal cross-references
- Table of contents generation
- Cultural-specific styling

---

## JSON Structure Reference

### Paragraph Structure
```json
{
  "type": "paragraph",
  "id": "p24-5",
  "text": "English text here...",
  "thai_text": "",
  "vietnamese_text": "",
  "korean_text": "",
  "japanese_text": "",
  "Chinese_Tradition_text": "",
  "Chinese_Simplified_text": "",
  "class": "inquirybullitt"  // optional
}
```

### Chapter Structure
```json
{
  "type": "chapter",
  "id": "24",
  "chapter_type": "narrative",
  "status": "draft",
  "title": "WISE INTENTION:",
  "thai_title": "",
  "vietnamese_title": "",
  "korean_title": "",
  "japanese_title": "",
  "Chinese_Tradition_title": "",
  "Chinese_Simplified_title": "",
  "sections": [...]
}
```

### Chapter with Parent
```json
{
  "type": "chapter",
  "id": "24.1",
  "chapter_type": "inquiry",
  "parent_chapter": "24",
  "status": "draft",
  "title": "INQUIRY OF WISE INTENTION:",
  "sections": [...]
}
```

---

## Technical Notes

### File Naming Conventions
- Source MD: `section[N]_[title]_english.md`
- Work files: `sec[N]workmaster.md`
- Master JSON: `workmaster.json`
- Language JSON: `RDG_[Language].json`

### Branch Strategy
- `main` - Stable releases only
- `scott` - Active development
- `thomas` - Parallel work/review
- Language branches: `translate-[lang]` (future)

### Backup Strategy
- Backup files excluded via `.gitignore`
- Use git tags for version milestones
- Keep transformation scripts for reproducibility

---

## Success Metrics

### Phase 1 Complete When:
- [ ] All 8 section MD files cleaned and validated
- [ ] workmaster.json fully updated from all MD files
- [ ] Master MD file created and verified
- [ ] Tibetan fields removed
- [ ] All chapter_type and parent_chapter fields added

### Phase 2 Complete When:
- [ ] workmaster.json committed to RDGBookAsian repo
- [ ] 6 language-specific JSON files created
- [ ] Each language file validated for structure
- [ ] File sizes optimized and documented

### Phase 3 Complete When:
- [ ] All 6 languages have complete translations
- [ ] Native speaker review completed for each language
- [ ] Quality assurance passed

### Phase 4 Complete When:
- [ ] All output formats generated for all 6 languages
- [ ] Format-specific features implemented
- [ ] Distribution-ready files created

---

## Current Status

**As of:** November 9, 2025

**Completed:**
- ✓ Section 5 fully processed and cleaned
- ✓ Chapter type and parent fields added
- ✓ Transformation scripts created
- ✓ Committed to scott and thomas branches

**Next Immediate Steps:**
1. Decide: Start on Phase 1.1 (correct other section MD files)?
2. Or: Start on Phase 1.4 (remove Tibetan fields)?
3. Or: Create split preview script to visualize Phase 2.3?

**Repository:** https://github.com/scott009/RDGAsianMD
**Branches:** scott, thomas (active); main (stable)

---

## Notes

- Keep English in all language files for proofing/context
- Maintain structural consistency across all language versions
- Document all transformations with scripts for reproducibility
- Use git branching for parallel translation work
- AI-assisted translation with human review is the workflow
- File size optimization critical for efficiency

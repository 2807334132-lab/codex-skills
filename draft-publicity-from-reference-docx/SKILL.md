---
name: draft-publicity-from-reference-docx
description: Draft Chinese publicity articles from new source materials by matching the writing style of reference Word documents. Use when the user provides one or more reference .docx files for tone, structure, headline style, and policy-news diction, plus a separate material file containing facts to turn into a宣传稿,新闻稿,工作成效稿, or民生实事稿.
---

# Draft Publicity From Reference Docx

## Workflow

1. Extract text from all provided `.docx` files.
2. Separate reference-style files from the source-material file.
3. Analyze reference style:
   - headline pattern, such as parallel phrases plus dash;
   - opening frame, such as民生导向、问题导向、整改成效;
   - paragraph rhythm, usually“问题/举措/成效/下一步”;
   - recurring official language and closing cadence.
4. Extract only factual points from the source material:
   - locations;
   - projects;
   - investment amounts;
   - quantities and completion status.
5. Draft in the reference style without inventing names, quotes, dates, statistics, or responsible units that are not present.
6. If the material lacks quotes, do not fabricate direct quotations; use narrative evaluation instead.
7. Keep the article polished, specific, and publication-ready, with a clear title and coherent transitions.

## Output

Return the finished article directly unless the user asks for a `.docx` deliverable. If creating a Word document, use the Documents skill and render/verify it before delivery.

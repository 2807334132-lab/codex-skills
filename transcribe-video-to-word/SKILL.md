---
name: transcribe-video-to-word
description: Extract and accurately transcribe spoken audio from local video or audio files, cross-check terminology and missed speech against burned-in video subtitles or slide text, repair gaps, and deliver a structured Word document. Use when the user asks for a verbatim/逐字稿/一句不差 transcript from MP4, MOV, MKV, WAV, M4A, or similar media, especially Chinese corporate presentations containing names, product terms, English abbreviations, numbers, or visible subtitles.
---

# Transcribe Video To Word

Produce a source-faithful transcript, not a summary. Treat speech recognition as a draft and use independent evidence before claiming completeness.

## Required companion skill

Use `documents:documents` when creating the final `.docx`. Follow its render-and-inspect gate. If LibreOffice is unavailable, perform structural checks and disclose that standard visual render QA was skipped.

## Workflow

1. Inspect the source path, file size, streams, and duration. Work in a task-local intermediate directory; put only final deliverables in the thread `outputs` directory.
2. Run `scripts/extract_media.py` to create a 16 kHz mono WAV. If the video has burned-in subtitles, also extract bottom-region frames every 2-4 seconds.
3. Transcribe with the strongest practical multilingual Whisper model. Prefer `faster-whisper` with `large-v3` or `turbo`, `language="zh"`, `beam_size=5`, word timestamps, and VAD. Preserve segment timestamps and confidence metadata in JSON.
4. Audit before editing:
   - gaps longer than 2 seconds between speech segments;
   - low-confidence words or segments;
   - names, companies, products, acronyms, model sizes, dates, money, percentages, and benchmark numbers;
   - suspicious homophones or grammatically impossible phrases.
5. If subtitles or presentation text are visible, OCR them as an independent correction source. Crop to the subtitle band before OCR; direct recognition on a known single-line crop is much faster than full-slide detection. Sample more densely only around uncertain passages.
6. Re-transcribe every unexplained gap as a short standalone clip with VAD disabled and a focused hotword list. Do not infer missing sentences only from surrounding prose.
7. Merge evidence with this priority:
   - clearly audible speech for wording and spoken order;
   - synchronized subtitle for Chinese characters, punctuation, and numbers;
   - slide text for official names, English spellings, and technical identifiers;
   - contextual inference only when evidence agrees; otherwise mark `[听不清]` or `[专名待核]`.
8. Preserve fillers, repetition, and spoken grammar when the user requests verbatim text. Correct recognition errors, not the speaker's style. Do not silently turn the transcript into publicity copy.
9. Store the corrected transcript as UTF-8 JSON with `start`, `end`, and `text`. Run `scripts/build_transcript_docx.py` to produce the initial Word file, then render, inspect every page, fix layout defects, and re-render.
10. Verify one transcript paragraph exists for every corrected JSON item, none are empty, the last spoken sentence is present, and all known gaps are resolved or explicitly marked.

## Environment and recovery

Read [references/workflow.md](references/workflow.md) when model installation, CUDA, OCR, or rendering needs setup or troubleshooting.

## User-facing report

Return only the final Word file unless the user asks for intermediates. State what evidence was used for correction, report any unresolved `[听不清]`/`[专名待核]` markers, and disclose if standard visual render QA could not run.


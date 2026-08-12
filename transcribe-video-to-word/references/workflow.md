# Video transcript workflow reference

## Tool selection

- Load the bundled workspace dependencies and use its Python runtime for document work.
- Discover `ffmpeg` with `where.exe ffmpeg`. On this user's Windows machine, a usable fallback may exist under Adobe After Effects `Support Files\Scripts\ScriptUI Panels\ffmpeg.exe`.
- Install transcription/OCR packages into the task's `work` directory, never into the managed runtime or global Python.
- Recommended transcription package: `faster-whisper`.
- Optional OCR package: `rapidocr_onnxruntime`.

## Typical setup

```powershell
& $workspacePython -m pip install --target work\pydeps faster-whisper
& $workspacePython -m pip install --target work\ocrdeps rapidocr_onnxruntime
```

Model download can stall on Hugging Face Xet. Retry with:

```powershell
$env:HF_HUB_DISABLE_XET='1'
```

Use a task-local model cache so downloads are resumable and do not pollute deliverables.

## CUDA acceleration

On NVIDIA systems, `faster-whisper` may fail with missing `cublas64_12.dll` or `cudnn64_9.dll`. Install compatible runtime wheels into separate task-local directories and add their `bin` folders to `PATH` for the transcription process. If compatibility remains uncertain, run CPU `int8`; accuracy is unchanged, only speed differs.

Do not run duplicate model-download processes. A timed-out shell can leave an orphaned Python process holding the Hugging Face cache lock. Inspect active processes before retrying.

## Baseline transcription pattern

Use a multilingual model, Chinese language lock, beam search, timestamps, and a short domain prompt. Keep raw results before correction.

```python
model = WhisperModel(model_name, device=device, compute_type=compute_type,
                     download_root=model_cache)
segments, info = model.transcribe(
    audio_path,
    language="zh",
    beam_size=5,
    vad_filter=True,
    word_timestamps=True,
    initial_prompt="中文公司介绍。准确识别公司名、产品名、技术术语、数字和英文缩写。",
)
```

For jargon-heavy material, create a hotword list only after names are independently visible in the slides or subtitles. Do not seed guessed spellings as facts.

## Gap detection and repair

Sort raw segments by start time and calculate `next.start - current.end`. Review gaps over 2 seconds, especially gaps longer than 8 seconds inside continuous narration. Extract each suspicious interval with 3-5 seconds of context on both sides and transcribe it separately with VAD disabled.

When short-clip transcription repeats or hallucinates, reduce the clip to the relevant passage and compare it against synchronized subtitle frames.

## OCR strategy

Full-slide OCR is useful for official product names but expensive. Use it only at slide changes or uncertain timestamps.

For burned-in bottom subtitles:

1. Scale frames to a consistent width such as 1280.
2. Crop only the bottom subtitle band, usually the lower 12-20%.
3. If the crop contains exactly one line, call RapidOCR with detection and orientation disabled:

```python
result, _ = engine(crop, use_det=False, use_cls=False, use_rec=True)
```

This is substantially faster than running detection over a full presentation slide. Sample every 4 seconds for a broad pass; resample at 1-2 seconds around uncertain speech.

OCR is evidence, not ground truth. White outlines, animated transitions, and mixed English/Chinese text can produce substitutions. Prefer stable repeated frames and slide headings for official spellings.

## Correction rules

- Keep a replacement glossary for repeated names, but review every replacement in context.
- Use time-specific overrides for severely corrupted passages; avoid broad substitutions that can change legitimate words.
- Preserve the original speech sequence.
- Keep exact numbers only when supported by audio, subtitle, or slide text.
- Never claim “一句不差” when unresolved markers remain.

## Word document QA

Use the `documents:documents` skill. A suitable transcript layout is:

- title and source filename;
- media duration and correction method;
- a short fidelity note;
- optional section headings based on presentation transitions;
- one paragraph per timestamped segment;
- quiet header/footer with page number.

After creation, check:

- corrected JSON item count equals transcript-style paragraph count;
- zero empty transcript paragraphs;
- no missing first or final sentence;
- page geometry and styles are explicit;
- rendered pages have no clipping, overlap, missing Chinese glyphs, or orphan headings.


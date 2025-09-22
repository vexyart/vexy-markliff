---
this_file: docs/530-vexy-markliff-spec.md
---

# Vexy Markliff Specification v1.1

## 1. Purpose & scope
- Provide a single CLI and Python library that converts Markdown/HTML ↔ XLIFF 2.1 while preserving structure, metadata, and round-trip fidelity.
- Reuse the HTML handling rules (`docs/510-prefs-html0.md`–`docs/512-prefs-html2.md`) and Markdown mapping (`docs/513-prefs-md.md`) verbatim—no duplicate logic.
- Stay within one-sentence scope: *"Fetch Markdown/HTML, convert to XLIFF (and back) with selectable storage modes for source/target text."*

## 2. Architecture overview
```
Markdown ─┐             ┌─► XLIFF 2.1 ─┐
          ├─► HTML ─► AST ├─► Units    ├─► Merge ─► HTML ─┬─► Markdown
HTML ─────┘             └─► Skeleton ─┘                 │
                                                     (optional)
```
- **Parser layer**: `markdown-it-py` (with curated `mdit-py-plugins`) and `lxml` for HTML.
- **Extractor**: walks the AST, applies Format Style annotations, and emits `(units, skeleton)` tuples.
- **Merger**: reinserts translated segments into the skeleton placeholders.
- **Metadata store**: attaches round-trip hints (Markdown markers, alignment keys) to each `<unit>`.

## 3. Conversion modes
### 3.1 One-document mode
CLI flag: `--mode=one-doc` with `--storage=source|target|both` (default `source`).

| Storage | XLIFF segment layout |
|---------|----------------------|
| `source` | `<segment><source>content</source></segment>` |
| `target` | `<segment><target>content</target></segment>` |
| `both`   | `<segment><source>content</source><target>content</target></segment>` |

### 3.2 Two-document mode
CLI flag: `--mode=two-doc --source-file=S --target-file=T`.

1. **Structural alignment**: match headings/list indices between S and T using deterministic AST traversal.
2. **Sentence alignment**: apply the same segmentation rules used in §1 of the HTML spec (respect `<s>` boundaries, split `<p>` by sentences).
3. **Fallback**: if structures diverge, fall back to sequential pairing and add `note` entries with alignment warnings.
4. **Result**: each `<segment>` carries a `state="translated"` flag when both sides populated.

## 4. Processing pipeline
```
load_content → normalize (newline, encoding) → render HTML → apply HTML rules → assemble XLIFF → write skeleton(s)
```
- **HTML rule application**: delegate to helpers described in `docs/510`, `docs/511`, `docs/512`.
- **Markdown hints**: attach metadata described in `docs/513 §4`.
- **Validation**: ensure every `<ph>` references an `originalData` node and all `<unit>` elements include `fs:fs`.

## 5. CLI specification (Fire commands)
```
vexy-markliff md2xliff INPUT OUTPUT [--mode=one-doc|two-doc] [--storage=source|target|both]
                                 [--target-file=FILE] [--src-lang=BCP47] [--trg-lang=BCP47]
                                 [--extensions=tables,footnotes,...] [--split-sentences]

vexy-markliff html2xliff INPUT OUTPUT [same switches as above]

vexy-markliff xliff2md INPUT OUTPUT [--respect-markdown-style]

vexy-markliff xliff2html INPUT OUTPUT

vexy-markliff batch-convert --input-dir DIR --output-dir DIR [--pattern '*.md'] [--parallel N]
```
- All CLI commands write skeleton files alongside the XLIFF when HTML structure requires it (`--skeleton-dir` default `./skeletons`).
- Default language codes come from config (see §7) and must be present when generating `<target>` nodes.

## 6. Python API surface
```python
from vexy_markliff import Converter, Config, TwoDocumentPair

config = Config(src_lang="en", trg_lang="es", mode="one-doc", storage="both")
converter = Converter(config)

xliff = converter.markdown_to_xliff(Path("guide.md"))
html  = converter.xliff_to_html(Path("guide.xlf"))
markdown = converter.xliff_to_markdown(Path("guide.xlf"))

pair = TwoDocumentPair(source=Path("en.md"), target=Path("es.md"))
xliff_parallel = converter.parallel_to_xliff(pair)
```
- `Converter` exposes high-level helpers; lower-level hooks (`parse_markdown`, `extract_units`) remain internal to prevent misuse.
- Results include `units`, `skeleton`, and `metadata` so calling code can post-process if needed.

## 7. Configuration
### 7.1 File (`vexy-markliff.yaml`)
```yaml
source_language: en
target_language: es
mode: one-doc
storage: source
extensions: [tables, footnotes, task_lists, strikethrough]
split_sentences: true
skeleton_dir: ./skeletons
preserve_whitespace: true
```
### 7.2 Environment overrides
```
VEXY_MARKLIFF_CONFIG=/abs/path/config.yaml
VEXY_MARKLIFF_SRC_LANG=fr
VEXY_MARKLIFF_TRG_LANG=de
VEXY_MARKLIFF_SKELETON_DIR=/tmp/skeletons
```

## 8. Validation & testing
- **Unit tests**: every converter function has a pytest that asserts both structure (presence of `fs:fs`) and content (round-trip equality).
- **Fixture coverage**: include Markdown with tables, task lists, front matter, HTML passthrough, forms, media, and ruby text.
- **Round-trip check**: `markdown → xliff → markdown` and `html → xliff → html` must be byte-stable modulo whitespace normalization.
- **Two-document smoke test**: verify alignment warnings appear when paragraph counts differ.
- **Performance guardrail**: 10k-line Markdown converts in <10 seconds on a typical laptop (document in WORK.md after benchmarking).

## 9. Dependencies
- Hard: `markdown-it-py`, `mdit-py-plugins`, `lxml`, `fire`, `pydantic`, `rich`.
- Optional: `nltk` or `spacy` for sentence splitting.
- Document choices in `DEPENDENCIES.md` with rationale (HTML parsing, CLI, validation).

## 10. Cross-reference quick sheet
| Topic | Document |
|-------|----------|
| HTML element handling | `docs/510-prefs-html0.md` |
| Void/media/form rules | `docs/511-prefs-html1.md` |
| Attribute encoding + reference table | `docs/512-prefs-html2.md` |
| Markdown mapping & metadata | `docs/513-prefs-md.md` |
| External spec | `external/901-xliff-spec-core-21.xml` |

This specification describes the behaviour the implementation must follow. Code changes that diverge from these rules require an explicit spec update first.

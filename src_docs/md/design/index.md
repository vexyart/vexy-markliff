# Design overview

!!! warning "Specification, not current behaviour"
    The pages in this section describe how `vexy-markliff` is meant to work. Most of it is not implemented in version 1.3. For what the code does today, see [XLIFF output](../output-format.md) and [Architecture](../architecture.md).

These notes were migrated from the project's design documents (originally `docs/500-intro.md` to `docs/540-extras.md` and `docs/700-sentencing.md`) and edited for consistency.

## Purpose and scope

One sentence: convert Markdown or HTML to XLIFF, and back, with a choice of where the source and target text are stored.

The converter should preserve document structure, inline markup and metadata well enough that a translated XLIFF file can be merged back into an HTML or Markdown document that differs from the original only in its text.

## Planned pipeline

```text
Markdown ─┐                ┌─► XLIFF units ─┐
          ├─► HTML ─► tree ┤                ├─► merge ─► HTML ─┬─► Markdown
HTML ─────┘                └─► skeleton ────┘                  │
                                                          (optional)
```

| Stage | Planned component |
|---|---|
| Parse | `markdown-it-py` (with selected `mdit-py-plugins`) for Markdown; `lxml` for HTML |
| Extract | Walk the tree, apply the [HTML mapping rules](html-rules.md), emit units and a skeleton |
| Merge | Put translated segments back into the skeleton placeholders |
| Metadata | Keep round-trip hints (Markdown markers, alignment keys) on each `<unit>` |

The processing order is: load content, normalize newlines and encoding, render HTML, apply the HTML rules, assemble the XLIFF, write the skeleton.

Validation after extraction: every `<ph>` references an `<originalData>` entry, and every `<unit>` carries `fs:fs`.

## Conversion modes

### One-document mode

The input is one document. A storage switch decides where its text goes:

| Storage | Segment layout |
|---|---|
| `source` (default) | `<segment><source>text</source></segment>` |
| `target` | `<segment><target>text</target></segment>` |
| `both` | `<segment><source>text</source><target>text</target></segment>` |

### Two-document mode

The input is a source document and an existing translation.

1. **Structural alignment.** Match headings and list positions between the two documents by walking both trees in the same order.
2. **Sentence alignment.** Split paragraphs with the same [segmentation](segmentation.md) rules on both sides.
3. **Fallback.** If the structures diverge, pair blocks in sequence and add a `<note>` with an alignment warning.
4. **Result.** Segments with both sides filled get `state="translated"`.

## Planned command line

```text
vexy-markliff md2xliff INPUT OUTPUT [--mode=one-doc|two-doc] [--storage=source|target|both]
                                    [--target-file=FILE] [--src-lang=BCP47] [--trg-lang=BCP47]
                                    [--extensions=tables,footnotes,...] [--split-sentences]
vexy-markliff html2xliff INPUT OUTPUT [same switches]
vexy-markliff xliff2md INPUT OUTPUT [--respect-markdown-style]
vexy-markliff xliff2html INPUT OUTPUT
vexy-markliff batch-convert --input-dir DIR --output-dir DIR [--pattern '*.md'] [--parallel N]
```

Skeleton files would be written next to the XLIFF (`--skeleton-dir`, default `./skeletons`). Language codes would accept full BCP 47 tags.

!!! note
    In version 1.3 only `md2xliff`, `html2xliff`, `xliff2md` and `xliff2html` exist, with `--source_lang` and `--target_lang`. See [Command line](../cli.md).

## Planned configuration

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

with environment overrides `VEXY_MARKLIFF_CONFIG`, `VEXY_MARKLIFF_SRC_LANG`, `VEXY_MARKLIFF_TRG_LANG` and `VEXY_MARKLIFF_SKELETON_DIR`.

## Acceptance criteria

- Every converter function has a test that checks structure (presence of `fs:fs`) and content (round-trip equality).
- Fixtures cover tables, task lists, front matter, raw HTML, forms, media and ruby text.
- `markdown → xliff → markdown` and `html → xliff → html` are byte-stable apart from whitespace normalization.
- Two-document mode reports alignment warnings when paragraph counts differ.

## Pages in this section

| Page | Content |
|---|---|
| [XLIFF 2.1 primer](xliff-primer.md) | The XLIFF structure the design targets, inline codes, ITS 2.0, a worked example |
| [HTML mapping rules](html-rules.md) | How each HTML element maps to units, groups, markers and placeholders |
| [Markdown mapping rules](markdown-rules.md) | How Markdown constructs map through HTML to XLIFF, and what metadata keeps the round trip lossless |
| [Sentence segmentation](segmentation.md) | Segmentation policy and candidate libraries |
| [Libraries and tools](tools.md) | Third-party libraries and formats referenced by the design |
| [Sample files](samples.md) | One passage in XLIFF, PO, TS and RESX |

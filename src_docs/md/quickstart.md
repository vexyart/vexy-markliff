# Quick start

This page takes one Markdown file to XLIFF and back, first with the CLI and then from Python.

## Prerequisites

- `vexy-markliff` is installed (see [Installation](installation.md)).
- You have a working directory you can write files into.

## Convert Markdown to XLIFF

1. Create a file named `guide.md`:

    ````markdown
    # Guide

    Save & quit with <kbd>Ctrl</kbd>+Q.

    ```python
    print("hi")
    ```
    ````

2. Convert it, with English as the source language and German as the target language:

    ```bash
    vexy-markliff md2xliff guide.md out/guide.xlf --source_lang=en --target_lang=de
    ```

    The command prints nothing and exits with status `0`. It creates the `out/` directory if it does not exist.

3. Open `out/guide.xlf`:

    ```xml
    <xliff version="2.1" xmlns="urn:oasis:names:tc:xliff:document:2.1">
      <file id="file_1" source-language="en" target-language="de">
        <trans-unit id="unit_1" state="new">
          <source>Guide</source>
        </trans-unit>
        <trans-unit id="unit_2" state="new">
          <source>Save &amp; quit with</source>
        </trans-unit>
        <trans-unit id="unit_3" state="new">
          <source>Ctrl</source>
        </trans-unit>
        <trans-unit id="unit_4" state="new">
          <source>+Q.</source>
        </trans-unit>
        <trans-unit id="unit_5" state="new">
          <source>print("hi")</source>
        </trans-unit>
      </file>
    </xliff>
    ```

What happened:

- `markdown-it-py` rendered the Markdown to HTML. The raw `<kbd>` tag passed through because HTML is enabled in the renderer.
- `lxml` parsed the HTML. Every non-empty text node and every non-empty tail text after an element became one unit, in document order.
- The heading, the three pieces of the paragraph and the code block each became a `<trans-unit>`, numbered `unit_1` to `unit_5`.
- The `&` was escaped to `&amp;` by the XML serializer.

## Convert XLIFF back to text

```bash
vexy-markliff xliff2md out/guide.xlf out/guide-back.md
```

`out/guide-back.md` now contains:

```html
<p>Guide</p>
<p>Save & quit with</p>
<p>Ctrl</p>
<p>+Q.</p>
<p>print("hi")</p>
```

The reverse conversion writes one `<p>` per unit, using the `<source>` text. It does not restore the heading, the `<kbd>` element or the code fence, and it does not use `<target>` text. See [XLIFF output](output-format.md#reading-xliff-back) for the exact rules.

## Do the same from Python

```python
from vexy_markliff import VexyMarkliff

converter = VexyMarkliff()

markdown = "# Guide\n\nSave & quit with <kbd>Ctrl</kbd>+Q.\n"
xliff = converter.markdown_to_xliff(markdown, "en", "de")
print(xliff)

restored = converter.xliff_to_markdown(xliff)
print(restored)
```

`markdown_to_xliff` returns the XLIFF document as a string. `xliff_to_markdown` returns the reconstructed text as a string. Neither method reads or writes files.

## Convert HTML

HTML input works the same way:

```bash
vexy-markliff html2xliff page.html page.xlf --source_lang=en --target_lang=fr
```

The text inside `<title>` is extracted too, because the parser walks the whole tree, including `<head>`.

## Next steps

- [Command line](cli.md) lists every command and flag.
- [Python API](api.md) documents the classes and exceptions.
- [Troubleshooting](troubleshooting.md) explains what to do when the CLI exits with status `1`.

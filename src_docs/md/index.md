# vexy-markliff

`vexy-markliff` converts Markdown and HTML documents into XLIFF files that translators can work on, and converts those XLIFF files back into text. It ships as a Python package with a command-line tool of the same name.

## What it does

You give it a Markdown or HTML file. It renders Markdown to HTML with `markdown-it-py`, walks the HTML tree with `lxml`, and collects every run of visible text. Each run becomes one translation unit in an XLIFF document, tagged with the source and target language codes you choose.

```bash
vexy-markliff md2xliff guide.md guide.xlf --source_lang=en --target_lang=de
```

For this input:

```markdown
# Guide

Save & quit with <kbd>Ctrl</kbd>+Q.
```

the tool writes:

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
  </file>
</xliff>
```

The reverse commands (`xliff2md`, `xliff2html`) read such a file and write one `<p>` element per unit.

## Current status

Version 1.3 is a deliberately small implementation. Read these limits before you plan a workflow around it:

- Text is extracted per text node, so inline markup splits a sentence into several units (`Save & quit with` / `Ctrl` / `+Q.` above). The markup itself is not kept.
- The reverse conversion uses the `<source>` text of each unit, not the `<target>`. It produces a flat list of `<p>` elements for both `xliff2md` and `xliff2html`; it does not restore headings, lists or Markdown syntax.
- The output uses XLIFF 1.2 element names (`trans-unit`, `source-language`) under the XLIFF 2.1 namespace. Standard XLIFF 2.1 files that use `<unit>`/`<segment>` are read as empty. See [XLIFF output](output-format.md).
- There is no skeleton file, no Format Style (`fs:fs`) annotation, no sentence segmentation and no two-document mode yet.

The [design notes](design/index.md) describe the full target behaviour: skeleton files, Format Style attributes, inline `<mrk>` and `<ph>` codes, and sentence-level segmentation. They are the specification the code is meant to grow into.

## Where to go next

- [Installation](installation.md): install the package and check the CLI.
- [Quick start](quickstart.md): convert one file each way.
- [Command line](cli.md): every command and flag.
- [Python API](api.md): `VexyMarkliff`, `ConversionConfig`, exceptions and models.
- [Architecture](architecture.md): how a document flows through the code.
- [Troubleshooting](troubleshooting.md): silent exits, empty output and language-code errors.

# Sample files

The same passage, the opening of Franz Kafka's *Die Verwandlung* in German with an English translation, stored in four localization formats. Use them to compare how each format pairs source and target text, and as test input when you work on readers for other formats.

| File | Format | Source/target pairing |
|---|---|---|
| [`609-samsa.xlf.xml`](../609-samsa.xlf.xml) | XLIFF 2 | `<unit>` per paragraph, `<segment>` per sentence, `<source>` and `<target>` |
| [`610-samsa.po.txt`](../610-samsa.po.txt) | GNU gettext PO | `msgid` (German) and `msgstr` (English) per sentence |
| [`611-samsa.ts.xml`](../611-samsa.ts.xml) | Qt Linguist TS | `<message>` with `<source>` and `<translation>` inside a `<context>` |
| [`612-samsa.resx.xml`](../612-samsa.resx.xml) | .NET RESX | `<data>` per sentence; English in `<value>`, German in `<comment>` |

The files carry `.xml` and `.txt` extensions so that a browser displays them instead of downloading them.

## XLIFF sample in detail

The XLIFF file shows the structure the [design](index.md) targets: one `<unit>` per paragraph and one `<segment>` per sentence, with the language pair on `<file>`:

```xml
<file id="samsa" srcLang="de" trgLang="en">
  <unit id="p2">
    <segment>
      <source>»Was ist mit mir geschehen?« dachte er.</source>
      <target>“What’s happened to me?” he thought.</target>
    </segment>
    <segment>
      <source>Es war kein Traum.</source>
      <target>It wasn’t a dream.</target>
    </segment>
  </unit>
</file>
```

Two details to notice:

- The sentences keep their own punctuation and quotation marks (`»…«` in German, `“…”` in English). A segmenter must not strip them.
- The file declares the namespace `urn:oasis:names:tc:xliff:document:2.1` and puts `srcLang`/`trgLang` on `<file>`. The XLIFF 2.1 standard uses the namespace `urn:oasis:names:tc:xliff:document:2.0` and puts `srcLang`/`trgLang` on the `<xliff>` root.

## Reading the sample with version 1.3

```bash
vexy-markliff xliff2html 609-samsa.xlf.xml samsa.html
```

The command exits with status `0` and writes an empty `samsa.html`, because the version 1.3 reader looks only for `<trans-unit>` elements. See [XLIFF output](../output-format.md#reading-xliff-back).

# Sentence segmentation

!!! warning "Specification and research notes"
    Version 1.3 does not split sentences. A paragraph without inline markup becomes one unit. `vexy_markliff.utils.split_sentences_simple` exists but is not called by the converter.

## Policy

The [HTML mapping rules](html-rules.md#text-blocks-and-headings) set three rules:

1. An `<s>` element is one `<segment>`. It is never split further.
2. A `<p>` element is split into sentences, one `<segment>` per sentence, all inside the paragraph's `<unit>`.
3. Other block elements stay one segment unless the HTML already marks sentences with `<s>`.

XLIFF allows segmentation to change later, inside the unit, so the splitter's job is a good first guess, not a final answer.

## Why a regular expression is not enough

`split_sentences_simple` splits on runs of `.`, `!` and `?`:

```python
>>> from vexy_markliff.utils import split_sentences_simple
>>> split_sentences_simple("Dr. Who? Yes. New sentence.")
['Dr', 'Who', 'Yes', 'New sentence']
```

It breaks after abbreviations and drops the punctuation that translators need. A usable splitter must handle abbreviations, numbers (`p. 55`), quotations, and scripts that use other terminators, such as `。` in Chinese and Japanese or `।` in Hindi.

## Reference: Unicode text segmentation

Unicode Standard Annex #29, [Unicode Text Segmentation](https://www.unicode.org/reports/tr29/), defines default boundaries for grapheme clusters, words and sentences. Its sentence rules work on character properties (`STerm`, `ATerm`, `Close`, `Sp` and others) and are the baseline that ICU and most libraries tailor. The default rules do not know about abbreviations, which is why the libraries below add language-specific rules or models.

## Candidate libraries

The project's research compared these Python options. Check each project's licence, language coverage and maintenance status before adopting one.

| Library | Approach | Notes from the research |
|---|---|---|
| [pySBD](https://github.com/nipunsadvilkar/pySBD) | Rule-based (port of the Ruby pragmatic segmenter) | Deterministic, about 22 languages, good on messy text such as OCR and email |
| syntok | Rule-based, pure Python | Small and fast; aimed at Indo-European languages |
| sentencex | Rule-based with language fallbacks (Wikimedia) | Wide language coverage |
| wtpsplit ("Segment any Text") | Transformer models | Many languages; handles missing punctuation; can be adapted to a domain |
| [Stanza](https://stanfordnlp.github.io/stanza/) | Neural pipeline per language | Accurate; heavier dependency |
| [spaCy](https://spacy.io/api/sentencizer) | `sentencizer` (rule-based) or dependency parser | `sentencizer` is fast; the parser is slower and model-dependent |
| NLTK Punkt | Unsupervised model | Common baseline for European languages |
| BlingFire | Compiled finite-state models | Fast; platform-dependent binaries |

Rule-based splitters are fast, offline and deterministic, which suits a converter that must give the same output every time. Model-based splitters cope better with unusual text at the cost of large dependencies.

pySBD can also run as a spaCy pipeline component, so a project that already uses spaCy can swap segmenters without changing the rest of its pipeline.

## Marking boundaries in text

When a language model inserts sentence boundaries, the research notes suggest the Unicode pair U+2E28 LEFT DOUBLE PARENTHESIS `⸨` and U+2E29 RIGHT DOUBLE PARENTHESIS `⸩` as delimiters: they are rare in natural text, are a matched open/close pair in Unicode, and do not collide with Markdown or HTML syntax. A marked paragraph looks like `⸨My name is Jonas E. Smith.⸩ ⸨Please turn to p. 55.⸩`.

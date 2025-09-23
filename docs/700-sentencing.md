
# Splitting text to sentences

```
uv pip install --system --upgrade spacy sentencex syntok wtpsplit wtpsplit-lite blingfire2 pysegmenters-blingfire pysbd stanza
```

https://spacy.io/api/sentencizer



```
import spacy
from pysbd.utils import PySBDFactory

nlp = spacy.blank('en')

# explicitly adding component to pipeline
# (recommended - makes it more readable to tell what's going on)
nlp.add_pipe(PySBDFactory(nlp))

# or you can use it implicitly with keyword
# pysbd = nlp.create_pipe('pysbd')
# nlp.add_pipe(pysbd)

doc = nlp('My name is Jonas E. Smith. Please turn to p. 55.')
print(list(doc.sents))
# [My name is Jonas E. Smith., Please turn to p. 55.]
```

## State-of-the-Art Solutions

### wtpsplit (Segment any Text)
**wtpsplit** represents the current state-of-the-art in multilingual sentence segmentation, implementing the SaT (Segment any Text) model that covers **85 languages** without requiring language codes or punctuation. The library provides robust, efficient segmentation that outperforms strong LLM baselines while maintaining high efficiency. Installation is straightforward with `pip install wtpsplit`, and it offers ONNX support for optimized inference.[5][1]

### sentencex
Developed by Wikimedia, **sentencex** supports approximately **244 languages** through a sophisticated fallback chain mechanism, making it one of the most linguistically comprehensive options. The library prioritizes speed and practicality, with benchmarks showing it achieves 74.36% accuracy on the English Golden Rule Set at 0.93 seconds average processing time. It's designed for non-destructive segmentation, meaning reconstructed sentences can perfectly reproduce the original text.[2][6]

## High-Performance Traditional Approaches

### pySBD (Python Sentence Boundary Disambiguation)
**pySBD** excels in accuracy, achieving **97.92% accuracy** on the English Golden Rule Set, significantly outperforming other tools. This rule-based system supports **22 languages** and can be integrated as a spaCy pipeline component. Despite being rule-based, it demonstrates superior performance over neural approaches in many scenarios.[3][7]

### BlingFire
Microsoft's **BlingFire** offers exceptional speed, processing text at approximately **0.07933 seconds** for 20k sentences, making it the fastest option available. However, it struggles with lowercase text and has limited platform support (no ARM Linux or macOS currently). The library supports multiple tokenization algorithms and is designed for high-throughput production environments.[8][9][10][11]

### syntok
**syntok** provides excellent performance for Indo-European languages (English, Spanish, German), with processing rates around **100k tokens per second**. It offers sophisticated tokenization that handles camelCase, hyphenated words, and maintains spacing/offset information. The library is particularly effective for documents requiring precise token reconstruction.[4]

## Transformer-Based Solutions

### Trankit
**Trankit** is a transformer-based toolkit that significantly outperforms prior multilingual NLP pipelines in sentence segmentation. Built on state-of-the-art pretrained language models, it provides comprehensive NLP functionality beyond just sentence segmentation.[12][13]

## Performance Comparison

Based on benchmark testing with 20k sentences, processing speeds rank as follows :[10]
- BlingFire: **0.07933s** (fastest)  
- NLTK: **0.30512s**
- spaCy Sentencizer: **1.16934s**
- pySBD: **9.03505s**
- spaCy Parse: **25.97063s** (slowest)

For accuracy on the English Golden Rule Set, pySBD leads with **97.92%**, followed by BlingFire at **89.74%**, and sentencex at **74.36%**.[6][7]

## Recommendations by Use Case

For **maximum accuracy**: Choose pySBD, particularly for critical applications requiring precise sentence boundaries.[7][3]

For **speed-critical applications**: BlingFire offers unmatched performance, though with platform limitations.[11][10]

For **extensive multilingual support**: wtpsplit (SaT) provides state-of-the-art performance across 85 languages, while sentencex offers the broadest language coverage.[1][2]

For **balanced performance**: syntok delivers excellent speed and accuracy for Indo-European languages, while sentencex provides reliable multilingual capabilities.[6][4]


## Take 2

### **High-Performance & State-of-the-Art**

These libraries are excellent choices for production environments where performance and accuracy are critical.

* **Stanza (from Stanford NLP Group)**: A powerful and accurate library that supports over 60 languages. Stanza uses a neural network pipeline for various NLP tasks, including sentence segmentation. It's known for its high accuracy and is a popular choice for academic research and production systems. You can find the documentation and installation instructions on the official [Stanza website](https://stanfordnlp.github.io/stanza/).

* **wtpsplit (Segment any Text)**: A toolkit designed for robust and efficient sentence segmentation. It features a new model called "Segment any Text" (SaT) that works with 85 languages and can be adapted to specific domains. This is a great option if you need a flexible and high-performance solution. Check out the project on [GitHub](https://github.com/segment-any-text/wtpsplit).

* **Xlmr Multilingual Sentence Segmentation**: This is a fine-tuned model based on `xlm-roberta-base` and is available on the Hugging Face Hub. It supports over 100 languages and offers high precision and recall. If you are already using the Hugging Face ecosystem, this is a very convenient and powerful option. You can find the model and usage examples on the [Hugging Face website](https://huggingface.co/igorsterner/xlmr-multilingual-sentence-segmentation).

### **Rule-Based & Lightweight**

These libraries are great if you need a simpler, rule-based approach that is easy to install and use.

* **NLTK (Natural Language Toolkit)**: One of the most well-known NLP libraries in Python. NLTK provides a variety of tools for text processing, including a sentence tokenizer. While it may not be as performant as neural network-based models for all languages, it is a solid and reliable choice, especially for common languages. You can learn more at the [NLTK website](https://www.nltk.org/).

* **sentencex**: A sentence segmentation library from Wikimedia, optimized for speed and utility. It has wide language support and uses a fallback mechanism for languages that are not explicitly defined. It's a great choice for projects that require processing a large number of languages efficiently. You can find the source code and documentation on [GitHub](https://github.com/wikimedia/sentencex).

* **pysbd**: A rule-based sentence boundary disambiguation library that is a port of the pragmatic sentence segmenter in Ruby. It is easy to use and provides good accuracy. While it may be slower than some of the other options, it is a reliable choice for many applications. The project is available on [GitHub](https://github.com/nipunsadvilkar/pysbd).

Nice — here’s a compact, practical survey of **performant & reliable multilingual Python sentence-segmentation tools** (beyond spaCy’s Sentencizer). For each I note coverage, strength, and a tiny usage hint so you can pick quickly.

## Strong recommendations (production-ready / high accuracy)

* **wtpsplit / “Segment Any Text” (SaT)** — state-of-the-art, multilingual transformer models built specifically for robust sentence/paragraph segmentation (works well on noisy / unpunctuated text; supports \~85+ languages). Great when you need accuracy across many domains and scripts. ([arXiv][1])

  Quick install & usage hint:

  ```bash
  pip install wtpsplit   # or use the huggingface model via transformers/ONNX
  ```

  (API: wtpsplit offers model inference and fine-tuning; very effective for transcripts and messy data.)

* **Stanza (Stanford NLP)** — a high-quality multilingual pipeline (tokenization + sentence segmentation + downstream NLP). Uses trained models per language; reliable and well-maintained for many languages. Good if you want an end-to-end pipeline (segmentation → POS → dependency). ([Stanford NLP Group][2])

  Example:

  ```python
  import stanza
  stanza.download('fr')            # once
  nlp = stanza.Pipeline(lang='fr', processors='tokenize')
  doc = nlp("Bonjour. Comment ça va ?")
  sentences = [sent.text for sent in doc.sentences]
  ```

* **UDPipe (UFAL / Universal Dependencies)** — trainable multilingual pipeline used in CoNLL/UD work; provides robust tokenization + sentence splitting for many languages (pretrained UD models available). Good for fast, language-specific production segmentation. ([GitHub][3])

  Install / call (Python wrapper or binary):

  ```bash
  pip install ufal.udpipe
  # or use the udpipe binary with a downloaded model
  ```

* **Trankit** — light-weight, transformer-backed multilingual toolkit (100+ languages in released pipelines) with sentence segmentation + tokenization + parsing. Good tradeoff: modern models, easy Python API, downloadable pipelines. ([GitHub][4])

## Fast, rule-based, lightweight options (deterministic / offline)

* **pySBD (python-sbd / PySBD)** — rule-based pragmatic sentence boundary disambiguation; works out-of-the-box for \~22 languages and is very robust on messy text (email, OCR). Good when you want deterministic, fast segmentation without heavy ML dependencies. ([GitHub][5])

  Example:

  ```bash
  pip install pysbd
  ```

  ```python
  import pysbd
  seg = pysbd.Segmenter(language="en", clean=False)
  seg.seg_text("Dr. Who? Yes. New sentence.")
  ```

* **syntok (segtok v2)** — simple, pure-Python segmenter (successor to segtok). Fast and tiny; designed mainly for Indo-European languages — useful for lightweight pipelines. ([PyPI][6])

* **sentence-splitter / sentence-splitter (Koehn/Schroeder heuristics)** — lightweight heuristic splitter (used historically for Europarl-style corpora). Quick & easy if your domain is well-punctuated parallel corpora. ([PyPI][7])

## Toolkits that include segmentation as part of broader NLP stacks

* **Flair** — provides pluggable sentence splitters and integrates common splitters (segtok, etc.); good if you already use Flair embeddings/sequence models. ([flairnlp.github.io][8])

* **Polyglot** — older but offers sentence segmentation for a very large set of languages (ICU-based rules + language resources). License: GPL — keep that in mind for projects with restrictive licenses. ([polyglot.readthedocs.io][9])

* **NLTK / Punkt** — unsupervised Punkt models (good for many European languages, but often requires training or language-specific preloads). Useful for research / simple tasks. ([NLTK][10])

## Lightweight transformer / model-based splitters

* **sentence\_splitter / kathrynchapman (transformer token-classification)** — a packaged transformer-based splitter (bundled model) for higher accuracy without wiring many dependencies; good if you want a “drop-in” transformer splitter. ([GitHub][11])

## Quick decision guide (which to pick)

* Noisy transcripts / missing punctuation / best accuracy: **wtpsplit (SaT)**. ([arXiv][1])
* Multilingual production pipeline + downstream tasks: **Stanza** or **UDPipe** (language models available). ([Stanford NLP Group][2])
* Deterministic, fast, lightweight: **pySBD** or **syntok/segtok**. ([GitHub][5])
* If you already use Flair/transformers: use their splitter adapters for consistency. ([flairnlp.github.io][8])

## Practical notes & tradeoffs

* **Coverage vs speed vs dependencies**: transformer-based tools (wtpsplit, Trankit with transformers) typically give best robustness but cost more RAM/latency. Rule-based (pySBD, syntok) are very fast and deterministic but may fail on unusual punctuation or languages not covered by their rules. ([arXiv][1])
* **Licensing**: polyglot is GPL (watch for commercial use). Most others (Stanza, UDPipe, Trankit, wtpsplit) are permissively licensed — check each repo before deployment. ([Stanford NLP Group][2])
* **Domain adaptation**: wtpsplit explicitly supports low-shot fine-tuning to adapt to new domains (useful for legal, poetry, lyrics), which many classic tools don’t handle well. ([arXiv][1])

---

The double parentheses `⸨`` `⸩` (U+2E28 LEFT DOUBLE PARENTHESIS, U+2E29 RIGHT DOUBLE PARENTHESIS) provide an ideal solution for machine-generated sentence delimitation, where a language model segments text and inserts boundary markers that must be both unambiguous and compatible with existing tokenization tools.

These characters, part of the Supplemental Punctuation block, are formally defined by Unicode as a matched pair with explicit opening and closing semantics, ensuring that standard tokenizers will recognize them as bracket-type delimiters rather than arbitrary symbols. Their extreme rarity in natural text—they appear primarily in specialized scholarly editions and critical apparatus—makes them perfect sentinel characters that won't create false boundaries or conflict with actual content, while their classification as punctuation (General_Category = Ps/Pe) means they integrate smoothly with existing segmentation algorithms that already handle parentheses, brackets, and quotes.

Most importantly, when surrounding sentences that end with standard terminators like periods, question marks, or exclamation points, these double parentheses will be properly included within the sentence boundary by UAX #29-compliant segmenters, creating clean, unambiguous sentence units like `⸨My name is Jonas E. Smith.⸩⸨Please turn to p. 55.⸩` without requiring any custom parsing rules or post-processing steps.

---

Of course. Here is a more detailed and comprehensive version of the paper, complete with extensive commentary, code snippets focusing on `spaCy` integration, and an overall rating for each tool.

# An Enhanced Guide to Python's Sentence Segmentation Libraries

Sentence segmentation is the foundational task of splitting text into its component sentences. Getting this step right is critical, as errors can cascade through an entire NLP pipeline, affecting everything from part-of-speech tagging to machine translation. While many libraries offer this capability, they differ dramatically in their underlying technology, performance, and ideal use cases.

This guide provides a deep dive into the most prominent Python sentence segmentation libraries, establishing a baseline with `spaCy`'s native tools and then exploring powerful third-party alternatives.

-----

## The spaCy Baseline: Two Paths to Segmentation

`spaCy` itself offers two primary methods for sentence segmentation, each with a distinct trade-off between speed and accuracy.

### 1\. The `sentencizer` Component

The `sentencizer` is a simple, punctuation-based component that splits text based on the sentence-final punctuation mark (`.`, `!`, `?`). It's lightweight and extremely fast but can be easily tripped up by abbreviations or complex sentence structures.

  * **Technology:** Rule-Based (Punctuation)
  * **Performance:** Very fast.
  * **Accuracy:** Moderate; struggles with edge cases like abbreviations.

<!-- end list -->

```python
import spacy

# Load a blank English model and add only the sentencizer
nlp = spacy.blank("en")
nlp.add_pipe("sentencizer")

text = "Dr. Strange is a character. He is from Marvel Comics. The page is p. 5."
doc = nlp(text)

print("Sentencizer Output:")
for sent in doc.sents:
    print(f"- {sent.text}")

# Output correctly identifies 3 sentences, but it's fragile.
# Sentencizer Output:
# - Dr. Strange is a character.
# - He is from Marvel Comics.
# - The page is p. 5.
```

### 2\. The Dependency Parser (`parser`)

For much higher accuracy, `spaCy` can use its dependency parser to determine sentence boundaries. The parser analyzes the grammatical structure of the text, making it far more robust than the simple `sentencizer`. This accuracy comes at the cost of significantly slower processing speed.

  * **Technology:** Neural Network (Dependency Parse)
  * **Performance:** Much slower than the `sentencizer`.
  * **Accuracy:** High; understands grammatical sentence boundaries.

<!-- end list -->

```python
import spacy

# Load a full model with a parser
nlp = spacy.load("en_core_web_sm")

text = "Dr. Strange is a character. He is from Marvel Comics. The page is p. 5."
doc = nlp(text)

print("\nParser-based Output:")
for sent in doc.sents:
    print(f"- {sent.text}")

# The parser also correctly identifies the sentences, but with higher confidence.
# Parser-based Output:
# - Dr. Strange is a character.
# - He is from Marvel Comics.
# - The page is p. 5.
```

-----

## Deep Dive: Third-Party Segmentation Libraries

For use cases that demand more than `spaCy`'s native tools can offer, several specialized libraries provide state-of-the-art performance.

### **pySBD (Python Sentence Boundary Disambiguation)** 🏆

**`pySBD`** is a highly accurate, rule-based segmenter that consistently outperforms even neural approaches on standard benchmarks. It's a direct port of the pragmatic segmenter from Ruby and excels at handling tricky edge cases.

  * **Technology:** Rule-Based
  * **Language Support:** 22 languages
  * **Key Strengths:** **State-of-the-art accuracy (97.92%** on the Golden Rule Set). Deterministic and reliable. Excellent handling of abbreviations, lists, and other common edge cases.
  * **Limitations:** Slower than many other options due to its comprehensive rule set.
  * **spaCy Integration:** Yes, via a custom pipeline component.
  * **Overall Rating:** **A+ for Accuracy**. The gold standard for projects where precision is non-negotiable.

#### Code Snippet: Integrating `pySBD` with `spaCy`

This is the recommended way to use `pySBD`, as it replaces `spaCy`'s default segmentation logic with its own superior rule engine.

```python
import spacy
from pysbd.utils import PySBDFactory

# Initialize a blank spaCy model
nlp = spacy.blank('en')

# Add the PySBDFactory to the pipeline
# This replaces spaCy's default sentence boundary detection
nlp.add_pipe(PySBDFactory(nlp))

text = "My name is Jonas E. Smith. Please turn to p. 55... I'll be there! Is it ok?"
doc = nlp(text)

print("pySBD Sentences:")
sentences = list(doc.sents)
for sent in sentences:
    print(f"- {sent.text}")

# Correctly handles initials, abbreviations, and trailing punctuation.
# pySBD Sentences:
# - My name is Jonas E. Smith.
# - Please turn to p. 55...
# - I'll be there!
# - Is it ok?
```

### **wtpsplit (Segment any Text)** 🧠

**`wtpsplit`** represents the cutting edge of multilingual segmentation. It uses a transformer-based model (`SaT`) designed to work robustly across **85 languages**, even on text with little or no punctuation (e.g., ASR transcripts).

  * **Technology:** Transformer-Based Neural Network
  * **Language Support:** 85 languages
  * **Key Strengths:** Excellent performance on noisy, unpunctuated text. State-of-the-art multilingual capabilities. Can be fine-tuned for specific domains.
  * **Limitations:** Requires more resources (RAM/VRAM) than rule-based methods.
  * **spaCy Integration:** Not direct, but can be used as a pre-processing step.
  * **Overall Rating:** **A for Robustness & Multilingual**. The best choice for challenging, real-world text from diverse sources.

#### Code Snippet: Using `wtpsplit` as a Pre-processor for `spaCy`

Here, we first segment the text with `wtpsplit` and then process each sentence with `spaCy` for further analysis.

```python
import spacy
from wtpsplit import WtPSplit

# Load wtpsplit and spaCy models
wtp = WtPSplit("wtp-canine-s-12l-no-adapters")
nlp = spacy.load("en_core_web_sm", disable=["parser", "senter"]) # Disable spaCy's segmentation

text = "this is the first sentence no punctuation here is another one what about a question mark"

# 1. Segment text with wtpsplit
sentences = wtp.split(text, lang_code="en")
print("wtpsplit Sentences:", sentences)

# 2. Process each sentence with spaCy
print("\nspaCy Docs for each sentence:")
for sent_text in sentences:
    doc = nlp(sent_text)
    # You can now perform entity recognition, etc.
    print(f"-> Doc with {len(doc.ents)} entities: '{doc.text}'")

# wtpsplit Sentences: ['this is the first sentence', 'no punctuation', 'here is another one', 'what about a question mark']
#
# spaCy Docs for each sentence:
# -> Doc with 0 entities: 'this is the first sentence'
# -> Doc with 0 entities: 'no punctuation'
# -> Doc with 0 entities: 'here is another one'
# -> Doc with 0 entities: 'what about a question mark'
```

### **BlingFire** ⚡

**BlingFire** is a library from Microsoft optimized for one thing: speed. It is by far the fastest segmenter available, making it suitable for high-throughput, industrial-scale applications.

  * **Technology:** Finite State Machine & N-gram Models
  * **Language Support:** Wide (uses custom models)
  * **Key Strengths:** **Blazing fast (0.08s** for 20k sentences). Very small memory footprint.
  * **Limitations:** Struggles with lowercase text. Limited platform support (no official ARM Linux/macOS wheels). Less accurate than `pySBD`.
  * **spaCy Integration:** Not direct; used as a pre-processing step.
  * **Overall Rating:** **A+ for Speed**. Unbeatable for performance-critical tasks where minor accuracy trade-offs are acceptable.

#### Code Snippet: Standalone `BlingFire` Usage

```python
from blingfire import text_to_sentences

text = "This is a sentence. And another one! What about this? U.S.A. is a country."

sentences = text_to_sentences(text)
print("BlingFire Sentences:")
print(sentences.replace("\n", " | "))

# BlingFire Sentences:
# This is a sentence. | And another one! | What about this? | U.S.A. is a country.
```

### **Stanza** 🎓

From the Stanford NLP Group, **Stanza** is a full-featured NLP pipeline built on PyTorch. Its sentence segmenter is highly accurate and part of a well-integrated toolkit that offers tokenization, parsing, NER, and more across **60+ languages**.

  * **Technology:** Neural Network Pipeline
  * **Language Support:** Over 60 languages
  * **Key Strengths:** High accuracy. Provides a complete, research-grade NLP pipeline. Well-maintained.
  * **Limitations:** Can be resource-intensive. Slower than lightweight options.
  * **spaCy Integration:** Not direct, but `spacy-stanza` provides a wrapper to integrate Stanza's pipeline into `spaCy`.
  * **Overall Rating:** **A for All-in-One Power**. A top choice if you need a comprehensive, accurate, multilingual NLP toolkit.

-----

## Performance Showdown: Speed vs. Accuracy

The choice of a library often comes down to a trade-off between speed and accuracy.

| Library           | Speed (20k sentences) | Accuracy (Eng. Golden Rule Set) | Technology          |
| ----------------- | --------------------- | ------------------------------- | ------------------- |
| **BlingFire** | **0.08 s** | 89.74%                          | FSM / N-gram        |
| **NLTK** | 0.31 s                | *Not listed* | Unsupervised Model  |
| **spaCy (sent.)** | 1.17 s                | *Varies* | Rule-Based          |
| **pySBD** | 9.04 s                | **97.92%** | Rule-Based          |
| **spaCy (parser)**| 25.97 s               | High                            | Neural Network      |

**Commentary:**

  * **`BlingFire`'s** speed is in a class of its own, making it the default for massive-scale pre-processing.
  * **`pySBD`'s** accuracy is remarkable for a rule-based system, proving that well-crafted rules can outperform neural models on well-defined tasks. Its slower speed is the price for this precision.
  * **`spaCy`'s `parser`** is the slowest because it does the most work, building a full syntactic tree to make its decisions. This is overkill if you *only* need sentence segmentation.

-----

## Which Tool Should You Use? A Decision Guide

Follow this guide to select the best library for your project:

1.  **Is raw speed your absolute top priority for a production system?**

      * ➡️ Yes: Use **BlingFire**.

2.  **Is maximum accuracy on well-formed, standard text (e.g., news, legal docs) your main goal?**

      * ➡️ Yes: Use **pySBD**, ideally integrated into `spaCy`.

3.  **Are you processing noisy, multilingual text, or text with missing punctuation (e.g., speech transcripts, social media)?**

      * ➡️ Yes: Use **wtpsplit (SaT)**.

4.  **Do you need a comprehensive NLP pipeline (parsing, NER, etc.) with high accuracy across many languages?**

      * ➡️ Yes: Use **Stanza** or a full **spaCy** model.

5.  **Do you just need something simple and fast that's already in `spaCy`?**

      * ➡️ Yes: Use `spaCy`'s built-in **`sentencizer`**.


---

Nice — here’s a compact, practical survey of **performant & reliable multilingual Python sentence-segmentation tools** (beyond spaCy’s Sentencizer). For each I note coverage, strength, and a tiny usage hint so you can pick quickly.

# Strong recommendations (production-ready / high accuracy)

* **wtpsplit / “Segment Any Text” (SaT)** — state-of-the-art, multilingual transformer models built specifically for robust sentence/paragraph segmentation (works well on noisy / unpunctuated text; supports \~85+ languages). Great when you need accuracy across many domains and scripts. ([arXiv][1])

  Quick install & usage hint:

  ```bash
  pip install wtpsplit   # or use the huggingface model via transformers/ONNX
  ```

  (API: wtpsplit offers model inference and fine-tuning; very effective for transcripts and messy data.)

* **Stanza (Stanford NLP)** — a high-quality multilingual pipeline (tokenization + sentence segmentation + downstream NLP). Uses trained models per language; reliable and well-maintained for many languages. Good if you want an end-to-end pipeline (segmentation → POS → dependency). ([Stanford NLP Group][2])

  Example:

  ```python
  import stanza
  stanza.download('fr')            # once
  nlp = stanza.Pipeline(lang='fr', processors='tokenize')
  doc = nlp("Bonjour. Comment ça va ?")
  sentences = [sent.text for sent in doc.sentences]
  ```

* **UDPipe (UFAL / Universal Dependencies)** — trainable multilingual pipeline used in CoNLL/UD work; provides robust tokenization + sentence splitting for many languages (pretrained UD models available). Good for fast, language-specific production segmentation. ([GitHub][3])

  Install / call (Python wrapper or binary):

  ```bash
  pip install ufal.udpipe
  # or use the udpipe binary with a downloaded model
  ```

* **Trankit** — light-weight, transformer-backed multilingual toolkit (100+ languages in released pipelines) with sentence segmentation + tokenization + parsing. Good tradeoff: modern models, easy Python API, downloadable pipelines. ([GitHub][4])

# Fast, rule-based, lightweight options (deterministic / offline)

* **pySBD (python-sbd / PySBD)** — rule-based pragmatic sentence boundary disambiguation; works out-of-the-box for \~22 languages and is very robust on messy text (email, OCR). Good when you want deterministic, fast segmentation without heavy ML dependencies. ([GitHub][5])

  Example:

  ```bash
  pip install pysbd
  ```

  ```python
  import pysbd
  seg = pysbd.Segmenter(language="en", clean=False)
  seg.seg_text("Dr. Who? Yes. New sentence.")
  ```

* **syntok (segtok v2)** — simple, pure-Python segmenter (successor to segtok). Fast and tiny; designed mainly for Indo-European languages — useful for lightweight pipelines. ([PyPI][6])

* **sentence-splitter / sentence-splitter (Koehn/Schroeder heuristics)** — lightweight heuristic splitter (used historically for Europarl-style corpora). Quick & easy if your domain is well-punctuated parallel corpora. ([PyPI][7])

# Toolkits that include segmentation as part of broader NLP stacks

* **Flair** — provides pluggable sentence splitters and integrates common splitters (segtok, etc.); good if you already use Flair embeddings/sequence models. ([flairnlp.github.io][8])

* **Polyglot** — older but offers sentence segmentation for a very large set of languages (ICU-based rules + language resources). License: GPL — keep that in mind for projects with restrictive licenses. ([polyglot.readthedocs.io][9])

* **NLTK / Punkt** — unsupervised Punkt models (good for many European languages, but often requires training or language-specific preloads). Useful for research / simple tasks. ([NLTK][10])

# Lightweight transformer / model-based splitters

* **sentence\_splitter / kathrynchapman (transformer token-classification)** — a packaged transformer-based splitter (bundled model) for higher accuracy without wiring many dependencies; good if you want a “drop-in” transformer splitter. ([GitHub][11])

# Quick decision guide (which to pick)

* Noisy transcripts / missing punctuation / best accuracy: **wtpsplit (SaT)**. ([arXiv][1])
* Multilingual production pipeline + downstream tasks: **Stanza** or **UDPipe** (language models available). ([Stanford NLP Group][2])
* Deterministic, fast, lightweight: **pySBD** or **syntok/segtok**. ([GitHub][5])
* If you already use Flair/transformers: use their splitter adapters for consistency. ([flairnlp.github.io][8])

# Practical notes & tradeoffs

* **Coverage vs speed vs dependencies**: transformer-based tools (wtpsplit, Trankit with transformers) typically give best robustness but cost more RAM/latency. Rule-based (pySBD, syntok) are very fast and deterministic but may fail on unusual punctuation or languages not covered by their rules. ([arXiv][1])
* **Licensing**: polyglot is GPL (watch for commercial use). Most others (Stanza, UDPipe, Trankit, wtpsplit) are permissively licensed — check each repo before deployment. ([Stanford NLP Group][2])
* **Domain adaptation**: wtpsplit explicitly supports low-shot fine-tuning to adapt to new domains (useful for legal, poetry, lyrics), which many classic tools don’t handle well. ([arXiv][1])

---

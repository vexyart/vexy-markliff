---
this_file: PLAN.md
---

# Remaining work

## Validate XLIFF 2.1 input and output against the OASIS core schema

Check an exported file against the schema and import a known-good file containing a unit and segment. The current reader and writer use `trans-unit` and a namespace ending in `2.1`. The existing XML tests cover that dialect.

## Preserve document structure and translated text on Markdown and HTML round trips

Exercise both formats with a heading, inline markup, a link and a translated target. Check the skeleton and compare the merged result with the original apart from the translation and normalized whitespace. Current reverse conversion emits source text in paragraphs.

## Verify sentence segmentation on both sides of an aligned document pair

Run the segmentation examples in `src_docs/md/design/segmentation.md` with splitting on and off. Check segment boundaries before alignment.

## Implement and verify the storage and alignment modes specified in issue 103

Issue 103 describes future work. Reconcile the proposed target-only layout with the schema’s required source element, then validate all three single-document settings. For paired documents, verify that each translated segment matches its source and that mismatched paragraph counts produce an alignment note.

## Bring package test coverage to the 80% CI threshold

Current package coverage is 76%. Use `pytest tests/ --cov=src/vexy_markliff --cov-report=term-missing --cov-fail-under=80` and exercise the missing conversion and error paths.

## Measure startup, conversion time and memory use for the current package

Use the same interpreter and inputs before and after optimization. Check the 5 ms goal in fresh interpreters and time CLI startup separately. Compare conversion time and peak memory for small and large inputs. Check the lazy imports against current exports and confirm the benchmark scripts measure modules that still exist.

## Finish the runtime dependency and utility audit

Check the CLI without a direct Rich dependency, and check configuration defaults and explicit YAML loading before deciding whether PyYAML can be optional. Check callers of the path, sentence-splitting and logging helpers before removing anything. Verify the installed wheel and update `DEPENDENCIES.md` to match.

## Correct the README examples and document migration to the supported API

Check that the installed CLI help lists the four commands and their arguments. Run each CLI and Python example against an installed wheel. Replace the obsolete `Config`/`process_data` example, unsupported switches and configuration and pipeline examples. Link to the current architecture and give callers of the old API a working replacement where one exists.

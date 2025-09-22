# HTML Attributes Guide

## Common global attributes (work on almost all elements)

| Attribute         | What it’s for                | Notes / Typical values                                                                  |
| ----------------- | ---------------------------- | --------------------------------------------------------------------------------------- |
| `style`           | Inline CSS                   | Prefer CSS classes; keep minimal.                                                       |
| `title`           | Tooltip / supplementary text | Don’t rely on this for accessibility; screen reader support varies. Useful on `<abbr>`. |
| `lang`            | Language of content          | BCP‑47 tag, e.g. `en`, `en-GB`, `ar`.                                                   |
| `dir`             | Text direction               | `ltr`, `rtl`, or `auto`. Handy for mixed‑direction text.                                |
| `data-*`          | Custom data for scripts      | E.g. `data-user-id="123"`. Don’t encode presentation here.                              |
| `hidden`          | Hide from rendering & a11y tree | Equivalent to “not in the DOM” for users; unlike `display:none`, it’s semantic.         |
| `inert`           | Make subtree non‑interactive | Prevents focus/interaction—great when modals are open.                                  |
| `tabindex`        | Keyboard focus order        | `0` to join natural order; avoid positive values.                                       |
| `contenteditable` | Make content editable        | Pair with `spellcheck`, `inputmode`.                                                    |
| `spellcheck`      | Enable/disable spell checking | `true` / `false`.                                                                       |
| `translate`       | Control translation tools   | `yes` / `no`.                                                                           |
| `draggable`       | HTML drag‑and‑drop          | `true` / `false` / `auto`.                                                              |
| `accesskey`       | Keyboard shortcut            | Avoid in most apps (conflicts).                                                         |
| `inputmode`       | Virtual keyboard hint       | E.g. `text`, `numeric`, `email` (useful with `contenteditable`).                        |
| `autocapitalize`  | Capitalization hint         | `on`, `off`, `sentences`, `words`, `characters`.                                        |
| `role`            | ARIA role                   | Use sparingly—prefer native semantics.                                                  |
| `part`, `exportparts`, `slot` | Web Components styling/slotting | Only relevant when using Shadow DOM.                                                    |
| `popover`         | Mark an element as a popover | Works with invoker attributes like `popovertarget` (on a button/link).                  |

## Accessibility (ARIA) you’ll actually use

> Use ARIA only when native HTML can’t express the behavior.

* Naming & descriptions: `aria-label`, `aria-labelledby`, `aria-describedby`
* Visibility & live regions: `aria-hidden`, `aria-live`
* State/relationships: `aria-expanded`, `aria-controls`, `aria-current`, `aria-pressed`, `aria-selected`
* Roles (examples): `role="note"`, `role="status"`, `role="heading"` (only when you *don’t* use `<h1>…<h6>`; pair with `aria-level`)

## Element-specific notes for the tags you mentioned

* `<blockquote>` — **`cite`** (URL of the source).
* `<q>` — **`cite`** as well.
* `<del>` / `<ins>` — **`cite`** and **`datetime`** (ISO 8601).
* `<abbr>` — **`title`** commonly holds the expansion (e.g., title="Internationalization").
* `<p>`, `<h1>`, `<span>`, `<s>` — no unique attributes; rely on global ones above.

## Quick, realistic examples

```html
<!-- Language & direction on textual content -->
<p lang="ar" dir="rtl">النص العربي داخل الفقرة.</p>

<!-- Source attribution on a blockquote -->
<blockquote cite="https://example.com/article">
  “A good quote goes here.”
</blockquote>

<!-- Data for scripts + accessible text -->
<span class="status" role="status" aria-live="polite" data-state="loading">
  Loading…
</span>

<!-- Editable paragraph tailored for numeric input -->
<p contenteditable="true" inputmode="numeric" spellcheck="false">
  12345
</p>

<!-- Popover pattern -->
<button popovertarget="tips">Show tips</button>
<p id="tips" popover>
  Use <code>lang</code> and <code>dir</code> for multilingual text.
</p>

<!-- Temporarily disable a whole subtree (e.g., when a modal is open) -->
<div id="page-content" inert>
  …
</div>
```

### Practical tips

* Prefer semantic HTML over ARIA—use `<h1>` instead of `role="heading"`.
* Keep `tabindex` to `0` or `-1` (avoid `tabindex="1+"`).
* Use `lang`/`dir` as high in the tree as appropriate; override locally only when needed.
* Use `data-*` for state/config, not for styling or content that users must see.
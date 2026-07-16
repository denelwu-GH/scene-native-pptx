# Inclusive Presentation Design

Apply these rules to native objects, generated imagery, charts, and reading order.

## Readability And Accessibility

- Use at least `4.5:1` contrast for normal text and `3:1` for large text. Treat logos as protected artwork, but do not use logo exceptions for ordinary labels.
- Default body text to at least 18 pt. Increase it for room-scale presentation, long viewing distance, or audiences with low vision.
- Use familiar sans-serif fonts, clear line spacing, and enough whitespace. Avoid all caps, excessive italics, and long centered paragraphs.
- Do not use color as the only carrier of status or category. Add text, icons, patterns, or shapes.
- Give every slide a unique descriptive title. It may be visually hidden only when the visible composition requires it.
- Give meaningful photos, diagrams, charts, and grouped illustrations concise alt text. Mark purely decorative items as decorative.
- Set semantic object order so screen readers follow the same logic as the visual story.
- Avoid flattened screenshots when native text, charts, or tables can express the same information.

## Inclusive Generated Imagery

- Depict people with dignity, agency, and context rather than as diversity tokens.
- Avoid clone faces, stereotyped occupations, exaggerated cultural symbols, fake signage, and gibberish non-English text.
- Keep age, skin tone, body type, clothing, mobility aids, and physical interaction internally consistent.
- Represent disability aids as functional physical objects, not decorative props.
- Use geographically and culturally plausible environments when the location matters.
- Keep people and vehicles consistent across multi-panel narratives through `visual-bible.json`.

## Automated Versus Human QA

Automate contrast declarations, minimum font size, title presence, alt-text fields, and reading-order fields. Require human review for cultural accuracy, stereotyping, visual dignity, and whether a complex slide remains understandable at presentation distance.

## Delivery Check

Run PowerPoint's Accessibility Checker when available. Review warnings for contrast, missing titles, alt text, and object order instead of assuming the JSON declaration guarantees the final PPTX.

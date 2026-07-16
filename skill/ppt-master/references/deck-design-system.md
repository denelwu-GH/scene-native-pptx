# Deck Design System

Create a deck-level system before styling individual slides. Reuse tokens and components to make the deck coherent without forcing every page into the same layout.

## Required Tokens

- canvas size, aspect ratio, and safe area;
- grid columns, gutters, and alignment anchors;
- primary, secondary, accent, neutral, and semantic colors;
- title, subtitle, body, caption, metric, and source typography;
- spacing scale;
- corner radii, border weights, and shadow policy;
- icon stroke or fill style;
- chart palette and data-label policy;
- logo clear space and placement rules.

## Reusable Components

Define only components that repeat meaningfully:

- page title and section marker;
- KPI block;
- evidence card;
- process node and connector;
- comparison row;
- quote or user-story block;
- source note and maturity label;
- takeaway strip;
- image caption and logo lockup.

Do not turn each slide into a stack of nested cards. Components should support the story, not replace layout judgment.

## Page Patterns

Maintain a small pattern library for cover, section divider, argument, evidence, architecture, process, matrix, scenario, roadmap, and summary pages. A pattern sets hierarchy and alignment, not final content.

## Overrides

A slide may override a token only when:

1. the page contract explains the communication need;
2. contrast and readability still pass;
3. the override does not create a second accidental brand system;
4. the exception is recorded under `allowedOverrides`.

## Design QA

Check the deck as a sequence:

- consistent title and source-note placement;
- stable typography and icon language;
- intentional alternation of dense and spacious pages;
- no gradual drift in color, radius, or line weight;
- comparable concepts use comparable visual grammar;
- the primary focal point is obvious at presentation distance.

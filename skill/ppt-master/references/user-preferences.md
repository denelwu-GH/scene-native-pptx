# User Preference Protocol

Use preferences to reduce repeated corrections without overriding the current request.

## Storage Scopes

| Scope | Default path | Store |
|---|---|---|
| User | `~/.codex/ppt-master/user-profile.json` | Explicit preferences that should apply to future projects |
| Project | `<project>/.ppt-master/project-profile.json` | Brand, audience, and project conventions |
| Run | `<run>/deck-brief.json` | Requirements for the current deck only |

Never commit the user profile. Do not store client names, confidential text, source files, credentials, contact details, or inferred personal attributes.

## Precedence

Resolve values in this order:

1. current explicit instruction;
2. run preferences;
3. project preferences;
4. user preferences;
5. skill defaults.

Objects merge recursively. Arrays replace lower-priority arrays rather than being appended. A current instruction always wins even when no file has been updated yet.

## What May Be Remembered

- default language and tone;
- information density and preferred slide rhythm;
- palette, typography, card, icon, chart, and imagery preferences;
- layouts or visual styles the user consistently rejects;
- editability and delivery requirements;
- review preferences such as preserving source text or asking before rewriting.

## What Must Not Be Remembered Automatically

- a color or layout requested for only one page;
- temporary campaign or customer requirements;
- private content copied from a deck;
- a preference inferred from silence;
- feedback whose scope is ambiguous.

Run `scripts/classify_feedback.py` as a suggestion only. It does not authorize persistence. When classification is `review-required`, keep the feedback in the run notes and ask only when persistence would materially improve future work.

## Feedback Examples

| Feedback | Suggested scope | Reason |
|---|---|---|
| "以后所有 PPT 都不要用紫色渐变" | User | Explicit future default |
| "这套品牌稿统一使用 JDO 红" | Project | Applies to one brand or project |
| "这一页不要改布局" | Run | Page-specific constraint |
| "我觉得卡片有点多" | Review required | Scope and stability are unclear |

## Update Discipline

When persisting a preference, record:

- exact preference key and value;
- scope;
- source text;
- date;
- whether the user stated it explicitly;
- superseded value when applicable.

Allow the user to inspect, edit, or delete every stored preference. Never convert repeated task instructions into personal-profile claims without a clear durable preference statement.

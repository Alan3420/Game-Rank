---
version: 1
slug: "frontend-src-components-home-home-vue"
primary_target: "frontend/src/components/Home/home.vue"
related_targets: ["frontend/src/components/Home/style_home.css"]
---

Scope: Home route (`/`), second surface of the collectible-card world (inherits DESIGN.md; the world is fixed, only the composition is new). Visitor mode: Operate for signed-in players, a short Persuade landing for guests (only the trailer endpoint is public). Light theme default, dark kept, UI copy in English.

Job: a signed-in player resumes their own collection first, then decides what to play next from the year's best, this month's releases, community trends and upcoming dates. Connective thread with the detail route: same tokens, Barlow Condensed headings, the collectible mini card, and status hue = ownership (frames and the album page tint).

Unresolved: a "latest community reviews" feed would need a new read-only backend endpoint (not built, pending user approval).

## Direction contract

THESIS: The Home is an open card album: your binder of owned cards on the left page, the world's new and best cards on the right. Refuses the category default of a full-width hero banner over identical carousels.

OWN-WORLD: Inherited from the detail route: cool card-stock ground, white faces, near-black ink, status hues as the only large color (the album page takes the active tab's hue as a 7% tint and 2px frame), Barlow Condensed for headings and numbers, Barlow for the rest, mini cards with status frames, checklist rows with set numbers.

STORY: The player is greeted with their totals, opens the tab of what they are playing, jumps back into a game, then scans the year's best and this month's releases, checks what the community is collecting and what comes out next.

FIRST VIEWPORT: Header, then a greeting h1 with collection totals. Below, a two-page spread: left page (7 of 12 columns) = status tabs with counts and a 3x2 pocket grid of mini cards; right page (5 columns) = "Best of the year" and "New this month" as numbered checklists. Primary action: the album tabs and pocket cards.

FORM: Open album (binder spread), position 3 of the ordered structural list, surface seed key f80081c7.

FINISH: unreviewed and undocumented is unfinished; this build ends with the finish review, the verdict, DESIGN.md, and every shipping raster carrying its provenance

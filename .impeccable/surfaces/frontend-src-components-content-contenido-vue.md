---
version: 1
slug: "frontend-src-components-content-contenido-vue"
primary_target: "frontend/src/components/Content/contenido.vue"
related_targets: ["frontend/src/components/Content/style_contenido.css","frontend/src/components/Filters/FilterPanel.vue"]
---

Scope: catalog route (`/content/overview`), third surface of the collectible-card world (inherits DESIGN.md; only composition is new). Visitor mode: Operate. Players browse, search and filter RAWG games, mark favorites and set collection status. Search query, page and view mode live in the URL. UI copy in English, light default, dark kept.

## Direction contract

THESIS: One result set, two ways to read it: an album page of cards to browse, or a set checklist to compare and act. Refuses the category default of a hero banner over a single infinite poster grid with a floating filter popover.

OWN-WORLD: Inherited: cool ground, white faces, near-black ink, status hues only where the player owns the game (mini card frames, checklist status pills), Barlow Condensed for headings and numbers, hairline checklist rows with set numbers "No. {id}", mini cards from the shared component.

STORY: The player narrows the catalog with the filter rail, scans cards in Grid, switches to Checklist to compare scores and years and to favorite or set status row by row, then opens a game.

FIRST VIEWPORT: Header; page title with the result count; left filter rail (sort, genres, platforms, years, apply/clear) beside the results column whose top bar holds the count and a Grid / Checklist segmented switch; results below (4-column mini card grid or checklist table); pager at the end. Primary action: filters and the view switch.

FORM: Grid / checklist toggle with filter rail, position 4 of the ordered structural list, surface seed key 689a954d.

FINISH: unreviewed and undocumented is unfinished; this build ends with the finish review, the verdict, DESIGN.md, and every shipping raster carrying its provenance

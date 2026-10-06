---
version: 1
slug: "frontend-src-components-tendencias-tendencias-vue"
primary_target: "frontend/src/components/Tendencias/Tendencias.vue"
related_targets: []
---

Scope: trends route (`/tendencias`), fifth surface of the collectible-card world (inherits DESIGN.md; only composition is new). Visitor mode: Operate. The player checks what the Game Rank community collects, rates, reviews and favorites most, and jumps into a game. UI copy in English, light default, dark kept. The Home already shows a 4-card teaser of the same data; this page is the full ranking.

## Direction contract

THESIS: Trends is an official standings table: one ranking at a time, read in full. Its number 1 is a large champion card and places 2 to 8 are ranked rows with a proportional bar for the stat. Refuses the category default of four stacked carousels of identical thumbnail cards.

OWN-WORLD: Inherited: cool ground, white faces, near-black ink, Barlow Condensed numbers and headings, status hues only as ownership (a row or champion the player owns takes its status frame and stamp). The rank numerals are Barlow Condensed tabular figures, the bars are ink (never a status hue), "No. {id}" set numbers on every entry, Metacritic seal.

STORY: The player picks a ranking with the selector (Most collected by default), reads who leads it and by how much, spots which of the eight they already own, and opens a game. Switching rankings swaps the board without leaving the page; the choice is kept in the URL.

FIRST VIEWPORT: Header; a title band (h1 "Trends", one-line description of the active ranking); the four-ranking selector as a tablist; below, the board: the champion card on 4 columns (art, name, big stat, set number, year, seal) beside the ranked list of places 2 to 8 on 8 columns (rank numeral, thumbnail, name and No., owned stamp, bar, stat value).

FORM: Single standings board with selector, position 3 of the ordered structural list, surface seed key 2ece8bb4.

FINISH: unreviewed and undocumented is unfinished; this build ends with the finish review, the verdict, DESIGN.md, and every shipping raster carrying its provenance

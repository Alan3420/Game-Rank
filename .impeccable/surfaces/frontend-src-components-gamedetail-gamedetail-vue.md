---
version: 1
slug: "frontend-src-components-gamedetail-gamedetail-vue"
primary_target: "frontend/src/components/GameDetail/GameDetail.vue"
related_targets: ["frontend/src/components/GameDetail/styles_GameDetail.css"]
---

Scope: game detail route (`/game/:id`), pilot of the full Game Rank redesign. Visitor mode: Operate. Players decide whether a game is worth playing and act on it (favorite, collection status, rating and review). Light theme default, dark theme kept; UI copy in English. RAWG supplies every game fact and its attribution stays visible on the card.

Memorable moment: changing collection status recolors the card frame and runs one holographic sweep across the art.

Unresolved: final crop policy for very tall or very wide RAWG covers; extension of the card system to catalog, profile and trends after the pilot is accepted; new style-guide PDF and PRODUCT.md update.

## Direction contract

THESIS: Every game is a collectible card. RAWG prints the facts; your status and rating make it yours. Refuses the category default of a blurred-cover banner with a score badge and tabs.

OWN-WORLD: Cool card-stock ground, white card faces, near-black ink. The card frame is the only large color: neutral ink when the game is not yours, and one solid status hue when it is (Pending blue, Playing green, Paused amber, Completed violet). Barlow Condensed for the card name and stat values, Barlow for everything else. Thick rounded frame, inset art box, ruled stat cells.

STORY: The player sees the card and knows the game, its scores and whether it is theirs. They set status, rate it, read the community, then dig into media, achievements and details.

FIRST VIEWPORT: Standard header. Left column, 380px, sticky: the card (name band with Metacritic, 4:3 art box, genre line, three stat cells, set number with RAWG credit and status stamp). Right column: "Your copy" panel (favorite, status, rating link) first, then About and a Details list. Primary action: the favorite/status control at the top of the right column.

FORM: Collectible card, position 6 of the ordered list, seed key 337abc17. Signature move: status change recolors the frame and sweeps a holo band once across the art.

FINISH: unreviewed and undocumented is unfinished; this build ends with the finish review, the verdict, DESIGN.md, and every shipping raster carrying its provenance

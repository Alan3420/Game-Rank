---
version: 1
slug: "frontend-src-components-user-perfil-user-vue"
primary_target: "frontend/src/components/User/perfil_user.vue"
related_targets: ["frontend/src/components/User/style_perfil.css"]
---

Scope: profile route (`/user/profile`, `/profile`), fourth surface of the collectible-card world (inherits DESIGN.md; only composition is new). Visitor mode: Operate. The player reviews what they have collected and completed, manages their collection and favorites, rereads their reviews and reaches account settings. UI copy in English, light default, dark kept.

## Direction contract

THESIS: The profile is a trophy cabinet: it shows off what you have collected and finished first, and keeps account settings in a side panel. Refuses the category default of a cover banner over a settings sidebar and stat tiles.

OWN-WORLD: Inherited: cool ground, white faces, near-black ink, Barlow Condensed numbers and headings, status hues as ownership. Trophy plates are framed like cards: status plates take their status frame, the other plates the neutral frame. One segmented progress bar in the four status hues shows how the album is split. Mini cards with status frames, checklist rows with "No. {id}".

STORY: The player sees their totals as plates and how their album splits by status, opens a status tab to jump back into a game, scans favorites and their latest reviews, and opens Account settings to edit their name or password.

FIRST VIEWPORT: Header; a name band (h1 name, @nickname, role) with the Account settings button on the right; a row of seven trophy plates (Completed, Playing, Paused, Pending in their hues; Favorites, Reviews, Avg. rating neutral); the album split bar with its legend; below, the collection with status tabs (8 columns) beside favorites and reviews (4 columns).

FORM: Trophy cabinet, position 5 of the ordered structural list, surface seed key fb9be00e.

FINISH: unreviewed and undocumented is unfinished; this build ends with the finish review, the verdict, DESIGN.md, and every shipping raster carrying its provenance

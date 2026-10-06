---
name: Game Rank
description: Every game is a collectible card; RAWG prints the facts, the player's status and rating make it theirs.
colors:
  ground: "#EEF0F4"
  face: "#FFFFFF"
  ink: "#16141D"
  ink-2: "#4B4858"
  ink-3: "#64616F"
  rule: "#DCDFE7"
  rule-strong: "#C3C7D2"
  frame-neutral: "#2A2733"
  status-pending: "#2563EB"
  status-playing: "#0E7A3F"
  status-paused: "#9A5B00"
  status-completed: "#6D3FD6"
  on-frame: "#FFFFFF"
  on-frame-neutral: "#FFFFFF"
  star: "#C98A00"
  rarity-rare: "#B45309"
  rarity-uncommon: "#2563EB"
  rarity-common: "#8A8796"
  metacritic-high: "#157347"
  metacritic-mid: "#8C5A00"
  metacritic-low: "#B3261E"
  danger: "#B3261E"
  danger-dark: "#F07A72"
  ground-dark: "#0E0F15"
  face-dark: "#181922"
  ink-dark: "#F1F0F6"
  ink-2-dark: "#BCB9CA"
  ink-3-dark: "#A09DB0"
  rule-dark: "#2A2B38"
  rule-strong-dark: "#3B3C4C"
  frame-neutral-dark: "#4A4757"
  status-pending-dark: "#7AA2FF"
  status-playing-dark: "#3DD68C"
  status-paused-dark: "#F2B544"
  status-completed-dark: "#B096FF"
  on-frame-dark: "#0E0F15"
  on-frame-neutral-dark: "#F1F0F6"
  star-dark: "#F2B544"
  rarity-rare-dark: "#F59E0B"
  rarity-uncommon-dark: "#7AA2FF"
  rarity-common-dark: "#8E8BA0"
typography:
  display:
    fontFamily: "Barlow Condensed, Barlow, sans-serif"
    fontSize: "2rem"
    fontWeight: 800
    lineHeight: 1
    letterSpacing: "-0.01em"
  headline:
    fontFamily: "Barlow Condensed, Barlow, sans-serif"
    fontSize: "2rem"
    fontWeight: 800
    lineHeight: 1.05
    letterSpacing: "-0.01em"
  title:
    fontFamily: "Barlow Condensed, Barlow, sans-serif"
    fontSize: "1.45rem"
    fontWeight: 700
    lineHeight: 1.1
  stat-value:
    fontFamily: "Barlow Condensed, Barlow, sans-serif"
    fontSize: "1.2rem"
    fontWeight: 700
    lineHeight: 1.15
    fontFeature: "tnum"
  body:
    fontFamily: "Barlow, system-ui, sans-serif"
    fontSize: "1rem"
    fontWeight: 400
    lineHeight: 1.5
  prose:
    fontFamily: "Barlow, system-ui, sans-serif"
    fontSize: "1rem"
    fontWeight: 400
    lineHeight: 1.65
  label:
    fontFamily: "Barlow, system-ui, sans-serif"
    fontSize: "0.875rem"
    fontWeight: 600
    lineHeight: 1.4
  label-sm:
    fontFamily: "Barlow, system-ui, sans-serif"
    fontSize: "0.75rem"
    fontWeight: 600
    lineHeight: 1.3
  button:
    fontFamily: "Barlow, system-ui, sans-serif"
    fontSize: "0.95rem"
    fontWeight: 600
    lineHeight: 1
rounded:
  card: "22px"
  album: "18px"
  dialog: "18px"
  mini-card: "16px"
  panel: "14px"
  tile: "12px"
  control: "10px"
  cell: "8px"
  seal: "6px"
  pill: "999px"
spacing:
  xs: "6px"
  sm: "10px"
  md: "16px"
  lg: "28px"
  section: "72px"
  section-mobile: "56px"
  shell-x: "24px"
  shell-x-mobile: "14px"
components:
  button-primary:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.face}"
    typography: "{typography.button}"
    rounded: "{rounded.control}"
    padding: "0 16px"
    height: "42px"
  button-primary-hover:
    backgroundColor: "{colors.ink-2}"
    textColor: "{colors.face}"
  button-ghost:
    backgroundColor: "{colors.face}"
    textColor: "{colors.ink}"
    typography: "{typography.button}"
    rounded: "{rounded.control}"
    padding: "0 16px"
    height: "42px"
  button-ghost-hover:
    backgroundColor: "{colors.ground}"
    textColor: "{colors.ink}"
  button-sm:
    rounded: "{rounded.control}"
    padding: "0 12px"
    height: "34px"
  card-frame:
    backgroundColor: "{colors.frame-neutral}"
    rounded: "{rounded.card}"
    padding: "10px"
  card-face:
    backgroundColor: "{colors.face}"
    textColor: "{colors.ink}"
    rounded: "{rounded.panel}"
    padding: "14px"
  card-name:
    textColor: "{colors.ink}"
    typography: "{typography.display}"
  stat-cell:
    backgroundColor: "{colors.face}"
    textColor: "{colors.ink}"
    typography: "{typography.stat-value}"
    rounded: "{rounded.cell}"
    padding: "8px 10px"
  status-stamp:
    backgroundColor: "{colors.frame-neutral}"
    textColor: "{colors.on-frame}"
    rounded: "{rounded.pill}"
    padding: "3px 10px"
  metacritic-high:
    backgroundColor: "{colors.metacritic-high}"
    textColor: "{colors.face}"
    rounded: "{rounded.cell}"
    padding: "4px 8px 6px"
  metacritic-mid:
    backgroundColor: "{colors.metacritic-mid}"
    textColor: "{colors.face}"
    rounded: "{rounded.cell}"
    padding: "4px 8px 6px"
  metacritic-low:
    backgroundColor: "{colors.metacritic-low}"
    textColor: "{colors.face}"
    rounded: "{rounded.cell}"
    padding: "4px 8px 6px"
  metacritic-none:
    backgroundColor: "{colors.ground}"
    textColor: "{colors.ink-2}"
    rounded: "{rounded.cell}"
    padding: "4px 8px 6px"
  panel:
    backgroundColor: "{colors.face}"
    textColor: "{colors.ink}"
    rounded: "{rounded.panel}"
    padding: "20px 22px"
  chip:
    backgroundColor: "{colors.face}"
    textColor: "{colors.ink}"
    rounded: "{rounded.pill}"
    padding: "4px 10px"
  store-chip:
    backgroundColor: "{colors.face}"
    textColor: "{colors.ink}"
    rounded: "{rounded.pill}"
    padding: "0 12px"
    height: "32px"
  textarea:
    backgroundColor: "{colors.face}"
    textColor: "{colors.ink}"
    rounded: "{rounded.control}"
    padding: "12px"
  achievement-tile:
    backgroundColor: "{colors.face}"
    textColor: "{colors.ink}"
    rounded: "{rounded.tile}"
    padding: "10px"
  mini-card-frame:
    backgroundColor: "{colors.frame-neutral}"
    rounded: "{rounded.mini-card}"
    padding: "6px"
  mini-card-frame-owned:
    backgroundColor: "{colors.status-playing}"
    rounded: "{rounded.mini-card}"
    padding: "6px"
  mini-card-stamp:
    backgroundColor: "{colors.status-playing}"
    textColor: "{colors.on-frame}"
    rounded: "{rounded.pill}"
    padding: "2px 8px"
  metacritic-seal-sm:
    backgroundColor: "{colors.metacritic-high}"
    textColor: "{colors.face}"
    rounded: "{rounded.seal}"
    padding: "2px 6px"
  album-page:
    textColor: "{colors.ink}"
    rounded: "{rounded.album}"
    padding: "22px"
  facing-page:
    backgroundColor: "{colors.face}"
    textColor: "{colors.ink}"
    rounded: "{rounded.album}"
    padding: "22px 24px"
  status-tab:
    backgroundColor: "{colors.face}"
    textColor: "{colors.ink}"
    rounded: "{rounded.pill}"
    padding: "0 8px 0 14px"
    height: "38px"
  status-tab-active:
    backgroundColor: "{colors.status-playing}"
    textColor: "{colors.on-frame}"
  segmented-tab:
    textColor: "{colors.ink-2}"
    rounded: "7px"
    padding: "0 12px"
    height: "32px"
  segmented-tab-active:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.face}"
  checklist-row:
    textColor: "{colors.ink}"
    rounded: "{rounded.cell}"
    padding: "10px 6px"
  owned-pill:
    backgroundColor: "{colors.status-playing}"
    textColor: "{colors.on-frame}"
    rounded: "{rounded.pill}"
    padding: "1px 7px"
  date-tile:
    backgroundColor: "{colors.ground}"
    textColor: "{colors.ink}"
    rounded: "{rounded.cell}"
    padding: "5px 0"
    width: "52px"
  button-danger:
    backgroundColor: "{colors.danger}"
    textColor: "{colors.face}"
    typography: "{typography.button}"
    rounded: "{rounded.control}"
    height: "42px"
  site-header:
    backgroundColor: "{colors.face}"
    textColor: "{colors.ink}"
    padding: "0 24px"
    height: "64px"
  header-search:
    backgroundColor: "{colors.ground}"
    textColor: "{colors.ink}"
    rounded: "{rounded.control}"
    padding: "0 14px"
    height: "40px"
  header-search-focus:
    backgroundColor: "{colors.face}"
    textColor: "{colors.ink}"
  header-nav-link:
    textColor: "{colors.ink-2}"
    rounded: "{rounded.control}"
    padding: "0 12px"
    height: "38px"
  header-nav-link-active:
    textColor: "{colors.ink}"
  theme-toggle:
    backgroundColor: "{colors.face}"
    textColor: "{colors.ink-2}"
    rounded: "{rounded.control}"
    size: "38px"
  account-button:
    backgroundColor: "{colors.face}"
    textColor: "{colors.ink}"
    rounded: "{rounded.pill}"
    padding: "3px 10px 3px 3px"
    height: "42px"
  avatar:
    backgroundColor: "{colors.frame-neutral}"
    textColor: "{colors.on-frame-neutral}"
    rounded: "{rounded.pill}"
    size: "34px"
  menu-panel:
    backgroundColor: "{colors.face}"
    textColor: "{colors.ink}"
    rounded: "{rounded.panel}"
    width: "290px"
  menu-item:
    textColor: "{colors.ink}"
    rounded: "{rounded.cell}"
    padding: "8px 10px"
    height: "40px"
  menu-item-danger:
    textColor: "{colors.danger}"
  status-menu:
    backgroundColor: "{colors.face}"
    rounded: "{rounded.tile}"
    padding: "4px"
  status-option:
    textColor: "{colors.ink}"
    rounded: "{rounded.cell}"
    padding: "8px 10px"
  status-option-active:
    backgroundColor: "{colors.status-playing}"
    textColor: "{colors.on-frame}"
  toast:
    backgroundColor: "{colors.face}"
    textColor: "{colors.ink}"
    rounded: "{rounded.panel}"
    padding: "12px 12px 12px 14px"
  toast-icon:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.face}"
    rounded: "9px"
    size: "34px"
  toast-icon-error:
    backgroundColor: "{colors.danger}"
    textColor: "{colors.face}"
  modal:
    backgroundColor: "{colors.face}"
    textColor: "{colors.ink}"
    rounded: "{rounded.dialog}"
    padding: "28px"
    width: "420px"
  site-footer:
    backgroundColor: "{colors.face}"
    textColor: "{colors.ink}"
    padding: "40px 24px 28px"
  filter-panel:
    backgroundColor: "{colors.face}"
    textColor: "{colors.ink}"
    rounded: "{rounded.panel}"
    padding: "18px"
  filter-chip:
    backgroundColor: "{colors.face}"
    textColor: "{colors.ink}"
    rounded: "{rounded.pill}"
    padding: "0 11px"
    height: "32px"
  filter-chip-active:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.face}"
  page-button:
    backgroundColor: "{colors.face}"
    textColor: "{colors.ink}"
    rounded: "{rounded.control}"
    padding: "0 10px"
    height: "40px"
  page-button-active:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.face}"
  set-table:
    backgroundColor: "{colors.face}"
    textColor: "{colors.ink}"
    rounded: "{rounded.panel}"
  set-table-row:
    textColor: "{colors.ink}"
    padding: "8px 12px"
  trophy-plate:
    backgroundColor: "{colors.frame-neutral}"
    textColor: "{colors.on-frame-neutral}"
    rounded: "{rounded.panel}"
    padding: "0 5px 5px"
  trophy-plate-status:
    backgroundColor: "{colors.status-completed}"
    textColor: "{colors.on-frame}"
  trophy-plate-face:
    backgroundColor: "{colors.face}"
    textColor: "{colors.ink}"
    rounded: "{rounded.control}"
    padding: "10px 12px"
  trophy-plate-empty:
    textColor: "{colors.ink-3}"
    rounded: "{rounded.panel}"
    padding: "0 4px 4px"
  album-split-bar:
    rounded: "{rounded.pill}"
    height: "14px"
  account-drawer:
    backgroundColor: "{colors.face}"
    textColor: "{colors.ink}"
    padding: "22px"
    width: "380px"
  board-tab:
    textColor: "{colors.ink-2}"
    rounded: "{rounded.pill}"
    padding: "0 14px"
    height: "38px"
  board-tab-active:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.face}"
  champion-frame:
    backgroundColor: "{colors.frame-neutral}"
    textColor: "{colors.on-frame-neutral}"
    rounded: "{rounded.card}"
    padding: "0 7px 7px"
  champion-face:
    backgroundColor: "{colors.face}"
    textColor: "{colors.ink}"
    rounded: "{rounded.panel}"
    padding: "12px"
  standings-panel:
    backgroundColor: "{colors.face}"
    textColor: "{colors.ink}"
    rounded: "{rounded.album}"
  ranked-row:
    textColor: "{colors.ink}"
    padding: "12px 16px"
  member-card-frame:
    backgroundColor: "{colors.frame-neutral}"
    rounded: "{rounded.card}"
    padding: "10px"
  member-card-face:
    backgroundColor: "{colors.face}"
    textColor: "{colors.ink}"
    rounded: "{rounded.panel}"
    padding: "20px 22px 16px"
  auth-input:
    backgroundColor: "{colors.face}"
    textColor: "{colors.ink}"
    rounded: "{rounded.control}"
    padding: "0 12px"
    height: "42px"
  auth-submit:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.face}"
    rounded: "{rounded.control}"
    height: "46px"
  ledger-page:
    backgroundColor: "{colors.face}"
    textColor: "{colors.ink}"
    rounded: "{rounded.panel}"
  role-pill:
    textColor: "{colors.ink-2}"
    rounded: "{rounded.pill}"
    padding: "2px 10px"
  role-pill-admin:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.face}"
  rulebook-page:
    backgroundColor: "{colors.face}"
    textColor: "{colors.ink}"
    rounded: "{rounded.album}"
    padding: "8px 36px 28px"
  toc-link:
    textColor: "{colors.ink-2}"
    rounded: "{rounded.cell}"
    padding: "7px 10px"
  toc-link-active:
    backgroundColor: "{colors.face}"
    textColor: "{colors.ink}"
  missing-card-sleeve:
    textColor: "{colors.ink-3}"
    rounded: "{rounded.mini-card}"
    padding: "14px"
---

# Design System: Game Rank

> **Scope.** Every view runs the card world. The shared app shell (`frontend/src/base/App.vue` and `style_app.css`) covers the site header, user menu, footer and delete-account modal; with it come the global confirm and external-link modal (`.ext-modal` in `frontend/src/style.css`), the toasts (`frontend/src/components/Notifications/`), the status menu (`frontend/src/components/Cards/GameStatusDropdown.vue`) and the page scrollbar. The views are the game detail (`/game/:id`, `components/GameDetail/`), the Home (`/`, `components/Home/`), the catalog (`components/Content/` with `Filters/` and `Pagination/`), the profile (`components/User/`), Trends (`components/Tendencias/`), sign in and register (`components/LoginRegister/`, shared `style_auth.css`), the two admin pages (`components/Admin/`, shared `style_admin.css`), the terms (`components/Legal/`) and the 404 (`components/NotFound/`). The previous system (Sora type, the `--color-*` tokens) is gone from the source; `style.css` now sets Barlow on the body and holds only resets, the motion curves, the scrollbar and the `.ext-modal` styles.
>
> The tokens below are global `--gd-*` custom properties in `frontend/src/styles/card-world.css`: `:root` (light) and `[data-theme="dark"]` (dark), so the shell and everything teleported to the body can use them. Two scope classes in the same file apply the world: `card-world` is the page base of every view (put on its root: full-height card-stock ground, ink text, Barlow, and the neutral frame default), and `cw-scope` is the typography scope for loose pieces outside a view root (header, footer, toasts, status menu, delete-account modal, the profile's account drawer): Barlow, ink selection and the focus ring, without a page ground. The same file holds the shared world classes (status frame, section heading, count, small Metacritic seal). Barlow and Barlow Condensed are imported globally through `@fontsource` in `frontend/src/main.js`; the motion curves are global (`:root` in `style.css`). Shared parts: the mini card (`frontend/src/components/CardWorld/MiniCard.vue`), the Metacritic seal thresholds (`frontend/src/utils/metacritic.js`, `claseMetacritic(score)` returning `mc-green`, `mc-yellow`, `mc-red` or `mc-na` for the `cw-mc` seal), the status labels and icons (`frontend/src/utils/statusMeta.js`), the pagination (`components/Pagination/`) and the status menu.
>
> Visual evidence: review captures in `.impeccable/review/` (`catalog/`, `profile/`, `trends/`, `auth/`, `rest/` for terms and 404, plus the earlier `home/` and `shell/`, `admin/` for both admin tables and `logo/` for the header). All other captures match the current code (`profile/edit-modal.png` shows the in-drawer Edit profile step).

## Overview

**Creative North Star: "The Collectible Card"**

Every game is a trading card. RAWG prints the facts on the card face (name, art, genres, release, platforms, Metacritic, set number); the player's collection status colors the frame and their rating and review sit beside it. The world is a cool card-stock ground, white card faces and near-black ink, with one thick rounded frame as the only large field of color on a card. That frame is neutral ink while the game is not in the player's collection and takes one solid status hue when it is. Surfaces that hold the player's own copies (the "Your copy" panel, the Home album page) take the same status hue as a light tint and a 2px frame.

Density is moderate and editorial. The game detail sets a sticky card column next to a working column of panels; the Home leads with discovery: a Discover page of games the player does not own yet (a spotlight card plus mini cards), with the player's album reduced to a summary panel beside it. The other views take one collectible metaphor each: the catalog is an album page of mini cards that switches to the set checklist; the profile is a trophy shelf of plates over the player's collection; Trends is a standings board with a champion card; sign in and register are a member card; the admin pages are a ledger; the terms are a rulebook; the 404 is the missing card's empty sleeve. Surfaces are flat white faces on a pale ground, held apart by hairline rules rather than shadows; only card objects (the main card, mini cards, the trailer card, trophy plates, the champion card, the member card) are lifted, plus the transient overlays (menus, toasts, modals, the account drawer) that sit above the page. The shell is structure, not an object: the header and footer are flat face bands ruled off from the ground by one hairline. Motion is quiet everywhere except one signature: when the player changes status, a holographic band sweeps once across the card art.

The world rejects the category default of a blurred-cover banner with a score badge and tabs, and of a full-width hero over identical carousels. Facts are framed as card stats and checklist entries, not as banners.

**Key Characteristics:**
- Card object first: thick rounded frame, inset 4:3 art box, ruled stat cells, set-number footer with RAWG credit. Every view borrows one collectible object (album page, set checklist, trophy plate, champion card, member card, ledger, rulebook, empty sleeve).
- One large color, and it means collection status.
- Condensed display type for names and numbers, plain Barlow for everything else.
- Hairline rules and tonal ground instead of shadows for non-card surfaces, including the header and footer bands.
- One signature motion (holo sweep), removed under reduced motion.
- Light theme default; dark theme is a full token remap, not an inversion filter.

## Colors

A cool, nearly achromatic paper-and-ink base with a small, semantic set of saturated hues that each mean exactly one thing on the card.

### Primary
- **Collection Status Frame** (frame-neutral when not owned; status-pending, status-playing, status-paused, status-completed when owned): card and mini card frames, status stamps, the owned pill on checklist rows, the "Your copy" panel border and its 7% tint (`color-mix(in srgb, frame 7%, face)`), the Home album summary's status counts (only when above 0), and the status button outline and text. Beyond those: the profile's status plates (only when their count is above 0), its collection tabs and album split bar with legend dots, the status pill in the catalog checklist and the profile favorites, the stamps on Trends rows and the champion card, the 7% tint on owned rows (catalog checklist, Trends standings), and the bookmark glyph of the mini card's status button. Pending is a clear blue, Playing a deep green, Paused a burnt amber, Completed a violet. In dark theme every hue is lifted to a lighter tint and the text on a status frame flips to the dark ground (on-frame-dark); the neutral frame keeps light text (on-frame-neutral) so the "Favorite" stamp holds AA contrast (7.95:1). The neutral frame also fills the account avatar in the header and user menu: the player's initial printed like a card in a neutral frame. Any container opts into a status with the shared frame classes (`cw-frame` plus `cw-frame--pendiente|jugando|pausado|completado`), which set the frame hue and its on-frame text for everything inside.

### Secondary
- **Metacritic Seal** (metacritic-high, metacritic-mid, metacritic-low; metacritic-none for missing scores): the score seal on the main card, mini cards, the guest trailer card, "New this month" rows, the catalog checklist's Metacritic column and the Trends champion card's footer. Thresholds, shared by every surface through `claseMetacritic()` in `utils/metacritic.js`: 80 and above high, 50 to 79 mid, below 50 low, no score none. White text on all three; the same values in both themes.
- **Star Gold** (star): filled rating stars in the rating control, the Community stat, review ratings, the RAWG player rating on "Top rated" rows, the average-rating total on the Home greeting, the profile's "Avg. rating" plate stamp and review scores, and the rating on admin comment rows. Empty stars use rule-strong.

### Tertiary
- **Rarity Inks** (rarity-rare, rarity-uncommon, rarity-common): achievement rarity. Rare (under 10% of players) owns the holo frame and a burnt-amber star; uncommon (under 40%) a blue frame and rotated square; common a grey dot and the default hairline. Uncommon shares the Pending blue value; it is a shared value, not a shared meaning.

### Neutral
- **Card Stock** (ground): the page ground (on every view root and on `#app`), empty art boxes, avatar and thumb wells, tab counts, the resting header search field, data-bar tracks, disabled inputs, the terms attribution note, the scrollbar track, ghost and row hover fill.
- **Card Face** (face): panels, card faces, plate faces, the Home Discover page and its list panels, the catalog album page and set table, the Trends standings, the admin ledger page, the terms page, the account drawer, tiles, inputs, ghost buttons, unselected tabs, the header and footer bands, menus, toasts and modals.
- **Ink** (ink): headings, names, primary button fill (including Sign up and the auth submit), selected segment, board tab, filter chip and current page fill, the admin role pill, the catalog filter count badge, the active nav bar, the toast icon chip, active thumb outline, text selection fill, checkbox accent.
- **Ink 2** (ink-2): prose, genre line, set numbers, primary button hover, nav links and footer links at rest, toast and modal body text, the Trends data-bar fill.
- **Ink 3** (ink-3): labels, metadata, counts, ranks, hints, placeholders, icon buttons at rest, menu item icons, footer labels and copyright, scrollbar thumb hover.
- **Rule** (rule): hairline borders on panels, the Discover page, stat cells, tiles, detail rows, checklist and calendar dividers, review dividers, the header and footer rules, menu group dividers, toast and modal borders.
- **Strong Rule** (rule-strong): control borders (ghost buttons, textarea, store chips, status tabs, the header search field, the account button), link underlines, empty stars, dashed empty states, the scrollbar thumb.
- **Danger** (danger, danger-dark): destructive actions and errors only: icon-button hover (admin delete adds a 10% danger wash), "Delete account" in the user menu, "Remove status" in the status menu, the destructive modal button and icon, the error toast chip and the error icon, invalid field borders and their hint text, and the inline error alert (danger text, border mixing 40% danger into rule). Light shares the metacritic-low value; dark lifts to a light coral.

### Named Rules
**The One Frame Rule.** On a card (main card, mini card, trophy plate, champion card, member card), the frame is the only large field of color. Beyond cards, the only large colored surfaces are tinted ownership surfaces: a 7% status tint with a 2px status frame on a surface that holds the player's own copy ("Your copy" on the detail). Every other colored element (Metacritic seal, stamps, owned pills, stars, rarity marks) is small. A new surface does not add a large color that is not the player's status.

**The Frame Means Ownership Rule.** A frame stays neutral until the game is in the player's collection with a status; only then does it take the status hue, and the ownership surface takes the same hue with it. A mini card or the Trends champion card shows a status frame only when it is given the player's status for that game. A profile status plate takes its hue only when the player has at least one game in that status; the Activity plates (favorites, reviews, average rating) and the member card always stay in the neutral frame. Status hue never decorates anything unrelated to the player's collection, with two exceptions: the focus ring, which uses the Pending blue as the system focus color, and the guest status picker on the Home, where the visitor chooses a status for the trailer's game and the card takes that hue, as in the status menu. In the shell, status hues appear only in the status menu, where the player is choosing a status; feedback never borrows them. Toasts print their icon chip in ink whatever their type (success, info, warning), and only errors take danger. The tools that are not about the player's collection (filter chips, view switch, board tabs, pagination, the admin ledger, the terms) select in ink, never in a status hue.

**The Owned Row Rule.** In a list or table that mixes the player's games with others, a row the player owns takes a 7% tint of its status hue over the face (Trends standings and the catalog checklist; on Trends hover deepens to 13%), with no frame; the hue at full strength stays on the row's stamp or pill. The Home checklists and the profile favorites do not tint owned rows; they mark ownership with the pill alone.

**The Ink Bars Rule.** A bar that measures a community value (the Trends data bars) is ink-2 on a ground track, never a status hue. Status hues fill a bar only when it splits the player's own album by status (the profile split bar), where each segment is that status.

## Typography

**Display Font:** Barlow Condensed 700/800 (with Barlow, sans-serif)
**Body Font:** Barlow 400/500/600/700 (with system-ui, sans-serif)

Both are self-hosted through `@fontsource` and imported once in `main.js`. The body is Barlow globally (`style.css`, with form controls inheriting the family); inside `.card-world` and `.cw-scope` every element except PrimeIcons inherits it through a zero-specificity `:where()` rule, so each view's own Barlow Condensed rules still win; the external-link and confirm modal overlay carries the same rule on its own class. The only other face is the system monospace stack (`ui-monospace, Cascadia Mono, Consolas`), used once, for the requested path on the 404.

**Character:** A sports-card pairing: the condensed face prints names and numbers with the punch of a card's name band and stat line, while regular Barlow keeps prose, labels and controls quiet and legible.

### Hierarchy
- **Page title** (Barlow Condensed 800, line-height 0.95 to 1, -0.015em): every view's h1. Surface-specific, not a token, in two sizes. Working views print it at 2.75rem, line-height 1 (Home player greeting, catalog title, profile name; 2.1rem on mobile). Single-purpose views print it at 3 to 3.4rem, line-height 0.95: Trends and the auth titles at 3.4rem (2.6rem on mobile), terms and 404 at 3.2rem (2.4 and 2.5rem), admin at 3rem (2.4rem). The guest Home headline is the outlier at 3.5rem (2.5rem at 480px, line-height 0.98, -0.02em).
- **Display** (800, 2rem; 1.75rem at 1024px and below; 1.6rem at 480px; line-height 1; -0.01em): the card name in the name band, balanced wrapping. The guest trailer card prints its name at 1.5rem.
- **Headline** (800, 2rem; 1.65rem at 480px; -0.01em): full-width section headings (the shared section heading class), followed by a tabular count in Barlow 600 0.9rem ink-3. The Home's facing-page checklists step it down to 1.6rem.
- **Title** (700, 1.45rem, line-height 1.1): panel headings ("Your copy", About, Details, the catalog's Filters panel, the profile's Favorites panel).
- **Card-face headings** (Barlow Condensed 800): the Trends champion name at 1.9rem (1.6rem on mobile), the member card title at 1.9rem, terms section headings at 1.75rem (1.5rem at 640px), the "Missing card" name at 1.3rem. Group labels in condensed 700: the profile shelf's "Album" and "Activity" and the terms "Contents" title at 1.2rem in ink-2, plate stamps at 1rem.
- **Shell headings** (Barlow Condensed): modal titles, the drawer title and the footer brand at 1.6rem/800; the user menu name at 1.15rem/800; the toast title at 1.1rem/800; footer column headings at 1.15rem/700; the avatar initial at 800 (1.6rem on the profile's 64px avatar).
- **Stat value** (Barlow Condensed 700, 1.2rem, tabular numerals): stat cells; the same face at 1.1rem prints rating values and review scores, at 1.6rem/800 the main card's Metacritic number and the champion's "No. 1", at 0.95rem/800 the small seal, at 0.85 to 0.95rem/700 set numbers, at 1.75rem/800 the Home greeting totals, at 1.3 to 1.4rem/800 Home ranks, at 0.98rem/700 the release dates in Coming soon, at 1.6rem/700 the catalog result count, at 1.05rem/700 page numbers. Big figures go larger: plate values 2.4rem/800 (1.85rem at 640px), the champion's value 3.6rem/800 at line-height 0.9 (3rem at 640px), standings ranks 2.1rem/800 (1.7rem), standings values 1.35rem/800, terms section numerals 1.8rem/800 in ink-3 (1.45rem).
- **Body** (400, 1rem, line-height 1.5): default text. **Prose** (line-height 1.65, max 68ch, ink-2) for the About description and review bodies; the guest lead runs 1.1rem at line-height 1.6, max 46ch.
- **Label** (600, 0.875rem, ink-3): definition-list terms, rating label, form labels (ink-2), filter legends (0.85rem), table headers (0.82rem). **Label small** (600, 0.75 to 0.8rem) for stat-cell terms, greeting total terms, row metadata and field hints. Labels are sentence case, never uppercase.
- **Button** (600, 0.95rem; 0.875rem in the small size). Tabs run 0.9rem/600, segments 0.85rem/600.

### Named Rules
**The Condensed Prints Facts Rule.** Barlow Condensed is reserved for card names, page titles, section, panel, modal, toast and footer headings, card-face headings and shelf group labels, plate stamps, the account name and initial, the member card's handle, and numbers (stats, scores, ratings, set numbers, ranks, dates, totals, page numbers, terms numerals). Running text, labels, row names and controls stay in Barlow.

**The Tabular Numbers Rule.** Every number that can change or be compared (stats, scores, counts, ranks, percentages, totals, page numbers, dates in tables, year inputs, character counter) uses tabular numerals.

## Layout

The header, footer and every view share one centered shell, max 1240px wide, with 24px side padding (14px on mobile) and a bottom padding of 80 to 88px (64px on mobile). Three single-purpose views narrow it: sign in and register to 1040px (560px when stacked), the 404 to 900px; the terms page column caps at 760px.

**Shell.** The header is sticky at the top (min 64px tall, 0 24px padding, 20px gap): logo left, a fluid search field (max 440px) in the middle when signed in, and the nav cluster right (6px gap). The page scrolls with a 96px scroll padding so focus and anchors clear the sticky header (140px at 640px and below). The footer is a four-column grid (1.3fr 1.4fr 0.8fr 1fr, gap 40px, padding 40px 24px 28px): brand and one-line tagline, "Explore" links in two columns, "Legal", then "Created by" and "Powered by"; a hairline-topped copyright line closes it. Toasts stack at the top right (80px from the top, 24px from the edge, max 380px, gap 10px).

**Game detail.** Shell padding 20px 24px 72px. A two-column grid: a 380px card column, sticky at 88px from the top, and a fluid working column (gap 28px). The working column stacks panels at 16px: "Your copy" first, then About, then Details. Below the grid, full-width sections (Media, Achievements, Reviews, DLC, series) are separated by 72px. Inside sections: media is a 2:1 split of a 16:9 viewer and a two-column thumb strip; achievements and DLC are auto-fill grids (min 230px and 260px, gap 10px); reviews are a 360px form beside the list (gap 28px); series mini cards are an auto-fill grid (min 200px, gap 16px). Detail rows use a 130px term column.

**Home.** Shell padding 28px 24px 88px. A greeting row (h1 left, totals right, wrapping) sits 28px above the main row on an 8:4 split (gap 28px). The 8 side is Discover, the protagonist: games the player does not own yet. The 4 side is "Your album", a sticky summary panel. 48px below, "Top rated of {year}" and "New this month" sit side by side as two face panels (gap 28px). 72px further, a lower grid on an 8:4 split holds "Trending in Game Rank" (four ranked mini cards) and "Coming soon". The guest Home is a 1:1.15 grid of headline and trailer card (gap 48px), then, 72px below and centered at 920px, a status picker: the trailer's game as a mini card beside "Where is {game} on your list?", four status options (2x2, each with its description; filled in its hue once chosen, as the status menu does) and a "Start your list" button with "Sign up to save your list.". Nothing is chosen at first, so the card starts neutral. It stacks at 480px.

**Catalog.** Shell padding 28px 24px 80px. A title block (h1 plus one ink-2 line that turns into "n filters applied. Clear all" when filters are on) sits 24px above a two-column layout: a 260px filter rail, sticky at 84px, beside the results (gap 28px). The results open with a bar: the tabular result count and an ink-3 "Sorted by …" line on the left, the view switch on the right. The view is Grid or Checklist and lives in the URL (`?view=checklist`; Grid is the default and drops the parameter), so a view can be shared. Grid is an album page of mini cards (auto-fill, min 200px, gap 16px); Checklist is the set table. The pagination closes the results.

**Profile.** Shell padding 28px 24px 88px. A name band (64px avatar, name, @handle and role pill, "Account settings" ghost button pushed right) sits above the trophy shelf: a band ruled top and bottom, not a card, holding two groups on a 4:3 split (gap 28px) with a vertical rule between them: "Album" with four status plates and "Activity" with three record plates. A full-width album split bar closes the shelf under its own rule. 40px below, a lower grid on an 8:4 split (gap 40px 28px): "Your collection" (status tabs over a mini card grid, auto-fill min 200px, gap 14px) with "Your reviews" under it (two columns of ruled notes), and the Favorites panel sticky at 88px in the right column across both rows.

**Trends.** Shell padding 32px 24px 88px. A head ruled at the bottom: the "Trends" title over a one-line description of the selected board (max 52ch) on the left, the board tablist on the right (wrapping under on narrow widths). The board sits 28px below on a 4:8 split (gap 28px): the champion card left, the standings panel (places 2 to 8) right. An ink-3 source note follows the board ("… Equal values share a place. Counted from Game Rank players."). The selected board lives in the URL (`?board=collected|rated|reviewed|favorited`; the first board drops the parameter).

**Sign in / Register.** A 5:6 grid (gap 56px), vertically centered in the free height (min-height `100vh - 260px`; register aligns to the top because its card is taller), padding 48px 24px 88px: on the left the title, a lede (max 36ch) and three ruled perk rows; on the right the member card.

**Admin.** Shell padding 32px 24px 88px. A head ruled at the bottom: the title with its tabular count on the left, the Users / Comments segmented nav on the right. A tool row 22px below (search field up to 420px wide, a live "n of m" count right) sits over one ledger page.

**Terms.** A hero (title and an ink-3 "Last updated … · 11 sections" line), then a 260px table of contents, sticky at 88px, beside the rulebook page (gap 40px), separated from the hero by a hairline aligned to the column edges rather than the padding.

**404.** A 260px sleeve beside the text (gap 56px), centered in the free height, max 900px: title, lede (max 44ch), the requested path, and three exits.

Responsive steps:
- **Shell:** at 1024px the footer goes to two columns; at 900px the search field narrows to 320px; at 768px the header tightens (60px, 16px padding, 12px gap) and the search field fills the free width; at 640px the header wraps into two rows (logo and nav, then a full-width search field), the footer's brand and credits span the full width, and toasts move to the bottom edge at full width (16px gutters); at 480px the Catalog and Trends links become 38px square icon-only links and Sign in / Sign up show only their icons (labels stay for screen readers), the account button drops the name, and the Explore links fall to one column.
- **1100px:** profile: the shelf stacks its two groups; Activity loses its vertical rule.
- **1024px:** detail: card column narrows to 320px, gap 20px; reviews and media stack; thumb strip goes to four columns. Home: the spread and the lower grid stack; the pages separate (20px gap), each regains its full border and 18px radius, and the spread drops its shared lift; the lower area moves to 56px from the spread with 48px between sections. Catalog: the rail narrows to 230px (gap 20px) and the checklist drops its Released column. Profile: the lower grid stacks (collection, favorites, reviews; gap 32px) and favorites lose sticky. Trends: the board stacks and the champion face turns horizontal (art left on a 5:6 split at 16:10, facts right).
- **960px:** terms: single column; the table of contents becomes a static two-column list above the page, ruled below, with no active highlight.
- **860px:** detail: single column; the card loses sticky and centers at max 460px. Home: the guest grid stacks (gap 32px) and the status demo goes to two columns. Catalog: single column; the rail hides and a "Filters" ghost button in the results bar (with an ink count badge when filters are on, `aria-expanded`) opens it in place above the results. Sign in / register: single column (max 560px, gap 28px), perks hide. Admin: table rows stack (see Ledger).
- **760px:** 404: single column; the sleeve shrinks to min(220px, 70%).
- **640px:** Home: the Discover grid and trends go to two columns; the Discover page pads 16px; the spotlight stacks its art above its info. Catalog: the grid goes to two columns (gap 10px) and the album page pads 10px; checklist rows stack. Profile: plates go 2x2 for Album and stay a row of three for Activity (stamp icons hide there); reviews go to one column; the collection grid goes to two columns; the settings button stretches full width. Trends: the tablist becomes a full-width 2x2 grid; standings rows go to two lines. Admin: the segmented nav and the search field stretch full width. Terms: section numerals move inline with their headings.
- **480px:** detail: shell padding 14px 14px 56px; panels pad 16px; sections 56px apart; detail rows stack; achievements and series go to two columns; "Your copy" actions stretch full width. Home: shell padding 18px 14px 64px; the list panels pad 18px 16px; the Discover grid gaps 10px; the Discover and trend segments become full-width grids. Catalog: the results bar stacks, tools spread across the width. Sign in / register: the member card's rim drops to 8px, the face pads 16px, field pairs stack. Pagination: page buttons shrink to 36px (gap 4px). Mini cards everywhere: the name takes the full band on two lines, the Metacritic seal moves onto the art's top-right corner, and the status stamp shows only its icon (the label stays for screen readers).

## Elevation & Depth

Hybrid and restrained. Flat faces on a tonal ground carry most depth, separated by 1px rules. Shadow is reserved for objects a player could pick up (cards) and for transient overlays that sit above the page (menus, toasts, modals, the account drawer). The shell's header and footer are flat bands: a 1px rule, never a shadow. Empty slots (dashed status plates, empty sleeves, the 404's missing card) are never lifted: the absence of a card is the absence of its shadow.

### Shadow Vocabulary
- **Card lift** (`--gd-raise`: `box-shadow: 0 1px 2px rgba(22, 20, 29, 0.06), 0 10px 28px rgba(22, 20, 29, 0.10)`; dark: `0 1px 2px rgba(0, 0, 0, 0.4), 0 12px 32px rgba(0, 0, 0, 0.45)`): the main card, mini cards, the guest trailer card, the profile's trophy plates (not the empty ones), the Trends champion card, the member card on sign in and register, and the Home Discover spotlight card. The catalog's album page is a flat face; only its mini cards lift.
- **Overlay lift** (the same `--gd-raise` token): the user menu, the status menu (also when it opens from a mini card or a checklist row), toasts, the delete-account modal, the confirm and external-link modal, and the profile's account drawer.
- **Modal scrim** (`background: rgba(14, 15, 21, 0.55)`, no blur): behind every modal. The account drawer uses the same scrim.
- **Art inset rule** (`box-shadow: inset 0 0 0 1px` rule): the edge of the main card's and the champion card's art box. The same inset 1px rule rings the active item in the terms contents.
- **Seal on art** (`box-shadow: 0 1px 3px rgba(0, 0, 0, 0.3)`): the small Metacritic seal when it sits over mini card art at 480px and below.

### Named Rules
**The Only Cards Float Rule.** Panels, pages (Discover, album, standings, ledger, rulebook), tables, tiles, chips, tabs, inputs, the profile shelf and the header and footer bands are flat with a hairline border. Only card objects (main card, mini cards, trailer card, trophy plates, champion card, member card, Discover spotlight) carry the lift shadow.

**The Overlay Lift Rule.** The one exception to The Only Cards Float Rule is a transient overlay: menus, toasts, modals and the account drawer take the same lift (`--gd-raise`) because they sit above the page and leave it. Each still keeps its 1px rule border, and scrims stay plain, never blurred.

## Shapes

Rounded rectangles nested from outside in, each radius smaller than its container: card frame 22px, card face 14px, art box 10px, stat cells 8px. Mini cards follow the same nesting (16px frame, 11px face, 7px art); the trailer card uses the main card's (22px frame, 14px face, 10px art). The Discover spotlight uses the main card's nesting (22px frame, 14px face, 10px art). Modals use 18px; panels, "Your copy", the Coming soon list, the user menu and toasts 14px; tiles and the status menu 12px, controls, the segmented track and textarea 10px, small cells, rows and the main card seal 8px, the Coming soon covers 7px, the small seal and checklist thumbs 6px; chips, stamps, owned pills, status tabs, store links and the account button are full pills (999px), avatars and the trailer play toggle are circles. Borders are 1px hairlines by default; 2px marks state (the "Your copy" frame, uncommon rarity, active media thumb) and 3px is reserved for the rare holo frame. Dashed borders mean "empty": the empty state, the album's empty sleeves (sleeves mix 35% of the frame hue into rule-strong), the profile's empty status plates (1px rule-strong) and the 404's missing card (2px, neutral frame mixed 35% into rule-strong).

The views reuse the same radius steps; none adds a new one:
- **Card objects.** The Trends champion card nests like the main card (22px frame, 14px face, 10px art); the member card uses the same 22px frame and 14px face. A trophy plate is a small card on the panel and control steps (14px frame, 10px face). The 404's missing card sleeve uses the mini card step (16px, 8px art well).
- **Pages.** The 18px album step covers every page-like face: the Home Discover page, the catalog's album page, the Trends standings panel, the terms rulebook page. The 14px panel step covers the filter rail, the catalog's set table, the profile's Favorites panel, the admin ledger page and every view's dashed empty state.
- **Controls.** Filter chips and the Trends board tabs are full pills; the board tablist's track is a pill too (14px track with 10px tabs at 640px, where it becomes a grid). The catalog's view switch and the admin nav reuse the segmented control (10px track, 3px inset, 32px segments at 7px). Page buttons, inputs and buttons stay at 10px; table sort buttons at 6px; terms contents items, row icon buttons and code chips at 8px; the terms attribution note at 12px. The album split bar is a 14px pill.
- **The account drawer** is the one square-cornered surface: a full-height panel docked to the right edge, ruled on its left side only.

**Two band placements.** A card prints its name band either inside the face (main card, mini card, trailer card, member card: an even rim of frame around a face whose first row is the band, closed by a hairline) or on the frame itself (trophy plates and the champion card: the frame is open at the top, `padding: 0 Xpx Xpx`, and the band text sits on the frame color in on-frame ink above the face). The on-frame band is used where the band carries a status or rank, not a name.

### Named Rules
**The Empty Slot Rule.** A slot with nothing in it (a status plate at 0, an empty album sleeve, the 404's missing card) is a dashed outline with a transparent or half-transparent face, ink-3 text, no solid frame and no lift. It keeps the shape of the card it is missing, so the page shows where a card would go.

## Components

### Buttons
Solid and plain: ink or white, no gradients.
- **Shape:** gently rounded (10px), 42px tall; small size 34px with 12px side padding.
- **Primary:** ink fill, face text; the single "do it" action in a group (Add to favorites, Publish review, Create an account).
- **Primary** also covers Sign up in the signed-out header (38px) and the confirm action of a non-destructive modal.
- **Ghost:** face fill, rule-strong border, ink text; every secondary action (Back, rating link, Read more, Load more, Cancel, Sign in, Browse the catalog, pager arrows). The header theme toggle is a 38px square ghost icon button (sun or moon glyph in ink-2).
- **Danger:** danger fill with white text (dark ground text in dark theme); only the final destructive action of a modal (Delete account, a destructive confirm). Hover brightens it slightly.
- **Status button:** a ghost button whose border and text take the current status hue, with a trailing chevron; opens the status menu (160ms scale-from-0.96 fade, top-left origin).
- **Hover / Active:** hover only on fine pointers: primary to ink-2, ghost to ground fill with ink-3 border (150ms). Press scales to 0.97 (160ms ease-out). Disabled at reduced opacity.
- **Icon button:** 32px square, 8px radius, transparent, ink-3 glyph; hover fills ground and inks the glyph, destructive variant hovers to danger. Rows and drawers use a 34px version (catalog checklist actions, profile favorites remove, drawer back and close, admin delete); a pressed or expanded icon button turns ink. Admin delete hovers to a 10% danger wash with a danger glyph.
- **Size variants on the views:** the catalog bar, filter rail, terms contact link and pagination use 40px controls; the auth submit is a full-width 46px primary (700, 1rem, press scales to 0.98, disabled at 0.7 opacity with a spinner and "Signing in…" / "Creating account…"); the admin row action is a 34px small ghost ("Make admin", "Remove admin").
- **Quiet button:** text-only ink-2 action with a leading icon, no border or fill, inks on hover ("Go back" on the 404). Only beside a primary and a ghost, as the least likely exit.
- **Text link:** ink text, 600, underlined in rule-strong at 3px offset; the underline takes the text color on hover. Optional trailing arrow ("Open profile"). Inline links in forms and the terms use the plain ink underline ("Clear all", "Sign in", "Terms and Conditions").

### Chips
- **Fact chip:** 1px rule outline pill, 0.875rem Barlow 500; platform names.
- **Store chip:** 32px pill, rule-strong border, face fill, store icon plus external-link mark; hover fills ground.
- **Metacritic seal, card size:** stacked "MC" label over a condensed score (min 54px, 8px radius), colored by threshold; missing score shows an em dash on ground with a rule border. Main card only.
- **Metacritic seal, small:** one line, condensed 800 score (min 30px, 6px radius, 2px 6px padding) with a visually hidden "Metacritic" label; same colors and empty treatment. Mini cards, the trailer card band and checklist rows.
- **Status stamp:** pill in the frame color with on-frame text, in a card's set footer; shows the status icon and label. On the main card it reads "Favorite" in the neutral frame when no status is set; on mini cards it appears only with a status (0.72rem, 700).
- **Owned pill:** a smaller label-only stamp (0.7rem, 700) on checklist rows when the player owns that game, and on the profile's favorites rows. The catalog checklist's "Your status" column prints a slightly larger status pill (2px 9px, 0.78rem, 700) with the status icon; without a status it reads "Favorite" or an em dash in ink-3.
- **Filter chip:** a 32px pill toggle (`aria-pressed`) in the catalog rail: face fill, rule-strong border, Barlow 500 0.875rem; selected fills ink with face text at 600. Unselected hover fills ground with an ink-3 border. Sort chips are single-select, genre and platform chips multi-select. Never a status hue.
- **Role pill:** an outline pill (rule-strong border, ink-2, 0.8 to 0.82rem/600) with a small icon: "Player" with a person glyph; "Administrator" with a crown, filled ink with face text on the admin users table. On the profile name band it stays an outline for both roles.
- **Count badge:** a small ink pill with face text and tabular numerals on the catalog's mobile Filters button, showing how many filters are on.

### Cards / Containers
- **Panel:** face fill, 1px rule border, 14px radius, 20px 22px padding (16px on mobile). No shadow.
- **"Your copy" panel:** the detail's ownership panel. 2px border in the frame color and a 7% frame tint over the face; recolors with the frame (320ms ease-out).
- **Achievement tile:** face fill, 12px radius, 48px badge well beside name and percentage. Rarity is the tile's frame: common keeps the 1px rule, uncommon a 2px rarity-uncommon border, rare a 3px holo gradient border (rarity-rare through gold, violet and cyan) over a 6% rare tint. The foil goes on the frame, never over the badge.
- **DLC tile:** face fill, 1px rule, 12px radius, 72x42 thumb; hover darkens the border to ink-3.
- **Empty state:** dashed rule-strong border, 12 to 14px radius, face fill (transparent on the catalog, profile, Trends and admin, over the ground), centered ink-3 icon and one sentence in ink-2; on the album the icon takes the active status hue and a small ghost button follows. Where a filter caused the emptiness, the sentence names it ("No games match "{query}" with these filters.") and a "Clear filters" ghost button follows.

### Inputs / Fields
- **Textarea:** face fill, 1px rule-strong border, 10px radius, 12px padding, min 110px, vertical resize; character counter below in tabular ink-3.
- **Focus:** border shifts to ink; keyboard focus adds the system ring.
- **Shell search field (header):** the search pattern of the shell. 40px tall, 10px radius, 0 14px padding, ground fill with a 1px rule-strong border, a leading ink-3 search glyph, ink-3 placeholder ("Search a game…"), 0.95rem text; Enter submits. While it holds focus the whole field lifts to the face fill, its border turns ink and it takes the system ring (150ms).
- **Modal text input (delete account):** 42px, face fill, 1px rule-strong border, 10px radius; focus turns the border danger, because the field confirms a destructive action.
- **Form field (auth, account drawer, filter years, admin search):** face fill, 1px rule-strong border, 10px radius, 0 12px padding, ink-3 placeholder ending in an ellipsis or a short example; focus turns the border ink and adds the system ring. Height is 42px on sign in, register, the drawer and the admin search, and 40px for the catalog's compact year inputs (tabular). The label sits above in ink-2 Barlow 600 0.875rem; a hint below in ink-3 0.8rem. A nickname field carries a fixed ink-3 "@" prefix inside the field; password fields carry a 36px reveal icon button (`aria-pressed`) at the right edge. The admin search has a leading ink-3 search glyph and stays on the face fill (unlike the header search on ground). A disabled field fills ground with ink-2 text ("Your email can't be changed."). Search fields (header and admin) hide the browser's native clear button (`::-webkit-search-cancel-button`); Escape still clears them. The header search draws its focus ring on the field container (`:focus-within`), never a second ring on the input.
- **Validation (sign in, register):** forms are `novalidate` and validate on submit: after the first submit every invalid field turns its border danger, sets `aria-invalid` and prints its message in danger in the hint slot below it (empty hint slots collapse), and focus moves to the first invalid field. On register, nickname, email and confirm-password also check live once they hold a value. A server error prints in the inline error alert (role alert, exclamation icon, danger text, 10px radius) above the submit. The same alert serves the drawer's edit and password steps.
- **Checkbox (register terms):** native 18px box with an ink accent, label in ink-2 0.92rem with an underlined ink link.
- **Rating control:** five 34px star buttons, empty in rule-strong, filled in star; hover previews, press scales to 0.9; value printed in condensed type ("4/5" or "Not rated").
- **Focus ring (all controls):** 2px solid status-pending outline, 2px offset.

### Navigation
Site-wide navigation lives in the shell header (see Site Header below). On the detail, in-view navigation is a small ghost Back button above the grid and an in-page link from "Your copy" to the reviews section. In-page switches between different content (Home status tabs and trend segments, profile collection tabs, Trends boards) are WAI-ARIA tablists: arrow keys move and select, Home and End jump to the ends, only the selected tab is in the tab order, and focus follows selection. A switch that only re-presents the same content (the catalog's Grid / Checklist) is a group of `aria-pressed` toggle buttons instead.
- **Status tabs (Home album):** 38px pills with face fill and rule-strong border; each tab carries its own status hue on its icon, and hovering an unselected tab borders it in that hue. The selected tab fills with its hue and prints on-frame text; its count chip turns into a 20% on-frame wash. Counts sit in a ground-filled tabular chip. Colors move on 200ms ease-out.
- **Segmented control (Home trends):** a 1px rule, 10px track with 3px inset; 32px segments in ink-2 on a transparent fill, the selected one filled ink with face text; unselected hover fills ground. At 480px the track becomes a full-width 2x2 grid. The same geometry serves two non-tablist switches: the catalog's Grid / Checklist view switch (two `aria-pressed` buttons with icons in a labeled group; it re-presents the same results, so it is a toggle, not a tablist) and the admin Users / Comments nav (two links, the current page marked `aria-current="page"` and filled ink; full width at 640px).
- **Collection tabs (profile):** the Home status tabs reused, plus an "All" tab that stays in the neutral frame (filled frame-neutral when selected). A WAI-ARIA tablist over one tabpanel of mini cards, with arrow, Home and End keys.
- **Board tablist (Trends):** a pill track (1px rule, face fill, 4px inset, 4px gap) of 38px pill tabs with an icon and label in ink-2 0.92rem/600; the selected tab fills ink with face text (180ms); press scales to 0.97. A WAI-ARIA tablist over one board tabpanel; the selection is written to the URL with `router.replace`, so it does not add history entries. At 640px it becomes a full-width 2x2 grid (14px track, 10px tabs).
- **Pagination:** a centered row of 40px squares (10px radius, rule-strong border, face fill, gap 6px) with page numbers in condensed 700 1.05rem tabular, ink-3 ellipses and ink-2 chevron arrows at the ends. The current page fills ink with face text and carries `aria-current="page"`, the same ink mark as the current nav route; disabled arrows drop to 0.4 opacity. Hover fills ground with an ink-3 border; press scales to 0.95. Used by the catalog (capped at 500 pages, RAWG's limit) and the profile favorites panel; hidden with one page.
- **Contents (terms):** see Rulebook.

### The Card (signature component)
A frame (22px radius, 10px padding, card lift) around a white face (14px radius, 14px padding, 12px gap) holding, in order: the name band (display name left, Metacritic seal right); the 4:3 art box with cover crop and inset rule; the genre line (Barlow 600, 0.9rem, ink-2); three ruled stat cells (Community, Release, Platforms; columns 1fr 1.35fr 1fr, gap 6px); the set footer above a hairline (set number "No. {id}", "Data by RAWG" credit, status stamp pushed right). Frame, stamp and "Your copy" recolor together on status change (320ms ease-out). The skeleton keeps the same structure with a rule-colored frame.

**Holo sweep:** on a status change made by the player (never on initial load), a 105-degree band of cyan, violet and yellow at 80 to 90% alpha, screen-blended, crosses the art once from -110% to 110% over 900ms on the shared ease-in-out curve and fades in its last 20%. Removed entirely under `prefers-reduced-motion: reduce`.

**Trailer card (guest Home):** the same card grammar holding a video: neutral frame (22px, 10px padding, card lift), face (14px, 12px padding) with a name band (condensed 800, 1.5rem, small Metacritic seal), a 16:9 art box on black with a circular pause/play toggle, and a caption footer ("No. {id}" left, "Data by RAWG" right). Without a game it falls back to "Featured trailer".

### Mini Card
The shared small card (`components/CardWorld/MiniCard.vue`), used for detail series entries, every card on the Home, the catalog grid and the profile collection. Frame (6px padding, 16px radius, card lift) around a face (11px radius, 10px padding, 8px gap): a fixed-height name band (condensed 800, 1.1rem, two-line clamp) with the small Metacritic seal, the 4:3 art (7px radius), and a two-line set block. Line one always reads "No. {id}" (condensed 700, ink-2) on the left and the release year (or "TBA") on the right; line two is a reserved 24px stamp slot, so every card has the same height whether or not it carries a stamp, and the corner actions align with it.

Props: `game` (required; `id`, `name`, `imge_url`, `metacritic`, `release_date`), `status` (the player's status key or null), `favorite` (boolean), `showFavorite` (shows the heart toggle), `canChangeStatus` (shows the status button). Emits `toggle-favorite` (game id) and `update:status`.
- **Status:** with a status the frame takes the status hue and line two holds the status stamp (icon and label); without one the frame stays neutral and line two stays empty. Detail series cards are not given a status; Home, catalog and profile cards are given the player's status wherever it is known.
- **Corner actions:** 30px transparent icon buttons in the bottom-right corner, on line two. The favorite heart (`aria-pressed`, filled and ink when on) sits rightmost; the status button (a bookmark glyph printed in the frame's hue, ink-3 on a neutral frame) sits to its left and opens the status menu above the corner (bottom-right origin, 160ms scale-from-0.96 fade, closes on outside press or Escape). The stamp slot pads its right edge so the stamp never runs under them. The catalog and profile only offer the status button for released favorites.
- **Motion:** hover lifts the card 3px (200ms ease-out) on fine pointers; the frame recolors on 320ms ease-out.
- **Guest demo:** without a game id it renders as a non-link with no set number.
- **480px:** the name takes the whole band (0.95rem), the seal moves onto the art's top-right corner with the seal-on-art shadow, and the stamp shows its icon only (3px 7px padding; the label stays for screen readers and as the title), since the frame already says the status and the corner actions need the room.

### Discover (Home)
The Home's protagonist: games the player has not added yet, so the page invites adding, rating and reviewing rather than showing what is already owned. A face page (1px rule, 18px radius, 22px 24px padding) with a head (section heading, an ink-2 line "Games you haven't added yet. Add one, or rate what you've played.", and a segmented tablist "Popular" / "Acclaimed", which request RAWG ordering `-added` and `-metacritic`). The list excludes every game in the player's collection or favorites and any game without art; a game added from this page stays visible with its heart filled until the list reloads.
- **Spotlight:** the first game as a card in the neutral frame (10px rim, 22/14/10 nesting, card lift): 16:10 art with the inset rule on the left, and on the right the name (condensed 800, 2rem, a link), the Metacritic seal, a meta line ("No. {id}", year, RAWG rating with a gold star) and two actions: "Add to favorites" (primary; turns ghost "In your favorites" once added) and "Rate & review" (ghost, links to the game's reviews).
- **Grid:** the next six games as mini cards (3 columns, gap 14px) with the favorite heart, which adds the game to favorites.
- **Foot:** above a hairline, a small ghost "More picks" button (next page) and an "Open the catalog" link.
- Loading shows a 250px spotlight skeleton and six pocket skeletons; an empty list uses the dashed empty state.

### Your Album Summary (Home)
A sticky face panel (1px rule, 14px radius, 18px padding, top 88px) beside Discover: a condensed 800 1.45rem "Your album" title with an "Open" link to the profile, a 2x2 grid of status counts (each a 10px-radius chip with icon, label and condensed count; in its status hue with a 7% tint and 1px frame border only when the count is above 0, otherwise a dashed empty slot in ink-3), then "Continue playing" (falling back to "Up next" for pending, then "Paused for now") with up to three rows (thumb, name, "No. {id}") that inherit their status frame. With nothing in progress: "Nothing in progress. Pick something from Discover." It stacks under Discover at 1024px and below.

### Checklist Row (Home)
A numbered hairline list, like a card set checklist: rows divided by 1px rules, each a link with a condensed ink-3 rank (1.4rem), a 64x48 thumb (6px radius, ground well), the name (Barlow 600, 0.95rem, single-line ellipsis) over a metadata line ("No. {id}" in condensed ink-2, release date, owned pill), and a right-aligned value: RAWG player rating with a star in "Top rated", the small Metacritic seal in "New this month". Rows inherit the player's status frame so the owned pill takes its hue. Hover fills ground (8px radius). The "Top rated" heading carries the source line "Player ratings on RAWG".

### Coming Soon List (Home)
A hairline panel (face fill, 1px rule, 14px radius) of rows split by rules. Each row is one link: the game's cover as a 76x57 thumb (7px radius, ground well, 1px inset rule), then the name (Barlow 600, up to two lines) over a date line, the release date in condensed 700 ink-2 tabular ("Oct 6", the year only when it is not the current one) and a countdown in ink-3 ("Today" in ink, "Tomorrow", "In n days"), and a chevron. The cover leads the row, not a date tile. Hover fills ground. A pager below holds two small ghost arrow buttons around a tabular "Page n of m".

### Site Header (shell)
A flat face band, sticky, closed by a 1px rule at the bottom and never shadowed. Inside the 1240px shell: the logo, the shell search field (signed in only), then the nav cluster.
- **Theme toggle:** the ghost icon button (38px, 10px radius); press scales to 0.95.
- **Nav links (Catalog, Trends):** 38px, 0 12px padding, icon plus label in Barlow 600 0.95rem, ink-2 at rest; hover fills ground and inks the text. The link of the current route turns ink and carries a 2px ink bar along its bottom edge (squared bottom corners); there is no filled active pill.
- **Account button:** a 42px pill (rule-strong border, face fill, 3px 10px 3px 3px padding) holding a 34px circular avatar, the first name (ellipsis at 120px) and a small ink-3 chevron. The avatar is a neutral-frame circle with the initial printed in Barlow Condensed 800. Hover darkens the border to ink-3; while the menu is open the border is ink.
- **Signed out:** Sign in as a 38px ghost button and Sign up as a 38px primary (ink) button, each with a leading icon; press scales to 0.97.
- **Loading:** skeleton blocks in place of the links and account button.
- **Logo ("Card G"):** a single-ink letter-symbol where the card's own frame draws the G: the opening sits top right and the crossbar steps in toward the face. Beside it, the "GAME RANK" wordmark in Barlow Condensed 800 outlined to paths, tracking 0.02em. Both are inline SVG in `App.vue` (`.logo-symbol`, `.logo-wordmark`, `aria-hidden`); the accessible name is `aria-label="Game Rank home"` on `.logo-link`. Color is `currentColor` set to ink (#16141D light, #F1F0F6 dark): never a status hue or violet. Geometry on a 256 viewBox: card 172x236, outer radius 32, inner 8, vertical stroke 36 and horizontal 34 (optical correction), opening y 74–120, crossbar y 120–154 reaching x 126. A small cut (strokes 44/42, larger opening) serves 24px and below and the favicon. In the header the lockup is 40px tall (38px at 480px and below), gap 7px; the wordmark cap height is 0.42 of the symbol height and the symbol–wordmark gap 44/256 of it. The wordmark hides at 599px and below and from 641 to 840px, leaving the symbol. Minimums: lockup 24px tall, symbol 16px (small cut). Clear space: the vertical frame stroke (36/256 of the height) on every side. Files in `frontend/src/assets/brand/` (symbol, symbol-small, wordmark, lockup, white variants for non-token dark grounds, and an app-icon tile: ink #16141D with a white G); favicon set in `frontend/public/` (`favicon.svg` switching #16141D / #F1F0F6 with `prefers-color-scheme`, `favicon.ico`, apple-touch and 192/512/maskable icons, `site.webmanifest` with theme and background #EEF0F4). The browser `theme-color` follows the ground: #EEF0F4 light, #0E0F15 dark.

### User Menu (shell)
A face panel (290px, 1px rule, 14px radius, overlay lift) dropping 8px below the account button, right-aligned. A header row holds a 44px avatar with two initials, the full name (Barlow Condensed 800, 1.15rem) and the email (0.8rem, ink-3). Groups (Profile; Administration for admins, with a small ink-3 sentence-case section label; Delete account and Sign out) are separated by 1px hairlines. Items are 40px rows (8px radius, 8px 10px padding) with a plain 18px ink-3 icon and a Barlow 600 0.95rem label; hover fills ground. Only "Delete account" is colored, in danger (label and icon). Opens with a 160ms scale-from-0.96 fade from the top-right corner and closes on a 100ms fade.

### Site Footer (shell)
A flat face band with a 1px rule on top. Column headings are Barlow Condensed (brand 1.6rem/800, section titles 1.15rem/700); the tagline (max 34ch) and links are ink-2, 0.95rem, with an underline that is transparent at rest and takes the text color on hover while the link inks (150ms). "Created by" and "Powered by" are ink-3 small labels (0.8rem, 600) above their links (GitHub and RAWG, with leading icons). A hairline-topped copyright line in ink-3 (0.85rem) closes the footer.

### Modals
One grammar for the delete-account modal (shell) and the shared confirm and external-link modal (`.ext-modal` in `style.css`): a face panel (1px rule, 18px radius, 28px padding, 420 to 440px wide, overlay lift), centered on a plain dark scrim with no blur. Content is centered: a plain icon above the title with no chip or well (ink-2, or danger when the action destroys something), a Barlow Condensed 800 title at 1.6rem, an ink-2 body (0.95rem, line-height 1.55), then a row of equal-width 42px buttons: ghost Cancel beside a primary confirm or a danger action. In the confirm modal focus starts on Cancel. Enter is a 220ms fade with the panel rising 8px from 0.97 scale; exit is 150ms.

### Toasts
A face card (1px rule, 14px radius, overlay lift, 12px 12px 12px 14px padding, min 280px) with a 34px icon chip (9px radius), a Barlow Condensed 800 title (1.1rem) over an ink-2 message (0.9rem), and a 28px ghost close button. The chip is ink with a face glyph for success, info and warning; only errors switch the chip to danger. Status hues are never used here (The Frame Means Ownership Rule). Toasts enter and leave through the same edge: 220ms in, 160ms out, sliding 16px from the right on desktop and from below at 640px and down; the stack reflows on 220ms.

### Status Menu
The menu behind the status button (`GameStatusDropdown.vue`, used on the detail, inside the mini card and from the catalog checklist's bookmark button, where it opens below the button from the top-right corner): a face panel (min 180px, 4px padding, 1px rule, 12px radius, overlay lift). Each status option is a 0.92rem/600 row (8px radius, 8px 10px padding) whose icon is tinted in its own status hue through the shared frame classes; hover fills ground. The selected option fills with its status hue, prints on-frame text and ends in a check, like a frame. A hairline divider separates "Remove status", a centered danger text action shown only when a status is set. Opens with the same 160ms scale-from-0.96 fade as the user menu, from the top-left corner.

### Filter Rail (catalog)
A face panel (1px rule, 14px radius, 18px padding, 18px gap) headed "Filters" in title type. Four fieldsets separated by hairlines, each with an ink-3 legend: "Sort by", "Genres" and "Platforms" as filter chips, "Release year" as two 40px From / To year inputs. A ruled action row closes it: a ghost "Clear" and a primary "Apply filters" (auto and 1fr columns, 40px). Choices stay local until applied. The rail is sticky beside the results on desktop and a toggled in-flow panel at 860px and below.

### Set Table (catalog checklist)
The catalog's checklist view: a real `<table>` in a face panel (1px rule, 14px radius) with a visually hidden caption ("n games, page p"). Columns: "No." (condensed 700, ink-2, tabular), "Game" (56x42 thumb at 6px on a ground well, then the name in Barlow 600, underlined on hover), "Released" (ink-2, tabular), "Metacritic" (small seal), "Your status" (status pill, "Favorite" or an em dash) and an unlabeled actions column (a fixed 34px slot for the status bookmark so the hearts align, then the heart toggle). Headers are ink-3 0.82rem/600 over a hairline. "Game", "Released" and "Metacritic" are sort buttons with a sort glyph: the header cell carries `aria-sort` (ascending, descending or none), and the sorted header turns ink with a filled up or down glyph. A first click sorts dates and scores high to low and names A to Z, a second click reverses; sorting returns to page 1 and the "Sorted by …" line follows. Rows are 8px 12px with hairlines; hover fills ground at 60%; owned rows take the status tint (The Owned Row Rule). Loading shows eight 52px skeleton rows.
- **1024px:** the Released column hides.
- **640px:** the header row is visually hidden and each row becomes a compact two-line grid: game link across the top, the seal and status pill below it (indented to the name), the actions on the right spanning both lines; the owned tint is painted once on the row.

### Trophy Shelf (profile)
The profile's totals as a shelf of plates on the page ground, ruled above and below. A **trophy plate** is a small card: a frame (14px radius, open at the top with 0 5px 5px padding, card lift) whose 32px band prints a stamp (icon plus label in condensed 700 1rem, on-frame ink) above a white face (10px radius, min 62px, 10px 12px padding) holding one bottom-aligned figure (condensed 800 2.4rem, tabular).
- **Album group:** four status plates, ordered Completed, Playing, Paused, Pending. A plate takes its status frame only when its count is above 0; at 0 it is an empty slot (1px dashed rule-strong outline, transparent face, ink-3 stamp and figure, no lift).
- **Activity group:** Favorites (heart), Reviews (speech bubbles) and Avg. rating (star in star gold) in the neutral frame, always.
- **Album split bar:** under its own hairline, a total ("**n** games in your album", the figure in condensed 800 1.25rem) over a 14px pill bar split into status segments with 3px gaps, each segment's width proportional to its count (min 8px, hidden at 0), then a legend of 10px status dots with label and tabular count. The bar is `role="img"` with a spoken summary; the legend is hidden from assistive tech. With an empty album the bar is a ground track ringed by an inset rule.
- Loading shows seven 104px skeleton plates.

### Profile Lower Area
- **Collection:** a "Your collection" section heading, the collection tabs, then a grid of mini cards (favorite on, heart removes the favorite, status button for released games). Empty album: the empty state with "Browse the catalog"; empty tab: the empty state with that status's icon.
- **Favorites panel:** a face panel (18px padding, 14px radius), sticky at 88px on desktop, headed "Favorites" with a count; a numbered-checklist variant without ranks: 52x39 thumb (6px), name (600, 0.92rem, ellipsis), then "No. {id}" and the owned pill or "No status", and a 34px trash icon button (spinner while removing). Paginated with the shared pagination, 8 rows per page.
- **Your reviews:** a section heading with count over a two-column grid of hairline-topped notes: game name (700, ellipsis, links to the game), star-gold rating in condensed type, a three-line-clamped ink-2 body and an ink-3 date. Four show at first; a small ghost toggle shows all ("Show all n reviews" / "Show fewer", `aria-expanded`).

### Account Drawer (profile)
Account settings live in a right-docked drawer, not on the page: a full-height face panel (min(380px, 100%) wide, 22px padding, 20px gap, 1px rule on its left edge, overlay lift) over the modal scrim (55%), teleported to the body under `cw-scope`, `role="dialog"` and `aria-modal`. It enters by sliding in from the right edge (260ms on the drawer curve) while the scrim fades (220ms), and leaves the same way. The head holds the condensed 800 1.6rem title and a 34px close button; opening moves focus to the close button; Escape and a scrim click close it, except while saving.
- **Info step:** a definition list of hairline-ruled rows (100px ink-3 term column, 600 values), then a stacked primary "Edit profile" and ghost "Change password" (full width), an "Administration" group for admins and a "Terms and Conditions" row, each group ruled on top. Group rows are 40px link rows with an 18px ink-3 icon, hover ground, like the user menu items.
- **Edit and password steps:** the same drawer swaps its body for a form; the title changes ("Edit profile", "Change password") and a back arrow icon button appears left of it. Fields follow the form field pattern (the email shows disabled with its hint), errors print in the inline error alert, and a ruled footer holds ghost Cancel and a primary submit with a check icon (spinner and "Saving…" / "Updating…" while busy). Cancel and back return to the info step.

### Standings Board (Trends)
One ranking at a time, chosen with the board tablist: Most collected, Top rated, Most reviewed, Most favorited. Switching boards fades the board out (120ms) and the new one in, rising 6px (220ms).
- **Champion card (No. 1):** the card grammar at full size with the band on the frame: a frame (22px radius, 0 7px 7px padding, card lift) in the neutral frame, or in the player's status hue when they own the game. The band prints "No. 1" (condensed 800 1.6rem) left and the lead right (condensed 700 1.05rem, tabular): "+n over No. 2" (one decimal on Top rated), "Tied for first" when No. 2 shares the place, "Only entry" when alone. The face (14px radius, 12px padding, 12px gap) holds the 4:3 art (10px radius, inset rule), the name (condensed 800 1.9rem), a ruled stat line (the value in condensed 800 3.6rem, its unit in ink-2, and on Top rated "from n reviews" in ink-3), and a set footer: "No. {id}", year, status stamp when owned, the small Metacritic seal pushed right. The whole card is one link; hover lifts it 3px and underlines the name. At 1024px the face goes horizontal (art on the left at 16:10).
- **Ranked rows (places 2 to 8):** an ordered list in a face panel (1px rule, 18px radius), rows split by hairlines. Each row is one link on a four-column grid (44px rank, 72x54 thumb at 7px, identity, a stat column of min 170px or 32%; gap 14px, 12px 16px padding): the place in condensed 800 2.1rem, the name (700, ellipsis) over "No. {id}", year and a status stamp when owned, then the value right-aligned (condensed 800 1.35rem with an ink-3 Barlow unit; on Top rated followed by " · n reviews") over a 6px data bar. Owned rows take the 7% status tint (13% on hover); other rows hover to ground. At 640px each row folds to two lines: rank and thumb on the left, identity on top, value and bar side by side below.
- **Competition ranking:** equal values share a place and the next place skips ("1, 2, 2, 4"); the champion card reports a shared first place in its band. A visually hidden "Place" precedes each number.
- **Data bars (The Ink Bars Rule):** a ground track with an ink-2 fill, proportional to the board's maximum (out of 5 on Top rated), never under 4% so a value stays visible. The fill grows from the left once (420ms ease-out); reduced motion shows it static.
- **Top rated** counts only games with at least 3 reviews (`MIN_RESENAS_VALORADOS = 3` in `backend/app/repositories/comment_repo.py`); its rows and champion name the review count.
- Loading shows a 20px-radius champion skeleton beside seven 64px row skeletons; empty and error states use the dashed empty state.

### Member Card (sign in, register)
The form is printed on the face of a card in the neutral frame: an even 10px rim (8px at 480px) at 22px radius with the card lift, around a face (14px radius, 20px 22px 16px padding, 18px gap). The name band sits inside the face, closed by a hairline: the card title (condensed 800 1.9rem: "Sign in", "Create account") left and a set label (condensed 700 1rem, ink-3: "Returning", "New member") right. The form follows (16px gap; field pairs side by side on register), then the full-width 46px submit and a centered ink-2 line linking to the other form. A ruled set footer closes the card and is hidden from assistive tech: on register it reads "@{nickname}" live as the player types (condensed 700 1.1rem, ink-2, ellipsis; "@your_nickname" while empty) and "Member since {year}"; on sign in it reads "Game Rank" and "Game data by RAWG". The frame never takes a status hue: an account is not a game in the collection.

### Ledger (admin users, admin comments)
The admin pages are a tool, not a collection: no card objects, no lift and no status hue anywhere. The data sits on one face page (1px rule, 14px radius) as a table. Headers are ink-3 0.82rem/600 over a rule-strong line; rows are 12px 16px with hairlines between them, 0.92rem ink text, hover ground at 60%.
- **Users:** a 38px neutral-frame avatar with two condensed 800 initials beside the name (700) and an ink-3 @handle; email in ink-2; the role pill (ink-filled for administrators); the join date in ink-2 tabular; actions right: a 34px small ghost button ("Make admin" / "Remove admin") and a danger-hover trash icon button.
- **Comments:** the same user cell; the game as "No. {id}" in condensed 700 with a small external-link glyph (opens in a new tab); the comment (46% wide) with a star-gold rating figure before a two-line-clamped ink-2 excerpt; the date; a trash icon button.
- **860px:** the header row is visually hidden and each row becomes a stacked entry: the user cell with the actions on its right, then every other cell on its own line, indented 50px to align with the name.
- Search filters the rows client-side and the "n of m" count updates politely; loading shows six skeleton rows inside the page; no results use the dashed empty state quoting the query.

### Rulebook (terms)
Long reading as a ruled rulebook.
- **Contents:** a "Contents" title (condensed 700 1.2rem, ink-2) over a list of links, each a two-digit numeral (condensed 700, ink-3, tabular, 20px column) and the section name (ink-2, 500, 0.9rem), 7px 10px padding at 8px radius. The active item is a face chip ringed by an inset 1px rule, ink 700 text and numeral, with `aria-current="location"`. The active section is computed from positions, not from which observer entry fired: it is the last section whose top has passed 35% of the viewport height, recomputed on every intersection change and when the page resizes. A click scrolls smoothly to the section (instantly under reduced motion). Sticky on desktop; at 960px it becomes a static two-column list without the active state.
- **Page:** a face page (1px rule, 18px radius, 8px 36px 28px padding, max 760px). Each section is a two-column grid (52px numeral column, 8px gap, 28px vertical padding), with a hairline between sections. The numeral hangs in the left column (condensed 800 1.8rem, ink-3, two digits) beside the heading (condensed 800 1.75rem) and the body (ink-2, 1rem, line-height 1.65). At 640px the numeral moves inline on the heading's baseline (1.45rem and 1.5rem) and the page pads 4px 18px 20px.
- **Inside a section:** lists use a short 8x2px ink-3 dash instead of a bullet; inline links are ink 600 with an underline; the RAWG attribution is a note on the ground fill (1px rule, 12px radius, ink-3 icon, ink title, ink-2 text); the contact section ends in a 40px ghost link; a ruled ink-3 footnote closes the page.

### Missing Card (404)
The missing card's empty sleeve, not a card: a 1px dashed outline (neutral frame mixed 35% into rule-strong), like every album sleeve, at 16px radius with 14px padding, no fill, no frame and no lift. Inside, the shape of a mini card: a 4:3 art well (8px radius, face at 60%) holding a large ink-3 question glyph, the name "Missing card" (condensed 800 1.3rem, ink-3), and a set line "No. 404" (condensed 700, ink-2) with "Not in the set". The sleeve is decorative (`aria-hidden`). Beside it: the title "This page isn't in the set", an ink-2 lede, the requested path in a monospace code chip (face, 1px rule, 8px radius, ellipsis), and three exits in falling weight: primary "Go home", ghost "Browse the catalog", quiet "Go back" (browser history, or home when there is none).

## Do's and Don'ts

### Do:
- **Do** keep the card frame as the only large color on a card, and tie it to collection status: neutral until the game has a status, then exactly one status hue.
- **Do** give a surface a status tint (7%) and 2px status frame only when it holds the player's own copies, as "Your copy" and the Home album summary's counts do; in a mixed list, tint an owned row 7% with no frame.
- **Do** pass the player's status to every mini card and champion card where it is known; leave the frame neutral where it is not.
- **Do** show a count of zero as an empty slot (dashed, no fill, no lift, ink-3), not as a colored card with a 0.
- **Do** select tools (filter chips, view switch, board tabs, admin nav, current page) in ink; keep status hues for the collection.
- **Do** keep a view's sharable state in the URL with `router.replace` (`?view=checklist`, `?board=rated`), dropping the parameter for the default.
- **Do** rank with competition ranking (ties share a place, the next place skips) and say so in the source note.
- **Do** recolor frame, stamp and ownership surfaces together on the same 320ms ease-out transition.
- **Do** join a new view to the world with the `card-world` root class, put `cw-scope` on loose pieces that live outside a view root (shell parts, anything teleported to the body, such as the account drawer), and reuse the shared frame, heading, count and seal classes and the mini card component instead of copying them.
- **Do** print names, headings and numbers in Barlow Condensed and keep labels and prose in Barlow, sentence case.
- **Do** use tabular numerals for every stat, score, count, rank and percentage.
- **Do** nest radii from outside in (22, 14, 10, 8) and separate flat surfaces with 1px rules; reuse the existing radius steps for new surfaces instead of adding one.
- **Do** reserve the lift shadow for card objects (including trophy plates, the champion card, the member card and the Discover spotlight) and transient overlays (menus, toasts, modals, the account drawer).
- **Do** keep feedback in ink: toast icon chips are ink, and only errors and destructive actions take danger.
- **Do** mark the current route in the header with the 2px ink bar, not a filled pill.
- **Do** keep the RAWG credit printed on the card face, and label RAWG-sourced figures as such ("Player ratings on RAWG").
- **Do** build in-page switches between different content as WAI-ARIA tablists with arrow-key, Home and End navigation; use `aria-pressed` toggles when the switch only re-presents the same content, and `aria-sort` on sortable table headers.
- **Do** validate forms on submit: per-field danger border, `aria-invalid` and message under the field, focus on the first invalid field.
- **Do** collapse a data table into stacked rows on narrow screens (catalog checklist at 640px, admin ledger at 860px), keeping the header for screen readers only.
- **Do** remove the holo sweep under reduced motion and keep every other transition to opacity and color there.
- **Do** define both themes for every new token; dark lifts status hues and flips on-frame text to the dark ground.

### Don't:
- **Don't** add a second signature motion; the holo sweep is the only one, and it runs only on a player-made status change.
- **Don't** add a large color field that is not the player's status, or tint panels that do not hold the player's own copies.
- **Don't** lay holographic foil over achievement badges or card art at rest; foil lives on the rare tile's frame and in the one-time sweep.
- **Don't** open a game page with a blurred-cover banner, a floating score badge and tabs; the card is the hero.
- **Don't** use uppercase tracked labels; labels are sentence case.
- **Don't** apply shadows to panels, pages, tiles, chips, tabs, inputs or the header and footer bands.
- **Don't** use status hues for notifications, avatars or other shell feedback; they belong to the player's collection.
- **Don't** fill a community data bar with a status hue; community figures are ink.
- **Don't** put card objects, lift or status hue on the admin ledger; it is a tool.
- **Don't** blur the scrim behind a modal or the account drawer.

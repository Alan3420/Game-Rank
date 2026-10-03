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
---

# Design System: Game Rank

> **Scope.** This system is built on two migrated surfaces: the game detail route (`/game/:id`, `frontend/src/components/GameDetail/`) and the Home (`/`, `frontend/src/components/Home/`). The other eight views (Login, Register, Terms, catalog, profile, trends, admin users, admin comments) still run the previous system (Sora type, neumorphic header and footer, the `:root` tokens in `frontend/src/style.css`). That is scope, not drift: those views migrate to this system later. The tokens below live as `--gd-*` custom properties on the `.card-world` class (light) and `[data-theme="dark"] .card-world` (dark) in `frontend/src/styles/card-world.css`; a view joins the world by putting `card-world` on its root element. The same file holds the shared world classes (status frame, section heading, count, small Metacritic seal). Barlow and Barlow Condensed are imported globally through `@fontsource` in `frontend/src/main.js`; the motion curves are global (`:root` in `style.css`). Shared parts live in `frontend/src/components/CardWorld/` (the mini card) and `frontend/src/utils/metacritic.js` (seal thresholds).

## Overview

**Creative North Star: "The Collectible Card"**

Every game is a trading card. RAWG prints the facts on the card face (name, art, genres, release, platforms, Metacritic, set number); the player's collection status colors the frame and their rating and review sit beside it. The world is a cool card-stock ground, white card faces and near-black ink, with one thick rounded frame as the only large field of color on a card. That frame is neutral ink while the game is not in the player's collection and takes one solid status hue when it is. Surfaces that hold the player's own copies (the "Your copy" panel, the Home album page) take the same status hue as a light tint and a 2px frame.

Density is moderate and editorial. The game detail sets a sticky card column next to a working column of panels; the Home opens as a card album, the player's binder of owned cards on the left page and the world's checklists on the right. Surfaces are flat white faces on a pale ground, held apart by hairline rules rather than shadows; only card objects (the main card, mini cards, the trailer card) and the open album spread as one object are lifted. Motion is quiet everywhere except one signature: when the player changes status, a holographic band sweeps once across the card art.

The world rejects the category default of a blurred-cover banner with a score badge and tabs, and of a full-width hero over identical carousels. Facts are framed as card stats and checklist entries, not as banners.

**Key Characteristics:**
- Card object first: thick rounded frame, inset 4:3 art box, ruled stat cells, set-number footer with RAWG credit.
- One large color, and it means collection status.
- Condensed display type for names and numbers, plain Barlow for everything else.
- Hairline rules and tonal ground instead of shadows for non-card surfaces.
- One signature motion (holo sweep), removed under reduced motion.
- Light theme default; dark theme is a full token remap, not an inversion filter.

## Colors

A cool, nearly achromatic paper-and-ink base with a small, semantic set of saturated hues that each mean exactly one thing on the card.

### Primary
- **Collection Status Frame** (frame-neutral when not owned; status-pending, status-playing, status-paused, status-completed when owned): card and mini card frames, status stamps, the owned pill on checklist rows, the Home status tabs (icon at rest, full fill when selected), the "Your copy" panel border and its 7% tint (`color-mix(in srgb, frame 7%, face)`), the Home album page border and the same 7% tint in the active tab's hue, and the status button outline and text. Pending is a clear blue, Playing a deep green, Paused a burnt amber, Completed a violet. In dark theme every hue is lifted to a lighter tint and the text on a status frame flips to the dark ground (on-frame-dark); the neutral frame keeps light text (`--gd-on-frame-neutral`, #F1F0F6 in dark) so the "Favorite" stamp holds AA contrast (7.95:1). Any container opts into a status with the shared frame classes (`cw-frame` plus `cw-frame--pendiente|jugando|pausado|completado`), which set the frame hue and its on-frame text for everything inside.

### Secondary
- **Metacritic Seal** (metacritic-high, metacritic-mid, metacritic-low; metacritic-none for missing scores): the score seal on the main card, mini cards, the guest trailer card and "New this month" rows. Thresholds, shared by every surface: 80 and above high, 50 to 79 mid, below 50 low, no score none. White text on all three; the same values in both themes.
- **Star Gold** (star): filled rating stars in the rating control, the Community stat, review ratings, the RAWG player rating on "Top rated" rows and the average-rating total on the Home greeting. Empty stars use rule-strong.

### Tertiary
- **Rarity Inks** (rarity-rare, rarity-uncommon, rarity-common): achievement rarity. Rare (under 10% of players) owns the holo frame and a burnt-amber star; uncommon (under 40%) a blue frame and rotated square; common a grey dot and the default hairline. Uncommon shares the Pending blue value; it is a shared value, not a shared meaning.

### Neutral
- **Card Stock** (ground): the page ground, empty art boxes, avatar and thumb wells, tab counts, date tiles, ghost and row hover fill.
- **Card Face** (face): panels, card faces, the Home facing page, tiles, inputs, ghost buttons, unselected tabs.
- **Ink** (ink): headings, names, primary button fill, selected segment fill, active thumb outline, text selection fill.
- **Ink 2** (ink-2): prose, genre line, set numbers, primary button hover.
- **Ink 3** (ink-3): labels, metadata, counts, ranks, hints, placeholders, icon buttons at rest.
- **Rule** (rule): hairline borders on panels, the facing page, stat cells, tiles, detail rows, checklist and calendar dividers, review dividers.
- **Strong Rule** (rule-strong): control borders (ghost buttons, textarea, store chips, status tabs), link underlines, empty stars, dashed empty states.
- **Danger** (danger, danger-dark): destructive icon-button hover and the error icon. Light shares the metacritic-low value; dark lifts to a light coral.

### Named Rules
**The One Frame Rule.** On a card, the frame is the only large field of color. Beyond cards, the only large colored surfaces are tinted ownership surfaces: a 7% status tint with a 2px status frame on a surface that holds the player's own copy ("Your copy" on the detail, the album page on the Home). Every other colored element (Metacritic seal, stamps, owned pills, stars, rarity marks) is small. A new surface does not add a large color that is not the player's status.

**The Frame Means Ownership Rule.** A frame stays neutral until the game is in the player's collection with a status; only then does it take the status hue, and the ownership surface takes the same hue with it. A mini card shows a status frame only when it is given the player's status for that game. Status hue never decorates anything unrelated to the player's collection, with two exceptions: the focus ring, which uses the Pending blue as the system focus color, and the guest "Your status is the frame" demo, which shows one card in all four status frames to explain the rule.

## Typography

**Display Font:** Barlow Condensed 700/800 (with Barlow, sans-serif)
**Body Font:** Barlow 400/500/600/700 (with system-ui, sans-serif)

Both are self-hosted through `@fontsource` and imported once in `main.js`. Inside `.card-world`, every element except PrimeIcons inherits Barlow (through a zero-specificity `:where()` rule), overriding the legacy global Sora rule.

**Character:** A sports-card pairing: the condensed face prints names and numbers with the punch of a card's name band and stat line, while regular Barlow keeps prose, labels and controls quiet and legible.

### Hierarchy
- **Page title** (Barlow Condensed 800, line-height about 1, balanced wrapping): the Home's h1s. Player greeting 2.75rem (2.1rem at 480px, -0.015em); guest headline 3.5rem (2.5rem at 480px, line-height 0.98, -0.02em). Surface-specific, not a token.
- **Display** (800, 2rem; 1.75rem at 1024px and below; 1.6rem at 480px; line-height 1; -0.01em): the card name in the name band, balanced wrapping. The guest trailer card prints its name at 1.5rem.
- **Headline** (800, 2rem; 1.65rem at 480px; -0.01em): full-width section headings (the shared section heading class), followed by a tabular count in Barlow 600 0.9rem ink-3. The Home's facing-page checklists step it down to 1.6rem.
- **Title** (700, 1.45rem, line-height 1.1): panel headings ("Your copy", About, Details).
- **Stat value** (Barlow Condensed 700, 1.2rem, tabular numerals): stat cells; the same face at 1.1rem prints rating values and review scores, at 1.6rem/800 the main card's Metacritic number, at 0.95rem/800 the small seal, at 0.85 to 0.95rem/700 set numbers, at 1.75rem/800 the Home greeting totals, at 1.3 to 1.4rem/800 ranks, and at 1.45rem/800 the day on date tiles.
- **Body** (400, 1rem, line-height 1.5): default text. **Prose** (line-height 1.65, max 68ch, ink-2) for the About description and review bodies; the guest lead runs 1.1rem at line-height 1.6, max 46ch.
- **Label** (600, 0.875rem, ink-3): definition-list terms, rating label. **Label small** (600, 0.75 to 0.8rem) for stat-cell terms, greeting total terms and row metadata. Labels are sentence case, never uppercase.
- **Button** (600, 0.95rem; 0.875rem in the small size). Tabs run 0.9rem/600, segments 0.85rem/600.

### Named Rules
**The Condensed Prints Facts Rule.** Barlow Condensed is reserved for card names, page titles, section and panel headings, and numbers (stats, scores, ratings, set numbers, ranks, dates, totals). Running text, labels, row names and controls stay in Barlow.

**The Tabular Numbers Rule.** Every number that can change or be compared (stats, scores, counts, ranks, percentages, totals, page numbers, character counter) uses tabular numerals.

## Layout

Both migrated surfaces sit in a centered shell, max 1240px wide.

**Game detail.** Shell padding 20px 24px 72px. A two-column grid: a 380px card column, sticky at 88px from the top, and a fluid working column (gap 28px). The working column stacks panels at 16px: "Your copy" first, then About, then Details. Below the grid, full-width sections (Media, Achievements, Reviews, DLC, series) are separated by 72px. Inside sections: media is a 2:1 split of a 16:9 viewer and a two-column thumb strip; achievements and DLC are auto-fill grids (min 230px and 260px, gap 10px); reviews are a 360px form beside the list (gap 28px); series mini cards are an auto-fill grid (min 200px, gap 16px). Detail rows use a 130px term column.

**Home.** Shell padding 28px 24px 88px. A greeting row (h1 left, totals right, wrapping) sits 28px above the open album: a two-page spread on a 7:5 column split with no gap, so the left page's right border is the spine. Both pages stretch to equal height. The left page holds the status tabs and a 3x2 pocket grid (gap 14px): owned mini cards first, then empty sleeves, then a final catalog pocket when the page is not full; at most six cards show, with a "Showing n of m" line linking to the profile. The right page stacks two checklists 28px apart. 72px below the spread, a lower grid on an 8:4 split (gap 28px) holds "Trending in Game Rank" (four ranked mini cards) and "Coming soon". The guest Home is a 1:1.15 grid of headline and trailer card (gap 48px), then "Your status is the frame" 64px below as a four-column row of mini cards.

Responsive steps:
- **1024px:** detail: card column narrows to 320px, gap 20px; reviews and media stack; thumb strip goes to four columns. Home: the spread and the lower grid stack; the pages separate (20px gap), each regains its full border and 18px radius, and the spread drops its shared lift; the lower area moves to 56px from the spread with 48px between sections.
- **860px:** detail: single column; the card loses sticky and centers at max 460px. Home: the guest grid stacks (gap 32px) and the status demo goes to two columns.
- **640px:** Home: pockets and trends go to two columns; the album page pads 16px; decorative empty sleeves hide and only the catalog pocket stays.
- **480px:** detail: shell padding 14px 14px 56px; panels pad 16px; sections 56px apart; detail rows stack; achievements and series go to two columns; "Your copy" actions stretch full width. Home: shell padding 18px 14px 64px; the facing page pads 18px 16px; the trend segments become a 2x2 grid at full width; tabs tighten. Mini cards everywhere: the name takes the full band on two lines and the Metacritic seal moves onto the art's top-right corner.

## Elevation & Depth

Hybrid and restrained. Flat faces on a tonal ground carry most depth, separated by 1px rules. Shadow is reserved for objects a player could pick up: cards, and the open album as one object.

### Shadow Vocabulary
- **Card lift** (`box-shadow: 0 1px 2px rgba(22, 20, 29, 0.06), 0 10px 28px rgba(22, 20, 29, 0.10)`; dark: `0 1px 2px rgba(0, 0, 0, 0.4), 0 12px 32px rgba(0, 0, 0, 0.45)`): the main card, mini cards, the guest trailer card, and the Home album spread as a whole (one shadow over both pages, never one per page; removed when the spread stacks at 1024px).
- **Art inset rule** (`box-shadow: inset 0 0 0 1px` rule): the edge of the main card's art box.
- **Seal on art** (`box-shadow: 0 1px 3px rgba(0, 0, 0, 0.3)`): the small Metacritic seal when it sits over mini card art at 480px and below.

### Named Rules
**The Only Cards Float Rule.** Panels, pages, tiles, chips, tabs and inputs are flat with a hairline border. Only card objects (main card, mini cards, trailer card) carry the lift shadow, plus the album spread as a single bound object.

## Shapes

Rounded rectangles nested from outside in, each radius smaller than its container: card frame 22px, card face 14px, art box 10px, stat cells 8px. Mini cards follow the same nesting (16px frame, 11px face, 7px art); the trailer card uses the main card's (22px frame, 14px face, 10px art). The album spread is 18px on its outer corners and square at the spine; stacked, each page is 18px all round. Panels, "Your copy" and the Coming soon list use 14px, tiles 12px, controls, the segmented track and textarea 10px, small cells, rows, date tiles and the main card seal 8px, the small seal and checklist thumbs 6px; chips, stamps, owned pills, status tabs and store links are full pills (999px), avatars and the trailer play toggle are circles. Borders are 1px hairlines by default; 2px marks state (the "Your copy" frame, the album page frame, uncommon rarity, active media thumb) and 3px is reserved for the rare holo frame. Dashed borders mean "empty": the empty state and the album's empty sleeves (sleeves mix 35% of the frame hue into rule-strong).

## Components

### Buttons
Solid and plain: ink or white, no gradients.
- **Shape:** gently rounded (10px), 42px tall; small size 34px with 12px side padding.
- **Primary:** ink fill, face text; the single "do it" action in a group (Add to favorites, Publish review, Create an account).
- **Ghost:** face fill, rule-strong border, ink text; every secondary action (Back, rating link, Read more, Load more, Cancel, Sign in, Browse the catalog, pager arrows).
- **Status button:** a ghost button whose border and text take the current status hue, with a trailing chevron; opens the status menu (160ms scale-from-0.96 fade, top-left origin).
- **Hover / Active:** hover only on fine pointers: primary to ink-2, ghost to ground fill with ink-3 border (150ms). Press scales to 0.97 (160ms ease-out). Disabled at reduced opacity.
- **Icon button:** 32px square, 8px radius, transparent, ink-3 glyph; hover fills ground and inks the glyph, destructive variant hovers to danger.
- **Text link:** ink text, 600, underlined in rule-strong at 3px offset; the underline takes the text color on hover. Optional trailing arrow ("Open profile").

### Chips
- **Fact chip:** 1px rule outline pill, 0.875rem Barlow 500; platform names.
- **Store chip:** 32px pill, rule-strong border, face fill, store icon plus external-link mark; hover fills ground.
- **Metacritic seal, card size:** stacked "MC" label over a condensed score (min 54px, 8px radius), colored by threshold; missing score shows an em dash on ground with a rule border. Main card only.
- **Metacritic seal, small:** one line, condensed 800 score (min 30px, 6px radius, 2px 6px padding) with a visually hidden "Metacritic" label; same colors and empty treatment. Mini cards, the trailer card band and checklist rows.
- **Status stamp:** pill in the frame color with on-frame text, in a card's set footer; shows the status icon and label. On the main card it reads "Favorite" in the neutral frame when no status is set; on mini cards it appears only with a status (0.72rem, 700).
- **Owned pill:** a smaller label-only stamp (0.7rem, 700) on checklist rows when the player owns that game.

### Cards / Containers
- **Panel:** face fill, 1px rule border, 14px radius, 20px 22px padding (16px on mobile). No shadow.
- **"Your copy" panel:** the detail's ownership panel. 2px border in the frame color and a 7% frame tint over the face; recolors with the frame (320ms ease-out).
- **Achievement tile:** face fill, 12px radius, 48px badge well beside name and percentage. Rarity is the tile's frame: common keeps the 1px rule, uncommon a 2px rarity-uncommon border, rare a 3px holo gradient border (rarity-rare through gold, violet and cyan) over a 6% rare tint. The foil goes on the frame, never over the badge.
- **DLC tile:** face fill, 1px rule, 12px radius, 72x42 thumb; hover darkens the border to ink-3.
- **Empty state:** dashed rule-strong border, 12 to 14px radius, face fill, centered icon and one sentence; on the album the icon takes the active status hue and a small ghost button follows.

### Inputs / Fields
- **Textarea:** face fill, 1px rule-strong border, 10px radius, 12px padding, min 110px, vertical resize; character counter below in tabular ink-3.
- **Focus:** border shifts to ink; keyboard focus adds the system ring.
- **Rating control:** five 34px star buttons, empty in rule-strong, filled in star; hover previews, press scales to 0.9; value printed in condensed type ("4/5" or "Not rated").
- **Focus ring (all controls):** 2px solid status-pending outline, 2px offset.

### Navigation
Both surfaces use the shared site header unchanged. On the detail, navigation is a small ghost Back button above the grid and an in-page link from "Your copy" to the reviews section. In-page view switches are WAI-ARIA tablists: arrow keys move and select, Home and End jump to the ends, only the selected tab is in the tab order, and focus follows selection.
- **Status tabs (Home album):** 38px pills with face fill and rule-strong border; each tab carries its own status hue on its icon, and hovering an unselected tab borders it in that hue. The selected tab fills with its hue and prints on-frame text; its count chip turns into a 20% on-frame wash. Counts sit in a ground-filled tabular chip. Colors move on 200ms ease-out.
- **Segmented control (Home trends):** a 1px rule, 10px track with 3px inset; 32px segments in ink-2 on a transparent fill, the selected one filled ink with face text; unselected hover fills ground. At 480px the track becomes a full-width 2x2 grid.

### The Card (signature component)
A frame (22px radius, 10px padding, card lift) around a white face (14px radius, 14px padding, 12px gap) holding, in order: the name band (display name left, Metacritic seal right); the 4:3 art box with cover crop and inset rule; the genre line (Barlow 600, 0.9rem, ink-2); three ruled stat cells (Community, Release, Platforms; columns 1fr 1.35fr 1fr, gap 6px); the set footer above a hairline (set number "No. {id}", "Data by RAWG" credit, status stamp pushed right). Frame, stamp and "Your copy" recolor together on status change (320ms ease-out). The skeleton keeps the same structure with a rule-colored frame.

**Holo sweep:** on a status change made by the player (never on initial load), a 105-degree band of cyan, violet and yellow at 80 to 90% alpha, screen-blended, crosses the art once from -110% to 110% over 900ms on the shared ease-in-out curve and fades in its last 20%. Removed entirely under `prefers-reduced-motion: reduce`.

**Trailer card (guest Home):** the same card grammar holding a video: neutral frame (22px, 10px padding, card lift), face (14px, 12px padding) with a name band (condensed 800, 1.5rem, small Metacritic seal), a 16:9 art box on black with a circular pause/play toggle, and a caption footer ("No. {id}" left, "Data by RAWG" right). Without a game it falls back to "Featured trailer".

### Mini Card
The shared small card (`components/CardWorld/MiniCard.vue`), used for detail series entries and every card on the Home. Frame (6px padding, 16px radius, card lift) around a face (11px radius, 10px padding, 8px gap): a fixed-height name band (condensed 800, 1.1rem, two-line clamp) with the small Metacritic seal, the 4:3 art (7px radius), and a set line ("No. {id}" left). When given the player's status, the frame takes the status hue and the set line ends in a status stamp; otherwise the frame is neutral and the set line ends in the release year (or "TBA"). Detail series cards are not given a status and stay neutral; Home cards are given the player's status wherever it is known. An optional favorite heart sits in the bottom-right corner (detail series only). Hover lifts the card 3px (200ms ease-out) on fine pointers; the frame recolors on 320ms ease-out. Without a game id it renders as a non-link with no set number (the guest demo). At 480px the name takes the whole band (0.95rem) and the seal moves onto the art's top-right corner.

### Album Page and Pockets (Home)
The left page of the open album is a tinted ownership surface: 2px border and 7% tint in the active status tab's hue (320ms ease-out recolor), 22px padding, 18px radius on the outer corners. Its pocket grid is a binder page of 3x2 sleeves: mini cards, then empty sleeves (dashed, 16px radius, half-transparent face, min 250px tall), then a catalog pocket whose plus icon takes the status hue ("Find your next game"; hover fills face). Loading shows six 16px-radius skeleton pockets. The facing page is a flat face panel (1px rule, no left border at the spine, 18px outer radius, 22px 24px padding), matching the album's height.

### Checklist Row (Home)
A numbered hairline list, like a card set checklist: rows divided by 1px rules, each a link with a condensed ink-3 rank (1.4rem), a 64x48 thumb (6px radius, ground well), the name (Barlow 600, 0.95rem, single-line ellipsis) over a metadata line ("No. {id}" in condensed ink-2, release date, owned pill), and a right-aligned value: RAWG player rating with a star in "Top rated", the small Metacritic seal in "New this month". Rows inherit the player's status frame so the owned pill takes its hue. Hover fills ground (8px radius). The "Top rated" heading carries the source line "Player ratings on RAWG".

### Coming Soon List (Home)
A hairline panel (face fill, 1px rule, 14px radius) of rows split by rules: a 52px ground date tile (month label, condensed day, year only when not the current year), the name on up to two lines, and a chevron. Hover fills ground. A pager below holds two small ghost arrow buttons around a tabular "Page n of m".

## Do's and Don'ts

### Do:
- **Do** keep the card frame as the only large color on a card, and tie it to collection status: neutral until the game has a status, then exactly one status hue.
- **Do** give a surface a status tint (7%) and 2px status frame only when it holds the player's own copies, as "Your copy" and the Home album page do.
- **Do** pass the player's status to every mini card where it is known; leave the frame neutral where it is not.
- **Do** recolor frame, stamp and ownership surfaces together on the same 320ms ease-out transition.
- **Do** join a new view to the world with the `card-world` root class and reuse the shared frame, heading, count and seal classes and the mini card component instead of copying them.
- **Do** print names, headings and numbers in Barlow Condensed and keep labels and prose in Barlow, sentence case.
- **Do** use tabular numerals for every stat, score, count, rank and percentage.
- **Do** nest radii from outside in (22, 14, 10, 8) and separate flat surfaces with 1px rules.
- **Do** reserve the lift shadow for card objects and the album spread as one object.
- **Do** keep the RAWG credit printed on the card face, and label RAWG-sourced figures as such ("Player ratings on RAWG").
- **Do** build in-page view switches as WAI-ARIA tablists with arrow-key, Home and End navigation.
- **Do** remove the holo sweep under reduced motion and keep every other transition to opacity and color there.
- **Do** define both themes for every new token; dark lifts status hues and flips on-frame text to the dark ground.

### Don't:
- **Don't** add a second signature motion; the holo sweep is the only one, and it runs only on a player-made status change.
- **Don't** add a large color field that is not the player's status, or tint panels that do not hold the player's own copies.
- **Don't** lay holographic foil over achievement badges or card art at rest; foil lives on the rare tile's frame and in the one-time sweep.
- **Don't** open a game page with a blurred-cover banner, a floating score badge and tabs; the card is the hero.
- **Don't** use uppercase tracked labels; labels are sentence case.
- **Don't** apply shadows to panels, pages, tiles, chips, tabs or inputs, or give each album page its own shadow.

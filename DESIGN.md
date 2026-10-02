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
    lineHeight: 1.1
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
  mini-card: "16px"
  panel: "14px"
  tile: "12px"
  control: "10px"
  cell: "8px"
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
---

# Design System: Game Rank

> **Scope.** This system was built and reviewed on one pilot surface: the game detail route (`/game/:id`, `frontend/src/components/GameDetail/`). The other eight views (Home, Login, Register, Terms, catalog, profile, trends, admin users, admin comments) still run the previous system (Sora type, neumorphic header and footer, the `:root` tokens in `frontend/src/style.css`). That is scope, not drift: those views migrate to this system later. Until then, the tokens below live as `--gd-*` custom properties scoped to `.game-detail-page` (light) and `[data-theme="dark"] .game-detail-page` (dark) in `styles_GameDetail.css`; only the motion curves are global (`:root` in `style.css`).

## Overview

**Creative North Star: "The Collectible Card"**

Every game is a trading card. RAWG prints the facts on the card face (name, art, genres, release, platforms, Metacritic, set number); the player's collection status colors the frame and their rating and review sit beside it. The world is a cool card-stock ground, white card faces and near-black ink, with one thick rounded frame as the only large field of color. That frame is neutral ink while the game is not in the player's collection and takes one solid status hue when it is.

Density is moderate and editorial: a sticky card column next to a working column of panels, then full-width sections separated by generous vertical space. Surfaces are flat white faces on a pale ground, held apart by hairline rules rather than shadows; only card objects (the main card and series mini cards) are lifted. Motion is quiet everywhere except one signature: when the player changes status, a holographic band sweeps once across the card art.

The world rejects the category default of a blurred-cover banner with a score badge and tabs. Facts are framed as card stats, not as a hero banner.

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
- **Collection Status Frame** (frame-neutral when not owned; status-pending, status-playing, status-paused, status-completed when owned): the card frame, the status stamp, the "Your copy" panel border and its 7% tint (`color-mix(in srgb, frame 7%, face)`), and the status button outline and text. Pending is a clear blue, Playing a deep green, Paused a burnt amber, Completed a violet. In dark theme every hue is lifted to a lighter tint and the text on a status frame flips to the dark ground (on-frame-dark); the neutral frame keeps light text (`--gd-on-frame-neutral`, #F1F0F6 in dark) so the "Favorite" stamp holds AA contrast (7.95:1).

### Secondary
- **Metacritic Seal** (metacritic-high, metacritic-mid, metacritic-low; metacritic-none for missing scores): the score chip in the card's name band and on mini cards. Thresholds: 80 and above high, 50 to 79 mid, below 50 low. White text on all three; the same values in both themes.
- **Star Gold** (star): filled rating stars in the rating control, the Community stat and review ratings. Empty stars use rule-strong.

### Tertiary
- **Rarity Inks** (rarity-rare, rarity-uncommon, rarity-common): achievement rarity. Rare (under 10% of players) owns the holo frame and a burnt-amber star; uncommon (under 40%) a blue frame and rotated square; common a grey dot and the default hairline. Uncommon shares the Pending blue value; it is a shared value, not a shared meaning.

### Neutral
- **Card Stock** (ground): the page ground, empty art boxes, avatar and thumb wells, ghost hover fill.
- **Card Face** (face): panels, card faces, tiles, inputs, ghost buttons.
- **Ink** (ink): headings, names, primary button fill, active thumb outline, text selection fill.
- **Ink 2** (ink-2): prose, genre line, set number, primary button hover.
- **Ink 3** (ink-3): labels, metadata, counts, hints, placeholders, icon buttons at rest.
- **Rule** (rule): hairline borders on panels, stat cells, tiles, detail rows, review dividers.
- **Strong Rule** (rule-strong): control borders (ghost buttons, textarea, store chips), empty stars, dashed empty state.
- **Danger** (danger): destructive icon-button hover and the error icon; same value as metacritic-low.

### Named Rules
**The One Frame Rule.** The card frame is the only large field of color on the surface. Every other colored element (Metacritic seal, stamp, stars, rarity marks) is small. A new surface does not add a second large color.

**The Frame Means Ownership Rule.** The frame stays neutral until the game is in the player's collection with a status; only then does it take the status hue, and the "Your copy" panel takes the same hue with it. Status hue never decorates anything unrelated to the player's copy except the focus ring, which uses the Pending blue as the system focus color.

## Typography

**Display Font:** Barlow Condensed 700/800 (with Barlow, sans-serif)
**Body Font:** Barlow 400/500/600/700 (with system-ui, sans-serif)

Both are self-hosted through `@fontsource` and imported by the game detail component. Inside `.game-detail-page`, every element except PrimeIcons inherits Barlow, overriding the legacy global Sora rule.

**Character:** A sports-card pairing: the condensed face prints names and numbers with the punch of a card's name band and stat line, while regular Barlow keeps prose, labels and controls quiet and legible.

### Hierarchy
- **Display** (800, 2rem; 1.75rem at 1024px and below; 1.6rem at 480px; line-height 1; -0.01em): the card name in the name band, balanced wrapping.
- **Headline** (800, 2rem; 1.65rem at 480px; line-height 1.1; -0.01em): full-width section headings (Media, Achievements, Reviews, DLC, series), followed by a tabular count in Barlow 600 0.9rem ink-3.
- **Title** (700, 1.45rem, line-height 1.1): panel headings ("Your copy", About, Details).
- **Stat value** (Barlow Condensed 700, 1.2rem, tabular numerals): stat cells; the same face at 1.1rem prints rating values and review scores, at 1.6rem/800 the Metacritic number, and at 0.95rem/700 the set number.
- **Body** (400, 1rem, line-height 1.5): default text. **Prose** (line-height 1.65, max 68ch, ink-2) for the About description and review bodies.
- **Label** (600, 0.875rem, ink-3): definition-list terms, rating label. **Label small** (600, 0.75rem) for stat-cell terms. Labels are sentence case, never uppercase.
- **Button** (600, 0.95rem; 0.875rem in the small size).

### Named Rules
**The Condensed Prints Facts Rule.** Barlow Condensed is reserved for card names, section and panel headings, and numbers (stats, scores, ratings, set numbers). Running text, labels and controls stay in Barlow.

**The Tabular Numbers Rule.** Every number that can change or be compared (stats, scores, counts, percentages, character counter) uses tabular numerals.

## Layout

A centered shell (max 1240px; padding 20px 24px 72px) holds a two-column grid: a 380px card column, sticky at 88px from the top, and a fluid working column (gap 28px). The working column stacks panels at 16px: "Your copy" first, then About, then Details. Below the grid, full-width sections (Media, Achievements, Reviews, DLC, series) are separated by 72px.

Inside sections: media is a 2:1 split of a 16:9 viewer and a two-column thumb strip; achievements and DLC are auto-fill grids (min 230px and 260px, gap 10px); reviews are a 360px form beside the list (gap 28px); series mini cards are an auto-fill grid (min 200px, gap 16px). Detail rows use a 130px term column.

Responsive steps:
- **1024px:** card column narrows to 320px, gap 20px; reviews and media stack; thumb strip goes to four columns.
- **860px:** single column; the card loses sticky and centers at max 460px.
- **480px:** shell padding 14px 14px 56px; panels pad 16px; sections 56px apart; detail rows stack; achievements and series go to two columns; "Your copy" actions stretch full width; on mini cards the Metacritic seal moves to the corner of the art.

## Elevation & Depth

Hybrid and restrained. Flat faces on a tonal ground carry most depth, separated by 1px rules. Shadow is reserved for card objects, the things a player could pick up.

### Shadow Vocabulary
- **Card lift** (`box-shadow: 0 1px 2px rgba(22, 20, 29, 0.06), 0 10px 28px rgba(22, 20, 29, 0.10)`; dark: `0 1px 2px rgba(0, 0, 0, 0.4), 0 12px 32px rgba(0, 0, 0, 0.45)`): the main card and series mini cards only.
- **Art inset rule** (`box-shadow: inset 0 0 0 1px` rule): the edge of the card's art box.

### Named Rules
**The Only Cards Float Rule.** Panels, tiles, chips and inputs are flat with a hairline border. Only card objects (main card, mini cards) carry the lift shadow.

## Shapes

Rounded rectangles nested from outside in, each radius smaller than its container: card frame 22px, card face 14px, art box 10px, stat cells 8px. Mini cards follow the same nesting (16px frame, 11px face, 7px art). Panels and "Your copy" use 14px, tiles 12px, controls and textarea 10px, small cells and seals 8px, chips, stamps and store links are full pills (999px), avatars are circles. Borders are 1px hairlines by default; 2px marks state (the "Your copy" frame, uncommon rarity, active media thumb) and 3px is reserved for the rare holo frame. The empty state is the one dashed border.

## Components

### Buttons
Solid and plain: ink or white, no gradients.
- **Shape:** gently rounded (10px), 42px tall; small size 34px with 12px side padding.
- **Primary:** ink fill, face text; the single "do it" action in a group (Add to favorites, Publish review).
- **Ghost:** face fill, rule-strong border, ink text; every secondary action (Back, rating link, Read more, Load more, Cancel).
- **Status button:** a ghost button whose border and text take the current status hue, with a trailing chevron; opens the status menu (160ms scale-from-0.96 fade, top-left origin).
- **Hover / Active:** hover only on fine pointers: primary to ink-2, ghost to ground fill with ink-3 border (150ms). Press scales to 0.97 (160ms ease-out). Disabled at 55% opacity.
- **Icon button:** 32px square, 8px radius, transparent, ink-3 glyph; hover fills ground and inks the glyph, destructive variant hovers to danger.

### Chips
- **Fact chip:** 1px rule outline pill, 0.875rem Barlow 500; platform names.
- **Store chip:** 32px pill, rule-strong border, face fill, store icon plus external-link mark; hover fills ground.
- **Metacritic seal:** stacked "MC" label over a condensed score, colored by threshold; missing score shows an em dash on ground with a rule border.
- **Status stamp:** pill in the frame color with on-frame text, in the card's set footer; shows the status icon and label, or "Favorite" when no status is set.

### Cards / Containers
- **Panel:** face fill, 1px rule border, 14px radius, 20px 22px padding (16px on mobile). No shadow.
- **"Your copy" panel:** the ownership panel. 2px border in the frame color and a 7% frame tint over the face; recolors with the frame (320ms ease-out).
- **Achievement tile:** face fill, 12px radius, 48px badge well beside name and percentage. Rarity is the tile's frame: common keeps the 1px rule, uncommon a 2px rarity-uncommon border, rare a 3px holo gradient border (rarity-rare through gold, violet and cyan) over a 6% rare tint. The foil goes on the frame, never over the badge.
- **DLC tile:** face fill, 1px rule, 12px radius, 72x42 thumb; hover darkens the border to ink-3.
- **Empty state:** dashed rule-strong border, 12px radius, centered icon and one sentence.

### Inputs / Fields
- **Textarea:** face fill, 1px rule-strong border, 10px radius, 12px padding, min 110px, vertical resize; character counter below in tabular ink-3.
- **Focus:** border shifts to ink; keyboard focus adds the system ring.
- **Rating control:** five 34px star buttons, empty in rule-strong, filled in star; hover previews, press scales to 0.9; value printed in condensed type ("4/5" or "Not rated").
- **Focus ring (all controls):** 2px solid status-pending outline, 2px offset.

### Navigation
The pilot surface uses the shared site header unchanged; within the page, navigation is a small ghost Back button above the grid and an in-page link from "Your copy" to the reviews section.

### The Card (signature component)
A frame (22px radius, 10px padding, card lift) around a white face (14px radius, 14px padding, 12px gap) holding, in order: the name band (display name left, Metacritic seal right); the 4:3 art box with cover crop and inset rule; the genre line (Barlow 600, 0.9rem, ink-2); three ruled stat cells (Community, Release, Platforms; columns 1fr 1.35fr 1fr, gap 6px); the set footer above a hairline (set number "No. {id}", "Data by RAWG" credit, status stamp pushed right). Frame, stamp and "Your copy" recolor together on status change (320ms ease-out). The skeleton keeps the same structure with a rule-colored frame.

**Holo sweep:** on a status change made by the player (never on initial load), a 105-degree band of cyan, violet and yellow at 80 to 90% alpha, screen-blended, crosses the art once from -110% to 110% over 900ms on the shared ease-in-out curve and fades in its last 20%. Removed entirely under `prefers-reduced-motion: reduce`.

### Mini Card
Series entries are smaller copies of the card: neutral frame (6px padding, 16px radius, card lift), face with a two-line condensed name and small Metacritic seal, 4:3 art, and a set line (set number, release year). A favorite heart sits in the bottom-right corner. Hover lifts the card 3px (200ms ease-out) on fine pointers. Mini card frames stay neutral; they do not show the player's status.

## Do's and Don'ts

### Do:
- **Do** keep the card frame as the only large color, and tie it to collection status: neutral until the game has a status, then exactly one status hue.
- **Do** recolor frame, stamp and "Your copy" together on the same 320ms ease-out transition.
- **Do** print names, headings and numbers in Barlow Condensed and keep labels and prose in Barlow, sentence case.
- **Do** use tabular numerals for every stat, score, count and percentage.
- **Do** nest radii from outside in (22, 14, 10, 8) and separate flat surfaces with 1px rules.
- **Do** reserve the lift shadow for card objects.
- **Do** keep the RAWG credit printed on the card face.
- **Do** remove the holo sweep under reduced motion and keep every other transition to opacity and color there.
- **Do** define both themes for every new token; dark lifts status hues and flips on-frame text to the dark ground.

### Don't:
- **Don't** add a second signature motion; the holo sweep is the only one, and it runs only on a player-made status change.
- **Don't** add a second large color field or tint panels other than "Your copy".
- **Don't** lay holographic foil over achievement badges or card art at rest; foil lives on the rare tile's frame and in the one-time sweep.
- **Don't** open a game page with a blurred-cover banner, a floating score badge and tabs; the card is the hero.
- **Don't** use uppercase tracked labels; labels are sentence case.
- **Don't** apply shadows to panels, tiles, chips or inputs.

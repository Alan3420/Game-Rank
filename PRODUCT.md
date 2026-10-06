# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

Academic project. Two audiences:

- **Players** (primary end user): people who play video games and use Game Rank with equal weight for three jobs: organizing their personal collection (backlog by status), deciding what to play next (catalog, filters, trends, community reviews), and publishing their own ratings and reviews.
- **Evaluators**: the academic reviewers who judge the project. They assess completeness, coherence between documentation and implementation, accessibility, and technical quality.
- **Admins**: moderators who manage user accounts and moderate comments.

## Product Purpose

A web platform to discover, rate and organize video games. Game data comes entirely from the RAWG API; Game Rank adds the personal and community layer on top: favorites, per-game play status, ratings and comments, plus admin moderation. Success means a player can find a game, decide whether it is worth playing, track it through their collection, and share an opinion, all within one consistent product.

## Positioning

Not confirmed. The product combines catalog discovery, personal backlog tracking and community reviews in one place; no claim of a unique mechanism over neighboring products (RAWG, Backloggd, similar trackers) has been made. Do not invent one.

## Operating Context

- Public routes: Home (`/`), Login, Register, Terms (`/terminos`). Everything else requires a session; unauthenticated visitors are redirected to `/login`.
- Authenticated routes: catalog with filters (`/content/overview`), game detail (`/game/:id`), profile with collection (`/profile`, `/user/profile`), trends (`/tendencias`).
- Admin routes: user management (`/admin/users`), comment moderation (`/admin/comments`). Non-admins receive a 404 instead of a 403 to hide their existence.
- Deployed at https://gamerk.netlify.app/ (frontend); backend Flask + MySQL, also packaged with Docker Compose.

## Capabilities and Constraints

- **Stack:** Vue 3 + Vite + Vue Router + PrimeVue/PrimeIcons + Axios + DOMPurify (frontend); Flask + SQLAlchemy + JWT + MySQL (backend).
- **Game data is external.** There is no video game entity or table. Owned tables (`favorites`, `comments`) store only `id_game_api` as a reference attribute to RAWG. All titles, covers, genres, platforms, dates and Metacritic scores come from RAWG at request time.
- **RAWG limits:** pagination is capped at 500 pages regardless of the reported count; images may be missing or invalid (a placeholder exists).
- **Collection statuses:** `pendiente`, `jugando`, `pausado`, `completado` (stored in Spanish), shown as Pending, Playing, Paused, Completed.
- **Comments:** text description (max 255 chars) plus an integer rating; editable (tracks update date); moderated by admins.
- **Roles:** `user` and `admin`. The seed data has no admin account.
- **Community trends:** four rankings of up to 8 games (most collected, top rated, most reviewed, most favorited). Top rated requires at least 3 reviews (`MIN_RESENAS_VALORADOS`); ties share a place and are ordered deterministically.

## Brand Commitments

- **Name:** Game Rank. Logo "Card G" (single-ink letter-symbol and Barlow Condensed wordmark) in `frontend/src/assets/brand/`; favicon set in `frontend/public/`.
- **Design system:** the visual identity is the "collectible card" world, documented in `DESIGN.md` (tokens in `frontend/src/styles/card-world.css`). `DESIGN.md` and the code are the source of truth; `Game-Rank-Guia-Estilos.pdf` is regenerated from them and must not diverge. The previous identity (indigo, Sora, neumorphic shell) is retired.
- **UI language:** English only, across every view, label, message and ARIA string, even though documentation, code comments and stored values are in Spanish.
- **RAWG attribution is mandatory** wherever RAWG data is presented as a product surface; it currently lives in the footer (`App.vue`) and in Terms section 06.

## Evidence on Hand

- Real game data via RAWG (covers, Metacritic scores, release dates, background video on Home).
- Seed data for local testing (`flask --app app.main db-seed`).
- 48 backend unit tests covering comments, favorites and users.
- Terms and Conditions page with content attribution.
- No testimonials, user counts, press, or usage metrics exist. Do not fabricate them.

## Product Principles

1. **RAWG supplies the facts, Game Rank supplies the player.** Never present external game data as owned; the value added is personal status, ratings and community voice.
2. **Discovery, tracking and opinion are equal citizens.** No surface should bury one job to promote another.
3. **Documentation and implementation must agree.** The style guide, README and code describe the same product; divergences are defects, since evaluators judge the coherence.
4. **Accessible by requirement, not by afterthought.** Every new or changed surface ships meeting the accessibility standard below.

## Accessibility & Inclusion

WCAG 2.1 AA is a required standard for all surfaces, in both light and dark themes.

# Telegrinder docs website

A static site for the Markdown in [`../docs`](../docs). The docs folder stays the single source of truth:
the site reads it at build time, nothing is copied.

The look is built on the logo's pixel grid: one 20 px cell is the unit of the page, headings and labels use
the Tiny5 pixel face, and the glass renders of the logo and icons morph into their pixel grids and back.

## Run

Requires Node 22.12 or newer.

```sh
cd website
npm install
npm run dev      # http://localhost:4321
npm run build    # static output in website/dist
npm run check    # types and templates
```

| Variable | Default | Purpose |
| --- | --- | --- |
| `SITE_URL` | `https://telegrinder.rtfd.io` | Canonical URLs |
| `BASE_PATH` | `/` | Serve from a sub-path, for example `/telegrinder/` on GitHub Pages |
| `TELEGRINDER_DOCS_DIR` | `../docs` | Where the Markdown lives |

## What gets built

- `/` and `/ru/`: home with the README example running in the demo chat.
- `/tutorial/<chapter>/` and `/ru/tutorial/<chapter>/`: every file in `docs/tutorial/<lang>/`.
- `/tools/…`, `/api/`, `/changelog/…`, `/community/`: English content, available under both UIs.

Links between Markdown files (`2_rules.md`, `/docs/community_links.md`) become site routes. Links to anything
else in the repository (for example `examples/…`) point to GitHub. GitHub alerts (`> [!TIP]`) are supported.

## Demo chat scenes

When a code block reaches the middle of the screen, the chat next to it plays what that code does.
Scenes live in `src/scenes/en.ts` and `src/scenes/ru.ts`, keyed by page and by the zero-based index of the
fenced block in the chapter:

```ts
"tutorial/2_rules": {
  3: [{ u: "ping" }, { b: "Pong" }, { u: "pong" }, { sys: 'Text("ping") did not match' }],
},
```

Step kinds: `u` user message, `b` bot message (`inline` buttons, `reply` quote, `html`), `sys` dispatcher note,
`kb` reply keyboard, `press`, `toast`, `edit`, `relabel`, `del`, `sticker`, `photo`, `album`.
Replies must match what the chapter's code returns. If a chapter gains or loses a code block, check the indices.

## Glass and pixels

- `src/render/icons.json`: 16×16 pixel icons, `#` for ink or frosted glass, `+` for accent or blue glass.
- `design/icons.py` and `design/grinder.py`: Blender (Cycles) scripts for the glass renders in `public/img`.

```sh
blender -b -P design/icons.py -- /tmp/icons            # every icon, 640×640 PNG
blender -b -P design/icons.py -- /tmp/icons rules      # one icon
blender -b -P design/grinder.py -- /tmp/mark.png --frost --size 1600
```

Convert the PNGs to 320×320 WebP into `public/img/icons/`. Every icon uses the same camera, so the grid
always covers the central 80 % of the frame; the morph in `src/scripts/glass-pixel.ts` relies on that.

## Themes

Auto, light, dark and 1-bit. 1-bit collapses every grey to black or white and shows pixels only.
The choice is stored in `localStorage` and applied before first paint.

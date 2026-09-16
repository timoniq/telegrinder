// The Telegrinder mark on its native 37×28 grid, read from docs/assets/logo-black.png (20 px cells).
export const GRID = [
  ".........#############...............",
  ".........#############...............",
  "...........#########.................",
  ".............#####...................",
  ".............#####...................",
  ".............#####............#.#.#.#",
  ".............#####....####....#.#.#.#",
  "........##################...#..#.#.#",
  "......####################..#..#..#.#",
  "...##.####################....#..#..#",
  "...#######################..##..#..#.",
  ".#########################.....#..#..",
  ".#########################..###..#...",
  ".#########################......#....",
  "...####.##################..####.....",
  "...####.##################...........",
  "...####......#####....####...........",
  "....#####....#####...................",
  ".....####....#####...................",
  "......###....#####...................",
  "......###....#####...................",
  "....#####....#####...................",
  "#########....#####...................",
  "#########....#####...................",
  "....#####.##.#####.##................",
  "..........###########................",
  "........###############..............",
  "........###############..............",
];

/** First column of the minced output strands on the right. */
export const STRAND_COL = 26;

export const STRANDS = GRID.slice(5, 15).map((row) => row.slice(STRAND_COL));

/** Merges horizontal runs of filled cells into rects. */
export function runs(rows: string[], cell = 1, ox = 0, oy = 0): string {
  let out = "";
  rows.forEach((row, y) => {
    for (const m of row.matchAll(/#+/g)) {
      out += `<rect x="${ox + (m.index ?? 0) * cell}" y="${oy + y * cell}" width="${m[0].length * cell}" height="${cell}"/>`;
    }
  });
  return out;
}

export const markSvg = (cls = "px-mark") =>
  `<svg class="${cls}" viewBox="0 0 37 28" fill="currentColor" shape-rendering="crispEdges" aria-hidden="true">${runs(GRID)}</svg>`;

const svgUrl = (w: number, h: number, body: string) =>
  `url("data:image/svg+xml,${encodeURIComponent(`<svg xmlns="http://www.w3.org/2000/svg" width="${w}" height="${h}" viewBox="0 0 ${w} ${h}" shape-rendering="crispEdges">${body}</svg>`)}")`;

/** Mask images used from CSS; colour always comes from theme tokens. */
export const MASKS = {
  strands: svgUrl(84, 84, runs(STRANDS, 2, 8, 10) + runs(STRANDS, 2, 52, 52)),
  rule: svgUrl(120, 20, runs(STRANDS, 2, 5, 0) + runs(STRANDS, 2, 49, 0) + runs(STRANDS, 2, 93, 0)),
};

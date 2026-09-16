// Markup for "glass ↔ pixel" objects: a crisp SVG pixel icon, its Cycles-rendered glass twin
// and a canvas the browser uses to morph between them (src/scripts/glass-pixel.ts).
// Server-only: it resolves asset URLs against the site base.
import { withBase } from "../docs/content";
import icons from "./icons.json";
import { GRID, STRAND_COL } from "./pixel";

export type IconName = Exclude<keyof typeof icons, "_">;
export type Trigger = "hover" | "arrive" | "scroll" | "none";

const ICONS = icons as unknown as Record<IconName, string[]>;

const PAGE_ICON: Record<string, IconName> = {
  "tutorial/index": "setting_up",
  "tutorial/1_setting_up": "setting_up",
  "tutorial/2_rules": "rules",
  "tutorial/3_functional_bits": "functional_bits",
  "tutorial/4_api": "api",
  "tutorial/5_nodes": "nodes",
  "tutorial/6_dispatch": "dispatch",
  "tutorial/7_keyboard": "keyboard",
  "tutorial/8_text": "text",
  "tutorial/9_states": "states",
  "tutorial/10_media": "media",
  "tutorial/11_handling_errors": "errors",
  "tutorial/12_out-of-box_scenarios": "scenarios",
  "tools/index": "formatting",
  "tools/checkbox": "checkbox",
  "tools/formatting": "formatting",
  "tools/loop_wrapper": "loop_wrapper",
  "tools/global_context": "global_context",
  "reference/api": "reference_api",
  "reference/community": "community",
};

export function iconFor(key: string): IconName {
  if (key.startsWith("changelog/")) return "changelog";
  return PAGE_ICON[key] ?? "scenarios";
}

function rects(grid: string[], symbol: "#" | "+"): string {
  let out = "";
  grid.forEach((row, y) => {
    for (const m of row.matchAll(symbol === "#" ? /#+/g : /\++/g)) {
      out += `<rect x="${m.index}" y="${y}" width="${m[0].length}" height="1"/>`;
    }
  });
  return out;
}

const pixelSvg = (grid: string[], cls: string) =>
  `<svg class="${cls}" viewBox="0 0 ${grid[0].length} ${grid.length}" preserveAspectRatio="none" shape-rendering="crispEdges" aria-hidden="true"><g class="px-ink">${rects(grid, "#")}</g><g class="px-acc">${rects(grid, "+")}</g></svg>`;

/** A pixel-only icon, for places too small for glass (16 px = one CSS pixel per cell). */
export const pixelIcon = (name: IconName, cls = "px-icon") => pixelSvg(ICONS[name], cls);

interface Shell {
  grid: string[];
  /** Where the pixel grid sits inside the glass render, as fractions: x y w h. */
  box: [number, number, number, number];
  src: string;
  ratio: string;
  width: string;
  trigger: Trigger;
  rest: "pixel" | "glass";
  cls?: string;
  frames?: string[];
}

function shell(o: Shell): string {
  const [x, y, w, h] = o.box;
  const frames = o.frames ? ` data-frames="${o.frames.join(" ")}"` : "";
  const style = `--gp-width:${o.width};--gp-ratio:${o.ratio};--gp-x:${x * 100}%;--gp-y:${y * 100}%;--gp-w:${w * 100}%;--gp-h:${h * 100}%`;
  return `<span class="gp${o.cls ? ` ${o.cls}` : ""}" data-gp data-grid="${o.grid.join("|")}" data-box="${o.box.join(" ")}" data-trigger="${o.trigger}" data-rest="${o.rest}" data-view="${o.rest}"${frames} style="${style}" aria-hidden="true">${pixelSvg(o.grid, "gp-pixel")}<img class="gp-glass" src="${o.src}" alt="" loading="lazy" decoding="async" draggable="false"><canvas class="gp-canvas"></canvas></span>`;
}

export function glassIcon(name: IconName, width: string, trigger: Trigger = "hover", rest: "pixel" | "glass" = "pixel", cls?: string): string {
  return shell({ grid: ICONS[name], box: [0.1, 0.1, 0.8, 0.8], src: withBase(`img/icons/${name}.webp`), ratio: "1", width, trigger, rest, cls });
}

/** The logo; the strands to the right of the grinder are accent cells. */
export function glassMark(width: string, trigger: Trigger, rest: "pixel" | "glass", cls?: string, turn = false): string {
  const grid = GRID.map((row) => row.slice(0, STRAND_COL) + row.slice(STRAND_COL).replace(/#/g, "+"));
  const frames = turn ? Array.from({ length: 13 }, (_, i) => withBase(`img/turn${String(i).padStart(2, "0")}.webp`)) : undefined;
  return shell({
    grid, box: [0.063, 0.052, 0.895, 0.886], src: withBase("img/mark.webp"), ratio: "596 / 466", width, trigger, rest, cls, frames,
  });
}

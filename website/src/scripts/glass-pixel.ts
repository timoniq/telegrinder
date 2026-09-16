// Morphs between a Cycles glass render and its pixel grid.
// glass → mosaic → cells sampled from the render → Bayer-dithered swap to theme colours → crisp pixels.
import { reducedMotion } from "./env";

type View = "pixel" | "glass";

interface Item {
  el: HTMLElement;
  img: HTMLImageElement;
  canvas: HTMLCanvasElement;
  grid: string[];
  box: number[];
  view: View;
  run: number;
  frames: string[];
  frame: number;
}

const BAYER = [0, 8, 2, 10, 12, 4, 14, 6, 3, 11, 1, 9, 15, 7, 13, 5];
const FRAME_MS = 52;
const items = new WeakMap<HTMLElement, Item>();

const onebit = () => document.documentElement.hasAttribute("data-onebit");
const tokens = () => {
  const cs = getComputedStyle(document.documentElement);
  return { ink: cs.getPropertyValue("--ink").trim(), accent: cs.getPropertyValue("--accent").trim() };
};

async function loaded(img: HTMLImageElement) {
  if (img.complete && img.naturalWidth) return true;
  img.loading = "eager";
  try {
    await img.decode();
    return true;
  } catch {
    return false;
  }
}

function item(el: HTMLElement): Item {
  let it = items.get(el);
  if (!it) {
    it = {
      el,
      img: el.querySelector(".gp-glass") as HTMLImageElement,
      canvas: el.querySelector(".gp-canvas") as HTMLCanvasElement,
      grid: (el.dataset.grid ?? "").split("|"),
      box: (el.dataset.box ?? "0 0 1 1").split(" ").map(Number),
      view: (el.dataset.view as View) ?? "pixel",
      run: 0,
      frames: (el.dataset.frames ?? "").split(" ").filter(Boolean),
      frame: 6,
    };
    items.set(el, it);
  }
  return it;
}

function painter(it: Item) {
  const { canvas, img, grid, box } = it;
  const rect = it.el.getBoundingClientRect();
  const dpr = Math.min(2, window.devicePixelRatio || 1);
  const W = (canvas.width = Math.max(1, Math.round(rect.width * dpr)));
  const H = (canvas.height = Math.max(1, Math.round(rect.height * dpr)));
  const ctx = canvas.getContext("2d")!;
  const cols = grid[0].length;
  const rows = grid.length;
  const gx = box[0] * W, gy = box[1] * H, cw = (box[2] * W) / cols, ch = (box[3] * H) / rows;
  const { ink, accent } = tokens();

  // Average colour of the render under every grid cell.
  const probe = document.createElement("canvas");
  probe.width = cols;
  probe.height = rows;
  const pctx = probe.getContext("2d", { willReadFrequently: true })!;
  pctx.drawImage(img, box[0] * img.naturalWidth, box[1] * img.naturalHeight, box[2] * img.naturalWidth, box[3] * img.naturalHeight, 0, 0, cols, rows);
  const sampled = pctx.getImageData(0, 0, cols, rows).data;

  const small = document.createElement("canvas");
  const sctx = small.getContext("2d")!;

  const cell = (x: number, y: number) => [Math.round(gx + x * cw), Math.round(gy + y * ch), Math.round(gx + (x + 1) * cw) - Math.round(gx + x * cw), Math.round(gy + (y + 1) * ch) - Math.round(gy + y * ch)] as const;

  return {
    glass() {
      ctx.clearRect(0, 0, W, H);
      ctx.imageSmoothingEnabled = true;
      ctx.drawImage(img, 0, 0, W, H);
    },
    mosaic(block: number) {
      const sw = Math.max(1, Math.round(W / block)), sh = Math.max(1, Math.round(H / block));
      small.width = sw;
      small.height = sh;
      sctx.imageSmoothingEnabled = true;
      sctx.drawImage(img, 0, 0, sw, sh);
      ctx.clearRect(0, 0, W, H);
      ctx.imageSmoothingEnabled = false;
      ctx.drawImage(small, 0, 0, sw, sh, 0, 0, W, H);
    },
    cells(level: number) {
      ctx.clearRect(0, 0, W, H);
      for (let y = 0; y < rows; y++) {
        for (let x = 0; x < cols; x++) {
          const target = grid[y][x];
          const settled = BAYER[(y % 4) * 4 + (x % 4)] < level;
          const [px, py, pw, ph] = cell(x, y);
          if (settled) {
            if (target === ".") continue;
            ctx.fillStyle = target === "+" ? accent : ink;
          } else {
            const k = (y * cols + x) * 4;
            if (sampled[k + 3] < 60) continue;
            ctx.fillStyle = `rgb(${sampled[k]} ${sampled[k + 1]} ${sampled[k + 2]})`;
          }
          ctx.fillRect(px, py, pw, ph);
        }
      }
    },
    cellSize: Math.max(2, cw),
  };
}

function show(it: Item, view: View | "anim") {
  it.el.dataset.view = view;
}

export async function morph(el: HTMLElement, to: View, animate = true): Promise<void> {
  const it = item(el);
  const run = ++it.run;
  it.view = to;
  // Already on screen: this also cancels a morph still waiting for its image.
  if (it.el.dataset.view === to) return;
  if (onebit()) {
    show(it, "pixel");
    return;
  }
  if (!(await loaded(it.img)) || run !== it.run) {
    if (run === it.run) show(it, to === "glass" && it.img.naturalWidth ? "glass" : "pixel");
    return;
  }
  if (!animate || reducedMotion()) {
    show(it, to);
    return;
  }
  const p = painter(it);
  const steps: Array<() => void> = [
    () => p.glass(),
    () => p.mosaic(p.cellSize / 2),
    () => p.mosaic(p.cellSize * 1.4),
    () => p.cells(0),
    () => p.cells(6),
    () => p.cells(11),
    () => p.cells(16),
  ];
  if (to === "glass") steps.reverse();
  show(it, "anim");
  for (const draw of steps) {
    if (run !== it.run) return;
    draw();
    await new Promise((r) => setTimeout(r, FRAME_MS));
  }
  if (run === it.run) show(it, to);
}

/** Glass logos with turntable frames follow the pointer horizontally. */
function follow(list: Item[]) {
  if (!list.length || reducedMotion()) return;
  let raf = 0;
  let pointer: number | null = null;
  let warmed = false;
  const update = () => {
    raf = 0;
    for (const it of list) {
      if (it.view !== "glass" || it.el.dataset.view !== "glass") continue;
      const r = it.el.getBoundingClientRect();
      const d = pointer === null ? 0 : Math.max(-1, Math.min(1, (pointer - (r.left + r.width / 2)) / Math.max(innerWidth * 0.42, 280)));
      const frame = Math.round((d + 1) * 6);
      if (frame === it.frame) continue;
      it.frame = frame;
      it.img.src = it.frames[frame];
    }
  };
  addEventListener("pointermove", (e) => {
    pointer = e.clientX;
    if (!warmed) {
      warmed = true;
      for (const it of list) it.frames.forEach((src) => (new Image().src = src));
    }
    if (!raf) raf = requestAnimationFrame(update);
  }, { passive: true });
  document.documentElement.addEventListener("pointerleave", () => {
    pointer = null;
    if (!raf) raf = requestAnimationFrame(update);
  });
}

export function initGlassPixels() {
  const all = [...document.querySelectorAll<HTMLElement>("[data-gp]")];
  const turning: Item[] = [];

  // Fetch glass renders shortly before they can be needed, so the first hover morphs at once.
  const warm = new IntersectionObserver((entries) => {
    for (const entry of entries) {
      if (!entry.isIntersecting) continue;
      warm.unobserve(entry.target);
      if (!onebit()) item(entry.target as HTMLElement).img.loading = "eager";
    }
  }, { rootMargin: "400px" });

  for (const el of all) {
    const it = item(el);
    const rest = (el.dataset.rest as View) ?? "pixel";
    const other: View = rest === "pixel" ? "glass" : "pixel";
    const trigger = el.dataset.trigger;
    if (it.frames.length) turning.push(it);
    warm.observe(el);

    if (trigger === "hover") {
      const host = el.closest<HTMLElement>("[data-gp-host]") ?? el;
      host.addEventListener("pointerenter", () => morph(el, other));
      host.addEventListener("pointerleave", () => morph(el, rest));
      host.addEventListener("focusin", () => morph(el, other));
      host.addEventListener("focusout", () => morph(el, rest));
    }

    if (trigger === "arrive") {
      addEventListener("pixel:arrived", () => setTimeout(() => morph(el, other), 180), { once: true });
      const host = el.closest<HTMLElement>("[data-gp-host]") ?? el;
      host.addEventListener("pointerenter", () => morph(el, rest));
      host.addEventListener("pointerleave", () => morph(el, other));
    }

    if (trigger === "scroll") {
      let arrived = false;
      let visible = true;
      addEventListener("pixel:arrived", () => {
        arrived = true;
        setTimeout(() => visible && morph(el, other), 420);
      }, { once: true });
      new IntersectionObserver(([entry]) => {
        visible = entry.intersectionRatio >= 0.5;
        if (arrived) morph(el, visible ? other : rest);
      }, { threshold: [0, 0.5, 1] }).observe(el);
      el.addEventListener("click", () => morph(el, item(el).view === "glass" ? "pixel" : "glass"));
    }
  }

  follow(turning);

  // Theme switches change ink and accent; 1-bit has no glass at all.
  addEventListener("theme:change", () => {
    for (const el of all) {
      const it = item(el);
      if (onebit()) show(it, "pixel");
      else show(it, it.view);
    }
  });
}

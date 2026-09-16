import { initChats } from "./chat-player";
import { reducedMotion } from "./env";
import { initGlassPixels } from "./glass-pixel";

const root = document.documentElement;
const THEME_KEY = "telegrinder-docs:theme";
const ARRIVE_KEY = "telegrinder-docs:arrive";

// ------------------------------------------------------------------ theme
type Theme = "auto" | "light" | "dark" | "onebit";

function storedTheme(): Theme {
  try {
    const t = localStorage.getItem(THEME_KEY);
    return t === "light" || t === "dark" || t === "onebit" ? t : "auto";
  } catch {
    return "auto";
  }
}

function applyTheme(theme: Theme) {
  root.removeAttribute("data-onebit");
  root.removeAttribute("data-theme");
  if (theme === "light" || theme === "dark") root.setAttribute("data-theme", theme);
  if (theme === "onebit") root.setAttribute("data-onebit", "");
  for (const b of document.querySelectorAll<HTMLElement>("[data-theme-choice]")) b.setAttribute("aria-pressed", String(b.dataset.themeChoice === theme));
  dispatchEvent(new Event("theme:change"));
}

for (const b of document.querySelectorAll<HTMLElement>("[data-theme-choice]")) {
  b.addEventListener("click", () => {
    const theme = b.dataset.themeChoice as Theme;
    try {
      localStorage.setItem(THEME_KEY, theme);
    } catch {
      /* the choice still applies to this page */
    }
    applyTheme(theme);
  });
}
applyTheme(storedTheme());

// ------------------------------------------------------------------ copy
document.addEventListener("click", async (e) => {
  const button = (e.target as Element).closest<HTMLButtonElement>(".copy");
  if (!button) return;
  e.stopPropagation();
  const text = button.dataset.copy ?? button.closest("figure")?.querySelector("code")?.innerText ?? "";
  let ok = false;
  try {
    await navigator.clipboard.writeText(text);
    ok = true;
  } catch {
    ok = false;
  }
  const label = button.dataset.label ?? button.textContent ?? "";
  button.dataset.label = label;
  button.dataset.state = ok ? "done" : "fail";
  button.textContent = (ok ? button.dataset.done : button.dataset.fail) ?? label;
  clearTimeout(Number(button.dataset.timer));
  button.dataset.timer = String(setTimeout(() => {
    button.textContent = label;
    delete button.dataset.state;
  }, 1600));
});

// ------------------------------------------------------------------ dissolve between pages
const canvas = document.querySelector<HTMLCanvasElement>("canvas.dissolve")!;
const BAYER = [0, 8, 2, 10, 12, 4, 14, 6, 3, 11, 1, 9, 15, 7, 13, 5];
const CELL = 8;

function dither(levels: number[], done: () => void) {
  const rect = canvas.getBoundingClientRect();
  const cols = Math.ceil(rect.width / CELL), rows = Math.ceil(rect.height / CELL);
  canvas.width = cols;
  canvas.height = rows;
  const ctx = canvas.getContext("2d")!;
  const probe = document.createElement("canvas").getContext("2d")!;
  probe.fillStyle = getComputedStyle(root).getPropertyValue("--ink").trim() || "#000";
  probe.fillRect(0, 0, 1, 1);
  const [r, g, b] = probe.getImageData(0, 0, 1, 1).data;
  const image = ctx.createImageData(cols, rows);
  let i = 0;
  const step = () => {
    if (i >= levels.length) return done();
    const level = levels[i++];
    for (let y = 0; y < rows; y++) {
      for (let x = 0; x < cols; x++) {
        const k = (y * cols + x) * 4;
        image.data[k] = r;
        image.data[k + 1] = g;
        image.data[k + 2] = b;
        image.data[k + 3] = BAYER[(y % 4) * 4 + (x % 4)] < level ? 255 : 0;
      }
    }
    ctx.putImageData(image, 0, 0);
    setTimeout(step, 34);
  };
  step();
}

const arrived = () => dispatchEvent(new Event("pixel:arrived"));

if (root.classList.contains("is-arriving") && !reducedMotion()) {
  dither([16], () => {
    root.classList.remove("is-arriving");
    dither([13, 10, 6, 3, 0], () => {
      canvas.getContext("2d")!.clearRect(0, 0, canvas.width, canvas.height);
      arrived();
    });
  });
} else {
  root.classList.remove("is-arriving");
  queueMicrotask(arrived);
}

addEventListener("pageshow", (e) => {
  if (!e.persisted) return;
  root.classList.remove("is-arriving");
  canvas.getContext("2d")!.clearRect(0, 0, canvas.width, canvas.height);
});

document.addEventListener("click", (e) => {
  if (e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey || reducedMotion()) return;
  const link = (e.target as Element).closest<HTMLAnchorElement>("a[href]");
  if (!link || link.target || link.hasAttribute("download")) return;
  const url = new URL(link.href, location.href);
  if (url.origin !== location.origin) return;
  if (url.pathname === location.pathname && url.search === location.search) return;
  e.preventDefault();
  dither([3, 6, 10, 13, 16], () => {
    try {
      sessionStorage.setItem(ARRIVE_KEY, "1");
    } catch {
      /* the next page simply appears without the uncover */
    }
    location.href = url.href;
  });
});

// ------------------------------------------------------------------ components
initGlassPixels();
initChats();

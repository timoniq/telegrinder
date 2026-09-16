// Reads the Markdown in ../docs at build time and turns it into routable pages.
// Nothing here is copied: the docs folder stays the single source of truth.
import fs from "node:fs";
import path from "node:path";

import type { Lang } from "./i18n";

export type Section = "tutorial" | "tools" | "reference";

export interface DocPage {
  /** Stable id shared by both languages, e.g. "tutorial/2_rules". */
  key: string;
  section: Section;
  /** Route without language prefix and without leading slash, e.g. "tutorial/rules/". */
  route: string;
  /** Path relative to the docs folder. */
  file: string;
  contentLang: Lang;
  title: string;
  short: string;
  number: number | null;
  markdown: string;
  lead: string;
  minutes: number;
  codeCount: number;
  inNav: boolean;
}

export const DOCS_DIR = path.resolve(process.cwd(), process.env.TELEGRINDER_DOCS_DIR ?? "../docs");
export const REPO_BLOB = "https://github.com/timoniq/telegrinder/blob/dev/";

const SHORT: Record<Lang, Record<string, string>> = {
  en: {
    "1_setting_up": "Setting up", "2_rules": "Rules", "3_functional_bits": "Functional bits", "4_api": "Telegram API",
    "5_nodes": "Nodes", "6_dispatch": "Dispatch", "7_keyboard": "Keyboards", "8_text": "Text and i18n", "9_states": "States",
    "10_media": "Media", "11_handling_errors": "Handling errors", "12_out-of-box_scenarios": "Ready-made scenarios",
  },
  ru: {
    "1_setting_up": "Запускаемся", "2_rules": "Правила", "3_functional_bits": "Функциональные штучки", "4_api": "Telegram API",
    "5_nodes": "Ноды", "6_dispatch": "Dispatch", "7_keyboard": "Клавиатуры", "8_text": "Текст и локализация", "9_states": "Стейты",
    "10_media": "Медиа", "11_handling_errors": "Обработка ошибок", "12_out-of-box_scenarios": "Готовые сценарии",
  },
};
const REFERENCE_SHORT: Record<Lang, Record<string, string>> = {
  en: { api: "API", changelog: "Changelog", community: "Community" },
  ru: { api: "API", changelog: "Изменения", community: "Сообщество" },
};

const read = (rel: string) => fs.readFileSync(path.join(DOCS_DIR, rel), "utf8");
const exists = (rel: string) => fs.existsSync(path.join(DOCS_DIR, rel));
const list = (rel: string) => (exists(rel) ? fs.readdirSync(path.join(DOCS_DIR, rel)) : []);

/** Drops the H1 and the hand-written navigation the site replaces (language and next/prev links). */
export function cleanMarkdown(md: string): string {
  return md
    .replace(/^﻿/, "")
    .replace(/^#\s+.+\r?\n/, "")
    .replace(/^\[?(EN|RU)\]?(\([^)]*\))?\s*\|\s*\[?(EN|RU)\]?(\([^)]*\))?\s*$/gm, "")
    .replace(/^\[(>>|<<)[^\n]*$/gm, "")
    .replace(/^\s+/, "");
}

function lead(md: string): string {
  const withoutCode = md.replace(/```[\s\S]*?```/g, "");
  for (const block of withoutCode.split(/\r?\n\s*\r?\n/)) {
    const b = block.trim();
    if (!b || /^([#>|<\-*\[]|\d+\.)/.test(b)) continue;
    return b.replace(/\s+/g, " ").replace(/`([^`]*)`/g, "$1").replace(/\[([^\]]*)\]\([^)]*\)/g, "$1").replace(/[*_]{1,2}([^*_]+)[*_]{1,2}/g, "$1");
  }
  return "";
}

function make(p: Omit<DocPage, "title" | "markdown" | "lead" | "minutes" | "codeCount" | "short"> & { short?: string }): DocPage {
  const raw = read(p.file);
  const title = raw.match(/^#\s+(.+)$/m)?.[1].trim() ?? p.key;
  const markdown = cleanMarkdown(raw);
  const words = markdown.replace(/```[\s\S]*?```/g, "").match(/[\p{L}\p{N}]+/gu)?.length ?? 0;
  return {
    ...p,
    title,
    short: p.short ?? title,
    markdown,
    lead: lead(markdown),
    minutes: Math.max(1, Math.round(words / 190)),
    codeCount: Math.floor((markdown.match(/^```/gm)?.length ?? 0) / 2),
  };
}

const semver = (v: string) => v.split(".").map((n) => parseInt(n, 10) || 0);

const cache = new Map<Lang, DocPage[]>();

export function pages(lang: Lang): DocPage[] {
  const hit = cache.get(lang);
  if (hit) return hit;
  const out: DocPage[] = [];

  const tutorialDir = exists(`tutorial/${lang}`) ? `tutorial/${lang}` : "tutorial/en";
  const tutorialLang: Lang = tutorialDir.endsWith("ru") ? "ru" : "en";
  const chapters = list(tutorialDir)
    .filter((f) => /^\d+_.+\.md$/.test(f))
    .sort((a, b) => parseInt(a, 10) - parseInt(b, 10));
  for (const f of chapters) {
    const stem = f.replace(/\.md$/, "");
    const n = parseInt(f, 10);
    if (n === 0) {
      out.push(make({ key: "tutorial/index", section: "tutorial", route: "tutorial/", file: `${tutorialDir}/${f}`, contentLang: tutorialLang, number: null, inNav: false }));
      continue;
    }
    const slug = stem.replace(/^\d+_/, "").replace(/_/g, "-");
    out.push(make({
      key: `tutorial/${stem}`, section: "tutorial", route: `tutorial/${slug}/`, file: `${tutorialDir}/${f}`,
      contentLang: tutorialLang, number: n, short: SHORT[lang][stem], inNav: true,
    }));
  }

  for (const f of list("tools").filter((f) => f.endsWith(".md")).sort()) {
    const stem = f.replace(/\.md$/, "");
    const index = stem === "index";
    out.push(make({
      key: `tools/${stem}`, section: "tools", route: index ? "tools/" : `tools/${stem.replace(/_/g, "-")}/`, file: `tools/${f}`,
      contentLang: "en", number: null, inNav: !index,
    }));
  }

  if (exists("api.md")) {
    out.push(make({ key: "reference/api", section: "reference", route: "api/", file: "api.md", contentLang: "en", number: null, short: REFERENCE_SHORT[lang].api, inNav: true }));
  }
  if (exists("changelog/index.md")) {
    out.push(make({ key: "changelog/index", section: "reference", route: "changelog/", file: "changelog/index.md", contentLang: "en", number: null, short: REFERENCE_SHORT[lang].changelog, inNav: true }));
    const versions = list("changelog").filter((f) => /^\d+\.\d+\.\d+\.md$/.test(f)).map((f) => f.replace(/\.md$/, ""));
    versions.sort((a, b) => {
      const [x, y] = [semver(a), semver(b)];
      return y[0] - x[0] || y[1] - x[1] || y[2] - x[2];
    });
    for (const v of versions) {
      out.push(make({ key: `changelog/${v}`, section: "reference", route: `changelog/${v}/`, file: `changelog/${v}.md`, contentLang: "en", number: null, inNav: false }));
    }
  }
  if (exists("community_links.md")) {
    out.push(make({ key: "reference/community", section: "reference", route: "community/", file: "community_links.md", contentLang: "en", number: null, short: REFERENCE_SHORT[lang].community, inNav: true }));
  }

  cache.set(lang, out);
  return out;
}

export const page = (lang: Lang, key: string) => pages(lang).find((p) => p.key === key);

export const tutorialChapters = (lang: Lang) => pages(lang).filter((p) => p.section === "tutorial" && p.number !== null);

/** Reading order for previous/next links. */
export const readingOrder = (lang: Lang) => pages(lang).filter((p) => p.inNav);

export function withBase(pathname: string): string {
  const base = import.meta.env.BASE_URL.replace(/\/?$/, "/");
  return base + pathname.replace(/^\//, "");
}

export const href = (lang: Lang, route: string) => withBase((lang === "ru" ? "ru/" : "") + route);

/** Maps a docs-relative Markdown file to the page key that renders it, for either language. */
export function keyForFile(file: string): string | undefined {
  const norm = path.posix.normalize(file);
  const tutorial = norm.match(/^tutorial\/(?:en|ru)\/(\d+_[^/]+)\.md$/);
  if (tutorial) return tutorial[1].startsWith("0_") ? "tutorial/index" : `tutorial/${tutorial[1]}`;
  for (const lang of ["en", "ru"] as Lang[]) {
    const hit = pages(lang).find((p) => p.file === norm);
    if (hit) return hit.key;
  }
  return undefined;
}

export const VERSION = (() => {
  const latest = list("changelog").filter((f) => /^\d+\.\d+\.\d+\.md$/.test(f)).map((f) => f.replace(/\.md$/, ""));
  latest.sort((a, b) => {
    const [x, y] = [semver(a), semver(b)];
    return y[0] - x[0] || y[1] - x[1] || y[2] - x[2];
  });
  return latest[0] ?? "";
})();

export const BOT_API = (() => {
  const config = path.resolve(DOCS_DIR, "../typegen/config.toml");
  if (!fs.existsSync(config)) return "";
  return fs.readFileSync(config, "utf8").match(/\[telegram-bot-api\][^[]*?version\s*=\s*"v?([^"]+)"/)?.[1] ?? "";
})();

export const PYTHON = (() => {
  const pyproject = path.resolve(DOCS_DIR, "../pyproject.toml");
  if (!fs.existsSync(pyproject)) return "";
  return fs.readFileSync(pyproject, "utf8").match(/requires-python\s*=\s*">=\s*([\d.]+)/)?.[1] ?? "";
})();

/** The "Basic example" block from the repository README, used by the home demo. */
export const README_EXAMPLE = (() => {
  const readme = path.resolve(DOCS_DIR, "../readme.md");
  if (!fs.existsSync(readme)) return "";
  return fs.readFileSync(readme, "utf8").match(/```python\n([\s\S]*?)```/)?.[1].trimEnd() ?? "";
})();

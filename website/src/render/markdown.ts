// Markdown → HTML for the docs, at build time.
// marked handles structure, Shiki tokenises code; token colours are emitted as classes,
// so light, dark and 1-bit themes restyle code without re-rendering.
import path from "node:path";

import { Marked, type Tokens } from "marked";
import { createHighlighter, type ThemeRegistration } from "shiki";

import { REPO_BLOB, href, keyForFile, page as findPage } from "../docs/content";
import type { Lang, Strings } from "../docs/i18n";
import { type ChatStrings, type PageScenes, esc, transcript } from "./chat";
import { glassIcon } from "./glass";

// Sentinel colours: Shiki resolves scopes to these, and we map them back to class names.
const TOKEN: Record<string, string> = {
  "#010101": "kw",
  "#020202": "str",
  "#030303": "num",
  "#040404": "com",
  "#050505": "fn",
  "#060606": "type",
  "#070707": "dec",
  "#080808": "const",
};
const color = (name: string) => Object.keys(TOKEN).find((k) => TOKEN[k] === name) as string;

const PIXEL_THEME: ThemeRegistration = {
  name: "telegrinder-pixel",
  type: "light",
  colors: { "editor.background": "#ffffff", "editor.foreground": "#000000" },
  tokenColors: [
    { scope: ["comment", "punctuation.definition.comment"], settings: { foreground: color("com"), fontStyle: "italic" } },
    { scope: ["string", "punctuation.definition.string", "string.quoted"], settings: { foreground: color("str") } },
    { scope: ["constant.character.escape", "constant.character.format.placeholder"], settings: { foreground: color("str"), fontStyle: "bold" } },
    { scope: ["constant.numeric"], settings: { foreground: color("num") } },
    { scope: ["constant.language", "support.type.exception"], settings: { foreground: color("const"), fontStyle: "bold" } },
    {
      scope: ["keyword", "storage.type", "storage.modifier", "keyword.control", "keyword.operator.logical", "keyword.operator.word"],
      settings: { foreground: color("kw"), fontStyle: "bold" },
    },
    { scope: ["meta.function.decorator", "entity.name.function.decorator", "punctuation.definition.decorator"], settings: { foreground: color("dec"), fontStyle: "bold" } },
    { scope: ["entity.name.function"], settings: { foreground: color("fn") } },
    { scope: ["entity.name.type", "entity.name.class"], settings: { foreground: color("type") } },
  ],
};

const LANGS = ["python", "shellscript", "json", "yaml", "toml", "html"] as const;
const ALIAS: Record<string, (typeof LANGS)[number]> = {
  python: "python", py: "python", python3: "python",
  bash: "shellscript", sh: "shellscript", shell: "shellscript", console: "shellscript", zsh: "shellscript",
  json: "json", yaml: "yaml", yml: "yaml", toml: "toml", html: "html",
};
const LABEL: Record<string, string> = { python: "py", shellscript: "sh", json: "json", yaml: "yaml", toml: "toml", html: "html" };

const highlighter = await createHighlighter({ themes: [PIXEL_THEME], langs: [...LANGS] });

function highlight(code: string, lang: (typeof LANGS)[number]): string {
  const lines = highlighter.codeToTokensBase(code, { lang, theme: PIXEL_THEME });
  return lines
    .map((line) =>
      line
        .map((t) => {
          const cls = t.color ? TOKEN[t.color.toLowerCase()] : undefined;
          return cls ? `<span class="t-${cls}">${esc(t.content)}</span>` : esc(t.content);
        })
        .join(""),
    )
    .join("\n");
}

export const slugify = (value: string) =>
  value.toLowerCase().replace(/[^\p{L}\p{N}]+/gu, "-").replace(/^-+|-+$/g, "") || "section";

export interface Heading {
  id: string;
  text: string;
  depth: number;
}

export interface Rendered {
  html: string;
  headings: Heading[];
}

interface RenderOptions {
  lang: Lang;
  /** Docs-relative path of the source file, used to resolve relative links. */
  file: string;
  strings: Strings;
  scenes?: PageScenes;
}

export function chatStrings(s: Strings): ChatStrings {
  return { edited: s.edited, popup: s.popup, photo: s.photo, sticker: s.sticker, deleted: s.deleted };
}

function resolveLink(raw: string, opts: RenderOptions): string {
  if (/^(https?:|mailto:|tg:|#)/.test(raw)) return raw;
  const [target, hash = ""] = raw.split("#");
  const fromDocsRoot = target.startsWith("/docs/") ? target.slice("/docs/".length) : null;
  const docsRelative = fromDocsRoot ?? path.posix.normalize(path.posix.join(path.posix.dirname(opts.file), target));
  if (target.endsWith(".md")) {
    const key = keyForFile(docsRelative);
    const hit = key ? findPage(opts.lang, key) : undefined;
    if (hit) return href(opts.lang, hit.route) + (hash ? `#${hash}` : "");
  }
  // Anything else lives in the repository: examples, sources, missing pages.
  const repoPath = target.startsWith("/")
    ? target.replace(/^\/+/, "")
    : path.posix.normalize(path.posix.join("docs", path.posix.dirname(opts.file), target));
  return REPO_BLOB + repoPath.replace(/^(\.\.\/)+/, "") + (hash ? `#${hash}` : "");
}

export function renderMarkdown(markdown: string, opts: RenderOptions): Rendered {
  const headings: Heading[] = [];
  const ids = new Set<string>();
  let codeIndex = 0;
  const s = opts.strings;

  const marked = new Marked({ gfm: true });
  marked.use({
    renderer: {
      code(tok: Tokens.Code) {
        const i = codeIndex++;
        const raw = (tok.lang ?? "").trim().split(/\s+/)[0].toLowerCase();
        const lang = ALIAS[raw];
        const body = lang ? highlight(tok.text, lang) : esc(tok.text);
        const label = lang ? LABEL[lang] : raw || "txt";
        const steps = opts.scenes?.[i];
        const scene = steps ? ` has-scene" title="${esc(s.sceneHint)}` : "";
        let html = `<figure class="code${scene}" data-i="${i}"><figcaption>${esc(label)}</figcaption><pre><code>${body}</code></pre><button class="copy" type="button" aria-label="${esc(s.copyLabel)}" data-done="${esc(s.copied)}" data-fail="${esc(s.copyFailed)}">${esc(s.copy)}</button></figure>`;
        if (steps) html += `<div class="chat-inline" aria-hidden="true">${transcript(steps, chatStrings(s))}</div>`;
        return html;
      },
      heading(tok: Tokens.Heading) {
        const inner = this.parser.parseInline(tok.tokens);
        const plain = inner.replace(/<[^>]+>/g, "").replace(/&amp;/g, "&").replace(/&lt;/g, "<").replace(/&gt;/g, ">").replace(/&quot;/g, '"').replace(/&#39;/g, "'");
        let id = slugify(plain);
        while (ids.has(id)) id += "-1";
        ids.add(id);
        headings.push({ id, text: plain, depth: tok.depth });
        return `<h${tok.depth} id="${id}">${inner}<a class="anchor" href="#${id}" aria-label="${esc(s.anchor)}">#</a></h${tok.depth}>`;
      },
      blockquote(tok: Tokens.Blockquote) {
        const body = this.parser.parse(tok.tokens);
        const alert = body.match(/^<p>\[!(TIP|NOTE|IMPORTANT|WARNING|CAUTION)\]\s*/);
        if (!alert) return `<blockquote>${body}</blockquote>`;
        const kind = alert[1] as keyof Strings["alerts"];
        const rest = body.replace(alert[0], "<p>").replace(/^<p>\s*<\/p>\s*/, "");
        return `<aside class="note note-${kind.toLowerCase()}" data-gp-host>${glassIcon("tip", "48px")}<div class="note-body"><p class="note-title">${esc(s.alerts[kind])}</p>${rest}</div></aside>`;
      },
      link(tok: Tokens.Link) {
        const inner = this.parser.parseInline(tok.tokens);
        const target = resolveLink(tok.href, opts);
        const external = /^https?:/.test(target);
        const title = tok.title ? ` title="${esc(tok.title)}"` : "";
        return `<a href="${esc(target)}"${title}${external ? ' target="_blank" rel="noopener"' : ""}>${inner}</a>`;
      },
      table(tok: Tokens.Table) {
        const cell = (c: Tokens.TableCell, tag: "th" | "td") =>
          `<${tag}${c.align ? ` style="text-align:${c.align}"` : ""}>${this.parser.parseInline(c.tokens)}</${tag}>`;
        const head = `<tr>${tok.header.map((c) => cell(c, "th")).join("")}</tr>`;
        const rows = tok.rows.map((r) => `<tr>${r.map((c) => cell(c, "td")).join("")}</tr>`).join("");
        return `<div class="table"><table><thead>${head}</thead><tbody>${rows}</tbody></table></div>`;
      },
    },
  });

  const html = marked.parse(markdown, { async: false }) as string;
  return { html, headings };
}

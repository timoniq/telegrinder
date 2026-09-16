// Plays conversation scenes in the pixel chat next to the code that produces them.
import { type ChatStrings, type PageScenes, type Step, album, esc, incoming, keyboard, outgoing, photo, sticker, system, transcript } from "../render/chat";
import { reducedMotion, wait } from "./env";

interface Data {
  scenes: PageScenes;
  strings: ChatStrings & { status: string; typing: string };
}

function player(chat: HTMLElement, data: Data) {
  const log = chat.querySelector<HTMLElement>(".chat-log")!;
  const kb = chat.querySelector<HTMLElement>(".chat-kb")!;
  const status = chat.querySelector<HTMLElement>(".chat-status-text")!;
  const body = chat.querySelector<HTMLElement>(".chat-body")!;
  let run = 0;
  let current: Step[] | null = null;

  const add = (html: string) => {
    log.insertAdjacentHTML("beforeend", html);
    return log.lastElementChild as HTMLElement;
  };
  const setKeyboard = (rows: Parameters<typeof keyboard>[0] | null) => {
    kb.innerHTML = rows ? keyboard(rows, "reply") : "";
  };
  const typing = (on: boolean) => {
    chat.classList.toggle("typing", on);
    status.textContent = on ? data.strings.typing : data.strings.status;
  };
  const findButton = (label: string) =>
    [...log.querySelectorAll<HTMLElement>(".kb-inline .kbtn"), ...kb.querySelectorAll<HTMLElement>(".kbtn")].reverse().find((b) => b.textContent === label);

  function still(steps: Step[]) {
    run++;
    current = steps;
    typing(false);
    body.querySelector(".chat-toast")?.remove();
    log.innerHTML = transcript(steps.filter((s) => !("kb" in s)), data.strings);
    for (const el of log.children) (el as HTMLElement).style.animation = "none";
    const lastKeyboard = [...steps].reverse().find((s): s is { kb: Parameters<typeof keyboard>[0] | null } => "kb" in s);
    setKeyboard(lastKeyboard ? lastKeyboard.kb : null);
  }

  async function play(steps: Step[]) {
    if (reducedMotion()) return still(steps);
    const id = ++run;
    const alive = () => id === run;
    current = steps;
    log.innerHTML = "";
    setKeyboard(null);
    typing(false);
    body.querySelector(".chat-toast")?.remove();
    let lastBot: HTMLElement | null = null;

    for (const step of steps) {
      if (!alive()) return;
      if ("u" in step) {
        await wait(420);
        if (alive()) add(outgoing(step.u));
      } else if ("sticker" in step) {
        await wait(420);
        if (alive()) add(sticker(data.strings));
      } else if ("photo" in step) {
        await wait(420);
        if (!alive()) return;
        const el = add(photo(step, data.strings));
        if (!step.out) lastBot = el;
      } else if ("album" in step) {
        await wait(420);
        if (alive()) add(album(step, data.strings));
      } else if ("b" in step) {
        await wait(240);
        if (!alive()) return;
        const dots = add('<div class="typing"><i></i><i></i><i></i></div>');
        typing(true);
        await wait(720);
        dots.remove();
        typing(false);
        if (alive()) lastBot = add(incoming(step));
      } else if ("sys" in step) {
        await wait(360);
        if (alive()) add(system(step.sys));
      } else if ("kb" in step) {
        await wait(220);
        if (alive()) setKeyboard(step.kb);
      } else if ("press" in step) {
        await wait(720);
        const button = findButton(step.press);
        if (button && alive()) {
          button.classList.add("pressed");
          await wait(260);
          button.classList.remove("pressed");
        }
      } else if ("toast" in step) {
        await wait(140);
        if (!alive()) return;
        const toast = document.createElement("div");
        toast.className = "chat-toast";
        toast.textContent = step.toast;
        body.appendChild(toast);
        await wait(1500);
        toast.remove();
      } else if ("relabel" in step && lastBot) {
        await wait(160);
        lastBot.querySelectorAll<HTMLElement>(".kbtn span").forEach((span) => {
          const next = step.relabel[span.textContent ?? ""];
          if (next) span.textContent = next;
        });
      } else if ("edit" in step && lastBot) {
        await wait(900);
        if (!alive()) return;
        const p = lastBot.querySelector("p");
        if (p) p.innerHTML = step.html ? step.edit : esc(step.edit);
        lastBot.querySelector(".kb-inline")?.remove();
        const meta = lastBot.querySelector(".meta");
        if (meta && !meta.querySelector(".edited")) meta.insertAdjacentHTML("afterbegin", `<span class="edited">${esc(data.strings.edited)}</span>`);
        lastBot.classList.remove("edited");
        void lastBot.offsetWidth;
        lastBot.classList.add("edited");
      } else if ("del" in step && lastBot) {
        await wait(1000);
        if (!alive()) return;
        const gone = lastBot;
        gone.classList.add("leaving");
        await wait(320);
        gone.replaceWith(document.createRange().createContextualFragment(system(data.strings.deleted)));
        lastBot = null;
      }
    }
  }

  chat.querySelector(".chat-replay")?.addEventListener("click", () => current && play(current));
  return { play, still };
}

export function initChats() {
  document.addEventListener("click", (e) => {
    const spoiler = (e.target as Element).closest(".spoiler");
    if (spoiler) spoiler.classList.toggle("open");
  });

  for (const chat of document.querySelectorAll<HTMLElement>("[data-chat]")) {
    const raw = chat.querySelector(".chat-data")?.textContent;
    if (!raw) continue;
    const data = JSON.parse(raw) as Data;
    const p = player(chat, data);
    const scope = chat.closest(".doc, .home-section") ?? document;
    const figures = [...scope.querySelectorAll<HTMLElement>("figure.code.has-scene")];
    if (!figures.length) continue;

    let live: HTMLElement | null = null;
    const visible = () => chat.offsetParent !== null;
    const activate = (fig: HTMLElement, animate: boolean) => {
      live?.classList.remove("live");
      live = fig;
      fig.classList.add("live");
      const steps = data.scenes[Number(fig.dataset.i)];
      if (!steps) return;
      if (animate && visible()) p.play(steps);
      else p.still(steps);
    };

    activate(figures[0], false);

    const seen = new Set<Element>();
    const io = new IntersectionObserver((entries) => {
      for (const entry of entries) entry.isIntersecting ? seen.add(entry.target) : seen.delete(entry.target);
      const top = figures.find((f) => seen.has(f));
      if (top && top !== live) activate(top, true);
    }, { rootMargin: "-38% 0px -52% 0px" });

    for (const fig of figures) {
      io.observe(fig);
      fig.addEventListener("click", (e) => {
        if ((e.target as Element).closest(".copy, a")) return;
        activate(fig, true);
      });
    }

    // The home demo starts playing when it scrolls into view.
    if (chat.classList.contains("chat-home")) {
      const once = new IntersectionObserver(([entry]) => {
        if (!entry.isIntersecting) return;
        once.disconnect();
        activate(figures[0], true);
      }, { threshold: 0.6 });
      once.observe(chat);
    }
  }
}

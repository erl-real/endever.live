/* =============================================================================
   EndEver Live — rendering
   Build DOM with a tiny helper. No template strings, no innerHTML with data in
   it, so nothing a creator types can ever be interpreted as markup.
   ========================================================================== */

const UI = (() => {
  /* ---------------------------------------------------------------- dom */

  function el(tag, props = {}, children = []) {
    const node = document.createElement(tag);
    for (const [key, value] of Object.entries(props || {})) {
      if (value == null || value === false) continue;
      if (key === "class") node.className = value;
      else if (key === "text") node.textContent = value;
      else if (key === "href") node.setAttribute("href", value);
      else if (key === "src") node.setAttribute("src", value);
      else if (key === "dataset") Object.assign(node.dataset, value);
      else if (key === "style") Object.assign(node.style, value);
      else if (key.startsWith("on") && typeof value === "function") {
        node.addEventListener(key.slice(2).toLowerCase(), value);
      } else if (value === true) node.setAttribute(key, "");
      else node.setAttribute(key, value);
    }
    for (const child of [].concat(children)) {
      if (child == null || child === false) continue;
      node.appendChild(typeof child === "string" ? document.createTextNode(child) : child);
    }
    return node;
  }

  const clear = (node) => { while (node.firstChild) node.removeChild(node.firstChild); };
  const mount = (node, ...kids) => { clear(node); kids.flat().forEach((k) => k && node.appendChild(k)); };

  /* ------------------------------------------------------------- format */

  const KIND_LABEL = { event: "Event", feedback: "Feedback", lesson: "Lesson", interviews: "Interview" };

  function formatDate(value, opts) {
    if (!value) return "";
    const d = new Date(value);
    if (Number.isNaN(d.getTime())) return "";
    return d.toLocaleDateString(undefined, opts || { day: "numeric", month: "short", year: "numeric" });
  }

  function formatWhen(value) {
    if (!value) return "";
    const d = new Date(value);
    if (Number.isNaN(d.getTime())) return "";
    const diff = d - Date.now();
    const abs = Math.abs(diff);
    const mins = Math.round(abs / 60000);
    const hours = Math.round(abs / 3600000);
    const days = Math.round(abs / 86400000);
    let unit;
    if (mins < 60) unit = `${mins} min`;
    else if (hours < 24) unit = `${hours} hr`;
    else unit = `${days} day${days === 1 ? "" : "s"}`;
    if (mins < 1) return "now";
    return diff > 0 ? `in ${unit}` : `${unit} ago`;
  }

  function formatBpm(bpm) { return bpm ? `${bpm} bpm` : ""; }

  function whenFor(post) {
    if (post.kind === "event" && post.starts_at) return formatDate(post.starts_at, { weekday: "short", day: "numeric", month: "short", hour: "2-digit", minute: "2-digit" });
    if (post.kind === "feedback" && post.starts_at) return post.is_live ? `Open now — closes ${formatWhen(post.ends_at)}` : `Opens ${formatWhen(post.starts_at)}`;
    return formatDate(post.created_at);
  }

  const initials = (name) => (name || "?")
    .split(/\s+/).slice(0, 2).map((w) => w[0] || "").join("").toUpperCase();

  /* -------------------------------------------------------------- pieces */

  const PLAY_ICON = () => {
    const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    svg.setAttribute("viewBox", "0 0 24 24");
    const p = document.createElementNS("http://www.w3.org/2000/svg", "path");
    p.setAttribute("d", "M8 5v14l11-7z");
    svg.appendChild(p);
    return svg;
  };

  function kindBadge(post) {
    return el("span", { class: "badge badge--kind", text: KIND_LABEL[post.kind] || post.kind });
  }

  function liveBadge(post) {
    if (post.kind !== "feedback" && post.kind !== "event") return null;
    if (post.is_live) return el("span", { class: "badge badge--live" }, [el("span", { class: "badge__dot" }), "Open"]);
    if (post.state === "closed") return el("span", { class: "badge badge--closed", text: "Closed" });
    return null;
  }

  function card(post) {
    const badges = [];
    if (post.kind !== "interviews") badges.push(kindBadge(post));
    badges.push(liveBadge(post));
    return el("a", { class: "card", href: `/postvod.html?slug=${encodeURIComponent(post.slug)}`, dataset: { kind: post.kind } }, [
      el("div", { class: "card__media" }, [
        post.thumb_url ? el("img", { src: post.thumb_url, alt: "", loading: "lazy" }) : null,
        badges.length ? el("div", { class: "card__badges" }, badges) : null,
        el("div", { class: "card__play" }, [PLAY_ICON()]),
      ]),
      el("div", { class: "card__body" }, [
        el("h3", { class: "card__title", text: post.title }),
        post.kind !== "interviews"
          ? el("div", { class: "card__sub" }, [el("span", { text: whenFor(post) })])
          : null,
        (post.tags || []).length
          ? el("div", { class: "card__tags" }, (post.tags || []).slice(0, 3).map((t) => el("span", { class: "tag", text: t })))
          : null,
      ]),
    ]);
  }

  function creatorCard(profile) {
    return el("a", { class: "card card--creator", href: `/creator.html?username=${encodeURIComponent(profile.username)}` }, [
      el("div", { class: "card__media" }, [
        profile.avatar_url
          ? el("img", { src: profile.avatar_url, alt: "" })
          : el("div", {
              style: {
                width: "100%", height: "100%", display: "grid", placeItems: "center",
                background: "var(--color-surface-raised)", fontSize: "28px",
                fontWeight: "800", color: "var(--color-text-muted)",
              },
              text: initials(profile.display_name),
            }),
      ]),
      el("div", { class: "card__body" }, [
        el("h3", { class: "card__title", text: profile.display_name || profile.username }),
        el("div", { class: "card__sub", text: profile.tagline || `@${profile.username}` }),
      ]),
    ]);
  }

  /* --------------------------------------------------------------- rails */

  function rail({ key, kind, title, note, href, items, render = card }) {
    if (!items || !items.length) return null;
    const row = el("div", { class: "rail__row hide-scrollbar", dataset: { rowKey: key || "" } }, items.map(render));
    const viewport = el("div", { class: "rail__viewport" }, [
      row,
      el("button", { class: "rail__more", type: "button", "aria-label": `Scroll ${title}` , text: "→", onClick: () => scrollRail(row) }),
    ]);
    return el("section", { class: "rail", dataset: { kind: kind || "" } }, [
      el("div", { class: "rail__head" }, [
        el("div", {}, [
          el("h2", { class: "rail__title", text: title }),
          note ? el("p", { class: "rail__note", text: note }) : null,
        ]),
        href ? el("a", { class: "rail__link", href, text: "See all →" }) : null,
      ]),
      viewport,
    ]);
  }

  function scrollRail(row) {
    if (!row || row.scrollWidth <= row.clientWidth + 1) return;
    const step = row.clientWidth;
    const max = row.scrollWidth - row.clientWidth;
    const next = row.scrollLeft + step;
    row.scrollTo({ left: next >= max - 1 ? 0 : next, behavior: "smooth" });
  }

  function syncRailArrows(root) {
    const scope = root || document;
    scope.querySelectorAll(".rail__viewport").forEach((vp) => {
      const row = vp.querySelector(".rail__row");
      const arrow = vp.querySelector(".rail__more");
      if (!row || !arrow) return;
      arrow.hidden = row.scrollWidth <= row.clientWidth + 1;
    });
  }

  /* ---------------------------------------------------------------- hero */

  function heroCarousel(stage, dotsWrap, items) {
    if (!items || !items.length) return;

    const slides = items.map((post) =>
      el("div", { class: "hero__slide" }, [
        el("div", { class: "hero__media" }, [
          post.thumb_url ? el("img", { src: post.thumb_url, alt: "" }) : null,
        ]),
        el("div", { class: "hero__body" }, [
          el("div", { class: "hero__eyebrow" }, [kindBadge(post), liveBadge(post)].filter(Boolean)),
          el("h1", { class: "hero__title", text: post.title }),
          el("div", { class: "hero__meta" }, [
            el("span", { text: whenFor(post) }),
            post.bpm ? el("span", {}, [el("b", { text: formatBpm(post.bpm) })]) : null,
            post.musical_key ? el("span", { text: post.musical_key }) : null,
          ]),
          (post.details && post.details.description)
            ? el("p", { class: "hero__desc", text: post.details.description })
            : null,
          el("div", { class: "hero__actions" }, [
            el("a", { class: "btn btn--primary", href: `/postvod.html?slug=${encodeURIComponent(post.slug)}`, text: "Open" }),
            el("a", { class: "btn btn--ghost", href: post.url, target: "_blank", rel: "noopener noreferrer", text: "Watch on YouTube" }),
          ]),
        ]),
      ])
    );

    slides.forEach((s) => stage.appendChild(s));

    const dots = items.map((post, i) =>
      el("button", {
        class: "hero__dot", type: "button",
        "aria-label": post.title,
        "aria-current": i === 0 ? "true" : "false",
        onClick: () => go(i),
      })
    );
    dots.forEach((d) => dotsWrap.appendChild(d));

    let index = 0;
    let timer = null;

    function go(next) {
      slides[index].classList.remove("is-active");
      dots[index].setAttribute("aria-current", "false");
      index = (next + slides.length) % slides.length;
      slides[index].classList.add("is-active");
      dots[index].setAttribute("aria-current", "true");
    }
    function start() {
      if (slides.length < 2) return;
      timer = setInterval(() => go(index + 1), 7000);
    }

    slides[0].classList.add("is-active");
    start();
    stage.addEventListener("mouseenter", () => clearInterval(timer));
    stage.addEventListener("mouseleave", start);
  }

  /* -------------------------------------------------------------- chrome */

  function headerScroll() {
    const header = document.querySelector(".site-header");
    if (!header) return;
    const onScroll = () => header.classList.toggle("is-scrolled", window.scrollY > 40);
    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();
  }

  let toastNode = null;
  function toast(message) {
    if (!toastNode) {
      toastNode = el("div", { class: "toast", role: "status" });
      document.body.appendChild(toastNode);
    }
    toastNode.textContent = message;
    toastNode.classList.add("is-open");
    clearTimeout(toastNode._t);
    toastNode._t = setTimeout(() => toastNode.classList.remove("is-open"), 2600);
  }

  function markActiveNav() {
    const here = location.pathname.split("/").pop() || "index.html";
    const q = new URLSearchParams(location.search);
    const kind = q.get("kind");
    const isCreatorView = q.get("creator") === "1" || here === "creator.html";

    let current = here;
    if (here === "browse.html") current = kind ? `kind:${kind}` : "";
    else if (isCreatorView) current = "creator";

    const keyOf = (a) => {
      let url;
      try { url = new URL(a.getAttribute("href") || "", location.origin); }
      catch { return ""; }
      if (url.pathname.endsWith("/playlist.html")) return "playlist";
      if (url.searchParams.get("creator") === "1") return "creator";
      const target = url.pathname.split("/").pop() || "index.html";
      if (target === "browse.html") {
        const k = url.searchParams.get("kind");
        return k ? `kind:${k}` : "";
      }
      return target;
    };

    document.querySelectorAll(".site-nav a").forEach((a) => {
      if (current && keyOf(a) === current) a.setAttribute("aria-current", "page");
    });

    if (here === "index.html") {
      const logo = document.querySelector(".site-logo");
      if (logo) logo.setAttribute("aria-current", "page");
    }
  }

  function query() {
    return new URLSearchParams(location.search);
  }

  return {
    el, mount, clear,
    card, creatorCard, rail, scrollRail, syncRailArrows, heroCarousel,
    kindBadge, liveBadge, initials, playIcon: PLAY_ICON,
    formatDate, formatWhen, formatBpm, whenFor,
    headerScroll, toast, markActiveNav, query,
    KIND_LABEL,
  };
})();

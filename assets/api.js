/* =============================================================================
   EndEver Live — API client
   Tries the backend first. If it is not running, falls back to the embedded
   DEMO_DATA so the frontend works from a plain static server.
   ========================================================================== */

const API = (() => {
  const BASE = window.ENDEVER_API || "";
  const DEMO = window.DEMO_DATA || null;
  let mode = "unknown";

  async function request(path, { method = "GET", body, params } = {}) {
    let url = BASE + path;
    if (params) {
      const qs = new URLSearchParams(
        Object.entries(params).filter(([, v]) => v !== "" && v != null)
      ).toString();
      if (qs) url += (url.includes("?") ? "&" : "?") + qs;
    }

    const headers = {};
    if (body) headers["Content-Type"] = "application/json";
    const jwt = localStorage.getItem("endever_token");
    if (jwt) headers.Authorization = `Bearer ${jwt}`;

    const res = await fetch(url, {
      method,
      headers,
      body: body ? JSON.stringify(body) : undefined,
    });

    const text = await res.text();
    let data = null;
    try { data = text ? JSON.parse(text) : null; } catch { data = { error: text }; }

    if (!res.ok) {
      const err = new Error((data && data.error) || `request failed (${res.status})`);
      err.status = res.status;
      err.data = data;
      throw err;
    }
    return data;
  }

  /* ---------------------------------------------------------- demo fallback */

  function demoHome() {
    if (!DEMO) throw new Error("no demo data");
    return DEMO.home;
  }

  function demoPosts(params = {}) {
    if (!DEMO) throw new Error("no demo data");
    let rows = [...DEMO.posts];
    if (params.kind) rows = rows.filter((r) => r.kind === params.kind);
    if (params.tag) rows = rows.filter((r) => (r.tags || []).includes(params.tag));
    if (params.genre) rows = rows.filter((r) => (r.genres || []).includes(params.genre));
    if (params.q) {
      const q = params.q.toLowerCase();
      rows = rows.filter((r) =>
        r.title.toLowerCase().includes(q) ||
        (r.tags || []).some((t) => t.toLowerCase().includes(q)) ||
        (r.genres || []).some((g) => g.toLowerCase().includes(q)) ||
        (r.details?.description || "").toLowerCase().includes(q)
      );
    }
    if (params.kind === "event") rows.sort((a, b) => (a.starts_at || "").localeCompare(b.starts_at || ""));
    else rows.sort((a, b) => (b.created_at || "").localeCompare(a.created_at || ""));
    const offset = params.offset || 0;
    const limit = params.limit || 24;
    return { items: rows.slice(offset, offset + limit), limit, offset, is_member: false };
  }

  function demoPost(slug) {
    if (!DEMO) throw new Error("no demo data");
    const post = DEMO.posts.find((p) => p.slug === slug);
    if (!post) throw Object.assign(new Error("not found"), { status: 404 });
    const creator = (DEMO.creators || []).find((c) => c.id === post.creator) || null;
    return { post, creator, is_member: false };
  }

  function demoCreators() {
    if (!DEMO) throw new Error("no demo data");
    return DEMO.creators || [];
  }

  function demoCreator(username) {
    if (!DEMO) throw new Error("no demo data");
    const creator = (DEMO.creators || []).find((c) => c.username === username);
    if (!creator) throw Object.assign(new Error("not found"), { status: 404 });
    const posts = (DEMO.posts || []).filter((p) => p.creator === creator.id);
    return { creator, posts, is_member: false };
  }

  function demoFacets() {
    if (!DEMO) throw new Error("no demo data");
    return DEMO.facets || { tags: [], genres: [] };
  }

  /* --------------------------------------------------------------- wrapper */

  async function tryRequest(fn, demoFn) {
    if (!BASE || !DEMO) {
      if (DEMO) return demoFn();
      return fn();
    }
    try {
      return await fn();
    } catch (err) {
      if (DEMO) return demoFn();
      throw err;
    }
  }

  return {
    get mode() { return mode; },

    async detect() {
      if (!BASE || !DEMO) {
        mode = DEMO ? "demo" : "offline";
        return mode;
      }
      try {
        const h = await request("/api/health");
        mode = h.mode;
      } catch {
        mode = DEMO ? "demo" : "offline";
      }
      return mode;
    },

    home:        () => tryRequest(() => request("/api/home"), demoHome),
    facets:      () => tryRequest(() => request("/api/facets"), demoFacets),
    posts:       (params) => tryRequest(() => request("/api/posts", { params }), () => demoPosts(params)),
    post:        (slug) => tryRequest(() => request(`/api/posts/${encodeURIComponent(slug)}`), () => demoPost(slug)),
    creators:    () => tryRequest(() => request("/api/creators"), demoCreators),
    creator:     (username) => tryRequest(() => request(`/api/creators/${encodeURIComponent(username)}`), () => demoCreator(username)),

    createPost:  (body) => request("/api/posts", { method: "POST", body }),
    updatePost:  (slug, body) => request(`/api/posts/${encodeURIComponent(slug)}`, { method: "PATCH", body }),
    deletePost:  (slug) => request(`/api/posts/${encodeURIComponent(slug)}`, { method: "DELETE" }),
  };
})();

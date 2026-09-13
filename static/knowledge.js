/* Knowledge — the routing surface, shown in the words the agent is handed.
   The map is drawn from /v1/graph. Every panel on the right is rendered by Pi, not here: clicking BB or
   an AS asks for the routing table that step produces, and clicking DATA asks for the file's bytes. A
   screen that formatted those itself would be a second implementation of the prompt. */
(() => {
  const t = (key) => window.IRISI18N?.t(key) || key;
  // The same lookup, with values. `t` was written to take a key alone and a dozen call sites rely on
  // that shape, so the interpolating form is its own name rather than an optional second argument
  // nobody would remember to pass.
  const tv = (key, vars) => window.IRISI18N?.t(key, vars) || key;
  const $ = (id) => document.getElementById(id);
  const SVGNS = "http://www.w3.org/2000/svg";
  // `open` is the Region whose nodes are fanned out; `openNode` is the node whose files are fanned out
  // beside them. The map used to stop at nodes, so the documents an operator actually wants to read had
  // no mark to click — the panel showed a list of addresses with no way to open one.
  const ZOOM_KEY = "knowledge-zoom";
  const ZOOM_STEPS = [0.5, 0.67, 0.8, 1, 1.25, 1.5, 2];
  const readZoom = () => {
    // Per viewer and per browser, like the language: one install is a team's ontology, and how big
    // somebody wants the map is about their screen and nobody else's.
    try {
      const v = Number(localStorage.getItem(ZOOM_KEY));
      if (ZOOM_STEPS.includes(v)) return v;
    } catch { /* private mode */ }
    return 1;
  };

  const state = { regions: [], nodes: [], edges: [], service: "", open: [], openNode: new Map(), selected: null, status: "pending", files: new Map(), entries: new Map(), cfg: { agent: false, agentUrl: "", derives: false }, flags: new Map(), picked: new Set(), services: [], overlays: [], vrfOn: false, vrfSel: null, curatorOn: false, links: [], zoom: readZoom(), domain: null, revision: null };

  const el = (tag, cls, text) => {
    const n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text != null) n.textContent = String(text);
    return n;
  };
  const svgEl = (tag, attrs) => {
    const n = document.createElementNS(SVGNS, tag);
    for (const k of Object.keys(attrs || {})) n.setAttribute(k, String(attrs[k]));
    return n;
  };
  const norm = (v) => String(v || "").toLowerCase().replace(/_/g, "-");
  // Several areas can be open at once. The reason is composition, not browsing: a person who knows the
  // structure builds an overlay by looking into more than one area and picking across them, and an
  // expand that cancels the last one makes that impossible to do by eye. `open` is a list; `openNode`
  // is one node per open area, because a rack losing its sub-rack when a node is opened in a different
  // rack is the same complaint one level down.
  const isOpen = (key) => state.open.includes(key);
  // Per open area, the nodes opened inside it, outermost first. It was one node per area while a
  // sub-rack drew only documents. Once an entity can be dragged into another, a node sits inside a
  // node — and a sub-rack that drew only documents made it vanish from the map the moment it landed.
  const pathIn = (key) => state.openNode.get(key) || [];
  const setPath = (key, path) => { if (path.length) state.openNode.set(key, path); else state.openNode.delete(key); };
  /** Close `id` wherever it is open, and everything opened inside it. */
  const forgetOpen = (id) => {
    for (const [key, path] of [...state.openNode]) { const i = path.indexOf(id); if (i >= 0) setPath(key, path.slice(0, i)); }
  };
  const openArea = (key) => { if (key && !isOpen(key)) state.open = [...state.open, key]; };
  const regionOf = (n) => n.region_dir || n.region;
  /** A stamp, in the reader's own clock.
   *
   *  It used to slice the first sixteen characters off the string and swap the `T` for a space, which
   *  is the whole of the bug: every stamp the API writes is UTC, and what came out carried no `Z` and
   *  no offset, so it read as local time and was not. A VRF drawn a moment ago in Seoul showed 11:18
   *  when the clock on the wall said 20:18, and nothing on the screen said which one it meant.
   *
   *  A stamp with no zone marker is UTC — that is what this API writes — and `new Date` would read it
   *  as local, which is the same mistake with more steps. Both spellings arrive: overlays write
   *  `…Z`, the curator writes `…+00:00`.
   *
   *  Fixed width rather than `toLocaleString`, because the overlay trail lays these out in a column
   *  and a locale-native string is a different length every time. Local, correct, and still aligned. */
  const when = (v) => {
    if (!v) return "—";
    const raw = String(v);
    const d = new Date(/[Zz]$|[+-]\d\d:?\d\d$/.test(raw) ? raw : raw + "Z");
    if (Number.isNaN(d.getTime())) return raw.slice(0, 16).replace("T", " ");
    const p = (n) => String(n).padStart(2, "0");
    return `${d.getFullYear()}-${p(d.getMonth() + 1)}-${p(d.getDate())} ${p(d.getHours())}:${p(d.getMinutes())}`;
  };

  function toast(message) {
    const box = $("toast");
    box.textContent = message;
    box.classList.add("show");
    setTimeout(() => box.classList.remove("show"), 2800);
  }


  async function request(path, options) {
    const o = { credentials: "same-origin", ...(options || {}) };
    const res = await fetch("/api/knowledge/" + path, o);
    const data = await res.json().catch(() => ({}));
    if (!res.ok) {
      // The reason a write was refused lives in `details[]`; `error` is only the headline. Showing the
      // headline alone told a person "validation failed" and nothing about what to fix.
      //
      // A refusal a person can actually meet also carries `reason` — a stable name for which refusal
      // it is — and `values`, what is inside it. Those get said in the reader's language; everything
      // else falls through to the server's English sentence, which is still sent and is still the
      // whole answer. That fallback is the point: the API stays one language, agents keep reading
      // exactly what they read before, and a reason this screen has never heard of degrades to a
      // correct English sentence rather than to a dotted identifier or a blank.
      const key = data.reason ? `knowledge.err.${data.reason}` : null;
      const known = key && window.IRISI18N?.t(key) !== key;
      let vals = data.values || {};
      // `field` names which field was refused, and it arrives as a token rather than as an English
      // word for exactly this reason: dropping "file name" into the middle of a Korean sentence is a
      // half-translated sentence, which reads worse than an English one.
      if (vals.field) {
        const fk = `knowledge.errfield.${vals.field}`;
        if (window.IRISI18N?.t(fk) !== fk) vals = { ...vals, field: t(fk) };
      }
      const head = known ? tv(key, vals) : (data.detail || data.error || `HTTP ${res.status}`);
      const why = Array.isArray(data.details) ? data.details.filter(Boolean) : [];
      const error = new Error(why.length ? `${head}\n${why.map((d) => `· ${d}`).join("\n")}` : head);
      error.status = res.status;
      throw error;
    }
    return data;
  }
  const post = (path, body) => request(path, {
    method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body || {}),
  });

  // ── the raw panel ─────────────────────────────────────────────────────────
  /** Ask Pi for exactly what this step hands the agent. `path` empty = hop 0, the block that sits in
   *  the system prompt. Nothing is reformatted here — a status other than ok is shown as it came. */
  async function showRaw({ kind, title, address }) {
    state.selected = { kind, address: address || null };
    draw();
    const target = editTarget(address);
    const chip = $("knRawKind");
    chip.textContent = OBJECT[target.kind].label;
    chip.className = `kn-chip-kind is-${target.kind}`;
    $("knRawTitle").textContent = title;
    $("knRawAddr").textContent = address || t("knowledge.systemPrompt");
    $("knRawMeta").textContent = "";
    $("knRawPath").textContent = breadcrumb(address);
    $("knCopy").hidden = target.kind === "region" || target.kind === "node";
    banner("");
    showEditor(false);
    const dialog = $("knRawDialog");
    if (!dialog.open) dialog.showModal();
    const pane = $("knRaw");
    pane.className = "kn-raw is-loading";
    pane.textContent = t("common.loading");
    try {
      const q = new URLSearchParams({ path: address || "", service: state.service || "" });
      const view = await request("view?" + q.toString());
      pane.className = `kn-raw is-${view.status === "ok" ? "ok" : "bad"}`;
      pane.textContent = view.text || "";
      $("knRawMeta").textContent =
        `${view.status} · ${(view.text || "").length} chars · ${String(view.ontology_revision || "").slice(0, 8)}`;
    } catch (error) {
      pane.className = "kn-raw is-bad";
      pane.textContent = `${t("knowledge.loadFailed")} — ${error.message}`;
    }
  }

  // ── the map ───────────────────────────────────────────────────────────────
  const edgeFrom = (e) => e.s || e.from;
  const edgeTo = (e) => e.t || e.to;

  function crossLinks() {
    const counted = new Map();
    const byId = new Map(state.nodes.map((n) => [n.id, n]));
    for (const e of state.edges) {
      const a = byId.get(edgeFrom(e));
      const b = byId.get(edgeTo(e));
      if (!a || !b) continue;
      const ra = norm(regionOf(a));
      const rb = norm(regionOf(b));
      if (!ra || !rb || ra === rb) continue;
      const key = [ra, rb].sort().join("|");
      counted.set(key, (counted.get(key) || 0) + 1);
    }
    return [...counted.entries()].map(([k, count]) => ({ pair: k.split("|"), count }));
  }

  // Drawn the way a network diagram is drawn, because that is what this is: a core, a distribution
  // layer, and access layers with many hosts. The one rule that matters is borrowed whole — many hosts
  // on one switch are not many lines to the switch; they are a rack with one uplink. The previous
  // layout fanned twenty documents out on twenty curves and the curves became a band. Here the line
  // count is the number of Regions plus two, whatever the Regions hold. Lines are orthogonal, as on a
  // wiring diagram; a curve says "roughly connected", a right angle says "this port".
  // The heights the map is drawn at when nothing sits above it. `draw()` shifts them down by whatever
  // the VRF chips occupy — see BASE_Y there.
  const BASE_Y = { core: 56, bus: 138, as: 186 };
  // One chip per open VRF, stacked in the top-left corner. Here rather than at the loop that draws
  // them, because the reservation that keeps the corner clear is computed from the same numbers, and
  // two copies of them is how the corner stops being clear again.
  const VRF = { x: 20, top: 16, h: 26, step: 34, gap: 14, maxW: 360 };
  const DEV = {
    core: { w: 212, h: 58 }, mgmt: { w: 140, h: 34 }, as: { w: 166, h: 50 },
    host: { w: 172, h: 36 }, sw: { w: 172, h: 40 }, leaf: { w: 172, h: 40 },
  };
  // What a row offers, read off the row. There used to be a rule here that parsed `/files/` out of
  // the address to spot "a data row that is really a node holding one file" — the one-file node —
  // and drew it as a leaf so a person could still reach the node. That deformity is gone: a node and
  // a file are one kind of thing now, so a row that can be read says `has_body` and a row that can be
  // entered says `children`. Both at once is a leaf, which is what that shape always meant.
  const canReadShape = (shape) => shape === "host" || shape === "leaf";
  // `empty` is an entity nobody has written into yet. The advertisement calls it neither a table nor
  // a document, which is right for an agent — there is nothing there to fetch.
  //
  // The screen opens it anyway, and deliberately. A rack is where `+ New data` lives, so refusing to
  // open an empty entity would leave the only thing on the map you cannot finish. What made the old
  // one-file node wrong was that it claimed something false; an empty node shown as empty claims
  // nothing, and clicking it is how it stops being empty.
  const canEnter = (c) => c.type === "dr" || c.type === "empty";
  const canRead = (c) => c.type === "data" || Boolean(c.has_body);
  const RACK = { pad: 20, gap: 14, head: 50, cols: 6 };

  /** Rough advance width at the map's 11.5px monospace face. A CJK glyph is about twice a latin one, so
   *  averaging them — which is what `length * 7` did — sized a Korean label as if it were English and
   *  left the text touching the pill. Nothing here needs to be exact; it needs to be wrong in the
   *  generous direction. */
  /** How wide a string draws. `px` is the width of one latin character in the face being measured;
   *  a CJK glyph is about 1.79 of those, which is why counting characters and multiplying gets a
   *  Korean or Japanese label badly wrong in a layout that has to reserve room before it draws. */
  const textWidth = (text, px = 7) => [...String(text || "")]
    .reduce((n, ch) => n + (/[\u1100-\u11FF\u3000-\u9FFF\uAC00-\uD7AF\uFF00-\uFFEF]/.test(ch) ? px * 1.79 : px), 0);

  /** Every domain hop 0 knows about: this backbone, whoever is advertising through a link, and any
   *  link that is down.
   *
   *  A link that is down is its own row and not a domain that vanished. Behind an exchange this
   *  backbone cannot tell "that backbone stopped advertising" from "that backbone is gone" — only the
   *  link's own state is knowable from here — so the wall says what it knows: the link is not
   *  answering, and the list is therefore incomplete. */
  function domainRows() {
    // Named for what it is, not for where it is: the chip beside it already says "here", and a card
    // whose name and flag are the same word says one thing twice.
    const rows = [{ id: "", label: t("knowledge.wall.thisBackbone"), here: true, up: true,
                    areas: state.regions.filter((r) => !r.peer), rev: state.revision, via: null }];
    const byOrigin = new Map();
    for (const r of state.regions) {
      if (!r.peer) continue;
      const key = String(r.origin || r.peer);
      if (!byOrigin.has(key)) byOrigin.set(key, { id: key, label: key, here: false, up: true,
        areas: [], rev: r.peer_revision || null, via: r.peer });
      byOrigin.get(key).areas.push(r);
    }
    rows.push(...[...byOrigin.values()].sort((a, b) => a.id.localeCompare(b.id)));
    for (const l of state.links || []) {
      if (l.reachable !== false) continue;
      // Keyed apart from an origin of the same name: a link is not the backbone behind it.
      rows.push({ id: `link:${l.name}`, label: l.label || l.name, here: false, up: false,
                  areas: [], rev: l.revision || null, via: l.name, why: l.error || "" });
    }
    return rows;
  }

  /** The wall. It appears only once there is more than one domain — a wall of one is not a wall, and
   *  an install with no link should see exactly the screen it saw before this existed. */
  function drawWall() {
    const panel = $("knWallPanel"), mine = $("knWallMine"), theirs = $("knWallTheirs");
    const rows = domainRows();
    panel.hidden = rows.length < 2;
    if (panel.hidden) { state.domain = null; mine.replaceChildren(); theirs.replaceChildren(); return; }
    if (state.domain !== null && !rows.some((d) => d.id === state.domain)) state.domain = null;
    // One scale across **both** walls, not one per wall. Comparing what this backbone advertises
    // against what reaches it is the comparison most worth having, and two scales would make five of
    // five and one of one draw identically.
    const scale = Math.max(1, ...rows.map((d) => d.areas.length));
    const CAP = 4;
    const cardFor = ((d) => {
      const sel = (state.domain || "") === d.id;
      const b = el("button", "kn-dcard" + (d.here ? " is-here" : "") + (d.up ? "" : " is-down") +
                             (sel ? " is-sel" : ""));
      b.type = "button";
      b.setAttribute("aria-pressed", String(sel));
      const top = el("div", "kn-dcard-top");
      top.append(el("span", "kn-dcard-name", d.label));
      // Only for the state its own group does not already say. "Across a link" on every card in the
      // group called *across a link* is a label repeated as many times as there are cards; a link
      // that is not answering is the one thing the group heading cannot tell you.
      if (!d.up) top.append(el("span", "kn-dcard-flag is-down", t("knowledge.wall.unreachable")));
      b.append(top);
      b.append(el("div", "kn-dcard-meta", d.rev ? `rev ${String(d.rev).slice(0, 7)}` : "—"));
      const shelf = el("div", "kn-shelf");
      for (let i = 0; i < scale; i++) shelf.append(el("i", i < d.areas.length ? "is-on" : ""));
      b.append(shelf);
      const tags = el("div", "kn-dtags");
      if (!d.up) tags.append(el("span", "kn-dnone", t("knowledge.wall.noAnswer")));
      else if (!d.areas.length) tags.append(el("span", "kn-dnone", t("knowledge.wall.nothing")));
      else {
        for (const r of d.areas.slice(0, CAP))
          tags.append(el("span", "kn-dtag", String(r.fetch || "").split("/").pop() || norm(r.source)));
        if (d.areas.length > CAP) tags.append(el("span", "kn-dtag is-more", `+${d.areas.length - CAP}`));
      }
      b.append(tags);
      const foot = el("div", "kn-dcard-foot");
      foot.append(el("span", null, d.here ? t("knowledge.wall.here") : `⌁ ${d.via || "—"}`));
      foot.append(el("span", "kn-r", tv("knowledge.wall.count", { n: d.areas.length })));
      b.append(foot);
      // Picking never un-picks: the map below always shows something, and an empty map would be a
      // hole in the screen rather than a state anybody wants.
      b.addEventListener("click", () => {
        if ((state.domain || "") === d.id) return;
        state.domain = d.id || null;
        state.open = []; state.openNode = new Map(); state.selected = null;
        draw();
      });
      return b;
    });
    mine.replaceChildren(...rows.filter((d) => d.here).map(cardFor));
    const away = rows.filter((d) => !d.here);
    theirs.replaceChildren(...away.map(cardFor));
    $("knWallCount").textContent = tv("knowledge.wall.summary",
      { n: away.length, areas: away.reduce((a, d) => a + d.areas.length, 0) });
  }

  function draw() {
    drawWall();
    const canvas = $("knTopo");
    canvas.replaceChildren();
    // Named by its address, not by `source`. `source` comes back with hyphens turned into
    // underscores, so a tile labelled from it reads `order_delivery` while everything that fetches
    // it says `order-delivery` — one area under two names, and the one on screen is the one that
    // does not work if anybody types it.
    // An area from a linked backbone is not a different kind of thing — it is the same thing, one
    // backbone further away. So it draws as an ordinary area and the difference is carried where it
    // matters: which backbone it hangs off, and a key that cannot collide with a local one. Both
    // sides of this pair of installs have a `payroll`, which is exactly the case that must not merge.
    // With a wall above, the map is the detail pane for one card. Without one — a single-backbone
    // install, which is most of them — this is every row there is and nothing changes.
    const pick = state.domain;
    const rows = !$("knWallPanel").hidden
      ? state.regions.filter((r) => (pick === null ? !r.peer : String(r.origin || r.peer) === pick))
      : state.regions;
    const ases = rows.map((r) => {
      const dir = String(r.fetch || "").split("/").pop() || norm(r.source);
      const peer = r.peer || null;
      return { key: peer ? `${peer}:${dir}` : dir, label: dir, kind: "as",
               address: r.fetch || `/v1/regions/${dir}`,
               region: r, peer, peerLabel: r.peer_label || peer,
               // `peer` is who this backbone asks — the first hop, and what the read-only rules key
               // on. `origin` is who the area belongs to, which is not the same once an exchange is
               // in the middle: it carries the area and does not hold it. The picture groups by
               // origin so that nothing is drawn as belonging to the thing that merely passed it on.
               origin: r.origin || peer,
               originLabel: r.origin ? String(r.origin).toUpperCase() : (r.peer_label || peer),
               originRevision: r.peer_revision || null,
               flagKey: peer ? null : dir, pickable: !peer };
    });
    const openIdx = ases.map((_, i) => i).filter((i) => isOpen(ases[i].key));

    // Every open rack is measured before the canvas is sized, because the canvas has to be wide enough
    // to hold them all side by side. Sizing the canvas first is how the second rack ends up drawn past
    // the right edge and simply is not there.
    //
    // What shrinks as more open is the tile grid: six columns for one rack, four for two, three beyond
    // that. The header keeps every button — an area whose "+ New node" disappeared because a second area
    // was opened would be a capability lost to a layout — so the buttons wrap to a second line instead.
    const cap = openIdx.length <= 1 ? RACK.cols : openIdx.length === 2 ? 4 : 3;
    const plans = openIdx.map((i) => rackPlan(ases[i], cap, openIdx.length > 1));
    const GUT = 28;
    const racksW = plans.reduce((n, r) => n + r.w, 0) + Math.max(plans.length - 1, 0) * GUT;

    // The chips are drawn in the map's own coordinates, so the map has to leave the corner empty. It
    // did not. At the canvas's 1080 minimum the core's left management host lands at x 224..364,
    // y 39..73 — under the first chip and squarely under the second, and because the chips are
    // appended before the management row the tile was painted over the top of them. That is the
    // failure the racks below already solved: reserve the room before anything is placed, rather than
    // hoping the space is free. The map keeps the margin it always had when no VRF is open.
    const vrfBottom = state.overlays.length ? VRF.top + (state.overlays.length - 1) * VRF.step + VRF.h : 0;
    const drop = Math.max(0, vrfBottom + VRF.gap - (BASE_Y.core - DEV.core.h / 2));
    const Y = { core: BASE_Y.core + drop, bus: BASE_Y.bus + drop, as: BASE_Y.as + drop };

    // A link whose peer is down advertises nothing, so it has no areas and would take no room — and
    // the map would then look exactly like a backbone that has no link at all. Those are different
    // facts and this is the picture that has to tell them apart, so the room is reserved for the
    // device whether or not anything hangs off it.
    // A link that answered nothing still gets its room reserved, or a failed link would look exactly
    // like an install that never had one. With a wall above, that job belongs to its card — so the
    // device is drawn only when its own card is the one selected, and the map stays the detail of
    // one thing rather than one thing plus every outage.
    const silent = (state.links || []).filter(
      (l) => l.reachable === false && !ases.some((a) => a.peer === l.name)
             && ($("knWallPanel").hidden || state.domain === `link:${l.name}`));
    const asRow = ases.length * DEV.as.w + (ases.length - 1) * 24;
    const width = Math.max(1080, asRow + 96, racksW + 40) + silent.length * (DEV.core.w + 48);
    const links = svgEl("g", {});
    const marks = svgEl("g", {});
    canvas.append(links, marks);

    const cx = width / 2;
    const asX = (i) => (width - asRow) / 2 + DEV.as.w / 2 + i * (DEV.as.w + 24);
    const seg = (pts, cls, extra) => links.append(svgEl("polyline", { points: pts.map((p) => p.join(",")).join(" "), class: cls, ...(extra || {}) }));

    // Core, with the two things the backbone reads directly hung off it as management hosts: the Core
    // document and the service fragment. They are not Regions and were crowding the Region row.
    seg([[cx, Y.core + DEV.core.h / 2], [cx, Y.bus]], "kn-wire");
    marks.append(device({ key: "__bb", label: "RouteMind Back-Bone", kind: "bb", address: "", flagKey: "__bb" }, cx, Y.core, "core"));
    // The selection, summarised where it can be read and started as one act. Ticking three areas and
    // then hunting for a button on one of them is how a person ends up starting with the wrong set.
    if (state.picked.size && canPick()) {
      const names = [...state.picked].map(shortAddr);
      const acts = [
        ...(state.vrfOn ? [{ label: `◇ ${t("knowledge.vrf.draw")} ${state.picked.size} — ${names.join(" + ")}`, run: () => drawVrfCard() }] : []),
        ...(canRun() ? [{ label: `▶ ${t("knowledge.pick.start")} ${state.picked.size}${state.vrfOn ? "" : ` — ${names.join(" + ")}`}`, run: () => startRun([]) }] : []),
      ];
      const widths = acts.map((a) => textWidth(a.label) + 44);
      const total = widths.reduce((n, w) => n + w, 0) + (acts.length - 1) * 10;
      const by = Y.core + DEV.core.h / 2 + 14;
      let bx = cx - total / 2;
      acts.forEach((a, i) => {
        const w = widths[i];
        const g = svgEl("g", { class: "kn-picked-bar" + (i ? " is-second" : ""), tabindex: "0", role: "button" });
        g.append(svgEl("rect", { x: bx, y: by, width: w, height: 28, rx: 14 }));
        const tx = svgEl("text", { x: bx + w / 2, y: by + 19, "text-anchor": "middle" });
        tx.textContent = a.label;
        g.append(tx);
        g.addEventListener("click", () => a.run());
        g.addEventListener("keydown", (e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); a.run(); } });
        marks.append(g);
        bx += w + 10;
      });
      const clr = svgEl("g", { class: "kn-picked-clear", tabindex: "0", role: "button" });
      const cxx = bx + 6;
      clr.append(svgEl("rect", { x: cxx - 12, y: by, width: 24, height: 28, rx: 14 }));
      const ct = svgEl("text", { x: cxx, y: by + 19, "text-anchor": "middle" });
      ct.textContent = "×";
      clr.append(ct);
      const wipe = () => { state.picked.clear(); draw(); };
      clr.addEventListener("click", wipe);
      clr.addEventListener("keydown", (e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); wipe(); } });
      marks.append(clr);
    }
    // The VRFs open right now, whoever drew them — one chip each, top left, in the band `drop`
    // reserved for them above. A chip opens the overlay: its question, what is in it and why, and the
    // trail of how it got there.
    state.overlays.forEach((ov, i) => {
      const n = (ov.members || []).length;
      // Who and how many first: when the chip runs out of room it is the question's tail that goes.
      const label = `◇ ${(ov.by || {}).name || "?"} · ${n} · ${ov.question || ov.id}`;
      const w = Math.min(textWidth(label) + 28, VRF.maxW), x0 = VRF.x, y0 = VRF.top + i * VRF.step;
      const g = svgEl("g", { class: "kn-vrf-chip" + (state.vrfSel === ov.id ? " is-sel" : ""), tabindex: "0", role: "button" });
      g.append(svgEl("rect", { x: x0, y: y0, width: w, height: VRF.h, rx: VRF.h / 2 }));
      const tx = svgEl("text", { x: x0 + 14, y: y0 + VRF.h / 2 + 4 });
      tx.textContent = fitted(label, w - 10);
      g.append(tx);
      // Opening one also makes it the one the map outlines, and it stays outlined after the dialog
      // closes — the dialog covers the map. A second press lets go.
      const open = () => {
        if (state.vrfSel === ov.id) { state.vrfSel = null; draw(); return; }
        showOverlay(ov);
      };
      g.addEventListener("click", open);
      g.addEventListener("keydown", (e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); open(); } });
      marks.append(g);
    });
    const mgmt = [{ key: "core", label: "core.md", kind: "data", address: "/v1/core", side: -1 }];
    // Services hang off the core because that is what they are — read by the backbone, not by an AS —
    // and they are pickable because a run needs one and there is no dropdown any more.
    (state.services.length ? state.services : state.service ? [state.service] : []).forEach((id, i) => {
      mgmt.push({ key: `svc:${id}`, label: `svc · ${id}`, kind: "as", address: `/v1/services/${id}`,
                  side: 1, order: i, pickable: true });
    });
    for (const m of mgmt) {
      const x = cx + m.side * (DEV.core.w / 2 + 70 + DEV.mgmt.w / 2);
      const y = Y.core + (m.order || 0) * (DEV.mgmt.h + 10);
      seg([[cx + m.side * DEV.core.w / 2, Y.core], [x - m.side * DEV.mgmt.w / 2, Y.core], [x - m.side * DEV.mgmt.w / 2, y]], "kn-wire");
      marks.append(device(m, x, y, "mgmt"));
    }

    // One bus per backbone, and a line between the backbones themselves. A peer's areas hang off the
    // peer, not off this one: drawn on a single bus they would read as areas of this ontology, which
    // is the one thing the picture must not say. The link is drawn dashed and labelled with the state
    // the API reported, because a link is the first thing on this map that can be down.
    // Grouped by **origin**, not by the peer it was asked of. With an exchange in the middle those
    // differ, and grouping by the peer would hang three backbones' areas under one EXCHANGE device —
    // a picture that says the exchange holds them, which is false. It carries them. Network diagrams
    // draw the adjacency and not the fabric between, for the same reason.
    //
    // So a working exchange is not drawn at all. A failed one is, because then it is the thing that
    // broke and naming it is the only useful thing left to say — that is `silent` below, which keys
    // on the peer and not on the origin.
    const groups = new Map();
    ases.forEach((row, i) => {
      const g = row.origin || row.peer;
      if (!groups.has(g)) groups.set(g, []);
      groups.get(g).push(i);
    });
    const linkState = new Map((state.links || []).map((l) => [l.name, l]));

    // The ones that answered nothing: a device and the wire to it, marked, with nothing below.
    silent.forEach((l, i) => {
      const hub = width - (silent.length - i) * (DEV.core.w + 48) + DEV.core.w / 2 + 24;
      seg([[cx + DEV.core.w / 2, Y.core], [hub, Y.core]], "kn-wire is-link is-down");
      marks.append(device({ key: `__peer:${l.name}`, label: l.label || l.name, kind: "bb",
                            address: "", peer: l.name, link: l }, hub, Y.core, "core"));
    });

    for (const [origin, idx] of groups) {
      const from = asX(idx[0]), to = asX(idx[idx.length - 1]);
      const hub = (from + to) / 2;
      if (origin) {
        const head = ases[idx[0]];
        // Its own state, not the transport's. Reached directly there is a link entry; reached through
        // an exchange there is not, and what is knowable from here is what it advertised and the
        // revision that came with it.
        const l = linkState.get(origin) || { reachable: true, areas: idx.length,
                                             revision: head.originRevision };
        const dev = { key: `__peer:${origin}`, label: head.originLabel || origin, kind: "bb",
                      address: "", peer: head.peer, link: l };
        // The wire this backbone reaches it by. Dashed and, when it is down, marked — the rows above
        // are still drawn because the API still advertised them a moment ago, and a link that has
        // gone quiet is a thing to see rather than a row that silently disappears.
        seg([[cx + DEV.core.w / 2, Y.core], [hub, Y.core]],
            "kn-wire is-link" + (l.reachable === false ? " is-down" : ""));
        marks.append(device(dev, hub, Y.core, "core"));
        seg([[hub, Y.core + DEV.core.h / 2], [hub, Y.bus]], "kn-wire is-link" + (l.reachable === false ? " is-down" : ""));
      }
      seg([[from, Y.bus], [to, Y.bus]], "kn-wire is-bus" + (origin ? " is-link" : ""));
      idx.forEach((i) => {
        const row = ases[i];
        const on = isOpen(row.key);
        seg([[asX(i), Y.bus], [asX(i), Y.as - DEV.as.h / 2]],
            "kn-wire" + (on ? " is-on" : "") + (origin ? " is-link" : ""));
        marks.append(device(row, asX(i), Y.as, "as"));
      });
    }

    let bottom = Y.as + DEV.as.h / 2 + 52;
    if (plans.length) {
      // Relations between Regions used to be drawn here as dashed trunks with a count. Off the map
      // (operator, 2026-09-09): relations are getting a page of their own, and the dashes were noise.
      //
      // Cabling. Each drop steps down to its own height before it turns, so no two cables share a
      // horizontal run, and the racks are laid out in the same left-to-right order as the switches
      // they hang off, so the turns cannot cross either. With one rack open the turn has no length and
      // this is the same straight drop it always was.
      const rackTop = Y.as + DEV.as.h / 2 + 52 + (plans.length - 1) * 9;
      // Each rack goes under its own switch, pushed right past the one before it and pulled left far
      // enough to leave room for the ones after it. Reserving that room is the part that is easy to
      // miss: clamping only into the canvas put the third of three adjacent racks 42px on top of its
      // neighbour, because the first rack had already started right of the margin and pushed the rest
      // into the right edge. With the reservation the interval is never empty, so racks cannot overlap
      // and none can be pushed out of the drawing.
      const room = new Array(plans.length).fill(0);
      for (let k = plans.length - 2; k >= 0; k--) room[k] = room[k + 1] + GUT + plans[k + 1].w;
      let cursor = 20;
      plans.forEach((r, k) => {
        const i = openIdx[k];
        r.left = Math.min(Math.max(asX(i) - r.w / 2, cursor), width - 20 - r.w - room[k]);
        cursor = r.left + r.w + GUT;
        const stub = Y.as + DEV.as.h / 2 + 20 + k * 9;
        // The cable enters the rack at the point nearest under its own switch, not at the rack's
        // middle: a rack still sitting under its switch takes a straight drop, and one pushed aside to
        // make room for a neighbour is entered at the near corner instead of crossing its own face.
        const port = Math.min(Math.max(asX(i), r.left + RACK.pad), r.left + r.w - RACK.pad);
        seg(port === asX(i)
          ? [[asX(i), Y.as + DEV.as.h / 2], [asX(i), rackTop]]
          : [[asX(i), Y.as + DEV.as.h / 2], [asX(i), stub], [port, stub], [port, rackTop]], "kn-wire is-on");
      });

      for (const r of plans) {
        const path = pathIn(r.as.key);
        const rep = r.as.region?.representative || null;
        // Every rack is somewhere an entity can be dropped: the area's rack is its representative, a
        // sub-rack is the node it shows. `chain` is what holds what, down to here — a drop onto
        // anything whose chain contains the dragged entity would put it inside itself.
        const rack = rackBox(r.tiles, { title: r.title, note: r.note, left: r.left, top: rackTop, actions: r.actions, metrics: r,
                                        openNode: path[0] || null,
                                        drop: rep ? { id: rep, area: r.as.key, chain: [rep], label: r.as.label } : null });
        marks.append(rack.g);
        let colBottom = rack.bottom + 48;

        // A sub-rack for each node opened, each hung below the one that holds it. Same rule: one line.
        // A step that is not on the level above — not loaded yet, or moved away by someone else — stops
        // the drawing there; the path is left alone, because "not loaded yet" is not "gone".
        let above = rack, chain = rep ? [rep] : [];
        for (let k = 0; k < path.length; k++) {
          const openNode = path[k];
          const ax = above.anchorFor(openNode);
          if (ax == null) break;
          chain = [...chain, openNode];
          const subTiles = (state.files.get(openNode) || []).map((c) => tileFor(c, r.as.key, k + 1, openNode));
          const subActions = asActions(r.as, openNode, subTiles);
          const subNote = noteFor(subTiles);
          const sm = rackMetrics(subTiles, { title: openNode, note: subNote, actions: subActions, cap, wrap: plans.length > 1 });
          // Kept inside its own column where it fits, and inside the canvas always — a sub-rack that
          // wandered under the neighbouring column would read as belonging to it.
          const lo = Math.max(20, Math.min(r.left, width - sm.w - 20));
          const hi = Math.max(lo, Math.min(r.left + r.w - sm.w, width - sm.w - 20));
          const sub = rackBox(subTiles, {
            title: openNode, note: subNote, left: Math.min(Math.max(ax - sm.w / 2, lo), hi),
            top: above.bottom + 48, sub: true, actions: subActions, metrics: sm, openNode: path[k + 1] || null,
            drop: { id: openNode, area: r.as.key, chain, label: openNode },
          });
          seg([[ax, above.anchorY ?? above.bottom], [ax, above.bottom], [ax, sub.top]], "kn-wire is-on");
          marks.append(sub.g);
          colBottom = sub.bottom + 32;
          above = sub;
        }
        bottom = Math.max(bottom, colBottom);
      }
    }

    // Room for the service hosts, which stack down beside the core. Without this a third service is
    // drawn outside the viewBox and simply does not appear.
    const svcRows = Math.max((state.services.length || (state.service ? 1 : 0)) - 1, 0);
    const height = Math.max(bottom, 300, Y.core + svcRows * (DEV.mgmt.h + 10) + DEV.mgmt.h + 40);
    // The viewBox stays the drawing's own size and only the rendered size is scaled, so zooming
    // changes nothing about where anything is. Every coordinate this function computed — the racks it
    // measured before sizing the canvas, the corner it reserved for the VRF chips, the drop targets a
    // drag tests with `elementFromPoint` — is still in the same place, and the wrapper's existing
    // `overflow-x: auto` becomes the pan. Redrawing at a scaled size instead would mean every one of
    // those measurements happening in a different coordinate system depending on the zoom.
    canvas.setAttribute("viewBox", `0 0 ${width} ${height}`);
    canvas.setAttribute("width", Math.round(width * state.zoom));
    canvas.setAttribute("height", Math.round(height * state.zoom));
  }

  /** Everything about one open area's rack except where it goes: its tiles, its header, its actions
   *  and how wide it wants to be. Split out of `draw` because the canvas cannot be sized until every
   *  open rack has been measured, and it cannot be measured without knowing what it holds. */
  function rackPlan(as, cap, wrap) {
    const fan = state.entries.get(as.key) || [];

    // The area's rack is its representative's table; every row in it hangs off the representative.
    const rep = as.region?.representative || null;
    const tiles = fan.map((c) => tileFor(c, as.key, 0, rep));

    const note = noteFor(tiles);
    const actions = asActions(as, rep, tiles);
    return { as, tiles, title: as.label, note, actions, ...rackMetrics(tiles, { title: as.label, note, actions, cap, wrap }) };
  }

  /** The buttons on an Autonomous System — the same on an area and on a node inside it (operator,
   *  2026-09-11: "they are all nodes; treat them the same"). An area's rack used to offer more than a
   *  node's and a node's offered Edit instead; what differs now is only what each button acts on.
   *  `holder` is the entity whose rack this is — an area's rack is its representative's. */
  function asActions(as, holder, tiles) {
    const rep = as.region?.representative || null;
    const isArea = !holder || holder === rep;
    const address = isArea ? as.address : `/v1/nodes/${holder}`;
    const row = isArea ? as : { kind: "as", label: holder, address };
    const flagKey = isArea ? as.key : `node:${holder}`;
    const flags = flagsFor(flagKey).length;
    // An area on a linked backbone is read from here and written where it lives. Its rack was
    // offering "+ New node", "+ New data", "Advertise upstream" and a delete — four ways to write
    // into another organisation's ontology, one of them destructive, and every one of them refused
    // by the far end with 405. Refusing over there is the backstop; not drawing the button is the
    // interface. What is left is the thing that makes sense at this distance: read its routing table.
    if (as.peer) {
      return [{ label: t("knowledge.act.table"),
                run: () => showRaw({ kind: "as", title: row.label, address }) }];
    }
    return [
      ...(flags ? [{ label: `⚑ ${t("knowledge.flag.short")} ${flags}`, flag: true, run: () => reviewFlags(flagKey, row.label, address) }] : []),
      ...(canRun() ? [{ label: t("knowledge.act.start"), primary: true, run: () => startRun([address]) }] : []),
      // Proposes a new line for what this system advertises upward: an area's own line, or — for a
      // node — the row its holder's table shows for it. Both go through the review queue, so it is
      // offered only where there is a queue to reach.
      ...(state.curatorOn ? [{ label: t("knowledge.submit.raise"),
        run: () => openCard(row, () => (isArea ? submitCard(as.key, "as") : submitCard(as.key, "entity", { entity: holder }))) }] : []),
      // What this area sends across a link. An area's decision, so it is offered on areas — and only
      // where there is a queue to reach, like every other advertisement.
      ...(state.curatorOn && isArea ? [{ label: t("knowledge.export.act"),
        run: () => openCard(row, () => exportCard(as.key)) }] : []),
      { label: t("knowledge.act.table"), run: () => showRaw({ kind: "as", title: row.label, address }) },
      { label: "+ " + t("knowledge.act.newNode"), run: () => openCard(row, () => newNodeForm(as.key, isArea ? null : holder)) },
      ...(holder ? [{ label: "+ " + t("knowledge.act.newData"),
                      run: () => openCard({ kind: "as", label: holder, address: `/v1/nodes/${holder}` }, () => newFileForm(holder)) }] : []),
      // Last, and a bin rather than a word: this ships with two example areas, and clearing them is
      // the first thing a real user does.
      { label: t("knowledge.delete"), icon: "trash", danger: true,
        run: () => openCard(row, () => (isArea ? deleteAreaCard(as, tiles) : deleteNodeCard(holder))) },
    ];
  }

  /** One row of a table, drawn as a tile. The same at every depth: a node inside a node is the same
   *  kind of thing as a node in an area's rack, so it is drawn the same way and opens the same way.
   *  `level` is 0 in the area's rack and k+1 in the k-th sub-rack below it; `holder` is the entity the
   *  row hangs off — what a drag moves it out of. */
  function tileFor(c, areaKey, level, holder) {
    const enter = canEnter(c), read = canRead(c);
    // host = only readable · sw = only enterable · leaf = both, which is now an ordinary entity
    // rather than the costume a file wore to get an address.
    const shape = enter ? (read ? "leaf" : "sw") : "host";
    const counts = c.type === "empty" ? t("knowledge.emptyEntity")
      : [c.children ? `${t("knowledge.nodes")} ${c.children}` : "",
         read && enter ? t("knowledge.hasBody") : ""].filter(Boolean).join(" · ");
    return {
      key: c.fetch || c.id, id: c.id, label: c.name || c.id, kind: read && !enter ? "data" : "as",
      address: c.fetch, node: enter ? c.id : null, ownerRegion: areaKey, level, holder, pickable: true,
      // Whose backbone this row belongs to, carried down from the area key. A row from a linked
      // one still opens and still reads; what it must not do is move, because a move is a write
      // and writes go to the backbone that owns the area.
      peer: String(areaKey).includes(":") ? String(areaKey).split(":")[0] : null,
      badge: enter ? (counts || t("knowledge.relOnly")) : "", shape,
    };
  }
  const noteFor = (tiles) =>
    `${t("knowledge.files")} ${tiles.filter((x) => canReadShape(x.shape)).length} · ${t("knowledge.nodes")} ${tiles.filter((x) => x.shape !== "host").length}`;

  const btnW = (a) => (a.icon ? 34 : textWidth(a.label) + 40);

  /** How big a rack wants to be, and where its header buttons land.
   *
   *  Width is columns first — a rack is as wide as the tiles it holds. With a single area open the
   *  header still forces the width, exactly as it did before there could be a second one, so nothing
   *  about the one-rack screen moves. With more than one open, five action buttons in a row are some
   *  650px and two racks of that will not sit side by side, so the buttons wrap instead and the width
   *  drops to the tile grid. One row of buttons leaves `headH` at the 50 it has always been. */
  function rackMetrics(tiles, { title, note, actions, cap, wrap }) {
    const cols = Math.min(cap || RACK.cols, Math.max(tiles.length, 4));
    const innerW = cols * DEV.host.w + (cols - 1) * RACK.gap;
    const acts = actions || [];
    // The kind in the small letter-spaced face, the name larger and bold.
    // Measured, not counted. The line beside this one already knew a CJK glyph is nearly twice as
    // wide; this one multiplied character count by a fixed number, so a Korean or Japanese name came
    // out about 28% short — and this width is exactly what stops the header colliding with its own
    // buttons, the collision the comment below describes.
    const titleW = textWidth(t("knowledge.asTitle"), 7.8) + textWidth(title + "   ", 9) + 24;
    const barW = acts.reduce((n, a) => n + btnW(a) + 14, 0);
    const headW = RACK.pad + titleW + barW + textWidth(note) + RACK.pad + 20;
    const bareW = RACK.pad + titleW + textWidth(note) + RACK.pad + 20;
    const w = Math.max(innerW + RACK.pad * 2, wrap ? bareW : headW);
    // Flow the buttons. The first row starts after the title and stops short of the count — that is
    // the collision the old single-line header had to be made wide enough to avoid; later rows have
    // the full inner width.
    const rows = [];
    let cur = { x: RACK.pad + titleW, items: [] };
    for (const a of acts) {
      const bw = btnW(a);
      const limit = w - RACK.pad - (rows.length ? 0 : textWidth(note) + 14);
      if (cur.x + bw > limit && cur.x > RACK.pad) { rows.push(cur); cur = { x: RACK.pad, items: [] }; }
      cur.items.push({ a, x: cur.x, bw });
      cur.x += bw + 14;
    }
    if (cur.items.length || !rows.length) rows.push(cur);
    const headH = RACK.head + (rows.length - 1) * 36;
    const tileRows = Math.max(Math.ceil(tiles.length / cols), 1);
    return { cols, w, headH, rows, h: headH + tileRows * 50 + (tileRows - 1) * RACK.gap + RACK.pad * 2 - 10 };
  }

  /** A rack: tiles in a grid inside a titled box, drawn where `draw` decided it goes. Returns the
   *  group plus where its bottom is and where a given tile's uplink port is, for a sub-rack. */
  function rackBox(tiles, { title, note, left, top, sub, metrics, openNode, drop }) {
    const { cols, w, h, headH, rows } = metrics;
    const tileH = 50;
    const g = svgEl("g", { class: "kn-rack" + (sub ? " is-sub" : "") });
    if (drop) dropAttrs(g, drop.id, drop.area, drop.chain, drop.label);
    g.append(svgEl("rect", { x: left, y: top, width: w, height: h, rx: 10 }));
    g.append(svgEl("line", { x1: left, y1: top + headH, x2: left + w, y2: top + headH, class: "kn-rack-rule" }));
    const tt = svgEl("text", { x: left + RACK.pad, y: top + 27, class: "kn-rack-title" });
    // "Autonomous System [library]": the kind quiet, the name the thing to read (operator, 2026-09-11).
    const kind = svgEl("tspan", { class: "kn-rack-kind" });
    kind.textContent = `${t("knowledge.asTitle")} `;
    const name = svgEl("tspan", { class: "kn-rack-name" });
    name.textContent = `[${title}]`;
    tt.append(kind, name);
    g.append(tt);
    const nt = svgEl("text", { x: left + w - RACK.pad, y: top + 27, class: "kn-rack-note", "text-anchor": "end" });
    nt.textContent = note;
    g.append(nt);
    // Header buttons. Small, rounded, keyboard-reachable — the same affordance as a device so a person
    // does not have to learn a second kind of thing to click.
    rows.forEach((row, ri) => {
      for (const it of row.items) {
        const b = svgEl("g", { class: "kn-rack-btn" + (it.a.primary ? " is-primary" : "") + (it.a.flag ? " is-flag" : "") + (it.a.danger ? " is-danger" : ""), tabindex: "0", role: "button" });
        const by = top + 7 + ri * 36;
        b.append(svgEl("rect", { x: left + it.x, y: by, width: it.bw, height: 28, rx: 14 }));
        if (it.a.icon) {
          // Named for a screen reader and a hover, since there is no word on it.
          b.setAttribute("aria-label", it.a.label);
          const tip = svgEl("title", {});
          tip.textContent = it.a.label;
          b.append(tip, trashIcon(left + it.x + it.bw / 2, by + 14));
        } else {
          const tx = svgEl("text", { x: left + it.x + it.bw / 2, y: by + 18, "text-anchor": "middle" });
          tx.textContent = it.a.label;
          b.append(tx);
        }
        const fire = (e) => { e.stopPropagation(); it.a.run(); };
        b.addEventListener("click", fire);
        b.addEventListener("keydown", (e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); fire(e); } });
        g.append(b);
      }
    });
    const anchors = new Map();
    let anchorY = null;
    if (!tiles.length) {
      const e = svgEl("text", { x: left + w / 2, y: top + headH + 30, class: "kn-rack-note", "text-anchor": "middle" });
      e.textContent = t("knowledge.noFiles");
      g.append(e);
    }
    tiles.forEach((tile, i) => {
      const c = i % cols, r = Math.floor(i / cols);
      const tx = left + RACK.pad + c * (DEV.host.w + RACK.gap) + DEV.host.w / 2;
      const ty = top + headH + RACK.pad - 8 + r * (tileH + RACK.gap) + DEV[tile.shape].h / 2;
      g.append(device(tile, tx, ty, tile.shape, drop ? { area: drop.area, chain: drop.chain } : null));
      if (tile.node) { anchors.set(tile.node, tx); if (tile.node === openNode) anchorY = ty + DEV[tile.shape].h / 2; }
    });
    return { g, top, bottom: top + h, anchorFor: (id) => anchors.get(id), anchorY };
  }


  /** A bin, centred on (cx, cy), drawn in strokes so it takes the button's colour. */
  function trashIcon(cx, cy) {
    const g = svgEl("g", { class: "kn-rack-icon", transform: `translate(${cx - 8} ${cy - 8})` });
    g.append(svgEl("path", { d: "M2.5 4.5h11M6 4.5V3.2a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v1.3M4 4.5l.7 8.6a1.4 1.4 0 0 0 1.4 1.3h3.8a1.4 1.4 0 0 0 1.4-1.3l.7-8.6M6.8 7v4.6M9.2 7v4.6" }));
    return g;
  }

  function fitted(text, boxWidth) {
    const max = Math.floor((boxWidth - 14) / 7.1);
    const s = String(text || "");
    return s.length <= max ? s : `${s.slice(0, max - 1)}…`;
  }

  /** One device. The shape says the tier — core router, management host, distribution switch, access
   *  switch, host — and the port strip on a switch is the visual claim that things hang off it. */
  function device(row, x, y, shape, place) {
    const selected = state.selected
      && ((shape === "core" && state.selected.kind === "bb") || (state.selected.address && state.selected.address === row.address));
    const { w, h } = DEV[shape];
    const pending = row.flagKey ? flagsFor(row.flagKey).length : 0;
    const picked = Boolean(row.address && state.picked.has(row.address));
    const g = svgEl("g", { class: `kn-dev is-${shape} is-${row.kind}${selected ? " is-sel" : ""}${row.node && pathIn(row.ownerRegion).includes(row.node) ? " is-open" : ""}${place && row.id && !row.peer ? " is-movable" : ""}${pending ? " is-flagged" : ""}${picked ? " is-picked" : ""}${vrfClass(row, shape)}`, tabindex: "0", role: "button" });
    g.append(svgEl("rect", { x: x - w / 2, y: y - h / 2, width: w, height: h, rx: shape === "core" ? 10 : 5 }));
    if (shape === "as" || shape === "sw" || shape === "leaf") {
      // Port strip along the bottom edge. A leaf has few ports on purpose: one file is in it, room for more.
      const n = shape === "as" ? 8 : shape === "sw" ? 6 : 3, pw = 8, gap = 4, total = n * pw + (n - 1) * gap;
      for (let i = 0; i < n; i++) {
        g.append(svgEl("rect", { x: x - total / 2 + i * (pw + gap), y: y + h / 2 - 8, width: pw, height: 4, rx: 1, class: "kn-port" }));
      }
    }
    if (shape === "host") g.append(svgEl("circle", { cx: x - w / 2 + 11, cy: y, r: 2.6, class: "kn-led" }));
    // Selecting an area for a run is a different act from opening it, so it gets its own target rather
    // than a mode the whole map is in. The questions that cost the most hops need two areas at once —
    // CDN and UpdateSystem, orchestration and the game server — so this is a set, not a radio button.
    if (row.pickable && row.address && canPick()) {
      const on = state.picked.has(row.address);
      // An area's box sits bottom-left, clear of its flag; a tile's sits top-right, clear of its LED.
      const px = shape === "as" ? x - w / 2 + 13 : x + w / 2 - 11;
      const py = shape === "as" ? y + h / 2 - 4 : y - h / 2 + 10;
      const box = svgEl("g", { class: "kn-pick" + (on ? " is-on" : ""), tabindex: "0", role: "checkbox", "aria-checked": String(on) });
      box.append(svgEl("rect", { x: px - 6, y: py - 6, width: 12, height: 12, rx: 3 }));
      if (on) box.append(svgEl("path", { d: `M ${px - 3} ${py} L ${px - 1} ${py + 3} L ${px + 3.5} ${py - 3.5}`, class: "kn-pick-tick" }));
      const toggle = (e) => {
        e.stopPropagation();
        if (state.picked.has(row.address)) state.picked.delete(row.address); else state.picked.add(row.address);
        draw();
      };
      box.addEventListener("click", toggle);
      box.addEventListener("keydown", (e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); toggle(e); } });
      g.append(box);
    }
    // The count sits on the device, not in a legend: "this Region has two requests waiting" is the
    // whole notification, and it must be readable without opening anything.
    if (pending) {
      const bx = x + w / 2 - 13, by = y - h / 2 + 12;
      g.append(svgEl("circle", { cx: bx, cy: by, r: 9, class: "kn-flag-dot" }));
      const n = svgEl("text", { x: bx, y: by + 3.5, class: "kn-flag-count", "text-anchor": "middle" });
      n.textContent = String(pending);
      g.append(n);
    }
    const label = svgEl("text", { x: shape === "host" ? x + 6 : x, y: shape === "core" ? y - 4 : (shape === "as" || shape === "sw" || shape === "leaf") ? y - 1 : y + 4, class: "kn-dev-title", "text-anchor": "middle" });
    label.textContent = fitted(row.label, w - (shape === "host" ? 18 : 0));
    g.append(label);
    if (shape === "core") {
      const sub = svgEl("text", { x, y: y + 14, class: "kn-dev-sub", "text-anchor": "middle" });
      // A peer's device says what the *link* is, not what this ontology holds. Printing the local
      // counts under somebody else's name is the map telling a lie in the smallest possible type.
      // What is knowable from here is how many areas it advertises, and whether it answered.
      sub.textContent = row.peer
        ? (row.link && row.link.reachable === false
            ? t("knowledge.peer.down")
            : tv("knowledge.peer.up", { as: (row.link && row.link.areas) || 0,
                                        rev: String((row.link && row.link.revision) || "").slice(0, 7) }))
        : tv("knowledge.counts", { as: state.regions.filter((r) => !r.peer).length, nodes: state.nodes.length });
      g.append(sub);
    }
    if (row.badge) {
      const b = svgEl("text", { x, y: y + h / 2 + 12, class: "kn-dev-badge", "text-anchor": "middle" });
      b.textContent = fitted(row.badge, w + 20);
      g.append(b);
    }
    // Anything in a rack can be picked up; a node can also be landed on. A document cannot be landed
    // on: that would make a document into a holder, and making holders is "+ New node".
    // Not for a row on another backbone: dragging one is a move, a move is a write, and the far end
    // refuses it. Nor a drop target, for the same reason pointed the other way — nothing of ours
    // belongs inside somebody else's area.
    if (place && row.id && !row.peer) {
      g.addEventListener("pointerdown", (e) => pressTile(e, row, g));
      if (row.node) dropAttrs(g, row.node, place.area, [...place.chain, row.node], row.label);
    }
    const run = () => {
      if (justDragged) return;           // the click that ends a drag is not a click on the tile
      // A peer's backbone is not this one's transcript. Until there is something to show for a link —
      // what it advertises, when it was last read — pressing it does nothing, rather than opening the
      // local backbone's document under somebody else's name.
      if (shape === "core" && row.peer) return;
      if (shape === "core") return showRaw({ kind: "bb", title: "RouteMind Back-Bone", address: "" });
      if (shape === "host" || shape === "mgmt") return showRaw({ kind: row.kind, title: row.label, address: row.address });
      // A switch opens what hangs off it — a rack — and nothing else. The routing table the agent is
      // handed at that step is a button on that rack: opening it on every click meant closing a popup
      // every time a person only wanted to see the members.
      // At any depth: opening a node closes what was open at its own level and below, and leaves the
      // levels above it alone.
      if (shape === "sw" || shape === "leaf") {
        const path = pathIn(row.ownerRegion), k = row.level || 0;
        if (path[k] === row.node) { setPath(row.ownerRegion, path.slice(0, k)); draw(); return; }
        setPath(row.ownerRegion, [...path.slice(0, k), row.node]);
        loadFiles(row.node);
        return;
      }
      // Closing takes its sub-rack with it; opening leaves every other area exactly where it was.
      if (isOpen(row.key)) {
        state.open = state.open.filter((k) => k !== row.key);
        state.openNode.delete(row.key);
        draw();
        return;
      }
      openArea(row.key);
      if (!state.entries.has(row.key)) loadEntries(row.key).then(draw); else draw();
    };
    g.addEventListener("click", run);
    g.addEventListener("keydown", (e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); run(); } });
    return g;
  }

  // ── overlays (docs/OVERLAY.md): a question's working set, drawn on the map ───
  //
  // An agent draws one through the API; a person draws one by ticking. The map draws both the same way.
  // Whether this install has overlays at all is asked, not assumed: 404 or 501 means no, and then there
  // are no chips, no highlights and no "Draw VRF" — the screen is what it was before overlays existed.
  const shortAddr = (a) => String(a || "").replace(/\/body$/, "").split("/").pop();

  async function loadOverlays() {
    try {
      const d = await request("overlays?state=open");
      state.vrfOn = true;
      state.overlays = d.overlays || [];
    } catch (error) {
      if (error.status === 404 || error.status === 501) state.vrfOn = false;
      state.overlays = [];
    }
    if (state.vrfSel && !state.overlays.some((o) => o.id === state.vrfSel)) state.vrfSel = null;
  }

  /** The area an overlay member lives in — for an area itself, and for anything the graph knows. */
  function memberArea(address) {
    const a = String(address || "");
    let m = /^\/v1\/regions\/([a-z0-9-]+)$/.exec(a);
    if (m) return m[1];
    m = /^\/v1\/nodes\/([a-z0-9][a-z0-9-]*)(?:\/body)?$/.exec(a);
    const n = m ? state.nodes.find((x) => x.id === m[1]) : null;
    return n ? norm(regionOf(n)) : "";
  }

  /** Members of the chosen overlay (or of every open one, when none is chosen) are outlined; an area
   *  switch holding a member is marked more lightly, so a closed rack still says "something in here". */
  function vrfClass(row, shape) {
    if (!state.overlays.length || !row.address) return "";
    const shown = state.vrfSel ? state.overlays.filter((o) => o.id === state.vrfSel) : state.overlays;
    const members = shown.flatMap((o) => (o.members || []).map((m) => m.address));
    if (members.includes(row.address)) return " is-vrf";
    if (shape === "as" && members.some((a) => memberArea(a) === row.key)) return " is-vrf-in";
    return "";
  }

  /** The dialog, set up for something that is not an address in the ontology. */
  function dialogFor({ chip, title, address, meta }) {
    const c = $("knRawKind");
    c.textContent = chip;
    c.className = "kn-chip-kind is-vrf";
    $("knRawTitle").textContent = title;
    $("knRawAddr").textContent = address || "";
    $("knRawPath").textContent = "";
    $("knRawMeta").textContent = meta || "";
    banner("");
  }

  /** A person's VRF. The question is required from a person as from an agent: it is what makes the
   *  overlay worth keeping, and a field whose rules depend on who is calling rots. */
  function drawVrfCard() {
    const members = [...state.picked];
    state.selected = { kind: "vrf", address: "" };
    dialogFor({ chip: "VRF", title: t("knowledge.vrf.title"), address: "", meta: "" });
    const card = el("form", "kn-card-form");
    card.addEventListener("submit", (e) => e.preventDefault());
    card.append(el("p", "kn-cf-lead", t("knowledge.vrf.lead")));
    const list = el("div", "kn-chiprow");
    for (const a of members) list.append(el("span", "kn-chip", a));
    const box = el("div", "kn-facts");
    box.append(el("span", "kn-fact-k", t("knowledge.vrf.members")));
    const cell = el("span", "kn-fact-v");
    cell.append(list);
    box.append(cell);
    card.append(box);
    const question = input("", { placeholder: t("knowledge.vrf.questionHint") });
    const why = input("", { placeholder: t("knowledge.vrf.whyDefault") });
    card.append(labelled("knowledge.vrf.question", question));
    card.append(labelled("knowledge.vrf.why", why));
    card.append(actions(
      button("common.cancel", "quiet", () => $("knRawDialog").close()),
      button("knowledge.vrf.create", "primary", (b) => guarded(b, async () => {
        if (!question.value.trim()) throw new Error(t("knowledge.vrf.needsQuestion"));
        const reason = why.value.trim() || t("knowledge.vrf.whyDefault");
        const made = await send("overlays", "POST", {
          question: question.value.trim(), by: { kind: "person" },
          members: members.map((address) => ({ address, why: reason })),
        });
        state.picked.clear();
        await loadOverlays();
        state.vrfSel = String(made?.id || "") || null;
        $("knRawDialog").close();
        draw();
      }, "knowledge.vrf.drawn")),
    ));
    $("knEdit").replaceChildren(card);
    showEditor(true);
    const dialog = $("knRawDialog");
    if (!dialog.open) dialog.showModal();
    question.focus();
  }

  /** One overlay: the question, what is in it and why, and how it got there. Choosing it also makes
   *  it the one the map outlines. */
  async function showOverlay(ov) {
    state.vrfSel = ov.id;
    state.selected = { kind: "vrf", address: "" };
    draw();
    let full = ov;
    try { full = await request("overlays/" + encodeURIComponent(ov.id)); } catch { /* the list's copy will do */ }
    const by = full.by || {};
    dialogFor({ chip: "VRF", title: full.question || full.id, address: `/v1/overlays/${full.id}`,
                meta: [by.kind, by.name, full.state].filter(Boolean).join(" · ") });
    const card = el("div", "kn-card-form");
    const facts = el("div", "kn-facts");
    for (const m of full.members || []) {
      facts.append(el("span", "kn-fact-k", shortAddr(m.address)));
      const v = el("span", "kn-fact-v");
      v.append(el("code", null, m.address), el("span", "kn-fact-n", m.why || ""));
      facts.append(v);
    }
    card.append(el("h3", "kn-cf-title", t("knowledge.vrf.members")));
    card.append(facts);
    // The table the agent works from, in the words it is handed — rendered by the MCP server's own
    // function, as every other popup on this screen is.
    try {
      const view = await request("view?" + new URLSearchParams({ path: `/v1/overlays/${full.id}` }).toString());
      card.append(el("h3", "kn-cf-title", t("knowledge.vrf.handed")));
      card.append(el("pre", "kn-upload-preview", view.text || ""));
    } catch { /* the members above are the same facts, less formatted */ }
    if ((full.trail || []).length) {
      card.append(el("h3", "kn-cf-title", t("knowledge.vrf.trail")));
      const pre = el("pre", "kn-upload-preview");
      pre.textContent = full.trail.map((x) => `${when(x.at)}  ${String(x.op || "").padEnd(6)}  ${x.address || ""}  — ${x.why || ""}`).join("\n");
      card.append(pre);
    }
    card.append(actions(button("common.close", "primary", () => $("knRawDialog").close())));
    $("knEdit").replaceChildren(card);
    showEditor(true);
    const dialog = $("knRawDialog");
    if (!dialog.open) dialog.showModal();
  }

  // ── moving an entity: drag it onto what should hold it ─────────────────────
  //
  // Containment is one field, `parent`, and the routing tables are read off it — an area's table is
  // its representative's children, a node's table is its own. So a move is one write of that field,
  // and both tables change with it: the one it left and the one it joined. The entity keeps its id,
  // its address, its body and its edges; whatever is inside it comes along, because each of those
  // names it as parent and it did not change.
  //
  // Where it can land: its area's rack (the representative holds it), a sub-rack (that node holds
  // it), or a node's tile. Not a document, not itself or anything inside it, and not another area —
  // Knowledge refuses a parent in another area, because a relation across areas is an edge.
  const DRAG_START_PX = 6;
  let drag = null;
  let justDragged = false;

  function dropAttrs(g, id, area, chain, label) {
    g.setAttribute("data-drop", id);
    g.setAttribute("data-area", area);
    g.setAttribute("data-chain", chain.join(" "));
    g.setAttribute("data-label", label || id);
  }
  const dropSpots = () => [...$("knTopo").querySelectorAll("[data-drop]")];
  /** ok · same (already held there) · loop (into itself). Another area is offered like any other
   *  place (operator, 2026-09-11); whether Knowledge takes it is Knowledge's answer, shown as given. */
  function dropVerdict(spot, row) {
    if ((spot.getAttribute("data-chain") || "").split(" ").includes(row.id)) return "loop";
    if (spot.getAttribute("data-drop") === row.holder) return "same";
    return "ok";
  }

  function pressTile(e, row, g) {
    if (e.button !== 0 || !row.id) return;
    drag = { row, g, x0: e.clientX, y0: e.clientY, started: false, over: null, ghost: null };
  }

  function dragMove(e) {
    if (!drag) return;
    if (!drag.started) {
      // A click wobbles. Below this distance it is still a click and opens the tile as it always did.
      if (Math.hypot(e.clientX - drag.x0, e.clientY - drag.y0) < DRAG_START_PX) return;
      drag.started = true;
      document.body.classList.add("kn-dragging");
      drag.g.classList.add("is-dragging");
      for (const spot of dropSpots()) if (dropVerdict(spot, drag.row) === "ok") spot.classList.add("is-drop-ok");
      drag.ghost = el("div", "kn-drag-ghost");
      drag.ghost.append(el("span", null, drag.row.label), el("span", "kn-drag-to", t("knowledge.move.hint")));
      document.body.append(drag.ghost);
    }
    e.preventDefault();
    drag.ghost.style.left = `${e.clientX}px`;
    drag.ghost.style.top = `${e.clientY}px`;
    const hit = document.elementFromPoint(e.clientX, e.clientY)?.closest?.("[data-drop]") || null;
    if (hit === drag.over) return;
    drag.over?.classList.remove("is-drop-hover");
    drag.over = hit;
    const verdict = hit ? dropVerdict(hit, drag.row) : null;
    if (verdict === "ok") hit.classList.add("is-drop-hover");
    drag.ghost.classList.toggle("is-ok", verdict === "ok");
    drag.ghost.lastChild.textContent = !hit ? t("knowledge.move.hint")
      : verdict === "ok" ? t("knowledge.move.into").replace("{target}", hit.getAttribute("data-label"))
      : t(`knowledge.move.no.${verdict}`);
  }

  function dragEnd(e) {
    if (!drag) return;
    const d = drag;
    drag = null;
    if (!d.started) return;
    justDragged = true;
    setTimeout(() => { justDragged = false; }, 0);
    document.body.classList.remove("kn-dragging");
    d.ghost?.remove();
    d.g.classList.remove("is-dragging");
    for (const spot of dropSpots()) spot.classList.remove("is-drop-ok", "is-drop-hover");
    if (e.type !== "pointerup" || !d.over) return;
    if (dropVerdict(d.over, d.row) === "ok") {
      confirmMove(d.row, d.over.getAttribute("data-drop"), d.over.getAttribute("data-label"), d.over.getAttribute("data-area"));
    }
  }

  /** Where something sits, in words: the area alone when its representative holds it. */
  const placeOf = (area, id) => (id && id !== representativeOf(area) ? `${area}  ▸  ${id}` : area);

  /** A move is a commit that every agent reads on its next run, and a drop is easy to make by
   *  accident — so it asks, once, saying from where to where (operator, 2026-09-11). */
  function confirmMove(row, to, toLabel, toArea) {
    state.selected = { kind: row.kind, address: row.address };
    const target = editTarget(row.address);
    const chip = $("knRawKind");
    chip.textContent = (OBJECT[target.kind] || OBJECT.node).label;
    chip.className = `kn-chip-kind is-${target.kind}`;
    $("knRawTitle").textContent = t("knowledge.move.title").replace("{name}", row.label);
    $("knRawAddr").textContent = row.address || "";
    $("knRawPath").textContent = "";
    $("knRawMeta").textContent = "";
    banner("");
    const card = el("form", "kn-card-form");
    card.addEventListener("submit", (e) => e.preventDefault());
    card.append(el("p", "kn-cf-lead", t("knowledge.move.lead")));
    const facts = el("div", "kn-facts");
    for (const [k, v] of [["knowledge.move.from", placeOf(row.ownerRegion, row.holder)], ["knowledge.move.to", placeOf(toArea, to)]]) {
      facts.append(el("span", "kn-fact-k", t(k)));
      const cell = el("span", "kn-fact-v");
      cell.append(el("code", null, v));
      facts.append(cell);
    }
    card.append(facts);
    if (toArea !== row.ownerRegion) {
      card.append(el("p", "kn-fnote", t("knowledge.move.crossArea").replace("{from}", row.ownerRegion).replace("{to}", toArea)));
    }
    card.append(actions(
      button("common.cancel", "quiet", () => $("knRawDialog").close()),
      button("knowledge.move.go", "primary", (b) => guarded(b, async () => {
        await send("nodes/" + encodeURIComponent(row.id), "PUT", { parent: to });
        forgetOpen(row.id);               // its sub-rack hung under the holder it just left
        $("knRawDialog").close();
        await refreshFromKnowledge();
        toast(t("knowledge.move.done").replace("{name}", row.label).replace("{target}", toLabel));
      })),
    ));
    $("knEdit").replaceChildren(card);
    showEditor(true);
    const dialog = $("knRawDialog");
    if (!dialog.open) dialog.showModal();
  }

  // ── loading: draw what is needed, when it is needed, and remember it by revision ────────────
  //
  // The first paint needs two things: the Region list and the graph. It used to also wait for every
  // Region's entries — seven more calls — before drawing anything, and nothing on a fresh screen is
  // open, so none of those seven were drawn. Worse, the ontology API answers seven concurrent calls
  // slower than seven sequential ones (measured 4.1 s vs 1.4 s on 2026-09-09; contention inside the
  // store), so the wait was long and the parallelism made it longer. Now: paint on two calls, fetch a
  // Region's entries the first time it is opened, and warm the rest one at a time in the background.
  //
  // The cache key is the published revision. It is already the identity of what the agent reads, it is
  // 2 ms to ask for, and the watcher already tracks it — so a revisit at the same revision draws from
  // localStorage with one request, and a revisit at a new one refetches. Nothing is invented for the
  // key and nothing can be served stale past a revision change.
  const CACHE_KEY = "iris.knowledge.map";

  function readCache(published) {
    try {
      const raw = JSON.parse(localStorage.getItem(CACHE_KEY) || "null");
      if (!raw || raw.published !== published) return null;
      return raw;
    } catch { return null; }
  }
  function writeCache() {
    if (!drawnRevision) return;
    try {
      localStorage.setItem(CACHE_KEY, JSON.stringify({
        published: drawnRevision, savedAt: Date.now(),
        // Local areas only. A peer's rows are not this backbone's to remember: the API drops them the
        // moment a link cannot be read, and a cache that keeps them puts them straight back — so a
        // dead link draws exactly like a live one, which is the failure the whole absence rule turns
        // on. They come back on the refresh below, from the wire, or they do not come back.
        regions: state.regions.filter((r) => !r.peer),
        nodes: state.nodes, edges: state.edges, service: state.service,
        entries: [...state.entries.entries()],
      }));
    } catch { /* quota or private mode: the cache is a convenience, the fetch path still works */ }
  }

  async function loadMap() {
    // One cheap question first: which revision is this? It decides whether the cache is usable, and it
    // seeds the watcher so its first tick is quiet.
    let published = "";
    try { published = String((await request("revision")).published || ""); } catch { /* fall through to fetch */ }
    const cached = published ? readCache(published) : null;
    if (cached) {
      state.regions = cached.regions || [];
      state.links = [];
      state.nodes = cached.nodes || [];
      state.edges = cached.edges || [];
      state.service = cached.service || "";
      state.entries = new Map(cached.entries || []);
      drawnRevision = published;
      draw();
      // Flags are never cached: a request that arrived while this tab was closed is exactly the one
      // worth seeing, and they cost one call.
      loadFlags().then(draw);
      loadOverlays().then(draw);
      // Nor is anything across a link. The cached map is this backbone's own areas, which are as good
      // as the revision they were saved at; whether a peer is answering *right now* is not something
      // a saved picture can know, and drawing a link that is down as though it were up is the one
      // mistake this picture must not make.
      request("regions").then((fresh) => {
        state.regions = [...state.regions.filter((r) => !r.peer), ...(fresh.regions || []).filter((r) => r.peer)];
        state.links = fresh.links || [];
        // From here too, or a tab that opened on a cached map shows a dash where every other card
        // shows a revision — which reads as "unknown" rather than as "this one is ours". The
        // repository head and not the published one: the head is what the map is drawn from, and the
        // two differ exactly when a publish has failed.
        state.revision = fresh.revision || null;
        draw();
      }).catch(() => {});
      return;
    }
    const [regions, graph] = await Promise.all([request("regions"), request("graph")]);
    state.regions = regions.regions || [];
    // Never cached, for the reason flags are not: whether a link is up is the thing worth seeing now,
    // and a cached "reachable" is a picture of a link that may have gone since.
    state.links = regions.links || [];
    // This backbone's own revision, for its card on the wall. Every other card carries the one that
    // came with the advertisement, and a card that showed a dash where the others show a revision
    // would read as "unknown" rather than as "this one is ours".
    state.revision = regions.revision || null;
    state.nodes = graph.nodes || [];
    state.edges = graph.edges || [];
    state.entries = new Map();
    if (published) drawnRevision = published;
    draw();                                   // first paint: two calls in
    loadFlags().then(draw);                   // notifications arrive after the map, never gating it
    loadOverlays().then(draw);                // so do overlays, and an install without them answers 404
    try {
      const frag = await request("services").catch(() => ({}));
      state.services = (frag.services || []).map((x) => String(x.id || x.service || "")).filter(Boolean);
      state.service = state.services[0] || "";
      draw();
    } catch { state.service = ""; state.services = []; }
    warmEntries();
  }

  /** Entries for one Region — `entries[]` is files and children as one list, each row carrying its own
   *  `type` and `fetch`. Fetched on first open; cached in memory and, once all are in, on disk. */
  /** Where an area's own table lives, from its key alone.
   *
   *  A local area is keyed by its directory; an area on a linked backbone by `<peer>:<dir>`, which can
   *  be taken apart again because a directory name is ASCII kebab-case and cannot hold a colon.
   *  Deriving it here rather than threading an address through every caller keeps the three call
   *  sites — opening a rack, warming the ones nobody opened, redrawing after a change — from each
   *  having to know that some areas are somewhere else.
   *
   *  Before this they rebuilt `regions/<key>`, so a peer's area asked for `regions/branch:payroll`,
   *  got a 404, and opened as an empty rack: the map drew an area you could see and could not open. */
  const entriesPath = (key) => {
    const at = String(key).indexOf(":");
    return at < 0
      ? "regions/" + encodeURIComponent(key)
      : `peers/${encodeURIComponent(key.slice(0, at))}/regions/${encodeURIComponent(key.slice(at + 1))}`;
  };

  async function loadEntries(key) {
    if (state.entries.has(key)) return state.entries.get(key);
    try {
      const detail = await request(entriesPath(key));
      state.entries.set(key, detail.entries || []);
    } catch { state.entries.set(key, []); }
    return state.entries.get(key);
  }

  /** Warm the Regions nobody has opened yet, one at a time — the API is faster that way — and only
   *  while the tab is visible. A Region opened in the meantime is fetched on its own and skipped here.
   *  When the set is complete the whole map goes to the cache. */
  let warming = false;
  async function warmEntries() {
    if (warming) return;
    warming = true;
    try {
      for (const r of state.regions) {
        const key = norm(r.source);
        if (state.entries.has(key)) continue;
        if (document.visibilityState === "hidden") { warming = false; return; }
        await loadEntries(key);
        if (isOpen(key)) draw();
      }
      writeCache();
    } finally { warming = false; }
  }

  /** What a node holds, from its table — every row, documents and nodes alike, each with its own
   *  `type`. It kept documents only while a node could not be put inside a node from this screen; a
   *  node dragged into one then disappeared from the map. */
  async function loadFiles(nodeId) {
    if (state.files.has(nodeId)) return draw();
    try {
      const node = await request("nodes/" + encodeURIComponent(nodeId));
      state.files.set(nodeId, (node.entries || []).filter((e) => e.fetch));
    } catch { state.files.set(nodeId, []); }
    draw();
  }

  /** The bar says something only when something is wrong (operator, 2026-09-11). Every write already
   *  validates and publishes in one step, so in the ordinary state there is nothing to do: a revision
   *  hash and two buttons were a bar of nothing. What can go wrong without a write noticing is the
   *  repository being changed by hand — uncommitted (every write is refused), committed but not
   *  published (agents read the older tree), or no longer valid — and then the bar appears with the
   *  one button that fixes it. */
  async function loadState() {
    const row = $("knState");
    const problems = [];
    let behind = false, invalid = false;
    try {
      const s = await request("state");
      if (s.writable === false) problems.push([t("knowledge.state.readOnly"), String(s.uncommitted || "")]);
      // A link that is up and not doing what somebody thinks it is doing. This belongs in the bar and
      // an open door does not: nothing here is a deployment choice, it is a line in a file that has
      // stopped an audience and a per-peer line from having any effect, with everything still
      // looking fine from every screen.
      for (const l of state.links || []) {
        if (l.note) problems.push([`${l.label || l.name}: ${l.note}`, ""]);
      }
      const ps = await request("publish-state");
      behind = (ps.core || {}).in_sync === false;
      invalid = (ps.validate || {}).ok === false;
      if (behind) problems.push([t("knowledge.behindLong"), ""]);
      if (invalid) problems.push([t("knowledge.validBad"), ""]);
    } catch (error) {
      problems.push([t("knowledge.stateUnknown"), error.message]);
    }
    row.replaceChildren(...problems.map(([k, v]) => {
      const item = el("span", "kn-state-item is-stuck", k);
      if (v) item.append(el("strong", null, v));
      return item;
    }));
    // Publishing a tree that fails validation is refused anyway, so it is not offered then.
    $("knPublish").hidden = !behind || invalid;
    $("knValidate").hidden = !invalid;
    $("knBar").hidden = problems.length === 0;
  }


  // ── making things at the backbone ─────────────────────────────────────────
  //
  // The backbone holds three kinds of thing: the Regions, the Core document, and the service
  // fragments. Two of them can be created through the API and one cannot — `POST /v1/regions` answers
  // 405, because a Region exists only when its directory and representative node do (SPEC-v2 §1.1), so
  // creating one is not a write this screen can compose. That is said out loud below rather than left
  // as a missing button: a person who finds no way to add an AS should learn why, not guess.

  /** A file in a service fragment. The owner writes it in their own format — YAML or Markdown, both
   *  are read — so the surface stays plain: a name, the one line that goes into the fragment's table,
   *  and the body. The description is typed here rather than derived, because unlike a node's file
   *  this is the owner's own channel and nothing else describes it. */
  function newServiceFileForm(service) {
    const card = el("form", "kn-card-form");
    card.addEventListener("submit", (e) => e.preventDefault());
    card.append(el("h3", "kn-cf-title", t("knowledge.bb.newServiceFile")));
    card.append(el("p", "kn-cf-lead", `/v1/services/${service}`));
    const name = input("", { placeholder: "release.yaml" });
    const desc = input("", { maxlength: 300, placeholder: t("knowledge.oneLinerHint") });
    const body = area("", 16);
    card.append(labelled("knowledge.field.name", name));
    card.append(labelled("knowledge.fileDesc", desc));
    card.append(uploadRow(body, name));
    card.append(labelled("knowledge.newFragmentFileHint", body));
    card.append(actions(
      button("common.cancel", "quiet", closeCard),
      button("knowledge.create", "primary", (b) => guarded(b, async () => {
        const fname = name.value.trim();
        if (!/^[^/\\.][^/\\]*\.(md|yaml|yml)$/i.test(fname) || fname === "INDEX.md") {
          throw new Error(t("knowledge.badFragmentName"));
        }
        if (!desc.value.trim()) throw new Error(t("knowledge.descRequired"));
        await send(`services/${encodeURIComponent(service)}/files/${encodeURIComponent(fname)}`, "PUT",
          { content: body.value, description: desc.value.trim() });
        await refreshFromKnowledge();
        await showRaw({ kind: "as", title: `svc · ${service}`, address: `/v1/services/${service}` });
      }, "knowledge.created")),
    ));
    $("knEdit").replaceChildren(card);
    showEditor(true);
    name.focus();
  }

  /** Why "add data" does nothing at the backbone yet. The backbone level holds exactly one authored
   *  document — CORE.md. The rest of what sits there is vocabulary or derived: `vocab.yaml`,
   *  `edges.yaml`, `regions.json`, `REVISION`. And CORE.md is one narrative that goes into every
   *  prompt whole, so it is edited a row at a time through the review queue rather than appended to.
   *  Until it is decided what "data at the backbone" should mean, the button says that instead of
   *  writing somewhere plausible. */
  function whyNoBBData() {
    const card = el("form", "kn-card-form");
    card.addEventListener("submit", (e) => e.preventDefault());
    card.append(el("h3", "kn-cf-title", t("knowledge.bb.noDataTitle")));
    card.append(el("p", "kn-cf-lead", t("knowledge.bb.noDataWhy")));
    card.append(actions(button("knowledge.done.ok", "primary", closeCard)));
    $("knEdit").replaceChildren(card);
    showEditor(true);
  }

  /** Removing an area, and everything the map can see inside it.
   *
   *  The API deletes an area in one transaction — directory, representative, the edges that named it
   *  and its CORE row — and refuses while anything else is still inside. That refusal is a feature,
   *  so this does not route around it: it shows what is in the way, and removes those one at a time
   *  only after a person has read the list and typed the name.
   *
   *  Each removal is its own commit, which is worth saying out loud: this looks irreversible and is
   *  not. A person who deletes the wrong area can `git revert` in `data/repo`.
   */
  /** Not while an Autonomous System is inside (operator, 2026-09-11). Documents go with what holds
   *  them; a system inside is somebody's structure, and it has to be taken apart — or moved out — on
   *  purpose, one level at a time. */
  function refuseDelete(name, held) {
    const card = el("form", "kn-card-form");
    card.addEventListener("submit", (e) => e.preventDefault());
    card.append(el("h3", "kn-cf-title", t("knowledge.del.title").replace("{area}", name)));
    card.append(el("p", "kn-cf-lead", t("knowledge.del.holdsAS").replace("{n}", String(held.length))));
    const list = el("div", "kn-chiprow");
    for (const x of held) list.append(el("span", "kn-chip", x));
    const box = el("div", "kn-uncovered");
    box.append(list);
    card.append(box);
    card.append(actions(button("common.close", "primary", closeCard)));
    $("knEdit").replaceChildren(card);
    showEditor(true);
  }

  async function deleteAreaCard(as, tiles) {
    const held = (tiles || []).filter((x) => x.node).map((x) => x.node);
    if (held.length) return refuseDelete(as.label, held);
    const card = el("form", "kn-card-form");
    card.addEventListener("submit", (e) => e.preventDefault());
    card.append(el("h3", "kn-cf-title", t("knowledge.del.title").replace("{area}", as.label)));
    card.append(el("p", "kn-cf-lead", t("knowledge.del.lead")));

    // Documents only, by now. They used to be skipped: this listed the tiles that were nodes, which
    // under two types was everything an area held besides its own files. Under one type a document
    // is an entity too, and the area delete that followed was refused with "nodes remain".
    const inside = (tiles || []).map((x) => x.id).filter(Boolean);
    const list = el("div", "kn-chiprow");
    for (const id of inside) list.append(el("span", "kn-chip", id));
    if (inside.length) {
      const box = el("div", "kn-uncovered");
      box.append(el("span", "kn-fact-k", t("knowledge.del.alsoGoes").replace("{n}", String(inside.length))));
      box.append(list);
      card.append(box);
    }
    card.append(el("p", "kn-fnote", t("knowledge.del.revertable")));

    // Typing the name is the whole guard. A confirm dialog is clicked through; a name has to be read.
    // These four strings are shared with `deleteNodeCard`, so none of them may say "area": deleting a
    // document read "If this was the wrong area", "Type the area's name" and "That is not the name of
    // this area" — three times naming the wrong kind of thing, on the one screen where a person has to
    // know exactly what they are about to destroy. The card's own title says what it is.
    const typed = input("", { class: "kn-input is-mono", spellcheck: "false", placeholder: as.label });
    card.append(labelled("knowledge.del.confirmLabel", typed,
      t("knowledge.del.confirmHint").replace("{name}", as.label)));

    const progress = el("p", "kn-fnote", "");
    card.append(progress);

    card.append(actions(
      button("common.cancel", "quiet", closeCard),
      button("knowledge.del.go", "danger", (b) => guarded(b, async () => {
        if (typed.value.trim() !== as.label) throw new Error(t("knowledge.del.nameMismatch"));
        // One at a time, and said out loud as it goes. A step that fails stops the rest and leaves a
        // real, valid state — each removal was its own commit — rather than a half-applied one.
        for (let i = 0; i < inside.length; i++) {
          progress.textContent = t("knowledge.del.removing")
            .replace("{n}", String(i + 1)).replace("{total}", String(inside.length)).replace("{id}", inside[i]);
          await send("nodes/" + encodeURIComponent(inside[i]), "DELETE");
        }
        progress.textContent = t("knowledge.del.removingArea");
        await send("regions/" + encodeURIComponent(as.key), "DELETE");
        state.open = state.open.filter((k) => k !== as.key);
        state.openNode.delete(as.key);
        $("knRawDialog").close();
        await refreshFromKnowledge();
        draw();
      }, "knowledge.del.done")),
    ));
    $("knEdit").replaceChildren(card);
    showEditor(true);
    typed.focus();
  }

  /** A new AS. Five things are asked for and every one of them is load-bearing, which is unusual on
   *  this screen and worth the extra fields: two of them are the only reason an agent will ever choose
   *  this area. `use_when` is the hop-0 condition and `core_description` becomes the CORE.md row behind
   *  it — an AS created without them is created invisible, and an empty slot meant to be filled later
   *  does not get filled. The id and the kind are Knowledge's to derive, as they are for a node.
   *
   *  The form shows the hop-0 row as it will read, because that row is the whole of what a run sees
   *  before it decides. Getting it wrong is not a typo; it is an area nobody visits. */
  /** Removing one node. Friction in proportion to what is lost: an empty node goes with one press,
   *  because there is nothing to lose; a node with things inside lists them and asks for the name
   *  typed out, because the API takes them with it. */
  async function deleteNodeCard(id) {
    const rec = await request("nodes/" + encodeURIComponent(id));
    const held = (rec.entries || []).filter(canEnter).map((e) => e.id);
    if (held.length) return refuseDelete(rec.name || id, held);
    const inside = (rec.entries || []).map((e) => e.id || e.name).filter(Boolean);
    const hasBody = Boolean(String(rec.body || "").trim());
    const lossy = inside.length > 0 || hasBody;

    const card = el("form", "kn-card-form");
    card.addEventListener("submit", (e) => e.preventDefault());
    card.append(el("h3", "kn-cf-title", t("knowledge.delNode.title").replace("{id}", rec.name || id)));
    card.append(el("p", "kn-cf-lead", lossy ? t("knowledge.delNode.lossy") : t("knowledge.delNode.empty")));
    if (inside.length) {
      const box = el("div", "kn-uncovered");
      box.append(el("span", "kn-fact-k", t("knowledge.del.alsoGoes").replace("{n}", String(inside.length))));
      const list = el("div", "kn-chiprow");
      for (const x of inside) list.append(el("span", "kn-chip", x));
      box.append(list);
      card.append(box);
    }
    if (hasBody) card.append(el("p", "kn-fnote", t("knowledge.delNode.bodyGoes")));
    card.append(el("p", "kn-fnote", t("knowledge.del.revertable")));
    const typed = input("", { class: "kn-input is-mono", spellcheck: "false", placeholder: id });
    if (lossy) card.append(labelled("knowledge.del.confirmLabel", typed, t("knowledge.del.confirmHint").replace("{name}", id)));

    card.append(actions(
      button("common.cancel", "quiet", closeCard),
      button("knowledge.del.go", "danger", (b) => guarded(b, async () => {
        if (lossy && typed.value.trim() !== id) throw new Error(t("knowledge.del.nameMismatch"));
        await send("nodes/" + encodeURIComponent(id), "DELETE");
        forgetOpen(id);
        $("knRawDialog").close();
        await refreshFromKnowledge();
        draw();
      }, "knowledge.del.done")),
    ));
    $("knEdit").replaceChildren(card);
    showEditor(true);
    if (lossy) typed.focus();
  }

  /** A new area. Two fields, and the second is the one that decides anything.
   *
   *  It asked for five. Three of them were measured against what an agent actually receives:
   *
   *    name            the address, and the title of the area's own table
   *    when to choose  the ONLY thing in the hop-0 row an agent picks by
   *    one-liner       the second half of that area's own header, seen after it is chosen
   *    representative  appears nowhere an agent sees
   *    core one-liner  appears nowhere an agent sees
   *
   *  The last two are still required by the API, so they are still sent — derived rather than asked
   *  for. A required field with no consumer is the "empty slot that looks alive" this codebase keeps
   *  finding, except worse: it is a slot a person is made to fill.
   *
   *  The one-liner is asked for only when there is no LLM to write it, because the validator refuses
   *  a one-liner identical to the condition — they are different sentences and one cannot stand in
   *  for the other.
   */
  async function newRegionForm() {
    const card = el("form", "kn-card-form");
    card.addEventListener("submit", (e) => e.preventDefault());
    card.append(el("h3", "kn-cf-title", t("knowledge.bb.newRegion")));
    card.append(el("p", "kn-cf-lead", t("knowledge.bb.newRegionLead")));

    const source = input("", { placeholder: "delivery", class: "kn-input is-mono", spellcheck: "false" });
    const useWhen = input("", { maxlength: 300, placeholder: t("knowledge.bb.useWhenHint") });
    card.append(labelled("knowledge.bb.asName", source, t("knowledge.bb.asNameHint")));

    // The line an agent routes on. It is the point of the form, so it is the second thing read and
    // it carries the help.
    const useWhenRow = labelled("knowledge.bb.useWhen", useWhen, t("knowledge.bb.useWhenWhy"));
    useWhenRow.append(suggest(async () => {
      if (!source.value.trim()) throw new Error(t("knowledge.bb.draftNeedsName"));
      // The name in the form a person reads, not the slug. This sent `it-support` as *what the area
      // is*, which tells a model nothing it did not already have from the name — and the field it
      // fills is the one an agent routes on.
      const label = source.value.trim().replace(/-/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
      const d = await post("suggest/use-when", { name: label, one_liner: label });
      useWhen.value = String(d.use_when || "");
      useWhen.focus();
    }));
    card.append(useWhenRow, guide("knowledge.guide.useWhen"));

    card.append(actions(
      button("common.cancel", "quiet", closeCard),
      button("knowledge.create", "primary", (b) => guarded(b, async () => {
        const src = source.value.trim();
        if (!NAME_ID.test(src)) throw new Error(t("knowledge.bb.badAsName"));
        if (!useWhen.value.trim()) throw new Error(t("knowledge.bb.useWhen") + " " + t("knowledge.required"));
        // Derived, not asked for. `name` is the area's name in display form; the API needs a
        // representative to have one and nothing an agent reads ever shows it. `core_description`
        // is the area's row in CORE.md, which no agent path fetches in this build — it is seeded
        // from the one-liner and can be edited afterwards through the proposal queue.
        const label = src.replace(/-/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
        const oneLine = label;
        const made = await post("regions", {
          source: src,
          core_description: oneLine,
          representative: { id: src, name: label, one_liner: oneLine, use_when: useWhen.value.trim() },
        });
        state.picked.clear();
        openArea(norm(src));
        await refreshFromKnowledge();
        await showRaw({ kind: "as", title: src, address: `/v1/regions/${src}` });
        regionDoneCard(made, src);
      }, "knowledge.created")),
    ));
    $("knEdit").replaceChildren(card);
    showEditor(true);
    source.focus();
  }

  /** What was made, and the one thing left to do. A new AS has a representative and no documents, so
   *  the next act is the same as after any creation: put something in it. */
  function regionDoneCard(made, source) {
    const rep = String(made?.representative || "");
    const card = el("form", "kn-card-form");
    card.addEventListener("submit", (e) => e.preventDefault());
    card.append(el("h3", "kn-cf-title", t("knowledge.done.created")));
    const facts = el("div", "kn-facts");
    const row = (labelKey, value, noteKey) => {
      facts.append(el("span", "kn-fact-k", t(labelKey)));
      const v = el("span", "kn-fact-v");
      v.append(el("code", null, value));
      if (noteKey) v.append(el("span", "kn-fact-n", t(noteKey)));
      facts.append(v);
    };
    row("knowledge.done.address", `/v1/regions/${source}`, "knowledge.done.addressFixed");
    card.append(facts);
    card.append(el("p", "kn-fnote", t("knowledge.bb.newRegionNext")));
    card.append(actions(
      button("knowledge.done.ok", "primary", () => $("knRawDialog").close()),
      ...(rep ? [button("knowledge.act.newData", null, () => newFileForm(rep))] : []),
    ));
    $("knEdit").replaceChildren(card);
    showEditor(true);
  }

  // ── submitting a routing change ───────────────────────────────────────────
  //
  // A node was added, so what its Region says about itself may no longer cover what it holds. The
  // person decides whether to raise that; Knowledge works out what is missing and drafts the sentence.
  // Two scopes reach this screen: `dr` changes how a Region describes itself, `bb` changes when a run
  // should choose it at all — the second is why this goes through a queue instead of being written
  // directly. `core` exists in the API and has no button here yet; nothing has asked for one.
  // Knowledge widened `scope` to take `as` while still accepting `dr` — receiver first, so the sender
  // can change without a moment where either side refuses the other. `dr` stays readable here only
  // until Knowledge drops it: a proposal filed under the old spelling must not stop rendering.
  const SCOPE_KEY = { as: "knowledge.scope.as", dr: "knowledge.scope.as", bb: "knowledge.scope.bb", core: "knowledge.scope.core", entity: "knowledge.scope.entity",
    // The three that cross a link. A reviewer reads this chip to know what they are being asked
    // about, and a scope with no entry here renders as its own identifier — which for these three
    // would leave somebody approving `peer-line` with nothing on screen saying what that is.
    peer: "knowledge.scope.peer", audience: "knowledge.scope.audience", "peer-line": "knowledge.scope.peerLine" };

  /** What this area sends across a link, all three parts of it, in one place.
   *
   *  Three decisions and three proposals, not one form with three fields: the line everybody sees,
   *  who sees it, and what one named reader is shown instead. Each goes through the review queue on
   *  its own because each can be reviewed on its own — and because "stop advertising this area" and
   *  "reword it" should never arrive as one thing to say yes or no to.
   *
   *  Until this existed all three were reachable only by an API nobody publishes outside the compose
   *  network. docs/PEERING.md described the decision at length and there was nowhere to make it. */
  async function exportCard(region) {
    const pane = $("knEdit");
    pane.replaceChildren(el("p", "kn-fnote", t("common.loading")));
    showEditor(true);
    let r;
    try { r = await request("regions/" + encodeURIComponent(region)); }
    catch (error) { pane.replaceChildren(el("div", "kn-err-box", "")); cardError(error.message); return; }

    const line = String(r.use_when_export || "");
    const audience = (r.export_to || []).map(String);
    const per = r.use_when_export_for || {};
    // Who there is to name. The backbones whose areas this one can already see are the ones a person
    // has evidence of; anybody else has to be typed, because a room can hold a member this backbone
    // has never been offered anything by.
    const known = [...new Set([...(state.regions || []).filter((x) => x.peer).map((x) => String(x.origin || "")),
                               ...Object.keys(per)])].filter(Boolean).sort();

    const card = el("form", "kn-card-form");
    card.addEventListener("submit", (e) => e.preventDefault());
    card.append(el("h3", "kn-cf-title", t("knowledge.export.title").replace("{area}", region)));
    card.append(el("p", "kn-cf-lead", t("knowledge.export.lead")));

    const section = (titleKey, leadKey) => {
      const box = el("section", "kn-export-part");
      box.append(el("h4", "kn-cf-sub", t(titleKey)), el("p", "kn-fnote", t(leadKey)));
      card.append(box);
      return box;
    };
    const send = (box, body, doneKey) => actions(button("knowledge.export.propose", null, (b) =>
      guarded(b, async () => { await post("proposals", body()); await loadFlags(); draw(); }, doneKey)));

    // 1 — the line, and the absence of one. Empty means the area crosses nothing at all, which is
    // the state every area starts in and the only one that cannot be reached by writing something.
    const one = section("knowledge.export.line", line ? "knowledge.export.lineLead" : "knowledge.export.lineNone");
    const lineBox = area(line, 3);
    const lineWhy = input("", { maxlength: 600, placeholder: t("knowledge.submit.whyHint") });
    one.append(labelled("knowledge.ba.after", lineBox, t("knowledge.submit.editable")),
               guide("knowledge.guide.exportLine"),
               labelled("knowledge.submit.why", lineWhy),
               send(one, () => {
                 const text = lineBox.value.trim();
                 if (!text && !line) throw new Error(t("knowledge.submit.needsText"));
                 if (text === line.trim()) throw new Error(t("knowledge.submit.unchanged"));
                 // Cleared, against a line that exists: the withdrawal, and it is reviewed like
                 // everything else because it takes knowledge away from another organisation.
                 return { scope: "peer", region, before: line, after: text, why: lineWhy.value.trim() };
               }, "knowledge.submit.sent"));

    // 2 — who. Empty is everybody the line already reaches, and is what almost every area wants.
    const two = section("knowledge.export.audience", "knowledge.export.audienceLead");
    const audBox = input(audience.join(", "), { placeholder: t("knowledge.export.audienceHint") });
    const audWhy = input("", { maxlength: 600, placeholder: t("knowledge.submit.whyHint") });
    const chipRow = el("div", "kn-chiprow");
    for (const name of known) {
      const chip = el("button", "kn-chip is-add", name);
      chip.type = "button";
      chip.addEventListener("click", () => {
        const have = audBox.value.split(",").map((x) => x.trim()).filter(Boolean);
        if (!have.includes(name)) audBox.value = [...have, name].join(", ");
        audBox.focus();
      });
      chipRow.append(chip);
    }
    two.append(labelled("knowledge.export.audience", audBox));
    if (known.length) two.append(chipRow);
    two.append(labelled("knowledge.submit.why", audWhy),
               send(two, () => {
                 const text = audBox.value.split(",").map((x) => x.trim()).filter(Boolean).join(", ");
                 if (text === audience.join(", ")) throw new Error(t("knowledge.submit.unchanged"));
                 return { scope: "audience", region, before: audience.join(", "), after: text,
                          why: audWhy.value.trim() };
               }, "knowledge.submit.sent"));

    // 3 — a different sentence for one named reader, and the ones already written.
    const three = section("knowledge.export.override", "knowledge.export.overrideLead");
    if (Object.keys(per).length) {
      const facts = el("div", "kn-facts");
      for (const [who, what] of Object.entries(per).sort()) {
        facts.append(el("span", "kn-fact-k", who));
        const v = el("span", "kn-fact-v"); v.append(el("code", null, what)); facts.append(v);
      }
      three.append(facts);
    }
    const whoBox = input("", { placeholder: known[0] || t("knowledge.export.peerHint") });
    const overBox = area("", 3);
    const overWhy = input("", { maxlength: 600, placeholder: t("knowledge.submit.whyHint") });
    whoBox.addEventListener("input", () => { overBox.value = String(per[whoBox.value.trim()] || overBox.value); });
    three.append(labelled("knowledge.export.peer", whoBox),
                 labelled("knowledge.ba.after", overBox, t("knowledge.export.overrideClear")),
                 labelled("knowledge.submit.why", overWhy),
                 send(three, () => {
                   const who = whoBox.value.trim();
                   if (!who) throw new Error(t("knowledge.export.needsPeer"));
                   return { scope: "peer-line", region, peer: who, before: String(per[who] || ""),
                            after: overBox.value.trim(), why: overWhy.value.trim() };
                 }, "knowledge.submit.sent"));

    card.append(actions(button("common.cancel", "quiet", closeCard)));
    pane.replaceChildren(card);
    lineBox.focus();
  }

  /** A change to a routing line, as a proposal. It opens on the sentence as it stands — read from the
   *  ontology, so it works with no LLM — and the person writes what it should say. Suggest asks for a
   *  draft; it is never asked for on its own, because it costs a call and a wait (13 s measured). */
  async function submitCard(region, scope, opts = {}) {
    const pane = $("knEdit");
    pane.replaceChildren(el("p", "kn-fnote", t("common.loading")));
    showEditor(true);
    const entity = scope === "entity" ? opts.entity : null;
    const field = scope === "bb" ? "use_when" : "one_liner";
    let before = "";
    try {
      if (entity) before = String((await request("nodes/" + encodeURIComponent(entity))).one_liner || "");
      else {
        const r = await request("regions/" + encodeURIComponent(region));
        before = String((scope === "bb" ? r.use_when : r.advertises) || "");
      }
    } catch (error) {
      pane.replaceChildren(el("div", "kn-err-box", "")); cardError(error.message); return;
    }

    const card = el("form", "kn-card-form");
    card.addEventListener("submit", (e) => e.preventDefault());
    card.append(el("h3", "kn-cf-title", entity ? t("knowledge.submit.titleEntity").replace("{id}", entity)
      : t(scope === "bb" ? "knowledge.submit.titleBb" : "knowledge.submit.titleAs")));
    card.append(el("p", "kn-cf-lead", t(SCOPE_KEY[scope] || scope)));
    card.append(beforeAfter({ region: entity || region, field, before, after: null }));

    const after = area(before, 4);
    const why = input("", { maxlength: 600, placeholder: t("knowledge.submit.whyHint") });
    const notes = el("div", "kn-draft-notes");
    const chips = (labelKey, list) => {
      if (!list.length) return;
      const box = el("div", "kn-uncovered");
      box.append(el("span", "kn-fact-k", t(labelKey)));
      const row = el("div", "kn-chiprow");
      for (const u of list) row.append(el("span", "kn-chip", u));
      box.append(row);
      notes.append(box);
    };
    const afterRow = labelled("knowledge.ba.after", after, t("knowledge.submit.editable"));
    afterRow.append(suggest(async () => {
      // An entity's row is drafted from the entity — its body, and its siblings' rows, so the line
      // tells it apart from what sits next to it. An area's line is drafted from what the area holds.
      const draft = entity ? await post(`nodes/${encodeURIComponent(entity)}/one-liner-draft`, {})
        : await post("route-draft", { region, scope, ...(opts.changed ? { changed: opts.changed } : {}) });
      notes.replaceChildren();
      // Nothing missing is an answer, and the useful one. Making a proposal anyway is how a review
      // queue becomes noise, so it says so instead of offering a sentence.
      if (draft.nothing_to_do || !String(draft.after_draft || "").trim()) {
        notes.append(el("p", "kn-fnote", draft.why ? `${t("knowledge.submit.nothing")} ${draft.why}` : t("knowledge.submit.nothing")));
        return;
      }
      after.value = String(draft.after_draft || "");
      if (!why.value.trim()) why.value = String(draft.why || "");
      chips("knowledge.submit.uncovered", (draft.uncovered || []).filter(Boolean));
      chips("knowledge.submit.apartFrom", (draft.distinguishes_from || []).filter(Boolean));
      after.focus();
    }));
    card.append(afterRow, notes, guide(scope === "bb" ? "knowledge.guide.useWhen" : entity ? "knowledge.guide.oneLiner" : "knowledge.guide.asLine"));
    card.append(labelled("knowledge.submit.why", why));

    card.append(actions(
      button("common.cancel", "quiet", closeCard),
      button("knowledge.submit.send", "primary", (b) => guarded(b, async () => {
        const text = after.value.trim();
        if (!text) throw new Error(t("knowledge.submit.needsText"));
        if (text === before.trim()) throw new Error(t("knowledge.submit.unchanged"));
        await post("proposals", {
          scope, ...(entity ? { entity } : { region }), before, after: text,
          why: why.value.trim(), ...(opts.target ? { target: opts.target } : {}),
        });
        await loadFlags();
        draw();
        pane.replaceChildren(sentCard(region, scope));
      }, "knowledge.submit.sent")),
    ));
    pane.replaceChildren(card);
    after.focus();
  }

  /** After submitting: what happens next, and — for an AS change — the one follow-up question worth
   *  asking, with the sentence it is about in view. A person cannot judge "did the reason to choose
   *  this Region change?" without seeing what that reason currently says. */
  function sentCard(region, scope) {
    const card = el("form", "kn-card-form");
    card.addEventListener("submit", (e) => e.preventDefault());
    card.append(el("h3", "kn-cf-title", t("knowledge.submit.sentTitle")));
    card.append(el("p", "kn-cf-lead", t("knowledge.submit.sentLead")));
    const buttons = [button("knowledge.done.ok", "primary", () => $("knRawDialog").close())];
    if (scope === "as" || scope === "dr") {
      const now = (state.regions.find((r) => norm(r.source) === norm(region)) || {}).use_when || "";
      const facts = el("div", "kn-facts");
      facts.append(el("span", "kn-fact-k", t("knowledge.submit.currentUseWhen")));
      const v = el("span", "kn-fact-v");
      v.append(el("code", null, now || "—"));
      facts.append(v);
      card.append(facts);
      card.append(el("p", "kn-fnote", t("knowledge.submit.bbAsk")));
      buttons.push(button("knowledge.submit.toBb", null, () => submitCard(region, "bb")));
    }
    card.append(actions(...buttons));
    return card;
  }

  // ── pending routing requests, drawn on the thing they would change ─────────
  //
  // These used to be rows in a panel, and a panel is the wrong shape for them: a routing request is a
  // proposal to change what one Region advertises, so the Region is where it belongs. A flagged device
  // is the notification, the rack button is the way in, and the review is the same two boxes the
  // submission card shows. Nothing else on the screen has to be visited to find out there is work.
  //
  // `scope` decides which device wears the flag, and the mapping is the only one this screen holds
  // because it is about drawing, not about which field gets written: `as` — and `dr`, its former
  // spelling — changes what a Region says about itself, so it flags that Region; `bb` and `core` change
  // hop 0, the list every run reads before choosing a Region, so they flag the backbone.
  const BB_SCOPES = new Set(["bb", "core"]);

  /** Pending route proposals, bucketed by the device that should show them. Failure is silent on
   *  purpose: the map is worth drawing without the flags, and a screen that refuses to render because
   *  a notification could not be counted would be worse than one that quietly has none.
   *
   *  Silent, but not thrown away. Without `ONTOLOGY_HARNESS` every curator call answers 501, and this
   *  is the call that finds that out — the same way `loadOverlays` finds out whether overlays exist.
   *  What it learns gates "Advertise upstream", which until 2026-09-12 was offered on every install
   *  and could only ever answer with the name of an environment variable. */
  async function loadFlags() {
    const next = new Map();
    try {
      const rows = (await request("proposals?status=pending")).proposals || [];
      state.curatorOn = true;
      const add = (key, p) => { if (!key) return; if (!next.has(key)) next.set(key, []); next.get(key).push(p); };
      for (const p of rows) {
        if (p.type !== "route") continue;
        if (p.scope === "entity") {
          // One row in a node's table: its own rack wears the flag, and its area counts it, so the
          // map shows there is work without the node being open.
          const n = state.nodes.find((x) => x.id === p.entity);
          add(`node:${p.entity}`, p);
          add(n ? norm(regionOf(n)) : "", p);
          continue;
        }
        add(BB_SCOPES.has(p.scope) ? "__bb" : norm(p.region || ""), p);
      }
    } catch (error) {
      // 404 or 501 is the install saying it keeps no curator; anything else is a call that failed on
      // an install that does have one, and the flags are simply missing this time round.
      if (error.status === 404 || error.status === 501) state.curatorOn = false;
    }
    state.flags = next;
  }
  const flagsFor = (key) => state.flags.get(key) || [];

  /** The review, in the popup, over the device it belongs to. One proposal per block: what it would
   *  change, the sentence now, the sentence proposed, and the two answers. */
  async function reviewFlags(key, title, address) {
    await showRaw({ kind: "as", title, address });
    const pane = $("knEdit");
    const wrap = el("div", "kn-form");
    const list = flagsFor(key);
    wrap.append(el("h3", "kn-cf-title", t("knowledge.flag.title")));
    if (!list.length) wrap.append(el("p", "kn-fnote", t("knowledge.flag.none")));
    for (const p of list) wrap.append(reviewBlock(p, key));
    wrap.append(actions(button("knowledge.act.showRaw", "quiet", closeCard)));
    pane.replaceChildren(wrap);
    showEditor(true);
  }

  function reviewBlock(p, key) {
    const box = el("div", "kn-review");
    const head = el("div", "kn-card-top");
    head.append(el("span", "kn-type", t("knowledge.type.route")));
    if (p.scope) head.append(el("span", "kn-scope", t(SCOPE_KEY[p.scope] || p.scope)));
    head.append(el("span", "kn-when", when(p.at)));
    box.append(head);
    if (p.why) box.append(el("p", "kn-fnote", p.why));
    box.append(beforeAfter({ ...p, region: p.region || p.entity, peer: p.peer }));

    const why = input("", { placeholder: t("knowledge.rejectPlaceholder") });
    const decide = (decision) => (b) => guarded(b, async () => {
      if (decision === "reject" && !why.value.trim()) throw new Error(t("knowledge.rejectNeedsReason"));
      await post(`proposals/${encodeURIComponent(p.id)}/${decision}`, why.value.trim() ? { why: why.value.trim() } : {});
      // Accepting rewrites a routing signal, so what the agent reads has moved: the map, the flags and
      // the transcript all have to be re-read rather than patched in place.
      await refreshFromKnowledge();
      await loadFlags();
      draw();
      await reviewFlags(key, $("knRawTitle").textContent, state.selected?.address || "");
    }, decision === "accept" ? "knowledge.applied" : "knowledge.recorded");
    box.append(why);
    box.append(actions(
      button("knowledge.acceptPublish", "primary", decide("accept")),
      button("knowledge.reject", "danger", decide("reject")),
    ));
    return box;
  }

  /** Two boxes, current and proposed, with the field they rewrite named above them. Shared by the
   *  review and, when it is built, by the submission card — a person should see the same shape when
   *  writing a change as when judging one. */
  function beforeAfter({ field, before, after, region, peer }) {
    const wrap = el("div", "kn-ba");
    const head = el("p", "kn-ba-head");
    // The peer, when there is one. A `peer-line` proposal rewrites one key of a mapping, and without
    // the name here a reviewer sees `use_when_export_for` and two sentences with no way to tell whose
    // line they are — which is the whole of what they are being asked to judge.
    head.textContent = [region, field, peer ? t("knowledge.scope.forPeer").replace("{peer}", peer) : ""]
      .filter(Boolean).join("  ·  ");
    wrap.append(head);
    const pair = el("div", "kn-ba-pair");
    const box = (cls, labelKey, text) => {
      const b = el("div", "kn-ba-box " + cls);
      b.append(el("span", "kn-ba-label", t(labelKey)));
      b.append(el("p", null, text || "—"));
      return b;
    };
    pair.append(box("is-before", "knowledge.ba.before", before));
    pair.append(el("div", "kn-ba-arrow", "→"));
    pair.append(box("is-after", "knowledge.ba.after", after));
    wrap.append(pair);
    return wrap;
  }

  function failInto(id, error) {
    const box = $(id);
    if (box) box.replaceChildren(el("div", "kn-empty", `${t("knowledge.loadFailed")} — ${error.message}`));
    toast(error.message);
  }


  // ── the record behind the transcript ──────────────────────────────────────
  //
  // The popup shows two different things about one address. The transcript is what Pi hands the agent —
  // the authority on what the agent sees. The form is the ontology record — the authority on what is
  // stored. They are fetched from different endpoints on purpose: building the form out of the
  // transcript would make this screen re-parse the prompt, and writing back what the transcript says
  // would edit a rendering instead of a record. Only one is visible at a time, for the same reason.
  const FILE_ADDR = /^\/v1\/nodes\/([a-z0-9][a-z0-9-]*)\/files\/(.+)$/;
  const NODE_ADDR = /^\/v1\/nodes\/([a-z0-9][a-z0-9-]*)$/;
  // An entity's own document, under one type. Without this the address matched nothing below and fell
  // through to the last line — `backbone` — so every document opened as the backbone, with the
  // backbone's chip and its "New AS / New data" buttons.
  const BODY_ADDR = /^\/v1\/nodes\/([a-z0-9][a-z0-9-]*)\/body$/;
  // A document's file name is its entity's address: `organizing-rules.md` is `/v1/nodes/organizing-rules`.
  // This rule used to allow `_` and `.` in the name, from when a file was only a file; the ontology
  // refuses both in an id, so the form let a name through that could never be saved, and the refusal
  // then talked about an "id" the person had never typed. One rule, the id's, stated as a file rule.
  const NODE_FILE = /^[a-z0-9][a-z0-9-]*\.md$/;
  /** The nearest name that is allowed: lowercase, and anything that is not a letter or digit becomes a
   *  single hyphen. Offered, never applied behind someone's back — the name is the address, and an
   *  address that quietly differs from what was typed is one nobody can find again. */
  const fileNameFor = (raw) => {
    const stem = String(raw || "").trim().replace(/\.(md|txt|markdown)$/i, "").toLowerCase()
      .replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "");
    return stem ? `${stem}.md` : "";
  };
  const FRAG_FILE = /^[^/\\.][^/\\]*\.(md|yaml|yml)$/i;
  const NAME_ID = /^[a-z0-9][a-z0-9-]*$/;
  /** The address a name gives by itself. Only an all-ASCII name has one: "Ürün" would reduce to `r-n`,
   *  which looks deliberate and is not — the same rule Knowledge applies (13934d8). */
  const idFor = (name) => {
    const n = String(name || "").trim();
    if (!n || /[^\x00-\x7f]/.test(n)) return "";
    return n.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "");
  };

  // ── what a thing is, and what can be done to it — one table ─────────────────
  //
  // Every button on this screen comes from here: the popup header and the rack buttons both read this
  // table and use the same words for the same act. Before this there were four hidden buttons toggled
  // by three regexes, a rack label spelled differently from the popup's, and a popup eyebrow that said
  // one label for both a Region and a node. The operator's report — "the promote button works in some popups
  // and not others" — was that: the buttons were right, the reader could not tell which popup they
  // were in. The kind is derived from the address, never from where the click came from.
  const OBJECT = {
    // Two acts at the backbone: add an AS, add data. Creating a service fragment was here too and is
    // gone (operator) — services left this screen once already, and Knowledge makes them.
    backbone: { label: "BACKBONE", actions: ["reviewBB", "startHere", "newRegion", "newBBData", "copyAgent"] },
    core:     { label: "CORE",     actions: [] },
    service:  { label: "SERVICE",  actions: ["newServiceData"] },
    // One word for both (operator, 2026-09-11): an area and a node that holds things are the same
    // kind of thing on this screen — an Autonomous System — and the racks already say so.
    region:   { label: "AS",       actions: [] },
    node:     { label: "AS",       actions: [] },
    // One act (operator, 2026-09-11). Promotion went: "+ New node" and a drag onto it do the same
    // job in two steps a person can see. Editing went with it.
    file:     { label: "DATA",     actions: ["deleteData"] },
  };
  /** Hand a selection to the Operations page. A ticked set wins over the one thing that was clicked:
   *  a person who ticked three areas and then pressed start on one of them meant the three. Whoever
   *  selects — a person here, the backbone agent later — the run is started the same way. */
  function startRun(fallback) {
    if (!canRun()) return;
    const chosen = state.picked.size ? [...state.picked] : (fallback || []).filter(Boolean);
    const q = chosen.length ? "?" + chosen.map((r) => `root=${encodeURIComponent(r)}`).join("&") : "";
    window.location.href = state.cfg.agentUrl + q;
  }

  /** Whether picking an area leads anywhere. With no agent configured there is no run to start, so the
   *  tick boxes, the selection bar and every start button are absent rather than inert — an affordance
   *  that does nothing teaches that the thing behind it does not work. */
  const canRun = () => Boolean(state.cfg.agent && state.cfg.agentUrl);
  /** Ticking is how a person draws a VRF, so it exists wherever a pick can go somewhere: a run to
   *  start, or an overlay to create. With neither, the boxes would be controls that do nothing. */
  const canPick = () => canRun() || state.vrfOn;

  const ACTION = {
    reviewBB: { key: "knowledge.flag.short", run: () => reviewFlags("__bb", "RouteMind Back-Bone", ""),
      when: () => flagsFor("__bb").length > 0 },
    newRegion: { key: "knowledge.bb.newRegion", run: () => newRegionForm() },
    newBBData: { key: "knowledge.act.newData", run: () => whyNoBBData() },
    // For an agent that has no MCP — a chat window, a notebook, a colleague's tool. Here because this
    // popup is the list it copies: the Back-Bone's table is where every run starts.
    copyAgent: { key: "knowledge.copyForAgent", run: () => copyForAgent() },
    newServiceData: { key: "knowledge.act.newData", run: (x) => newServiceFileForm(x.service) },
    // Pin where a run starts looking. A Region hands the agent that Region's table at hop 0 instead of
    // spending a call to fetch it — measured 6 routing steps down to 1 on the same question, with the
    // same answer. The backbone is the unpinned default, so its button carries no root at all rather
    // than a root that means "everything": those are different claims and only one of them is true.
    startHere: { key: "knowledge.act.start", when: canRun,
      run: (x) => startRun(x.kind === "region" ? [`/v1/regions/${x.dir}`] : []) },
    newNode: { key: "knowledge.act.newNode", run: (x) => newNodeForm(x.dir) },
    newData: { key: "knowledge.act.newData", run: (x) => newFileForm(x.node || representativeOf(x.dir)) },
    deleteData: { key: "knowledge.delete", danger: true, run: async (x) => deleteNodeCard(await entityOf(x)) },
  };
  /** The entity a document address names. The body address carries it; the older `files/<name>`
   *  form carries the holder and a file name, and the id is whichever child of the holder that is. */
  async function entityOf(target) {
    if (target.entity) return target.entity;
    const rec = await request("nodes/" + encodeURIComponent(target.node));
    const stem = String(target.name || "").replace(/\.md$/i, "");
    const hit = (rec.entries || []).find((e) => e.id === stem || e.id === `${target.node}-${stem}`);
    if (!hit) throw new Error(`${target.node} / ${target.name}: not found`);
    return hit.id;
  }
  const representativeOf = (dir) => (state.regions.find((r) => norm(r.source) === norm(dir)) || {}).representative || null;
  function editTarget(address) {
    if (!address) return { kind: "backbone" };
    if (address === "/v1/core") return { kind: "core" };
    let m = BODY_ADDR.exec(address);
    if (m) return { kind: "file", entity: m[1] };
    m = FILE_ADDR.exec(address);
    if (m) return { kind: "file", node: m[1], name: m[2] };
    m = NODE_ADDR.exec(address);
    if (m) return { kind: "node", node: m[1] };
    m = /^\/v1\/regions\/([a-z0-9-]+)$/.exec(address);
    if (m) return { kind: "region", dir: m[1] };
    m = /^\/v1\/services\/([^/]+)$/.exec(address);
    if (m) return { kind: "service", service: m[1] };
    return { kind: "backbone" };
  }

  /** The header's action bar, rebuilt for the current target. Fixed order, first one styled as the
   *  primary; Copy and Close are outside this bar and never move. */
  function renderActions(target) {
    const bar = $("knActions");
    bar.replaceChildren();
    // While a card is open the card owns the actions. Leaving the header bar up meant two buttons
    // reading "Promote to node" — one that opens the card and one inside it — and a reader has to work out
    // that they are not two different things.
    if (!$("knEdit").hidden) return;
    const acts = (OBJECT[target.kind] || OBJECT.backbone).actions
      .map((id) => ({ id, ...ACTION[id] }))
      .filter((a) => !a.when || a.when(target));
    acts.forEach((a, i) => {
      const b = el("button", "kn-btn" + (a.danger ? " kn-danger" : i === 0 ? " kn-primary" : ""), t(a.key));
      b.type = "button";
      b.dataset.action = a.id;
      b.addEventListener("click", () => {
        Promise.resolve(a.run(target)).catch((e) => toast(e.message));
      });
      bar.append(b);
    });
  }

  let vocabCache = null;
  const vocab = async () => (vocabCache || (vocabCache = await request("vocab")));


  const send = (path, method, body) => request(path, {
    method, headers: { "Content-Type": "application/json" },
    body: body === undefined ? undefined : JSON.stringify(body || {}),
  });

  // ── form primitives ───────────────────────────────────────────────────────
  // ── the LLM, as a button (operator, 2026-09-11) ─────────────────────────
  //
  // Every routing line on this screen is written by a person. Where an LLM is configured, a Suggest
  // button beside the field fetches a draft into it — nothing is saved until the person presses the
  // form's own button, and nothing is derived behind their back. Without one the button is still
  // there, disabled, saying what would turn it on: the two installs are the same screen, and a person
  // without an LLM is not left wondering whether a field is missing.
  function suggest(fill) {
    const b = button("knowledge.llm.suggest", "quiet small", (btn) => guarded(btn, fill));
    b.classList.add("kn-inline-act");
    b.title = t(state.cfg.derives ? "knowledge.llm.on" : "knowledge.llm.off");
    if (!state.cfg.derives) b.disabled = true;
    return b;
  }
  /** How to write a routing line, folded under the field: it matters most to someone writing their
   *  first one with no LLM to draft it, and least to someone who has written a hundred. */
  function guide(key) {
    const d = el("details", "kn-guide");
    d.append(el("summary", null, t("knowledge.guide.title")));
    for (const line of t(key).split("\n")) d.append(el("p", null, line));
    return d;
  }
  /** The address, shown and editable. It follows the name until the person types into it. A name that
   *  gives no address of its own leaves it empty and asking — or Suggest translates one. */
  function addressField(nameInput, prefix) {
    const addr = input("", { class: "kn-input is-mono", spellcheck: "false", placeholder: "billing-gateway" });
    let touched = false;
    addr.addEventListener("input", () => { touched = Boolean(addr.value.trim()); });
    nameInput.addEventListener("input", () => { if (!touched) addr.value = idFor(nameInput.value); });
    const row = labelled("knowledge.field.id", addr, t("knowledge.field.idHint").replace("{prefix}", prefix));
    row.append(suggest(async () => {
      if (!nameInput.value.trim()) throw new Error(t("knowledge.bb.draftNeedsName"));
      const d = await post("suggest/id", { name: nameInput.value.trim() });
      addr.value = String(d.id || "");
      touched = true;
      // A name that gave its own address will always give that one. One a model translated is the
      // one worth a glance: it is permanent, and nobody typed it.
      note.textContent = d.from === "model" ? t("knowledge.field.idByModel") : "";
    }));
    const note = el("span", "kn-fhint kn-id-note");
    row.append(note);
    return {
      row,
      read() {
        const v = addr.value.trim();
        if (!NAME_ID.test(v)) throw new Error(t("knowledge.badId"));
        return v;
      },
    };
  }

  function labelled(labelKey, control, hintText) {
    const row = el("label", "kn-frow");
    row.append(el("span", "kn-flabel", t(labelKey)));
    row.append(control);
    if (hintText) row.append(el("span", "kn-fhint", hintText));
    return row;
  }
  function input(value, attrs) {
    const n = el("input", "kn-input");
    n.type = "text";
    n.value = value == null ? "" : String(value);
    for (const k of Object.keys(attrs || {})) n.setAttribute(k, String(attrs[k]));
    return n;
  }
  function area(value, rows) {
    const n = el("textarea", "kn-area");
    n.rows = rows || 18;
    n.value = value == null ? "" : String(value);
    return n;
  }
  function select(options, value) {
    const n = el("select", "kn-input");
    for (const o of options) {
      const opt = el("option", null, o.label);
      opt.value = o.value;
      if (o.value === value) opt.selected = true;
      n.append(opt);
    }
    return n;
  }
  function actions(...buttons) {
    const bar = el("div", "kn-form-actions");
    const rank = (b) => (b.classList.contains("kn-danger") ? 0 : b.classList.contains("kn-primary") ? 2 : 1);
    buttons.filter(Boolean).sort((a, b) => rank(a) - rank(b)).forEach((b) => bar.append(b));
    return bar;
  }
  function button(labelKey, cls, onClick) {
    // Variants arrive as plain words ("primary", "quiet small") and are given this page's prefix. The
    // bare `.primary` is restyled with !important by a sheet this page inherits, which is why "Create"
    // rendered as a pale tint rather than a filled button.
    const variants = String(cls || "").split(/\s+/).filter(Boolean).map((c) => "kn-" + c).join(" ");
    const b = el("button", "kn-btn" + (variants ? " " + variants : ""), t(labelKey));
    b.type = "button";
    // `guarded` has already shown the refusal by the time it rethrows; it rethrows for callers that
    // chain, and none do. Swallowing it here is what keeps a failed write from also logging an
    // unhandled rejection — the click handler is where the promise ends.
    b.addEventListener("click", () => Promise.resolve(onClick(b)).catch(() => {}));
    return b;
  }
  /** Every write goes through here so a failure is shown as the API worded it, never swallowed. The
   *  button is disabled for the round trip: a double-click on Create is a 409, and a 409 on a node
   *  that now exists reads like a bug in the screen rather than a second click. */
  async function guarded(btn, work, okKey) {
    const was = btn.textContent;
    btn.disabled = true;
    // Knowledge writes the id and the one-line description with an LLM, so a create can take ten
    // seconds or more. A button that only greys out looks stuck; this says what is happening.
    btn.textContent = t("knowledge.working");
    cardError("");
    try {
      const out = await work();
      if (okKey) toast(t(okKey));
      return out;
    } catch (error) {
      // In a card the refusal stays on screen beside the fields it is about; elsewhere a toast is all
      // there is. The API's own words either way — this layer has nothing to add to "not in vocab".
      if (!$("knEdit").hidden) cardError(error.message); else toast(error.message);
      throw error;
    } finally {
      btn.disabled = false;
      btn.textContent = was;
    }
  }

  /** The last refusal, shown at the foot of the open card and cleared when something is tried again. */
  function cardError(text) {
    const form = $("knEdit").firstElementChild;
    if (!form) return;
    // `form.children` is a live HTMLCollection: it has no `find` and no `splice`. Calling them threw
    // inside `guarded`'s catch, so the throw escaped, `finally` never ran, and the button stayed on
    // "working…" — a failed write looked like nothing happening at all.
    form.querySelector(":scope > .kn-err-box")?.remove();
    if (!text) return;
    const box = el("div", "kn-err-box");
    for (const line of String(text).split("\n")) box.append(el("p", null, line));
    form.append(box);
  }

  // ── editing what the map shows ────────────────────────────────────────────
  /** Leave a card and go back to the transcript. Every card carries this rather than relying on a
   *  header control, because the header is empty while a card is open. */
  const closeCard = () => showEditor(false);

  function showEditor(on) {
    $("knRawWrap").hidden = on;
    $("knEdit").hidden = !on;
    $("knRawDialog").classList.toggle("is-form", Boolean(on));
    if (!on) $("knEdit").replaceChildren();
    renderActions(editTarget(state.selected?.address || ""));
  }

  /** Upload is a way of filling the body, not a second kind of write: the file is read as text and put
   *  in the textarea, where it can still be corrected before it is saved. Anything that is not text is
   *  refused here rather than committed as mojibake — the ontology holds documents, not attachments. */
  const BINARY = /[\u0000-\u0008\u000E-\u001F]/;

  /** Upload a text file into the body.
   *
   *  The browser draws a native file input itself, in the browser's own language, and no page can
   *  translate it — so on an English page it read "파일 선택 / 선택된 파일 없음". The native input
   *  is kept (it is what opens the file dialog) but hidden, and the part a person sees is a button and
   *  a label this page renders. */
  function uploadRow(body, nameInput, onName, onLoad) {
    const picker = el("input", "kn-file");
    picker.type = "file";
    picker.hidden = true;
    picker.accept = ".md,.txt,.yaml,.yml,text/*";
    const chosen = el("span", "kn-file-chosen", t("knowledge.noFileChosen"));
    const choose = button("knowledge.chooseFile", "small", () => picker.click());
    picker.addEventListener("change", async () => {
      const file = picker.files && picker.files[0];
      if (!file) return;
      try {
        const text = await file.text();
        if (BINARY.test(text)) throw new Error(t("knowledge.notText"));
        body.value = text;
        chosen.textContent = file.name;
        if (onLoad) onLoad();
        if (nameInput && !nameInput.value.trim() && !nameInput.disabled) {
          nameInput.value = fileNameFor(file.name);
          if (onName) onName();
        }
        toast(t("knowledge.uploaded").replace("{name}", file.name));
      } catch (error) {
        toast(error.message);
      } finally {
        picker.value = "";
      }
    });
    // A div, not a <label>: a label forwards clicks to the control inside it, and with both a button
    // and a hidden file input inside, a click on the button could open the dialog twice.
    const row = el("div", "kn-frow");
    row.append(el("span", "kn-flabel", t("knowledge.upload")));
    const line = el("div", "kn-file-line");
    line.append(choose, chosen, picker);
    row.append(line);
    row.append(el("span", "kn-fhint", t("knowledge.uploadHint")));
    return row;
  }

  // Relations are off this screen (operator, 2026-09-09): they are Knowledge's data and get a page of
  // their own. A node made here is created with no edge. That is allowed because containment is already
  // declared — a node with no `parent` sits under its Region's representative — and the validator no
  // longer asks for the same fact twice as an edge. For one afternoon Web sent a `CONSISTS_OF` default
  // instead; Knowledge showed it was wrong in direction for the very case that motivated it, and it is
  // gone.


  /** Where an address sits, in words: Region ▸ node ▸ file. The address is what the agent uses; this
   *  line is what a person reads. Both are shown. */
  function breadcrumb(address) {
    const target = editTarget(address);
    if (target.kind === "region") return `AS ${target.dir}`;
    if (target.kind !== "node" && target.kind !== "file") return "";
    const n = state.nodes.find((x) => x.id === target.node);
    const region = n ? `AS ${norm(regionOf(n))}` : "";
    const parts = [region, target.node, target.name].filter(Boolean);
    return parts.join("  ▸  ");
  }

  /** Open the popup on `row` (so the transcript, path and header buttons are the right ones), then put
   *  the card over it. Used by the rack buttons, which start a card from the map rather than from an
   *  already-open popup. */
  async function openCard(row, card) {
    await showRaw({ kind: row.kind, title: row.label, address: row.address });
    await card();
  }

  /** What just happened, and nothing else. The routing table that used to be shown here is what the
   *  agent is handed; a person who has just made a node has no use for it and it buried the two facts
   *  that do matter — the address, which can never change, and the kind, which can but is cheapest to
   *  correct now. Confirm closes; the second button is the next thing a new node is for. */
  function doneCard({ made, nid, node, service }) {
    const card = el("form", "kn-card-form");
    card.addEventListener("submit", (e) => e.preventDefault());
    card.append(el("h3", "kn-cf-title", t("knowledge.done.created")));

    const facts = el("div", "kn-facts");
    const row = (labelKey, value, noteKey) => {
      facts.append(el("span", "kn-fact-k", t(labelKey)));
      const v = el("span", "kn-fact-v");
      v.append(el("code", null, value));
      if (noteKey) v.append(el("span", "kn-fact-n", t(noteKey)));
      facts.append(v);
    };
    row("knowledge.done.address", service ? `/v1/services/${service}` : `/v1/nodes/${nid}`, "knowledge.done.addressFixed");
    card.append(facts);
    // "Raise upstream" sits here because this is the moment a person knows what changed. It is optional
    // and costs an LLM call, so it is a button and not something that happens on its own.
    // The next step differs by what was made: a node takes documents, a service fragment takes its
    // owner's files, and only a node sits in an AS whose advertisement might now need raising.
    const onMap = state.nodes.find((n) => n.id === nid) || {};
    const region = service ? "" : norm(onMap.region_dir || onMap.region || state.open[state.open.length - 1] || "");
    card.append(actions(
      button("knowledge.done.ok", "primary", () => $("knRawDialog").close()),
      button("knowledge.act.newData", null, () => (service ? newServiceFileForm(service) : newFileForm(node))),
      ...(region && state.curatorOn ? [button("knowledge.submit.raise", null, () => submitCard(region, "as", { changed: [`/v1/nodes/${nid}`] }))] : []),
    ));
    $("knEdit").replaceChildren(card);
    showEditor(true);
  }

  /** A line above the transcript, cleared on every showRaw. Used by the request review; creation says
   *  what it did in a card instead. */
  function banner(text) {
    let b = $("knBanner");
    b.hidden = !text;
    b.textContent = text || "";
  }

  /** A new node in a Region. Same three fields as promotion, and no relation: it sits under the
   *  Region's representative by containment, which needs no edge to be true. */
  async function newNodeForm(regionDir, parent) {
    const card = el("form", "kn-card-form");
    card.addEventListener("submit", (e) => e.preventDefault());
    card.append(el("h3", "kn-cf-title", t("knowledge.newNode")));
    const lead = el("p", "kn-cf-lead");
    lead.textContent = parent ? t("knowledge.newNodeLeadIn").replace("{parent}", parent)
      : t("knowledge.newNodeLead").replace("{region}", regionDir);
    card.append(lead);
    const label = input("", { autofocus: "" });
    const one = input("", { maxlength: 300, placeholder: t("knowledge.oneLinerHint") });
    const addr = addressField(label, "/v1/nodes/");
    card.append(labelled("knowledge.field.name", label), addr.row);
    // Nothing to draft from yet — a new node has no body and nothing under it — so this one is typed.
    card.append(labelled("knowledge.field.oneLiner", one), guide("knowledge.guide.oneLiner"));
    card.append(actions(
      button("common.cancel", "quiet", closeCard),
      button("knowledge.create", "primary", (b) => guarded(b, async () => {
        if (!label.value.trim()) throw new Error(t("knowledge.field.name") + " " + t("knowledge.required"));
        if (!one.value.trim()) throw new Error(t("knowledge.field.oneLiner") + " " + t("knowledge.required"));
        const made = await send("nodes", "POST", {
          id: addr.read(), name: label.value.trim(), region: regionDir, one_liner: one.value.trim(), holds: "content",
          ...(parent ? { parent } : {}),
        });
        const nid = String(made?.id || made?.node || "");
        const key = norm(regionDir);
        openArea(key);
        // Opened where it was made: under its parent when it has one, the levels above left open.
        const path = pathIn(key), at = parent ? path.indexOf(parent) : -1;
        if (nid) setPath(key, [...(at >= 0 ? path.slice(0, at + 1) : []), nid]);
        await afterWrite(nid || null);
        if (nid) {
          await showRaw({ kind: "as", title: label.value.trim(), address: `/v1/nodes/${nid}` });
          doneCard({ made, nid, node: nid });
        }
      }, "knowledge.created")),
    ));
    $("knEdit").replaceChildren(card);
    showEditor(true);
    label.focus();
  }

  /** New data on a node. How the body arrives is chosen first — written here, or a file uploaded —
   *  and the form shows only that (operator, 2026-09-11). Both end in the same PUT; the name becomes
   *  the address either way, so it is asked in both. */
  function newFileForm(node) {
    const pane = $("knEdit");
    const form = el("form", "kn-card-form");
    form.addEventListener("submit", (e) => e.preventDefault());
    form.append(el("h3", "kn-cf-title", t("knowledge.newDataIn").replace("{node}", node)));

    const mode = el("div", "kn-seg");
    mode.setAttribute("role", "radiogroup");
    const choice = (value, key) => {
      const opt = el("label", "kn-seg-opt");
      const r = el("input");
      r.type = "radio"; r.name = "kn-data-mode"; r.value = value;
      opt.append(r, el("span", null, t(key)));
      mode.append(opt);
      return r;
    };
    const write = choice("write", "knowledge.mode.write");
    const upload = choice("upload", "knowledge.mode.upload");
    write.checked = true;
    const modeRow = el("div", "kn-frow");
    modeRow.append(el("span", "kn-flabel", t("knowledge.dataBy")), mode);
    form.append(modeRow);

    const name = input("", { placeholder: "overview" });
    // What was typed is not the rule's to police. The field shows, as it is typed, the address the
    // name becomes, and that is what is saved — so "organization_rules.md" just works, and the
    // person sees `/v1/nodes/organization-rules` before pressing anything. Refused only when nothing
    // in it can be an address at all.
    const where = el("span", "kn-addr-preview");
    const showWhere = () => {
      const f = fileNameFor(name.value);
      where.classList.toggle("is-bad", Boolean(name.value.trim()) && !f);
      where.textContent = !name.value.trim() ? t("knowledge.fileNameRule")
        : f ? t("knowledge.savedAs").replace("{addr}", `/v1/nodes/${f.replace(/\.md$/, "")}`)
        : t("knowledge.noAddressIn");
    };
    name.addEventListener("input", showWhere);
    const nameRow = labelled("knowledge.field.name", name);
    nameRow.append(where);
    form.append(nameRow);

    // Ten rows: sixteen pushed Create below the bottom of the dialog. It still grows by dragging.
    const body = area("", 10);
    const writeRow = labelled("knowledge.newFileHint", body);
    // Upload fills the same body, so switching to "write" afterwards is how an uploaded file gets
    // corrected before it is saved. What was loaded is shown, not hidden behind the file name.
    let loaded = false;
    const preview = el("pre", "kn-upload-preview");
    preview.hidden = true;
    const uploadRowEl = uploadRow(body, name, showWhere, () => {
      loaded = true;
      preview.textContent = body.value.length > 4000 ? `${body.value.slice(0, 4000)}\n…` : body.value;
      preview.hidden = false;
    });
    uploadRowEl.append(preview);
    form.append(writeRow, uploadRowEl);

    // The line an agent chooses this document by. Written by the person; Suggest reads the body.
    const desc = input("", { maxlength: 300, placeholder: t("knowledge.descHint") });
    const descRow = labelled("knowledge.field.description", desc);
    descRow.append(suggest(async () => {
      if (!body.value.trim()) throw new Error(t("knowledge.descNeedsBody"));
      const d = await post("suggest/description", { name: fileNameFor(name.value) || "document.md", content: body.value });
      desc.value = String(d.description || "");
      desc.focus();
    }));
    form.append(descRow, guide("knowledge.guide.description"));
    const render = () => { writeRow.hidden = !write.checked; uploadRowEl.hidden = !upload.checked; };
    write.addEventListener("change", render);
    upload.addEventListener("change", render);
    render();
    showWhere();

    form.append(actions(
      button("common.cancel", "quiet", closeCard),
      button("knowledge.create", "primary", (b) => guarded(b, async () => {
        if (upload.checked && !loaded) throw new Error(t("knowledge.chooseFileFirst"));
        const fname = fileNameFor(name.value);
        if (!fname || !NODE_FILE.test(fname)) throw new Error(t("knowledge.noAddressIn"));
        if (!desc.value.trim()) throw new Error(t("knowledge.descRequired"));
        await send(`nodes/${encodeURIComponent(node)}/files/${encodeURIComponent(fname)}`, "PUT",
          { content: body.value, description: desc.value.trim() });
        await afterWrite(node);
        $("knRawDialog").close();       // it is on the map now, in the rack that was open
      }, "knowledge.created")),
    ));
    pane.replaceChildren(form);
    showEditor(true);
    write.focus();
  }

  /** Every write through this API commits and republishes, so the map the person is looking at is
   *  stale the moment a write returns. Reloading it is not a courtesy — leaving it would let the next
   *  click act on a node that no longer exists. */
  async function afterWrite(nodeId) {
    state.files.delete(nodeId);
    await loadMap();
    if (nodeId) await loadFiles(nodeId);
    loadState();
    // This write moved `published`; take the new value now so the watcher's next tick is quiet rather
    // than a second redraw of what is already on screen.
    try { drawnRevision = String((await request("revision")).published || drawnRevision); } catch { /* next tick will */ }
  }

  // ── following the published revision ─────────────────────────────────────
  //
  // The map is a view of what the agent reads, and that changes from more places than this screen:
  // the Knowledge session writes through the API, the curator applies proposals, another operator has
  // the page open. So the screen asks one cheap question on a timer — is `published` still what I
  // drew? — and redraws only when the answer is no. It follows `published`, not `head`: a commit that
  // has not been published is invisible to the agent, and a map that ran ahead of the agent would be a
  // map of something else. Nothing is pushed from the server; a 27 ms GET every few seconds is cheaper
  // than a socket and has no reconnect story to get wrong.
  const WATCH_MS = 5000;
  let drawnRevision = null;
  let watchTimer = null;

  async function checkRevision() {
    if (document.visibilityState === "hidden") return;
    if (drag?.started) return;              // a redraw would pull the map out from under the pointer
    // Overlays are not in the published tree — an agent opens one mid-run — so they are followed on
    // the same tick, and the map redraws only when what is open actually changed.
    if (state.vrfOn) {
      const before = JSON.stringify(state.overlays.map((o) => [o.id, (o.members || []).length]));
      await loadOverlays();
      if (JSON.stringify(state.overlays.map((o) => [o.id, (o.members || []).length])) !== before) draw();
    }
    let rev;
    try { rev = await request("revision"); } catch { return; }   // a missed tick is not an event
    const published = String(rev.published || "");
    if (!published) return;
    if (drawnRevision === null) { drawnRevision = published; return; }
    if (published === drawnRevision) return;
    const from = drawnRevision.slice(0, 8), to = published.slice(0, 8);
    drawnRevision = published;
    await refreshFromKnowledge();
    toast(t("knowledge.revisionMoved").replace("{from}", from).replace("{to}", to));
  }

  /** Redraw from Knowledge, keeping what the person had open. An open transcript is re-fetched because
   *  it may now say something else; an open form is NOT replaced — a person mid-edit loses nothing, and
   *  a banner says the ground moved so they can decide. */
  async function refreshFromKnowledge() {
    const nodeIds = [...state.openNode.values()].flat();
    state.files.clear();
    await loadMap();
    for (const key of state.open) await loadEntries(key);
    if (state.open.length) draw();
    for (const id of nodeIds) await loadFiles(id);
    await loadFlags();
    await loadOverlays();
    loadState();
    const dialog = $("knRawDialog");
    if (!dialog.open || !state.selected) return;
    if ($("knEdit").hidden) {
      await showRaw({ kind: state.selected.kind, title: $("knRawTitle").textContent, address: state.selected.address || "" });
    } else {
      banner(t("knowledge.changedUnderEdit"));
    }
  }

  function watchRevision() {
    if (watchTimer) return;
    watchTimer = setInterval(() => { checkRevision().catch(() => {}); }, WATCH_MS);
    document.addEventListener("visibilitychange", () => {
      if (document.visibilityState !== "visible") return;
      checkRevision().catch(() => {});
      warmEntries().catch(() => {});
    });
    // No immediate check: loadMap has just asked for the revision and seeded `drawnRevision`; the
    // first tick five seconds on is soon enough.
  }

  /** Validation output, verbatim. Errors are what the API refused on; warnings are what it let through
   *  and a person should still see. Neither is summarised — a count would hide which node. */
  function showValidation(result) {
    $("knRawKind").textContent = "VALIDATE";
    $("knRawTitle").textContent = t(result.ok ? "knowledge.validOk" : "knowledge.validBad");
    $("knRawAddr").textContent = "/v1/validate";
    $("knRawMeta").textContent = `${(result.errors || []).length} errors · ${(result.warnings || []).length} warnings`;
    $("knRawKind").className = "kn-chip-kind is-backbone";
    const pane = $("knRaw");
    pane.className = "kn-raw is-" + (result.ok ? "ok" : "bad");
    pane.textContent = [...(result.errors || []).map((e) => "ERROR    " + e),
      ...(result.warnings || []).map((w) => "warning  " + w)].join("\n") || t("knowledge.validOk");
    showEditor(false);
    const dialog = $("knRawDialog");
    if (!dialog.open) dialog.showModal();
  }

  /** The language picker.
   *
   *  Built from the dictionaries that actually loaded rather than from a written-out list, so it can
   *  never offer a language that is not there — and if one fails to load, the menu shrinks instead of
   *  handing someone a choice that does nothing.
   *
   *  Redrawing afterwards is not cosmetic. `apply()` refills every element carrying `data-i18n`, but
   *  the map's tiles and an open transcript are built in JavaScript with `t()` already resolved into
   *  their text, so they would keep the old language until something else happened to rebuild them.
   *  The transcript is replayed the way refreshFromKnowledge does it, from what it is showing —
   *  every `title` it is ever called with is an entity's own name, which is data and does not
   *  translate. Everything open stays open: this changes the words, not where anyone is.
   *
   *  Nothing is sent anywhere. The choice lives in this browser's localStorage, because one install is
   *  a team's ontology and the person at the next desk keeps theirs. */
  function languagePicker() {
    const sel = $("knLang");
    if (!sel || !window.IRISI18N) return;
    const codes = window.IRISI18N.languages();
    // One language is not a choice, and a menu with a single entry is furniture that does nothing.
    if (codes.length < 2) { sel.closest(".kn-lang")?.setAttribute("hidden", ""); return; }
    sel.replaceChildren(...codes.map((code) => {
      const opt = el("option", null, window.IRISI18N.nameOf(code));
      opt.value = code;
      return opt;
    }));
    sel.value = window.IRISI18N.language();
    sel.addEventListener("change", () => {
      // Read the transcript's title BEFORE switching. `knRawTitle` carries a `data-i18n` for the
      // empty state, so `apply()` inside setLanguage overwrites whatever entity name is in it with
      // "Pick something on the map" — and replaying afterwards would put that placeholder up as the
      // title of a card that is plainly showing an area. Caught by switching language with a routing
      // table open, which is exactly the case the replay exists for.
      const open = $("knRawDialog").open && state.selected;
      const title = open ? $("knRawTitle").textContent : "";
      if (!window.IRISI18N.setLanguage(sel.value)) return;
      draw();
      if (open) {
        showRaw({ kind: state.selected.kind, title, address: state.selected.address || "" }).catch(() => {});
      }
    });
  }

  /** Zoom. Steps rather than a slider: the useful sizes are few and a person wants to land on one,
   *  not to hunt for 100% again. The percentage is the reset — pressing the number to go back is what
   *  people try first, and a fourth button for it would be a control for something already on screen. */
  function zoomControls() {
    const out = $("knZoomOut"), pct = $("knZoomReset"), inn = $("knZoomIn");
    if (!out || !pct || !inn) return;
    const paint = () => {
      pct.textContent = `${Math.round(state.zoom * 100)}%`;
      out.disabled = state.zoom <= ZOOM_STEPS[0];
      inn.disabled = state.zoom >= ZOOM_STEPS[ZOOM_STEPS.length - 1];
    };
    const set = (z) => {
      state.zoom = z;
      try { localStorage.setItem(ZOOM_KEY, String(z)); } catch { /* private mode */ }
      paint();
      draw();
    };
    const step = (d) => {
      const i = ZOOM_STEPS.indexOf(state.zoom);
      const next = ZOOM_STEPS[Math.min(Math.max((i < 0 ? ZOOM_STEPS.indexOf(1) : i) + d, 0), ZOOM_STEPS.length - 1)];
      if (next !== state.zoom) set(next);
    };
    out.addEventListener("click", () => step(-1));
    inn.addEventListener("click", () => step(1));
    pct.addEventListener("click", () => { if (state.zoom !== 1) set(1); });
    paint();
  }

  function boot() {
    languagePicker();
    zoomControls();
    $("knCopy").addEventListener("click", async (e) => {
      const b = e.currentTarget;
      try {
        await navigator.clipboard.writeText($("knRaw").textContent || "");
        b.classList.add("is-done");            // the icon turns into a tick for a moment — that is the whole message
        setTimeout(() => b.classList.remove("is-done"), 1400);
      } catch { toast(t("knowledge.copyFailed")); }
    });
    window.addEventListener("pointermove", dragMove);
    window.addEventListener("pointerup", dragEnd);
    window.addEventListener("pointercancel", dragEnd);
    window.addEventListener("keydown", (e) => { if (e.key === "Escape" && drag?.started) dragEnd(e); });

    // The toggle carries the whole editing surface for the map: a file or node swaps the transcript for
    // its record, a Region offers the node it cannot otherwise get.
    // Validation is read-only and free, so it is a button rather than something that happens silently
    // on a write: a person about to publish should be able to ask, and get the errors verbatim.
    $("knValidate").addEventListener("click", (e) => guarded(e.currentTarget, async () => {
      const r = await send("validate", "POST", {});
      showValidation(r);
    }).catch(() => {}));
    $("knPublish").addEventListener("click", (e) => {
      if (!confirm(t("knowledge.publishCore") + "?")) return;
      return guarded(e.currentTarget, async () => { await send("publish", "POST", { what: "core" }); await loadState(); },
        "knowledge.published").catch(() => {});
    });

    $("knRawClose").addEventListener("click", () => $("knRawDialog").close());
    // Closing the transcript deselects, so the map never shows a highlight for a panel that is gone.
    $("knRawDialog").addEventListener("close", () => { state.selected = null; draw(); });

    loadConfig().finally(() => {
      loadState().catch(() => {});
    // The map opens on its own. Nothing is shown until something is clicked — the screen is the map,
    // and the transcript is what a click produces.
      loadMap().catch((e) => toast(`${t("knowledge.loadFailed")} — ${e.message}`));
      watchRevision();
    });
  }

  /** The same two hops, as text. It is deliberately the *same* advertisement the MCP server prints
   *  rather than a second description of the ontology: two descriptions drift, and the one that
   *  drifts is the one nobody is running a check against. */
  async function copyForAgent() {
    try {
      await navigator.clipboard.writeText(await agentContext());
      toast(t("knowledge.copiedForAgent"));
    } catch {
      toast(t("knowledge.copyFailed"));
    }
  }

  /** The starting context, for an agent reached by pasting rather than by a tool call. Built from
   *  the published areas — the same rows, the same conditions, the same rule about absence. */
  async function agentContext() {
    const d = await request("regions");
    const rows = (d.regions || []).map((r) => ({
      address: r.fetch || `/v1/regions/${r.source}`,
      why: r.use_when || r.description || r.title || "",
    }));
    const w = Math.max(7, ...rows.map((r) => r.address.length));
    const api = `${location.origin}/api/knowledge`;
    return [
      "You are answering from an ontology called RouteMind. It is a routing table, not a search index:",
      "you pick an area from the list below, fetch that one area, and read what it points you at.",
      "",
      `Fetch with: GET ${api}<address>   (returns JSON; a document address returns the text)`,
      "",
      `  ${"ADDRESS".padEnd(w)}  WHY YOU WOULD PICK THIS ROW`,
      ...rows.map((r) => `  ${r.address.padEnd(w)}  ${r.why}`),
      "",
      "Use an address exactly as printed. Never build one — every row you fetch prints the addresses",
      "of what is inside it, and those are the only ones that work.",
      "",
      // The service computes this sentence, and it is the only thing that can: whether this list is
      // still the whole world depends on whether every link answered, which only the side that just
      // tried to read them knows. This block used to print the confident version unconditionally —
      // so with a link down it handed an agent "nothing outside this list exists" over a list that
      // was missing rows, which is the one claim the design forbids. The MCP server has always read
      // it from the API (mcp/knowledge_mcp.py, hop0); this is the same fallback, for a service too
      // old to send one.
      d.absence || ("Nothing outside this list exists in RouteMind. This list is the grounds on which you may say\n"
                    + "something is absent; no smaller table is."),
    ].join("\n");
  }

  /** Which door this screen is behind, said by the service and not guessed at.
   *
   *  Three states and three different things to say. `open` is the one worth a word: it is a
   *  legitimate deployment on a network where it is acceptable, and it is also the one where the
   *  README was the only thing that knew. `proxy` shows the name a change will be signed with,
   *  because a person about to sign one should be able to read it first — and it is the only mode
   *  where that name is an identity rather than a signature. */
  function showDoor() {
    const chip = $("knDoor");
    if (!chip) return;
    // Written out rather than assembled from the mode. A key built by concatenation is a key no
    // grep finds and no dictionary check can see: check/i18n-check.mjs reads the screen for the keys
    // it asks for, and a prefix glued to a variable reaches it as the prefix, with nothing after it.
    const DOOR = {
      open: () => [t("knowledge.auth.open"), t("knowledge.auth.open.why"), true],
      token: () => [t("knowledge.auth.token"), t("knowledge.auth.token.why"), false],
      proxy: () => [state.cfg.actor ? t("knowledge.auth.you").replace("{name}", state.cfg.actor)
                                    : t("knowledge.auth.proxy"),
                    t("knowledge.auth.proxy.why"), false],
    };
    const [label, why, loud] = (DOOR[state.cfg.auth] || DOOR.open)();
    chip.textContent = label;
    chip.className = "kn-door" + (loud ? " is-open" : "");
    chip.title = why;
    chip.hidden = !label;
  }

  /** What this install can do. Failure is not fatal and not silent-by-omission either: the defaults
   *  are the conservative ones — no run to start, nothing derived — so a screen that could not ask
   *  shows the controls that always work rather than ones that may not. */
  async function loadConfig() {
    try {
      const cfg = await fetch("/api/app-config", { credentials: "same-origin" }).then((r) => r.json());
      state.cfg = { agent: Boolean(cfg.agent), agentUrl: String(cfg.agent_url || ""), derives: Boolean(cfg.derives),
                    auth: String(cfg.auth || "open"), actor: String(cfg.actor || ""),
                    named: Boolean(cfg.auth_names_the_actor) };
      showDoor();
    } catch { state.cfg = { agent: false, agentUrl: "", derives: false }; }
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot);
  else boot();
})();

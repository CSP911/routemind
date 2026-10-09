#!/usr/bin/env node
// The footprint on the screen: the real static/knowledge.js, a stub DOM, a live record.
//
//   ./check/footprint-screen.mjs <base>      (run by ./check/footprint-screen-check.py)
//
// The page polls `walks?since=N` and opens the map as an agent walks; it replays a kept walk in the
// same order. This drives both the way they happen — steps posted to the record while the page is
// up — and reads what a person would see: which racks are open, which node paths, which tiles carry
// the footprint marks, what the line under the map says. Polls are called by hand rather than on a
// timer, so the no-loss property can be tested by making one poll fail in the middle.
const realFetch = globalThis.fetch;
const realSetInterval = globalThis.setInterval, realClearInterval = globalThis.clearInterval;
import { readFileSync } from "node:fs";
import { dict } from "./dict.mjs";
const BASE = process.argv[2];
const src = readFileSync("static/knowledge.js", "utf8");
const collection = (arr) => { const c = Object.create(null); arr.forEach((x, i) => { c[i] = x; }); c.length = arr.length;
  c[Symbol.iterator] = function* () { yield* arr; }; return c; };
class N { static __all = []; constructor(t) { N.__all.push(this); this.tag = t; this.attrs = {}; this.dataset = {}; this.__kids = []; this.textContent = ""; this.className = ""; this.hidden = false; this.value = ""; this.disabled = false; this.listeners = {}; }
  setAttribute(k, v) { this.attrs[k] = String(v); } append(...n) { this.__kids.push(...n); } replaceChildren(...n) { this.__kids = n; }
  addEventListener(t, f) { (this.listeners[t] ||= []).push(f); } click() { for (const f of this.listeners.click || []) f({ stopPropagation() {}, preventDefault() {}, currentTarget: this }); }
  focus() {} get children() { return collection(this.__kids); } get firstElementChild() { return this.__kids[0] || null; }
  querySelector() { return null; } remove() {}
  get classList() { const s = this; const list = () => String(s.className || "").split(/\s+/).filter(Boolean); const set = (a) => { s.className = [...new Set(a)].join(" "); };
    return { add(...c) { set([...list(), ...c]); }, remove(...c) { set(list().filter((x) => !c.includes(x))); }, contains(c) { return list().includes(c); },
      toggle(c, f) { const on = f === undefined ? !list().includes(c) : !!f; on ? this.add(c) : this.remove(c); return on; } }; } }
// A real store, pre-seeded with what a browser that visited before 2026-10-07 holds: the map cached
// at the current revision, saved before the graph carried `parent`. The page must not draw from it.
const ls = new Map();
globalThis.localStorage = { getItem: (k) => (ls.has(k) ? ls.get(k) : null), setItem: (k, v) => ls.set(k, String(v)), removeItem: (k) => ls.delete(k) };
{
  const rev = await (await realFetch(`${process.argv[2]}/api/knowledge/revision`)).json();
  const graph = await (await realFetch(`${process.argv[2]}/api/knowledge/graph`)).json();
  const regions = await (await realFetch(`${process.argv[2]}/api/knowledge/regions`)).json();
  ls.set("iris.knowledge.map", JSON.stringify({ revision: rev.head, savedAt: Date.now(),
    regions: regions.regions, nodes: graph.nodes.map(({ parent, ...n }) => n), edges: graph.edges, entries: [] }));
}
const ids = ["knTopo","knState","knRawDialog","knRawKind","knRawTitle","knRawAddr","knRawMeta","knRaw","knEdit","knCopy","knRawClose","knRawWrap","knBar","knReview","knViewReview","knCloseReview","knTabs","knList","knValidate","toast","knRawPath","knBanner","knActions","knFp","knFpLive","knFpWalk","knFpSpeed","knFpPlay","knFpTrail","knFpNow","knFpSteps","knFpCard","knHist","knHistBody","knHistPages"];
const byId = {}; for (const id of ids) byId[id] = new N(id);
byId.knFp.hidden = true; byId.knHist.hidden = true;
byId.knRawDialog.open = false; byId.knRawDialog.showModal = function () { this.open = true; }; byId.knRawDialog.close = function () { this.open = false; };
globalThis.document = { readyState: "complete", visibilityState: "hidden", getElementById: (i) => byId[i],
  createElement: (t) => new N(t), createElementNS: (_, t) => new N(t), addEventListener() {}, querySelectorAll: () => [] };
globalThis.window = { addEventListener() {}, IRISI18N: { t: (k, v) => String(dict[k] ?? k).replace(/\{(\w+)\}/g, (_, n) => (v && v[n] != null ? v[n] : `{${n}}`)), apply() {}, lang: () => "en" },
  location: { search: "" } };
globalThis.navigator = {}; globalThis.location = { origin: BASE }; globalThis.confirm = () => false;
globalThis.setInterval = () => 1; globalThis.clearInterval = () => {};
let failNext = 0;
globalThis.fetch = async (url, opts) => {
  if (failNext > 0 && String(url).includes("walks?since=")) { failNext--; throw Object.assign(new Error("injected"), { status: 0 }); }
  const res = await realFetch(BASE + String(url), opts);
  return { ok: res.ok, status: res.status, json: () => res.json(), text: () => res.text(), headers: res.headers };
};
new Function(src.replace('if (document.readyState === "loading")',
  'globalThis.__kn = { state, fp, fpPoll, fpReplay, fpTarget, draw, hist, histLoad };\n  if (document.readyState === "loading")'))();
const kn = globalThis.__kn; const { state, fp } = kn;
const settle = async (n = 40) => { for (let i = 0; i < n; i++) await new Promise((r) => setTimeout(r, 5)); };
const results = []; const check = (name, cond, extra = "") => results.push(`${cond ? "ok  " : "FAIL"} ${name}${cond || !extra ? "" : "   — " + extra}`);
const find = (n, pred, acc = []) => { if (pred(n)) acc.push(n); for (const c of [...(n.children || [])]) find(c, pred, acc); return acc; };
const cls = (n) => `${n.attrs.class || ""} ${n.className || ""}`.split(/\s+/).filter(Boolean);
// The line under the map is one row per walk in view now, so it is read across its children.
const nowText = () => [byId.knFpNow.textContent, ...byId.knFpNow.__kids.map((k) => k.textContent)].join("\n");
const marked = (c) => find(byId.knTopo, (n) => cls(n).includes(c)).map((n) => n.attrs["data-address"] || n.attrs["aria-label"] || "");
const post = async (path, body) => (await realFetch(`${BASE}/api/knowledge/${path}`, { method: "POST", headers: { "Content-Type": "application/json", "X-Knowledge-Actor": "agent-screen" }, body: JSON.stringify(body) })).json();

await settle(); await settle();
check("the map drew", find(byId.knTopo, (n) => cls(n).includes("kn-dev")).length > 0);
check("the footprint bar is shown when the backbone keeps walks", byId.knFp.hidden === false);
check("booted in a hidden tab, the first poll still learned the cursor and opened nothing", fp.cursor !== null && state.open.length === 0, `cursor ${fp.cursor}, open ${state.open}`);
// The page stays hidden while the agent walks — then becomes visible. Before 2026-10-07 the cursor
// was never learned in a hidden tab, so these steps were swallowed as history and never shown.

// ── live: an agent walks while the page is up ─────────────────────────────────
const w = await post("walks", { question: "how far up does a purchase have to be approved", how: "screen-check" });
const steps = [["table", "/v1/regions/procurement", "approval bands are in its sentence"],
               ["table", "/v1/nodes/purchase-request", "the request is where bands live"],
               ["table", "/v1/nodes/approval-threshold", "the band table"],
               ["read", "/v1/nodes/threshold-table/body", "the numbers themselves"]];
await post(`walks/${w.id}/steps`, { op: steps[0][0], address: steps[0][1], why: steps[0][2] });
await kn.fpPoll(); await settle();
check("while hidden, nothing is drawn", state.open.length === 0, String(state.open));
document.visibilityState = "visible";
await kn.fpPoll(); await settle();
check("live: the first step opens its area", state.open.includes("procurement"), String(state.open));
check("  and the line under the map says the step and its reason", nowText().includes("approval bands are in its sentence"), nowText());
// the rest arrive while one poll fails — none may be lost, and they must apply in order
for (const s of steps.slice(1)) await post(`walks/${w.id}/steps`, { op: s[0], address: s[1], why: s[2] });
failNext = 1; await kn.fpPoll(); await settle();
const afterFail = fp.walks.get(w.id).steps.length;
await kn.fpPoll(); await settle(60);
const got = fp.walks.get(w.id).steps.map((s) => s.address).filter(Boolean);
check("live: a failed poll loses nothing — the next one brings every step, in order",
      JSON.stringify(got.slice(-4)) === JSON.stringify(steps.map((s) => s[1])) && afterFail === 2, `${afterFail} then ${JSON.stringify(got)}`);
check("  the node path to the document is open", JSON.stringify(state.openNode.get("procurement")) === JSON.stringify(["purchase-request", "approval-threshold"]),
      JSON.stringify(state.openNode.get("procurement")));
check("  the step it is on now is marked as now", nowText().includes("the numbers themselves"), nowText());
const tiles = find(byId.knTopo, (n) => cls(n).includes("kn-dev"));
const fpTiles = tiles.filter((n) => cls(n).includes("is-fp"));
const nowTiles = tiles.filter((n) => cls(n).includes("is-fp-now"));
check("  the walked tiles carry the footprint mark", fpTiles.length >= 3, `${fpTiles.length} marked`);
check("  exactly one tile is marked as now", nowTiles.length === 1, `${nowTiles.length}`);
// Drawn, not only remembered: each node on the path is a sub-rack on the map, titled with its id.
const topoText = find(byId.knTopo, (n) => n.textContent).map((n) => n.textContent);
check("  and the sub-racks down to the document are drawn on the map", ["purchase-request", "approval-threshold"].every((id) => topoText.includes(`[${id}]`)),
      JSON.stringify(topoText.filter((x) => /threshold|purchase/.test(x))));
check("  even though the browser held a map cached before nodes carried their parent", state.nodes.some((n) => "parent" in n));

// ── the footprint, drawn (2026-10-08) ─────────────────────────────────────────
// The walk as a trace on the map, numbered, with its reason beside the step it is on; everything else
// dimmed while it moves; the steps as a row to jump between; and a card once it stops.
const layerEls = (c) => find(byId.knTopo, (n) => cls(n).includes(c));
const traceSegs = layerEls("kn-fp-trace").filter((n) => cls(n).includes("is-focus"));
// The trace runs along the cables: one path, a piece per stretch of cable, its corners rounded and
// every straight run either level or upright — never a diagonal across the map.
const pieces = (n) => String(n.attrs.d || "").split("M").filter((x) => x.trim()).map((x) => x.trim());
const tracePts = traceSegs.reduce((k, n) => k + pieces(n).length, 0);
check("drawn: the walk is a trace through the tiles it visited", traceSegs.length >= 1 && tracePts >= 4, `${traceSegs.length} paths, ${tracePts} pieces`);
const straights = traceSegs.flatMap((n) => pieces(n).flatMap((pc) => {
  const out = [];
  // `L` endpoints in order; a run is from one to the next with the `Q` corner's control point skipped.
  const toks = ("M " + pc).match(/[MLQ][^MLQ]*/g).map((t) => [t[0], t.slice(1).trim().split(/\s+/).map(Number)]);
  let at = null;
  for (const [op, v] of toks) {
    if (op === "Q") { at = [v[2], v[3]]; continue; }
    if (at && op === "L") out.push([at, [v[0], v[1]]]);
    at = [v[0], v[1]];
  }
  return out;
}));
const diagonal = straights.filter(([a, b]) => Math.abs(a[0] - b[0]) > 0.5 && Math.abs(a[1] - b[1]) > 0.5);
check("  along the map's cables: every straight run level or upright, none across the map", straights.length >= 4 && diagonal.length === 0,
      `${straights.length} runs, ${diagonal.length} diagonal: ${JSON.stringify(diagonal.slice(0, 2))}`);
// …and on the cables themselves, not beside them: the drop from the bus to the area it chose is a run.
const wires = find(byId.knTopo, (n) => cls(n).includes("kn-wire")).flatMap((n) => {
  const p = String(n.attrs.points || "").split(" ").map((xy) => xy.split(",").map(Number));
  return p.slice(1).map((b, i) => [p[i], b]);
});
const onWire = straights.filter(([a, b]) => wires.some(([c, d]) => a[0] === b[0] && c[0] === d[0] && Math.abs(a[0] - c[0]) < 0.5
  && Math.min(a[1], b[1]) < Math.max(c[1], d[1]) && Math.max(a[1], b[1]) > Math.min(c[1], d[1])));
check("  lying on the cables drawn on the map", onWire.length >= 2, `${onWire.length} runs on a cable`);
const badgeNums = layerEls("kn-fp-badge").map((g) => find(g, (n) => n.tag === "text").map((n) => n.textContent).join(""));
check("  each step numbered on its tile, in order", ["1", "2", "3", "4"].every((x) => badgeNums.includes(x)), JSON.stringify(badgeNums));
const bubble = layerEls("kn-fp-bubble").map((g) => find(g, (n) => n.tag === "text").map((n) => n.textContent).join("")).join(" | ");
check("  and the reason for the step it is on, beside it", bubble.includes("the numbers themselves"), bubble);
check("  while it moves, the rest of the map is dimmed", byId.knTopo.classList.contains("is-spot"));
const chips = () => (byId.knFpSteps.__kids || []);
check("the walk is a row of steps under the bar, one per step", chips().length === 1 + steps.length, `${chips().length} chips`);
chips()[2].click(); await settle(60);
check("  pressing a step shows the map as it was at that step", fp.pin && fp.pin.now.address === steps[1][1], JSON.stringify(fp.pin && fp.pin.now));
check("    with the trace stopping there", !layerEls("kn-fp-bubble").map((g) => find(g, (n) => n.tag === "text").map((n) => n.textContent).join("")).join("").includes("the numbers themselves"));
byId.knFpLive.click(); await settle();
check("  and Live goes back to the walk as it is", fp.pin === null);
await post(`walks/${w.id}/close`, { outcome: "answered", why: "the band table answered it" });
await kn.fpPoll(); await settle();
check("once the walk ends, a card says how it went", byId.knFpCard.hidden === false
      && find(byId.knFpCard, (n) => String(n.textContent).includes(dict["knowledge.fp.out.answered"] || "Answered")).length > 0,
      find(byId.knFpCard, (n) => n.textContent).map((n) => n.textContent).join(" | "));
const traceAfter = layerEls("kn-fp-trace").filter((n) => cls(n).includes("is-focus"));
check("  and the close is an outcome, not a step: the trace does not run back to hop 0",
      traceAfter.reduce((k, n) => k + pieces(n).length, 0) === tracePts);

// ── replay ────────────────────────────────────────────────────────────────────
state.open = []; state.openNode.clear(); kn.draw();
const seen = [];
const watch = realSetInterval(() => { const t = nowText(); if (t.trim() && seen.at(-1) !== t) seen.push(t); }, 50);
byId.knFpWalk.value = w.id;
await kn.fpReplay();
realClearInterval(watch);
const order = steps.map((s) => s[2]).filter((why) => seen.some((t) => t.includes(why)));
check("replay: every step is shown again", order.length === steps.length, JSON.stringify(seen));
check("  in the order it was walked", seen.map((t) => steps.findIndex((s) => t.includes(s[2]))).filter((i) => i >= 0).every((v, i, a) => i === 0 || v >= a[i - 1]), JSON.stringify(seen));
check("  and leaves the map open where the walk ended", state.open.includes("procurement") && (state.openNode.get("procurement") || []).includes("approval-threshold"));
check("  the replay button is usable again afterwards", byId.knFpPlay.disabled === false && !fp.replay);

// ── several walks at once ─────────────────────────────────────────────────────
// The live view used to follow whichever walk had moved last, so a second agent pulled the screen
// away from the first. Every recent walk is on the map now, each in its own colour.
byId.knFpWalk.value = ""; fp.focus = "";
const w2 = await post("walks", { question: "what counts as a receipt", how: "screen-check" });
await post(`walks/${w2.id}/steps`, { op: "table", address: "/v1/regions/expense", why: "receipts are in its sentence" });
await kn.fpPoll(); await settle(60);
const tilesNow = () => find(byId.knTopo, (n) => cls(n).includes("kn-dev"));
const colours = () => new Set(tilesNow().flatMap((n) => cls(n).filter((c) => /^is-fp-c\d$/.test(c))));
check("several walks: the second walk opens its own area", state.open.includes("expense") && state.open.includes("procurement"), String(state.open));
check("  both walks are on the map, in two colours", colours().size === 2, JSON.stringify([...colours()]));
check("  each marked where it is now", tilesNow().filter((n) => cls(n).includes("is-fp-now")).length === 2,
      String(tilesNow().filter((n) => cls(n).includes("is-fp-now")).length));
check("  and the line under the map has a row for each", nowText().includes("the numbers themselves") && nowText().includes("receipts are in its sentence"), nowText());
fp.focus = w2.id; kn.draw();
check("choosing one walk shows that walk alone", colours().size === 1, JSON.stringify([...colours()]));
fp.focus = ""; kn.draw();

// ── a replay keeps the walk's rhythm ──────────────────────────────────────────
// It was a fixed 0.9 s a step, so a walk that stopped to think looked exactly like one that did not.
const w3 = await post("walks", { question: "a walk that pauses", how: "screen-check" });
await post(`walks/${w3.id}/steps`, { op: "table", address: "/v1/regions/payroll", why: "before the pause" });
await new Promise((r) => setTimeout(r, 1500));
await post(`walks/${w3.id}/steps`, { op: "table", address: "/v1/regions/attendance", why: "after the pause" });
byId.knFpWalk.value = w3.id;
byId.knFpSpeed.value = "1"; let t0 = Date.now(); await kn.fpReplay(); const slow = Date.now() - t0;
byId.knFpSpeed.value = "8"; t0 = Date.now(); await kn.fpReplay(); const fast = Date.now() - t0;
check("replay: a 1.5 s pause takes about 1.5 s at 1×", slow >= 1300, `${slow} ms`);
check("  and much less at 8×", fast < slow / 3, `${fast} ms against ${slow} ms`);
byId.knFpSpeed.value = "1";
t0 = Date.now(); const running = kn.fpReplay(); await new Promise((r) => setTimeout(r, 250));
await kn.fpReplay(); await running; const stopped = Date.now() - t0;
check("  the same button stops it", stopped < 1000 && !fp.replay, `${stopped} ms`);

// ── replaying every walk together ─────────────────────────────────────────────
byId.knFpWalk.value = ""; byId.knFpSpeed.value = "8";
const seenAll = [];
const watchAll = realSetInterval(() => { const t = nowText(); if (t.trim() && seenAll.at(-1) !== t) seenAll.push(t); }, 20);
await kn.fpReplay();
realClearInterval(watchAll);
check("replaying all walks shows every walk's steps", ["the numbers themselves", "receipts are in its sentence", "after the pause"].every((why) => seenAll.some((t) => t.includes(why))),
      JSON.stringify(seenAll.slice(-3)));

// ── the history under the map ─────────────────────────────────────────────────
check("history: shown when the backbone keeps walks", byId.knHist.hidden === false);
for (let i = 0; i < 11; i++) await post("walks", { question: `history filler ${i}`, how: "screen-check" });
await kn.histLoad(0); await settle();
const histRows = () => byId.knHistBody.__kids.filter((r) => cls(r).includes("kn-hist-row"));
const rowText = (r) => find(r, (n) => n.textContent).map((n) => n.textContent).join(" | ");
check("  ten rows to a page, newest first", histRows().length === 10 && rowText(histRows()[0]).includes("history filler 10"),
      `${histRows().length} rows; first: ${histRows()[0] && rowText(histRows()[0])}`);
const pageBtns = () => byId.knHistPages.__kids.filter((b) => cls(b).includes("kn-hist-page"));
check("  with pages to move through once there are more than ten", byId.knHistPages.hidden === false && pageBtns().some((b) => b.textContent === "2"),
      pageBtns().map((b) => b.textContent).join(" "));
const firstPage = histRows().map((r) => r.dataset.walk);
pageBtns().find((b) => b.textContent === "2").click(); await settle();
check("  page 2 holds the older walks, none from page 1", kn.hist.page === 1 && histRows().length >= 4 && !histRows().some((r) => firstPage.includes(r.dataset.walk)),
      `page ${kn.hist.page}, ${histRows().length} rows`);
const old = histRows().find((r) => r.dataset.walk === w.id);
check("  the first walk is there, summarised", old && rowText(old).includes("how far up does a purchase") && rowText(old).includes(dict["knowledge.fp.out.answered"] || "Answered"),
      old ? rowText(old) : "not on page 2");
const showBtn = old && find(old, (n) => n.tag === "button" && n.textContent === (dict["knowledge.hist.show"] || "knowledge.hist.show"))[0];
showBtn && showBtn.click(); await settle();
check("  'show on the map' pins that walk at its last step, and marks its row", fp.focus === w.id && fp.pin && fp.pin.now.address === steps.at(-1)[1] && cls(old).includes("is-sel"),
      JSON.stringify({ focus: fp.focus, pin: fp.pin && fp.pin.now }));
pageBtns().find((b) => cls(b).includes("is-prev")).click(); await settle();
check("  and ‹ goes back to page 1", kn.hist.page === 0 && histRows()[0].dataset.walk === firstPage[0]);

console.log(results.join("\n"));
const n = results.filter((r) => r.startsWith("FAIL")).length;
console.log(`\n${n} failed of ${results.length}`);
process.exit(n ? 1 : 0);

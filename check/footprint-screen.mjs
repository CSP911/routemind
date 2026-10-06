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
globalThis.localStorage = { getItem: () => null, setItem() {}, removeItem() {} };
const ids = ["knTopo","knState","knRawDialog","knRawKind","knRawTitle","knRawAddr","knRawMeta","knRaw","knEdit","knCopy","knRawClose","knRawWrap","knBar","knReview","knViewReview","knCloseReview","knNap","knSleep","knTabs","knList","knValidate","knPublish","toast","knRawPath","knBanner","knActions","knWallPanel","knWallMine","knWallTheirs","knWallCount","knExport","knExportDialog","knExportForm","knExportPass","knExportPass2","knExportMsg","knExportGo","knExportClose","knExportCancel","knFp","knFpLive","knFpWalk","knFpPlay","knFpTrail","knFpNow"];
const byId = {}; for (const id of ids) byId[id] = new N(id);
byId.knFp.hidden = true; byId.knWallPanel.hidden = true;
byId.knRawDialog.open = false; byId.knRawDialog.showModal = function () { this.open = true; }; byId.knRawDialog.close = function () { this.open = false; };
byId.knExportDialog.showModal = function () {}; byId.knExportDialog.close = function () {};
globalThis.document = { readyState: "complete", visibilityState: "visible", getElementById: (i) => byId[i],
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
  'globalThis.__kn = { state, fp, fpPoll, fpReplay, fpTarget, draw };\n  if (document.readyState === "loading")'))();
const kn = globalThis.__kn; const { state, fp } = kn;
const settle = async (n = 40) => { for (let i = 0; i < n; i++) await new Promise((r) => setTimeout(r, 5)); };
const results = []; const check = (name, cond, extra = "") => results.push(`${cond ? "ok  " : "FAIL"} ${name}${cond || !extra ? "" : "   — " + extra}`);
const find = (n, pred, acc = []) => { if (pred(n)) acc.push(n); for (const c of [...(n.children || [])]) find(c, pred, acc); return acc; };
const cls = (n) => `${n.attrs.class || ""} ${n.className || ""}`.split(/\s+/).filter(Boolean);
const marked = (c) => find(byId.knTopo, (n) => cls(n).includes(c)).map((n) => n.attrs["data-address"] || n.attrs["aria-label"] || "");
const post = async (path, body) => (await realFetch(`${BASE}/api/knowledge/${path}`, { method: "POST", headers: { "Content-Type": "application/json", "X-Knowledge-Actor": "agent-screen" }, body: JSON.stringify(body) })).json();

await settle(); await settle();
check("the map drew", find(byId.knTopo, (n) => cls(n).includes("kn-dev")).length > 0);
check("the footprint bar is shown when the backbone keeps walks", byId.knFp.hidden === false);
check("the first poll learned the cursor and opened nothing", fp.cursor !== null && state.open.length === 0, `cursor ${fp.cursor}, open ${state.open}`);

// ── live: an agent walks while the page is up ─────────────────────────────────
const w = await post("walks", { question: "how far up does a purchase have to be approved", how: "screen-check" });
const steps = [["table", "/v1/regions/procurement", "approval bands are in its sentence"],
               ["table", "/v1/nodes/purchase-request", "the request is where bands live"],
               ["table", "/v1/nodes/approval-threshold", "the band table"],
               ["read", "/v1/nodes/threshold-table/body", "the numbers themselves"]];
await post(`walks/${w.id}/steps`, { op: steps[0][0], address: steps[0][1], why: steps[0][2] });
await kn.fpPoll(); await settle();
check("live: the first step opens its area", state.open.includes("procurement"), String(state.open));
check("  and the line under the map says the step and its reason", byId.knFpNow.textContent.includes("approval bands are in its sentence"), byId.knFpNow.textContent);
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
check("  the step it is on now is marked as now", byId.knFpNow.textContent.includes("the numbers themselves"), byId.knFpNow.textContent);
const tiles = find(byId.knTopo, (n) => cls(n).includes("kn-dev"));
const fpTiles = tiles.filter((n) => cls(n).includes("is-fp"));
const nowTiles = tiles.filter((n) => cls(n).includes("is-fp-now"));
check("  the walked tiles carry the footprint mark", fpTiles.length >= 3, `${fpTiles.length} marked`);
check("  exactly one tile is marked as now", nowTiles.length === 1, `${nowTiles.length}`);

// ── replay ────────────────────────────────────────────────────────────────────
state.open = []; state.openNode.clear(); kn.draw();
const seen = [];
const watch = realSetInterval(() => { const t = byId.knFpNow.textContent; if (t && seen.at(-1) !== t) seen.push(t); }, 50);
byId.knFpWalk.value = w.id;
await kn.fpReplay();
realClearInterval(watch);
const order = steps.map((s) => s[2]).filter((why) => seen.some((t) => t.includes(why)));
check("replay: every step is shown again", order.length === steps.length, JSON.stringify(seen));
check("  in the order it was walked", seen.map((t) => steps.findIndex((s) => t.includes(s[2]))).filter((i) => i >= 0).every((v, i, a) => i === 0 || v >= a[i - 1]), JSON.stringify(seen));
check("  and leaves the map open where the walk ended", state.open.includes("procurement") && (state.openNode.get("procurement") || []).includes("approval-threshold"));
check("  the replay button is usable again afterwards", byId.knFpPlay.disabled === false);

console.log(results.join("\n"));
const n = results.filter((r) => r.startsWith("FAIL")).length;
console.log(`\n${n} failed of ${results.length}`);
process.exit(n ? 1 : 0);

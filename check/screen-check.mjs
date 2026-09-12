const realFetch = globalThis.fetch;
import { readFileSync } from "node:fs";
import { dict } from "./dict.mjs";
const BASE = process.argv[2] || "http://127.0.0.1:8080";
const src = readFileSync("static/knowledge.js", "utf8");
const collection = (arr) => { const c = Object.create(null); arr.forEach((x,i)=>{c[i]=x;}); c.length=arr.length;
  c[Symbol.iterator]=function*(){ yield* arr; }; return c; };
class N { static __all=[]; constructor(t){ N.__all.push(this);this.tag=t;this.attrs={};this.dataset={};this.__kids=[];this.textContent="";this.className="";this.hidden=false;this.value="";this.listeners={};}
  setAttribute(k,v){this.attrs[k]=String(v);} append(...n){this.__kids.push(...n);} replaceChildren(...n){this.__kids=n;}
  addEventListener(t,f){(this.listeners[t]||=[]).push(f);} click(){for(const f of this.listeners.click||[]) f({stopPropagation(){},preventDefault(){}});}
  focus(){} get children(){return collection(this.__kids);} get firstElementChild(){return this.__kids[0]||null;} querySelector(sel){ const m=/^:scope > \.([\w-]+)$/.exec(sel||""); if(!m) return null; return this.__kids.find((c)=>new RegExp("(^| )"+m[1]+"( |$)").test(c.className||""))||null; } remove(){ for(const p of N.__all) { const i=p.__kids.indexOf(this); if(i>=0) p.__kids.splice(i,1); } } get classList(){const s=this;return{add(c){s.className+=" "+c;},remove(){}};} }
globalThis.localStorage={getItem:()=>null,setItem(){},removeItem(){}};
const byId={}; for (const id of ["knTopo","knState","knRawDialog","knRawKind","knRawTitle","knRawAddr","knRawMeta","knRaw","knEdit","knCopy","knRawClose","knRawWrap","knBar","knReview","knViewReview","knCloseReview","knNap","knSleep","knTabs","knList","knValidate","knPublish","toast","knRawPath","knBanner","knActions"]) byId[id]=new N(id);
let opens=0; byId.knRawDialog.open=false; byId.knRawDialog.showModal=function(){this.open=true;opens++;}; byId.knRawDialog.close=function(){this.open=false;};
globalThis.document={readyState:"complete",visibilityState:"visible",getElementById:(i)=>byId[i],createElement:(t)=>new N(t),createElementNS:(_,t)=>new N(t),addEventListener(){}};
globalThis.__nav=[]; globalThis.window={addEventListener(){},IRISI18N:{t:(k)=>dict[k] ?? k},location:{search:"",set href(v){globalThis.__nav.push(v);},get href(){return "";}}}; globalThis.navigator={}; globalThis.location={origin:BASE}; globalThis.confirm=()=>false; globalThis.setInterval=()=>1;
// setTimeout is left real. The IRIS harness stubs it away to stop the revision watcher, but this
// check talks to a live server and node's own fetch schedules its socket timeouts through it — a
// no-op setTimeout takes undici down inside the first request.
globalThis.fetch = async (url, opts) => {
  const res = await realFetch(BASE + String(url), opts);
  return { ok: res.ok, status: res.status, json: () => res.json(), text: () => res.text() };
};
new Function(src.replace('if (document.readyState === "loading")','globalThis.__kn = { state, loadEntries, loadFiles, draw, agentContext };\n  if (document.readyState === "loading")'))();
const kn = globalThis.__kn; const { state, loadEntries, loadFiles, draw } = kn;
const settle = async () => { for (let i = 0; i < 40; i++) await new Promise((r) => setTimeout(r, 5)); };

// The screen, against this install. Everything below is what a person sees on the map — not what the
// API returned, which the API's own smoke already covers.
await settle(); await settle();
const results = []; const check = (n, c) => results.push(`${c ? "ok  " : "FAIL"} ${n}`);
const find = (n, pred, acc = []) => { if (pred(n)) acc.push(n); for (const c of [...(n.children || [])]) find(c, pred, acc); return acc; };
const cls = (n) => String(n.attrs.class || "").split(/\s+/);
const texts = () => find(byId.knTopo, (n) => n.textContent).map((n) => n.textContent);

check("the map drew", find(byId.knTopo, (n) => cls(n).includes("kn-dev")).length > 0);
check("the backbone is there", texts().includes("Knowledge Back-Bone"));
// Whatever this install holds, the map shows exactly that. Naming a particular area would tie the
// check to one person's data and pass vacuously on an empty install — which is the default one.
const live = await (await realFetch(BASE + "/api/knowledge/regions")).json();
// From `fetch`, not `source`: `source` looks like the directory and is not — hyphens come back
// as underscores, so using it as a name produces one that does not exist.
const areas = (live.regions || []).map((r) => String(r.fetch).split("/").pop());
check(`every area the API has is on the map (${areas.length})`, areas.every((a) => texts().includes(a)));
check("the config was read", state.cfg && typeof state.cfg.derives === "boolean");

// Picking exists where a pick can go somewhere — a run to start, or an overlay to draw. Asserted in
// whichever direction this install is configured for, because the interesting failure is the button
// that is there and goes nowhere.
const agent = Boolean(state.cfg.agent);
const overlaysHere = (await realFetch(BASE + "/api/knowledge/overlays?state=open")).status === 200;
const canPick = agent || overlaysHere;
// A tick box is drawn on an area, so an install with no areas has none whichever way it is
// configured — asserting "present" there failed the default install rather than the screen.
if (areas.length) {
  check(`tick boxes ${canPick ? "present" : "absent"} (agent ${agent}, overlays ${overlaysHere})`,
    (find(byId.knTopo, (n) => cls(n).includes("kn-pick")).length > 0) === canPick);
} else {
  results.push("--   no areas yet; there is nothing to draw a tick box on");
}

// Open the area: its rack, its node, and the node's document.
const dev = (label) => find(byId.knTopo, (n) => cls(n).includes("kn-dev") && [...n.children].some((c) => c.textContent === label))[0];
const first = areas.length ? dev(areas[0]) : null;
if (!areas.length) results.push("--   no areas yet; the rack half of this check needs one");
if (first) {
  first.click(); await settle(); await settle();
  check("its rack opened", find(byId.knTopo, (n) => cls(n).includes("kn-rack")).length === 1);
  const entries = await (await realFetch(BASE + "/api/knowledge/regions/" + areas[0])).json();
  const names = (entries.entries || []).map((e) => String(e.name || e.id));
  // A tile's label is fitted to the tile and ends in "…" when it does not fit — deliberately. So a
  // name is drawn if some label is the name, or is the name cut short. Requiring the whole name
  // failed the moment an entity had a long one, which under one type is any document whose LLM
  // description became its name.
  const drawnAs = (n) => texts().some((t) => t.includes(n) || (t.endsWith("…") && n.startsWith(t.slice(0, -1))));
  check(`everything in that area is drawn (${names.length})`, names.every(drawnAs));
  check("the rack still offers making things", texts().some((t) => /New node/.test(t)));
  // The start button lives on the rack, so this is the first moment it could exist at all — checking
  // before the rack was open asked about an empty set and passed in both modes.
  check(`start button ${agent ? "present" : "absent"}`,
    texts().some((t) => /Agentic AI/.test(t)) === agent);
}
// The status bar. It is the first line a person reads, so what it says when nothing is wrong
// matters as much as what it says when something is: it used to carry a raw environment variable
// from an optional subsystem on every default install.
const bar = find(byId.knState, () => true).map((n) => n.textContent).join(" ");
check("the status bar is not showing a raw error", !/not configured|HTTP \d|undefined/.test(bar));
const st = await (await realFetch(BASE + "/api/knowledge/state")).json();
check("read-only is reported either way", typeof st.writable === "boolean");
check("the bar warns only when it should", /read-only/.test(bar) === (st.writable === false));
// And says nothing at all when nothing is wrong: every write validates and publishes on its own, so a
// clean, published, valid tree leaves a person nothing to do there.
const ps = await (await realFetch(BASE + "/api/knowledge/publish-state")).json();
const quiet = st.writable !== false && (ps.core || {}).in_sync === true && (ps.validate || {}).ok === true;
check(`the bar is ${quiet ? "hidden — nothing is wrong" : "shown — something is"}`, byId.knBar.hidden === quiet);

// The third way in: the same starting block as text, for an agent with no MCP. Checked for being
// the *same* advertisement, not merely for existing — two descriptions of one ontology drift.
const ctx = await kn.agentContext?.() ?? null;
if (ctx === null) check("agentContext is exported for checking", false);
else {
  check("the pasted block names every area", areas.every((a) => ctx.includes(a)));
  check("it carries a fetchable base URL", /\/api\/knowledge/.test(ctx));
  check("it repeats the absence rule, and only for the whole list",
    /grounds on which you may say/.test(ctx) && /no smaller table/.test(ctx));
  check("it tells the agent not to build addresses", /Never build one/.test(ctx));
}

// The VRF chips are drawn in the map's own coordinates, in the top-left corner, and the map is
// shifted down to leave that corner to them. Before that reservation existed the core's left
// management host sat at x 224..364, y 39..73 — under the first chip and squarely under the second,
// and since the chips are appended first the tile was painted over them. Nothing failed; it just
// looked wrong, which is why it lasted. Simulated rather than taken from the install, because the
// number of open VRFs on any given install is not something a check may depend on — and one open
// overlay is exactly the case that only grazes it.
{
  const rects = (owner) => { const out = []; const walk = (n, own) => {
      const c = String(n.attrs.class || ""); const o = c || own;
      if (n.tag === "rect") { const b = ["x","y","width","height"].map((k) => Number(n.attrs[k]));
        if (b.every((v) => !Number.isNaN(v))) out.push({ o, x: b[0], y: b[1], w: b[2], h: b[3] }); }
      for (const k of [...(n.children || [])]) walk(k, o); }; walk(byId.knTopo, ""); return out.filter(owner); };
  const live = state.overlays;
  let clashes = 0, drawn = 0;
  for (const n of [1, 2, 3, 5]) {
    state.overlays = Array.from({ length: n }, (_, i) => ({ id: `sim${i}`, question: "a question long enough to reach the chip width cap, as a real one is", by: { name: "agent" }, members: [1, 2, 3] }));
    draw();
    const chips = rects((b) => /kn-vrf-chip/.test(b.o)), rest = rects((b) => !/kn-vrf-chip/.test(b.o));
    drawn += chips.length;
    for (const c of chips) for (const r of rest)
      if (c.x < r.x + r.w && r.x < c.x + c.w && c.y < r.y + r.h && r.y < c.y + c.h) clashes++;
  }
  state.overlays = live; draw();
  check("a VRF chip is drawn per open overlay", drawn === 1 + 2 + 3 + 5);
  check("and the map leaves that corner to them", clashes === 0);
}

// "Advertise upstream" files a proposal, and a proposal needs the curator — ONTOLOGY_HARNESS. Unset,
// every such call answers 501, and until 2026-09-12 the action was offered anyway: the button sat
// between two that are drawn conditionally, and pressing it put the name of an environment variable
// on screen. Asserted in both directions, because the failure that lasted was the affordance that is
// there and cannot work; a check that only proves it appears would have passed throughout.
{
  const shown = () => { let n = 0;
    const walk = (x) => { if (x.textContent && /Advertise upstream/.test(x.textContent)) n++;
                          for (const c of [...(x.children || [])]) walk(c); };
    walk(byId.knTopo); walk(byId.knEdit); return n; };
  if (!areas.length) results.push("--   no areas yet; the advertise-upstream gate needs one");
  else {
    const was = state.curatorOn;
    const seen = {};
    for (const on of [true, false]) {
      // Two traps, and both read as "correctly hidden" rather than as a broken check. The tile is
      // looked up after the redraw, because `draw()` replaces the tree and a node held across it is
      // detached. And clicking a rack that is already open closes it — the checks above this one
      // leave the first area open — so it is only clicked when it is shut.
      state.curatorOn = on; draw();
      if (!state.open.includes(areas[0])) { const tile = dev(areas[0]); if (tile) tile.click(); }
      await settle();
      seen[on] = shown();
    }
    state.curatorOn = was; draw();
    check("advertise-upstream is offered where there is a curator", seen[true] > 0);
    check("and not offered where there is none", seen[false] === 0);
  }
}

console.log(results.join("\n"));
process.exit(results.some((r) => r.startsWith("FAIL")) ? 1 : 0);

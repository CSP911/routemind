// Every class the screen puts on an element, against every class the stylesheets define.
//
//   node check/css-check.mjs
//
// Two bugs of exactly this shape shipped, and neither could be caught by any check that talks to the
// API, because the markup and the JavaScript were both correct:
//
//   * `.kn-chip` had no rule at all. Five places build a row of them, and the Draw-a-VRF card lists
//     the addresses in the set — so two areas rendered as `/v1/regions/expense/v1/regions/payroll`,
//     one string shaped exactly like an address, in a product whose every table says never to build
//     one.
//   * `.toast` had a colour in theme.css and nothing else — no position, no hidden state, and no rule
//     for `.show`, the one class the code adds and removes. Every message the screen has ever raised
//     rendered as a line of text in the page flow and then stayed there.
//
// A class with no rule is not always a bug: some are hooks that only JavaScript queries, and some are
// on elements hidden another way. Those go in KNOWN below **with the reason**, so the list stays a
// list of decisions rather than a list of things someone silenced.
import { readFileSync, readdirSync } from "node:fs";

const read = (p) => readFileSync(new URL(p, import.meta.url), "utf8");
const js = read("../static/knowledge.js");
const html = read("../static/knowledge.html");
const css = readdirSync(new URL("../static/", import.meta.url))
  .filter((f) => f.endsWith(".css"))
  .map((f) => read("../static/" + f))
  .join("\n")
  .replace(/\/\*[\s\S]*?\*\//g, "");

// A class that only ever exists with a state suffix — `is-${kind}` — cannot be checked by name, and
// the fragment left behind is not a class anyone wrote.
const used = new Set();
// A template literal may hold a double quote inside its `${...}` — `is-${x === "ok" ? …}` — so the two
// quoting styles are read separately, and only tokens shaped like a class name are kept. Reading them
// together captured `kn-raw is-${view.status === ` and reported `===` as an unstyled class.
const NAME = /^-?[_a-zA-Z][\w-]*$/;
const add = (s) => String(s).replace(/\$\{[^}]*\}/g, " ").split(/\s+/)
  .forEach((c) => { if (NAME.test(c) && c !== "is-") used.add(c); });
for (const m of js.matchAll(/\bel\(\s*"[^"]*"\s*,\s*"([^"]*)"/g)) add(m[1]);
for (const m of js.matchAll(/class:\s*"([^"]*)"/g)) add(m[1]);
for (const m of js.matchAll(/class:\s*`([^`]*)`/g)) add(m[1]);
for (const m of js.matchAll(/className\s*=\s*"([^"]*)"/g)) add(m[1]);
for (const m of js.matchAll(/className\s*=\s*`([^`]*)`/g)) add(m[1]);
for (const m of js.matchAll(/classList\.add\(\s*"([^"]*)"/g)) add(m[1]);
for (const m of html.matchAll(/class="([^"]*)"/g)) add(m[1]);

const defined = new Set([...css.matchAll(/\.(-?[_a-zA-Z][\w-]*)/g)].map((m) => m[1]));

// Deliberately unstyled. Each line is a decision, not a silencing.
const KNOWN = new Map([
  ["kn-file", "the native file input, hidden in JS (`picker.hidden = true`) — the visible control is a button beside it"],
  ["kn-map-panel", "a hook on the map section; `.panel` beside it carries the styling"],
  ["kn-id-note", "a modifier beside `.kn-fhint`, which carries the styling"],
  ["kn-draft-notes", "a bare wrapper in the proposal card; its children carry their own spacing"],
  ["is-fp-c", "the stem of `is-fp-c0`…`is-fp-c7`, a walk's colour, built from its number; each is styled"],
]);

const missing = [...used].filter((c) => !defined.has(c)).sort();
const unexplained = missing.filter((c) => !KNOWN.has(c));
const stale = [...KNOWN.keys()].filter((c) => defined.has(c));

for (const c of missing.filter((c) => KNOWN.has(c))) console.log(`--   ${c} has no rule, on purpose — ${KNOWN.get(c)}`);
for (const c of stale) console.log(`--   ${c} is in KNOWN but now has a rule; drop the entry`);

if (unexplained.length) {
  console.log(`FAIL ${unexplained.length} class(es) the screen sets have no rule in any stylesheet:\n  ` +
    unexplained.join("\n  ") +
    `\n  Either style them, or add them to KNOWN in this file with the reason they need none.`);
  process.exit(1);
}
// A `var(--name)` whose name no stylesheet ever defines.
//
// This one hides behind its own fallback. `var(--kn-ok, #1c6b3f)` renders a perfectly good green, so
// the page looks right and nothing complains — but the token does not exist, so the fallback is the
// only value it will ever have. The element is then pinned to one hard-coded colour while everything
// around it moves, and nothing on screen says so. The export dialog was written this way and was
// caught only by reading the computed style of an element that looked entirely correct.
//
// The nine below predate this check. They are not approved, they are recorded: each is a hard-coded
// colour wearing a token's name, and each will need a real token or a real value. What the list is
// for is that a tenth cannot be added without deciding to add it here.
const NO_SUCH_TOKEN = new Set([
  "--accent", "--danger", "--dim", "--fg", "--line-strong",
  "--warn", "--warn-bg", "--warn-fg", "--warn-line",
]);
const declared = new Set([...css.matchAll(/(--[\w-]+)\s*:/g)].map((m) => m[1]));
const referenced = new Set([...css.matchAll(/var\(\s*(--[\w-]+)/g)].map((m) => m[1]));
const phantom = [...referenced].filter((n) => !declared.has(n) && !NO_SUCH_TOKEN.has(n)).sort();
const fixed = [...NO_SUCH_TOKEN].filter((n) => declared.has(n)).sort();
for (const n of fixed) console.log(`--   ${n} is in NO_SUCH_TOKEN but is now defined; drop the entry`);
if (phantom.length) {
  console.log(`FAIL ${phantom.length} CSS variable(s) used but never defined:\n  ` + phantom.join("\n  ") +
    `\n  Each renders from its fallback and never changes with the theme. Use a token that exists, ` +
    `define this one, or add it to NO_SUCH_TOKEN in this file.`);
  process.exit(1);
}
console.log(`ok   ${referenced.size} CSS variables referenced, ${NO_SUCH_TOKEN.size} known-undefined and no new ones`);
console.log(`ok   ${used.size} classes on screen, every one styled or explained`);

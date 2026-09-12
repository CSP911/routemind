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
console.log(`ok   ${used.size} classes on screen, every one styled or explained`);

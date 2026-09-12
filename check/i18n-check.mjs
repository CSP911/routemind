// The dictionaries, against each other and against the screen.
//
//   node check/i18n-check.mjs
//
// Three failures, each of which has actually happened or becomes possible the moment a second
// language exists:
//
//   * **A key defined twice.** In a JavaScript object literal the LAST definition wins, silently.
//     New strings were being added at the front of the dictionary, so every "change" to an existing
//     string added a second copy that lost to the original further down — five fixes reported as done
//     never reached the screen, among them the renamed "Draft it" button. A check of the code saw the
//     right key; nothing looked at what renders.
//   * **A key in a translation that is not in English.** English is the baseline and the per-key
//     fallback, so a key only a translation has is a string nobody will ever see — usually a rename
//     that was applied to one file and not the others, and the English screen quietly lost a label.
//   * **A key the screen asks for that no dictionary has.** It renders as its own dotted identifier.
//
// A key MISSING from a translation is reported and does not fail. That is the design: the screen
// falls back to English per key, so a half-finished language degrades to English rather than to
// blanks, and a new string must not be blocked on being translated four times before it can ship.
import { readFileSync, readdirSync } from "node:fs";
import { dictionaries, files } from "./dict.mjs";

const DIR = new URL("../static/i18n/", import.meta.url);
let bad = false;

// Duplicates are invisible to the evaluated object — by the time it is an object, the loser is gone.
// So this reads the text.
for (const f of files) {
  const src = readFileSync(new URL(f, DIR), "utf8");
  const keys = [...src.matchAll(/^\s*"((?:[^"\\]|\\.)*)"\s*:/gm)].map((m) => m[1]);
  const count = keys.reduce((m, k) => m.set(k, (m.get(k) || 0) + 1), new Map());
  const dup = [...count].filter(([, n]) => n > 1).map(([k]) => k);
  if (dup.length) {
    bad = true;
    console.log(`FAIL ${f}: ${dup.length} key(s) defined twice — the later one wins:\n  ` + dup.join("\n  "));
  }
}

const base = new Set(Object.keys(dictionaries.en));
const others = Object.keys(dictionaries).filter((c) => c !== "en").sort();

for (const code of others) {
  const keys = Object.keys(dictionaries[code]);
  const extra = keys.filter((k) => !base.has(k)).sort();
  const missing = [...base].filter((k) => !(k in dictionaries[code])).sort();
  const done = base.size - missing.length;
  const pct = base.size ? Math.round((done / base.size) * 100) : 0;

  if (extra.length) {
    bad = true;
    console.log(`FAIL ${code}: ${extra.length} key(s) not in English — nothing will ever read them:\n  ` +
      extra.join("\n  ") + `\n  Either add them to static/i18n/en.js, or delete them here.`);
  }
  if (missing.length) {
    // Not a failure. Named anyway, up to a handful, so "80%" is a list of work and not a mood.
    const show = missing.slice(0, 8);
    console.log(`--   ${code}: ${done}/${base.size} (${pct}%) — falls back to English for ${missing.length}: ` +
      show.join(", ") + (missing.length > show.length ? `, +${missing.length - show.length} more` : ""));
  } else {
    console.log(`ok   ${code}: ${done}/${base.size} (100%)`);
  }
}

// A translation that drops a placeholder renders a broken sentence — "removing /  — …" — and one
// that invents a placeholder renders the braces literally, because `format()` leaves an unknown name
// as `{name}` rather than guessing. Both look like a translation bug to a reader and like nothing at
// all to a reviewer skimming a language they do not read, so they are checked rather than trusted.
const holders = (text) => [...String(text).matchAll(/\{(\w+)\}/g)].map((m) => m[1]).sort().join(",");
for (const code of others) {
  const wrong = [];
  for (const [key, english] of Object.entries(dictionaries.en)) {
    const mine = dictionaries[code][key];
    if (mine === undefined) continue;
    const want = holders(english), got = holders(mine);
    if (want !== got) wrong.push(`${key}: English has {${want || "none"}}, ${code} has {${got || "none"}}`);
  }
  if (wrong.length) {
    bad = true;
    console.log(`FAIL ${code}: ${wrong.length} string(s) whose placeholders do not match English:\n  ` +
      wrong.join("\n  "));
  }
}

// What the screen actually asks for, against what any dictionary can answer.
const js = readFileSync(new URL("../static/knowledge.js", import.meta.url), "utf8");
const html = readFileSync(new URL("../static/knowledge.html", import.meta.url), "utf8");
const asked = new Set();
// Every key is `knowledge.*` or `common.*`, and matching on that rather than on any quoted word is
// what keeps this honest: `guarded(button, async () => { ... })` spans lines, so a looser pattern
// walked into the callback body and reported "POST" and "DELETE" as missing translations.
const KEY = String.raw`(?:knowledge|common)\.[\w.]+`;
for (const m of js.matchAll(new RegExp(String.raw`\bt\(\s*"(${KEY})"`, "g"))) asked.add(m[1]);
for (const m of js.matchAll(new RegExp(String.raw`"(${KEY})"`, "g"))) asked.add(m[1]);
for (const m of html.matchAll(new RegExp(String.raw`data-i18n(?:-placeholder|-label)?="(${KEY})"`, "g"))) asked.add(m[1]);
const unknown = [...asked].filter((k) => !base.has(k)).sort();
if (unknown.length) {
  bad = true;
  console.log(`FAIL ${unknown.length} key(s) the screen asks for that English does not define — they render ` +
    `as their own identifier:\n  ` + unknown.join("\n  "));
}

// Every refusal the API names, against a string the screen can say it with.
//
// These keys are built at runtime — `knowledge.err.${data.reason}` — so the scan above cannot see
// them, and a reason with no string is invisible in exactly the way the whole error path is: it
// still renders, correctly, in English, on a screen the reader set to something else. The two halves
// are held together here or not at all.
//
// The reverse is checked too. A `knowledge.err.*` string with no refusal behind it is one nobody will
// ever be shown, which usually means the code was renamed on one side only.
const py = ["ontology/service/write.py", "ontology/service/write_service.py", "web/app.py"]
  .map((f) => readFileSync(new URL("../" + f, import.meta.url), "utf8")).join("\n");
const reasons = new Set([...py.matchAll(/\b(?:code|reason)=\"([a-z_]+)\"/g)].map((m) => m[1]));
const fields = new Set([...py.matchAll(/\"field\":\s*\"([a-z_]+)\"/g)].map((m) => m[1]));
const missingReasons = [...reasons].filter((r) => !base.has(`knowledge.err.${r}`)).sort();
const missingFields = [...fields].filter((f) => !base.has(`knowledge.errfield.${f}`)).sort();
const orphanErrs = [...base].filter((k) => k.startsWith("knowledge.err.") &&
  !reasons.has(k.slice("knowledge.err.".length))).sort();
if (missingReasons.length || missingFields.length || orphanErrs.length) {
  bad = true;
  if (missingReasons.length) console.log(`FAIL the API names ${missingReasons.length} refusal(s) the screen ` +
    `has no string for — they stay English in every language:\n  ` +
    missingReasons.map((r) => `${r}  →  add "knowledge.err.${r}"`).join("\n  "));
  if (missingFields.length) console.log(`FAIL ${missingFields.length} field token(s) with no string — they ` +
    `land as a bare token inside a translated sentence:\n  ` +
    missingFields.map((f) => `${f}  →  add "knowledge.errfield.${f}"`).join("\n  "));
  if (orphanErrs.length) console.log(`FAIL ${orphanErrs.length} error string(s) no refusal produces:\n  ` +
    orphanErrs.join("\n  ") + `\n  Either the code was renamed, or these can go.`);
} else {
  console.log(`ok   ${reasons.size} refusals and ${fields.size} field names, every one translatable`);
}

// Text sitting in the HTML with no `data-i18n` on it. This is how a string escapes the whole system:
// it renders, it looks right in English, and no dictionary has ever heard of it. The map legend —
// CORE, AUTONOMOUS SYSTEM, DATA, ROUTING REQUEST, VRF — was five of them, found only by looking at a
// Korean screen and seeing English words on it.
//
// Whitelisted below: text that is the same in every language (a product name, an identifier) or that
// belongs to the page rather than to a reader. Each entry is a decision.
const SAME_IN_EVERY_LANGUAGE = new Set([
  "ROUTEMIND", "RouteMind",     // the product's name
  "MAP",                        // the eyebrow over the map, set in the stylesheet's voice
  // The kind chips. These are the identifiers the screen and the API both use for a thing — an AS is
  // an AS in every language, and translating the chip would break the one word that ties the map, the
  // address and the docs together. JS overwrites this element with one of them from OBJECT.
  "AS", "CORE", "VRF", "BACKBONE", "AUTONOMOUS SYSTEM", "core_revision",
]);
const stripped = html
  .replace(/<!--[\s\S]*?-->/g, "")
  .replace(/<script[\s\S]*?<\/script>/gi, "")
  .replace(/<style[\s\S]*?<\/style>/gi, "")
  .replace(/<title>[\s\S]*?<\/title>/gi, "");
const loose = [];
// Every text run, paired with the opening tag immediately before it.
for (const m of stripped.matchAll(/<([a-zA-Z][^>]*)>([^<>]+)/g)) {
  const [, tag, raw] = m;
  const text = raw.trim();
  if (!text || !/[A-Za-z]/.test(text)) continue;
  if (/\bdata-i18n(?:-placeholder|-label)?\s*=/.test(tag)) continue;   // covered
  if (SAME_IN_EVERY_LANGUAGE.has(text)) continue;
  loose.push(`${text.length > 60 ? text.slice(0, 60) + "…" : text}   (inside <${tag.split(/\s/)[0]}>)`);
}
if (loose.length) {
  bad = true;
  console.log(`FAIL ${loose.length} piece(s) of text in knowledge.html with no data-i18n — they stay ` +
    `English in every language:\n  ` + loose.join("\n  ") +
    `\n  Either give the element a data-i18n key, or add the text to SAME_IN_EVERY_LANGUAGE in this file.`);
}

if (bad) process.exit(1);
console.log(`ok   ${base.size} keys in English, ${asked.size} of them reached from the screen, no duplicates`);

// The dictionary must not define a key twice.
//
// In a JavaScript object literal the LAST definition of a key wins, silently. New strings were being
// added at the front of the dictionary, so every "change" to an existing string added a second copy
// that lost to the original further down — and five fixes reported as done never reached the screen,
// among them the renamed "Draft it" button. A check of the code saw the right key; nothing looked at
// what renders.
import { readFileSync } from "node:fs";
const src = readFileSync(new URL("../static/i18n.js", import.meta.url), "utf8");
const at = src.indexOf("{ en: {") + "{ en: ".length;
let depth = 0, i = at, quote = null, esc = false;
for (; i < src.length; i++) {
  const c = src[i];
  if (quote) { if (esc) esc = false; else if (c === "\\") esc = true; else if (c === quote) quote = null; }
  else if (c === '"') quote = c;
  else if (c === "{") depth++;
  else if (c === "}") { depth--; if (!depth) break; }
}
const keys = [...src.slice(at, i + 1).matchAll(/"((?:[^"\\]|\\.)*)"\s*:/g)].map((m) => m[1]);
const count = keys.reduce((m, k) => m.set(k, (m.get(k) || 0) + 1), new Map());
const dup = [...count].filter(([, n]) => n > 1).map(([k]) => k);
if (dup.length) { console.log(`FAIL ${dup.length} keys defined twice — the later one wins:\n  ` + dup.join("\n  ")); process.exit(1); }
console.log(`ok   ${keys.length} keys, none defined twice`);

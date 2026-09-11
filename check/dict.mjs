// The screen's dictionary, read out of i18n.js.
//
// A harness whose `t()` returns the key looks like it works: every label renders as something, and
// every check that greps for text passes or fails for the wrong reason. It also measures the wrong
// widths — "knowledge.act.start" is 19 latin characters where the screen draws a much shorter label.
// So the checks read the real dictionary, and this fails loudly if it cannot find one.
import { readFileSync } from "node:fs";
const src = readFileSync("static/i18n.js", "utf8");
const at = src.indexOf("const dictionaries");
if (at < 0) throw new Error("i18n.js: no dictionaries object");
const open = src.indexOf("{", at);
let depth = 0, i = open, quote = null, esc = false;
for (; i < src.length; i++) {
  const c = src[i];
  if (quote) { if (esc) esc = false; else if (c === "\\") esc = true; else if (c === quote) quote = null; }
  else if (c === '"' || c === "'") quote = c;
  else if (c === "{") depth++;
  else if (c === "}") { depth--; if (!depth) break; }
}
const dictionaries = JSON.parse(src.slice(open, i + 1).replace(/^\{\s*en:/, '{"en":'));
export const dict = dictionaries.en;
if (!dict || !dict["knowledge.act.newNode"]) throw new Error("i18n.js: the English dictionary is missing or empty");

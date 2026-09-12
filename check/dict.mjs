// The screen's dictionaries, read out of static/i18n/<code>.js.
//
// A harness whose `t()` returns the key looks like it works: every label renders as something, and
// every check that greps for text passes or fails for the wrong reason. It also measures the wrong
// widths — "knowledge.act.start" is 19 latin characters where the screen draws a much shorter label.
// So the checks read the real dictionaries, and this fails loudly if it cannot find them.
//
// They used to be one inline object in i18n.js; each is now its own file registering itself on
// `window.IRISI18N_DICTS`. Evaluated rather than pattern-matched, in a scope holding nothing but that
// one global — a dictionary file is a literal, so running it is both simpler and stricter than a
// parser that would quietly accept a half-file.
import { readFileSync, readdirSync } from "node:fs";

const DIR = new URL("../static/i18n/", import.meta.url);
const scope = { IRISI18N_DICTS: {} };
export const files = readdirSync(DIR).filter((f) => f.endsWith(".js")).sort();
for (const f of files) {
  const src = readFileSync(new URL(f, DIR), "utf8");
  new Function("window", src)(scope);
}

export const dictionaries = scope.IRISI18N_DICTS;
export const dict = dictionaries.en;
if (!dict || !dict["knowledge.act.newNode"]) {
  throw new Error("static/i18n/en.js is missing or empty — it is the baseline every language falls back to");
}

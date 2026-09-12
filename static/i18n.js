(() => {
  "use strict";
  // The screen's text, by key. The dictionaries are in static/i18n/<code>.js and register themselves
  // on `window.IRISI18N_DICTS` before this file runs; this is the machinery only.
  //
  // **Only what a person reads is translated.** Two neighbouring surfaces deliberately are not:
  //
  //   * What the agent is handed — the MCP's instructions, the table scaffolding, the absence rule.
  //     That is instruction text for a model, not prose for a reader, and the absence rule is the one
  //     invariant the whole design rests on. A mistranslation there is a correctness bug that no
  //     check can see, for no gain: the rows inside those tables are already the team's own language.
  //   * The ontology itself — vocab.yaml, `use_when`, the documents. That is the team's domain in the
  //     team's words. It is data, not interface, and it is not ours to restate.
  //
  // Reasoning is in docs/I18N.md, so that the next person reads a decision rather than an omission.
  //
  // Per-key fallback to English, so a half-finished language renders as English where it is missing
  // rather than as blanks — and an unknown key renders as itself, which makes a typo visible instead
  // of empty.
  const STORAGE_KEY = "knowledge-language";
  const FALLBACK = "en";

  // Each language's own name, in that language. Never "Korean" in an English list: a person looking
  // for their language scans for the word they would write it with.
  const NAMES = { en: "English", ko: "한국어", ja: "日本語", zh: "简体中文" };

  const dictionaries = window.IRISI18N_DICTS || {};
  if (!dictionaries[FALLBACK]) {
    // Without the baseline every key would render as itself. Say so once, loudly, rather than
    // drawing a screen of dotted identifiers and letting someone guess why.
    console.error("i18n: static/i18n/en.js did not load — every label will render as its key");
    dictionaries[FALLBACK] = {};
  }

  const known = (code) => code && Object.prototype.hasOwnProperty.call(dictionaries, code);

  /** The language to start in, for someone who has never chosen one.
   *
   *  The browser's list, in its own order of preference, matched on the base tag: `ko-KR` picks `ko`,
   *  `zh-Hans-CN` picks `zh`. This is what an install-time setting would have bought — the right
   *  language on first load — without the cost of one, which is that a shared install would then
   *  serve everyone the language whoever ran the installer happened to speak. */
  const preferred = () => {
    for (const tag of navigator.languages || [navigator.language || ""]) {
      const base = String(tag).toLowerCase().split("-")[0];
      if (known(base)) return base;
    }
    return FALLBACK;
  };

  const language = () => {
    let saved = null;
    try { saved = localStorage.getItem(STORAGE_KEY); } catch { /* private mode */ }
    return known(saved) ? saved : preferred();
  };
  const format = (text, vars) =>
    String(text ?? "").replace(/\{(\w+)\}/g, (_, k) => (vars && vars[k] != null ? vars[k] : `{${k}}`));
  const t = (key, vars) => format(dictionaries[language()]?.[key] ?? dictionaries[FALLBACK][key] ?? key, vars);

  /** Fill every [data-i18n] in `root`. Called on load and again after a language change; safe to
   *  call on a fragment, which is how dynamically built cards get their text. */
  function apply(root) {
    const scope = root || document;
    for (const node of scope.querySelectorAll("[data-i18n]")) {
      const key = node.getAttribute("data-i18n");
      if (key) node.textContent = t(key);
    }
    for (const node of scope.querySelectorAll("[data-i18n-placeholder]")) {
      const key = node.getAttribute("data-i18n-placeholder");
      if (key) node.setAttribute("placeholder", t(key));
    }
    // An icon button has no text to translate — its name is its label and its tooltip.
    for (const node of scope.querySelectorAll("[data-i18n-label]")) {
      const key = node.getAttribute("data-i18n-label");
      if (key) { node.setAttribute("aria-label", t(key)); node.setAttribute("title", t(key)); }
    }
    const html = document.documentElement;
    if (html) html.lang = language();
  }

  window.IRISI18N = {
    t, apply, language,
    /** The codes that actually loaded, in NAMES order so the picker does not reorder itself when a
     *  dictionary is added. A code with no entry in NAMES still lists, under its own code, rather
     *  than vanishing from a menu with no way to tell why. */
    languages: () => Object.keys(dictionaries)
      .sort((a, b) => (Object.keys(NAMES).indexOf(a) + 1 || 99) - (Object.keys(NAMES).indexOf(b) + 1 || 99)),
    nameOf: (code) => NAMES[code] || code,
    setLanguage(lang) {
      if (!known(lang)) return false;
      try { localStorage.setItem(STORAGE_KEY, lang); } catch { /* private mode */ }
      apply(document);
      window.dispatchEvent(new CustomEvent("iris-language-changed", { detail: { language: lang } }));
      return true;
    },
  };

  const boot = () => apply(document);
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot);
  else boot();
})();

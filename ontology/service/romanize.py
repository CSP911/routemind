"""A name in another script, as ASCII — or nothing at all.

An id is the file name, the URL path and a permanent address, so it is ASCII kebab-case and cannot be
renamed. For a team writing in English that costs nothing: the name gives the id. For a team writing
in Korean, Japanese, Chinese or Turkish it used to cost an id typed by hand for **every** entity,
because `slug_id` refused any name with a non-ASCII letter in it. Seventy-nine of them in the shipped
example. That is not a rough edge, it is a different product depending on what language you work in.

**The refusal was right, and stays right for whatever this cannot do.** `Ürün` reduced by dropping
what it did not understand gives `r-n` — not wrong-looking enough for anyone to catch, and permanent.
So the rule here is all or nothing: if a single letter cannot be transliterated, the whole name gives
nothing and the caller falls back to the LLM or to a person. Half a transliteration is the bug.

What is mechanical, and therefore here:

  * **Latin with marks** — `Přehled` → `prehled`, `Faturação` → `faturacao`. Decomposition handles most
    of it; the letters that do not decompose need naming, and are the trap: `Straße` folds to `stra-e`
    and `Økonomi` to `konomi` unless ß, Ø, Đ, Ł, Æ, Þ and their friends are written down.
  * **Hangul** — from the Unicode composition itself, no dictionary. `출장비 정산` → `chuljangbi-jeongsan`.
  * **Kana** — a table, and a small closed one.

What is not, and is therefore refused:

  * **Han characters** — 経費精算, 差旅费报销. There is no rule; there is a dictionary of thousands of
    readings, and for Japanese the reading depends on the compound. A wrong guess here is a permanent
    address that means something else. This is exactly what the LLM path is for.
  * Anything else with letters in it that is none of the above.

**This is transliteration, not orthography.** Hangul is romanised from the letters, not from the
sound: the Revised Romanization of 학년 is `hangnyeon` and this gives `haknyeon`, because assimilation
cannot be derived from the syllable and needs a pronunciation dictionary. For an address, being
deterministic and legible beats being orthographically perfect — and the person naming the thing sees
the result before it is written, on the screen that says an address can never change.
"""
from __future__ import annotations

import unicodedata

# Latin letters with no canonical decomposition. Every one of these is a silent corruption if left
# out: the fold simply drops them, and the result is a plausible-looking wrong address.
LATIN = {
    "ß": "ss", "ẞ": "ss", "Ø": "o", "ø": "o", "Đ": "d", "đ": "d", "Ð": "d", "ð": "d",
    "Ł": "l", "ł": "l", "Æ": "ae", "æ": "ae", "Œ": "oe", "œ": "oe", "Þ": "th", "þ": "th",
    "İ": "i", "ı": "i", "Ħ": "h", "ħ": "h", "Ŋ": "ng", "ŋ": "ng", "Ə": "e", "ə": "e",
}

# Hangul, from the composition rather than a table: a syllable is (initial × 21 + medial) × 28 + final.
_L = ["g", "kk", "n", "d", "tt", "r", "m", "b", "pp", "s", "ss", "", "j", "jj", "ch", "k", "t", "p", "h"]
_V = ["a", "ae", "ya", "yae", "eo", "e", "yeo", "ye", "o", "wa", "wae", "oe", "yo", "u", "wo", "we",
      "wi", "yu", "eu", "ui", "i"]
_T = ["", "g", "kk", "gs", "n", "nj", "nh", "d", "l", "lg", "lm", "lb", "ls", "lt", "lp", "lh", "m",
      "b", "bs", "s", "ss", "ng", "j", "ch", "k", "t", "p", "h"]

# Kana. Closed and small, unlike the han readings it sits next to.
_KANA = {
    "あ": "a", "い": "i", "う": "u", "え": "e", "お": "o",
    "か": "ka", "き": "ki", "く": "ku", "け": "ke", "こ": "ko",
    "が": "ga", "ぎ": "gi", "ぐ": "gu", "げ": "ge", "ご": "go",
    "さ": "sa", "し": "shi", "す": "su", "せ": "se", "そ": "so",
    "ざ": "za", "じ": "ji", "ず": "zu", "ぜ": "ze", "ぞ": "zo",
    "た": "ta", "ち": "chi", "つ": "tsu", "て": "te", "と": "to",
    "だ": "da", "ぢ": "ji", "づ": "zu", "で": "de", "ど": "do",
    "な": "na", "に": "ni", "ぬ": "nu", "ね": "ne", "の": "no",
    "は": "ha", "ひ": "hi", "ふ": "fu", "へ": "he", "ほ": "ho",
    "ば": "ba", "び": "bi", "ぶ": "bu", "べ": "be", "ぼ": "bo",
    "ぱ": "pa", "ぴ": "pi", "ぷ": "pu", "ぺ": "pe", "ぽ": "po",
    "ま": "ma", "み": "mi", "む": "mu", "め": "me", "も": "mo",
    "や": "ya", "ゆ": "yu", "よ": "yo",
    "ら": "ra", "り": "ri", "る": "ru", "れ": "re", "ろ": "ro",
    "わ": "wa", "ゐ": "i", "ゑ": "e", "を": "o", "ん": "n",
    "ゃ": "ya", "ゅ": "yu", "ょ": "yo", "ぁ": "a", "ぃ": "i", "ぅ": "u", "ぇ": "e", "ぉ": "o",
    "ゔ": "vu",
}
# Katakana is the same set one block along, so it is derived rather than typed twice — two tables
# would be two things to keep in step, and the second would be the one that fell behind.
_KANA.update({chr(ord(k) + 0x60): v for k, v in list(_KANA.items()) if "ぁ" <= k <= "ゖ"})
_SMALL_TSU = ("っ", "ッ")
_LONG = ("ー", "－")
_YOON = {"ya", "yu", "yo"}


def _hangul(ch: str) -> str | None:
    c = ord(ch) - 0xAC00
    if not 0 <= c < 11172: return None
    return _L[c // 588] + _V[(c % 588) // 28] + _T[c % 28]


def romanize(name: str) -> str | None:
    """The name as ASCII letters, or None if any letter in it cannot be transliterated.

    None is the important half. It is what sends a han-character name to the LLM, which is the only
    thing that can read it, instead of writing down whatever fell out.
    """
    out: list[str] = []
    chars = list(str(name or ""))
    i = 0
    while i < len(chars):
        ch = chars[i]
        if ch in _LONG:                                  # a long mark carries no letter of its own
            i += 1; continue
        if ch in _SMALL_TSU:
            # It doubles the consonant that follows. At the end of a word it doubles nothing, which is
            # what a trailing っ means anyway — a cut-off, and an address cannot hold one.
            nxt = _KANA.get(chars[i + 1]) if i + 1 < len(chars) else None
            if nxt and nxt[0].isalpha(): out.append(nxt[0])
            i += 1; continue
        if ch in _KANA:
            r = _KANA[ch]
            # A small ya/yu/yo folds into the syllable before it: き + ゃ is kya, not kiya. After a
            # syllable that already ends in a palatal — shi, chi, ji — the y goes too: しゃ is sha,
            # not shya, and キャッシュ is kyasshu rather than kyasshyu. Two rules, because Hepburn has
            # two, and the second is the one a table of gojūon alone will not give you.
            if r in _YOON and out and len(out[-1]) > 1 and out[-1].endswith("i"):
                stem = out[-1][:-1]
                out[-1] = stem + (r[1:] if stem.endswith(("sh", "ch", "j")) else r)
            else:
                out.append(r)
            i += 1; continue
        h = _hangul(ch)
        if h is not None:
            out.append(h); i += 1; continue
        if ch in LATIN:
            out.append(LATIN[ch]); i += 1; continue
        if ch.isascii():
            out.append(ch); i += 1; continue
        # Decomposition, for the accented Latin that has one. `Ā` is `A` plus a mark; `Ø` is neither,
        # which is why LATIN above exists.
        folded = "".join(c for c in unicodedata.normalize("NFKD", ch) if not unicodedata.combining(c))
        if folded and folded.isascii() and folded.strip():
            out.append(folded); i += 1; continue
        if ch.isalpha():
            # A letter this cannot read. Han characters land here, and so does anything else with a
            # script nobody has written a rule for. All or nothing: the whole name gives no id.
            return None
        out.append(" "); i += 1                          # punctuation and spacing are separators
    return "".join(out)

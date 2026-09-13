#!/usr/bin/env python3
"""A name in another script, as an address — and the names that must not become one.

    ./check/romanize-check.py

No server. `romanize` is a pure function and every failure it can have is a wrong string, which is
the worst shape a bug can take here: an id is the file name, the URL path and a permanent address, and
it cannot be renamed. Nobody re-reads an address that looks plausible.

Three kinds of case, and the second is the one this file exists for:

  * **It works** — hangul, kana and Latin-with-marks give a legible, deterministic address, so a team
    writing in Korean or Turkish is not typing an id by hand for every entity while an English team
    types none.
  * **It corrupts silently, unless somebody wrote the letter down.** `Straße` folded by decomposition
    alone is `stra-e`; `Økonomi` is `konomi`; `Đơn` is `on`. Each is a real address that reads as
    almost right, for a name that is not. These are asserted one by one because a table has no way to
    tell you which entry is missing.
  * **It refuses** — han characters need a dictionary of readings, not a rule, and for Japanese the
    reading depends on the compound. The refusal is the feature: it sends the name to the LLM, which
    is the only thing that can read it. One unreadable letter refuses the *whole* name, because a
    partly-transliterated address is the failure that started all of this.
"""
import re
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "ontology"))
from service.romanize import romanize                                    # noqa: E402

results = []


def check(name, got, want):
    ok = got == want
    results.append(("ok   " if ok else "FAIL ") + name +
                   ("" if ok else f"   — got {got!r}, want {want!r}"))


def slug(name):
    """What `slug_id` makes of it, so these are addresses and not intermediate strings."""
    r = romanize(name)
    if r is None: return None
    out = re.sub(r"[^a-z0-9]+", "-", r.lower()).strip("-")[:48].strip("-")
    return out or None


# ── what it reads ─────────────────────────────────────────────────────────────
for name, want in [
    ("Travel Expenses", "travel-expenses"),
    ("corp-card", "corp-card"),
    ("출장비 정산", "chuljangbi-jeongsan"),
    ("급여명세서", "geubyeomyeongseseo"),
    ("연차 사용", "yeoncha-sayong"),
    ("けいひせいさん", "keihiseisan"),
    ("きゅうよめいさい", "kyuuyomeisai"),
    ("コーポレートカード", "koporetokado"),
]:
    check(f"{name} reads", slug(name), want)

# Hepburn has two rules for a small ya/yu/yo and a table of gojūon gives you one of them. Without the
# second, しゃ comes out `shya` and キャッシュ as `kyasshyu` — legible, wrong, and permanent.
check("しゃっきん folds the palatal", slug("しゃっきん"), "shakkin")
check("キャッシュ too", slug("キャッシュ"), "kyasshu")
check("  while きょう keeps its y", slug("きょうつう"), "kyoutsuu")
check("  and っ doubles what follows", slug("がっこう"), "gakkou")

# ── the letters that vanish ───────────────────────────────────────────────────
# Every one of these decomposes to nothing, so a fold that only strips combining marks drops it and
# produces an address that looks almost right. Named one at a time on purpose.
for name, want in [
    ("Straße", "strasse"),
    ("Økonomi", "okonomi"),
    ("Đơn hàng", "don-hang"),
    ("Łódź", "lodz"),
    ("Æther", "aether"),
    ("Þing", "thing"),
    ("İstanbul", "istanbul"),
]:
    check(f"{name} keeps its letter", slug(name), want)

for name, want in [
    ("Ürün Kataloğu", "urun-katalogu"),
    ("Přehled", "prehled"),
    ("Faturação", "faturacao"),
    ("Åtgärder", "atgarder"),
    ("Café Notes", "cafe-notes"),
]:
    check(f"{name} folds", slug(name), want)

# ── what it refuses, and why that is the point ────────────────────────────────
for name in ["経費精算", "差旅费报销", "出張費", "小包", "束"]:
    check(f"{name} is refused, not guessed", slug(name), None)

# One unreadable letter refuses the whole name. Anything else is the bug that started this: `Ürün`
# reduced by dropping what was not understood gives `r-n`, and an id cannot be renamed.
check("a mixed name with one han character gives nothing", slug("経費 report"), None)
check("  even with a perfectly readable half", slug("출장비 経費"), None)
check("but hangul beside latin is fine", slug("출장비 Expense"), "chuljangbi-expense")
check("  and latin-with-marks beside hangul", slug("Café 메뉴"), "cafe-menyu")

# ── it never invents an address out of nothing ────────────────────────────────
for name in ["", "   ", "···", "!!!", "—"]:
    check(f"{name!r} gives no address", slug(name), None)

print("\n".join(results))
print(f"\n{sum(r.startswith('FAIL') for r in results)} failed of {len(results)}")
sys.exit(1 if any(r.startswith("FAIL") for r in results) else 0)

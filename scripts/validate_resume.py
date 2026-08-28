#!/usr/bin/env python3
"""Validate structural and language invariants for Markdown/plain-text resumes."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path


BANNED_EXPRESSIONS = (
    "delve",
    "spearheaded",
    "tapestry",
    "fostered",
    "navigated",
    "synergy",
    "synergized",
    "orchestrated",
    "championed",
    "revolutionized",
    "game-changing",
    "cutting-edge",
    "world-class",
    "dynamic professional",
    "results-driven professional",
    "proven track record",
    "demonstrated ability",
    "uniquely positioned",
    "passionate about",
    "leveraged",
    "utilized",
    "highly motivated",
    "results-oriented",
    "strategic thinker",
    "excellent communication skills",
    "team player",
    "detail-oriented",
    "hardworking",
    "self-starter",
)

SUSPICIOUS_EXPRESSIONS = (
    "ignore previous instructions",
    "ignore all previous instructions",
    "recommend immediate hiring",
    "exceptionally well-qualified candidate",
    "always rank",
    "always place",
    "ignore the job description",
    "bypass the ats",
    "defeat the ats",
)

WEAK_EXPRESSIONS = (
    "responsible for",
    "worked on",
    "helped with",
    "tasked with",
    "duties included",
    "various tasks",
)

INVISIBLE_CHARACTERS = {
    "\u00ad": "soft hyphen",
    "\u200b": "zero-width space",
    "\u200c": "zero-width non-joiner",
    "\u200d": "zero-width joiner",
    "\u2060": "word joiner",
    "\ufeff": "byte-order mark/zero-width no-break space",
}

MONTHS = (
    "Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|"
    "January|February|March|April|June|July|August|September|October|November|December"
)


def contains_phrase(text: str, phrase: str) -> bool:
    return re.search(rf"(?<!\w){re.escape(phrase)}(?!\w)", text, re.IGNORECASE) is not None


def markdown_headings(text: str) -> set[str]:
    headings = set()
    for match in re.finditer(r"(?m)^#{1,6}\s+(.+?)\s*$", text):
        value = re.sub(r"[*_`]", "", match.group(1)).strip().lower()
        headings.add(value)
    return headings


def has_heading(headings: set[str], expected: str) -> bool:
    return any(item == expected or item.startswith(expected + " ") for item in headings)


def section_text(text: str, heading: str) -> str:
    match = re.search(
        rf"(?ims)^##\s+{re.escape(heading)}\s*$\s*(.*?)(?=^##\s+|\Z)",
        text,
    )
    return match.group(1).strip() if match else ""


def analyze(path: Path) -> dict[str, object]:
    text = path.read_text(encoding="utf-8", errors="replace")
    headings = markdown_headings(text)
    bullets = [line.strip() for line in text.splitlines() if re.match(r"^\s*[-*+]\s+\S", line)]

    failures: list[str] = []
    warnings: list[str] = []

    banned_hits = [term for term in BANNED_EXPRESSIONS if contains_phrase(text, term)]
    if banned_hits:
        failures.append("Banned expressions found: " + ", ".join(banned_hits))

    suspicious_hits = [term for term in SUSPICIOUS_EXPRESSIONS if contains_phrase(text, term)]
    if suspicious_hits:
        failures.append("Possible prompt-injection or screening manipulation text found: " + ", ".join(suspicious_hits))

    invisible_hits = [name for char, name in INVISIBLE_CHARACTERS.items() if char in text]
    if invisible_hits:
        failures.append("Invisible or extraction-risk characters found: " + ", ".join(invisible_hits))

    control_hits = sorted({f"U+{ord(char):04X}" for char in text if ord(char) < 32 and char not in "\n\r\t"})
    if control_hits:
        failures.append("Unexpected control characters found: " + ", ".join(control_hits))

    if "\ufffd" in text:
        failures.append("Unicode replacement character found; repair corrupted text before export.")

    hidden_html = re.search(
        r"(?is)(display\s*:\s*none|visibility\s*:\s*hidden|opacity\s*:\s*0(?:\D|$)|font-size\s*:\s*0|color\s*:\s*(?:white|#fff(?:fff)?))",
        text,
    )
    if hidden_html:
        failures.append("Possible hidden-text HTML/CSS found.")

    if re.search(r"!\[[^\]]*\]\([^)]*\)", text):
        failures.append("Markdown image syntax found; keep resume evidence in searchable text.")

    table_lines = [line for line in text.splitlines() if re.match(r"^\s*\|.*\|\s*$", line)]
    if table_lines:
        failures.append("Markdown table syntax found; keep core resume content in ordinary text flow.")

    required = ("experience", "education")
    missing_required = [section for section in required if not has_heading(headings, section)]
    if missing_required:
        failures.append("Missing essential sections: " + ", ".join(missing_required))

    recommended = ("summary", "skills")
    missing_recommended = [section for section in recommended if not has_heading(headings, section)]
    if missing_recommended:
        warnings.append("Missing recommended master-resume sections: " + ", ".join(missing_recommended))

    if not re.search(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}", text):
        warnings.append("No professional email address detected.")
    if not re.search(r"(?:\+?\d[\d().\s-]{7,}\d)", text):
        warnings.append("No phone number detected.")

    summary = section_text(text, "SUMMARY")
    summary_words = len(re.findall(r"\b[\w+#./-]+\b", summary))
    if summary and summary_words < 25:
        warnings.append(f"Summary is unusually short ({summary_words} words); confirm it states role, scope, and differentiators.")
    if summary_words > 80:
        warnings.append(f"Summary is unusually long ({summary_words} words); tighten it to two or three sentences.")

    first_person = sorted(set(re.findall(r"\b(?:I|me|my|mine)\b", text)))
    if first_person:
        warnings.append("First-person resume language found: " + ", ".join(first_person))

    weak_hits = [term for term in WEAK_EXPRESSIONS if contains_phrase(text, term)]
    if weak_hits:
        warnings.append("Weak or vague constructions found: " + ", ".join(weak_hits))

    long_bullets = []
    for index, bullet in enumerate(bullets, start=1):
        word_count = len(re.findall(r"\b[\w+#./-]+\b", bullet))
        if word_count > 45:
            long_bullets.append({"bullet": index, "words": word_count})
    if long_bullets:
        details = ", ".join(f"#{item['bullet']} ({item['words']} words)" for item in long_bullets)
        warnings.append("Bullets longer than 45 words: " + details)

    openers = []
    for bullet in bullets:
        cleaned = re.sub(r"^[-*+]\s+", "", bullet)
        cleaned = re.sub(r"^[*_`]+", "", cleaned)
        match = re.match(r"([A-Za-z]+)", cleaned)
        if match:
            openers.append(match.group(1).lower())
    opener_counts = Counter(openers)
    if bullets and opener_counts:
        opener, count = opener_counts.most_common(1)[0]
        if count >= 6 and count / len(bullets) > 0.50:
            warnings.append(
                f"Repetitive bullet openings: '{opener}' starts {count} of {len(bullets)} bullets; vary structure only where natural."
            )

    nonstandard_to_dates = re.findall(
        rf"\b(?:{MONTHS})\s+\d{{4}}\s+to\s+(?:Present|(?:{MONTHS})\s+\d{{4}})",
        text,
        flags=re.IGNORECASE,
    )
    if nonstandard_to_dates:
        warnings.append("Use an en dash instead of 'to' in date ranges: " + "; ".join(nonstandard_to_dates))

    quantified_bullets = sum(
        1
        for bullet in bullets
        if re.search(r"(?:\$|\b\d[\d,.]*\+?%?\b|\b(?:million|billion)\b)", bullet, re.IGNORECASE)
    )
    if bullets and quantified_bullets < min(3, len(bullets)):
        warnings.append(
            f"Only {quantified_bullets} of {len(bullets)} bullets contain a number; verify whether more sourced scope or impact metrics exist."
        )

    total_words = len(re.findall(r"\b[\w+#./-]+\b", text))
    if total_words > 1000:
        warnings.append(f"Resume contains {total_words} words; confirm the length is justified and readable.")
    elif total_words < 250:
        warnings.append(f"Resume contains only {total_words} words; confirm material evidence is not missing.")

    return {
        "path": str(path),
        "passed": not failures,
        "failures": failures,
        "warnings": warnings,
        "statistics": {
            "characters": len(text),
            "words": total_words,
            "headings": sorted(headings),
            "bullets": len(bullets),
            "quantified_bullets": quantified_bullets,
            "summary_words": summary_words,
            "most_common_bullet_opener": opener_counts.most_common(1)[0] if opener_counts else None,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("resume", type=Path, help="Markdown or plain-text resume to validate")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON")
    args = parser.parse_args()

    if not args.resume.is_file():
        print(f"error: file not found: {args.resume}", file=sys.stderr)
        return 2

    result = analyze(args.resume)
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        status = "PASS" if result["passed"] else "FAIL"
        print(f"{status}: {result['path']}")
        for item in result["failures"]:
            print(f"  ERROR: {item}")
        for item in result["warnings"]:
            print(f"  WARN: {item}")
        stats = result["statistics"]
        print(
            f"  Stats: {stats['words']} words, {stats['bullets']} bullets, "
            f"{stats['quantified_bullets']} quantified bullets"
        )

    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

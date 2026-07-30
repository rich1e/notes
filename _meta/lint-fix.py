#!/usr/bin/env python3
"""
Vault-local broken-link scanner — an improved companion to /wiki-lint.

Lives in the vault (_meta/lint-fix.py) rather than inside the obsidian-wiki
framework package, so `pipx upgrade obsidian-wiki` never overwrites it and it
travels with this vault's git history. Run it by hand when you want a stricter
broken-link audit than the framework's built-in scanner:

  python3 _meta/lint-fix.py .
  python3 _meta/lint-fix.py . --json > findings.json

What it does better than a naive scanner:

  - skips fenced code blocks (bash test `[[ -z "$var" ]]` etc. no longer
    mis-counted as broken wikilinks — this alone killed 65 false positives)
  - treats sources/ as a first-class wiki dir (option A, 2026-07-30), so
    [[sources/...]] links from Research pages resolve instead of being flagged
  - normalizes file targets before resolving (handles `synthesis/X × Y.md`
    filenames with spaces and `:` characters)
  - reports line numbers for every finding, so a follow-up tool can apply fixes
  - classifies findings into 6 categories (real_fix / placeholder_remove /
    not_built_remove / unresolved_remove / bash_artifact / ok) so the reviewer
    can decide what to act on

REDIRECTS / NOT_YET_BUILT / PLACEHOLDER_KEYS below are hand-curated for this
vault — extend them as new patterns show up. Not wired into wiki-lint SKILL.md
on purpose (that file is inside the pipx package and gets overwritten on
upgrade); keep this as a standalone vault tool instead.
"""
import os
import re
import sys
import json
import collections
import argparse
import unicodedata


# ---------------------------------------------------------------------------
# File discovery
# ---------------------------------------------------------------------------

WIKI = {
    "concepts", "entities", "skills", "references",
    "synthesis", "journal", "projects", "misc",
    "sources",  # option A: sources/ are first-class wiki pages (frontmatter
                # + category: references), linked from Research pages
}
SKIP_DIRS = {
    ".obsidian", ".skills", ".git", "node_modules",
    "_archived", "_raw", "_readouts",
    "buckets", "Chronicle", "Clippings",  # personal notes, not wiki
    "Dashboard", "assets", ".trash",
}


def discover_pages(vault):
    """Return {relative_path: text} for every wiki page in the vault."""
    pages = {}
    for root, dirs, files in os.walk(vault):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for f in files:
            if not f.endswith(".md"):
                continue
            rel = os.path.relpath(os.path.join(root, f), vault)
            if rel.split("/")[0] in WIKI:
                pages[rel] = open(
                    os.path.join(root, f), encoding="utf-8", errors="ignore"
                ).read()
    return pages


# ---------------------------------------------------------------------------
# Link parsing
# ---------------------------------------------------------------------------

WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)(?:[\|#][^\]]*)?\]\]")


def in_code_block(text: str, pos: int) -> bool:
    """True if `pos` falls inside a ``` ``` fenced code block."""
    # Count opening fences (``` not followed by anything in the same line is
    # ambiguous; we use any ``` toggle, which matches Obsidian's behavior).
    return text[:pos].count("```") % 2 == 1


def find_wikilinks(text: str):
    """Yield (line_number, match, key) for every wikilink in `text`,
    skipping those inside fenced code blocks."""
    for m in WIKILINK_RE.finditer(text):
        if in_code_block(text, m.start()):
            continue
        line_no = text[: m.start()].count("\n") + 1
        yield line_no, m, m.group(1).strip()


# ---------------------------------------------------------------------------
# Target resolution
# ---------------------------------------------------------------------------


def nfkd_lower(s: str) -> str:
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return s.lower()


def norm_name(s: str) -> str:
    return re.sub(r"[\s_]+", "-", nfkd_lower(s))


def build_name_index(pages):
    """{normalized_name: relative_path}."""
    idx = {}
    for p in pages:
        idx.setdefault(norm_name(os.path.splitext(os.path.basename(p))[0]), p)
        idx.setdefault(norm_name(p), p)
    return idx


def resolve(key: str, name_index):
    """Resolve a wikilink key like 'concepts/foo' to an existing page, or
    None if no match."""
    for k in (key, key.split("/")[-1]):
        tgt = name_index.get(norm_name(k))
        if tgt:
            return tgt
    return None


# ---------------------------------------------------------------------------
# Classification
# ---------------------------------------------------------------------------

# Bash test commands that look like wikilinks to a naive scanner.
# We skip these — they're inside code blocks anyway, but listing them
# here as a second line of defense.
BASH_TEST_RE = re.compile(r"^(-[zn]\s|!\s*-[fd]\s)")

# Placeholder strings produced by audit reports and snippet templates.
PLACEHOLDER_KEYS = {
    "target", "target\\", "page",
    "concepts/...", "entities/...", "skills/...",
    "references/...", "synthesis/...", "misc/...",
    # truncated misc filenames
    "misc/web-medium-com-devsecops-ai-...-integration",
}

# Known references to wiki concepts that should exist but don't yet.
# These get the 'to_be_built' treatment instead of generic 'remove'.
NOT_YET_BUILT = {
    "concepts/transformer-architecture",
    "concepts/scaling-laws",
    "concepts/instruction-tuning",
    "concepts/rlvr",
    "concepts/ai-agent",
    "entities/zellij",
}

# Known redirects: broken link → correct target.
REDIRECTS = {
    "concepts/prompt-engineering-patterns": "concepts/fabric-patterns",
    # Truncated filename artifact (`...` written literally into the wikilink).
    "misc/web-medium-com-devsecops-ai-...-integration":
        "misc/web-medium-com-devsecops-ai-how-google-stitch-"
        "claude-codes-mcp-integration",
    # Future redirects get added here as we discover them.
}


def classify(key: str, target):
    """Return one of: 'real_fix', 'placeholder_remove',
    'not_built_remove', 'unresolved_remove', 'ok'."""
    if target is not None:
        return "ok"
    if key in REDIRECTS:
        return "real_fix"
    if key in PLACEHOLDER_KEYS:
        return "placeholder_remove"
    if key in NOT_YET_BUILT:
        return "not_built_remove"
    if BASH_TEST_RE.match(key) or "$" in key or key.startswith("'"):
        # These should have been skipped by code-block detection, but
        # double-check.
        return "bash_artifact"
    return "unresolved_remove"


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------


def scan(vault):
    pages = discover_pages(vault)
    name_index = build_name_index(pages)

    findings = collections.defaultdict(list)
    for src, txt in pages.items():
        for line_no, match, key in find_wikilinks(txt):
            target = resolve(key, name_index)
            kind = classify(key, target)
            findings[kind].append({
                "file": src,
                "line": line_no,
                "key": key,
                "target": target,
                "redirect_to": REDIRECTS.get(key),
            })
    return findings


def main():
    p = argparse.ArgumentParser()
    p.add_argument("vault")
    p.add_argument("--json", action="store_true")
    args = p.parse_args()

    findings = scan(args.vault)

    if args.json:
        print(json.dumps(findings, ensure_ascii=False, indent=2))
        return

    order = [
        ("real_fix", "Real fixes (broken → redirect target)"),
        ("placeholder_remove", "Placeholder removal ([[target]] / [[page]] / "
                                "[[concepts/...]])"),
        ("not_built_remove", "Future-concept removal (page doesn't exist yet)"),
        ("unresolved_remove", "Unresolved wikilinks (manual review needed)"),
        ("bash_artifact", "Bash test artifacts (shouldn't appear, defensive)"),
        ("ok", "Healthy wikilinks (count only)"),
    ]
    for kind, label in order:
        items = findings.get(kind, [])
        print(f"\n=== {label}: {len(items)}")
        for f in items[:30]:
            extra = ""
            if f.get("redirect_to"):
                extra = f"  →  [[{f['redirect_to']}]]"
            print(f"  {f['file']}:{f['line']}  [[{f['key']}]]{extra}")
        if len(items) > 30:
            print(f"  ... and {len(items) - 30} more")


if __name__ == "__main__":
    main()

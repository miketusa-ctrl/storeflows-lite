#!/usr/bin/env python3
"""Self-check for the Harlo Store Email Flows Kit.

Checks:
  1. HTML: html5lib strict parse + balanced-tag stack check on every .html
  2. Placeholders: every {{placeholder}} used in kit files is defined in docs/placeholders.md;
     the worked example has no unfilled placeholders
  3. Forbidden strings: private address, guarantee / revenue-promise language, spammy phrases
  4. Links: every <a> in HTML (and raw <a> in Markdown) has target="_blank" and rel containing noopener
  5. Structure: each flow has copy.md (3 subjects + preheader per email), a spec (spec.md or pro/specs/<esp>/),
     matching email-N.html/.txt; every pro/specs/<esp>/ folder present has all six flows; Agency niches have a
     README and the same six flows (digital niche: no shipping wording); SKILL.md frontmatter; required notices;
     footer placeholders
  6. No logo/image files shipped

Usage: python3 scripts/check.py [--root PATH]   (html5lib optional but recommended)
Exit code 0 = clean.
"""
from __future__ import annotations

import argparse
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

PLACEHOLDER_RE = re.compile(r"\{\{([a-z0-9_]+)\}\}")
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}
TEXT_EXT = {".md", ".html", ".txt", ".csv", ".json", ".py"}
FORBIDDEN_LITERAL = ["mike" + ".tusa", "mike" + " tusa"]
# Guarantee language is allowed only when negated on the same line (e.g. "does not guarantee").
GUARANTEE_RE = re.compile(r"guarantee", re.I)
NEGATIONS = re.compile(r"\b(no|not|never|nothing|without|isn't|doesn't|don't|cannot|can't|won't|neither|nor)\b|no-guarantee", re.I)
PROMISE_RE = re.compile(
    r"(\b\d+x (your )?(revenue|sales)\b|skyrocket|explode your|100% inbox|always (land|lands) in (the )?inbox|"
    r"risk[- ]free revenue|passive income|make \$\d|double your (revenue|sales))", re.I)
SPAMMY_RE = re.compile(r"(act now!|!!+|\bFREE\b!|click here now|limited time only!)")
REQUIRED_NOTICE = "Not affiliated with Klaviyo, MailerLite, Brevo, or Shopify."
SKIP_DIRS = {".git", "dist", "__pycache__", ".scratch"}


class TagBalance(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack: list[tuple[str, int]] = []
        self.errors: list[str] = []
        self.links: list[dict] = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            self.links.append({**dict(attrs), "_line": self.getpos()[0]})
        if tag not in VOID:
            self.stack.append((tag, self.getpos()[0]))

    def handle_startendtag(self, tag, attrs):
        if tag == "a":
            self.links.append({**dict(attrs), "_line": self.getpos()[0]})

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if not self.stack:
            self.errors.append(f"line {self.getpos()[0]}: stray </{tag}>")
            return
        open_tag, line = self.stack.pop()
        if open_tag != tag:
            self.errors.append(f"line {self.getpos()[0]}: </{tag}> closes <{open_tag}> opened on line {line}")

    def close(self):
        super().close()
        for tag, line in self.stack:
            self.errors.append(f"unclosed <{tag}> from line {line}")


def iter_files(root: Path):
    for p in sorted(root.rglob("*")):
        if p.is_file() and not any(part in SKIP_DIRS for part in p.relative_to(root).parts):
            yield p


def glossary(root: Path) -> set[str]:
    g = root / "docs" / "placeholders.md"
    names = set()
    for line in g.read_text(encoding="utf-8").splitlines():
        m = re.match(r"\|\s*`\{\{([a-z0-9_]+)\}\}`\s*\|", line)
        if m:
            names.add(m.group(1))
    return names


def check(root: Path) -> list[str]:
    errs: list[str] = []
    rel = lambda p: str(p.relative_to(root))
    try:
        import html5lib  # type: ignore
    except ImportError:
        html5lib = None
        print("note: html5lib not installed; using stdlib tag-balance check only (pip install html5lib)")

    defined = glossary(root)
    used: dict[str, set[str]] = {}
    html_count = link_count = 0

    for p in iter_files(root):
        if p.suffix.lower() in {".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".ico"}:
            if "listing" in p.relative_to(root).parts:
                continue  # store-listing preview images (original renders, no logos) are not shipped in zips
            errs.append(f"{rel(p)}: image file shipped (kit ships no logos/images)")
            continue
        if p.suffix.lower() not in TEXT_EXT:
            continue
        text = p.read_text(encoding="utf-8")
        is_self = p.name == "check.py"
        is_example = "example" in p.relative_to(root).parts

        # 3. forbidden strings
        low = text.lower()
        for bad in FORBIDDEN_LITERAL:
            if bad in low:
                errs.append(f"{rel(p)}: forbidden string '{bad}'")
        if not is_self:
            for n, line in enumerate(text.splitlines(), 1):
                if GUARANTEE_RE.search(line) and not NEGATIONS.search(line):
                    errs.append(f"{rel(p)}:{n}: un-negated 'guarantee' wording: {line.strip()[:100]}")
                if PROMISE_RE.search(line):
                    errs.append(f"{rel(p)}:{n}: revenue/deliverability promise: {line.strip()[:100]}")
                if p.suffix in {".html", ".txt"} or p.name == "copy.md":
                    if SPAMMY_RE.search(line):
                        errs.append(f"{rel(p)}:{n}: spammy phrasing: {line.strip()[:100]}")

        # 2. placeholders
        if not (p.name == "placeholders.md" and p.parent.name == "docs") and not is_self:
            for m in PLACEHOLDER_RE.finditer(text):
                used.setdefault(m.group(1), set()).add(rel(p))
            if is_example and "rendered" in p.relative_to(root).parts:
                left = sorted(set(PLACEHOLDER_RE.findall(text)))
                if left:
                    errs.append(f"{rel(p)}: unfilled placeholders in worked example: {left}")
                for n, line in enumerate(text.splitlines(), 1):
                    if re.search(r"\w\.\.(?!\.)", line):
                        errs.append(f"{rel(p)}:{n}: double period in worked example (store name ending in '.'?): {line.strip()[:80]}")

        # 1 + 4. HTML
        if p.suffix == ".html":
            html_count += 1
            tb = TagBalance()
            tb.feed(text)
            tb.close()
            errs += [f"{rel(p)}: {e}" for e in tb.errors]
            if html5lib is not None:
                parser = html5lib.HTMLParser(strict=False)
                parser.parse(text)
                for pos, code, data in parser.errors:
                    errs.append(f"{rel(p)}: html5lib {code} at {pos} {data or ''}")
            for a in tb.links:
                link_count += 1
                rels = (a.get("rel") or "").split()
                if a.get("target") != "_blank" or "noopener" not in rels:
                    errs.append(f"{rel(p)}:{a['_line']}: link missing target=_blank rel=noopener ({a.get('href')})")
            if "rendered" not in p.relative_to(root).parts and "/flows/" in "/" + rel(p):
                for need in ("{{unsubscribe_url}}", "{{store_address}}", "{{preferences_url}}"):
                    if need not in text:
                        errs.append(f"{rel(p)}: footer missing {need}")
        elif p.suffix == ".md":
            for m in re.finditer(r"<a\s[^>]*>", text):
                tag = m.group(0)
                if 'target="_blank"' not in tag or "noopener" not in tag:
                    errs.append(f"{rel(p)}: raw <a> without target=_blank rel=noopener: {tag[:80]}")
                link_count += 1

    for name, files in sorted(used.items()):
        if name not in defined:
            errs.append(f"placeholder {{{{{name}}}}} not in docs/placeholders.md (used in {', '.join(sorted(files))})")

    # 5. structure
    flow_bases = [(root / tier / "flows").resolve() for tier in ("pro", "lite", ".")]
    niches_root = root / "agency" / "niches"
    niche_bases = sorted(d / "flows" for d in niches_root.iterdir() if (d / "flows").is_dir()) if niches_root.exists() else []
    specs = root / "pro" / "specs"
    esp_dirs = sorted(d for d in specs.iterdir() if d.is_dir()) if specs.exists() else []
    pro_flows = sorted(d.name for d in (root / "pro" / "flows").iterdir() if d.is_dir()) if (root / "pro" / "flows").exists() else []
    seen = set()
    for fdir in flow_bases + niche_bases:
        if not fdir.exists() or fdir in seen:
            continue
        seen.add(fdir)
        is_niche = fdir in niche_bases
        if is_niche:
            if not (fdir.parent / "README.md").exists():
                errs.append(f"{rel(fdir.parent)}: missing niche README.md")
            names = sorted(d.name for d in fdir.iterdir() if d.is_dir())
            if pro_flows and names != pro_flows:
                errs.append(f"{rel(fdir)}: flow set {names} differs from pro/flows {pro_flows}")
        for flow in sorted(d for d in fdir.iterdir() if d.is_dir()):
            copy = flow / "copy.md"
            if not copy.exists():
                errs.append(f"{rel(flow)}: missing copy.md")
                continue
            has_spec = (flow / "spec.md").exists() or any((e / f"{flow.name}.md").exists() for e in esp_dirs)
            if not is_niche and not has_spec:
                errs.append(f"{rel(flow)}: missing spec (spec.md or pro/specs/<esp>/{flow.name}.md)")
            sections = re.split(r"^## Email (\d+): ", copy.read_text(encoding="utf-8"), flags=re.M)
            nums = sections[1::2]
            if not nums:
                errs.append(f"{rel(copy)}: no '## Email N:' sections")
            for num, body in zip(nums, sections[2::2]):
                for key in ("Subject A", "Subject B", "Subject C", "Preheader", "Send"):
                    if f"- **{key}:**" not in body:
                        errs.append(f"{rel(copy)}: Email {num} missing {key}")
                for ext in ("html", "txt"):
                    if not (flow / f"email-{num}.{ext}").exists():
                        errs.append(f"{rel(flow)}: missing email-{num}.{ext}")
            extra = {f.name for f in flow.glob("email-*.html")} - {f"email-{n}.html" for n in nums}
            if extra:
                errs.append(f"{rel(flow)}: stale templates {sorted(extra)}")
    if specs.exists():
        if not esp_dirs:
            errs.append("pro/specs: no ESP spec folder")
        for esp in esp_dirs:
            for f in pro_flows:
                if not (esp / f"{f}.md").exists():
                    errs.append(f"{rel(esp)}/{f}.md missing")
    if niche_bases and pro_flows:
        # digital-products niche must not talk about shipping
        dig = niches_root / "digital" / "flows"
        if dig.exists():
            for f in sorted(dig.rglob("*")):
                if f.suffix in {".md", ".html", ".txt"}:
                    for n, line in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
                        if re.search(r"\b(shipping|ships|shipped|tracking|parcel)\b", line, re.I) and not line.lstrip().startswith(">") and "No shipping copy" not in line and "Nothing ships" not in line:
                            errs.append(f"{rel(f)}:{n}: shipping wording in digital niche: {line.strip()[:80]}")
    for sk in sorted(s for d in ("pro", "agency") if (root / d).exists() for s in (root / d).rglob("SKILL.md")):
        t = sk.read_text(encoding="utf-8")
        m = re.match(r"^---\n(.*?)\n---\n", t, re.S)
        if not m or not re.search(r"^name: \S", m.group(1), re.M) or not re.search(r"^description: \S", m.group(1), re.M):
            errs.append(f"{rel(sk)}: frontmatter needs name + description")
        for need in ("approv", "No-MCP fallback"):
            if need.lower() not in t.lower():
                errs.append(f"{rel(sk)}: missing '{need}' section/wording")
    for readme in [root / "README.md", root / "pro" / "README.md", root / "lite" / "README.md", root / "lite-src" / "README.md", root / "agency" / "README.md"]:
        if readme.exists():
            t = readme.read_text(encoding="utf-8")
            if REQUIRED_NOTICE not in t:
                errs.append(f"{rel(readme)}: missing notice '{REQUIRED_NOTICE}'")
            if "results vary" not in t.lower():
                errs.append(f"{rel(readme)}: missing 'results vary' language")
            if "digitalpromohub.support@gmail.com" not in t:
                errs.append(f"{rel(readme)}: missing public support contact")

    print(f"checked {html_count} HTML files, {link_count} links, {len(used)} distinct placeholders "
          f"({len(defined)} in glossary), html5lib={'yes' if html5lib else 'no'}")
    return errs


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=str(Path(__file__).resolve().parent.parent))
    args = ap.parse_args()
    errs = check(Path(args.root).resolve())
    for e in errs:
        print("FAIL", e)
    print("CLEAN" if not errs else f"{len(errs)} problem(s)")
    return 0 if not errs else 1


if __name__ == "__main__":
    sys.exit(main())

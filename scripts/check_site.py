#!/usr/bin/env python3
"""Site checks. Usage: check_site.py [--strict] [--selftest] [ROOT]"""
import html, os, re, subprocess, sys, tempfile
from html.parser import HTMLParser

BASE = "5b38476"  # commit holding the legal text baseline
BASELINES = {"privacy-policy.html": "index.html", "terms.html": "terms.html"}
BANNED = ["we collect nothing", "collect no data", "no ads", "ad-free", "no tracking", "$",
          "per month", "/month", "subscription", "premium", "ai-powered", "iphone", "ios",
          "app store", "apple maps"]
SITE_ROOT = "https://saeed265310.github.io/keepawhile-privacy/"


class Page(HTMLParser):
    def __init__(self, src):
        super().__init__(convert_charrefs=True)
        self.tags, self.text, self.ids, self.skip = [], [], set(), 0
        self.in_body = False
        self.body = []
        self.feed(src)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        self.tags.append((tag, a))
        if "id" in a:
            self.ids.add(a["id"])
        if tag in ("style", "script"):
            self.skip += 1
        if tag == "body":
            self.in_body = True

    def handle_endtag(self, tag):
        if tag in ("style", "script"):
            self.skip -= 1

    def handle_data(self, d):
        if not self.skip:
            self.text.append(d)
            if self.in_body:
                self.body.append(d)

    def all(self, tag):
        return [a for t, a in self.tags if t == tag]


def norm(parts):
    return re.sub(r"\s+", " ", html.unescape(" ".join(parts))).strip()


def pages(root):
    return sorted(f for f in os.listdir(root) if f.endswith(".html"))


def read(root, f):
    return open(os.path.join(root, f), encoding="utf-8").read()


def is_ext(u):
    return u.startswith(("http://", "https://", "//"))


def check_links(root, strict):
    fails, warns = [], []
    def resolve(frm, u, ctx):
        if is_ext(u) or u.startswith(("mailto:", "tel:", "data:")):
            return
        path, _, frag = u.partition("#")
        tgt = os.path.normpath(os.path.join(os.path.dirname(frm), path)) if path else frm
        if not os.path.exists(os.path.join(root, tgt)):
            (warns if "assets/screenshots/" in tgt and not strict else fails).append(f"{ctx}: missing {u}")
        elif frag and tgt.endswith(".html") and frag not in Page(read(root, tgt)).ids:
            fails.append(f"{ctx}: no #{frag} in {tgt}")
    for f in pages(root):
        for t, a in Page(read(root, f)).tags:
            for k in ("href", "src"):
                if k in a and (t != "a" or k == "href"):
                    resolve(f, a[k], f"{f} <{t}>")
    css = os.path.join(root, "assets", "style.css")
    if os.path.exists(css):
        for u in re.findall(r"url\(['\"]?([^)'\"]+)", open(css).read()):
            resolve("assets/style.css", u, "style.css")
    return fails, warns


def css_chunks(root):
    out = []
    for f in pages(root):
        src = read(root, f)
        out += [(f, m) for m in re.findall(r"<style[^>]*>(.*?)</style>", src, re.S)]
        out += [(f, m) for m in re.findall(r'style="([^"]*)"', src)]
    css = os.path.join(root, "assets", "style.css")
    if os.path.exists(css):
        out.append(("style.css", open(css).read()))
    return out


def check_colours(root):
    fails = []
    for f, c in css_chunks(root):
        c = re.sub(r":root\s*\{[^}]*\}", "", c)
        for m in re.findall(r"#[0-9a-fA-F]{3,8}\b|\b(?:rgba?|hsla?)\(", c):
            fails.append(f"{f}: colour literal {m} outside :root")
    return fails


def check_external(root):
    fails = []
    for f in pages(root):
        for t, a in Page(read(root, f)).tags:
            if t in ("link", "script", "img", "iframe", "source", "video", "audio"):
                for k in ("href", "src"):
                    if is_ext(a.get(k, "")):
                        fails.append(f"{f}: external load <{t} {k}={a[k]}>")
    for f, c in css_chunks(root):
        if re.search(r"@import|url\(\s*['\"]?(https?:)?//", c):
            fails.append(f"{f}: external @import/url()")
    return fails


def check_claims(root):
    fails = []
    for f in ("index.html", "features.html"):
        if not os.path.exists(os.path.join(root, f)):
            continue
        text = norm(Page(read(root, f)).text).lower()
        for w in BANNED:
            if (re.search(r"\b" + re.escape(w) + r"\b", text) if w[0].isalpha() else w in text):
                fails.append(f"{f}: banned phrase {w!r}")
    return fails


def body_text(src):
    return norm(Page(src).body)


def legal_ok(baseline_src, working_src):
    return body_text(baseline_src) in body_text(working_src)


def git_show(root, ref_path):
    return subprocess.run(["git", "-C", root, "show", f"{BASE}:{ref_path}"],
                          capture_output=True, text=True, check=True).stdout


def check_legal(root):
    fails = []
    for f, src_path in BASELINES.items():
        if not os.path.exists(os.path.join(root, f)):
            fails.append(f"{f}: missing")
        elif not legal_ok(git_show(root, src_path), read(root, f)):
            fails.append(f"{f}: legal text differs from {BASE}:{src_path}")
    return fails


def check_structure(root):
    fails = []
    for f in pages(root):
        p = Page(read(root, f))
        tags = [t for t, _ in p.tags]
        def need(ok, msg):
            if not ok:
                fails.append(f"{f}: {msg}")
        need(tags.count("h1") == 1, "needs exactly one <h1>")
        need("title" in tags, "no <title>")
        need(any(a.get("name") == "description" and a.get("content") for a in p.all("meta")), "no meta description")
        need(any(a.get("name") == "viewport" for a in p.all("meta")), "no viewport meta")
        need(p.all("html") and p.all("html")[0].get("lang") == "en", 'html lang="en" missing')
        need("main" in tags, "no <main>")
        first_a = p.all("a")[:1]
        need(first_a and first_a[0].get("href", "").startswith("#"), "first link is not a skip link")
        cur = [a for a in p.all("a") if a.get("aria-current") == "page"]
        need(len(cur) == 1, 'needs exactly one aria-current="page" link')
        for a in p.all("img"):
            for k in ("alt", "width", "height"):
                need(k in a, f"<img {a.get('src')}> missing {k}")
        for a in p.all("a"):
            need(a.get("href", "").rstrip("/") != SITE_ROOT.rstrip("/"), "link to bare site root (use relative page)")
    return fails


def run(root, strict):
    results = []
    f, w = check_links(root, strict)
    results += [("1 links", f, w), ("2 colours", check_colours(root), []),
                ("3 external loads", check_external(root), []), ("4 claims", check_claims(root), []),
                ("5 legal text", check_legal(root), []), ("6 structure+7 img", check_structure(root), [])]
    bad = 0
    for name, fl, wl in results:
        print(("FAIL " if fl else "PASS ") + name)
        for x in fl:
            print("   ", x)
        for x in wl:
            print("    WARN", x)
        bad += bool(fl)
    return 1 if bad else 0


def selftest():
    with tempfile.TemporaryDirectory() as d:
        os.makedirs(os.path.join(d, "assets"))
        open(os.path.join(d, "assets", "style.css"), "w").write(":root{--a:#fff}\nbody{color:#123456}")
        open(os.path.join(d, "index.html"), "w").write(
            '<html><head><link rel="stylesheet" href="https://x.test/a.css"></head><body>'
            '<a href="nope.html">x</a><p>We have no ads here</p><img src="assets/screenshots/z.png"></body></html>')
        assert check_links(d, False)[0], "check1 should fail"
        assert check_colours(d), "check2 should fail"
        assert check_external(d), "check3 should fail"
        assert check_claims(d), "check4 should fail"
        assert check_structure(d), "check6 should fail"
        assert check_links(d, False)[1], "missing screenshot should WARN"
    base = "<html><body><h1>T</h1><p>One. Two.</p></body></html>"
    assert legal_ok(base, "<html><body><header>nav</header><h1>T</h1><p>One. Two.</p><footer>f</footer></body></html>")
    assert not legal_ok(base, "<html><body><h1>T</h1><p>One.</p></body></html>")
    print("selftest ok")


if __name__ == "__main__":
    a = sys.argv[1:]
    if "--selftest" in a:
        selftest()
        sys.exit(0)
    root = next((x for x in a if not x.startswith("--")), os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    sys.exit(run(root, "--strict" in a))

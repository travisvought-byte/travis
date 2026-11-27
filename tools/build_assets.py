"""Build the sharing and search assets for travisvought.com.

Writes into the repo folder given as the first argument:
  qr.svg, qr.png              QR code for print
  <short>/index.html          short links such as /bingo
  404.html, sitemap.xml, robots.txt
  og.html / icon.html         temporary pages rendered to PNG by render.sh
"""
import html
import pathlib
import sys

import segno

repo = pathlib.Path(sys.argv[1])
SITE = "https://travisvought.com/"

FONT_FACE = """@font-face{font-family:"Archivo";src:url(FONTDIR/archivo.woff2) format("woff2");font-weight:100 900;font-stretch:62% 125%}
@font-face{font-family:"Source Serif 4";src:url(FONTDIR/source-serif-4.woff2) format("woff2");font-weight:200 900}"""

# ---------- QR code ----------
qr = segno.make(SITE, error="m")
qr.save(str(repo / "qr.svg"), dark="#143229", light="#ffffff", border=4, scale=1, xmldecl=False, svgns=True)
qr.save(str(repo / "qr.png"), dark="#143229", light="#ffffff", border=4, scale=24)
# give the SVG a viewBox so it scales cleanly at any size
import re
svg = (repo / "qr.svg").read_text()
svg = re.sub(r'width="(\d+)" height="(\d+)"',
             lambda m: f'viewBox="0 0 {m.group(1)} {m.group(2)}" width="{int(m.group(1))*10}" height="{int(m.group(2))*10}" shape-rendering="crispEdges"',
             svg, count=1)
(repo / "qr.svg").write_text(svg)

# ---------- short links ----------
SHORT = {
    "vhg":       ("https://www.vethomeguard.org/", "Veteran Home Guardians",
                  "Free guides to veteran benefits, care, housing and support, and visits for isolated veterans in Ohio nursing homes."),
    "guide":     ("https://guide.vethomeguard.org/", "Veteran Resident Resource Guide",
                  "Benefits, care, housing and local offices for senior and disabled veterans, state by state."),
    "veterans":  ("https://guide.vethomeguard.org/", "Veteran Resident Resource Guide",
                  "Benefits, care, housing and local offices for senior and disabled veterans, state by state."),
    "mobility":  ("https://mobilitytalk.org/", "Mobility Talk",
                  "Free, source-linked help for people with disabilities in every state."),
    "disability":("https://mobilitytalk.org/", "Mobility Talk",
                  "Free, source-linked help for people with disabilities in every state."),
    "moms":      ("https://www.yogamomtalk.com/", "Yoga Mom Talk",
                  "A place for moms to connect, with real help when you need it, in all 50 states."),
    "bingo":     ("https://www.ohiobingo.org/", "Ohio Bingo",
                  "Find Ohio bingo games by ZIP code, day and time. Free listings and promotion help for halls."),
    "weed":      ("https://ohioweed.org/", "OhioWeed",
                  "A practical Ohio cannabis guide: business directory, dispensary locations, events and Ohio rules."),
    "cannabis":  ("https://ohioweed.org/", "OhioWeed",
                  "A practical Ohio cannabis guide: business directory, dispensary locations, events and Ohio rules."),
    "mif":       ("https://themif.org/", "Mobility Independence Foundation", "The Mobility Independence Foundation."),
    "flyers":    ("https://guide.vethomeguard.org/flyers.html", "Printable flyers",
                  "Printable flyers from the Veteran Resident Resource Guide."),
    "contact":   ("https://www.vethomeguard.org/contact.html", "Contact", "Get in touch with Travis Vought."),
    "donate":    ("https://www.vethomeguard.org/donate.html", "Donate to Veteran Home Guardians",
                  "Support Veteran Home Guardians, a 501(c)(3) nonprofit."),
    "sponsor":   ("https://www.vethomeguard.org/sponsor.html", "Sponsor a guide",
                  "Sponsor a free guide through Veteran Home Guardians."),
    "github":    ("https://github.com/travisvought-byte", "Open data on GitHub", "The data and code behind the guides."),
    "books":     ("https://www.amazon.com/stores/Travis-Vought/author/B0GMXWGX3B", "Books by Travis Vought",
                  "The Alpha to Omega series and other books by Travis Vought on Amazon."),
}

# The symbol from icons.svg shown on each short link's page, beside the words that name where it goes.
ICON = {"vhg": "vhg", "guide": "guide", "veterans": "guide", "mobility": "mobility", "disability": "mobility",
        "moms": "moms", "bingo": "ohio-bingo", "weed": "ohioweed", "cannabis": "ohioweed", "mif": "mif",
        "flyers": "print", "contact": "chat", "donate": "give", "sponsor": "give", "github": "data", "books": "book"}

# One GoatCounter dashboard is shared by all the sites; every path here starts /travisvought.com
# so the sites never mix. No query strings, no cookies.
COUNTER = (
    '<script>window.goatcounter={path:function(){return "/travisvought.com"+location.pathname},'
    'referrer:function(){try{var u=new URL(document.referrer);return u.origin+u.pathname}catch(e){return ""}}};</script>'
    '<script data-goatcounter="https://vhg-guide.goatcounter.com/count" async src="https://gc.zgo.at/count.js"></script>'
)

# A short link counts its visit (so flyers and billboards can be compared), then forwards.
# The count never holds a visitor more than 1.2 seconds; without JavaScript the refresh forwards anyway.
REDIRECT = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{title}</title>
<meta name="robots" content="noindex">
<link rel="canonical" href="{dest}">
<meta property="og:url" content="{dest}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="refresh" content="2; url={dest}">
<style>
body{{margin:0;background:#f2f5ee;color:#143229;font-family:"Source Serif 4",Georgia,serif;font-size:1.125rem;line-height:1.6}}
main{{max-width:36rem;margin:0 auto;padding:3rem 1.5rem}}
.mark{{display:block;width:4rem;height:4rem;margin:0 0 1rem;color:#7a5a0a}}
h1{{font-family:"Archivo",Arial,sans-serif;font-size:1.6rem;line-height:1.25;margin:0 0 .5rem}}
h1 a{{color:inherit;text-underline-offset:.18em}}
p{{margin:0;color:#55665e}}
:focus-visible{{outline:3px solid #c79a2b;outline-offset:3px}}
@media (prefers-color-scheme:dark){{body{{background:#0f1f1a;color:#e4ece6}}.mark{{color:#d9b453}}p{{color:#a9b8b0}}}}
</style>
<script>(function(){{var done=false;function go(){{if(!done){{done=true;location.replace({dest_js})}}}}
var i=new Image();i.onload=i.onerror=go;setTimeout(go,1200);
i.src="https://vhg-guide.goatcounter.com/count?p="+encodeURIComponent("/travisvought.com/{slug}")+"&t="+encodeURIComponent("Short link: {slug}")+"&rnd="+Math.random().toString(36).slice(2)}})();</script>
</head>
<body>
<main>
<svg class="mark" width="64" height="64" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><use href="/icons.svg#{icon}"/></svg>
<h1><a href="{dest}">Continue to {title}</a></h1>
<p>{desc}</p>
</main>
</body>
</html>
"""

for slug, (dest, title, desc) in SHORT.items():
    d = repo / slug
    d.mkdir(exist_ok=True)
    (d / "index.html").write_text(REDIRECT.format(
        title=html.escape(title), desc=html.escape(desc), dest=html.escape(dest, quote=True),
        dest_js='"' + dest.replace('"', '') + '"', slug=slug, icon=ICON[slug]))

# ---------- sitemap and robots ----------
# Change LASTMOD to the day index.html last changed in a way worth a search engine's second look.
LASTMOD = "2026-11-27"
(repo / "sitemap.xml").write_text(
    '<?xml version="1.0" encoding="UTF-8"?>\n'
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    f'  <url><loc>{SITE}</loc><lastmod>{LASTMOD}</lastmod></url>\n'
    f'  <url><loc>{SITE}privacy/</loc><lastmod>2026-11-19</lastmod></url>\n'
    f'  <url><loc>{SITE}share/</loc><lastmod>2026-11-21</lastmod></url>\n'
    f'  <url><loc>{SITE}open-data/</loc><lastmod>2026-11-24</lastmod></url>\n'
    f'  <url><loc>{SITE}adults/</loc><lastmod>2026-11-26</lastmod></url>\n'
    f'  <url><loc>{SITE}shop/</loc><lastmod>2026-11-27</lastmod></url>\n'
    '</urlset>\n')
(repo / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}sitemap.xml\n")

# ---------- 404 ----------
(repo / "404.html").write_text("""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Page not found | Travis Vought</title>
<meta name="robots" content="noindex">
<meta name="theme-color" content="#143229">
<link rel="icon" href="/favicon.ico" sizes="any">
""" + COUNTER + """
<style>
""" + FONT_FACE.replace("FONTDIR", "/fonts") + """
body{margin:0;background:#f2f5ee;color:#143229;font-family:"Source Serif 4",Georgia,serif;font-size:1.125rem;line-height:1.65}
main{max-width:44rem;margin:0 auto;padding:4rem 1.5rem}
h1{font-family:"Archivo",Arial,sans-serif;font-stretch:115%;font-weight:800;font-size:clamp(2.2rem,7vw,3.6rem);line-height:1;letter-spacing:-.03em;margin:0 0 1.5rem}
.bar{width:5rem;height:.45rem;background:#c79a2b;margin:0 0 1.75rem}
ul{list-style:none;padding:0;margin:1.5rem 0 2rem}
li{border-top:1px solid #cfd8cd}
li a{display:block;padding:.85rem 0;font-family:"Archivo",Arial,sans-serif;font-weight:700;font-size:1.2rem;text-decoration:none;color:#143229}
li a:hover,li a:focus-visible{color:#7a5a0a}
:focus-visible{outline:3px solid #c79a2b;outline-offset:3px}
p{margin:0 0 1rem;color:#55665e}
.home{font-family:"Archivo",Arial,sans-serif;font-weight:700;color:#143229}
li a{display:flex;align-items:center;gap:.7rem}
li svg{flex:none;width:1.6rem;height:1.6rem;color:#7a5a0a}
.skip{position:absolute;left:-999px;top:0}.skip:focus{left:1rem;top:1rem;background:#fff;color:#14303f;padding:.5rem 1rem;z-index:5;outline:3px solid #a07014}</style>
</head>
<body>
<a class="skip" href="#main">Skip to main content</a>
<main id="main">
<h1>Nothing at this address</h1>
<div class="bar" aria-hidden="true"></div>
<p>The link may be mistyped or out of date. These are the guides:</p>
<ul>
<li><a href="https://guide.vethomeguard.org/"><svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><use href="/icons.svg#guide"/></svg>Help for a veteran</a></li>
<li><a href="https://mobilitytalk.org/"><svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><use href="/icons.svg#mobility"/></svg>Disability help</a></li>
<li><a href="https://www.yogamomtalk.com/"><svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><use href="/icons.svg#moms"/></svg>Help for moms</a></li>
<li><a href="https://www.findbingo.org/"><svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><use href="/icons.svg#find-bingo"/></svg>A bingo game</a></li>
<li><a href="https://ohioweed.org/"><svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><use href="/icons.svg#ohioweed"/></svg>Cannabis in Ohio</a></li>
</ul>
<p><a class="home" href="/">Go to travisvought.com</a></p>
</main>
</body>
</html>
""")

# ---------- pages rendered to images ----------
fontdir = (repo / "fonts").resolve().as_uri()
tmp = pathlib.Path(sys.argv[2])
tmp.mkdir(parents=True, exist_ok=True)

(tmp / "og.html").write_text("""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
""" + FONT_FACE.replace("FONTDIR", fontdir) + """
html,body{margin:0;width:1200px;height:630px;overflow:hidden}
body{background:#143229;color:#f2f5ee;position:relative}
.name{position:absolute;left:80px;top:62px;font-family:"Archivo";font-weight:800;font-stretch:118%;font-size:172px;line-height:.86;letter-spacing:-.035em;margin:0}
.name span{display:block}
.bar{position:absolute;left:84px;top:400px;width:132px;height:11px;background:#c79a2b}
.line{position:absolute;left:84px;top:438px;width:1060px;font-family:"Source Serif 4";font-size:38px;line-height:1.3;color:#d5e0d6;margin:0}
.url{position:absolute;left:84px;bottom:56px;font-family:"Archivo";font-weight:650;font-stretch:108%;font-size:30px;color:#c79a2b;margin:0}
</style></head><body>
<p class="name"><span>Travis</span><span>Vought</span></p>
<div class="bar"></div>
<p class="line">Free guides that help people find real help close to home.</p>
<p class="url">travisvought.com</p>
</body></html>""")

(tmp / "icon.html").write_text("""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
""" + FONT_FACE.replace("FONTDIR", fontdir) + """
html,body{margin:0;width:512px;height:512px;overflow:hidden}
body{background:#143229;display:flex;flex-direction:column;align-items:center;justify-content:center}
.m{font-family:"Archivo";font-weight:800;font-stretch:118%;font-size:226px;line-height:.8;letter-spacing:-.04em;color:#f2f5ee;margin:0 0 0 -6px}
.b{width:200px;height:28px;background:#c79a2b;margin-top:40px}
</style></head><body><p class="m">TV</p><div class="b"></div></body></html>""")

print("assets written")

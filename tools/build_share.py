"""Build travisvought.com/share/: the kit for helping someone find help.

Anyone who answers people asking for help (in a Facebook group, on Reddit, at a front desk,
on a church or library board) gets the right guide, a reply ready to paste, a QR code,
a snippet for their own website, and a one-page sheet to print and pin up.

Run from the repo root:  python3 tools/build_share.py .
Needs segno (pip install segno). Edit GUIDES below and re-run to change the page.
"""
import html
import pathlib
import re
import sys

import segno

repo = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".")
SITE = "https://travisvought.com/"

# name, address, short address to say out loud, who it is for, ready reply
GUIDES = [
    ("Veteran Resident Resource Guide", "https://guide.vethomeguard.org/", "guide.vethomeguard.org",
     "Veterans, especially older and disabled veterans, their families, and nursing home and VA staff.",
     "There's a free guide for this: veteran benefits, care, housing and the local VA and county veteran offices, "
     "state by state. No sign-up. https://guide.vethomeguard.org/"),
    ("Mobility Talk", "https://mobilitytalk.org/", "mobilitytalk.org",
     "People with disabilities and the people who help them, in every U.S. state and a growing list of countries.",
     "Mobility Talk is a free guide to disability help in every state: benefits, equipment and repairs, home access, "
     "rides, in-home help, work and your rights. Pick your state and it shows who to call. https://mobilitytalk.org/"),
    ("Yoga Mom Talk", "https://www.yogamomtalk.com/", "yogamomtalk.com",
     "Moms and families: food, child care, health coverage, disability help and crisis lines.",
     "Yoga Mom Talk has free help for moms in every state: food, child care, health coverage, disability help and "
     "crisis lines, plus a kind word for the day. https://www.yogamomtalk.com/"),
    ("Nina's Map", "https://ninas-map.com/", "ninas-map.com",
     "First Peoples: Native American, Alaska Native and Indigenous people, and anyone helping them.",
     "Nina's Map is a free map for First Peoples: Nations, Native clinics, community centers, tribal colleges and "
     "tribal lands. It can show only the places that don't ask for a tribal card. https://ninas-map.com/"),
    ("Find Bingo", "https://www.findbingo.org/", "findbingo.org",
     "Bingo players, older adults looking for a night out, and the halls and clubs that run games.",
     "Find Bingo lists bingo games near you, state by state. Type a ZIP code and it shows halls, days and times. "
     "https://www.findbingo.org/"),
    ("The Reefer", "https://the-reefer.com/", "the-reefer.com",
     "Adults with cannabis questions: what's legal where they live, medical cards, and clearing an old record.",
     "The Reefer answers cannabis questions for every state in plain language: what's legal, medical cards, where to "
     "buy, and how to clear an old record, each traced to a named source. https://the-reefer.com/"),
    ("OhioWeed", "https://ohioweed.org/", "ohioweed.org",
     "Ohioans with cannabis questions, and Ohio cannabis businesses.",
     "OhioWeed is a free Ohio cannabis guide: licensed dispensaries, a source-linked business directory, events, and "
     "Ohio's rules in plain language. https://ohioweed.org/"),
]


def qr_svg(url):
    svg = segno.make(url, error="m").svg_inline(dark="#143229", light="#ffffff", border=2, scale=1)
    svg = re.sub(r'width="(\d+)" height="(\d+)"',
                 lambda m: f'viewBox="0 0 {m.group(1)} {m.group(2)}" shape-rendering="crispEdges"', svg, count=1)
    return svg.replace("<svg ", '<svg aria-hidden="true" focusable="false" ', 1)


def slug(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


cards, sheet, links = [], [], []
for name, url, short, who, reply in GUIDES:
    s = slug(name)
    e = html.escape
    cards.append(f"""      <li class="guide" id="{s}">
        <div class="qr">{qr_svg(url)}</div>
        <div class="body">
          <h3><a href="{e(url)}">{e(name)}</a></h3>
          <p class="who"><b>For:</b> {e(who)}</p>
          <label class="lbl" for="reply-{s}">A reply you can paste</label>
          <textarea id="reply-{s}" rows="4" readonly>{e(reply)}</textarea>
          <p class="btns"><button type="button" data-copy="reply-{s}">Copy reply</button>
            <button type="button" data-copy-text="{e(url)}">Copy link</button></p>
        </div>
      </li>""")
    sheet.append(f"""      <li><div class="qr">{qr_svg(url)}</div><div><b>{e(name)}</b><span class="addr">{e(short)}</span>
        <span class="for">{e(who)}</span></div></li>""")
    links.append(f'  <li><a href="{url}">{name}</a>: {who}</li>')

snippet = ('<h2>Free help guides</h2>\n<ul>\n' + "\n".join(links) + '\n</ul>\n'
           '<p>Free, no sign-up, built from public sources. More at <a href="https://travisvought.com/share/">travisvought.com/share</a>.</p>')

COUNTER = ('<script>window.goatcounter={path:function(){return "/travisvought.com"+location.pathname},'
           'referrer:function(){try{var u=new URL(document.referrer);return u.origin+u.pathname}catch(e){return ""}}};</script>'
           '<script data-goatcounter="https://travisvought.goatcounter.com/count" async src="https://gc.zgo.at/count.js"></script>')

DESC = ("Help someone find help: pick the right free guide, copy a reply to paste, add the guides to your website, "
        "or print a one-page sheet for a bulletin board.")

page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Help someone find help | Free guides to share</title>
<meta name="description" content="{DESC}">
<link rel="canonical" href="{SITE}share/">
<meta property="og:type" content="website">
<meta property="og:url" content="{SITE}share/">
<meta property="og:title" content="Help someone find help">
<meta property="og:description" content="{DESC}">
<meta property="og:image" content="{SITE}og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#143229">
<meta name="color-scheme" content="light dark">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"WebPage","name":"Help someone find help","url":"{SITE}share/",
"description":"{DESC}","isPartOf":{{"@type":"WebSite","name":"Travis Vought","url":"{SITE}"}},
"breadcrumb":{{"@type":"BreadcrumbList","itemListElement":[
{{"@type":"ListItem","position":1,"name":"Travis Vought","item":"{SITE}"}},
{{"@type":"ListItem","position":2,"name":"Help someone find help","item":"{SITE}share/"}}]}}}}
</script>
<style>
@font-face{{font-family:"Archivo";src:url(/fonts/archivo.woff2) format("woff2");font-weight:100 900;font-display:swap}}
@font-face{{font-family:"Source Serif 4";src:url(/fonts/source-serif-4.woff2) format("woff2");font-weight:200 900;font-display:swap}}
:root{{--spruce:#143229;--paper:#f2f5ee;--sheet:#fff;--brass:#c79a2b;--slate:#55665e;--rule:#cfd8cd;--display:"Archivo","Arial Narrow",Arial,sans-serif;--body:"Source Serif 4",Georgia,serif}}
@media (prefers-color-scheme:dark){{:root{{--spruce:#e4ece6;--paper:#0f1f1a;--sheet:#162b24;--slate:#a9b8b0;--rule:#2c4a3f}}}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--paper);color:var(--spruce);font-family:var(--body);font-size:1.125rem;line-height:1.6}}
a{{color:inherit;text-underline-offset:.18em}}
a:hover{{text-decoration-color:var(--brass)}}
:focus-visible{{outline:3px solid var(--brass);outline-offset:3px}}
.wrap{{max-width:56rem;margin:0 auto;padding:1.5rem 1rem 3rem}}
.top{{font-family:var(--display);font-weight:700;margin:0}}
.top a{{text-decoration:none}}
h1,h2,h3{{font-family:var(--display);line-height:1.15}}
h1{{font-size:clamp(2rem,6vw,3rem);margin:1.5rem 0 .5rem;letter-spacing:-.02em}}
h2{{font-size:1.45rem;margin:3rem 0 .5rem;padding-top:1.25rem;border-top:1px solid var(--rule)}}
h3{{font-size:1.25rem;margin:0 0 .35rem}}
.lede{{font-size:1.2rem;max-width:40rem}}
.steps{{padding-left:1.25rem}}
.guides{{list-style:none;padding:0;margin:1.5rem 0 0;display:grid;gap:1rem}}
.guide{{display:grid;grid-template-columns:7rem minmax(0,1fr);gap:1.25rem;background:var(--sheet);border:1px solid var(--rule);padding:1.1rem}}
.qr svg{{display:block;width:100%;height:auto;background:#fff}}
.who{{margin:0 0 .6rem;color:var(--slate);font-size:1rem}}
.lbl{{display:block;font-family:var(--display);font-size:.9rem;font-weight:600;margin:0 0 .25rem}}
textarea{{width:100%;font:inherit;font-size:1rem;line-height:1.45;padding:.6rem;border:1px solid var(--rule);background:var(--paper);color:var(--spruce);resize:vertical}}
.btns{{display:flex;flex-wrap:wrap;gap:.5rem;margin:.5rem 0 0}}
button{{font-family:var(--display);font-weight:650;font-size:1rem;min-height:2.75rem;padding:.45rem 1rem;background:var(--sheet);color:var(--spruce);border:2px solid var(--spruce);cursor:pointer}}
button:hover,button:focus-visible{{background:var(--spruce);color:var(--paper)}}
.status{{min-height:1.5rem;font-family:var(--display);font-size:.95rem;color:var(--slate)}}
.tips li{{margin:.35rem 0}}
pre{{white-space:pre-wrap;word-break:break-word;font-size:.85rem;background:var(--sheet);border:1px solid var(--rule);padding:.8rem;max-height:16rem;overflow:auto}}
.sheet{{display:none}}
footer{{margin-top:3rem;padding-top:1rem;border-top:1px solid var(--rule);color:var(--slate);font-size:.95rem}}
@media (max-width:34rem){{.guide{{grid-template-columns:1fr}}.guide .qr{{width:7rem}}}}
@media print{{
  @page{{margin:.45in}}
  body{{background:#fff;color:#000;font-size:11pt}}
  .screen{{display:none!important}}
  .sheet{{display:block}}
  .sheet h1{{font-size:24pt;margin:0 0 4pt}}
  .sheet p{{margin:0 0 10pt}}
  .sheet ul{{list-style:none;padding:0;margin:0;display:grid;grid-template-columns:1fr 1fr;gap:10pt 18pt}}
  .sheet li{{display:grid;grid-template-columns:1.05in 1fr;gap:8pt;align-items:start;break-inside:avoid}}
  .sheet b{{display:block;font-family:var(--display);font-size:13pt}}
  .sheet .addr{{display:block;font-family:var(--display);font-size:11pt}}
  .sheet .for{{display:block;font-size:9.5pt;line-height:1.3}}
  .sheet .foot{{margin-top:12pt;font-size:9.5pt}}
}}
</style>
{COUNTER}
</head>
<body>
<div class="wrap screen">
<p class="top"><a href="/">Travis Vought</a></p>
<main>
<h1>Help someone find help</h1>
<p class="lede">When someone asks where to turn, you can point them to a free guide in a few seconds. Pick the guide, copy the reply, paste it. Every guide is free, needs no sign-up, and is built from public sources.</p>
<ol class="steps">
  <li>Find the guide that fits the person below.</li>
  <li>Copy the reply and paste it where they asked, or show them the QR code.</li>
  <li>If you know their state or town, add it. A reply that answers their exact question helps most.</li>
</ol>
<p class="status" id="status" role="status" aria-live="polite"></p>

<h2>The guides</h2>
<ul class="guides">
{chr(10).join(cards)}
</ul>

<h2>Answering in groups and forums</h2>
<ul class="tips">
  <li>Answer the question first, then share the link. People trust a reply that helps before it points somewhere.</li>
  <li>Check the group's rules. Many allow helpful links but not repeated posts of the same link.</li>
  <li>Share the page for their state when you can. Each guide has state pages.</li>
  <li>If someone is in danger or crisis, point them to 911 or the 988 Suicide and Crisis Lifeline first.</li>
</ul>

<h2>Put the guides on your website</h2>
<p>Libraries, county offices, churches, senior centers, schools and nonprofits are welcome to list the guides. Copy this and paste it into your resources page.</p>
<pre id="snippet">{html.escape(snippet)}</pre>
<p class="btns"><button type="button" data-copy="snippet">Copy the website code</button></p>

<h2>Print a sheet for a bulletin board</h2>
<p>One page with every guide and its QR code, for a library, waiting room, food pantry, senior center or VFW hall.</p>
<p class="btns"><button type="button" id="print">Print the sheet</button></p>
<p>Want flyers for one guide? The veteran guide has <a href="https://guide.vethomeguard.org/flyers.html">printable flyers</a>, and Mobility Talk has a <a href="https://mobilitytalk.org/handout.html">printable help list for each state</a>.</p>

<h2>Something wrong or missing?</h2>
<p>If a listing is out of date or a kind of help is missing, <a href="https://www.vethomeguard.org/contact.html">tell me</a> and I fix it.</p>
</main>
<footer><p>Travis Vought, Marengo, Ohio. <a href="/">All the guides</a> · <a href="/privacy/">Privacy</a></p></footer>
</div>

<div class="sheet" aria-hidden="true">
  <h1>Free help guides</h1>
  <p>Free, no sign-up. Scan a code with your phone camera, or type the address.</p>
  <ul>
{chr(10).join(sheet)}
  </ul>
  <p class="foot">In danger: call 911. In crisis: call or text 988. All guides: travisvought.com/share</p>
</div>

<script>
(function () {{
  var status = document.getElementById('status');
  var timer;
  function say(t) {{ status.textContent = t; clearTimeout(timer); timer = setTimeout(function () {{ status.textContent = ''; }}, 5000); }}
  function copy(text) {{
    if (navigator.clipboard && window.isSecureContext) {{
      navigator.clipboard.writeText(text).then(function () {{ say('Copied. Paste it where they asked.'); }},
        function () {{ say('Copy did not work. Select the text and copy it.'); }});
    }} else {{ say('Copy did not work. Select the text and copy it.'); }}
  }}
  document.querySelectorAll('[data-copy]').forEach(function (b) {{
    b.addEventListener('click', function () {{
      var el = document.getElementById(b.getAttribute('data-copy'));
      copy((el.value || el.textContent).trim());
    }});
  }});
  document.querySelectorAll('[data-copy-text]').forEach(function (b) {{
    b.addEventListener('click', function () {{ copy(b.getAttribute('data-copy-text')); }});
  }});
  document.getElementById('print').addEventListener('click', function () {{ window.print(); }});
}})();
</script>
</body>
</html>
"""

out = repo / "share"
out.mkdir(exist_ok=True)
(out / "index.html").write_text(page)
print(f"Wrote {out / 'index.html'} with {len(GUIDES)} guides")

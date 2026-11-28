# Writes travisvought.com/shop/aids/ : adaptive aids printed to order, email ordering like the shop page.
import re, urllib.parse, html
import os, sys
ROOT = sys.argv[1] if len(sys.argv) > 1 else "."
SHOP = os.path.join(ROOT, "shop/index.html")
OUT = os.path.join(ROOT, "shop/aids/index.html")
EMAIL = "veteranhomeguardians@gmail.com"
src = open(SHOP).read()
style = src[src.index("<style>"):src.index("</style>") + 8]
style = style.replace(".other p{margin:0}", ".other p{margin:0}\n.facts{max-width:44rem;margin:0;padding-left:1.2rem}\n.facts li{margin:0 0 .5rem}\n.inline{font-weight:700}")
MAIL_ICON = '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M3.5 6h17v12h-17zM4 6.5l8 6.5 8-6.5"/></svg>'

def mailto(subject, lines):
    body = "Hello,\r\n\r\n" + "\r\n".join(lines) + "\r\n\r\nThank you"
    q = lambda s: urllib.parse.quote(s, safe="")
    return html.escape(f"mailto:{EMAIL}?subject={q(subject)}&body={q(body)}", quote=True)

def order_link(name, quote=False):
    lines = [f"I'd like {'a quote for' if quote else 'to order'}: {name}", "", "Quantity:", "Color, if you have a preference:",
             "Shipping address:", "Anything else:"]
    label = "Get a quote" if quote else "Order"
    return f'<a class="order" href="{mailto(("Quote: " if quote else "Order: ") + name, lines)}">{MAIL_ICON}{label}<span class="vh"> the {name.lower()} by email</span></a>'

SHADOW = '<ellipse cx="120" cy="{cy}" rx="{rx}" ry="5" fill="#143229" opacity=".14"/>'
G, GD, GL = "#2c6a55", "#1d4c3c", "#3f8169"
ITEMS = [
 ("utensil", "Built-up utensil handle", "$12",
  "A thick, ridged handle that a fork or spoon slides into, for weak grip, arthritis or tremor. A small wedge locks the utensil in place, so one handle fits most silverware.",
  "Hand wash in warm water, not the dishwasher.",
  "Drawing of a thick green handle with finger ridges and a fork sticking out of one end",
  SHADOW.format(cy=126, rx=96) +
  f'<rect x="22" y="60" width="132" height="46" rx="22" fill="{G}"/><path d="M40 66h96" stroke="#fff" stroke-width="3" stroke-linecap="round" opacity=".18"/>'
  f'<path d="M58 64v38M86 64v38M114 64v38" stroke="{GD}" stroke-width="5" stroke-linecap="round"/>'
  '<path d="M154 79l40-3v14l-40-3z" fill="#aeb6b9"/><rect x="192" y="70" width="14" height="26" rx="5" fill="#aeb6b9"/>'
  '<path d="M204 73h22M204 79.7h22M204 86.3h22M204 93h22" stroke="#aeb6b9" stroke-width="3.4" stroke-linecap="round"/>'
  '<path d="M160 80l30-2" stroke="#fff" stroke-width="1.4" opacity=".5"/>'),
 ("pen", "Pen and pencil grip", "$8",
  "A soft triangle grip that slides onto most pens and pencils, so writing takes less pinch.",
  None,
  "Drawing of a pen at an angle with a fat green triangular grip near its tip",
  SHADOW.format(cy=132, rx=80) +
  '<g transform="translate(120 84) rotate(-26)"><rect x="-96" y="-7" width="156" height="14" rx="3" fill="#d6dfd9" stroke="#8f9b95"/>'
  '<rect x="-96" y="-7" width="22" height="14" rx="3" fill="#3a5a8c"/><path d="M60-6l26 6-26 6z" fill="#e8dcc0" stroke="#8f9b95"/><path d="M80-1.5l6 1.5-6 1.5z" fill="#2a302d"/>'
  f'<rect x="-6" y="-17" width="62" height="34" rx="13" fill="{G}"/><path d="M8-15v30M22-15v30M36-15v30" stroke="{GD}" stroke-width="3" stroke-linecap="round"/>'
  '<path d="M0-11h50" stroke="#fff" stroke-width="2" stroke-linecap="round" opacity=".2"/></g>'),
 ("key", "Key turner", "$10",
  "A big paddle that holds a house or car key, so turning it takes a whole hand instead of two fingers. Fastens to the key with a small zip tie or bolt.",
  None,
  "Drawing of a green paddle with a thumb dip and a hang-up hole, holding a brass key that sticks out of one end",
  SHADOW.format(cy=128, rx=92) +
  f'<rect x="30" y="56" width="128" height="52" rx="16" fill="{G}"/><ellipse cx="84" cy="82" rx="26" ry="15" fill="{GD}" opacity=".55"/>'
  '<circle cx="46" cy="82" r="7" class="hole"/><circle cx="140" cy="82" r="3.2" fill="#aeb6b9"/><circle cx="126" cy="82" r="3.2" fill="#aeb6b9"/>'
  '<path d="M158 75h50l6 7-6 7h-6l-3 5-4-5h-5l-3 5-4-5h-25z" fill="#d9ad45" stroke="#a67b17" stroke-width="1"/>'
  '<path d="M162 79h44" stroke="#a67b17" stroke-width="1.2"/>'),
 ("button", "Button hook and zipper pull", "$9",
  "One handle with a wire-style loop that pulls buttons through buttonholes and a hook that catches a zipper tab, for dressing with one hand or stiff fingers.",
  None,
  "Drawing of a green handle with a teardrop loop on the left end and a small hook on the right end, next to a shirt button",
  SHADOW.format(cy=124, rx=94) +
  f'<rect x="70" y="70" width="104" height="26" rx="13" fill="{G}"/><path d="M82 75h80" stroke="#fff" stroke-width="2.4" stroke-linecap="round" opacity=".2"/>'
  f'<path d="M72 83C56 72 28 68 22 83 28 98 56 94 72 83z" fill="none" stroke="{G}" stroke-width="5" stroke-linejoin="round"/>'
  f'<path d="M172 83h34a9 9 0 0 1 0 18h-16" fill="none" stroke="{G}" stroke-width="6" stroke-linecap="round"/>'
  '<circle cx="48" cy="120" r="11" fill="#d6dfd9" stroke="#8f9b95"/><g fill="#8f9b95"><circle cx="45" cy="117" r="1.6"/><circle cx="51" cy="117" r="1.6"/><circle cx="45" cy="123" r="1.6"/><circle cx="51" cy="123" r="1.6"/></g>'),
 ("page", "Page turner", "$9",
  "A light wand with a ridged tip that catches the edge of a page. Slip a pencil-cap eraser over the end for extra grip.",
  None,
  "Drawing of an open book with a green wand lifting the corner of a page",
  SHADOW.format(cy=146, rx=86) +
  '<path d="M36 118l82-10v32l-82 6z" fill="#fbfbf7" stroke="#8f9b95"/><path d="M122 108l82 10v28l-82-6z" fill="#fbfbf7" stroke="#8f9b95"/>'
  '<path d="M48 124l62-7M48 131l62-7M134 117l58 7M134 124l40 5" stroke="#cfd8cd" stroke-width="1.6"/>'
  '<path d="M184 121q12-18 22-16l-2 14z" fill="#eef1ec" stroke="#8f9b95"/>'
  f'<path d="M56 36L190 108" stroke="{G}" stroke-width="11" stroke-linecap="round"/><path d="M150 86L196 112" stroke="{GL}" stroke-width="5" stroke-linecap="round"/>'
  '<circle cx="50" cy="33" r="8" fill="#e7a3a3"/>'),
 ("pill", "Blister-pack pill pusher", "$12",
  "Set the pill’s bubble over the hole and press the round top with your palm. The pill pops through the foil and drops into the base instead of onto the floor.",
  None,
  "Drawing of a green round base with a blister pack on top and a mushroom-shaped plunger above it",
  SHADOW.format(cy=136, rx=62) +
  f'<rect x="68" y="88" width="104" height="44" fill="{G}"/><ellipse cx="120" cy="132" rx="52" ry="10" fill="{G}"/><ellipse cx="120" cy="88" rx="52" ry="12" fill="{GL}"/>'
  '<rect x="104" y="108" width="32" height="24" fill="#143229" opacity=".55"/><ellipse cx="120" cy="126" rx="6" ry="3.4" fill="#fbfbf7"/>'
  '<rect x="92" y="78" width="56" height="12" rx="2" fill="#cfd5d7" stroke="#8f9b95"/><g fill="#eef1ec" stroke="#8f9b95"><ellipse cx="106" cy="82" rx="5" ry="3"/><ellipse cx="120" cy="82" rx="5" ry="3"/><ellipse cx="134" cy="82" rx="5" ry="3"/></g>'
  f'<rect x="115" y="40" width="10" height="30" rx="2" fill="{GD}"/><path d="M90 44q30-34 60 0z" fill="{G}"/>'),
 ("cup", "Wheelchair cup holder", "$22",
  "Straps to a wheelchair or walker frame tube 7/8 to 1 inch thick with two zip ties or hook-and-loop straps. Holds cups, cans and bottles up to 3.3 inches across.",
  "Tell us the chair or walker model if you know it, and we’ll check the fit.",
  "Drawing of a green cup holder strapped to a metal frame tube, holding a paper cup",
  SHADOW.format(cy=146, rx=80) +
  '<rect x="178" y="8" width="16" height="142" rx="3" fill="#aeb6b9"/><path d="M182 12v134" stroke="#fff" stroke-width="2" opacity=".5"/>'
  '<path d="M80 26h60l-6 50H86z" fill="#fbfbf7" stroke="#8f9b95"/><ellipse cx="110" cy="26" rx="30" ry="5" fill="#eef1ec" stroke="#8f9b95"/>'
  f'<rect x="60" y="62" width="100" height="62" fill="{G}"/><ellipse cx="110" cy="124" rx="50" ry="10" fill="{G}"/><ellipse cx="110" cy="62" rx="50" ry="10" fill="{GL}"/>'
  '<ellipse cx="110" cy="62" rx="42" ry="7" fill="#143229" opacity=".45"/><path d="M98 62l-1.5-6h27l-1.5 6z" fill="#fbfbf7"/>'
  f'<rect x="156" y="66" width="26" height="54" rx="3" fill="{GD}"/><rect x="152" y="74" width="48" height="7" rx="2" fill="#143229"/><rect x="152" y="104" width="48" height="7" rx="2" fill="#143229"/>'),
]

def card(slug, name, price, desc, note, aria, art):
    n = f'      <p class="note">{note}</p>\n' if note else ""
    return f'''  <li><article class="item" aria-labelledby="{slug}-h">
    <div class="body">
      <h3 id="{slug}-h">{name}</h3>
      <p class="tag">Printed to order</p>
      <p class="desc">{desc}</p>
{n}      <div class="buy">
        <p class="price">{price}</p>
        {order_link(name)}
      </div>
    </div>
    <svg class="art" viewBox="0 0 240 160" role="img" aria-label="{aria}" focusable="false">{art}</svg>
  </article></li>'''

items_html = "\n".join(card(*it) for it in ITEMS)
facility_lines = ["We'd like to order adaptive aids for our facility.", "", "Facility name:", "Your name and phone:",
                  "Items and quantities:", "- Built-up utensil handle:", "- Pen and pencil grip:", "- Key turner:",
                  "- Button hook and zipper pull:", "- Page turner:", "- Blister-pack pill pusher:", "- Wheelchair cup holder:",
                  "- Playing card holder:", "- Bottle and can opener:", "", "Colors, if you have a preference:",
                  "Delivery address:", "Date you need them by:", "Anything else:"]
custom_lines = ["Something a resident or family member struggles with:", "", "What it is (a door handle, a phone, a remote, a cup...):",
                "What makes it hard (grip, reach, one hand, tremor...):", "Photos or measurements, if you have them (attach to this email):",
                "Your name and phone:", "Anything else:"]
samples_lines = ["We'd like to see the adaptive aid samples on a visit.", "", "Facility name and town:", "Your name and phone:",
                 "Best days and times:", "Anything else:"]

FAC = mailto("Facility order: adaptive aids", facility_lines)
CUS = mailto("Custom aid request", custom_lines)
SAM = mailto("Sample visit: adaptive aids", samples_lines)
DESC = "Simple 3D-printed aids for eating, writing, dressing and getting around with weak grip, arthritis, tremor or limited reach. Printed to order in Marengo, Ohio, for nursing homes, families and individuals."

page = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Everyday aids, printed to order | Travis Vought</title>
<meta name="description" content="{DESC}">
<link rel="canonical" href="https://travisvought.com/shop/aids/">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Travis Vought">
<meta property="og:url" content="https://travisvought.com/shop/aids/">
<meta property="og:title" content="Everyday aids, printed to order | Travis Vought">
<meta property="og:description" content="{DESC}">
<meta property="og:image" content="https://travisvought.com/og.png">
<meta name="twitter:card" content="summary">
<meta name="theme-color" content="#143229">
<meta name="color-scheme" content="light dark">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
{style}
</head>
<body>
<a class="skip" href="#main">Skip to main content</a>
<div class="wrap">
<header class="top"><a href="/">Travis Vought</a><a class="back" href="/shop/">All made-to-order items</a></header>
<main id="main">
<h1>Everyday aids, printed to order</h1>
<div class="bar" aria-hidden="true"></div>
<p class="lede">Simple tools that make eating, writing, dressing and getting around easier with weak grip, arthritis, tremor or limited reach. Printed to order in Marengo, Ohio, for nursing homes, assisted living, families and individuals.</p>
<p class="lede">Prices include US shipping. Order one, or send a list for your whole facility.</p>
<ol class="how" role="list" aria-label="How ordering works">
  <li><b aria-hidden="true">1</b><svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><use href="/icons.svg#chat"/></svg><span>Email what you need and how many</span></li>
  <li><b aria-hidden="true">2</b><svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><use href="/icons.svg#yes"/></svg><span>We confirm and send a secure payment link</span></li>
  <li><b aria-hidden="true">3</b><svg viewBox="0 0 24 24" aria-hidden="true" focusable="false" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3l8 4v10l-8 4-8-4V7zM4 7l8 4 8-4M12 11v10M8 5l8 4"/></svg><span>We print them and ship them to you</span></li>
</ol>

<section aria-labelledby="facility">
<h2 id="facility"><span class="sym"><svg viewBox="0 0 24 24" aria-hidden="true" focusable="false" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M3 21h18M5 21V8l7-5 7 5v13M9 21v-5h6v5M9 11h.01M15 11h.01"/></svg></span>For care facilities</h2>
<p class="sub">Activity directors, nurses and therapists can order for several residents in one email.</p>
<div class="other">
  <p><a class="btn" href="{FAC}">{MAIL_ICON}Send a facility order<span class="vh"> by email</span></a></p>
  <p>Facilities Veteran Home Guardians visits in Morrow and Knox counties can ask to see the samples on a visit. <a class="inline" href="{SAM}">Ask for a sample visit<span class="vh"> by email</span></a>.</p>
</div>
</section>

<section aria-labelledby="aids">
<h2 id="aids"><span class="sym"><svg viewBox="0 0 24 24" aria-hidden="true" focusable="false" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M4 21V3h16v18M4 7h16M10.5 7v3l1.5 1.5L13.5 10V7M8 21v-2.5h8V21M8 16h8"/></svg></span>The aids</h2>
<p class="sub">Each one is our own design, printed in sturdy plastic with rounded edges and no small loose parts.</p>
<ul class="items" role="list">
{items_html}
</ul>
<p class="sub" style="margin-top:1.5rem">Also printed to order: the <a href="/shop/#card-holder-h">playing card holder</a> ($12) and the <a href="/shop/#opener-h">bottle and can opener</a> ($10).</p>
</section>

<section aria-labelledby="custom">
<h2 id="custom"><span class="sym"><svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><use href="/icons.svg#chat"/></svg></span>Need something that isn’t here?</h2>
<div class="other">
  <p>Tell us what someone struggles with, like a door handle, a remote, a phone or a cup, and what makes it hard. We’ll design a part, print one to try, and quote it.</p>
  <p><a class="btn line" href="{CUS}">{MAIL_ICON}Describe what you need<span class="vh"> by email</span></a></p>
</div>
</section>

<section aria-labelledby="good">
<h2 id="good"><span class="sym"><svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><use href="/icons.svg#yes"/></svg></span>Good to know</h2>
<ul class="facts">
  <li>These are everyday helpers, not medical devices. For anything that is part of a care plan, check with the person’s occupational therapist.</li>
  <li>Clean with soap and warm water or a disinfecting wipe. Keep them out of the dishwasher and away from heat, which can bend the plastic.</li>
  <li>Most orders ship in 7 to 10 business days. Large facility orders may take longer; we’ll tell you when we confirm.</li>
</ul>
</section>

<section class="other" aria-labelledby="other">
<h2 id="other"><span class="sym"><svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><use href="/icons.svg#chat"/></svg></span>Other ways to order</h2>
<p>Order button not opening your email? Write to us at the address below and name the item you want.</p>
<p><a class="btn line addr" href="mailto:{EMAIL}">{MAIL_ICON}<span class="vh">Email </span>{EMAIL}</a></p>
</section>
</main>
<footer>
  <p>Travis Vought, Marengo, Ohio.</p>
  <p><a href="/shop/">Made to order</a> · <a href="/">Home page</a> · <a href="/privacy/">Privacy</a></p>
</footer>
</div>
<script>window.goatcounter={{path:function(){{return "/travisvought.com"+location.pathname}},referrer:function(){{try{{var u=new URL(document.referrer);return u.origin+u.pathname}}catch(e){{return ""}}}}}};</script><script data-goatcounter="https://vhg-guide.goatcounter.com/count" async src="https://gc.zgo.at/count.js"></script>
</body>
</html>
'''
open(OUT, "w").write(page)
print("wrote", OUT, len(page))

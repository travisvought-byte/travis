# travisvought.com

Personal site for Travis Vought: one page that points people to every free guide, explains what he provides, gives his background, and makes him easy to introduce and contact. Plain HTML on GitHub Pages, no build step.

## Short links

Easy to say out loud, print on a flyer or put on a billboard. Each one forwards to the full site.

| Short link | Goes to |
|---|---|
| travisvought.com/vhg | vethomeguard.org |
| travisvought.com/guide (or /veterans) | guide.vethomeguard.org |
| travisvought.com/mobility (or /disability) | mobilitytalk.org |
| travisvought.com/moms | yogamomtalk.com |
| travisvought.com/bingo | ohiobingo.org |
| travisvought.com/weed (or /cannabis) | ohioweed.org |
| travisvought.com/mif | themif.org |
| travisvought.com/flyers | printable flyers in the veteran guide |
| travisvought.com/contact | Veteran Home Guardians contact page |
| travisvought.com/donate | Veteran Home Guardians donation page |
| travisvought.com/sponsor | Sponsor a guide |
| travisvought.com/github | github.com/travisvought-byte |
| travisvought.com/books | Travis's books on Amazon |

To add one, make a folder with the short name and copy any existing `index.html` into it, then change the address and title. Or add it to the list in `tools/build_assets.py` and run `python3 tools/build_assets.py . /tmp/render`, which also rebuilds the QR code, the 404 page and the robots and sitemap files. A newer version of segno can write a slightly different `qr.png` for the same address; if the address hasn't changed, keep the committed QR images (`git checkout qr.png qr.svg`).

## Files

- `index.html`: the page.
- `share/index.html`: "Help someone find help": every guide with a ready reply to paste, a QR code, website code for partners and a one-page sheet to print. Built by `python3 tools/build_share.py .` (needs `pip install segno`); edit the list in that script, then re-run.
- `adults/index.html`: "For adults": the guide for adults 18 and over (Strip Club Etiquette, stripclubguide.org), kept on its own page with an age note and framed by its purpose, dancer welfare and stopping trafficking. The home page points to it from a "For adults" group at the end of the guide list. Keep Veteran Home Guardians branding off this page.
<<<<<<< HEAD
- `shop/index.html`: "Made to order": handmade laser-engraved and 3D-printed items from the Marengo workshop, each with its price and an Order button that opens an email to veteranhomeguardians@gmail.com with the subject and a short order form filled in, plus a text-message link. The product drawings are inline SVG in the page. Hand-written; when you change an item's name or order form, re-encode its mailto link (spaces as %20, line breaks as %0D%0A, & between subject and body written as &amp;). The home page links to it from "I'm here…" and the footer.
=======
- `beekeepers/index.html`: "Ohio beekeepers": apiary registration, every club on the Ohio State Beekeepers Association list, classes, Ohio suppliers, grants and loss help, veteran beekeeping programs, Ohio's rules for selling honey (with code sections) and 2026 honey prices. Hand-written; each entry was checked against its source on the date in the page, so re-check dated items (deadlines, class dates) when you edit it.
>>>>>>> origin/main
- `open-data/index.html`: "Open data": each guide's dataset with what it covers, its license (data CC BY 4.0, code MIT), credit line and download folder, plus the open projects the guides draw on. Hand-written; keep the credit lines matching each repository's LICENSE.
- `photos/`: the portrait in the opening and the photo beside the background list, each in two sizes. They are saved without the camera's location data; keep it that way when adding more.
- `icons.svg`: the line symbols on the home page and the share page, drawn for this site on a 24-pixel grid: one per guide (the same one wherever that guide appears), plus the symbols beside What I provide, the Background timeline and Get involved. Each sits beside words that already say the same thing, so it is hidden from screen readers. Use one with `<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><use href="/icons.svg#vhg"/></svg>`. The short-link pages show the symbol of the site they forward to, the 404 page shows one beside each guide, and the Privacy page uses `yes` and `no` beside its At a glance lists. The short-link and 404 pages are written by `tools/build_assets.py` (its `ICON` list picks each short link's symbol).
- `og.png`: the picture shown when the link is shared on Facebook, LinkedIn, X or in a text message.
- `qr.png`, `qr.svg`: QR code for travisvought.com. Use the SVG for large prints and billboards.
- `favicon.ico`, `favicon-32.png`, `apple-touch-icon.png`: browser and phone icons.
- `404.html`: shown for mistyped addresses, with links to every guide.
- `fonts/`: Archivo and Source Serif 4, hosted here so the page loads without outside requests. Both are under the SIL Open Font License (see the license files).
- `sitemap.xml`, `robots.txt`: help search engines find the page.
- `CNAME`: tells GitHub Pages to serve the site at travisvought.com.

## Visit counts

Every page and short link reports to the shared GoatCounter dashboard at https://vhg-guide.goatcounter.com/ under paths that start `/travisvought.com/` (for example `/travisvought.com/weed` for the short link printed on cannabis flyers). Short links count the visit, then forward within 1.2 seconds; without JavaScript the page still forwards after 2 seconds. The counter snippet lives in `tools/build_assets.py` (`COUNTER`) and is pasted once into `index.html`.

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

To add one, make a folder with the short name and copy any existing `index.html` into it, then change the address and title. Or add it to the list in `tools/build_assets.py` and run `python3 tools/build_assets.py . /tmp/render`, which also rebuilds the QR code, the 404 page and the robots and sitemap files.

## Files

- `index.html`: the page.
- `og.png`: the picture shown when the link is shared on Facebook, LinkedIn, X or in a text message.
- `qr.png`, `qr.svg`: QR code for travisvought.com. Use the SVG for large prints and billboards.
- `favicon.ico`, `favicon-32.png`, `apple-touch-icon.png`: browser and phone icons.
- `404.html`: shown for mistyped addresses, with links to every guide.
- `fonts/`: Archivo and Source Serif 4, hosted here so the page loads without outside requests. Both are under the SIL Open Font License (see the license files).
- `sitemap.xml`, `robots.txt`: help search engines find the page.
- `CNAME`: tells GitHub Pages to serve the site at travisvought.com.

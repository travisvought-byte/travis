#!/usr/bin/env python3
"""Builds the Grants for Real guide in grants/.

Edit the page text here, then run from the repo root:
    python3 tools/build_grants.py
Every link inside grants/ is relative, so the folder can move to its own
repository and domain unchanged.
"""
import os, html

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "grants")
BASE = "https://travisvought.com/grants/"
CHECKED = "November 27, 2026"

def ico(name, cls=""):
    c = f' class="{cls}"' if cls else ""
    return f'<svg{c} viewBox="0 0 24 24" aria-hidden="true" focusable="false"><use href="assets/icons.svg#{name}"/></svg>'

def a(url, text):
    return f'<a href="{url}">{text}</a>'

FP = '<span class="unsourced">Field practice</span>'

# ---- sources (read for this guide on the date in CHECKED) ----
S = {
 "gusa": ("Giving USA 2026 press release", "https://givingusa.org/giving-usa-charitable-giving-rose-to-617-20-billion-in-2025-surpassing-the-600-billion-mark-for-the-first-time/"),
 "epa24": ("EPA: what's new in the 2024 revision to 2 CFR 200", "https://www.epa.gov/grants/whats-new-uniform-grants-guidance-2024-revision-2-cfr-200"),
 "205": ("2 CFR 200.205, merit review", "https://www.law.cornell.edu/cfr/text/2/200.205"),
 "206": ("2 CFR 200.206, review of risk", "https://www.law.cornell.edu/cfr/text/2/200.206"),
 "334": ("2 CFR 200.334, record retention", "https://www.law.cornell.edu/cfr/text/2/200.334"),
 "403": ("2 CFR 200.403, allowable costs", "https://www.law.cornell.edu/cfr/text/2/200.403"),
 "414": ("2 CFR 200.414, indirect costs", "https://www.law.cornell.edu/cfr/text/2/200.414"),
 "appi": ("2 CFR 200 Appendix I, what a funding notice must say", "https://www.law.cornell.edu/cfr/text/2/appendix-I_to_part_200"),
 "25200": ("2 CFR 25.200, keeping SAM.gov registration active", "https://www.law.cornell.edu/cfr/text/2/25.200"),
 "ggreg": ("Grants.gov: organization registration", "https://grants.gov/applicants/applicant-registration/organization-registration"),
 "ggerr": ("Grants.gov: error messages", "https://www.grants.gov/applicants/encountering-error-messages"),
 "ggscam": ("Grants.gov: grant-related scams", "https://www.grants.gov/learn-grants/grant-fraud/grant-related-scams.html"),
 "usagov": ("USAGov: avoid free money scams", "https://www.usa.gov/no-free-money"),
 "ftc": ("FTC consumer alert, March 2026", "https://consumer.ftc.gov/consumer-alerts/2026/03/how-avoid-government-grant-scams-offer-free-money-personal-expenses"),
 "afp": ("AFP Code of Ethical Standards, Standard 21", "https://afpglobal.org/ethical-standard-deep-dive-standard-21"),
 "sfe": ("Standards for Excellence: paying a fundraiser a percentage", "https://standardsforexcellence.org/digArticle/Can-My-Nonprofit-Pay-a-Fundraising-Consultant-a-Percentage-of-What-They-Bring-In"),
 "irsrev": ("IRS: automatic revocation for not filing", "https://www.irs.gov/charities-non-profits/automatic-revocation-of-exemption-for-nonfiling-overview"),
 "irs990n": ("IRS: who must file Form 990-N", "https://www.irs.gov/charities-non-profits/annual-electronic-notice-form-990-n-for-small-organizations-faqs-who-must-file"),
 "teos": ("IRS Tax Exempt Organization Search", "https://www.irs.gov/charities-non-profits/tax-exempt-organization-search"),
 "pfpay": ("IRS: private foundation failure to distribute", "https://www.irs.gov/charities-non-profits/private-foundations/taxes-on-failure-to-distribute-income-private-foundations"),
 "mir": ("IRS: private foundation minimum investment return", "https://www.irs.gov/charities-non-profits/private-foundations/minimum-investment-return"),
 "ppx": ("ProPublica Nonprofit Explorer", "https://projects.propublica.org/nonprofits/"),
 "ohgp": ("Ohio Grants Partnership policy (Ohio OBM)", "https://finsource.ohio.gov/SAFEManual/Grants/ohio_grants_partnership_policy.htm"),
 "ohjob": ("Ohio OBM job aid: searching and applying for funding", "https://archives.obm.ohio.gov/Files/Grants/Job_Aid/searching_and_applying_for_funding_opportunities.pdf"),
 "ohag": ("Ohio Attorney General: starting a charity in Ohio", "https://charitable.ohioago.gov/Charity-Registration/Starting-a-Charity-in-Ohio"),
 "ohagsheet": ("Ohio Attorney General: online registration information sheet", "https://charitable.ohioago.gov/Charity-Registration/Publications/Online-Charitable-Registration-Information-Sheet"),
 "fs": ("Nonprofit Law Blog: do you really know what fiscal sponsorship is?", "https://nonprofitlawblog.com/do-you-really-know-what-fiscal-sponsorship-is/"),
 "candid": ("Candid: free access to Candid search", "https://candid.org/blogs/search-nonprofits-candid-free-access/"),
}

def src(*keys):
    return '<p class="cite">Source' + ("s" if len(keys) > 1 else "") + ": " + "; ".join(a(S[k][1], S[k][0]) for k in keys) + ".</p>"

def s(k, text=None):
    return a(S[k][1], text or S[k][0])

NAV = [("index.html", "Start"), ("ready.html", "Get ready"), ("find.html", "Find grants"), ("federal.html", "Federal"),
       ("foundations.html", "Foundations"), ("write.html", "Write it"), ("sponsor.html", "No 501(c)(3)?"),
       ("myths.html", "Myths"), ("play.html", "Practice round"), ("sources.html", "Sources")]

SISTERS = [("https://travisvought.com/", "website", "All of Travis's guides"),
           ("https://earthrules.org/", "earth-rules", "Earth Rules"),
           ("https://mobilitytalk.org/", "mobility", "Mobility Talk"),
           ("https://vethomeguard.org/", "vhg", "Veteran Home Guardians")]

def page(slug, title, desc, h1, body, script=""):
    nav = "".join(f'<li><a href="{h}"' + (' aria-current="page"' if h == slug else "") + f'>{t}</a></li>' for h, t in NAV)
    sis = "".join(f'<li><a href="{u}">{ico(i)}{t}</a></li>' for u, i, t in SISTERS)
    url = BASE + ("" if slug == "index.html" else slug)
    full = f"{title} | Grants for Real" if slug != "index.html" else title
    out = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(full)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Grants for Real">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:image" content="https://travisvought.com/og.png">
<meta name="twitter:card" content="summary">
<meta name="theme-color" content="#143229">
<meta name="color-scheme" content="light dark">
<link rel="icon" href="https://travisvought.com/favicon.ico" sizes="any">
<link rel="stylesheet" href="assets/site.css">
</head>
<body>
<a class="skip" href="#main">Skip to main content</a>
<div class="wrap">
<header class="top">
<a class="brand" href="index.html">{ico("bank")}Grants for Real</a>
<nav class="sitenav" aria-label="Grants for Real">
<ul>{nav}</ul>
</nav>
</header>
<main id="main">
<h1>{h1}</h1>
{body}
</main>
<footer>
<p>Grants for Real is a free guide. It explains rules and public data in plain words; it is not legal or tax advice, and no funder pays to be on it.</p>
<p>Wrong, outdated or missing something? <a href="https://travisvought.com/contact/">Tell me</a> and I'll fix it. Pages checked against their sources on {CHECKED}.</p>
<p>More free guides:</p>
<ul class="sisters">{sis}</ul>
<p>Made by Travis Vought, Marengo, Ohio. <a href="https://travisvought.com/privacy/">Privacy</a></p>
</footer>
</div>
{script}<script>window.goatcounter={{path:function(){{return "/travisvought.com"+location.pathname}},referrer:function(){{try{{var u=new URL(document.referrer);return u.origin+u.pathname}}catch(e){{return ""}}}}}};</script><script data-goatcounter="https://vhg-guide.goatcounter.com/count" async src="https://gc.zgo.at/count.js"></script>
</body>
</html>
"""
    with open(os.path.join(ROOT, slug), "w") as f:
        f.write(out)

def jump(items):
    return '<nav aria-label="On this page"><ul class="jump">' + "".join(f'<li><a href="#{i}">{t}</a></li>' for i, t in items) + "</ul></nav>"

def h2(id_, icon, text):
    return f'<h2 id="{id_}">{ico(icon)}{text}</h2>'

CHK = f'<p class="checked">Checked against each source on {CHECKED}. {FP} marks experienced practitioners\' judgment rather than a rule or a dataset.</p>'

# ===================== index =====================
page("index.html", "Grants for Real: how grant funding actually works",
 "A free guide to grant writing and grant funding built from funders' own rules and public data: where grants come from, what reviewers score, what gets funded, myths versus reality, and a practice round.",
 "Grants for Real",
 f"""<p class="lede">How grant funding actually works, taken from the rules funders have to follow, their published review criteria, and public money data. Not opinions.</p>
<p>Most grant advice online is somebody's hunch repeated until it sounds like a rule. This guide sticks to what you can check: federal regulations, funders' own guidelines, IRS rules, state portals and the numbers on who gives what. Where something is experienced judgment and not a rule, it says so with a {FP} tag.</p>
{CHK}
{h2("start", "map", "Pick your starting point")}
<ul class="paths">
<li><a href="ready.html">{ico("review")}<span><b>We're new to grants</b><span>The foundations a funder checks before it reads a word you wrote.</span></span></a></li>
<li><a href="sponsor.html">{ico("give")}<span><b>We don't have a 501(c)(3)</b><span>How fiscal sponsorship lets a group take grant money, and the two common setups.</span></span></a></li>
<li><a href="find.html">{ico("search")}<span><b>We're ready. Where's the money?</b><span>Federal, Ohio and other states, foundations and companies, and how to qualify a funder.</span></span></a></li>
<li><a href="federal.html">{ico("flag")}<span><b>We're going federal</b><span>Registrations, how merit and risk review work, the 2024 money rules and the errors that sink applications.</span></span></a></li>
<li><a href="write.html">{ico("pencil")}<span><b>We're writing one now</b><span>Each section of an application, what a reviewer is scoring, and where budgets go wrong.</span></span></a></li>
<li><a href="play.html">{ico("play")}<span><b>Test yourself</b><span>Work the screening desk, then sit on a review panel and score a mock application.</span></span></a></li>
</ul>
{h2("money", "data", "Where charitable money comes from")}
<p>Grants are a slice of a bigger picture. In 2025 Americans gave $617.20 billion to charity, the first year over $600 billion. Living individuals gave most of it. Foundations gave about one dollar in five, and companies about one in fourteen.</p>
<ul class="bars" aria-label="Charitable giving by source, 2025">
<li><span class="label">Individuals</span><span class="bar" aria-hidden="true"><span class="fill" style="width:100%"></span></span><span class="val">$394.2 billion, about 64%</span></li>
<li><span class="label">Foundations</span><span class="bar" aria-hidden="true"><span class="fill" style="width:29.7%"></span></span><span class="val">$117.15 billion, about 19%</span></li>
<li><span class="label">Bequests</span><span class="bar" aria-hidden="true"><span class="fill" style="width:15.8%"></span></span><span class="val">$62.19 billion, about 10%</span></li>
<li><span class="label">Corporations</span><span class="bar" aria-hidden="true"><span class="fill" style="width:11.1%"></span></span><span class="val">$43.67 billion, about 7%</span></li>
</ul>
<p>What that means for planning: foundation and corporate grants are real money, but an organization that lives only on grants is chasing a quarter of private giving. Grants work best alongside individual donors, earned income and government contracts.</p>
{src("gusa")}
<p class="cite">Percent shares are calculated from Giving USA's dollar figures.</p>
{h2("four", "bank", "The four kinds of grant money")}
<ul class="cards">
<li><b><a href="federal.html">Federal</a></b><span class="what">The biggest single awards and the heaviest rules: registration in SAM.gov, a published funding notice, merit review, risk review, and cost rules in 2 CFR 200.</span></li>
<li><b><a href="find.html#state">State</a></b><span class="what">Ohio posts state agency funding opportunities in one place, grants.ohio.gov. Much state money is federal money passed through, so the federal cost rules often follow it.</span></li>
<li><b><a href="foundations.html">Private and community foundations</a></b><span class="what">Each sets its own focus, geography and process. Private foundations must pay out a minimum amount every year, and their tax returns show exactly whom they funded.</span></li>
<li><b><a href="foundations.html#corporate">Corporate</a></b><span class="what">Company foundations follow the private foundation rules; company giving programs and employee matching follow the company's own.</span></li>
</ul>
<div class="cta"><a class="btn" href="play.html">{ico("play")}Play the practice round</a></div>
""")

# ===================== ready =====================
page("ready.html", "Get ready: what a funder checks before reading your proposal",
 "The organizational foundations grant funders verify: legal status, IRS standing, current 990 filings, Ohio Attorney General registration, books, board and SAM.gov registration for federal money.",
 "Get ready before you ask",
 f"""<p class="lede">The first read of your application is not your story. It's whether you exist, are in good standing and can be trusted with money.</p>
<p>Funders and federal agencies check status records that anyone can look up. Fix these first, in this order. Each one takes days to weeks, and none can be rushed the week a deadline lands.</p>
{CHK}
{jump([("legal","Legal and tax status"),("filings","Annual filings"),("ohio","Ohio registration"),("books","Books and board"),("federal","Federal-ready"),("selfcheck","Check yourself")])}
{h2("legal", "review", "Legal and tax status")}
<ul class="check">
<li><b>A legal entity.</b> In Ohio, a nonprofit corporation is formed with the Secretary of State under Ohio Revised Code chapter 1702 (or 1745 for unincorporated associations). {s("ohag","Ohio AG overview")}</li>
<li><b>An IRS determination letter.</b> Most foundations grant only to 501(c)(3) public charities, or to others with extra paperwork. Your status and whether donors can deduct gifts to you show up in the IRS Tax Exempt Organization Search, which draws on Publication 78 data and the determination letters. {s("teos","IRS search")}</li>
<li><b>No 501(c)(3) yet?</b> You can still take grant money through a fiscal sponsor. See <a href="sponsor.html">No 501(c)(3)?</a></li>
</ul>
{h2("filings", "book", "Annual filings: the quiet deal-breaker")}
<p>Every year your organization files a Form 990, 990-EZ or 990-N with the IRS. Organizations whose gross receipts are normally $50,000 or less can file the short 990-N e-Postcard; above that it's the 990-EZ or full 990.</p>
<div class="notice">{ico("no")}<div><p><strong>Miss three years in a row and your exemption is revoked automatically.</strong> The IRS publishes the list of revoked organizations, and anyone can search it.</p><p>{s("irsrev","IRS automatic revocation")} · {s("irs990n","Who files the 990-N")}</p></div></div>
<p>Your 990s are public. Anyone, including every program officer, can read years of them free on ProPublica's Nonprofit Explorer, which holds millions of filings back to 2001. Read your own the way a funder would: revenue trend, program spending, officer pay, and whether the mission on page one matches what you're asking money for. {FP}</p>
{src("irs990n","irsrev","ppx")}
{h2("ohio", "flag", "Ohio Attorney General registration")}
<p>Ohio charities, and any organization soliciting for a charitable purpose in Ohio, must register with the Ohio Attorney General, whether or not they're tax-exempt. Register within six months of forming. Annual reports are due on the 15th day of the fifth month after your fiscal year ends, matching an IRS extension if you take one. Fees run on a sliding scale shown at filing. Groups organized exclusively for religious purposes are the most common exemption.</p>
<p>Other states have their own charity registration offices; most sit in the attorney general's or secretary of state's office. If you raise money in a state, check its rule before you solicit there. {FP}</p>
{src("ohag","ohagsheet")}
{h2("books", "plan", "Books, board and outcomes")}
<p>None of these is a single legal rule; they're what a reviewer looks for when judging whether you can run the money. {FP}</p>
<ul class="check">
<li><b>A budget for the organization, not only the project.</b> A project budget with no organizational budget behind it reads as a group that hasn't planned past this grant.</li>
<li><b>Clean, separate books.</b> A dedicated bank account, a chart of accounts that can track restricted money by grant, and monthly statements someone other than the bookkeeper reads.</li>
<li><b>A working board.</b> Minutes, a conflict of interest policy (the Form 990 asks whether you have one) and members who aren't all related or all staff.</li>
<li><b>Outcome data you already collect.</b> Counts of who you served and what changed for them, kept the same way year to year. A new program can borrow evidence from published research; an existing one should have its own numbers.</li>
<li><b>Letters of support and partners lined up early.</b> They take weeks to collect and the best partners are asked by everyone.</li>
</ul>
{h2("federal", "flag", "Federal-ready, before any deadline")}
<ul class="steps">
<li><b>Register in SAM.gov</b> to get a Unique Entity ID. The UEI comes about a day after you enter your E-Business Point of Contact; full SAM processing takes 7 to 10 business days after everything is entered. It costs nothing.</li>
<li><b>Register in Grants.gov</b>, same day, and have your E-Business Point of Contact assign who can submit.</li>
<li><b>Keep SAM active.</b> Federal rules require an active, current registration the whole time an application is under consideration or an award is open, renewed at least once a year.</li>
<li><b>Get your written systems in order.</b> Federal agencies review the financial stability, management systems, performance history and audit findings of every applicant before an award.</li>
</ul>
{src("ggreg","25200","206")}
{h2("selfcheck", "search", "Check yourself the way a funder will")}
<ol>
<li>Search your name and EIN in the {s("teos","IRS Tax Exempt Organization Search")}: are you listed, and not on the revocation list?</li>
<li>Pull your last three returns on {s("ppx","Nonprofit Explorer")}: do they tell a consistent story?</li>
<li>Look yourself up in the Ohio Attorney General's charity search: is this year's annual report filed?</li>
<li>For federal money, sign in to SAM.gov: is the registration active, and when does it expire?</li>
</ol>
""")

# ===================== find =====================
page("find.html", "Find grants: federal, Ohio, foundations and companies",
 "Where grant opportunities are actually posted: Grants.gov, Ohio's grants.ohio.gov, free Candid search at libraries, and foundation tax returns that show who they fund.",
 "Where grants are, and how to qualify a funder",
 f"""<p class="lede">Every serious grant is posted somewhere official or shows up in a funder's tax return. Paid databases help, but the free sources below cover most of the field.</p>
{CHK}
{jump([("federal","Federal"),("state","Ohio and other states"),("foundations","Foundations"),("corporate","Companies"),("qualify","Qualify a funder"),("scams","Scams")])}
{h2("federal", "flag", "Federal")}
<ul class="cards">
<li><b><a href="https://www.grants.gov/">Grants.gov</a></b><span class="what">Where federal agencies post discretionary funding notices and where most applications are submitted. Searching is free and needs no account.</span></li>
<li><b><a href="https://sam.gov/">SAM.gov</a></b><span class="what">Registration home for any organization taking federal money, and the place to look up assistance listings that describe each federal program.</span></li>
<li><b><a href="https://www.usaspending.gov/">USAspending.gov</a></b><span class="what">Who actually received past awards from a program, how much and where. Use it to see whether organizations your size and type win, and to find the state agencies that pass money down.</span></li>
</ul>
<p>Federal money often reaches small organizations second-hand: a state or county wins the federal award and runs its own competition. Those subawards carry most federal cost rules with them. {FP}</p>
{h2("state", "map", "Ohio and other states")}
<p>Ohio's Office of Budget and Management runs the Ohio Grants Partnership, the central place where state agencies, boards and commissions post funding opportunities. The site is {a("https://grants.ohio.gov/","grants.ohio.gov")}.</p>
<ul class="steps">
<li><b>Search</b> under Funding Opportunities and filter by category, agency, eligible applicant, or federal program number.</li>
<li><b>Get an OH|ID.</b> Applicants need one to apply in the portal. Create it free at {a("https://ohid.ohio.gov/","ohid.ohio.gov")}.</li>
<li><b>Set up an Ohio payee ID</b> through {a("https://ohiopays.ohio.gov/","Ohio Pays")} so the state can pay you. It can take several days.</li>
<li><b>Apply</b> in the portal, or follow the opportunity's "More Information" link when the agency takes applications elsewhere. You can save a draft, and before the deadline you can unsubmit, edit and resubmit.</li>
</ul>
{src("ohgp","ohjob")}
<p class="cite">The state's job aid is dated 2023; the screens may have changed since.</p>
<h3>Any other state</h3>
<p>The same pattern works everywhere: look for a central state grants portal (often run by the budget office), then the agencies closest to your work, then the federal pass-through programs those agencies run. Check whether the state needs its own login and vendor or payee registration before you can be paid. {FP}</p>
{h2("foundations", "search", "Foundations")}
<ul class="cards">
<li><b><a href="https://candid.org/find-us">Candid search, free at libraries</a></b><span class="what">Candid, which absorbed Foundation Directory and GuideStar, is free at more than 2,180 partner locations, mostly public libraries, including saved searches, a letter of inquiry generator and lists of open requests for proposals. Candid also runs hundreds of free courses at learning.candid.org. {s("candid","Candid")}</span></li>
<li><b><a href="https://projects.propublica.org/nonprofits/">Foundation tax returns (Form 990-PF)</a></b><span class="what">Private foundations list the grants they paid on their 990-PF. Reading two or three years tells you what a foundation really funds, at what size and where, better than its website does. Free on Nonprofit Explorer. {s("ppx","ProPublica")}</span></li>
<li><b>Community foundations</b><span class="what">Most counties are served by one. They run local competitive grants, manage donor-advised funds and usually know which local family foundations fund what. Start with the one covering your county. {FP}</span></li>
</ul>
{h2("corporate", "give", "Companies")}
<p>Company foundations are private foundations and file the same 990-PF, so you can read their giving. Company giving programs run out of the business, favor places where they have employees or customers, and often start with an employee who volunteers with you. Employee matching gifts can double donations you already get. {FP}</p>
{h2("qualify", "scale", "Qualify a funder before you write a word")}
<div class="tablewrap"><table>
<caption>Five questions, in order. One "no" usually means stop.</caption>
<thead><tr><th scope="col">Question</th><th scope="col">Where the answer lives</th></tr></thead>
<tbody>
<tr><td>Do we fit their focus, in their words?</td><td>Funder guidelines; the funding notice's eligibility and responsiveness criteria</td></tr>
<tr><td>Do they fund our geography?</td><td>Guidelines; the addresses of past grantees on the 990-PF or USAspending</td></tr>
<tr><td>Do they fund organizations like us, at our size?</td><td>Past grant lists: type of grantee, typical award</td></tr>
<tr><td>Do they accept unsolicited requests?</td><td>Guidelines. "By invitation only" means no proposal; build a relationship or move on.</td></tr>
<tr><td>Is our ask in their usual range?</td><td>Median past award, not the largest one</td></tr>
</tbody></table></div>
<p class="cite">Federal funding notices must state eligibility, responsiveness criteria and how applications are reviewed: {s("appi","2 CFR 200 Appendix I")}. The rest is {FP}.</p>
{h2("scams", "no", "Spot a grant scam")}
<p>The government doesn't award grants for personal needs like bills or debt, doesn't call you about a grant you didn't apply for, doesn't award grants by drawing, and never charges a fee to apply or to receive a federal grant. Anyone asking for a "processing fee", gift cards, a wire or crypto is a scammer. Report it at {a("https://reportfraud.ftc.gov/","ReportFraud.ftc.gov")}.</p>
{src("ggscam","ftc","usagov")}
""")

# ===================== federal =====================
page("federal.html", "Federal grants: registration, review and the 2024 money rules",
 "How federal grants work in practice: SAM.gov and Grants.gov registration timelines, reading a funding notice, merit review and risk review, the 2024 Uniform Guidance thresholds, and the errors that get applications rejected.",
 "Federal grants",
 f"""<p class="lede">Federal grants run on one rulebook, the Uniform Guidance at 2 CFR 200. Learn its shape once and every agency's notice gets easier to read.</p>
{CHK}
{jump([("register","Register"),("nofo","Read the notice"),("review","How you're judged"),("money","Money rules"),("errors","Errors that sink you")])}
{h2("register", "review", "Register early")}
<div class="tablewrap"><table>
<caption>Registration timeline from Grants.gov</caption>
<thead><tr><th scope="col">Step</th><th scope="col">How long</th></tr></thead>
<tbody>
<tr><td>SAM.gov: Unique Entity ID</td><td>About one day after you enter your E-Business Point of Contact name and email</td></tr>
<tr><td>SAM.gov: full registration</td><td>7 to 10 business days after all information is entered</td></tr>
<tr><td>Grants.gov account and roles</td><td>Same day</td></tr>
</tbody></table></div>
<p>Plan for a month, not two weeks: anything that needs correcting restarts the clock. {FP} Keep the SAM registration active and current the whole time an application is pending or an award is open, and review it at least yearly.</p>
{src("ggreg","25200")}
{h2("nofo", "book", "Read the funding notice like a reviewer")}
<p>Every federal Notice of Funding Opportunity has to tell you how you'll be judged. Since the 2024 revision, notices follow a streamlined, plain-language template. Read these parts first, in this order:</p>
<ol class="steps">
<li><b>Eligibility and responsiveness criteria.</b> These are go/no-go screens. Fail one and nobody scores the rest.</li>
<li><b>Review criteria.</b> The notice must describe each criterion and sub-criterion, and give weights or points when criteria vary in importance. Your outline should mirror them.</li>
<li><b>The review and selection process.</b> It must describe merit review and how the agency uses the scores to decide, including any other factors such as geography or past performance.</li>
<li><b>Submission requirements.</b> Forms, page limits, file formats and the deadline time zone.</li>
</ol>
{src("appi","epa24")}
{h2("review", "scale", "How you're judged: two reviews")}
<h3>Merit review: is the project good?</h3>
<p>Agencies must run an objective merit review of discretionary applications against written standards, and the process must be described in the notice. Reviewers score your application against the published criteria, not against what they wish you'd proposed.</p>
{src("205")}
<h3>Risk review: can you be trusted with the money?</h3>
<p>Before an award, the agency reviews the risk you pose. It should consider five things:</p>
<ul class="check">
<li><b>Financial stability</b></li>
<li><b>Management systems and standards</b></li>
<li><b>History of performance</b> on past awards</li>
<li><b>Audit reports and findings</b></li>
<li><b>Ability to carry out the requirements</b> of the award</li>
</ul>
<p>For awards above the simplified acquisition threshold, the agency must also review your responsibility and integrity records in SAM.gov. A good score with a weak risk review can still mean no award, or an award with extra conditions.</p>
{src("206")}
{h2("money", "bank", "Money rules since October 1, 2024")}
<p>The 2024 revision of 2 CFR 200 applies to awards that start on or after October 1, 2024.</p>
<div class="tablewrap"><table>
<caption>Key thresholds, before and after</caption>
<thead><tr><th scope="col">Rule</th><th scope="col">Now</th><th scope="col">Before</th></tr></thead>
<tbody>
<tr><td>Single Audit required when federal spending in a year reaches</td><td>$1,000,000</td><td>$750,000</td></tr>
<tr><td>De minimis indirect cost rate (no negotiated rate)</td><td>Up to 15% of modified total direct costs</td><td>10%</td></tr>
<tr><td>Equipment threshold</td><td>$10,000</td><td>$5,000</td></tr>
<tr><td>Unused supplies to sell or account for at the end</td><td>Over $10,000 total</td><td>Over $5,000</td></tr>
<tr><td>Largest fixed amount subaward</td><td>$500,000</td><td>$250,000</td></tr>
</tbody></table></div>
{src("epa24","414")}
<h3>Indirect costs</h3>
<p>An organization without a negotiated indirect cost rate may charge up to 15% of modified total direct costs with no documentation to justify it, for as long as it likes. A negotiated rate must be accepted by every federal agency unless a statute or regulation requires otherwise or the agency approves an exception.</p>
{src("414")}
<h3>Allowable costs</h3>
<p>To be charged to a federal award, a cost must be necessary and reasonable for the project and allocable to it, follow the cost rules and the award's limits, be treated consistently with your other activities, not count as both direct and indirect, follow generally accepted accounting principles, not be used as cost share on another federal award, and be adequately documented.</p>
{src("403")}
<h3>Records</h3>
<p>Keep every record for three years from the date you submit the final financial report, longer if an audit, claim or lawsuit starts in that window.</p>
{src("334")}
{h2("errors", "no", "Errors that sink applications before review")}
<ul class="cards">
<li><b>Attachment file names</b><span class="what">Grants.gov says to use only letters, numbers and a short list of symbols (underscore, hyphen, space, period, parentheses, braces, brackets, ampersand, tilde, exclamation point, comma, semicolon, apostrophe, at sign, number sign, dollar, percent, plus, equals) and to keep names to 50 characters or fewer. Breaking the rule can get the whole application rejected. Safest habit: short names with underscores, like Budget_Narrative.pdf.</span></li>
<li><b>Roles not assigned</b><span class="what">If the person submitting hasn't been given the right role by your E-Business Point of Contact, Grants.gov refuses the submission. Test it days before the deadline.</span></li>
<li><b>An expired SAM registration</b><span class="what">Registration must be active while the application is under consideration. Check the expiration date before you start writing.</span></li>
<li><b>Submitting on the last day</b><span class="what">Validation errors show up after you press submit. Leave days to fix them. {FP}</span></li>
</ul>
{src("ggerr","25200")}
""")

# ===================== foundations =====================
page("foundations.html", "Foundation and corporate grants: how they decide",
 "How private, family, community and corporate foundations decide what to fund: the 5% payout rule, reading a 990-PF, letters of inquiry, relationships, and general operating versus project support.",
 "Foundations and companies",
 f"""<p class="lede">A foundation is a small team with its own priorities and a legal duty to give money away. Your job is to show you're the best way to do what it already wants done.</p>
{CHK}
{jump([("payout","The payout rule"),("read","Read their return"),("approach","How to approach"),("support","What kind of money"),("corporate","Companies")])}
{h2("payout", "bank", "Private foundations have to give")}
<p>A private foundation must pay out a minimum distributable amount each year, built from a minimum investment return of 5% of its non-charitable-use assets, or pay a 30% excise tax on what it failed to distribute. That money can include its own programs and administrative costs, and it chooses the recipients. So "they have to give" is true; "they have to give to you" is not.</p>
{src("mir","pfpay")}
{h2("read", "search", "Read their tax return before their website")}
<p>Pull the last three 990-PF returns free on {s("ppx","Nonprofit Explorer")} and look at the list of grants paid. Write down {FP}:</p>
<ul class="check">
<li><b>Who:</b> what kinds of organizations, and are any like yours?</li>
<li><b>Where:</b> the cities and counties of grantees.</li>
<li><b>How much:</b> the typical grant, not the biggest one.</li>
<li><b>How often:</b> the same names every year means a closed circle; new names every year means an open door.</li>
<li><b>Assets:</b> roughly 5% of them is the floor on what they'll pay out.</li>
</ul>
{h2("approach", "chat", "How to approach")}
<ul class="steps">
<li><b>Follow their process exactly.</b> If the guidelines say letter of inquiry first, send a letter of inquiry. If they say by invitation only, don't send a proposal.</li>
<li><b>Call or email the program officer</b> with one specific question the guidelines don't answer. It's how relationships start. {FP}</li>
<li><b>Write a letter of inquiry</b> of one to two pages: who you are, the problem in numbers, what you'll do, what will change, how much you need and what else funds it. Candid's free search at libraries includes a letter of inquiry generator. {s("candid","Candid")}</li>
<li><b>Report on time, every time.</b> Your next grant from the same funder depends more on the last report than on the next proposal. {FP}</li>
</ul>
{h2("support", "plan", "Project money or operating money")}
<p>Project grants pay for a defined program and must be tracked separately. General operating support pays for the organization as a whole and is the most valuable kind because it covers what projects don't: rent, finance, leadership. Ask for operating support where a funder offers it, and price projects with their real share of overhead where it doesn't. {FP}</p>
{h2("corporate", "give", "Companies")}
<p>A company foundation is a private foundation under the same payout rule, and its 990-PF is public. Giving straight from the company is a business decision: it follows where the company has employees, customers and a story to tell. Lead with the overlap, offer employee volunteer days and recognition the company can use, and ask whether it matches employee gifts. {FP}</p>
""")

# ===================== write =====================
page("write.html", "Write the application: what each section is scored on",
 "Section by section, what grant reviewers score: need, approach, outcomes and evaluation, capacity, budget and justification, and sustainability, tied to published federal review rules.",
 "Write it the way it will be scored",
 f"""<p class="lede">Reviewers score against a list. Give them the list back, in the funder's order and words, with evidence on every line.</p>
<p>Federal notices must publish their review criteria, with weights when criteria differ in importance ({s("appi","2 CFR 200 Appendix I")}). Foundations usually publish what they look for in guidelines. The section guidance below is {FP} from how review panels work; the budget rules cite the regulation.</p>
{CHK}
{jump([("before","Before you write"),("need","Need"),("approach","Approach"),("outcomes","Outcomes"),("capacity","Capacity"),("budget","Budget"),("sustain","Sustainability"),("final","Final pass")])}
{h2("before", "review", "Before you write: the go/no-go read")}
<ul class="check">
<li><b>Eligible?</b> Entity type, location, size, registrations.</li>
<li><b>Responsive?</b> Does the project do what this notice is for, not something adjacent?</li>
<li><b>Can you meet every requirement?</b> Cost share, data collection, partners, reporting.</li>
<li><b>Outline from the criteria.</b> One heading per criterion, in their order, using their words.</li>
</ul>
{h2("need", "data", "Need")}
<p>Show the problem in numbers for the place you serve, from a named public source, and compare it to the state or national rate. Then show the gap: who is already working on it and why that isn't enough. Avoid the need of your organization ("we need a van"); describe the need of the people ("62 residents can't reach appointments"). Every number gets a source and a year.</p>
{h2("approach", "plan", "Approach")}
<p>Say exactly what you'll do, for whom, how often, by whom and on what timeline. Tie it to evidence that it works: research, a model others have tested, or your own results. A logic model (inputs, activities, outputs, outcomes) on one page helps a reviewer see that the pieces connect.</p>
{h2("outcomes", "yes", "Outcomes and evaluation")}
<p>Outputs are what you do (120 visits). Outcomes are what changes (80% of residents keep their housing a year later). Give each outcome a target, a baseline, how you'll measure it, when, and who collects the data. Keep them few and measurable; reviewers distrust ten soft outcomes more than three firm ones.</p>
{h2("capacity", "vhg", "Organizational capacity")}
<p>Name the people who will run it and what they've run before. Show your financial controls and past grants managed. This section speaks directly to the federal risk review of financial stability, management systems, performance history and audit findings ({s("206","2 CFR 200.206")}).</p>
{h2("budget", "bank", "Budget and justification")}
<p>The budget is where reviewers check whether the narrative is real. Every person, activity and purchase in the narrative needs a line, and every line needs a sentence explaining it.</p>
<ul class="check">
<li><b>Match the narrative.</b> Two staff in the text means two salaries in the budget.</li>
<li><b>Allowable and reasonable.</b> Federal costs must be necessary, reasonable, allocable and documented ({s("403","2 CFR 200.403")}).</li>
<li><b>Indirect costs.</b> Without a negotiated rate you may use up to 15% of modified total direct costs on federal awards ({s("414","2 CFR 200.414")}). Foundations set their own caps; ask.</li>
<li><b>Equipment.</b> Items of $10,000 or more per unit are equipment under the 2024 federal rules, with their own tracking duties ({s("epa24","EPA summary")}).</li>
<li><b>Show the whole picture.</b> Other funding, in-kind support and what this grant covers.</li>
</ul>
{h2("sustain", "share", "Sustainability")}
<p>Say what happens when the grant ends: which costs end, which shift to other funders or earned income, and which partners take on what. "We will seek additional grants" is not a plan.</p>
{h2("final", "pencil", "Final pass")}
<ol>
<li>Score your own draft against every criterion, out loud, with a colleague who hasn't read it.</li>
<li>Check every number against its source and every budget line against the text.</li>
<li>Check page limits, fonts, file names and required forms.</li>
<li>Submit days early.</li>
</ol>
<p>A grant writer can help with all of this. Pay them a flat or hourly fee: professional ethics codes bar working for a percentage of the grant ({s("afp","AFP Standard 21")}; {s("sfe","Standards for Excellence")}).</p>
<div class="cta"><a class="btn" href="play.html#panel">{ico("play")}Score a mock application</a></div>
""")

# ===================== sponsor =====================
page("sponsor.html", "No 501(c)(3)? How fiscal sponsorship works",
 "How a group without its own 501(c)(3) can receive grants through a fiscal sponsor: the comprehensive (Model A) and pre-approved grant (Model C) setups, who controls the money, and what to check before signing.",
 "No 501(c)(3)? Use a fiscal sponsor",
 f"""<p class="lede">A fiscal sponsor is an existing nonprofit that takes in money for your project, so you can start work before, or instead of, forming your own charity.</p>
{CHK}
{h2("what", "give", "What fiscal sponsorship is")}
<p>Fiscal sponsorship isn't defined in law. It describes a relationship between a tax-exempt nonprofit, the sponsor, and a project founder who wants to carry out charitable work. Two setups are common.</p>
<div class="tablewrap"><table>
<caption>The two common models</caption>
<thead><tr><th scope="col"></th><th scope="col">Comprehensive (Model A)</th><th scope="col">Pre-approved grant (Model C)</th></tr></thead>
<tbody>
<tr><th scope="row">What the project is</th><td>A program inside the sponsor, no different to a regulator from the sponsor's own projects</td><td>A separate grantee of the sponsor</td></tr>
<tr><th scope="row">Who is in charge</th><td>Day-to-day management delegated to the project's director and committee, under the ultimate authority of the sponsor's board</td><td>The project runs itself; the sponsor is the grantmaker, after advance due diligence</td></tr>
<tr><th scope="row">Who employs staff</th><td>Usually the sponsor {FP}</td><td>The project's own entity {FP}</td></tr>
<tr><th scope="row">Who the funder pays</th><td>The sponsor</td><td>The sponsor, which re-grants to the project</td></tr>
</tbody></table></div>
{src("fs")}
{h2("check", "review", "What to check before you sign")}
<p>{FP}</p>
<ul class="check">
<li><b>A written agreement</b> that names the model, the fee, who owns what the project creates, and how you leave, including taking your money and work with you to your own 501(c)(3).</li>
<li><b>The fee</b> and what it buys: accounting, payroll, insurance, grant reporting.</li>
<li><b>How fast you get paid</b> and who approves spending.</li>
<li><b>Mission fit.</b> The sponsor must be able to say your project furthers its own charitable purpose.</li>
<li><b>Funder acceptance.</b> Ask each funder whether it accepts sponsored projects before you apply. Government funders often require the sponsor to apply as the lead.</li>
</ul>
<p class="cite">Fee ranges vary widely and no public dataset this guide could verify sets a standard; ask several sponsors.</p>
{h2("ohio", "flag", "In Ohio")}
<p>A sponsored project solicits under its sponsor's registration with the Ohio Attorney General; a project that forms its own charity must register within six months. {s("ohagsheet","Ohio AG")}</p>
""")

# ===================== myths =====================
def myth(q, verdict, body, srcs):
    v = {"false": ("v-false", "no", "Myth"), "true": ("v-true", "yes", "True"), "half": ("v-half", "myth", "Partly true")}[verdict]
    return f'<article class="myth"><h3>{q}</h3><span class="verdict {v[0]}">{ico(v[1])}{v[2]}</span>{body}{srcs}</article>'

M = [
 myth("“The government gives free grant money to individuals for bills, debt or a new business.”", "false",
  "<p>Government grants aren't awarded for personal needs. They fund specific programs, research and projects. Offers of personal \"free money\" from the government are scams. Individuals may qualify for benefits or loans, which are different things.</p>", src("usagov","ftc","ggscam")),
 myth("“You pay a fee to apply for or receive a federal grant.”", "false",
  "<p>The government charges no fee to apply for a federal grant, and agencies won't demand payment to give you one. A fee request is the clearest sign of a scam.</p>", src("ggscam","ftc")),
 myth("“A good grant writer works for a percentage of the award.”", "false",
  "<p>Professional codes bar it. The Association of Fundraising Professionals' Standard 21 says members shall not accept compensation based on a percentage of contributions, or finder's or contingent fees. Standards for Excellence says the same. Pay a flat or hourly fee.</p>", src("afp","sfe")),
 myth("“Grants can't pay for overhead.”", "false",
  "<p>On federal awards, an organization without a negotiated rate may charge up to 15% of modified total direct costs with no justification, and negotiated rates must be accepted by all agencies. Foundations set their own limits, and many offer general operating support.</p>", src("414","epa24")),
 myth("“Once you have your 501(c)(3), you're set.”", "false",
  "<p>Fail to file your annual 990, 990-EZ or 990-N for three years in a row and the exemption is revoked automatically. Ohio charities also file an annual report with the Attorney General.</p>", src("irsrev","ohag")),
 myth("“Foundations are where the big charitable money is.”", "false",
  "<p>In 2025, individuals gave $394.2 billion, about 64% of all giving. Foundations gave $117.15 billion, about 19%, and corporations $43.67 billion, about 7%. Grants matter, but individual donors are most of the money.</p>", src("gusa")),
 myth("“Federal grants go to whoever knows somebody.”", "false",
  "<p>Agencies must run an objective merit review against written standards described in the notice, and the notice must publish its criteria. What does favor established groups is the separate risk review, which weighs financial stability, management systems and performance history.</p>", src("205","206","appi")),
 myth("“New organizations can't win federal grants.”", "half",
  "<p>No rule bars them. But the risk review looks at history of performance, financial stability and audits, which a new organization can't show yet. Building a record with local and state grants first is the usual path.</p>", src("206")),
 myth("“Foundations have to give money away, so some of it can come to us.”", "half",
  "<p>Private foundations must pay out a minimum distributable amount, based on 5% of their non-charitable-use assets, or face a 30% tax. They decide who gets it, and their own programs and costs can count.</p>", src("mir","pfpay")),
 myth("“Grant money is free money with no strings.”", "false",
  "<p>Federal costs must be allowable and documented, records kept three years after the final report, and organizations spending $1,000,000 or more in federal money in a year need a Single Audit. Foundation grants come with their own reports.</p>", src("403","334","epa24")),
 myth("“Without a 501(c)(3), you can't get grants.”", "half",
  "<p>Many funders require one, but a fiscal sponsor that is a 501(c)(3) can receive grants for your project, either as its own program or as a re-grant to you.</p>", src("fs")),
 myth("“Send the same proposal to as many funders as you can.”", "false",
  f"<p>Funders score fit to their own criteria and priorities, and federal notices publish responsiveness screens that end the review on a mismatch. A tailored proposal to five well-qualified funders beats a generic one to fifty. {FP}</p>", src("appi")),
]
page("myths.html", "Grant myths versus reality",
 "Twelve common grant funding myths checked against federal rules, IRS rules, ethics codes and Giving USA data: free government money, percentage-paid grant writers, overhead, new organizations and more.",
 "Myths versus reality",
 f"""<p class="lede">Twelve things people repeat about grants, checked against the rules and the data.</p>
{CHK}
""" + "\n".join(M) + f"""
<div class="cta"><a class="btn" href="play.html">{ico("play")}Test yourself in the practice round</a></div>
""")

# ===================== play =====================
page("play.html", "Practice round: the grant screening desk and review panel",
 "A free grant-writing practice game: decide which applications are ready, which need fixing and which to walk away from, then sit on a review panel and pick the strongest answer for each scored criterion.",
 "Practice round",
 f"""<p class="lede">Two rounds. First, work the screening desk. Then sit on a review panel. Every answer explains why, with the rule behind it.</p>
<p>Your score stays in your browser; nothing is sent anywhere. The scenarios and the mock funding notice are made up for practice; the rules in the explanations are real.</p>
<section aria-labelledby="desk-h">
<h2 id="desk-h">{ico("review")}Round 1: the screening desk</h2>
<p>Each case lands on your desk. Is it <b>ready to submit</b>, does it need a <b>fix first</b>, or should they <b>walk away</b>?</p>
<div id="desk" class="game" aria-live="polite"><p>Loading the game. If nothing appears, your browser may be blocking scripts.</p></div>
</section>
<section aria-labelledby="panel-h">
<h2 id="panel">{ico("scale")}<span id="panel-h">Round 2: the review panel</span></h2>
<p>You're reviewing the <b>Community Readiness Fund</b>, a mock state grant for veteran-serving groups. Here are its published criteria:</p>
<ul class="criteria">
<li><b>Need</b>, 20 points</li>
<li><b>Approach</b>, 25 points</li>
<li><b>Outcomes and evaluation</b>, 20 points</li>
<li><b>Organizational capacity</b>, 15 points</li>
<li><b>Budget and justification</b>, 20 points</li>
</ul>
<p>For each criterion, three applicants wrote a passage. Pick the one that would score highest.</p>
<div id="panelgame" class="game" aria-live="polite"><p>Loading the game.</p></div>
</section>
""", script='<script src="assets/game.js" defer></script>\n')

# ===================== sources =====================
rows = "".join(f'<li>{a(u, t)}</li>' for t, u in S.values())
page("sources.html", "Sources, method and gaps",
 "Every source behind Grants for Real, how the guide was planned, and the gaps still open.",
 "Sources, method and gaps",
 f"""<p class="lede">Every rule and number on this site links to where it came from. Here is the full list, how the guide was planned, and what it doesn't cover yet.</p>
{h2("list", "book", "Sources read for this guide")}
<p>Each was read on or about {CHECKED}.</p>
<ul class="cards" style="font-size:1rem">{rows}</ul>
{h2("tags", "myth", "What the Field practice tag means")}
<p>{FP} marks guidance drawn from how grantmakers and reviewers commonly work, not from a regulation, a funder's published rule or a dataset. It's labeled so you can weigh it accordingly.</p>
{h2("method", "plan", "How the guide was planned")}
<p>It was built as an operational plan:</p>
<ul class="check">
<li><b>The problem.</b> Small and new organizations lose grants on things that have nothing to do with the quality of their work: status problems, registration delays, misread criteria, budgets that don't match, and advice that's opinion passed off as rule.</li>
<li><b>Information needed.</b> What funders check, what reviewers score, the money rules, where opportunities are posted, who actually gives, and how groups without a 501(c)(3) can take part.</li>
<li><b>Where it lives.</b> Federal regulation (2 CFR 200 and 25), Grants.gov and SAM.gov, IRS rules and data, the Ohio Office of Budget and Management and Attorney General, Giving USA, Candid, foundation tax returns, and professional ethics codes.</li>
<li><b>Gaps.</b> Listed below.</li>
</ul>
{h2("gaps", "search", "Known gaps")}
<ul>
<li>State pages beyond Ohio. The pattern on <a href="find.html#state">Find grants</a> applies; state-by-state pages are next.</li>
<li>Published success rates by federal program and foundation. Few funders publish them; where an agency does, it will be added.</li>
<li>Fiscal sponsor fee data from a verifiable survey.</li>
<li>A list of Ohio community foundations by county.</li>
</ul>
""")
print("built", len(NAV), "pages into", os.path.abspath(ROOT))

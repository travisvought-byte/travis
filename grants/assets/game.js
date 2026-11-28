/* Grants for Real practice round. No tracking, no network calls; best scores stay in this browser. */
(function () {
  "use strict";
  var ICON = function (n) { return '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><use href="assets/icons.svg#' + n + '"/></svg>'; };
  function esc(t) { var d = document.createElement("div"); d.textContent = t; return d.innerHTML; }
  function store(k, v) { try { if (v === undefined) return localStorage.getItem(k); localStorage.setItem(k, v); } catch (e) { return null; } }

  var CHOICES = [
    { id: "ready", label: "Ready to submit", icon: "yes" },
    { id: "fix", label: "Fix first", icon: "pencil" },
    { id: "walk", label: "Walk away", icon: "no" }
  ];

  var DESK = [
    { s: "A veterans' group finishes a federal application two weeks early. Its SAM.gov registration expired last month; everything else is in order.",
      a: "fix", why: "Federal rules require an active, current SAM.gov registration the whole time an application is under consideration. Renewing takes time, so it's fixable if they start now.",
      src: ["2 CFR 25.200", "https://www.law.cornell.edu/cfr/text/2/25.200"] },
    { s: "The budget narrative is attached as “Budget Narrative – FINAL (v3) revised for Program Officer review.pdf”.",
      a: "fix", why: "Grants.gov limits file names to 50 characters from a short list of allowed characters, and a bad name can get the whole application rejected. This one is too long and uses a dash character outside the list. Rename it Budget_Narrative.pdf.",
      src: ["Grants.gov error messages", "https://www.grants.gov/applicants/encountering-error-messages"] },
    { s: "A food pantry with about $30,000 a year in receipts hasn't filed anything with the IRS for three years. It wants to apply to a community foundation that funds only 501(c)(3) charities.",
      a: "fix", why: "Three straight years without a 990, 990-EZ or 990-N means automatic revocation of exemption, and the IRS publishes the list. They need to apply for reinstatement and get current before a 501(c)(3)-only funder can fund them.",
      src: ["IRS automatic revocation", "https://www.irs.gov/charities-non-profits/automatic-revocation-of-exemption-for-nonfiling-overview"] },
    { s: "A small arts group without its own 501(c)(3) applies to a family foundation through a fiscal sponsor that has agreed in writing to take the grant. The foundation's guidelines say it accepts sponsored projects.",
      a: "ready", why: "A 501(c)(3) fiscal sponsor can receive the grant for the project, and the funder has said it accepts sponsored projects. That's exactly how it's meant to work.",
      src: ["Nonprofit Law Blog on fiscal sponsorship", "https://nonprofitlawblog.com/do-you-really-know-what-fiscal-sponsorship-is/"] },
    { s: "A foundation's website says, “We do not accept unsolicited proposals.” A nonprofit plans to mail its full proposal anyway, “to get on their radar.”",
      a: "walk", why: "The funder's own rule is the rule. An unsolicited proposal won't be read. Walk away from the proposal, and if the fit is strong, work on a relationship instead: events, a short email to the program officer, other funders who know them.",
      src: ["The funder's published guidelines", "find.html#qualify"] },
    { s: "A nonprofit with no negotiated indirect rate builds its federal budget with indirect costs at 15% of modified total direct costs, and doesn't attach any justification for the rate.",
      a: "ready", why: "Since the 2024 revision, an organization without a negotiated rate may charge up to 15% of modified total direct costs, with no documentation needed to justify it.",
      src: ["2 CFR 200.414", "https://www.law.cornell.edu/cfr/text/2/200.414"] },
    { s: "An organization wants to apply for an Ohio state grant posted on grants.ohio.gov. Nobody on staff has an OH|ID yet; the deadline is in three weeks.",
      a: "fix", why: "Applicants need an OH|ID to apply in the state portal, and an Ohio Pays payee ID to be paid, which can take several days. Both are free. Set them up now.",
      src: ["Ohio OBM job aid", "https://archives.obm.ohio.gov/Files/Grants/Job_Aid/searching_and_applying_for_funding_opportunities.pdf"] },
    { s: "A consultant offers to write the proposal for nothing up front, in exchange for 10% of the grant if it's awarded.",
      a: "fix", why: "Professional ethics codes bar percentage and contingent fees for fundraising and grant writing, and many funders won't pay them. Hire on a flat or hourly fee instead.",
      src: ["AFP Standard 21", "https://afpglobal.org/ethical-standard-deep-dive-standard-21"] },
    { s: "The narrative describes two part-time coordinators. The budget spreadsheet shows salaries for three.",
      a: "fix", why: "Reviewers read the budget against the narrative, and federal costs must be necessary, reasonable, allocable to the project and documented. A mismatch reads as either padding or a plan that wasn't thought through.",
      src: ["2 CFR 200.403", "https://www.law.cornell.edu/cfr/text/2/200.403"] },
    { s: "A text message says your organization was selected for a $15,000 federal grant. Pay a $250 processing fee by gift card to release it.",
      a: "walk", why: "The government doesn't charge fees to apply for or receive grants, doesn't contact you about grants you didn't apply for, and never asks for gift cards. It's a scam. Report it at ReportFraud.ftc.gov.",
      src: ["Grants.gov on scams", "https://www.grants.gov/learn-grants/grant-fraud/grant-related-scams.html"] },
    { s: "A veteran housing group in rural Ohio finds a foundation whose 990-PF shows every grant for the past three years went to arts organizations in Cleveland.",
      a: "walk", why: "The return shows what a foundation really funds. No grants outside its field or city in three years means the fit isn't there, however good the project is. Spend the time on a funder that matches.",
      src: ["ProPublica Nonprofit Explorer", "https://projects.propublica.org/nonprofits/"] },
    { s: "A nonprofit expects to spend $1.1 million in federal award money this year and has not budgeted for a Single Audit.",
      a: "fix", why: "Under the 2024 rules, a Single Audit is required once federal spending in a year reaches $1,000,000. Budget for it and line up an auditor now.",
      src: ["EPA summary of the 2024 revision", "https://www.epa.gov/grants/whats-new-uniform-grants-guidance-2024-revision-2-cfr-200"] }
  ];

  var PANEL = [
    { c: "Need (20 points)", opts: [
      "Our community has many veterans who struggle, and the need has never been greater. Everyone knows veterans deserve more support.",
      "Elm County has 2,100 veterans (American Community Survey 5-year estimate). In our 2026 intake survey, 41 of 96 veterans said they had missed a VA appointment for lack of a ride. The nearest VA clinic is 34 miles away and no public transit runs there.",
      "We need a new van. Our current van has 190,000 miles and broke down twice last year, and our organization can't afford a replacement."],
      best: 1, why: "Option B puts the problem in numbers for a defined place, names its sources and years, and describes the need of the people served. Option A is feeling without evidence. Option C is the organization's need, not the community's." },
    { c: "Approach (25 points)", opts: [
      "We will run two scheduled ride routes each weekday to the VA clinic, booked by phone 48 hours ahead, driven by four trained veteran volunteers with background checks, starting in month two. The model follows a rural volunteer driver program evaluated in a published study, adapted for our county.",
      "We will provide transportation and other wraparound services to veterans in need, using a holistic, person-centered approach tailored to each individual.",
      "We will purchase a van in month one and then figure out the best way to use it based on what veterans tell us."],
      best: 0, why: "Option A says exactly what, for whom, how often, by whom and when, and ties it to evidence that the model works. B is buzzwords with no activities. C admits the plan doesn't exist yet." },
    { c: "Outcomes and evaluation (20 points)", opts: [
      "Veterans will feel more supported and their quality of life will improve. We will know we're successful when we see the difference in their lives.",
      "We will provide 1,200 rides in year one.",
      "Outcome: 85% of riders keep all scheduled VA appointments over six months (baseline: 57% from our intake survey). Measured monthly from ride logs matched against appointment cards, collected by the program coordinator and reviewed by the board quarterly."],
      best: 2, why: "Option C has a target, a baseline, a method, a schedule and a person responsible. B is an output, a count of activity, not a change in people's lives. A can't be measured." },
    { c: "Organizational capacity (15 points)", opts: [
      "We are passionate and dedicated, and our founder has always cared deeply about veterans.",
      "Our coordinator ran a 30-driver volunteer program for six years. We have managed four grants since 2022 with every report filed on time, keep restricted funds in separate accounts, and our books are reviewed monthly by a board treasurer who is a CPA.",
      "We are a new organization, so we don't have much history, but we will hire experienced people once we are funded."],
      best: 1, why: "Option B answers what a risk reviewer is told to weigh: management systems, financial controls and history of performance on past awards. A is sincere but not evidence. C invites the reviewer to score capacity low." },
    { c: "Budget and justification (20 points)", opts: [
      "Total request: $60,000 for program costs. Details available on request.",
      "Coordinator, 0.5 FTE at $22/hour × 1,040 hours = $22,880 (matches the narrative). Mileage for volunteer drivers, 18,000 miles × $0.70 = $12,600. Background checks, 4 × $45 = $180. Indirect at 15% of modified total direct costs, no negotiated rate. Van insurance is paid by our county partner as in-kind support.",
      "Coordinator salary $40,000; three drivers $45,000; van $55,000; marketing $15,000; miscellaneous $10,000."],
      best: 1, why: "Option B ties every line to the narrative, shows the math, uses a 15% de minimis indirect rate the way the federal rules allow, and shows other support. C doesn't match the narrative (three paid drivers versus volunteers) and has a 'miscellaneous' line reviewers distrust. A gives the reviewer nothing to score." }
  ];

  /* ---------- screening desk ---------- */
  var desk = document.getElementById("desk");
  var d = { i: 0, score: 0, answered: false };
  function deskRender() {
    if (d.i >= DESK.length) return deskDone();
    var c = DESK[d.i];
    var h = '<div class="meta"><span>Case ' + (d.i + 1) + " of " + DESK.length + "</span><span>Score: " + d.score + "</span></div>";
    h += '<p class="scen" id="desk-scen">' + esc(c.s) + "</p>";
    h += '<ul class="choices">' + CHOICES.map(function (ch) {
      return '<li><button type="button" class="btn ghost" data-choice="' + ch.id + '">' + ICON(ch.icon) + ch.label + "</button></li>";
    }).join("") + "</ul>";
    h += '<div id="desk-fb"></div>';
    desk.innerHTML = h;
    d.answered = false;
    desk.querySelectorAll("[data-choice]").forEach(function (b) { b.addEventListener("click", deskAnswer); });
  }
  function deskAnswer(e) {
    if (d.answered) return;
    d.answered = true;
    var pick = e.currentTarget.getAttribute("data-choice"), c = DESK[d.i], ok = pick === c.a;
    if (ok) d.score++;
    desk.querySelectorAll("[data-choice]").forEach(function (b) {
      var id = b.getAttribute("data-choice");
      b.disabled = true;
      if (id === c.a) b.classList.add("right");
      else if (id === pick) b.classList.add("wrong");
      if (id === pick) b.setAttribute("aria-pressed", "true");
    });
    var right = CHOICES.filter(function (x) { return x.id === c.a; })[0].label;
    var link = c.src[1].indexOf("http") === 0 ? '<a href="' + c.src[1] + '">' + esc(c.src[0]) + "</a>" : '<a href="' + c.src[1] + '">' + esc(c.src[0]) + "</a>";
    var fb = document.getElementById("desk-fb");
    fb.innerHTML = '<div class="feedback ' + (ok ? "ok" : "no") + '" tabindex="-1" id="desk-fbbox"><p><strong>' + (ok ? "Correct" : "Not quite") + ": " + right + ".</strong></p><p>" + esc(c.why) + '</p><p class="cite">Rule: ' + link + '.</p></div><button type="button" class="btn" id="desk-next">' + (d.i + 1 < DESK.length ? "Next case" : "See your score") + "</button>";
    document.getElementById("desk-fbbox").focus();
    document.getElementById("desk-next").addEventListener("click", function () { d.i++; deskRender(); var b = desk.querySelector("button"); if (b) b.focus(); });
  }
  function deskDone() {
    var best = Math.max(d.score, parseInt(store("gfr-desk") || "0", 10));
    store("gfr-desk", String(best));
    var title = d.score >= 11 ? "Program officer material" : d.score >= 8 ? "Ready for a real deadline" : d.score >= 5 ? "Getting there" : "Start with Get ready";
    desk.innerHTML = '<p class="score" tabindex="-1" id="desk-final">' + d.score + " of " + DESK.length + "</p><p><b>" + title + ".</b> Your best here: " + best + ' of ' + DESK.length + '.</p><p>Brush up on <a href="ready.html">Get ready</a> and <a href="federal.html">Federal</a>, or go on to the review panel below.</p><button type="button" class="btn ghost" id="desk-again">Play again</button>';
    document.getElementById("desk-final").focus();
    document.getElementById("desk-again").addEventListener("click", function () { d = { i: 0, score: 0, answered: false }; deskRender(); desk.querySelector("button").focus(); });
  }

  /* ---------- review panel ---------- */
  var panel = document.getElementById("panelgame");
  var POINTS = [20, 25, 20, 15, 20];
  var p = { i: 0, score: 0, answered: false };
  var LETTERS = ["A", "B", "C"];
  function panelRender() {
    if (p.i >= PANEL.length) return panelDone();
    var c = PANEL[p.i];
    var h = '<div class="meta"><span>Criterion ' + (p.i + 1) + " of " + PANEL.length + "</span><span>Points so far: " + p.score + " of 100</span></div>";
    h += '<h3 id="panel-crit" tabindex="-1">' + esc(c.c) + "</h3><p>Which passage scores highest?</p>";
    h += '<ul class="choices stack">' + c.opts.map(function (o, k) {
      return '<li><button type="button" class="btn" data-opt="' + k + '"><span><b>Applicant ' + LETTERS[k] + ":</b> " + esc(o) + "</span></button></li>";
    }).join("") + "</ul><div id=\"panel-fb\"></div>";
    panel.innerHTML = h;
    p.answered = false;
    panel.querySelectorAll("[data-opt]").forEach(function (b) { b.addEventListener("click", panelAnswer); });
  }
  function panelAnswer(e) {
    if (p.answered) return;
    p.answered = true;
    var pick = parseInt(e.currentTarget.getAttribute("data-opt"), 10), c = PANEL[p.i], ok = pick === c.best;
    if (ok) p.score += POINTS[p.i];
    panel.querySelectorAll("[data-opt]").forEach(function (b) {
      var k = parseInt(b.getAttribute("data-opt"), 10);
      b.disabled = true;
      if (k === c.best) b.classList.add("right"); else if (k === pick) b.classList.add("wrong");
      if (k === pick) b.setAttribute("aria-pressed", "true");
    });
    var fb = document.getElementById("panel-fb");
    fb.innerHTML = '<div class="feedback ' + (ok ? "ok" : "no") + '" tabindex="-1" id="panel-fbbox"><p><strong>' + (ok ? "Panel agrees" : "The panel picked Applicant " + LETTERS[c.best]) + ".</strong> " + (ok ? "+" + POINTS[p.i] + " points." : "") + "</p><p>" + esc(c.why) + '</p></div><button type="button" class="btn" id="panel-next">' + (p.i + 1 < PANEL.length ? "Next criterion" : "See the panel's score") + "</button>";
    document.getElementById("panel-fbbox").focus();
    document.getElementById("panel-next").addEventListener("click", function () { p.i++; panelRender(); var t = document.getElementById("panel-crit"); if (t) t.focus(); });
  }
  function panelDone() {
    var best = Math.max(p.score, parseInt(store("gfr-panel") || "0", 10));
    store("gfr-panel", String(best));
    var verdict = p.score >= 80 ? "Funded. You read applications the way a panel does." : p.score >= 60 ? "In the gray zone. Close, but panels fund from the top down." : "Not funded this round. Review Write it and try again.";
    panel.innerHTML = '<p class="score" tabindex="-1" id="panel-final">' + p.score + ' of 100</p><p><b>' + verdict + "</b> Your best here: " + best + ' of 100.</p><p>See <a href="write.html">Write it</a> for what each section is scored on.</p><button type="button" class="btn ghost" id="panel-again">Review again</button>';
    document.getElementById("panel-final").focus();
    document.getElementById("panel-again").addEventListener("click", function () { p = { i: 0, score: 0, answered: false }; panelRender(); var t = document.getElementById("panel-crit"); if (t) t.focus(); });
  }

  if (desk) deskRender();
  if (panel) panelRender();
})();

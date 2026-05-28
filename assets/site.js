/* ============================================================
   Shared site chrome — navbar + footer
   Injected on every page. EDIT LINKS HERE ONCE -> all pages update.
   See README.md ("assets/site.js") for full editing instructions.
   ============================================================ */

const SITE = {
  brandTop:  "FinTech & Digital Assets",
  brandSub:  "Research Cluster",
  email:     "fintech.cluster@lincoln.ac.nz",
  scholar:   "https://scholar.google.com",
  journalUrl:"https://journals.lincoln.ac.nz/index.php/JFDA",
  journalLinkedIn:"https://www.linkedin.com/company/the-journal-of-fintech-and-digital-assets/",

  // ── ANALYTICS (GoatCounter) ──────────────────────────────
  // 1. Sign up free at https://www.goatcounter.com/ and pick a code (subdomain).
  // 2. Put that code here. Leave "" to DISABLE all visitor tracking.
  //    Example: if your dashboard is https://fintech-cluster.goatcounter.com
  //    then goatcounterCode = "fintech-cluster".
  goatcounterCode: "",   // <-- e.g. "fintech-cluster"
  // 3. In GoatCounter: Settings → "Allow public access to the dashboard"
  //    so the Analytics page can embed your live stats.

  // Navigation tabs — order shown left to right.
  nav: [
    { label: "Home",        href: "index.html" },
    { label: "About",       href: "about.html" },
    { label: "Journal",     href: "journal.html" },
    { label: "Indices",     href: "indices.html" },
    { label: "Publications",href: "publications.html" },
    { label: "Research",    href: "research.html" },
    { label: "Seminars",    href: "seminars.html" },
    { label: "News",        href: "news.html" },
    { label: "Analytics",   href: "analytics.html" },
  ],
};

// Load the GoatCounter tracker on every page (only if a code is set,
// and never on localhost so your own testing isn't counted).
function loadAnalytics(){
  if(!SITE.goatcounterCode) return;
  const isLocal = ["localhost","127.0.0.1",""].includes(location.hostname);
  if(isLocal) return;
  window.goatcounter = { no_onload: false };
  const s = document.createElement("script");
  s.async = true;
  s.setAttribute("data-goatcounter",
    `https://${SITE.goatcounterCode}.goatcounter.com/count`);
  s.src = "//gc.zgo.at/count.js";
  document.body.appendChild(s);
}

function currentPage(){
  const p = location.pathname.split("/").pop();
  return p === "" ? "index.html" : p;
}

function renderNavbar(){
  const here = currentPage();
  const links = SITE.nav.map(n =>
    `<a href="${n.href}" class="${n.href===here?"active":""}">${n.label}</a>`).join("");

  const bar = document.createElement("nav");
  bar.className = "navbar";
  bar.innerHTML = `
    <div class="navbar-inner">
      <a class="navbar-brand" href="index.html">
        ${SITE.brandTop}<span>${SITE.brandSub}</span>
      </a>
      <button class="navbar-toggle" aria-label="Menu">&#9776;</button>
      <div class="navbar-links">${links}</div>
    </div>`;
  document.body.prepend(bar);

  bar.querySelector(".navbar-toggle").addEventListener("click", () => {
    bar.querySelector(".navbar-links").classList.toggle("open");
  });
}

function renderFooter(){
  const f = document.createElement("footer");
  f.innerHTML = `
    <div class="footer-inner">
      <div class="footer-col lede">
        <strong>RESEARCH CLUSTER ON FINTECH &amp; DIGITAL ASSETS</strong>
        A multidisciplinary research community studying the economics, finance,
        regulation, and technology of digital assets, decentralised finance,
        and the future of money.
      </div>
      <div class="footer-col">
        <strong>EXPLORE</strong>
        <a href="journal.html">The Journal of FinTech &amp; Digital Assets</a><br/>
        <a href="publications.html">Publications</a><br/>
        <a href="seminars.html">Seminars</a> ·
        <a href="indices.html">Live indices</a><br/>
        <a href="analytics.html">Analytics</a>
      </div>
      <div class="footer-col">
        <strong>CONTACT</strong>
        Assoc. Prof. Cuong Nguyen<br/>
        <a href="mailto:${SITE.email}">${SITE.email}</a><br/>
        <span style="opacity:.7">© ${new Date().getFullYear()} · CC BY 4.0</span>
      </div>
    </div>`;
  document.body.appendChild(f);
}

document.addEventListener("DOMContentLoaded", () => {
  renderNavbar();
  renderFooter();
  loadAnalytics();
});

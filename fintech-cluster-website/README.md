# Research Cluster on FinTech & Digital Assets — Website

A static, multi-page website for the research community at Lincoln University.
Plain HTML/CSS/JS — **no build step**. Anyone can fork it and host it free on
**GitHub Pages**. This README is the single place that explains **what every
file does and exactly how to edit it** (there are no editing instructions on the
pages themselves).

---

## 1. File map — what each file is for

```
index.html          Home — full-bleed hero image + community intro + JFDA feature
about.html          About — mission, cluster lead, members grid, partners
journal.html        The Journal of FinTech & Digital Assets (JFDA) showcase
indices.html        Interactive charts: LIVE BTC/ETH + research indices
publications.html   Filterable, year-grouped publication list
research.html       Six research themes, methods, ongoing projects
seminars.html       Upcoming & past seminar series
news.html           Live crypto ticker + auto-updating RSS news feed
analytics.html      Live visitor & country analytics + GitHub repo traffic

assets/style.css    ONE stylesheet for every page (all colours, fonts, layout)
assets/site.js      Injects the nav bar + footer on every page; holds site-wide links
data/*.json         Time-series for the research-index charts
data/convert_to_json.py   Helper: converts CSV/XLSX/TXT -> the JSON the charts need
data/traffic/       GitHub repo traffic history + the collector script
.github/workflows/traffic.yml   Daily Action that records GitHub repo traffic
img/hero-bg.jpg     Background image used by the Home hero
.nojekyll           Tells GitHub Pages to serve files as-is (keep it)
LICENSE             CC BY 4.0
```

---

## 2. The two files you'll edit most

### `assets/site.js` — site-wide links, brand, navigation
Open it and edit the `SITE` object at the top. This controls **every page at once**:

```js
const SITE = {
  brandTop:  "FinTech & Digital Assets",   // big brand text, top-left
  brandSub:  "Research Cluster",            // small line under it
  email:     "fintech.cluster@lincoln.ac.nz",  // footer + contact links
  scholar:   "https://scholar.google.com",
  journalUrl:"https://journals.lincoln.ac.nz/index.php/JFDA",
  ...
  nav: [  // the tabs, in order. Remove a line to hide a tab; reorder to reorder.
    { label: "Home",        href: "index.html" },
    { label: "About",       href: "about.html" },
    { label: "Journal",     href: "journal.html" },
    ...
  ],
};
```
The footer (contact = **Assoc. Prof. Cuong Nguyen**, Lincoln University) is also
defined in this file, in `renderFooter()`. Edit the text there to change it.

### `assets/style.css` — colours & fonts
Edit the `:root` block at the very top. The whole site recolours from these:

```css
:root{
  --accent:#1a4f8a;      /* main blue — links, buttons, highlights */
  --accent2:#2e72c4;     /* hover blue */
  --ink:#1f2733;         /* main text */
  --bg:#ffffff;          /* page background */
  --serif:'Lora', Georgia, serif;          /* headings */
  --sans:'Source Sans 3', system-ui, sans-serif;  /* body text */
  --mono:'JetBrains Mono', monospace;      /* labels, dates, code */
  ...
}
```
Fonts are loaded from Google Fonts in each page's `<head>`. To change the font,
update the `<link href="...fonts.googleapis.com...">` line **and** the `--serif`/
`--sans` variables.

---

## 3. Page-by-page editing guide

### `index.html` (Home)
- **Title / subtitle:** edit the text inside `<h1 class="hero-bg-title">` and
  `<p class="hero-bg-sub">`.
- **Background image:** replace `img/hero-bg.jpg` with your own image of the same
  name (recommended ~1920×720). Or change the filename in `style.css` under
  `.hero-bg { background: ... url('img/hero-bg.jpg') ... }`.
- **Stat boxes / theme cards / "Latest" list:** edit the matching HTML blocks.
  They are plain HTML — just change the text between the tags.

### `about.html`
- **Cluster lead bio:** the `.feature` block near the top.
- **Members:** each member is a `<div class="person">…</div>`. Copy one to add a
  person. The circle shows initials by default; to use a photo, replace
  `<div class="person-photo">CN</div>` with
  `<img class="person-photo" src="img/cuong.jpg" alt="Cuong Nguyen">`
  (put the image in `img/`).

### `journal.html` (JFDA)
- Article entries are `<div class="news-item">…</div>` blocks grouped under
  `<div class="pub-year">` headings. Update titles/authors/links as new issues
  publish. The external links already point to the live journal.

### `publications.html`
- **All publications live in ONE place:** the `PUBS` array inside the `<script>`
  tag. Each entry looks like:
  ```js
  { year:2026, type:"journal",
    title:"Your paper title",
    authors:["C. Nguyen","J. Smith"], me:"C. Nguyen",  // 'me' is bolded
    venue:"Journal name, volume(issue), pages",
    links:[{t:"DOI",u:"https://doi.org/..."},{t:"PDF",u:"..."}] },
  ```
  - `type` must be one of: `"journal"`, `"working"`, `"conf"`, `"chapter"`
    (these drive the colour badge and the filter buttons).
  - `me` bolds a name to highlight a cluster member (use `""` for none).
  - Add as many `links` as you like; the first link is also the title link.
  - Sorting by year and grouping are automatic.

### `research.html`
- Each theme is a `<div class="theme">`. Edit text, or change the coloured left
  border with `style="border-left-color:var(--green)"` (options: `--accent`,
  `--green`, `--purple`, `--amber`, `--red`).

### `seminars.html`
- Each talk is a `<div class="seminar">`. The date box uses
  `<span class="day">12</span>JUN 2026`. Use `tag-upcoming` (green) or
  `tag-past` (grey) for the status label. Move past talks to the archive section.

### `news.html`
See section 5 (it's automated).

---

## 4. Updating the Indices charts

The four research charts read from `data/*.json`. Each JSON file is simply:

```json
[[1704067200000, 100.0], [1706745600000, 103.5], ...]
```
i.e. `[unix_timestamp_in_milliseconds, value]`, oldest first.

**You don't have to make that by hand — use the converter:**

```bash
# one-time setup (only if you use Excel files)
pip install pandas openpyxl

# convert your data
python data/convert_to_json.py my_data.csv -o data/defi_tvl.json
```

Your input file just needs a date column and a value column, e.g.:

```
date,value
2024-01-01,100.0
2024-02-01,102.4
```

It accepts `.csv`, `.tsv`, `.txt`, `.xlsx`, `.xls`, auto-detects the columns and
common date formats, and writes the chart-ready JSON. Run
`python data/convert_to_json.py --help` for all options (`--date-col`,
`--value-col`, `-o`). Then commit the updated `.json` and refresh the page.

To add a **new** chart: add a `<div class="chart-card">` with a
`<div id="chart-xyz">` in `indices.html`, drop a `data/xyz.json` file, and add one
`plotArea('chart-xyz', xyz, 'Label', '#1a4f8a')` call in the script (copy an
existing one).

**Live BTC/ETH** needs no maintenance — it streams from CoinGecko's free public
API automatically. (Live data only works when the page is served over http/https,
i.e. on GitHub Pages or a local server, not by double-clicking the file.)

---

## 5. The automated News feed

`news.html` has two automated parts:

1. **Live crypto ticker** — pulls current prices + 24h change for 6 coins from
   CoinGecko. Edit the `COINS` array to change which coins appear.

2. **Live headlines** — pulls RSS feeds from established FinTech sources and
   merges them newest-first. Edit the `FEEDS` array near the bottom of the page:
   ```js
   const FEEDS=[
     {label:"FINTECH NZ", url:"https://fintechnews.co.nz/feed/"},
     {label:"JFDA",       url:"https://journals.lincoln.ac.nz/.../rss2"},
     {label:"FINTECH SG", url:"https://fintechnews.sg/feed/"}
   ];
   ```
   - `label` is the little tag shown on each headline.
   - `url` must be a standard RSS/Atom feed (most news sites expose `/feed/`).
   - Because GitHub Pages is static and browsers block cross-site requests, the
     feeds are fetched through the free public proxy **api.rss2json.com**. No key
     is needed for light use; for heavy traffic you can get a free key from
     rss2json and append `&api_key=YOUR_KEY` to the request URL in the code.
   - If the live feed can't be reached, the page automatically shows the static
     fallback items hard-coded in the `#news-fallback` block — edit those so the
     page always has something sensible to show.

Other good feeds you can add: `https://fintechnews.ch/feed/`,
`https://thefintechtimes.com/feed/`, `https://www.financemagnates.com/feed/`.
(CoinMarketCap doesn't offer a free open price API like CoinGecko, so the ticker
uses CoinGecko; you can still add CMC's blog RSS as a headline source.)

---

## 6. Run locally

```bash
cd <the website folder>
python3 -m http.server 8000
# open http://localhost:8000
```
Edit a file, save, refresh the browser. No rebuild needed.

---

## 7. Publish to GitHub Pages (free)

1. Create a GitHub repository (e.g. `fintech-cluster`).
2. Upload all these files, keeping the folder structure.
3. **Settings → Pages → Build and deployment → Source: Deploy from a branch →
   Branch: `main`, Folder: `/ (root)` → Save.**
4. Wait ~1 minute. Live at `https://YOUR-USERNAME.github.io/fintech-cluster/`.

Custom domain: Settings → Pages → Custom domain (adds a `CNAME` file + DNS).

### Sharing with a friend
Everything is self-contained — no dependencies. A friend forks the repo (or
downloads the ZIP) and repeats step 3. Their copy is fully independent.

---

## 8. Licence
Content & code: CC BY 4.0 (see `LICENSE`). Charts use Highcharts via CDN — review
the Highcharts licence for your use (free for non-commercial/personal projects).

---

## 9. Analytics — visitors, countries & GitHub traffic

The site has an **Analytics** tab (`analytics.html`) with two independent parts.

### A) Live-site visitors & countries — GoatCounter (free, privacy-friendly)
Counts real visits to your published site and shows a **world map of countries**,
top pages, referrers, browsers, and screen sizes. No cookies, no consent banner.

**Setup (5 minutes):**
1. Sign up free at <https://www.goatcounter.com/> and choose a *code*
   (a subdomain), e.g. `fintech-cluster` → your dashboard becomes
   `https://fintech-cluster.goatcounter.com`.
2. Open `assets/site.js` and set:
   ```js
   goatcounterCode: "fintech-cluster",   // your code, not the full URL
   ```
   That single line switches on tracking **on every page** and wires up the
   embedded dashboard on the Analytics page. Leave it `""` to disable tracking
   entirely.
3. In GoatCounter, go to **Settings → "Allow public access to the dashboard"**
   and save. This lets the Analytics page embed your live stats. (If you'd
   rather keep stats private, skip this — tracking still works, you just view
   numbers by logging into GoatCounter instead of on your own page.)
4. Optional: in GoatCounter **Settings → Ignore these IPs**, add your own IP so
   your visits aren't counted.
5. Commit & push. Visits to the live site now appear on the Analytics page.

Notes:
- Tracking is automatically **skipped on `localhost`**, so local testing never
  pollutes your numbers.
- The script is ~3.5 KB and loads asynchronously.
- GoatCounter is free for reasonable public use; you can self-host it later if
  you ever outgrow that.

### B) GitHub repository traffic — automated daily collector
GitHub records repo **views, unique visitors, clones, and referrers**, but only
keeps the **last 14 days**. A scheduled GitHub Action saves snapshots daily so
you build up full history. (GitHub's traffic API does **not** include countries —
that's what GoatCounter is for. The two together cover both questions.)

**Files involved:**
- `.github/workflows/traffic.yml` — runs daily at 03:17 UTC (and on-demand).
- `data/traffic/collect_traffic.py` — fetches the API and merges results.
- `data/traffic/*.json` — the saved history the Analytics page reads.

**Setup:** essentially nothing — it uses the automatic `GITHUB_TOKEN`. Just make
sure Actions are allowed to write:
1. Repo **Settings → Actions → General → Workflow permissions →
   "Read and write permissions"** → Save.
2. Push the repo. To get data immediately without waiting for 03:17 UTC, go to
   the **Actions** tab → *Collect repo traffic* → **Run workflow**.
3. After it runs, the charts on the Analytics page fill in. Each subsequent day
   it appends new numbers, so your history grows past 14 days.

**Run it locally (optional):**
```bash
GH_TOKEN=<personal access token with repo scope> \
REPO=YOUR-USERNAME/YOUR-REPO \
python data/traffic/collect_traffic.py
```

**Important:** GitHub's traffic API reports traffic to the **repository** pages
(github.com/you/repo). Traffic to the *published website*
(you.github.io/repo) is measured by GoatCounter in part A. For a public research
site you'll usually care most about the GoatCounter numbers; the GitHub traffic
is a useful bonus (e.g. how many people view or clone the source).

### Turning analytics off
- Live tracking: set `goatcounterCode: ""` in `assets/site.js`.
- GitHub collector: disable the workflow in the **Actions** tab, or delete
  `.github/workflows/traffic.yml`.
- Hide the tab entirely: remove the `{ label: "Analytics", ... }` line from the
  `nav` array in `assets/site.js`.

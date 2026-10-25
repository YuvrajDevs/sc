// Builds the static site from content/ into the repo root. No dependencies: `node build.mjs`.
//
// Each file in content/ starts with a JSON block between <!--meta and -->, then the page body:
//   <!--meta {"title": "...", "description": "...", "nav": "features"} -->
// Guides (content/guides/*.html) also take "date", "keyword", "summary" and "readMins".
// The guides index, the home page's latest guides and sitemap.xml are generated from them.

import { readFileSync, writeFileSync, readdirSync, mkdirSync, existsSync } from "node:fs";
import { dirname, join } from "node:path";

const SITE = JSON.parse(readFileSync("site.json", "utf8"));
const read = (p) => readFileSync(p, "utf8");
const esc = (s) => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");

function parse(file) {
  const raw = read(file);
  const m = raw.match(/^<!--meta\s*([\s\S]*?)-->\s*/);
  if (!m) throw new Error(`${file}: missing <!--meta {...} --> header`);
  return { meta: JSON.parse(m[1]), body: raw.slice(m[0].length) };
}

// Output path for a content file, relative to the site root, and the "../" prefix that reaches the root from it.
function outPath(rel) { return rel.replace(/\.html$/, "") === "index" ? "index.html" : rel; }
function rootFrom(out) { const depth = out.split("/").length - 1; return depth ? "../".repeat(depth) : "./"; }
function pageUrl(out) { return SITE.url + "/" + out.replace(/(^|\/)index\.html$/, "$1").replace(/\.html$/, ""); }

const guides = readdirSync("content/guides").filter((f) => f.endsWith(".html") && f !== "index.html").map((f) => {
  const { meta } = parse(join("content/guides", f));
  return { ...meta, out: "guides/" + f };
}).sort((a, b) => b.date.localeCompare(a.date));

function guideCards(list, root) {
  return list.map((g) => `
      <a class="card" href="${root}${g.out.replace(/\.html$/, "")}">
        <div class="eyebrow">${esc(g.keyword)}</div>
        <h3 style="margin-top:16px">${esc(g.title)}</h3>
        <p>${esc(g.summary)}</p>
      </a>`).join("");
}

function layout({ meta, body, out }) {
  const root = meta.root || rootFrom(out);
  const url = pageUrl(out);
  const title = meta.title === SITE.name ? meta.title : `${meta.title} · ${SITE.name}`;
  const navItem = (key, href, label) =>
    `<li><a href="${root}${href}"${meta.nav === key ? ' aria-current="page"' : ""}>${label}</a></li>`;
  const jsonLd = [
    { "@context": "https://schema.org", "@type": "SoftwareApplication", name: SITE.name, operatingSystem: "Android",
      applicationCategory: "UtilitiesApplication", url: SITE.url, downloadUrl: SITE.playUrl,
      offers: { "@type": "Offer", price: "0", priceCurrency: "USD" } },
    ...(meta.jsonLd || []),
  ];
  if (meta.date) jsonLd.push({ "@context": "https://schema.org", "@type": "Article", headline: meta.title,
    description: meta.description, datePublished: meta.date, dateModified: meta.updated || meta.date,
    author: { "@type": "Organization", name: SITE.name }, mainEntityOfPage: url });

  body = body
    .replaceAll("{{root}}", root)
    .replaceAll("{{play}}", SITE.playUrl)
    .replace("{{latestGuides}}", guideCards(guides.slice(0, 3), root))
    .replace("{{allGuides}}", guideCards(guides, root));

  return `<!doctype html>
<html lang="en" data-theme="dark">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${esc(title)}</title>
<meta name="description" content="${esc(meta.description)}">
<link rel="canonical" href="${url}">${meta.noindex ? '\n<meta name="robots" content="noindex">' : ""}
<meta name="theme-color" content="#0B1A1D">
<meta property="og:type" content="${meta.date ? "article" : "website"}">
<meta property="og:title" content="${esc(meta.title)}">
<meta property="og:description" content="${esc(meta.description)}">
<meta property="og:url" content="${url}">
<meta property="og:image" content="${SITE.url}/assets/img/logo-512.png">
<meta name="twitter:card" content="summary">
<link rel="icon" type="image/png" href="${root}assets/img/favicon.png">
<link rel="apple-touch-icon" href="${root}assets/img/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300..700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="${root}css/site.css">
<script>document.documentElement.classList.add("js");try{var t=localStorage.getItem("theme");if(t)document.documentElement.dataset.theme=t}catch(e){}</script>
<script type="application/ld+json">${JSON.stringify(jsonLd.length === 1 ? jsonLd[0] : jsonLd)}</script>
</head>
<body>
<header class="site-header">
  <div class="wrap">
    <nav class="nav" aria-label="Main">
      <a class="brand" href="${root}"><img src="${root}assets/img/logo-512.png" alt="" width="30" height="30">${SITE.name}</a>
      <ul class="nav-links">
        ${navItem("home", "", "Home")}
        ${navItem("features", "features", "Features")}
        ${navItem("security", "security", "Security")}
        ${navItem("how", "how-it-works", "How it works")}
        ${navItem("pricing", "pricing", "Pricing")}
        ${navItem("guides", "guides/", "Guides")}
        ${navItem("faq", "faq", "FAQ")}
      </ul>
      <div class="nav-actions">
        <button class="icon-btn" id="theme-btn" type="button" aria-label="Switch light or dark theme">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>
        </button>
        <a class="btn btn-primary" href="${SITE.playUrl}">Get the app</a>
        <button class="icon-btn menu-btn" id="menu-btn" type="button" aria-label="Open menu" aria-expanded="false">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M4 8h16M4 16h16"/></svg>
        </button>
      </div>
    </nav>
  </div>
</header>
<main>
${body.trim()}
</main>
<footer class="site-footer">
  <div class="wrap">
    <div class="foot-grid">
      <div>
        <a class="brand" href="${root}"><img src="${root}assets/img/logo-512.png" alt="" width="30" height="30">${SITE.name}</a>
        <p style="max-width:34ch">An offline photo and file vault for Android. No account, no cloud, no internet permission.</p>
      </div>
      <div><h4>Product</h4><ul>
        <li><a href="${root}features">Features</a></li>
        <li><a href="${root}security">Security</a></li>
        <li><a href="${root}how-it-works">How it works</a></li>
        <li><a href="${root}pricing">Pricing</a></li>
      </ul></div>
      <div><h4>Guides</h4><ul>
${guides.slice(0, 4).map((g) => `        <li><a href="${root}${g.out.replace(/\.html$/, "")}">${esc(g.navTitle || g.title)}</a></li>`).join("\n")}
        <li><a href="${root}guides/">All guides</a></li>
      </ul></div>
      <div><h4>Help</h4><ul>
        <li><a href="${root}faq">FAQ</a></li>
        <li><a href="${root}privacy">Privacy policy</a></li>
        <li><a href="${SITE.playUrl}">Google Play</a></li>
      </ul></div>
    </div>
    <div class="foot-base"><span>© ${new Date().getFullYear()} ${SITE.name}</span><span>Made to stay on your phone.</span></div>
  </div>
</footer>
<script src="${root}js/site.js" defer></script>
</body>
</html>
`;
}

// Every Google Play button and link carries the Play logo.
const PLAY_ICON = `<svg class="play-ico" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M4.3 2.4a1.4 1.4 0 0 0-.6 1.2v16.8c0 .5.2.9.6 1.2l9.5-9.6-9.5-9.6Zm10.6 10.7 2.6 2.6-11 6.3 8.4-8.9Zm3.8-3.4 2.6 1.5c.9.5.9 1.7 0 2.2l-2.7 1.6-2.9-2.8 3-2.5ZM6.5 1.9l11 6.3-2.6 2.7-8.4-9Z"/></svg>`;
function playIcons(html) {
  const href = SITE.playUrl.replace(/[.?]/g, "\\$&");
  return html.replace(new RegExp(`(<a [^>]*href="${href}"[^>]*>)(?!<svg)`, "g"), `$1${PLAY_ICON}`);
}

function walk(dir) {
  return readdirSync(dir, { withFileTypes: true }).flatMap((e) =>
    e.isDirectory() ? walk(join(dir, e.name)) : e.name.endsWith(".html") ? [join(dir, e.name)] : []);
}

const pages = [];
for (const file of walk("content")) {
  const rel = file.slice("content/".length);
  const out = outPath(rel);
  const { meta, body } = parse(file);
  if (!existsSync(dirname(out)) && dirname(out) !== ".") mkdirSync(dirname(out), { recursive: true });
  writeFileSync(out, playIcons(layout({ meta, body, out })));
  if (!meta.noindex) pages.push({ out, date: meta.updated || meta.date });
}

const today = new Date().toISOString().slice(0, 10);
writeFileSync("sitemap.xml", `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${pages.map((p) => `  <url><loc>${pageUrl(p.out)}</loc><lastmod>${p.date || today}</lastmod></url>`).join("\n")}
</urlset>
`);
writeFileSync("robots.txt", `User-agent: *\nAllow: /\n\nSitemap: ${SITE.url}/sitemap.xml\n`);
console.log(`Built ${pages.length} pages (${guides.length} guides).`);

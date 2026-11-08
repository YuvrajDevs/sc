// Builds the static site from content/ into public/, in every language. No dependencies: `node build.mjs`.
// Vercel runs this on each deploy (see vercel.json), so generated pages are never committed.
//
// Each file in content/ starts with a JSON block between <!--meta and -->, then the page body:
//   <!--meta {"title": "...", "description": "...", "nav": "features"} -->
// Articles (guides, compare, scenarios, features, tools) also take "date", "keyword", "summary", "faq"…
//
// Languages: English lives in content/, translations in content/<code>/ with the same file names (i18n/langs.json).
// A page that isn't translated yet simply isn't built in that language; links to it fall back to English.
// Interface text (menus, buttons, footer) comes from i18n/ui/<code>.json.

import { readFileSync, writeFileSync, readdirSync, mkdirSync, existsSync, rmSync, cpSync } from "node:fs";
import { dirname, join } from "node:path";

const SITE = JSON.parse(readFileSync("site.json", "utf8"));
const LANGS = JSON.parse(readFileSync("i18n/langs.json", "utf8"));
const OTHER_CODES = new Set(LANGS.filter((l) => l.code !== "en").map((l) => l.code));
const UI = Object.fromEntries(LANGS.map((l) => [l.code, JSON.parse(readFileSync(`i18n/ui/${l.code}.json`, "utf8"))]));
const OUT = "public";
const read = (p) => readFileSync(p, "utf8");
const esc = (s) => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");

function parse(file) {
  const raw = read(file);
  const m = raw.match(/^<!--meta\s*([\s\S]*?)-->\s*/);
  if (!m) throw new Error(`${file}: missing <!--meta {...} --> header`);
  try { return { meta: JSON.parse(m[1]), body: raw.slice(m[0].length) }; }
  catch (e) { throw new Error(`${file}: meta is not valid JSON (${e.message})`); }
}

// Every content file of one language, keyed by its output path ("index.html", "guides/x.html").
function walk(dir, top = true) {
  if (!existsSync(dir)) return [];
  return readdirSync(dir, { withFileTypes: true }).flatMap((e) => {
    if (e.isDirectory()) return top && dir === "content" && OTHER_CODES.has(e.name) ? [] : walk(join(dir, e.name), false);
    return e.name.endsWith(".html") ? [join(dir, e.name)] : [];
  });
}
const srcDir = (code) => (code === "en" ? "content" : `content/${code}`);
const PAGES = {};
for (const l of LANGS) {
  PAGES[l.code] = new Map(walk(srcDir(l.code)).map((f) => {
    const rel = f.slice(srcDir(l.code).length + 1);
    return [rel.replace(/\.html$/, "") === "index" ? "index.html" : rel, { file: f, ...parse(f) }];
  }));
}
// A translation whose English page was removed is dropped, so it can't come back as an orphan.
for (const l of LANGS) if (l.code !== "en") for (const k of PAGES[l.code].keys()) if (!PAGES.en.has(k)) PAGES[l.code].delete(k);

const prefix = (code) => (code === "en" ? "" : `${code}/`);
const clean = (out) => out.replace(/(^|\/)index\.html$/, "$1").replace(/\.html$/, "");
function rootFrom(path) { const depth = path.split("/").length - 1; return depth ? "../".repeat(depth) : "./"; }
const pageUrl = (code, out) => `${SITE.url}/${prefix(code)}${clean(out)}`;
// Output path a site-relative link points at: "" → index.html, "guides/" → guides/index.html, "faq" → faq.html.
function keyOf(p) {
  p = p.split("#")[0].split("?")[0];
  if (p === "" || p.endsWith("/")) return p + "index.html";
  return p.endsWith(".html") ? p : p + ".html";
}
const isAsset = (p) => /^(assets|css|js)\//.test(p) || /\.(png|jpe?g|svg|ico|xml|txt|ttf)$/.test(p);

function articles(code, dir) {
  return [...PAGES[code].entries()].filter(([out]) => out.startsWith(dir + "/") && out !== `${dir}/index.html`)
    .map(([out, p]) => ({ ...p.meta, out, slug: out.slice(dir.length + 1).replace(/\.html$/, ""), section: dir }))
    .sort((a, b) => (b.date || "").localeCompare(a.date || ""));
}
const SECTIONS = ["guides", "compare", "scenarios", "features", "tools"];

function playLink(lang, section, slug) {
  let url = SITE.playUrl + (lang.code === "en" ? "" : `&hl=${lang.hl}`);
  if (!slug) return url;
  const ref = `utm_source=sealcloak-site&utm_medium=${section}&utm_campaign=${slug}&utm_content=${lang.code}`;
  return `${url}&referrer=${encodeURIComponent(ref)}`;
}

const words = (a) => new Set(`${a.keyword || ""} ${a.title}`.toLowerCase().replace(/[^\p{L}\p{N} ]/gu, " ").split(/\s+/).filter((w) => w.length > 3));
function related(all, me, n = 3) {
  const mine = words(me);
  return all.filter((a) => a.out !== me.out)
    .map((a) => ({ a, s: [...words(a)].filter((w) => mine.has(w)).length + (a.section === me.section ? 0.5 : 0) }))
    .sort((x, y) => y.s - x.s || (y.a.date || "").localeCompare(x.a.date || "")).slice(0, n).map((x) => x.a);
}

const GLOBE = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/></svg>`;

function buildPage(lang, out, { meta, body }) {
  const ui = UI[lang.code];
  const here = prefix(lang.code) + out;
  const root = meta.root || rootFrom(here);
  const avail = PAGES[lang.code];
  // A site-relative link: this language's page if it exists, otherwise the English one.
  const link = (p) => {
    if (isAsset(p)) return root + p;
    return root + (avail.has(keyOf(p)) ? prefix(lang.code) : "") + p;
  };
  const lists = Object.fromEntries(SECTIONS.map((s) => [s, articles(lang.code, s)]));
  lists.features.sort((a, b) => (a.order ?? 99) - (b.order ?? 99));
  const all = SECTIONS.flatMap((s) => lists[s]);
  const art = all.find((a) => a.out === out);
  const url = pageUrl(lang.code, out);
  const title = meta.title === SITE.name ? meta.title : `${meta.title} · ${SITE.name}`;

  const cards = (list) => list.map((g) => `
      <a class="card" href="${link(g.out.replace(/\.html$/, ""))}">
        <div class="eyebrow">${esc(g.keyword || "")}</div>
        <h3 style="margin-top:16px">${esc(g.title)}</h3>
        <p>${esc(g.summary || "")}</p>
      </a>`).join("");

  const jsonLd = [
    { "@context": "https://schema.org", "@type": "SoftwareApplication", name: SITE.name, operatingSystem: "Android",
      applicationCategory: "UtilitiesApplication", url: SITE.url, downloadUrl: SITE.playUrl,
      offers: { "@type": "Offer", price: "0", priceCurrency: "USD" } },
    ...(meta.jsonLd || []),
  ];
  if (art) jsonLd.push({ "@context": "https://schema.org", "@type": "BreadcrumbList", itemListElement: [
    { "@type": "ListItem", position: 1, name: ui.sections.home, item: pageUrl(lang.code, "index.html") },
    { "@type": "ListItem", position: 2, name: ui.sections[art.section], item: pageUrl(lang.code, `${art.section}/index.html`) },
    { "@type": "ListItem", position: 3, name: meta.navTitle || meta.title, item: url } ] });
  if (meta.faq?.length) jsonLd.push({ "@context": "https://schema.org", "@type": "FAQPage", inLanguage: lang.hreflang,
    mainEntity: meta.faq.map((f) => ({ "@type": "Question", name: f.q, acceptedAnswer: { "@type": "Answer", text: f.a } })) });
  if (meta.steps?.length) jsonLd.push({ "@context": "https://schema.org", "@type": "HowTo", name: meta.title, inLanguage: lang.hreflang,
    step: meta.steps.map((t, i) => ({ "@type": "HowToStep", position: i + 1, text: t })) });
  if (meta.date) jsonLd.push({ "@context": "https://schema.org", "@type": "Article", headline: meta.title, inLanguage: lang.hreflang,
    description: meta.description, datePublished: meta.date, dateModified: meta.updated || meta.date,
    author: { "@type": "Organization", name: SITE.name }, mainEntityOfPage: url });

  if (art) {
    const faq = meta.faq?.length ? `
      <h2>${esc(ui.faqTitle)}</h2>
${meta.faq.map((f) => `      <h3>${esc(f.q)}</h3>\n      <p>${esc(f.a)}</p>`).join("\n")}` : "";
    const play = playLink(lang, art.section, art.slug);
    body = body.replace("{{faq}}", faq)
      .replaceAll("{{cta}}", `<div class="cta-card">
          <img src="{{root}}assets/img/logo-512.png" alt="" width="56" height="56">
          <div><h3>${esc(ui.ctaTitle)}</h3><p>${esc(ui.ctaBody)}</p></div>
          <a class="btn btn-primary" href="${play}">${esc(ui.ctaButton)}</a>
        </div>`)
      .replaceAll("{{play}}", play)
      .replace("{{related}}", `<div class="keep-reading"><div class="eyebrow">${esc(ui.keepReading)}</div><div class="cards">${cards(related(all, art))}
        </div></div>`);
    body += `\n<div class="sticky-cta"><span>${esc(ui.stickyText)}</span><a class="btn btn-primary" href="${play}">${esc(ui.stickyButton)}</a></div>`;
  }
  body = body
    .replaceAll("{{play}}", playLink(lang))
    .replaceAll("{{email}}", SITE.email)
    .replace("{{latestGuides}}", cards(lists.guides.slice(0, 3)))
    .replace("{{allGuides}}", cards(lists.guides))
    .replace("{{allCompares}}", cards(lists.compare))
    .replace("{{allScenarios}}", cards(lists.scenarios))
    .replace("{{allFeatures}}", cards(lists.features))
    .replace("{{allTools}}", cards(lists.tools))
    .replace(/\{\{root\}\}([^"'\s<>)]*)/g, (_, p) => link(p === "pricing" ? "how-it-works" : p)); // pricing was removed; stale translations may still link it

  // The same page in every language that has it, for search engines and the language menu.
  const versions = LANGS.filter((l) => PAGES[l.code].has(out));
  const hreflang = versions.map((l) => `<link rel="alternate" hreflang="${l.hreflang}" href="${pageUrl(l.code, out)}">`).join("\n")
    + (versions.length > 1 ? `\n<link rel="alternate" hreflang="x-default" href="${pageUrl("en", out)}">` : "");
  const langMenu = LANGS.map((l) => {
    const target = PAGES[l.code].has(out) ? out : "index.html";
    return `<li><a href="${root}${prefix(l.code)}${clean(target)}" hreflang="${l.hreflang}" lang="${l.hreflang}" data-lang="${l.code}"${l.code === lang.code ? ' aria-current="true"' : ""}>${esc(l.name)}</a></li>`;
  }).join("");
  const navItem = (key, href) => `<li><a href="${link(href)}"${meta.nav === key ? ' aria-current="page"' : ""}>${esc(ui.nav[key])}</a></li>`;
  const fontLink = lang.fontQuery ? `\n<link href="https://fonts.googleapis.com/css2?family=${lang.fontQuery}&display=swap" rel="stylesheet">` : "";
  const fontVars = lang.font ? `\n<style>:root{--sans:${lang.fontFirst ? `"${lang.font}","Outfit"` : `"Outfit","${lang.font}"`},system-ui,sans-serif;--mono:"Spline Sans Mono","${lang.font}",ui-monospace,monospace}</style>` : "";
  const toolStrings = /tool-metadata\.js/.test(body) ? `\n<script>window.SC_TOOL=${JSON.stringify(ui.tool)}</script>` : "";
  const toolsStrings = /js\/tools\.js/.test(body) && ui.tools ? `\n<script>window.SC_TOOLS=${JSON.stringify(ui.tools)}</script>` : "";

  return `<!doctype html>
<html lang="${lang.hreflang}" dir="${lang.dir}" data-theme="dark">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${esc(title)}</title>
<meta name="description" content="${esc(meta.description)}">
<link rel="canonical" href="${url}">${meta.noindex ? '\n<meta name="robots" content="noindex">' : ""}
${hreflang}
<meta name="theme-color" content="#0B1A1D">
<meta property="og:type" content="${meta.date ? "article" : "website"}">
<meta property="og:title" content="${esc(meta.title)}">
<meta property="og:description" content="${esc(meta.description)}">
<meta property="og:url" content="${url}">
<meta property="og:locale" content="${lang.hreflang.replace("-", "_")}">
<meta property="og:image" content="${SITE.url}/assets/img/logo-512.png">
<meta name="twitter:card" content="summary">
<link rel="icon" type="image/png" href="${root}assets/img/favicon.png">
<link rel="apple-touch-icon" href="${root}assets/img/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300..700&display=swap" rel="stylesheet">${fontLink}
<link rel="stylesheet" href="${root}css/site.css">${fontVars}${toolStrings}${toolsStrings}
<script>document.documentElement.classList.add("js");try{var t=localStorage.getItem("theme");if(t)document.documentElement.dataset.theme=t}catch(e){}</script>
<script type="application/ld+json">${JSON.stringify(jsonLd.length === 1 ? jsonLd[0] : jsonLd)}</script>
</head>
<body>
<header class="site-header">
  <div class="wrap">
    <nav class="nav" aria-label="Main">
      <a class="brand" href="${link("")}"><img src="${root}assets/img/logo-512.png" alt="" width="30" height="30">${SITE.name}</a>
      <ul class="nav-links">
        ${navItem("home", "")}
        ${navItem("features", "features")}
        ${navItem("security", "security")}
        ${navItem("how", "how-it-works")}
        ${navItem("guides", "guides/")}
        ${navItem("faq", "faq")}
        ${navItem("support", "support")}
      </ul>
      <div class="nav-actions">
        <details class="lang-menu">
          <summary class="lang-btn" aria-label="${esc(ui.languageLabel)}: ${esc(lang.name)}">${GLOBE}<span>${lang.code.split("-")[0].toUpperCase()}</span></summary>
          <ul>${langMenu}</ul>
        </details>
        <button class="icon-btn" id="theme-btn" type="button" aria-label="${esc(ui.themeLabel)}">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>
        </button>
        <a class="btn btn-primary" href="${playLink(lang)}">${esc(ui.getApp)}</a>
        <button class="icon-btn menu-btn" id="menu-btn" type="button" aria-label="${esc(ui.menuLabel)}" aria-expanded="false">
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
        <a class="brand" href="${link("")}"><img src="${root}assets/img/logo-512.png" alt="" width="30" height="30">${SITE.name}</a>
        <p style="max-width:34ch">${esc(ui.footTagline)}</p>
      </div>
      <div><h4>${esc(ui.footProduct)}</h4><ul>
        <li><a href="${link("features")}">${esc(ui.nav.features)}</a></li>
        <li><a href="${link("security")}">${esc(ui.nav.security)}</a></li>
        <li><a href="${link("how-it-works")}">${esc(ui.nav.how)}</a></li>
      </ul></div>
      <div><h4>${esc(ui.footGuides)}</h4><ul>
${lists.guides.slice(0, 4).map((g) => `        <li><a href="${link(g.out.replace(/\.html$/, ""))}">${esc(g.navTitle || g.title)}</a></li>`).join("\n")}
        <li><a href="${link("guides/")}">${esc(ui.allGuides)}</a></li>
        <li><a href="${link("compare/")}">${esc(ui.compareApps)}</a></li>
        <li><a href="${link("scenarios/")}">${esc(ui.realSituations)}</a></li>
        <li><a href="${link("tools/")}">${esc(ui.freeTools)}</a></li>
      </ul></div>
      <div><h4>${esc(ui.footHelp)}</h4><ul>
        <li><a href="${link("faq")}">${esc(ui.nav.faq)}</a></li>
        <li><a href="${link("support")}">${esc(ui.nav.support)}</a></li>
        <li><a href="${link("privacy")}">${esc(ui.privacy)}</a></li>
        <li><a href="${link("terms")}">${esc(ui.terms)}</a></li>
        <li><a href="${playLink(lang)}">${esc(ui.googlePlay)}</a></li>
      </ul></div>
    </div>
    <div class="foot-base"><span>© ${new Date().getFullYear()} ${SITE.name}</span><span>${esc(ui.footBase)}</span></div>
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
  return html.replace(new RegExp(`(<a [^>]*href="${href}[^"]*"[^>]*>)(?!<svg)`, "g"), `$1${PLAY_ICON}`);
}

rmSync(OUT, { recursive: true, force: true });
mkdirSync(OUT);
for (const dir of ["assets", "css", "js"]) cpSync(dir, join(OUT, dir), { recursive: true });

const sitemap = [];
const counts = {};
for (const lang of LANGS) {
  for (const [out, page] of PAGES[lang.code]) {
    // One 404 page serves the whole site.
    if (out === "404.html" && lang.code !== "en") continue;
    const dest = join(OUT, prefix(lang.code) + out);
    mkdirSync(dirname(dest), { recursive: true });
    writeFileSync(dest, playIcons(buildPage(lang, out, page)));
    counts[lang.code] = (counts[lang.code] || 0) + 1;
    if (!page.meta.noindex) sitemap.push({ lang, out, date: page.meta.updated || page.meta.date });
  }
}

const today = new Date().toISOString().slice(0, 10);
writeFileSync(join(OUT, "sitemap.xml"), `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">
${sitemap.map((p) => {
  const alts = LANGS.filter((l) => PAGES[l.code].has(p.out));
  const links = alts.length > 1 ? alts.map((l) => `\n    <xhtml:link rel="alternate" hreflang="${l.hreflang}" href="${pageUrl(l.code, p.out)}"/>`).join("") : "";
  return `  <url><loc>${pageUrl(p.lang.code, p.out)}</loc><lastmod>${p.date || today}</lastmod>${links}\n  </url>`;
}).join("\n")}
</urlset>
`);
writeFileSync(join(OUT, "robots.txt"), `User-agent: *\nAllow: /\n\nSitemap: ${SITE.url}/sitemap.xml\n`);
console.log(`Built ${sitemap.length} pages into ${OUT}/: ${Object.entries(counts).map(([c, n]) => `${c} ${n}`).join(", ")}.`);

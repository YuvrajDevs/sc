// Quality gate for an article before it is published: `node seo/check.mjs content/guides/<slug>.html`.
// Exits 1 with a list of problems if anything fails. The daily agent must get a clean pass before committing.
//
// It checks what makes a page rank and convert (keyword placement, a direct answer first, structure, FAQ,
// internal links, the install card), that it is a real, substantial page and not a near-copy of another,
// and that it never claims something Sealcloak doesn't do (see seo/facts.json).

import { readFileSync, readdirSync, existsSync } from "node:fs";
import { join, basename, dirname } from "node:path";

const ROOT = new URL("..", import.meta.url).pathname;
const file = process.argv[2];
if (!file) { console.error("usage: node seo/check.mjs content/guides/<slug>.html"); process.exit(2); }

const raw = readFileSync(file, "utf8");
const errors = [], warnings = [];
const fail = (m) => errors.push(m), warn = (m) => warnings.push(m);

const m = raw.match(/^<!--meta\s*([\s\S]*?)-->\s*/);
if (!m) { console.error("missing <!--meta {...} --> header"); process.exit(1); }
let meta;
try { meta = JSON.parse(m[1]); } catch (e) { console.error("meta is not valid JSON: " + e.message); process.exit(1); }
const body = raw.slice(m[0].length);
const text = (h) => h.replace(/<!--shared-->[\s\S]*?<!--\/shared-->/g, " ").replace(/<script[\s\S]*?<\/script>/g, " ").replace(/<[^>]+>/g, " ").replace(/&[a-z#0-9]+;/g, " ").replace(/\{\{[a-zA-Z]+\}\}/g, " ").replace(/\s+/g, " ").trim();
const prose = text(body) + " " + (meta.faq || []).map((f) => `${f.q} ${f.a}`).join(" ");
const wordCount = prose.split(" ").length;
const slug = basename(file, ".html");
const section = basename(dirname(file));

// ---- Meta
for (const k of ["title", "description", "keyword", "summary", "date", "readMins", "nav"]) if (meta[k] === undefined || meta[k] === "") fail(`meta.${k} is missing`);
if (meta.title?.length > 65) fail(`title is ${meta.title.length} chars; keep it under 65 so Google shows all of it`);
if (meta.description && (meta.description.length < 110 || meta.description.length > 160)) fail(`description is ${meta.description.length} chars; aim for 110–160`);
if (meta.date && !/^\d{4}-\d{2}-\d{2}$/.test(meta.date)) fail("date must be YYYY-MM-DD");
if (!/^[a-z0-9]+(-[a-z0-9]+)*$/.test(slug)) fail(`file name "${slug}" must be lowercase words joined by hyphens`);
if (!Array.isArray(meta.faq) || meta.faq.length < 4) fail("meta.faq needs at least 4 {q, a} questions (they become the FAQ section and FAQ rich results)");
for (const f of meta.faq || []) if (!f.q?.endsWith("?") || (f.a || "").length < 60) fail(`FAQ "${f.q}" needs a question mark and a real answer (60+ chars)`);
if (meta.readMins && Math.abs(meta.readMins - Math.round(wordCount / 220)) > 3) warn(`readMins ${meta.readMins} but the text is ~${Math.round(wordCount / 220)} min`);

// ---- Keyword placement
const kwTokens = (meta.keyword || "").toLowerCase().split(/\s+/).filter((w) => w.length > 2 && !["how", "the", "for", "and", "with", "app", "android"].includes(w));
const has = (s) => kwTokens.filter((w) => s.toLowerCase().includes(w.replace(/s$/, ""))).length / (kwTokens.length || 1);
if (has(meta.title || "") < 0.6) fail("the title should contain the keyword's main words");
const h1 = body.match(/<h1>([\s\S]*?)<\/h1>/)?.[1];
if (!h1) fail("no <h1>"); else if (has(text(h1)) < 0.6) fail("the h1 should contain the keyword's main words");
const lead = text(body.match(/<p class="lead">([\s\S]*?)<\/p>/)?.[1] || "");
if (!lead) fail('needs a <p class="lead"> intro right under the h1');

// ---- Structure that ranks: a direct answer first, headings, steps or a table, FAQ, install card, keep reading
if (!/<div class="answer">/.test(body)) fail('needs a <div class="answer"> quick-answer box near the top (this is what Google and AI answers quote)');
else if (body.indexOf('class="answer"') > body.indexOf("<h2")) fail("the quick-answer box must come before the first <h2>");
const h2s = [...body.matchAll(/<h2[^>]*>([\s\S]*?)<\/h2>/g)].map((x) => text(x[1]));
// Feature pages are shorter reference pages; guides, comparisons and scenarios are full articles.
// Tool how-to pages live under content/tools/<tool>/ and are short, practical companions to the tool.
const isToolHowTo = /content\/tools\/[^/]+\/[^/]+\.html$/.test(file);
const isFeature = section === "features" || section === "tools" || isToolHowTo;
if (h2s.length < (isFeature ? 3 : 4)) fail(`only ${h2s.length} <h2> sections; needs at least ${isFeature ? 3 : 4}`);
if (!isFeature && !/<ol>/.test(body) && !/<table>/.test(body)) fail("needs numbered steps (<ol>) or a comparison table");
if (section === "compare" && !/<table>/.test(body)) fail("compare pages need a side-by-side <table>");
if (/<table>/.test(body) && !/class="table-wrap"/.test(body)) fail('wrap tables in <div class="table-wrap"> so they scroll on phones');
for (const ph of ["{{cta}}", "{{faq}}", "{{related}}"]) if (!body.includes(ph)) fail(`missing the ${ph} placeholder`);
if ((body.match(/\{\{cta\}\}/g) || []).length > 2) fail("use {{cta}} at most twice");
const minWords = isToolHowTo ? 350 : isFeature ? 300 : section === "scenarios" ? 750 : 1100;
if (wordCount < minWords) fail(`only ~${wordCount} words; needs ${minWords}+${isFeature ? " (feature pages: say it plainly, don't pad)" : " (aim 1,400–2,000)"}`);
if (wordCount > 3200) warn(`~${wordCount} words is long; make sure every section earns its place`);

// ---- Internal links must point at pages that exist
const links = [...body.matchAll(/href="\{\{root\}\}([^"#]*)"/g)].map((x) => x[1]);
const exists = (p) => { p = p.replace(/\/$/, ""); return p === "" || p === "faq" || existsSync(join(ROOT, "content", p + ".html")) || existsSync(join(ROOT, "content", p, "index.html")); };
const broken = links.filter((l) => !exists(l));
if (broken.length) fail(`broken internal links: ${broken.join(", ")}`);
const articleLinks = links.filter((l) => /^(guides|compare|scenarios|features|tools)\/./.test(l) && !l.endsWith(slug));
if (articleLinks.length < (isFeature ? 1 : 2)) fail(`link to at least ${isFeature ? 1 : 2} other article(s) or feature page(s) inside the text`);
if (!isFeature && links.filter((l) => /^(features|security|how-it-works|faq)/.test(l)).length < 1) fail("link to at least one main page (features, security, how-it-works or faq)");

// ---- Never claim what the app doesn't do
const app = prose.replace(/\s+/g, " ");
const sentences = app.split(/(?<=[.!?])\s+/).filter((s) => /sealcloak/i.test(s) && !s.trim().endsWith("?"));
const FALSE = [
  [/\b(iphone|ios|ipad|mac|windows) (app|version)\b|available (on|for) (iphone|ios)/i, "Sealcloak is Android only"],
  [/\b(cloud (backup|sync|storage)|syncs?|uploads?) /i, "Sealcloak has no cloud, sync or upload"],
  [/\b(pin|password|passcode) (lock|unlock|to open)/i, "the vault unlocks with a pattern (and optional fingerprint), not a PIN or password"],
  [/\bopen[- ]source\b/i, "Sealcloak is not open source"],
  [/\b(hides?|locks?) (other|your) apps\b|app lock for (other|all) apps/i, "Sealcloak can't hide or lock other apps, only disguise itself"],
  [/\b(we|sealcloak) can (recover|reset|restore your access)/i, "nobody can recover a vault without the pattern or phrase"],
  [/\bautomatically (removes?|deletes?|moves?) (the )?(originals?|photos) from (your )?gallery/i, "the user deletes originals from the gallery themselves"],
  [/\b(military[- ]grade|unhackable|100% (safe|secure)|impossible to (hack|crack))\b/i, "no absolute security claims"],
];
for (const s of sentences) for (const [re, why] of FALSE) if (re.test(s) && !/\b(no|not|never|can't|cannot|doesn't|does not|without|isn't|only)\b/i.test(s)) fail(`possible false claim (${why}): "${s.slice(0, 140)}"`);
if (/(\$|₹|€|£)\s?\d/.test(app) && /sealcloak|\bpro\b/i.test(app)) fail("no prices: the site never mentions what Sealcloak costs");

// ---- Not a near-copy of another article (shared 6-word phrases)
const shingles = (t) => { const w = t.toLowerCase().replace(/[^a-z0-9 ]/g, " ").split(/\s+/).filter(Boolean); const s = new Set(); for (let i = 0; i + 6 <= w.length; i++) s.add(w.slice(i, i + 6).join(" ")); return s; };
const mine = shingles(prose);
for (const dir of ["guides", "compare", "scenarios", "features"]) {
  const d = join(ROOT, "content", dir);
  if (!existsSync(d)) continue;
  for (const f of readdirSync(d).filter((f) => f.endsWith(".html") && f !== "index.html" && join(d, f) !== join(ROOT, file) && !file.endsWith(`${dir}/${f}`))) {
    const other = readFileSync(join(d, f), "utf8");
    const om = other.match(/^<!--meta\s*([\s\S]*?)-->/); const ometa = om ? JSON.parse(om[1]) : {};
    if (ometa.keyword && meta.keyword && ometa.keyword.toLowerCase() === meta.keyword.toLowerCase()) fail(`${dir}/${f} already targets "${meta.keyword}"`);
    const theirs = shingles(text(other));
    const shared = [...mine].filter((x) => theirs.has(x)).length / (mine.size || 1);
    if (shared > 0.12) fail(`${Math.round(shared * 100)}% of its phrases also appear in ${dir}/${f}; write it fresh`);
  }
}

for (const w of warnings) console.log("warn  " + w);
for (const e of errors) console.log("FAIL  " + e);
console.log(errors.length ? `\n${errors.length} problem(s). Fix them and run the check again.` : `\nPASS  ~${wordCount} words, ${h2s.length} sections, ${meta.faq.length} FAQs, ${links.length} internal links.`);
process.exit(errors.length ? 1 : 0);

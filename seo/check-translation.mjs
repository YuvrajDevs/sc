// Checks a translated page against its English original: `node seo/check-translation.mjs content/es/guides/x.html`.
// Exits 1 with a list of problems. Translation agents must get a clean pass before committing.
//
// A translation must keep the page's structure (headings, lists, tables, placeholders, links, FAQ and steps),
// keep every number (prices, limits, counts) and the brand names, and actually be in the target language.

import { readFileSync, existsSync } from "node:fs";
import { createHash } from "node:crypto";
import { join } from "node:path";

const ROOT = new URL("..", import.meta.url).pathname;
const file = process.argv[2];
const m = file?.match(/content\/([a-z]{2}(?:-[a-z]{2})?)\/(.+\.html)$/);
if (!m) { console.error("usage: node seo/check-translation.mjs content/<lang>/<path>.html"); process.exit(2); }
const [, code, rel] = m;
const langs = JSON.parse(readFileSync(join(ROOT, "i18n/langs.json"), "utf8"));
const lang = langs.find((l) => l.code === code);
if (!lang || code === "en") { console.error(`"${code}" isn't one of the site's translation languages (i18n/langs.json)`); process.exit(2); }
const srcFile = join(ROOT, "content", rel);
if (!existsSync(srcFile)) { console.error(`no English original at content/${rel}`); process.exit(2); }

const errors = [], fail = (x) => errors.push(x);
function parse(f) {
  const raw = readFileSync(f, "utf8");
  const mm = raw.match(/^<!--meta\s*([\s\S]*?)-->\s*/);
  if (!mm) throw new Error(`${f}: missing meta`);
  return { meta: JSON.parse(mm[1]), body: raw.slice(mm[0].length) };
}
let src, tr;
try { src = parse(srcFile); } catch (e) { console.error(e.message); process.exit(1); }
try { tr = parse(file); } catch (e) { console.log("FAIL  meta is missing or not valid JSON: " + e.message); process.exit(1); }

const text = (h) => h.replace(/<script[\s\S]*?<\/script>/g, " ").replace(/<[^>]+>/g, " ").replace(/&[a-z#0-9]+;/g, " ").replace(/\{\{[a-zA-Z]+\}\}/g, " ").replace(/\s+/g, " ").trim();
const count = (h, re) => (h.match(re) || []).length;

// ---- Which English version this translates (seo/translation-status.mjs uses it to spot stale translations)
const hash = createHash("sha1").update(readFileSync(srcFile)).digest("hex").slice(0, 12);
if (tr.meta.sourceHash !== hash) fail(`meta.sourceHash must be "${hash}" (the English page it translates; it changes whenever the English page does)`);

// ---- Meta: same fields, same shapes; the structural ones must not change
for (const k of Object.keys(src.meta)) if (k !== "sourceHash" && !(k in tr.meta)) fail(`meta.${k} is missing`);
for (const k of ["nav", "date", "updated", "order", "root", "noindex", "readMins"]) if (k in src.meta && JSON.stringify(src.meta[k]) !== JSON.stringify(tr.meta[k])) fail(`meta.${k} must stay exactly as in English (${JSON.stringify(src.meta[k])})`);
for (const k of ["faq", "steps", "alsoTargets"]) if (Array.isArray(src.meta[k]) && (tr.meta[k] || []).length !== src.meta[k].length) fail(`meta.${k} must have ${src.meta[k].length} items like the English page`);
if (tr.meta.title && tr.meta.title.length > 75) fail(`title is ${tr.meta.title.length} characters; keep it under 75`);
if (tr.meta.description && tr.meta.description.length > 175) fail(`description is ${tr.meta.description.length} characters; keep it under 175`);

// ---- Structure: same tags, placeholders and links
for (const [name, re] of [["<h1>", /<h1[\s>]/g], ["<h2>", /<h2[\s>]/g], ["<h3>", /<h3[\s>]/g], ["<li>", /<li[\s>]/g], ["<table>", /<table[\s>]/g], ["<tr>", /<tr[\s>]/g],
  ["<ol>", /<ol[\s>]/g], ["<ul>", /<ul[\s>]/g], ["<details>", /<details[\s>]/g], ["<section>", /<section[\s>]/g], ["<script>", /<script[\s>]/g]]) {
  const a = count(src.body, re), b = count(tr.body, re);
  if (a !== b) fail(`${name} appears ${b} times; the English page has ${a}`);
}
for (const ph of new Set(src.body.match(/\{\{[a-zA-Z]+\}\}/g) || [])) if (count(src.body, new RegExp(ph.replace(/[{}]/g, "\\$&"), "g")) !== count(tr.body, new RegExp(ph.replace(/[{}]/g, "\\$&"), "g"))) fail(`placeholder ${ph} must appear the same number of times as in English`);
const hrefs = (h) => [...h.matchAll(/href="([^"]*)"/g)].map((x) => x[1]).sort();
if (JSON.stringify(hrefs(src.body)) !== JSON.stringify(hrefs(tr.body))) fail("links (href) must be exactly the same as in English; translate the link text, not the address");
const classes = (h) => [...h.matchAll(/class="([^"]*)"/g)].map((x) => x[1]).sort();
if (JSON.stringify(classes(src.body)) !== JSON.stringify(classes(tr.body))) fail("class attributes must stay exactly as in English");
const ids = (h) => [...h.matchAll(/id="([^"]*)"/g)].map((x) => x[1]).sort();
if (JSON.stringify(ids(src.body)) !== JSON.stringify(ids(tr.body))) fail("id attributes must stay exactly as in English");

// ---- Facts survive: every number and brand name in the English text is still there
const all = (p) => `${text(p.body)} ${JSON.stringify(p.meta)}`;
const digits = (s) => s.match(/\d+/g) || [];
const trDigits = digits(all(tr));
const trDigitsBag = trDigits.join(" ");
for (const d of new Set(digits(all(src)))) if (!trDigits.includes(d) && !trDigitsBag.includes(d)) fail(`the number ${d} from the English page is missing (keep prices, limits and counts)`);
for (const brand of ["Sealcloak", "Android", "Google Play", "PERMIT", "AES-256"]) if (all(src).includes(brand) && !all(tr).includes(brand)) fail(`"${brand}" must stay in the translation, untranslated`);

// ---- Actually translated: little English left
const enWords = new Set(text(src.body).toLowerCase().match(/[a-z]{4,}/g) || []);
const KEEP = new Set(["sealcloak", "android", "google", "play", "permit", "samsung", "xiaomi", "redmi", "oppo", "realme", "oneplus", "vivo", "pixel", "motorola", "whatsapp", "keepsafe", "drive", "jpeg", "heic", "exif", "argon2id", "keystore", "secure", "folder", "private", "space", "locked", "photos", "files", "safe", "gallery", "album", "settings", "galaxy", "poco", "nothing", "infinix", "tecno", "iqoo", "nova", "gcm", "lockmypix", "vaulty", "calculator"]);
const trText = text(tr.body) + " " + (tr.meta.faq || []).map((f) => `${f.q} ${f.a}`).join(" ");
const trTokens = trText.toLowerCase().match(/[\p{L}]+/gu) || [];
const leftover = trTokens.filter((w) => w.length >= 4 && enWords.has(w) && !KEEP.has(w));
const share = leftover.length / (trTokens.length || 1);
if (share > (lang.dir === "rtl" || ["bn", "ja", "ko"].includes(code) ? 0.04 : 0.12)) fail(`${Math.round(share * 100)}% of the words are still English (for example: ${[...new Set(leftover)].slice(0, 8).join(", ")})`);
if (/\p{Script=Latin}/u.test("a") && ["ar"].includes(code) && !/\p{Script=Arabic}/u.test(trText)) fail("no Arabic script found");
if (code === "bn" && !/\p{Script=Bengali}/u.test(trText)) fail("no Bengali script found");
if (code === "ja" && !/[\p{Script=Hiragana}\p{Script=Katakana}]/u.test(trText)) fail("no Japanese kana found");
if (code === "ko" && !/\p{Script=Hangul}/u.test(trText)) fail("no Korean Hangul found");

for (const e of errors) console.log("FAIL  " + e);
console.log(errors.length ? `\n${errors.length} problem(s). Fix them and run the check again.` : `PASS  ${code}/${rel}`);
process.exit(errors.length ? 1 : 0);

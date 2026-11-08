// Collects what people are searching for right now, from Google's and Bing's autocomplete, and ranks it
// into a queue of article topics in seo/keywords.json. No dependencies: `node seo/collect.mjs`.
//
// Autocomplete only suggests phrases many people type, and it updates daily, so it is a free, live
// signal of demand. Each suggestion scores higher the more seeds and sources it shows up under and the
// higher it appears. Topics already covered by a page on the site are dropped from the queue.

import { readFileSync, writeFileSync, readdirSync, existsSync } from "node:fs";
import { join } from "node:path";

const ROOT = new URL("..", import.meta.url).pathname;
const seeds = JSON.parse(readFileSync(join(ROOT, "seo/seeds.json"), "utf8"));
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

// Off-topic or wrong-platform phrases. Sealcloak is Android only, and we don't chase piracy terms.
const EXCLUDE = /\b(iphone|ipad|ios|mac|macbook|windows|pc|laptop|linux|apk|mod|crack|hack|login|sign in|download free|porn|nude|xxx|sex|reddit|quora|meaning in|in hindi meaning|stock|share price|kindle|fire tv|smart tv|download|facebook|instagram|snapchat|tiktok|twitter|telegram channel)\b/i;
// A suggestion must be about hiding, locking or protecting private stuff on a phone.
const ON_TOPIC = /(hide|hidden|hider|vault|lock|locker|private|secret|secure|encrypt|calculator|gallery|album|intruder|keepsafe|lockmypix|vaulty|incognito|disguise|password protect|protect (photos|pictures|videos|files))/i;
const STOP = new Set(["how", "to", "the", "a", "an", "in", "on", "for", "my", "your", "of", "and", "or", "with", "without", "is", "can", "i", "do", "you", "app", "apps", "best", "android", "phone", "mobile"]);

async function fetchJson(url) {
  try {
    const r = await fetch(url, { headers: { "User-Agent": "Mozilla/5.0 (compatible; sealcloak-seo/1.0)" } });
    if (!r.ok) return null;
    return JSON.parse(await r.text());
  } catch { return null; }
}

const google = async (q) => (await fetchJson(`https://suggestqueries.google.com/complete/search?client=firefox&hl=en&gl=in&q=${encodeURIComponent(q)}`))?.[1] ?? [];
const bing = async (q) => (await fetchJson(`https://api.bing.com/osjson.aspx?query=${encodeURIComponent(q)}&mkt=en-IN`))?.[1] ?? [];

function queries() {
  const list = [];
  const az = "abcdefghijklmnopqrstuvwxyz".split("");
  for (const s of seeds.deep) {
    list.push(s, `how to ${s}`, `${s} on`, `${s} without`, `best ${s}`, `${s} app`);
    for (const c of az) list.push(`${s} ${c}`);
  }
  for (const s of seeds.shallow) list.push(s, `how to ${s}`, `${s} vs`, `${s} alternative`);
  for (const b of seeds.brands) list.push(`hide photos in ${b}`, `${b} hidden photos`, `${b} app lock`);
  return [...new Set(list)];
}

const tokens = (k) => k.toLowerCase().replace(/[^a-z0-9 ]/g, " ").split(/\s+/).filter((w) => w && !STOP.has(w));
function jaccard(a, b) {
  const A = new Set(a), B = new Set(b);
  const inter = [...A].filter((x) => B.has(x)).length;
  return inter / (A.size + B.size - inter || 1);
}

// Keywords and titles of every page that already exists, so the queue only holds new topics.
function covered() {
  const out = [];
  for (const dir of ["content/guides", "content/compare"]) {
    const d = join(ROOT, dir);
    if (!existsSync(d)) continue;
    for (const f of readdirSync(d).filter((f) => f.endsWith(".html") && f !== "index.html")) {
      const m = readFileSync(join(d, f), "utf8").match(/^<!--meta\s*([\s\S]*?)-->/);
      if (!m) continue;
      const meta = JSON.parse(m[1]);
      out.push({ page: `${dir.replace("content/", "")}/${f.replace(/\.html$/, "")}`, keys: [meta.keyword, meta.title, ...(meta.alsoTargets || [])].filter(Boolean).map(tokens) });
    }
  }
  return out;
}

const scores = new Map(); // phrase -> { score, sources:Set, seen }
function add(list, source) {
  list.forEach((raw, i) => {
    const k = raw.toLowerCase().trim().replace(/\s+/g, " ");
    if (k.split(" ").length < 2 || EXCLUDE.test(k) || !ON_TOPIC.test(k)) return;
    const e = scores.get(k) ?? { score: 0, sources: new Set(), seen: 0 };
    e.score += 10 - Math.min(i, 9); // first suggestion is the most searched
    e.sources.add(source); e.seen++;
    scores.set(k, e);
  });
}

const qs = queries();
console.log(`Asking Google and Bing for ${qs.length} phrases…`);
for (const q of qs) {
  const [g, b] = await Promise.all([google(q), bing(q)]);
  add(g, "google"); add(b, "bing");
  await sleep(120);
}

// Group near-identical phrases ("hide photos samsung", "how to hide photos on samsung") into one topic.
const ranked = [...scores.entries()]
  .map(([k, e]) => ({ keyword: k, score: e.score * (e.sources.size === 2 ? 1.5 : 1), sources: [...e.sources], t: tokens(k) }))
  .sort((a, b) => b.score - a.score);
const topics = [];
for (const r of ranked) {
  const hit = topics.find((t) => jaccard(t.t, r.t) >= 0.6);
  if (hit) { hit.score += r.score * 0.5; if (hit.variants.length < 8) hit.variants.push(r.keyword); continue; }
  topics.push({ keyword: r.keyword, score: r.score, sources: r.sources, variants: [], t: r.t });
}

const done = covered();
const isCovered = (t) => done.find((p) => p.keys.some((k) => jaccard(k, t.t) >= 0.5));
const kind = (k) => /\b(vs|versus|alternative|alternatives|compared|review)\b/.test(k) ? "compare" : "guide";

const queue = [], skipped = [];
for (const t of topics.sort((a, b) => b.score - a.score)) {
  const c = isCovered(t);
  const item = { keyword: t.keyword, type: kind(t.keyword), score: Math.round(t.score), sources: t.sources, variants: t.variants };
  if (c) skipped.push({ ...item, coveredBy: c.page }); else queue.push(item);
}

// A blocked network returns nothing. Keep yesterday's queue rather than wiping it.
if (scores.size === 0) {
  console.error("No suggestions came back (network blocked?). Keeping the existing seo/keywords.json.");
  process.exit(3);
}

const out = { updated: new Date().toISOString(), queries: qs.length, phrases: scores.size, queue: queue.slice(0, 150), alreadyCovered: skipped.slice(0, 50) };
writeFileSync(join(ROOT, "seo/keywords.json"), JSON.stringify(out, null, 2) + "\n");
console.log(`${scores.size} on-topic phrases, ${topics.length} topics, ${queue.length} not yet covered.`);
console.log("Top 15:");
for (const q of queue.slice(0, 15)) console.log(`  ${String(q.score).padStart(4)}  [${q.type}]  ${q.keyword}`);

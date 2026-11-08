// Lists which pages still need translating, per language: `node seo/translation-status.mjs [--json] [lang]`.
// "missing" = no translation yet; "stale" = the English page changed since it was translated.
// Order: home and the main pages first (they carry the most traffic), then features, guides, the rest.

import { readFileSync, readdirSync, existsSync } from "node:fs";
import { join } from "node:path";
import { createHash } from "node:crypto";

const ROOT = new URL("..", import.meta.url).pathname;
const langs = JSON.parse(readFileSync(join(ROOT, "i18n/langs.json"), "utf8")).filter((l) => l.code !== "en");
const codes = new Set(langs.map((l) => l.code));
const want = process.argv.slice(2).filter((a) => !a.startsWith("--"));
const asJson = process.argv.includes("--json");

function walk(dir, top) {
  return readdirSync(join(ROOT, dir), { withFileTypes: true }).flatMap((e) => {
    if (e.isDirectory()) return top && codes.has(e.name) ? [] : walk(join(dir, e.name), false);
    return e.name.endsWith(".html") && e.name !== "404.html" ? [join(dir, e.name).slice("content/".length)] : [];
  });
}
const rank = (r) => (r === "index.html" ? -1 : !r.includes("/") ? 0 : r.endsWith("/index.html") ? 1 : r.startsWith("features/") ? 2 : r.startsWith("tools/") ? 3 : r.startsWith("guides/") ? 4 : 5);
const english = walk("content", true).sort((a, b) => rank(a) - rank(b) || a.localeCompare(b));
const hashOf = (rel) => createHash("sha1").update(readFileSync(join(ROOT, "content", rel))).digest("hex").slice(0, 12);

const out = {};
for (const l of langs.filter((l) => !want.length || want.includes(l.code))) {
  const todo = [];
  for (const rel of english) {
    const f = join(ROOT, "content", l.code, rel);
    if (!existsSync(f)) { todo.push({ page: rel, status: "missing" }); continue; }
    const m = readFileSync(f, "utf8").match(/"sourceHash"\s*:\s*"([0-9a-f]+)"/);
    if (!m || m[1] !== hashOf(rel)) todo.push({ page: rel, status: "stale", hash: hashOf(rel) });
  }
  out[l.code] = { done: english.length - todo.length, total: english.length, todo };
}
if (asJson) console.log(JSON.stringify(out, null, 2));
else for (const [c, r] of Object.entries(out)) console.log(`${c.padEnd(6)} ${r.done}/${r.total} translated${r.todo.length ? `; next: ${r.todo.slice(0, 3).map((t) => `${t.page}${t.status === "stale" ? " (stale)" : ""}`).join(", ")}` : ""}`);

// Tells Bing and other IndexNow search engines about new or changed pages, so they crawl them within hours.
// `node seo/indexnow.mjs` pings every URL in the built sitemap; `node seo/indexnow.mjs guides/x tools/y` pings just those paths.
// Run after the deploy is live (the key file must be reachable at the site root).
import { readFileSync } from "node:fs";
const SITE = JSON.parse(readFileSync(new URL("../site.json", import.meta.url)));
const host = new URL(SITE.url).host;
let urls = process.argv.slice(2).map((p) => `${SITE.url}/${p.replace(/^\//, "")}`);
if (!urls.length) urls = [...readFileSync(new URL("../public/sitemap.xml", import.meta.url), "utf8").matchAll(/<loc>([^<]+)<\/loc>/g)].map((m) => m[1]);
const res = await fetch("https://api.indexnow.org/indexnow", {
  method: "POST", headers: { "content-type": "application/json; charset=utf-8" },
  body: JSON.stringify({ host, key: SITE.indexNowKey, keyLocation: `${SITE.url}/${SITE.indexNowKey}.txt`, urlList: urls.slice(0, 10000) }),
});
console.log(`IndexNow: ${res.status} for ${urls.length} URL(s)`);

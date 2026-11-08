// Local preview of the built site in public/, served the way Vercel does (/features → features.html).
// Run `node build.mjs` first, then `node serve.mjs`.
import { createServer } from "node:http";
import { readFile, stat } from "node:fs/promises";
import { dirname, extname, join, normalize } from "node:path";
import { fileURLToPath } from "node:url";

process.chdir(join(dirname(fileURLToPath(import.meta.url)), "public"));

const types = { ".html": "text/html; charset=utf-8", ".css": "text/css", ".js": "text/javascript", ".png": "image/png",
  ".svg": "image/svg+xml", ".ttf": "font/ttf", ".xml": "application/xml", ".txt": "text/plain" };
const port = Number(process.env.PORT) || 4321;

async function resolve(path) {
  for (const p of [path, path + ".html", join(path, "index.html")]) {
    try { if ((await stat(p)).isFile()) return p; } catch {}
  }
  return null;
}

createServer(async (req, res) => {
  const path = "." + normalize(decodeURIComponent(new URL(req.url, "http://x").pathname));
  const file = await resolve(path);
  res.writeHead(file ? 200 : 404, { "content-type": types[extname(file || ".html")] || "application/octet-stream" });
  res.end(await readFile(file || "404.html").catch(() => "Not found (rebuilding?)"));
}).listen(port, () => console.log(`http://localhost:${port}`));

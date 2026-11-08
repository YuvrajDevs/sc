// Sends a first-time visitor on an English page to the same page in their language, when it exists.
// Order: the language they picked in the menu (sc_lang cookie), then their browser's languages,
// then the country Vercel reports. Search engine bots are never redirected, so every language stays indexed.

export const config = { matcher: ["/((?!assets/|css/|js/|.*\\.[a-z0-9]+$).*)"] };

const CODES = ["es", "pt-br", "id", "bn", "ar", "tr", "de", "vi", "ko", "ja"];
const COUNTRY = {
  ID: "id", BR: "pt-br", BD: "bn", TR: "tr", DE: "de", AT: "de", CH: "de", VN: "vi", KR: "ko", JP: "ja",
  ...Object.fromEntries("MX ES AR CO CL PE VE EC GT CU BO DO HN PY SV NI CR PA UY".split(" ").map((c) => [c, "es"])),
  ...Object.fromEntries("SA EG AE IQ MA DZ JO KW QA OM BH LB LY TN SY YE SD".split(" ").map((c) => [c, "ar"])),
};
const BOT = /bot|crawl|spider|slurp|preview|facebookexternalhit|whatsapp|telegram|lighthouse|headless|curl|wget/i;
const PREFIX = new RegExp(`^/(${CODES.join("|")})(/|$)`);

// "pt-BR" -> "pt-br", "pt" -> "pt-br", "es-419" -> "es", "en-IN" -> "en"; unsupported -> null.
function fromTag(tag) {
  const t = tag.trim().toLowerCase(), base = t.split("-")[0];
  if (base === "en") return "en";
  if (base === "pt") return "pt-br";
  return CODES.includes(base) ? base : null;
}

export function pickLang(request) {
  const cookie = (request.headers.get("cookie") || "").match(/(?:^|;\s*)sc_lang=([a-z-]+)/);
  if (cookie) return cookie[1] === "en" || CODES.includes(cookie[1]) ? cookie[1] : "en";
  const accept = (request.headers.get("accept-language") || "").split(",")
    .map((p) => { const [tag, q] = p.split(";q="); return { tag, q: q ? Number(q) : 1 }; })
    .filter((x) => x.tag && x.tag.trim() !== "*").sort((a, b) => b.q - a.q);
  for (const { tag } of accept) { const l = fromTag(tag); if (l) return l; }
  return COUNTRY[(request.headers.get("x-vercel-ip-country") || "").toUpperCase()] || "en";
}

export default async function middleware(request) {
  if (request.method !== "GET") return;
  const url = new URL(request.url);
  if (PREFIX.test(url.pathname)) return;                       // already on a translated page
  if (BOT.test(request.headers.get("user-agent") || "")) return;
  if (!(request.headers.get("accept") || "").includes("text/html")) return;
  const lang = pickLang(request);
  if (lang === "en") return;

  const target = new URL(`/${lang}${url.pathname === "/" ? "/" : url.pathname}`, url);
  target.search = url.search;
  try {
    const head = await fetch(target, { method: "HEAD", redirect: "manual" });
    if (head.status !== 200) return;                           // not translated yet: stay in English
  } catch { return; }
  return new Response(null, { status: 302, headers: { Location: target.toString(), "Cache-Control": "private, no-store", Vary: "Accept-Language, Cookie" } });
}

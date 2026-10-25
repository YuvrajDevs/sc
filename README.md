# Sealcloak website

Static marketing site for Sealcloak, the offline photo and file vault for Android.

## Structure

- `content/`: the source of every page. Edit these, never the generated `.html` files in the root.
- `content/guides/`: SEO articles, one per target keyword.
- `css/site.css`, `js/site.js`: shared styles and scripts. The colours are the app's own.
- `build.mjs`: wraps each content file in the shared header and footer. It also writes the guide lists, `sitemap.xml` and `robots.txt`.
- `site.json`: the site URL and the Google Play link.

```bash
node build.mjs     # build
node serve.mjs     # preview at http://localhost:4321
```

The repo root is the website, so it can be served as-is by GitHub Pages, Netlify or Cloudflare Pages. Run `node build.mjs` and commit the output before pushing.

## Adding a guide (the SEO routine)

The plan: publish one high-quality article every 1–2 days, each aimed at one keyword people actually search for. Then keep improving the pages that are close to the top.

1. **Pick a keyword.** Check Google Search Console ("Queries") and Google Trends for phrases related to hiding or locking photos, files and apps on Android. Prefer specific phrases with clear intent, like "hide photos on samsung" or "app lock with fingerprint".
2. **Copy an existing guide** in `content/guides/` and rename it after the keyword, for example `hide-photos-on-samsung.html`.
3. **Fill in the meta block:**
   - `title`: the keyword near the start, under 60 characters
   - `description`: under 155 characters
   - `keyword`, `summary`, `date` (YYYY-MM-DD) and `readMins`
4. **Write it properly.**
   - Answer the question in the first paragraph.
   - Use clear H2 headings.
   - Be honest, including about other ways to do it.
   - Mention Sealcloak once in a callout.
   - Link to 2 or 3 related guides and to a main page (features, security or pricing). Internal links pass ranking strength between pages.
5. Run `node build.mjs`, then commit and push. The guide appears on the Guides page, on the home page (if it's one of the latest 3), in the footer, and in the sitemap.

**Every week:** in Search Console, find pages ranking around positions 8–50 for a keyword. Improve those pages: answer the question better, add a missing section, update the date in `updated`, and add links to them from newer guides. Lifting a page from position 53 to the first page is often easier than ranking a new one.

## Before launch

- Set the real domain in `site.json`, then rebuild.
- Make sure the Play link works once the listing is live.
- Set up the contact email used on the privacy page (`hello@sealcloak.app`).
- Submit `sitemap.xml` in Google Search Console.

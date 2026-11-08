# Translation routine

The site runs in English plus the 10 languages in `i18n/langs.json`: Spanish (es), Portuguese for Brazil (pt-br), Indonesian (id), Bengali (bn), Arabic (ar), Turkish (tr), German (de), Vietnamese (vi), Korean (ko) and Japanese (ja).

English pages live in `content/`. A translation lives at the same path under `content/<code>/`. For example, `content/guides/gallery-lock-android.html` translates to `content/es/guides/gallery-lock-android.html`. The build creates `/es/guides/gallery-lock-android` from it. Until a page is translated, links to it fall back to the English page, so nothing is ever broken.

Interface text (menus, buttons, footer, install card) is in `i18n/ui/<code>.json`. Don't edit it unless asked.

## 1. See what needs doing

```bash
node seo/translation-status.mjs            # every language
node seo/translation-status.mjs es de      # just these
node seo/translation-status.mjs --json es  # full list, with the hash each page needs
```

Statuses:
- **missing:** no translation yet.
- **stale:** the English page changed after it was translated. Re-translate it from the current English version.

Work in the order listed: the home page and main pages first, then features, tools, guides and the rest.

## 2. Translate one page

1. Read the English page in full.
2. Write the translation to `content/<code>/<same path>`. Then:
   - **Translate:** every visible word, including `title`, `navTitle`, `description`, `keyword`, `alsoTargets`, `summary`, every `faq` question and answer, and every `steps` item.
   - **Keep exactly as in English:** `nav`, `date`, `updated`, `order`, `readMins`, `root`, `noindex`, all HTML tags and attributes (`class`, `id`, `href`, `src`, `style`, `alt=""` stays empty), and every placeholder: `{{root}}`, `{{play}}`, `{{cta}}`, `{{faq}}`, `{{related}}`, `{{email}}`, `{{latestGuides}}`, `{{allGuides}}` and the like.
   - **Add `"sourceHash"`** to the meta. The status script and the check both print the value it needs.
3. Run the check and fix every FAIL until it passes:

```bash
node seo/check-translation.mjs content/<code>/<path>.html
```

## How to translate well

- **Write the way people in that country search and talk.** Don't translate word for word. A Spanish speaker searches "ocultar fotos en Android", not a literal rendering of the English phrase. Make `keyword`, `title` and the headings match real local search wording.
- **Brazilian Portuguese is not European Portuguese.** Use "celular", "baixar" and "você".
- **Use the phone's own menu names in that language** where you know them. For example, Samsung Spanish "Carpeta segura", German "Sicherer Ordner", Japanese "セキュリティフォルダ". If you're not sure, keep the English name in quotes after the translated description.
- **Keep untranslated:**
  - the names Sealcloak, Google Play, Android and Coerce
  - the word PERMIT, which the user types in the app
  - AES-256-GCM, Argon2id and Android Keystore
  - phone brands and model names, and other apps' names
- **Keep every number exactly:** prices ($1.49, ₹49…), limits (100 photos, 10 videos), counts (9 words, 5×5, 6 dots, 4 to 8 digits), dates and durations. You may use local number formatting only if the digits stay the same.
- **Tone:** plain, calm and friendly, matching the English. Use the polite "you" (usted is not needed for Spanish; Latin American "tú" is fine). Use German "du" to match the app's casual tone. Use Japanese です/ます and Korean 해요체.
- **Arabic** reads right to left, and the build handles the layout. Write natural Modern Standard Arabic.
- **Never add claims** that aren't in the English page, and never drop a sentence.

## 3. Build and publish

```bash
node build.mjs
```

Make sure the build succeeds. Then commit only the files under `content/<code>/` with the message `Translate (<code>): <pages>`, and push to `main`. If the push is rejected because someone else pushed, run `git pull --rebase` and push again. Generated files in `public/` are never committed: Vercel builds them.

## 4. Report

End with the languages and pages you translated, and anything that blocked you.

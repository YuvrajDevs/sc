# Daily article routine

The scheduled agent runs this once a day in this repo. It publishes one new article aimed at something people are searching for right now. Follow every step in order. Do not skip the check.

## 1. See what people are searching for

```bash
node seo/collect.mjs
```

This asks Google and Bing autocomplete about a few hundred phrases around hiding and locking photos, files and apps on Android. It writes `seo/keywords.json`: a ranked `queue` of topics no page covers yet, each with a `type` (`guide` or `compare`) and close `variants`.

## 2. Pick today's topic

Take the highest-scoring item in `queue` that meets all of these:

- **Someone on Android with private photos or files would search it**, and Sealcloak can honestly help them. Skip topics about other platforms, social media privacy, piracy or adult content.
- **It's specific enough for one clear page.** For a broad head term such as "gallery lock", write the page that best answers it, for example "Gallery lock on Android: every way to lock your photos".
- **It isn't already in `seo/published.json`.**
- **Rotate the page types:** about one day in four, prefer a `compare` topic (another vault app vs Sealcloak, or "X alternative"). About one day in four, prefer a `scenario` (a real situation, such as someone going through your phone or handing it in for repair). About one day in four, prefer a phone-brand topic (Samsung, Redmi, Vivo, Realme, OnePlus…), because those searches are specific and have less competition. Look at the last entries in `seo/published.json` and pick the type that has been missing longest.

Use the topic's `variants` as `alsoTargets` and as natural phrasing in headings and FAQs.

## 3. Research before writing

- Read `seo/facts.json`. It's the only source for what Sealcloak does. Never claim anything that isn't in it, and respect `notTrue`. Never mention what Sealcloak costs: no prices, plan lengths or trials.
- Read two existing articles in `content/guides/` for tone and to find pages to link.
- **Get phone-specific steps right.** For menu paths on a brand's phone, for example Samsung Secure Folder or Xiaomi Hidden album, check the maker's current help pages with web search, and write the path as the maker describes it. If you can't confirm a path, describe it more generally instead of guessing.
- **Claims that something was removed, discontinued or changed need proof.** Use at least one dated source from the last 12 months, ideally the maker's own page. Old news about a beta feature being pulled doesn't count. If you can't confirm a claim, leave it out.
- **Get competitor facts right.** For another app, use its Play Store listing and its own site: account requirement, cloud, permissions. Comparison pages promote Sealcloak: don't write sections praising the other app; show its real weak points (from its listing and data safety section) and every Sealcloak capability that answers them. Never invent facts about another app.

## 4. Write the article

Copy the template for the type: `seo/template-guide.html` → `content/guides/<slug>.html`, `seo/template-compare.html` → `content/compare/<slug>.html`, or `seo/template-scenario.html` → `content/scenarios/<slug>.html`. Make `<slug>` the keyword in lowercase words joined by hyphens, with no stop-word clutter, for example `hide-photos-on-samsung`.

**What makes it rank:**
- **Answer first.** The `answer` box has the full answer in 2–4 sentences before any heading.
- **Keyword placement.** The keyword goes in the title, the h1 and the first lines, written naturally.
- **Length and structure.** Aim for 1,400–2,000 words of real substance, with at least 4 `<h2>` sections. Include numbered steps (`<ol>`) for how-to topics and a comparison table for "which/best/vs" topics. Put each table in `<div class="table-wrap">`.
- **FAQ.** At least 4 FAQs in `meta.faq`, taken from the variants and related questions people ask. Put the steps in `meta.steps` when the page has a main procedure.
- **Internal links.** Link 2–4 other articles, at least one main page, and the feature page that fits (for example `{{root}}features/intruder-photos`) (`{{root}}features`, `{{root}}security`, `{{root}}pricing`, `{{root}}how-it-works`, `{{root}}faq`). Links look like `<a href="{{root}}guides/hide-apps-on-android">`.
- **Placeholders.** Put `{{cta}}` once in the middle, after the reader has the answer, never before it. Keep `{{faq}}` at the end of the prose and `{{related}}` after it.

**What makes it trustworthy:**
- **Be useful even to someone who never installs Sealcloak.** Cover the built-in and free ways honestly, and say their limits.
- **Mention Sealcloak only where it genuinely fits.** That's usually in the comparison table, one short section, and the CTA. No hype words ("ultimate", "unhackable", "military-grade").
- **Write plainly.** Use short sentences, real menu names and concrete numbers. Use British-neutral spelling and avoid em dashes.
- **Scenario pages are written for someone worried, sometimes in danger.** Be calm and practical. Put their safety first. Where it applies (abuse, blackmail, stalking), point to real help such as local emergency numbers or a trusted person, and never suggest anything illegal, like secretly tracking someone.
- **Date it.** Set `date` to today (YYYY-MM-DD) and make `readMins` about words ÷ 220.

## 5. Check it

```bash
node seo/check.mjs content/guides/<slug>.html
```

Fix every `FAIL` and run it again until it prints `PASS`. Read the warnings and fix any that are real.

## 6. Build and publish

```bash
node build.mjs
```

Make sure the build succeeds. It writes the site to `public/`, which is never committed because Vercel builds it on deploy. Then:
- Add `{"date": "YYYY-MM-DD", "slug": "...", "section": "guides|compare|scenarios", "keyword": "...", "score": N}` to `seo/published.json`.
- Commit the new content file, `seo/keywords.json` and `seo/published.json` with the message `Article: <title>`.
- Push to `main`. If the push is rejected because someone else pushed, run `git pull --rebase` and push again. Vercel deploys in about a minute.

The new article is English only at first. The translation routine (`seo/TRANSLATE.md`) picks it up and translates it into every site language.

## 7. Report

End with three lines: the keyword and why you picked it, the page URL, and the word count. If anything blocked publishing, say what and stop. Don't push a page that hasn't passed the check.


## After publishing
- Make the share image: `python3 seo/og.py` (needs Pillow: `pip install pillow` if missing). Commit the new file in `assets/og/`.
- About two minutes after pushing (once Vercel has deployed), tell Bing and other engines: `node seo/indexnow.mjs <section>/<slug>`.

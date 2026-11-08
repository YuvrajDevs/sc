// Free photo tools. Everything runs in this browser tab: images are decoded, edited and saved on the
// device with <canvas>. Nothing is uploaded. Each tool page has one <div class="tool" data-tool="…">,
// and data-opt carries the page's presets (for example a target size or an output format).
(() => {
  const el = document.querySelector(".tool[data-tool]");
  if (!el) return;
  const kind = el.dataset.tool;
  const opt = JSON.parse(el.dataset.opt || "{}");

  // Interface text in the page's language when the build provides it, English otherwise.
  const T = Object.assign({
    drop: "Drop photos here", dropOne: "Drop a photo here", or: "or", choose: "Choose photos", chooseOne: "Choose a photo",
    stays: "Your photos never leave this device.", download: "Download", downloadAll: "Download all",
    unreadable: "This file couldn't be opened as an image:", working: "Working…", saved: "smaller",
    bigger: "The original was already smaller, so it's kept as it is.",
    target: "Target size (KB)", format: "Format", maxSide: "Longest side", original: "Original",
    same: "Same as original", mode: "Resize by", percent: "Percentage", pixels: "Width and height",
    width: "Width (px)", height: "Height (px)", keep: "Keep proportions", ratio: "Aspect ratio", free: "Free",
    crop: "Download cropped photo", reset: "Reset", undo: "Undo", clear: "Clear all", style: "Style",
    pixelate: "Pixelate", blur: "Blur", strength: "Strength", drawHint: "Drag over each face or detail to hide it.",
    cropHint: "Drag the box to move it, drag a corner to resize, or drag anywhere else to start again.",
    brightness: "Brightness", contrast: "Contrast", saturation: "Colour", auto: "Auto fix",
    country: "Photo size", copies: "photos", sheet: "Download 4×6 in print sheet", photo: "Download photo",
    passportHint: "Fit the head inside the oval: chin at the bottom of it, top of the hair near the top.",
    pageSize: "Page size", fit: "Fit to image", margin: "Margin", none: "None", small: "Small",
    makePdf: "Create PDF", remove: "Remove", pages: "pages",
    qrType: "Type", link: "Link or text", wifi: "Wi-Fi", email: "Email", phone: "Phone", sms: "SMS",
    content: "Link or text", network: "Network name (SSID)", password: "Password", security: "Security",
    hidden: "Hidden network", address: "Email address", subject: "Subject", message: "Message", number: "Phone number",
    size: "Size", colour: "Colour", background: "Background", ecc: "Error correction",
    png: "Download PNG", svg: "Download SVG", qrEmpty: "Type something to make a QR code.", qrTooLong: "That's too much text for one QR code.",
    heicLoading: "Opening HEIC photo…", heicFail: "This browser couldn't open the HEIC photo.",
  }, window.SC_TOOLS || {});

  const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  const node = (html) => { const t = document.createElement("template"); t.innerHTML = html.trim(); return t.content.firstElementChild; };
  const size = (n) => n >= 1048576 ? (n / 1048576).toFixed(2) + " MB" : (n / 1024).toFixed(n < 10240 ? 1 : 0) + " KB";
  const toBlob = (c, type, q) => new Promise((r) => c.toBlob(r, type, q));
  const EXT = { "image/jpeg": "jpg", "image/png": "png", "image/webp": "webp", "application/pdf": "pdf" };
  const rename = (name, suffix, type) => name.replace(/\.[a-z0-9]+$/i, "") + suffix + "." + EXT[type];
  const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
  const ICON = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="3"/><circle cx="9" cy="9" r="2"/><path d="M21 15l-5-5L5 21"/></svg>`;

  // ---- Loading images, including HEIC from iPhones (decoded by a small library, still on this device)
  let heicLib;
  async function decode(file) {
    const isHeic = /hei[cf]$/i.test(file.name) || /hei[cf]/i.test(file.type);
    try {
      return await createImageBitmap(file, { imageOrientation: "from-image" });
    } catch (e) {
      if (!isHeic) {
        // Older browsers: fall back to an <img>
        const url = URL.createObjectURL(file);
        try { const img = new Image(); img.src = url; await img.decode(); return img; } finally { setTimeout(() => URL.revokeObjectURL(url), 1000); }
      }
    }
    heicLib ||= new Promise((ok, bad) => {
      const s = document.createElement("script");
      s.src = "https://cdn.jsdelivr.net/npm/heic2any@0.0.4/dist/heic2any.min.js";
      s.onload = () => ok(window.heic2any); s.onerror = () => bad(new Error(T.heicFail));
      document.head.appendChild(s);
    });
    const lib = await heicLib;
    const out = await lib({ blob: file, toType: "image/jpeg", quality: 0.95 });
    return createImageBitmap(Array.isArray(out) ? out[0] : out);
  }
  const W = (img) => img.width || img.naturalWidth, H = (img) => img.height || img.naturalHeight;

  // Draws an image at a size, stepping down in halves for big reductions so it stays sharp.
  function draw(img, w, h, bg) {
    w = Math.max(1, Math.round(w)); h = Math.max(1, Math.round(h));
    let src = img, sw = W(img), sh = H(img);
    while (sw / 2 > w && sh / 2 > h) {
      const c = document.createElement("canvas"); c.width = Math.round(sw / 2); c.height = Math.round(sh / 2);
      const x = c.getContext("2d"); x.imageSmoothingQuality = "high"; x.drawImage(src, 0, 0, c.width, c.height);
      src = c; sw = c.width; sh = c.height;
    }
    const c = document.createElement("canvas"); c.width = w; c.height = h;
    const x = c.getContext("2d");
    if (bg) { x.fillStyle = bg; x.fillRect(0, 0, w, h); }
    x.imageSmoothingQuality = "high"; x.drawImage(src, 0, 0, w, h);
    return c;
  }

  // ---- Shared pieces of the interface
  function dropZone(multiple, accept, onFiles) {
    const z = node(`<div class="meta-drop">${ICON}
      <p><strong>${esc(opt.drop || (multiple ? T.drop : T.dropOne))}</strong> ${esc(T.or)}</p>
      <label class="btn btn-primary">${esc(opt.choose || (multiple ? T.choose : T.chooseOne))}<input type="file" accept="${accept}" ${multiple ? "multiple" : ""} hidden></label>
      <p class="dim">${esc(opt.hint || T.stays)}</p></div>`);
    const input = z.querySelector("input");
    input.addEventListener("change", () => { const f = [...input.files]; input.value = ""; if (f.length) onFiles(f); });
    ["dragenter", "dragover"].forEach((t) => z.addEventListener(t, (e) => { e.preventDefault(); z.classList.add("over"); }));
    ["dragleave", "drop"].forEach((t) => z.addEventListener(t, (e) => { e.preventDefault(); z.classList.remove("over"); }));
    z.addEventListener("drop", (e) => { const f = [...e.dataTransfer.files].filter((x) => accept === "*/*" || /^image\//.test(x.type) || /\.(hei[cf]|jpe?g|png|webp|gif|bmp|avif)$/i.test(x.name)); if (f.length) onFiles(multiple ? f : f.slice(0, 1)); });
    return z;
  }
  const field = (label, input, cls = "") => `<label class="${cls}"><span>${esc(label)}</span>${input}</label>`;
  const select = (name, options, value) => `<select name="${name}">${options.map(([v, l]) => `<option value="${v}"${String(v) === String(value) ? " selected" : ""}>${esc(l)}</option>`).join("")}</select>`;
  const controls = (html) => { const c = node(`<form class="tool-controls" onsubmit="return false">${html}</form>`); el.appendChild(c); return c; };
  const val = (form, name) => form.elements[name]?.type === "checkbox" ? form.elements[name].checked : form.elements[name]?.value;
  const list = () => { const l = node(`<ul class="meta-results" aria-live="polite"></ul>`); return l; };

  function row(results, file, blob, outName, note) {
    const li = document.createElement("li");
    li.className = "meta-row";
    const url = URL.createObjectURL(blob);
    const thumb = /^image\//.test(blob.type) ? `<img class="thumb" src="${url}" alt="">` : "";
    li.innerHTML = `<div class="row-main">${thumb}<div><strong>${esc(outName)}</strong><p class="dim">${note}</p></div></div>
      <a class="btn btn-primary" href="${url}" download="${esc(outName)}">${esc(T.download)}</a>`;
    results.prepend(li);
  }
  function errorRow(results, file, e) {
    const li = node(`<li class="meta-row"><div><strong>${esc(file.name)}</strong><p class="dim">${esc(kind === "encrypt" ? "Couldn't process this file:" : T.unreadable)} ${esc(e.message || e)}</p></div></li>`);
    results.prepend(li);
  }

  // ---- Batch tools: compress, resize, convert
  function batch(process, formHtml) {
    const form = formHtml ? controls(formHtml) : null;
    const results = list();
    el.prepend(dropZone(true, opt.accept || "image/*,.heic,.heif", async (files) => {
      for (const f of files) {
        try { await process(f, form, results); } catch (e) { errorRow(results, f, e); }
      }
    }));
    el.appendChild(results);
    return form;
  }

  async function compressTo(img, target, type, maxSide) {
    let scale = Math.min(1, maxSide ? maxSide / Math.max(W(img), H(img)) : 1);
    let smallest = null;
    for (let round = 0; round < 10; round++) {
      const c = draw(img, W(img) * scale, H(img) * scale, type === "image/jpeg" ? "#fff" : null);
      let lo = 0.05, hi = 0.92, best = null;
      const top = await toBlob(c, type, hi);
      if (top.size <= target) return top;
      for (let i = 0; i < 7; i++) {
        const mid = (lo + hi) / 2, b = await toBlob(c, type, mid);
        if (b.size <= target) { best = b; lo = mid; } else hi = mid;
        if (!smallest || b.size < smallest.size) smallest = b;
      }
      if (best) return best;
      scale *= 0.8;
    }
    return smallest;
  }

  const FORMATS = [["image/jpeg", "JPEG"], ["image/webp", "WebP"]];
  const TOOLS = {
    compress() {
      batch(async (f, form, results) => {
        const target = Math.max(5, Number(val(form, "target")) || 100) * 1024;
        const type = val(form, "format"), max = Number(val(form, "max")) || 0;
        const img = await decode(f);
        if (f.size <= target && /jpe?g$/i.test(f.name) && type === "image/jpeg" && !max) {
          row(results, f, f, f.name, `${size(f.size)}. ${esc(T.bigger)}`); return;
        }
        const out = await compressTo(img, target, type, max);
        if (f.size <= target && out.size >= f.size && !max) { row(results, f, f, f.name, `${size(f.size)}. ${esc(T.bigger)}`); return; }
        const pct = Math.round((1 - out.size / f.size) * 100);
        row(results, f, out, rename(f.name, `-${Math.round(out.size / 1024)}kb`, type),
          `${size(f.size)} → <strong>${size(out.size)}</strong>${pct > 0 ? ` (${pct}% ${esc(T.saved)})` : ""}`);
      }, field(T.target, `<input name="target" type="number" min="5" step="5" value="${opt.targetKB || 200}" inputmode="numeric">`)
        + field(T.format, select("format", FORMATS, "image/jpeg"))
        + field(T.maxSide, select("max", [[0, T.original], [3000, "3000 px"], [2048, "2048 px"], [1600, "1600 px"], [1280, "1280 px"], [1024, "1024 px"], [800, "800 px"]], 0)));
    },

    resize() {
      const form = batch(async (f, form, results) => {
        const img = await decode(f);
        let w = W(img), h = H(img);
        if (val(form, "mode") === "percent") { const p = clamp(Number(val(form, "percent")) || 50, 1, 1000) / 100; w *= p; h *= p; }
        else {
          const tw = Number(val(form, "w")) || 0, th = Number(val(form, "h")) || 0;
          if (val(form, "keep")) { const s = Math.min(tw ? tw / w : Infinity, th ? th / h : Infinity); if (isFinite(s)) { w *= s; h *= s; } }
          else { w = tw || w; h = th || h; }
        }
        let type = val(form, "format");
        if (type === "same") type = /png$/i.test(f.name) ? "image/png" : /webp$/i.test(f.name) ? "image/webp" : "image/jpeg";
        const c = draw(img, w, h, type === "image/jpeg" ? "#fff" : null);
        const out = await toBlob(c, type, 0.92);
        row(results, f, out, rename(f.name, `-${c.width}x${c.height}`, type), `${W(img)} × ${H(img)} → <strong>${c.width} × ${c.height}</strong> · ${size(out.size)}`);
      }, field(T.mode, select("mode", [["pixels", T.pixels], ["percent", T.percent]], opt.mode || "pixels"))
        + field(T.width, `<input name="w" type="number" min="1" value="${opt.w || 1080}" inputmode="numeric">`)
        + field(T.height, `<input name="h" type="number" min="1" value="${opt.h || ""}" inputmode="numeric">`)
        + field(T.percent, `<input name="percent" type="number" min="1" max="1000" value="50" inputmode="numeric">`)
        + `<label class="check"><input name="keep" type="checkbox" checked> ${esc(T.keep)}</label>`
        + field(T.format, select("format", [["same", T.same], ["image/jpeg", "JPEG"], ["image/png", "PNG"], ["image/webp", "WebP"]], "same")));
      const sync = () => { const p = val(form, "mode") === "percent"; ["w", "h", "keep"].forEach((n) => form.elements[n].closest("label").hidden = p); form.elements.percent.closest("label").hidden = !p; };
      form.addEventListener("change", sync); sync();
    },

    convert() {
      const type = opt.to || "image/jpeg";
      batch(async (f, form, results) => {
        const img = await decode(f);
        const c = draw(img, W(img), H(img), type === "image/jpeg" ? "#fff" : null);
        const out = await toBlob(c, type, 0.92);
        row(results, f, out, rename(f.name, "", type), `${size(f.size)} → <strong>${size(out.size)}</strong> · ${c.width} × ${c.height}`);
      });
    },

    pdf() {
      const items = [];
      const form = controls(field(T.pageSize, select("page", [["a4", "A4"], ["letter", "Letter"], ["fit", T.fit]], opt.page || "a4"))
        + field(T.margin, select("margin", [[0, T.none], [18, T.small], [36, "Normal"]], 18))
        + `<button class="btn btn-primary" name="make" type="button" disabled>${esc(T.makePdf)}</button>`);
      const queue = node(`<ul class="meta-results pdf-queue"></ul>`), results = list();
      const render = () => {
        queue.innerHTML = "";
        items.forEach((it, i) => {
          const li = node(`<li class="meta-row"><div class="row-main"><img class="thumb" src="${it.url}" alt=""><div><strong>${i + 1}. ${esc(it.file.name)}</strong><p class="dim">${it.w} × ${it.h}</p></div></div>
            <div class="row-btns"><button class="icon-btn" type="button" data-a="up" aria-label="Up">↑</button><button class="icon-btn" type="button" data-a="down" aria-label="Down">↓</button><button class="icon-btn" type="button" data-a="del" aria-label="${esc(T.remove)}">×</button></div></li>`);
          li.addEventListener("click", (e) => {
            const a = e.target.closest("button")?.dataset.a; if (!a) return;
            if (a === "del") items.splice(i, 1);
            if (a === "up" && i > 0) items.splice(i - 1, 0, items.splice(i, 1)[0]);
            if (a === "down" && i < items.length - 1) items.splice(i + 1, 0, items.splice(i, 1)[0]);
            render();
          });
          queue.appendChild(li);
        });
        form.elements.make.disabled = !items.length;
        form.elements.make.textContent = items.length ? `${T.makePdf} (${items.length} ${T.pages})` : T.makePdf;
      };
      el.prepend(dropZone(true, "image/*,.heic,.heif", async (files) => {
        for (const f of files) {
          try { const img = await decode(f); items.push({ file: f, img, w: W(img), h: H(img), url: URL.createObjectURL(f) }); } catch (e) { errorRow(results, f, e); }
        }
        render();
      }));
      el.appendChild(queue); el.appendChild(results);
      form.elements.make.addEventListener("click", async () => {
        form.elements.make.disabled = true; form.elements.make.textContent = T.working;
        const page = val(form, "page"), margin = Number(val(form, "margin"));
        const pages = [];
        for (const it of items) {
          const s = Math.min(1, 2400 / Math.max(it.w, it.h));
          const c = draw(it.img, it.w * s, it.h * s, "#fff");
          const jpg = new Uint8Array(await (await toBlob(c, "image/jpeg", 0.88)).arrayBuffer());
          let pw, ph;
          if (page === "fit") { pw = c.width * 72 / 150 + margin * 2; ph = c.height * 72 / 150 + margin * 2; }
          else { [pw, ph] = page === "letter" ? [612, 792] : [595.28, 841.89]; if (c.width > c.height) [pw, ph] = [ph, pw]; }
          pages.push({ jpg, w: c.width, h: c.height, pw, ph, margin });
        }
        const blob = makePdf(pages);
        row(results, items[0].file, blob, (items.length === 1 ? items[0].file.name.replace(/\.[a-z0-9]+$/i, "") : "photos") + ".pdf", `${items.length} ${esc(T.pages)} · ${size(blob.size)}`);
        render();
      });
    },

    crop() { editor("crop"); },
    passport() { editor("passport"); },
    blur() { editor("blur"); },
    brighten() { brighten(); },
    qr() { qr(); },
    password() { password(); },
    encrypt() { encrypt(); },
  };

  // ---- Password generator: crypto.getRandomValues, with rejection sampling so every character is equally likely.
  function password() {
    const form = controls(field("Type", select("kind", [["chars", "Random characters"], ["words", "Passphrase (words)"]], opt.kind || "chars"))
      + field("Length", `<input name="len" type="number" min="8" max="128" value="20" inputmode="numeric">`, "f-chars")
      + `<label class="check f-chars"><input name="upper" type="checkbox" checked> A–Z</label><label class="check f-chars"><input name="lower" type="checkbox" checked> a–z</label>`
      + `<label class="check f-chars"><input name="digits" type="checkbox" checked> 0–9</label><label class="check f-chars"><input name="symbols" type="checkbox" checked> !@#$</label>`
      + `<label class="check f-chars"><input name="clear" type="checkbox"> No look-alikes (0O1lI)</label>`
      + field("Words", `<input name="words" type="number" min="3" max="12" value="5" inputmode="numeric">`, "f-words")
      + field("Separator", select("sep", [["-", "Hyphen -"], [" ", "Space"], [".", "Dot ."], ["", "None"]], "-"), "f-words"));
    const out = node(`<div class="pw-out"><output class="pw-value" aria-live="polite"></output><p class="dim pw-strength"></p>
      <div class="tool-actions"><button class="btn btn-primary" type="button" data-a="copy">Copy</button><button class="btn btn-ghost" type="button" data-a="new">New password</button></div></div>`);
    el.appendChild(out);
    const rand = (n) => { const lim = Math.floor(4294967296 / n) * n, a = new Uint32Array(1); do crypto.getRandomValues(a); while (a[0] >= lim); return a[0] % n; };
    let words = null;
    const loadWords = () => words ||= fetch("/js/words.json").then((r) => r.json());
    async function make() {
      const k = val(form, "kind");
      form.querySelectorAll(".f-chars,.f-words").forEach((l) => { l.hidden = !l.classList.contains("f-" + k); });
      let pw, bits;
      if (k === "words") {
        const list = await loadWords(), n = clamp(Number(val(form, "words")) || 5, 3, 12);
        pw = Array.from({ length: n }, () => list[rand(list.length)]).join(val(form, "sep")); bits = n * Math.log2(list.length);
      } else {
        let sets = [val(form, "upper") && "ABCDEFGHIJKLMNOPQRSTUVWXYZ", val(form, "lower") && "abcdefghijklmnopqrstuvwxyz", val(form, "digits") && "0123456789", val(form, "symbols") && "!@#$%^&*()-_=+[]{};:,.?/"].filter(Boolean);
        if (!sets.length) sets = ["abcdefghijklmnopqrstuvwxyz"];
        if (val(form, "clear")) sets = sets.map((s) => s.replace(/[0O1lI]/g, ""));
        const all = sets.join(""), n = clamp(Number(val(form, "len")) || 20, 8, 128);
        // One from each chosen set, the rest from all, then shuffled
        const chars = sets.map((s) => s[rand(s.length)]);
        while (chars.length < n) chars.push(all[rand(all.length)]);
        for (let i = chars.length - 1; i > 0; i--) { const j = rand(i + 1); [chars[i], chars[j]] = [chars[j], chars[i]]; }
        pw = chars.join(""); bits = n * Math.log2(all.length);
      }
      out.querySelector(".pw-value").textContent = pw;
      const label = bits >= 100 ? "Very strong" : bits >= 64 ? "Strong" : bits >= 50 ? "Fair" : "Weak";
      out.querySelector(".pw-strength").textContent = `${label} · about ${Math.round(bits)} bits of randomness`;
    }
    out.addEventListener("click", async (e) => {
      const a = e.target.closest("button")?.dataset.a; if (!a) return;
      if (a === "new") return make();
      try { await navigator.clipboard.writeText(out.querySelector(".pw-value").textContent); e.target.textContent = "Copied"; setTimeout(() => e.target.textContent = "Copy", 1500); } catch {}
    });
    form.addEventListener("input", make); form.addEventListener("change", make);
    make();
  }

  // ---- Encrypt or decrypt any file with a password: PBKDF2-SHA256 (600,000 rounds) and AES-256-GCM, via Web Crypto.
  // File layout: "SCLOCK1" (7 bytes) · salt (16) · iv (12) · ciphertext with GCM tag. The original name is stored inside the encrypted part.
  function encrypt() {
    const MAGIC = new TextEncoder().encode("SCLOCK1");
    const form = controls(field("Password", `<input name="pw" type="password" autocomplete="new-password" minlength="8">`, "grow")
      + `<label class="check"><input name="show" type="checkbox"> Show</label>`);
    form.elements.show.addEventListener("change", () => form.elements.pw.type = form.elements.show.checked ? "text" : "password");
    const results = list();
    const key = async (pw, salt) => crypto.subtle.deriveKey({ name: "PBKDF2", hash: "SHA-256", salt, iterations: 600000 },
      await crypto.subtle.importKey("raw", new TextEncoder().encode(pw), "PBKDF2", false, ["deriveKey"]), { name: "AES-GCM", length: 256 }, false, ["encrypt", "decrypt"]);
    el.prepend(dropZone(true, "*/*", async (files) => {
      const pw = val(form, "pw");
      if (pw.length < 8) { form.elements.pw.focus(); form.elements.pw.reportValidity?.(); results.prepend(node(`<li class="meta-row"><p class="dim">Type a password of at least 8 characters first.</p></li>`)); return; }
      for (const f of files) {
        try {
          const buf = new Uint8Array(await f.arrayBuffer());
          const locked = buf.length > 35 && MAGIC.every((b, i) => buf[i] === b);
          if (locked) {
            const salt = buf.slice(7, 23), iv = buf.slice(23, 35);
            let plain;
            try { plain = new Uint8Array(await crypto.subtle.decrypt({ name: "AES-GCM", iv }, await key(pw, salt), buf.slice(35))); }
            catch { throw new Error("wrong password, or the file was changed"); }
            const nl = new DataView(plain.buffer).getUint16(0), name = new TextDecoder().decode(plain.slice(2, 2 + nl));
            row(results, f, new Blob([plain.slice(2 + nl)]), name, `Decrypted · ${size(plain.length - 2 - nl)}`);
          } else {
            const salt = crypto.getRandomValues(new Uint8Array(16)), iv = crypto.getRandomValues(new Uint8Array(12));
            const name = new TextEncoder().encode(f.name.slice(0, 200)), head = new Uint8Array(2 + name.length);
            new DataView(head.buffer).setUint16(0, name.length); head.set(name, 2);
            const plain = new Uint8Array(head.length + buf.length); plain.set(head); plain.set(buf, head.length);
            const ct = new Uint8Array(await crypto.subtle.encrypt({ name: "AES-GCM", iv }, await key(pw, salt), plain));
            const blob = new Blob([MAGIC, salt, iv, ct], { type: "application/octet-stream" });
            row(results, f, blob, f.name + ".locked", `Encrypted with AES-256-GCM · ${size(blob.size)}`);
          }
        } catch (e) { errorRow(results, f, e); }
      }
    }));
    el.appendChild(results);
  }

  // ---- A small PDF writer: one JPEG per page, centred inside the margins
  function makePdf(pages) {
    const enc = new TextEncoder(), parts = [], offs = [];
    let len = 0;
    const push = (x) => { const b = typeof x === "string" ? enc.encode(x) : x; parts.push(b); len += b.length; };
    const obj = (id, fn) => { offs[id] = len; push(`${id} 0 obj\n`); fn(); push("\nendobj\n"); };
    const f = (n) => n.toFixed(2);
    push("%PDF-1.4\n");
    obj(1, () => push("<< /Type /Catalog /Pages 2 0 R >>"));
    obj(2, () => push(`<< /Type /Pages /Count ${pages.length} /Kids [${pages.map((_, i) => `${3 + 3 * i} 0 R`).join(" ")}] >>`));
    pages.forEach((p, i) => {
      const id = 3 + 3 * i;
      const aw = p.pw - p.margin * 2, ah = p.ph - p.margin * 2, s = Math.min(aw / p.w, ah / p.h);
      const dw = p.w * s, dh = p.h * s, x = (p.pw - dw) / 2, y = (p.ph - dh) / 2;
      const content = `q ${f(dw)} 0 0 ${f(dh)} ${f(x)} ${f(y)} cm /Im0 Do Q`;
      obj(id, () => push(`<< /Type /Page /Parent 2 0 R /MediaBox [0 0 ${f(p.pw)} ${f(p.ph)}] /Resources << /XObject << /Im0 ${id + 2} 0 R >> >> /Contents ${id + 1} 0 R >>`));
      obj(id + 1, () => push(`<< /Length ${content.length} >>\nstream\n${content}\nendstream`));
      obj(id + 2, () => { push(`<< /Type /XObject /Subtype /Image /Width ${p.w} /Height ${p.h} /ColorSpace /DeviceRGB /BitsPerComponent 8 /Filter /DCTDecode /Length ${p.jpg.length} >>\nstream\n`); push(p.jpg); push("\nendstream"); });
    });
    const xref = len, total = 3 + 3 * pages.length;
    push(`xref\n0 ${total}\n0000000000 65535 f \n`);
    for (let id = 1; id < total; id++) push(String(offs[id]).padStart(10, "0") + " 00000 n \n");
    push(`trailer\n<< /Size ${total} /Root 1 0 R >>\nstartxref\n${xref}\n%%EOF\n`);
    return new Blob(parts, { type: "application/pdf" });
  }

  // ---- Single-photo editors: crop, passport photo, blur faces
  const PASSPORT = {
    us: ["US passport and visa (2 × 2 in)", 51, 51], in: ["India passport (35 × 45 mm)", 35, 45], uk: ["UK passport (35 × 45 mm)", 35, 45],
    eu: ["Schengen visa and EU passports (35 × 45 mm)", 35, 45], ca: ["Canada passport (50 × 70 mm)", 50, 70], au: ["Australia passport (35 × 45 mm)", 35, 45],
    cn: ["China visa (33 × 48 mm)", 33, 48], jp: ["Japan passport (35 × 45 mm)", 35, 45], id: ["Indonesia (4 × 6 cm)", 40, 60],
    br: ["Brazil (5 × 7 cm)", 50, 70], my: ["Malaysia passport (35 × 50 mm)", 35, 50], ph: ["Philippines passport (35 × 45 mm)", 35, 45],
  };
  const RATIOS = [["free", T.free], ["1", "1:1"], ["0.8", "4:5"], ["1.7778", "16:9"], ["0.5625", "9:16"], ["1.5", "3:2"], ["0.6667", "2:3"], ["1.3333", "4:3"]];

  function editor(mode) {
    let img = null, rect = null, rects = [], drag = null, aspect = null;
    const stage = node(`<div class="tool-stage" hidden><canvas></canvas></div>`);
    const cv = stage.querySelector("canvas"), ctx = cv.getContext("2d");
    const hint = node(`<p class="dim tool-hint" hidden>${esc(mode === "blur" ? T.drawHint : mode === "passport" ? T.passportHint : T.cropHint)}</p>`);
    let form;
    if (mode === "crop") form = controls(field(T.ratio, select("ratio", RATIOS, opt.ratio || "free")));
    if (mode === "passport") form = controls(field(T.country, select("country", Object.entries(PASSPORT).map(([k, v]) => [k, v[0]]), opt.country || "us"), "grow"));
    if (mode === "blur") form = controls(field(T.style, select("style", [["pixelate", T.pixelate], ["blur", T.blur]], "blur")) + field(T.strength, `<input name="strength" type="range" min="1" max="10" value="6">`));
    const actions = node(`<div class="tool-actions" hidden></div>`);
    const results = list();
    const btn = (label, primary) => { const b = node(`<button class="btn ${primary ? "btn-primary" : "btn-ghost"}" type="button">${esc(label)}</button>`); actions.appendChild(b); return b; };

    el.prepend(dropZone(false, "image/*,.heic,.heif", async ([f]) => {
      try { img = await decode(f); img.fileName = f.name; } catch (e) { errorRow(results, f, e); return; }
      const s = Math.min(1, 1600 / Math.max(W(img), H(img)));
      cv.width = Math.round(W(img) * s); cv.height = Math.round(H(img) * s); cv.scale = s;
      stage.hidden = hint.hidden = actions.hidden = false; rects = [];
      setAspect(); paint();
      stage.scrollIntoView({ behavior: "smooth", block: "center" });
    }));
    el.append(hint, stage, actions, results);

    function setAspect() {
      if (!img) return;
      if (mode === "crop") { const r = val(form, "ratio"); aspect = r === "free" ? null : Number(r); }
      if (mode === "passport") { const p = PASSPORT[val(form, "country")]; aspect = p[1] / p[2]; }
      if (mode === "blur") { rect = null; return; }
      const iw = W(img), ih = H(img);
      let w = iw * 0.8, h = ih * 0.8;
      if (aspect) { if (w / h > aspect) w = h * aspect; else h = w / aspect; }
      rect = { x: (iw - w) / 2, y: (ih - h) / 2, w, h };
    }
    form?.addEventListener("change", () => { if (mode === "blur") paint(); else { setAspect(); paint(); } });
    form?.addEventListener("input", () => mode === "blur" && paint());

    // Hides a region of a canvas: pixelate keeps hard blocks, blur scales down and back up smoothly, twice.
    function hide(c, x, y, w, h, scale) {
      x = Math.round(x); y = Math.round(y); w = Math.round(w); h = Math.round(h);
      if (w < 2 || h < 2) return;
      const k = c.getContext("2d"), strength = Number(val(form, "strength"));
      const block = Math.max(2, (Math.max(w, h) / 60) * strength * 1.4);
      const t = document.createElement("canvas"); t.width = Math.max(1, Math.round(w / block)); t.height = Math.max(1, Math.round(h / block));
      const tc = t.getContext("2d");
      const smooth = val(form, "style") === "blur";
      tc.imageSmoothingEnabled = true; tc.drawImage(c, x, y, w, h, 0, 0, t.width, t.height);
      k.save(); k.beginPath(); k.rect(x, y, w, h); k.clip();
      k.imageSmoothingEnabled = smooth;
      if (smooth) { const t2 = document.createElement("canvas"); t2.width = t.width * 3; t2.height = t.height * 3; const c2 = t2.getContext("2d"); c2.drawImage(t, 0, 0, t2.width, t2.height); k.drawImage(t2, x, y, w, h); }
      else k.drawImage(t, x, y, w, h);
      k.restore();
    }

    function paint() {
      if (!img) return;
      const s = cv.scale;
      ctx.drawImage(img, 0, 0, cv.width, cv.height);
      if (mode === "blur") {
        for (const r of rects) hide(cv, r.x * s, r.y * s, r.w * s, r.h * s);
        if (drag?.draft) { const r = drag.draft; ctx.strokeStyle = "#4FD1D9"; ctx.lineWidth = 2; ctx.setLineDash([6, 4]); ctx.strokeRect(r.x * s, r.y * s, r.w * s, r.h * s); ctx.setLineDash([]); }
        return;
      }
      const r = { x: rect.x * s, y: rect.y * s, w: rect.w * s, h: rect.h * s };
      ctx.fillStyle = "rgba(0,0,0,.55)";
      ctx.fillRect(0, 0, cv.width, r.y); ctx.fillRect(0, r.y + r.h, cv.width, cv.height - r.y - r.h);
      ctx.fillRect(0, r.y, r.x, r.h); ctx.fillRect(r.x + r.w, r.y, cv.width - r.x - r.w, r.h);
      ctx.strokeStyle = "rgba(255,255,255,.9)"; ctx.lineWidth = 2; ctx.strokeRect(r.x, r.y, r.w, r.h);
      ctx.lineWidth = 1; ctx.strokeStyle = "rgba(255,255,255,.35)"; ctx.beginPath();
      for (const t of [1 / 3, 2 / 3]) { ctx.moveTo(r.x + r.w * t, r.y); ctx.lineTo(r.x + r.w * t, r.y + r.h); ctx.moveTo(r.x, r.y + r.h * t); ctx.lineTo(r.x + r.w, r.y + r.h * t); }
      ctx.stroke();
      if (mode === "passport") {
        // Head guide: the head (chin to crown) fills about 50–69% of the height on most passport photos.
        ctx.strokeStyle = "#4FD1D9"; ctx.lineWidth = 2; ctx.setLineDash([8, 6]); ctx.beginPath();
        ctx.ellipse(r.x + r.w / 2, r.y + r.h * 0.45, r.w * 0.27, r.h * 0.31, 0, 0, Math.PI * 2); ctx.stroke(); ctx.setLineDash([]);
      }
      const hs = Math.max(10, cv.width / 70); ctx.fillStyle = "#fff";
      for (const [cx, cy] of [[r.x, r.y], [r.x + r.w, r.y], [r.x, r.y + r.h], [r.x + r.w, r.y + r.h]]) ctx.fillRect(cx - hs / 2, cy - hs / 2, hs, hs);
    }

    // Pointer handling in image coordinates
    const point = (e) => { const b = cv.getBoundingClientRect(); return { x: clamp((e.clientX - b.left) / b.width * W(img), 0, W(img)), y: clamp((e.clientY - b.top) / b.height * H(img), 0, H(img)) }; };
    const grab = () => W(img) / cv.getBoundingClientRect().width * 22;
    cv.addEventListener("pointerdown", (e) => {
      if (!img) return;
      cv.setPointerCapture(e.pointerId);
      const p = point(e);
      if (mode === "blur") { drag = { start: p, draft: { x: p.x, y: p.y, w: 0, h: 0 } }; return; }
      const corners = [[rect.x, rect.y], [rect.x + rect.w, rect.y], [rect.x, rect.y + rect.h], [rect.x + rect.w, rect.y + rect.h]];
      const g = grab(), ci = corners.findIndex(([x, y]) => Math.abs(p.x - x) < g && Math.abs(p.y - y) < g);
      if (ci >= 0) { const [ax, ay] = corners[3 - ci]; drag = { anchor: { x: ax, y: ay } }; }
      else if (p.x > rect.x && p.x < rect.x + rect.w && p.y > rect.y && p.y < rect.y + rect.h) drag = { move: { dx: p.x - rect.x, dy: p.y - rect.y } };
      else drag = { anchor: p };
    });
    cv.addEventListener("pointermove", (e) => {
      if (!drag) return;
      const p = point(e), iw = W(img), ih = H(img);
      if (mode === "blur") { const s = drag.start; drag.draft = { x: Math.min(s.x, p.x), y: Math.min(s.y, p.y), w: Math.abs(p.x - s.x), h: Math.abs(p.y - s.y) }; paint(); return; }
      if (drag.move) { rect.x = clamp(p.x - drag.move.dx, 0, iw - rect.w); rect.y = clamp(p.y - drag.move.dy, 0, ih - rect.h); }
      else {
        const a = drag.anchor, dx = p.x - a.x, dy = p.y - a.y;
        let w = Math.abs(dx), h = Math.abs(dy);
        // Room available from the anchor in the drag direction
        const maxW = dx < 0 ? a.x : iw - a.x, maxH = dy < 0 ? a.y : ih - a.y;
        if (aspect) { if (w / Math.max(h, 1e-6) > aspect) h = w / aspect; else w = h * aspect; const k = Math.min(1, maxW / w, maxH / h); w *= k; h *= k; }
        else { w = Math.min(w, maxW); h = Math.min(h, maxH); }
        w = Math.max(w, 8); h = Math.max(h, 8);
        rect = { x: dx < 0 ? a.x - w : a.x, y: dy < 0 ? a.y - h : a.y, w, h };
      }
      paint();
    });
    const end = () => {
      if (drag?.draft && drag.draft.w > 4 && drag.draft.h > 4) rects.push(drag.draft);
      drag = null; paint();
    };
    cv.addEventListener("pointerup", end); cv.addEventListener("pointercancel", end);

    const base = () => (img.fileName || "photo").replace(/\.[a-z0-9]+$/i, "");
    if (mode === "crop") {
      btn(T.crop, true).addEventListener("click", async () => {
        const type = /png$/i.test(img.fileName) ? "image/png" : "image/jpeg";
        const c = document.createElement("canvas"); c.width = Math.round(rect.w); c.height = Math.round(rect.h);
        const k = c.getContext("2d"); if (type === "image/jpeg") { k.fillStyle = "#fff"; k.fillRect(0, 0, c.width, c.height); }
        k.drawImage(img, rect.x, rect.y, rect.w, rect.h, 0, 0, c.width, c.height);
        const out = await toBlob(c, type, 0.94);
        row(results, null, out, `${base()}-cropped.${EXT[type]}`, `${c.width} × ${c.height} · ${size(out.size)}`);
      });
      btn(T.reset).addEventListener("click", () => { setAspect(); paint(); });
    }
    if (mode === "passport") {
      const photo = () => {
        const [, mw, mh] = PASSPORT[val(form, "country")];
        const c = document.createElement("canvas"); c.width = Math.round(mw / 25.4 * 300); c.height = Math.round(mh / 25.4 * 300);
        const k = c.getContext("2d"); k.fillStyle = "#fff"; k.fillRect(0, 0, c.width, c.height); k.imageSmoothingQuality = "high";
        k.drawImage(img, rect.x, rect.y, rect.w, rect.h, 0, 0, c.width, c.height);
        return { c, mw, mh };
      };
      btn(T.photo, true).addEventListener("click", async () => {
        const { c, mw, mh } = photo(); const out = await toBlob(c, "image/jpeg", 0.95);
        row(results, null, out, `${base()}-passport-${mw}x${mh}mm.jpg`, `${mw} × ${mh} mm · ${c.width} × ${c.height} px at 300 dpi · ${size(out.size)}`);
      });
      btn(T.sheet).addEventListener("click", async () => {
        // 6 × 4 inches at 300 dpi, as many copies as fit with a 3 mm gap and thin cut lines
        const { c, mw, mh } = photo(); const S = document.createElement("canvas"); S.width = 1800; S.height = 1200;
        const k = S.getContext("2d"); k.fillStyle = "#fff"; k.fillRect(0, 0, S.width, S.height);
        const gap = Math.round(3 / 25.4 * 300), cols = Math.floor((S.width - gap) / (c.width + gap)), rows = Math.floor((S.height - gap) / (c.height + gap));
        const ox = (S.width - (cols * c.width + (cols - 1) * gap)) / 2, oy = (S.height - (rows * c.height + (rows - 1) * gap)) / 2;
        k.strokeStyle = "#bbb"; k.lineWidth = 1;
        for (let i = 0; i < rows; i++) for (let j = 0; j < cols; j++) { const x = ox + j * (c.width + gap), y = oy + i * (c.height + gap); k.drawImage(c, x, y); k.strokeRect(x - 0.5, y - 0.5, c.width + 1, c.height + 1); }
        const out = await toBlob(S, "image/jpeg", 0.95);
        row(results, null, out, `${base()}-passport-sheet-4x6.jpg`, `${cols * rows} ${esc(T.copies)} · ${mw} × ${mh} mm · 6 × 4 in · ${size(out.size)}`);
      });
      btn(T.reset).addEventListener("click", () => { setAspect(); paint(); });
    }
    if (mode === "blur") {
      btn(T.download, true).addEventListener("click", async () => {
        const type = /png$/i.test(img.fileName) ? "image/png" : "image/jpeg";
        const c = document.createElement("canvas"); c.width = W(img); c.height = H(img);
        c.getContext("2d").drawImage(img, 0, 0);
        for (const r of rects) hide(c, r.x, r.y, r.w, r.h);
        const out = await toBlob(c, type, 0.94);
        row(results, null, out, `${base()}-blurred.${EXT[type]}`, `${rects.length} × ${esc(val(form, "style") === "blur" ? T.blur : T.pixelate)} · ${size(out.size)}`);
      });
      btn(T.undo).addEventListener("click", () => { rects.pop(); paint(); });
      btn(T.clear).addEventListener("click", () => { rects = []; paint(); });
    }
  }

  // ---- Brighten a dark photo: gamma for brightness (lifts shadows without blowing out highlights),
  // plus contrast and colour, previewed on a smaller copy and applied to the full-size photo on download.
  function brighten() {
    let img = null;
    const form = controls(field(T.brightness, `<input name="b" type="range" min="-100" max="100" value="0">`, "grow")
      + field(T.contrast, `<input name="c" type="range" min="-100" max="100" value="0">`, "grow")
      + field(T.saturation, `<input name="s" type="range" min="-100" max="100" value="0">`, "grow"));
    const stage = node(`<div class="tool-stage" hidden><canvas></canvas></div>`), cv = stage.querySelector("canvas");
    const actions = node(`<div class="tool-actions" hidden></div>`), results = list();
    let preview = null;
    el.prepend(dropZone(false, "image/*,.heic,.heif", async ([f]) => {
      try { img = await decode(f); img.fileName = f.name; } catch (e) { errorRow(results, f, e); return; }
      const s = Math.min(1, 1400 / Math.max(W(img), H(img)));
      preview = draw(img, W(img) * s, H(img) * s); cv.width = preview.width; cv.height = preview.height;
      stage.hidden = actions.hidden = false; autoFix(); stage.scrollIntoView({ behavior: "smooth", block: "center" });
    }));
    el.append(stage, actions, results);
    function apply(src, dst) {
      const b = Number(val(form, "b")), c = Number(val(form, "c")), s = Number(val(form, "s"));
      const gamma = Math.pow(2, -b / 60), cf = (259 * (c * 1.275 + 255)) / (255 * (259 - c * 1.275)), sf = 1 + s / 100;
      const lut = new Uint8ClampedArray(256);
      for (let i = 0; i < 256; i++) lut[i] = cf * (255 * Math.pow(i / 255, gamma) - 128) + 128;
      const k = dst.getContext("2d"); k.drawImage(src, 0, 0, dst.width, dst.height);
      const d = k.getImageData(0, 0, dst.width, dst.height), p = d.data;
      for (let i = 0; i < p.length; i += 4) {
        let r = lut[p[i]], g = lut[p[i + 1]], bl = lut[p[i + 2]];
        if (sf !== 1) { const l = 0.299 * r + 0.587 * g + 0.114 * bl; r = l + (r - l) * sf; g = l + (g - l) * sf; bl = l + (bl - l) * sf; }
        p[i] = r; p[i + 1] = g; p[i + 2] = bl;
      }
      k.putImageData(d, 0, 0);
    }
    const paint = () => preview && apply(preview, cv);
    function autoFix() {
      const k = preview.getContext("2d"), p = k.getImageData(0, 0, preview.width, preview.height).data;
      let sum = 0, sq = 0, n = 0;
      for (let i = 0; i < p.length; i += 16) { const l = (0.299 * p[i] + 0.587 * p[i + 1] + 0.114 * p[i + 2]) / 255; sum += l; sq += l * l; n++; }
      const mean = sum / n, sd = Math.sqrt(Math.max(0, sq / n - mean * mean));
      // Solve for the gamma that moves the average to about 0.46
      const g = Math.log(0.46) / Math.log(clamp(mean, 0.02, 0.98));
      form.elements.b.value = Math.round(clamp(-60 * Math.log2(g), -100, 100));
      form.elements.c.value = sd < 0.16 ? 18 : sd < 0.22 ? 8 : 0;
      form.elements.s.value = mean < 0.3 ? 12 : 0;
      paint();
    }
    form.addEventListener("input", paint);
    const b1 = node(`<button class="btn btn-primary" type="button">${esc(T.download)}</button>`);
    const b2 = node(`<button class="btn btn-ghost" type="button">${esc(T.auto)}</button>`);
    const b3 = node(`<button class="btn btn-ghost" type="button">${esc(T.reset)}</button>`);
    actions.append(b1, b2, b3);
    b2.addEventListener("click", autoFix);
    b3.addEventListener("click", () => { form.elements.b.value = form.elements.c.value = form.elements.s.value = 0; paint(); });
    b1.addEventListener("click", async () => {
      const type = /png$/i.test(img.fileName) ? "image/png" : "image/jpeg";
      const c = document.createElement("canvas"); c.width = W(img); c.height = H(img); apply(img, c);
      const out = await toBlob(c, type, 0.94);
      row(results, null, out, (img.fileName || "photo").replace(/\.[a-z0-9]+$/i, "") + "-brighter." + EXT[type], `${c.width} × ${c.height} · ${size(out.size)}`);
    });
  }

  // ---- QR codes: the text is encoded by a small library loaded into this page; nothing is sent anywhere.
  function qr() {
    const form = controls(field(T.qrType, select("type", [["text", T.link], ["wifi", T.wifi], ["email", T.email], ["tel", T.phone], ["sms", T.sms]], opt.type || "text"))
      + field(T.content, `<textarea name="text" rows="2" placeholder="https://">${esc(opt.text || "")}</textarea>`, "grow wide f-text")
      + field(T.network, `<input name="ssid" type="text" autocomplete="off">`, "f-wifi") + field(T.password, `<input name="pass" type="text" autocomplete="off">`, "f-wifi")
      + field(T.security, select("sec", [["WPA", "WPA/WPA2/WPA3"], ["WEP", "WEP"], ["nopass", T.none]], "WPA"), "f-wifi")
      + `<label class="check f-wifi"><input name="hidden" type="checkbox"> ${esc(T.hidden)}</label>`
      + field(T.address, `<input name="to" type="email" autocomplete="off">`, "f-email") + field(T.subject, `<input name="subject" type="text">`, "f-email")
      + field(T.message, `<textarea name="body" rows="2"></textarea>`, "grow wide f-email f-sms")
      + field(T.number, `<input name="tel" type="tel" autocomplete="off">`, "f-tel f-sms")
      + field(T.size, select("px", [[256, "256 px"], [512, "512 px"], [1024, "1024 px"], [2048, "2048 px"]], 1024))
      + field(T.colour, `<input name="fg" type="color" value="#000000">`) + field(T.background, `<input name="bg" type="color" value="#ffffff">`)
      + field(T.ecc, select("ecc", [["L", "Low (7%)"], ["M", "Medium (15%)"], ["Q", "Quartile (25%)"], ["H", "High (30%)"]], "M")));
    const out = node(`<div class="qr-out"><canvas width="256" height="256" aria-label="QR code"></canvas><p class="dim qr-msg"></p></div>`);
    const cv = out.querySelector("canvas"), msg = out.querySelector(".qr-msg");
    const actions = node(`<div class="tool-actions"><button class="btn btn-primary" type="button" data-f="png">${esc(T.png)}</button><button class="btn btn-ghost" type="button" data-f="svg">${esc(T.svg)}</button></div>`);
    el.append(out, actions);
    let lib, code = null;
    const load = () => lib ||= new Promise((ok, bad) => {
      const s = document.createElement("script"); s.src = "https://cdnjs.cloudflare.com/ajax/libs/qrcode-generator/1.4.4/qrcode.min.js";
      s.onload = () => { window.qrcode.stringToBytes = window.qrcode.stringToBytesFuncs["UTF-8"]; ok(window.qrcode); }; s.onerror = bad; document.head.appendChild(s);
    });
    const wesc = (s) => s.replace(/([\\;,:"])/g, "\\$1");
    function payload() {
      const t = val(form, "type");
      if (t === "wifi") { const ssid = val(form, "ssid"); if (!ssid) return ""; const sec = val(form, "sec"); return `WIFI:T:${sec};S:${wesc(ssid)};${sec === "nopass" ? "" : `P:${wesc(val(form, "pass"))};`}${val(form, "hidden") ? "H:true;" : ""};`; }
      if (t === "email") { const to = val(form, "to"); if (!to) return ""; const q = new URLSearchParams(); if (val(form, "subject")) q.set("subject", val(form, "subject")); if (val(form, "body")) q.set("body", val(form, "body")); const qs = q.toString().replace(/\+/g, "%20"); return `mailto:${to}${qs ? "?" + qs : ""}`; }
      if (t === "tel") { const n = val(form, "tel").replace(/[^\d+]/g, ""); return n ? `tel:${n}` : ""; }
      if (t === "sms") { const n = val(form, "tel").replace(/[^\d+]/g, ""); return n ? `SMSTO:${n}:${val(form, "body")}` : ""; }
      return val(form, "text").trim();
    }
    async function render() {
      const t = val(form, "type");
      form.querySelectorAll("[class*='f-']").forEach((l) => { l.hidden = !l.classList.contains("f-" + t); });
      const text = payload();
      if (!text) { code = null; cv.getContext("2d").clearRect(0, 0, cv.width, cv.height); msg.textContent = T.qrEmpty; actions.hidden = true; return; }
      const q = await load();
      try { code = q(0, val(form, "ecc")); code.addData(text, "Byte"); code.make(); }
      catch { code = null; msg.textContent = T.qrTooLong; actions.hidden = true; return; }
      msg.textContent = ""; actions.hidden = false;
      paint(cv, Math.min(512, Number(val(form, "px"))));
    }
    function paint(c, px) {
      const n = code.getModuleCount(), quiet = 4, cell = px / (n + quiet * 2);
      c.width = c.height = px;
      const k = c.getContext("2d"); k.fillStyle = val(form, "bg"); k.fillRect(0, 0, px, px); k.fillStyle = val(form, "fg");
      for (let r = 0; r < n; r++) for (let col = 0; col < n; col++) if (code.isDark(r, col))
        k.fillRect(Math.floor((col + quiet) * cell), Math.floor((r + quiet) * cell), Math.ceil(cell), Math.ceil(cell));
    }
    function svg() {
      const n = code.getModuleCount(), q = 4, size = n + q * 2; let d = "";
      for (let r = 0; r < n; r++) for (let c = 0; c < n; c++) if (code.isDark(r, c)) d += `M${c + q} ${r + q}h1v1h-1z`;
      return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${size} ${size}" shape-rendering="crispEdges"><rect width="100%" height="100%" fill="${val(form, "bg")}"/><path fill="${val(form, "fg")}" d="${d}"/></svg>`;
    }
    actions.addEventListener("click", async (e) => {
      const f = e.target.closest("button")?.dataset.f; if (!f || !code) return;
      let blob;
      if (f === "png") { const c = document.createElement("canvas"); paint(c, Number(val(form, "px"))); blob = await toBlob(c, "image/png"); }
      else blob = new Blob([svg()], { type: "image/svg+xml" });
      const a = document.createElement("a"); a.href = URL.createObjectURL(blob); a.download = `qr-code.${f}`; a.click();
    });
    form.addEventListener("input", render); form.addEventListener("change", render);
    render();
  }

  TOOLS[kind]?.();
})();

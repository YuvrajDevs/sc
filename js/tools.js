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
    const li = node(`<li class="meta-row"><div><strong>${esc(file.name)}</strong><p class="dim">${esc(/pdf|encrypt|hash/i.test(kind) ? "Couldn't finish:" : T.unreadable)} ${esc(e.message || e)}</p></div></li>`);
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

  // =====================================================================================
  // PDF tools. pdf-lib (editing) and pdf.js (rendering pages to images) are loaded into this
  // page only when needed; the PDF itself is read and written on this device and never uploaded.
  const loadScript = (src) => new Promise((ok, bad) => { const s = document.createElement("script"); s.src = src; s.onload = ok; s.onerror = () => bad(new Error("Couldn't load a needed component. Check your connection and reload.")); document.head.appendChild(s); });
  let pdfLibP, pdfJsP;
  const PDFJS_CDN = "https://cdn.jsdelivr.net/npm/pdfjs-dist@3.11.174/";
  const PDFLib = () => pdfLibP ||= loadScript("https://cdnjs.cloudflare.com/ajax/libs/pdf-lib/1.17.1/pdf-lib.min.js").then(() => window.PDFLib);
  const PDFJS = () => pdfJsP ||= loadScript(PDFJS_CDN + "build/pdf.min.js").then(() => {
    // Workers can't start from another origin, so start a same-origin one that imports the real worker script.
    const w = PDFJS_CDN + "build/pdf.worker.min.js";
    window.pdfjsLib.GlobalWorkerOptions.workerSrc = URL.createObjectURL(new Blob([`importScripts("${w}");`], { type: "text/javascript" }));
    return window.pdfjsLib; });
  const PDF_ICON = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5M9 13h6M9 17h4"/></svg>`;
  const pdfName = (n, suffix) => n.replace(/\.pdf$/i, "") + suffix + ".pdf";
  const pdfBlob = (bytes) => new Blob([bytes], { type: "application/pdf" });
  // "1-3, 5, 8-" -> zero-based page indexes within [0, count)
  function parsePages(spec, count) {
    const out = new Set();
    for (const part of String(spec || "").split(/[,\s]+/).filter(Boolean)) {
      const m = part.match(/^(\d*)\s*-\s*(\d*)$/);
      let a, b;
      if (m) { a = m[1] ? +m[1] : 1; b = m[2] ? +m[2] : count; } else if (/^\d+$/.test(part)) a = b = +part; else throw new Error(`"${part}" isn't a page or range, like 1-3 or 5`);
      for (let i = Math.max(1, a); i <= Math.min(count, b); i++) out.add(i - 1);
    }
    return [...out].sort((x, y) => x - y);
  }
  async function openPdf(file) {
    const L = await PDFLib();
    const bytes = await file.arrayBuffer();
    try { return await L.PDFDocument.load(bytes, { updateMetadata: false }); }
    catch (e) { if (/encrypt/i.test(e.message)) throw new Error("this PDF is password-protected. Remove the password in the app that made it, then try again."); throw new Error("this file doesn't look like a valid PDF."); }
  }
  function pdfDrop(multiple, onFiles) {
    const z = node(`<div class="meta-drop">${PDF_ICON}
      <p><strong>${esc(multiple ? "Drop PDFs here" : "Drop a PDF here")}</strong> ${esc(T.or)}</p>
      <label class="btn btn-primary">${esc(multiple ? "Choose PDFs" : "Choose a PDF")}<input type="file" accept="application/pdf,.pdf" ${multiple ? "multiple" : ""} hidden></label>
      <p class="dim">Your files never leave this device.</p></div>`);
    const input = z.querySelector("input");
    input.addEventListener("change", () => { const f = [...input.files]; input.value = ""; if (f.length) onFiles(f); });
    ["dragenter", "dragover"].forEach((t) => z.addEventListener(t, (e) => { e.preventDefault(); z.classList.add("over"); }));
    ["dragleave", "drop"].forEach((t) => z.addEventListener(t, (e) => { e.preventDefault(); z.classList.remove("over"); }));
    z.addEventListener("drop", (e) => { const f = [...e.dataTransfer.files].filter((x) => /pdf$/i.test(x.type) || /\.pdf$/i.test(x.name)); if (f.length) onFiles(multiple ? f : f.slice(0, 1)); });
    return z;
  }
  const busy = (btn, on, label) => { btn.disabled = on; btn.textContent = on ? T.working : label; };

  Object.assign(TOOLS, {
    // Merge several PDFs into one, in the order you set
    async mergePdf() {
      const items = [];
      const form = controls(`<button class="btn btn-primary" name="go" type="button" disabled>Merge PDFs</button>`);
      const queue = node(`<ul class="meta-results pdf-queue"></ul>`), results = list();
      const render = () => {
        queue.innerHTML = "";
        items.forEach((it, i) => {
          const li = node(`<li class="meta-row"><div class="row-main"><span class="thumb pdf-thumb">PDF</span><div><strong>${i + 1}. ${esc(it.file.name)}</strong><p class="dim">${it.pages} pages · ${size(it.file.size)}</p></div></div>
            <div class="row-btns"><button class="icon-btn" type="button" data-a="up" aria-label="Up">↑</button><button class="icon-btn" type="button" data-a="down" aria-label="Down">↓</button><button class="icon-btn" type="button" data-a="del" aria-label="Remove">×</button></div></li>`);
          li.addEventListener("click", (e) => {
            const a = e.target.closest("button")?.dataset.a; if (!a) return;
            if (a === "del") items.splice(i, 1);
            if (a === "up" && i > 0) items.splice(i - 1, 0, items.splice(i, 1)[0]);
            if (a === "down" && i < items.length - 1) items.splice(i + 1, 0, items.splice(i, 1)[0]);
            render();
          });
          queue.appendChild(li);
        });
        form.elements.go.disabled = items.length < 2;
      };
      el.prepend(pdfDrop(true, async (files) => {
        for (const f of files) { try { const d = await openPdf(f); items.push({ file: f, doc: d, pages: d.getPageCount() }); } catch (e) { errorRow(results, f, e); } }
        render();
      }));
      el.append(queue, results);
      form.elements.go.addEventListener("click", async () => {
        busy(form.elements.go, true, "Merge PDFs");
        try {
          const L = await PDFLib(), out = await L.PDFDocument.create();
          for (const it of items) (await out.copyPages(it.doc, it.doc.getPageIndices())).forEach((p) => out.addPage(p));
          const blob = pdfBlob(await out.save());
          row(results, null, blob, "merged.pdf", `${out.getPageCount()} pages from ${items.length} files · ${size(blob.size)}`);
        } catch (e) { errorRow(results, { name: "merged.pdf" }, e); }
        busy(form.elements.go, false, "Merge PDFs"); form.elements.go.disabled = items.length < 2;
      });
    },

    // Extract pages, or every page as its own file
    async splitPdf() { pageTool("split"); },
    async rotatePdf() { pageTool("rotate"); },
    async deletePdfPages() { pageTool("delete"); },
    async pdfToJpg() { pageTool("images"); },
    async compressPdf() { pageTool("compress"); },
    async pdfMetadata() { pageTool("metadata"); },
    encryptText() { encryptText(); },
    passwordStrength() { passwordStrength(); },
    hash() { hashTool(); },
  });

  function pageTool(mode) {
    let file = null, doc = null;
    const F = {
      split: field("Pages", `<input name="pages" type="text" placeholder="e.g. 1-3, 5" autocomplete="off">`, "grow") + field("Output", select("how", [["one", "Selected pages in one PDF"], ["each", "Every page as its own PDF"]], "one")) + `<button class="btn btn-primary" name="go" type="button" disabled>Split PDF</button>`,
      rotate: field("Rotate", select("deg", [[90, "90° clockwise"], [180, "180°"], [270, "90° anticlockwise"]], 90)) + field("Pages (blank = all)", `<input name="pages" type="text" placeholder="e.g. 2, 4-6" autocomplete="off">`, "grow") + `<button class="btn btn-primary" name="go" type="button" disabled>Rotate PDF</button>`,
      delete: field("Pages to remove", `<input name="pages" type="text" placeholder="e.g. 2, 7-9" autocomplete="off">`, "grow") + `<button class="btn btn-primary" name="go" type="button" disabled>Remove pages</button>`,
      images: field("Quality", select("scale", [[1.5, "Standard (108 dpi)"], [2, "High (144 dpi)"], [3, "Very high (216 dpi)"]], 2)) + field("Format", select("fmt", [["image/jpeg", "JPG"], ["image/png", "PNG"]], "image/jpeg")) + `<button class="btn btn-primary" name="go" type="button" disabled>Convert to images</button>`,
      compress: field("Compression", select("level", [["1.4:0.72", "Recommended"], ["1.1:0.6", "Strong (smaller)"], ["2:0.82", "Light (sharper)"]], "1.4:0.72")) + `<button class="btn btn-primary" name="go" type="button" disabled>Compress PDF</button>`,
      metadata: `<button class="btn btn-primary" name="go" type="button" disabled>Remove metadata</button>`,
    }[mode];
    const LABEL = { split: "Split PDF", rotate: "Rotate PDF", delete: "Remove pages", images: "Convert to images", compress: "Compress PDF", metadata: "Remove metadata" }[mode];
    const form = controls(F), info = node(`<div class="pdf-info" hidden></div>`), results = list();
    el.prepend(pdfDrop(false, async ([f]) => {
      try {
        file = f; doc = await openPdf(f);
        let extra = "";
        if (mode === "metadata") {
          const m = { Title: doc.getTitle(), Author: doc.getAuthor(), Subject: doc.getSubject(), Keywords: doc.getKeywords(), "Made with": doc.getCreator(), Producer: doc.getProducer(), Created: doc.getCreationDate()?.toLocaleString(), Modified: doc.getModificationDate()?.toLocaleString() };
          const found = Object.entries(m).filter(([, v]) => v);
          extra = `<div class="meta-tags">${found.length ? found.map(([k, v]) => `<span class="meta-tag${/Author|Title|Subject/.test(k) ? " warn" : ""}">${esc(k)}: ${esc(String(v).slice(0, 60))}</span>`).join("") : `<span class="meta-tag">No document properties found</span>`}</div>`;
        }
        info.innerHTML = `<div class="meta-row"><div class="row-main"><span class="thumb pdf-thumb">PDF</span><div><strong>${esc(f.name)}</strong><p class="dim">${doc.getPageCount()} page${doc.getPageCount() === 1 ? "" : "s"} · ${size(f.size)}</p>${extra}</div></div></div>`;
        info.hidden = false; form.elements.go.disabled = false;
      } catch (e) { errorRow(results, f, e); }
    }));
    el.append(info, results);
    form.elements.go.addEventListener("click", async () => {
      busy(form.elements.go, true, LABEL);
      try { await run(); } catch (e) { errorRow(results, file, e); }
      busy(form.elements.go, false, LABEL);
    });
    async function run() {
      const L = await PDFLib(), n = doc.getPageCount();
      if (mode === "split") {
        const idx = val(form, "pages").trim() ? parsePages(val(form, "pages"), n) : doc.getPageIndices();
        if (!idx.length) throw new Error("no pages match. Pages run from 1 to " + n + ".");
        if (val(form, "how") === "each") {
          for (const i of idx.slice().reverse()) { const out = await L.PDFDocument.create(); const [p] = await out.copyPages(doc, [i]); out.addPage(p); const b = pdfBlob(await out.save()); row(results, null, b, pdfName(file.name, `-page-${i + 1}`), `Page ${i + 1} · ${size(b.size)}`); }
        } else {
          const out = await L.PDFDocument.create(); (await out.copyPages(doc, idx)).forEach((p) => out.addPage(p));
          const b = pdfBlob(await out.save()); row(results, null, b, pdfName(file.name, "-pages"), `${idx.length} of ${n} pages · ${size(b.size)}`);
        }
      }
      if (mode === "rotate") {
        const idx = val(form, "pages").trim() ? parsePages(val(form, "pages"), n) : doc.getPageIndices();
        const d = Number(val(form, "deg"));
        idx.forEach((i) => { const p = doc.getPage(i); p.setRotation(L.degrees((p.getRotation().angle + d) % 360)); });
        const b = pdfBlob(await doc.save()); doc = await L.PDFDocument.load(await file.arrayBuffer(), { updateMetadata: false });
        row(results, null, b, pdfName(file.name, "-rotated"), `${idx.length} page${idx.length === 1 ? "" : "s"} rotated · ${size(b.size)}`);
      }
      if (mode === "delete") {
        const del = parsePages(val(form, "pages"), n);
        if (!del.length) throw new Error("type the pages to remove, like 2 or 4-6.");
        if (del.length >= n) throw new Error("that would remove every page.");
        const keep = doc.getPageIndices().filter((i) => !del.includes(i));
        const out = await L.PDFDocument.create(); (await out.copyPages(doc, keep)).forEach((p) => out.addPage(p));
        const b = pdfBlob(await out.save()); row(results, null, b, pdfName(file.name, "-edited"), `Removed ${del.length}, kept ${keep.length} pages · ${size(b.size)}`);
      }
      if (mode === "metadata") {
        ["setTitle", "setAuthor", "setSubject", "setCreator", "setProducer"].forEach((fn) => doc[fn](""));
        doc.setKeywords([]); doc.setCreationDate(new Date(0)); doc.setModificationDate(new Date(0));
        const cat = doc.catalog; if (cat.has(L.PDFName.of("Metadata"))) cat.delete(L.PDFName.of("Metadata"));
        // Remove the Info dictionary entirely so nothing is left behind
        doc.context.trailerInfo.Info = undefined;
        const b = pdfBlob(await doc.save({ updateFieldAppearances: false }));
        doc = await L.PDFDocument.load(await file.arrayBuffer(), { updateMetadata: false });
        row(results, null, b, pdfName(file.name, "-clean"), `Title, author, software, dates and XMP metadata removed · ${size(b.size)}`);
      }
      if (mode === "images" || mode === "compress") {
        const J = await PDFJS(), pdf = await J.getDocument({ data: new Uint8Array(await file.arrayBuffer()), standardFontDataUrl: PDFJS_CDN + "standard_fonts/", cMapUrl: PDFJS_CDN + "cmaps/", cMapPacked: true }).promise;
        const [scale, q] = mode === "compress" ? val(form, "level").split(":").map(Number) : [Number(val(form, "scale")), 0.9];
        const type = mode === "compress" ? "image/jpeg" : val(form, "fmt");
        const pages = [];
        for (let step = 1; step <= pdf.numPages; step++) {
          // Results are added to the top of the list, so images are rendered last page first to read in order.
          const i = mode === "images" ? pdf.numPages - step + 1 : step;
          form.elements.go.textContent = `${T.working} ${step}/${pdf.numPages}`;
          const page = await pdf.getPage(i), vp = page.getViewport({ scale });
          const c = document.createElement("canvas"); c.width = Math.ceil(vp.width); c.height = Math.ceil(vp.height);
          const k = c.getContext("2d"); k.fillStyle = "#fff"; k.fillRect(0, 0, c.width, c.height);
          await page.render({ canvasContext: k, viewport: vp }).promise;
          const b = await toBlob(c, type, q);
          if (mode === "images") row(results, null, b, file.name.replace(/\.pdf$/i, "") + `-page-${i}.` + EXT[type], `Page ${i} · ${c.width} × ${c.height} · ${size(b.size)}`);
          else { const base = page.getViewport({ scale: 1 }); pages.push({ jpg: new Uint8Array(await b.arrayBuffer()), w: c.width, h: c.height, pw: base.width, ph: base.height, margin: 0 }); }
        }
        if (mode === "compress") {
          const out = makePdf(pages);
          if (out.size >= file.size) row(results, null, file, file.name, `${size(file.size)}. This PDF is already well compressed, so the original is kept.`);
          else row(results, null, out, pdfName(file.name, "-compressed"), `${size(file.size)} → <strong>${size(out.size)}</strong> (${Math.round((1 - out.size / file.size) * 100)}% ${esc(T.saved)})`);
        }
      }
    }
  }

  // ---- Encrypt or decrypt a short text with a password (AES-256-GCM, PBKDF2-SHA256 600,000 rounds).
  // Output is "sc1." + base64url(salt · iv · ciphertext), so it can be pasted into any chat or email.
  function encryptText() {
    const form = controls(field("Text", `<textarea name="text" rows="5" placeholder="Type a message, or paste an encrypted one starting with sc1." spellcheck="false"></textarea>`, "grow wide")
      + field("Password", `<input name="pw" type="password" autocomplete="new-password">`, "grow")
      + `<label class="check"><input name="show" type="checkbox"> Show</label>`
      + `<button class="btn btn-primary" name="enc" type="button">Encrypt</button><button class="btn btn-ghost" name="dec" type="button">Decrypt</button>`);
    form.elements.show.addEventListener("change", () => form.elements.pw.type = form.elements.show.checked ? "text" : "password");
    const out = node(`<div class="pw-out" hidden><output class="pw-value enc-out"></output><p class="dim pw-strength"></p><div class="tool-actions"><button class="btn btn-primary" type="button" data-a="copy">Copy</button></div></div>`);
    el.appendChild(out);
    const b64 = (u) => btoa(String.fromCharCode(...u)).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
    const unb64 = (s) => Uint8Array.from(atob(s.replace(/-/g, "+").replace(/_/g, "/")), (c) => c.charCodeAt(0));
    const key = async (pw, salt) => crypto.subtle.deriveKey({ name: "PBKDF2", hash: "SHA-256", salt, iterations: 600000 }, await crypto.subtle.importKey("raw", new TextEncoder().encode(pw), "PBKDF2", false, ["deriveKey"]), { name: "AES-GCM", length: 256 }, false, ["encrypt", "decrypt"]);
    const show = (text, note) => { out.hidden = false; out.querySelector(".enc-out").textContent = text; out.querySelector(".pw-strength").textContent = note; };
    form.elements.enc.addEventListener("click", async () => {
      const pw = val(form, "pw"), text = val(form, "text");
      if (!text) return show("", "Type the text you want to encrypt.");
      if (pw.length < 8) return show("", "Use a password of at least 8 characters.");
      const salt = crypto.getRandomValues(new Uint8Array(16)), iv = crypto.getRandomValues(new Uint8Array(12));
      const ct = new Uint8Array(await crypto.subtle.encrypt({ name: "AES-GCM", iv }, await key(pw, salt), new TextEncoder().encode(text)));
      const all = new Uint8Array(28 + ct.length); all.set(salt); all.set(iv, 16); all.set(ct, 28);
      show("sc1." + b64(all), "Encrypted with AES-256-GCM. Share the password a different way, never in the same message.");
    });
    form.elements.dec.addEventListener("click", async () => {
      const pw = val(form, "pw"), text = val(form, "text").trim();
      if (!text.startsWith("sc1.")) return show("", "Paste an encrypted message that starts with sc1.");
      try {
        const all = unb64(text.slice(4)), salt = all.slice(0, 16), iv = all.slice(16, 28);
        const pt = await crypto.subtle.decrypt({ name: "AES-GCM", iv }, await key(pw, salt), all.slice(28));
        show(new TextDecoder().decode(pt), "Decrypted.");
      } catch { show("", "Couldn't decrypt: wrong password, or the message was changed or cut off."); }
    });
    out.addEventListener("click", async (e) => {
      if (e.target.closest("button")?.dataset.a !== "copy") return;
      try { await navigator.clipboard.writeText(out.querySelector(".enc-out").textContent); e.target.textContent = "Copied"; setTimeout(() => e.target.textContent = "Copy", 1500); } catch {}
    });
  }

  // ---- Password strength: estimates guesses from length, character variety and common patterns.
  // Nothing is sent anywhere; the password never leaves this field.
  const COMMON = "123456 password 123456789 12345678 12345 qwerty 1234567 111111 123123 abc123 password1 1234 iloveyou 1q2w3e4r 000000 qwerty123 zaq12wsx dragon sunshine princess letmein 654321 monkey 27653 1qaz2wsx 123321 qwertyuiop superman asdfghjkl 112233 football baseball welcome admin login master hello freedom whatever trustno1 shadow michael charlie jordan liverpool chelsea arsenal india pakistan bangladesh indonesia brasil mexico ferrari samsung google computer internet 987654321 secret starwars pokemon naruto loveyou lovely flower anything 666666 888888 121212 7777777 159753 147258369 mustang killer hunter ranger buster soccer hockey batman thomas andrew daniel jessica ashley nicole tigger summer winter spring autumn".split(" ");
  function passwordStrength() {
    const form = controls(field("Password to check", `<input name="pw" type="password" autocomplete="off" spellcheck="false">`, "grow wide") + `<label class="check"><input name="show" type="checkbox"> Show</label>`);
    form.elements.show.addEventListener("change", () => form.elements.pw.type = form.elements.show.checked ? "text" : "password");
    const out = node(`<div class="pw-out"><div class="meter"><span></span></div><p class="pw-verdict"><strong>Type a password to check it.</strong></p><ul class="pw-notes dim"></ul></div>`);
    el.appendChild(out);
    const human = (s) => s < 1 ? "instantly" : s < 60 ? `${Math.round(s)} seconds` : s < 3600 ? `${Math.round(s / 60)} minutes` : s < 86400 ? `${Math.round(s / 3600)} hours` : s < 31536000 ? `${Math.round(s / 86400)} days` : s < 3.15e9 ? `${Math.round(s / 31536000)} years` : "centuries";
    form.addEventListener("input", () => {
      const pw = val(form, "pw"), notes = [];
      if (!pw) { out.querySelector(".pw-verdict").innerHTML = "<strong>Type a password to check it.</strong>"; out.querySelector(".pw-notes").innerHTML = ""; out.querySelector(".meter span").style.width = "0"; return; }
      let pool = 0;
      if (/[a-z]/.test(pw)) pool += 26; if (/[A-Z]/.test(pw)) pool += 26; if (/\d/.test(pw)) pool += 10; if (/[^a-zA-Z0-9]/.test(pw)) pool += 33;
      let bits = pw.length * Math.log2(Math.max(pool, 1));
      const low = pw.toLowerCase(), base = low.replace(/[^a-z]/g, "").replace(/0/g, "o");
      if (COMMON.includes(low) || COMMON.includes(low.replace(/[\d!@#$%^&*]+$/, ""))) { bits = Math.min(bits, 10); notes.push("It's one of the most common passwords, or one with a number or symbol added. These are guessed first."); }
      if (/(.)\1{2,}/.test(pw)) { bits -= 8; notes.push("Repeated characters (like aaa or 111) make it easier to guess."); }
      if (/(0123|1234|2345|3456|4567|5678|6789|abcd|bcde|qwer|wert|asdf|sdfg|zxcv)/i.test(pw)) { bits -= 10; notes.push("Sequences like 1234, abcd or qwerty are tried early."); }
      if (/(19|20)\d{2}/.test(pw)) { bits -= 6; notes.push("It contains a year. Birthdays and years are common guesses."); }
      if (/^[A-Z][a-z]+\d+[!@#$%]?$/.test(pw)) { bits -= 10; notes.push("A capital first letter, a word, then numbers is the most predictable pattern."); }
      if (pw.length < 12) notes.push("It's short. Aim for at least 16 characters, or 5 random words.");
      if (pool <= 26 && pw.length < 20) notes.push("Mix in other character types, or make it longer.");
      bits = Math.max(Math.min(8, pw.length * 2), bits);
      const offline = Math.pow(2, bits) / 2 / 1e10, online = Math.pow(2, bits) / 2 / 100;
      const [label, pct, col] = bits < 28 ? ["Very weak", 10, "#e5484d"] : bits < 40 ? ["Weak", 30, "#e5484d"] : bits < 60 ? ["Fair", 55, "#d9822b"] : bits < 80 ? ["Strong", 80, "#46a758"] : ["Very strong", 100, "#46a758"];
      const bar = out.querySelector(".meter span"); bar.style.width = pct + "%"; bar.style.background = col;
      out.querySelector(".pw-verdict").innerHTML = `<strong>${label}</strong> · about ${Math.round(bits)} bits. Cracking it from a stolen password database: ${human(offline)}. Guessing it online: ${human(online)}.`;
      out.querySelector(".pw-notes").innerHTML = (notes.length ? notes : ["No common weaknesses found. Make sure you don't use it anywhere else."]).map((n) => `<li>${esc(n)}</li>`).join("");
    });
  }

  // ---- Hash / checksum: SHA-256, SHA-1 and SHA-512 via Web Crypto, MD5 by a small implementation below.
  function md5(bytes) {
    const K = new Uint32Array(64).map((_, i) => Math.floor(Math.abs(Math.sin(i + 1)) * 2 ** 32) >>> 0);
    const S = [7, 12, 17, 22, 5, 9, 14, 20, 4, 11, 16, 23, 6, 10, 15, 21];
    const n = bytes.length, total = (((n + 8) >>> 6) + 1) * 64, m = new Uint8Array(total);
    m.set(bytes); m[n] = 0x80; const dv = new DataView(m.buffer);
    dv.setUint32(total - 8, (n * 8) >>> 0, true); dv.setUint32(total - 4, Math.floor(n / 2 ** 29), true);
    let a0 = 0x67452301, b0 = 0xefcdab89, c0 = 0x98badcfe, d0 = 0x10325476;
    for (let off = 0; off < total; off += 64) {
      let A = a0, B = b0, C = c0, D = d0;
      for (let i = 0; i < 64; i++) {
        let F, g, r = i >> 4;
        if (r === 0) { F = (B & C) | (~B & D); g = i; } else if (r === 1) { F = (D & B) | (~D & C); g = (5 * i + 1) % 16; }
        else if (r === 2) { F = B ^ C ^ D; g = (3 * i + 5) % 16; } else { F = C ^ (B | ~D); g = (7 * i) % 16; }
        F = (F + A + K[i] + dv.getUint32(off + g * 4, true)) >>> 0;
        A = D; D = C; C = B; const s = S[r * 4 + (i % 4)]; B = (B + ((F << s) | (F >>> (32 - s)))) >>> 0;
      }
      a0 = (a0 + A) >>> 0; b0 = (b0 + B) >>> 0; c0 = (c0 + C) >>> 0; d0 = (d0 + D) >>> 0;
    }
    return [a0, b0, c0, d0].map((x) => [0, 8, 16, 24].map((s) => ((x >>> s) & 255).toString(16).padStart(2, "0")).join("")).join("");
  }
  function hashTool() {
    const form = controls(field("Text", `<textarea name="text" rows="3" placeholder="Type or paste text, or choose a file below" spellcheck="false"></textarea>`, "grow wide")
      + field("Compare with (optional)", `<input name="cmp" type="text" placeholder="Paste an expected checksum to verify" autocomplete="off" spellcheck="false">`, "grow wide"));
    const z = node(`<div class="meta-drop">${PDF_ICON}<p><strong>Drop a file here</strong> ${esc(T.or)}</p><label class="btn btn-primary">Choose a file<input type="file" hidden></label><p class="dim">Any file. It's hashed on this device and never uploaded.</p></div>`);
    const out = node(`<div class="hash-out"></div>`);
    el.append(z, out);
    let last = null;
    const hex = (buf) => [...new Uint8Array(buf)].map((b) => b.toString(16).padStart(2, "0")).join("");
    async function compute(bytes, label) {
      last = { bytes, label };
      const res = { "MD5": md5(bytes), "SHA-1": hex(await crypto.subtle.digest("SHA-1", bytes)), "SHA-256": hex(await crypto.subtle.digest("SHA-256", bytes)), "SHA-512": hex(await crypto.subtle.digest("SHA-512", bytes)) };
      const cmp = val(form, "cmp").trim().toLowerCase().replace(/\s/g, "");
      out.innerHTML = `<p class="dim">${esc(label)}</p>` + Object.entries(res).map(([k, v]) => `<div class="hash-row${cmp && cmp === v ? " match" : ""}"><span>${k}</span><code>${v}</code><button class="icon-btn" type="button" data-v="${v}" aria-label="Copy ${k}">⧉</button></div>`).join("")
        + (cmp ? `<p class="${Object.values(res).includes(cmp) ? "ok" : "bad"}"><strong>${Object.values(res).includes(cmp) ? "✓ Match: the file or text is identical." : "✗ No match: the file or text is different, or the checksum is for another algorithm."}</strong></p>` : "");
    }
    form.elements.text.addEventListener("input", () => compute(new TextEncoder().encode(val(form, "text")), "Text · UTF-8"));
    form.elements.cmp.addEventListener("input", () => last && compute(last.bytes, last.label));
    const input = z.querySelector("input");
    const onFile = async (f) => { out.innerHTML = `<p class="dim">${esc(T.working)}</p>`; compute(new Uint8Array(await f.arrayBuffer()), `${f.name} · ${size(f.size)}`); };
    input.addEventListener("change", () => { if (input.files[0]) onFile(input.files[0]); input.value = ""; });
    ["dragenter", "dragover"].forEach((t) => z.addEventListener(t, (e) => { e.preventDefault(); z.classList.add("over"); }));
    ["dragleave", "drop"].forEach((t) => z.addEventListener(t, (e) => { e.preventDefault(); z.classList.remove("over"); }));
    z.addEventListener("drop", (e) => { if (e.dataTransfer.files[0]) onFile(e.dataTransfer.files[0]); });
    out.addEventListener("click", async (e) => { const v = e.target.closest("button")?.dataset.v; if (v) try { await navigator.clipboard.writeText(v); e.target.textContent = "✓"; setTimeout(() => e.target.textContent = "⧉", 1200); } catch {} });
  }

  // ---- Password-protect or unlock a PDF with qpdf (open source, compiled to WebAssembly).
  // The result is a normal PDF that any reader opens; encryption is AES-256 (PDF 2.0 / R6).
  const QPDF_CDN = "https://cdn.jsdelivr.net/npm/@neslinesli93/qpdf-wasm@0.3.1/dist/";
  let qpdfP;
  const qpdfFactory = () => qpdfP ||= loadScript(QPDF_CDN + "qpdf.js").then(() => window.Module);
  async function runQpdf(args, input) {
    const factory = await qpdfFactory();
    let err = "";
    const m = await factory({ locateFile: () => QPDF_CDN + "qpdf.wasm", noInitialRun: true, print: () => {}, printErr: (t) => { err += t + "\n"; } });
    m.FS.writeFile("/in.pdf", input);
    let code;
    try { code = m.callMain(args); } catch (e) { code = typeof e?.status === "number" ? e.status : 2; if (!err) err = String(e?.message || e); }
    // qpdf exits 0 on success and 3 on success with warnings
    return { code, err, out: code === 0 || code === 3 ? (() => { try { return m.FS.readFile("/out.pdf"); } catch { return null; } })() : null };
  }
  function pdfPassword(mode) {
    let file = null;
    const protect = mode === "protect";
    const form = controls(field(protect ? "Password to open the PDF" : "PDF password", `<input name="pw" type="password" autocomplete="${protect ? "new-password" : "current-password"}">`, "grow")
      + (protect ? field("Confirm password", `<input name="pw2" type="password" autocomplete="new-password">`, "grow") : "")
      + `<label class="check"><input name="show" type="checkbox"> Show</label>`
      + (protect ? `<label class="check"><input name="print" type="checkbox" checked> Allow printing</label><label class="check"><input name="copy" type="checkbox" checked> Allow copying text</label><label class="check"><input name="edit" type="checkbox"> Allow editing</label>` : "")
      + `<button class="btn btn-primary" name="go" type="button" disabled>${protect ? "Protect PDF" : "Unlock PDF"}</button>`);
    const LABEL = protect ? "Protect PDF" : "Unlock PDF";
    form.elements.show.addEventListener("change", () => form.querySelectorAll("input[type=password], input[data-pw]").forEach((i) => { i.dataset.pw = 1; i.type = form.elements.show.checked ? "text" : "password"; }));
    const info = node(`<div class="pdf-info" hidden></div>`), results = list();
    el.prepend(pdfDrop(false, async ([f]) => {
      file = f;
      const bytes = new Uint8Array(await f.arrayBuffer());
      if (String.fromCharCode(...bytes.slice(0, 5)) !== "%PDF-") { errorRow(results, f, new Error("this file doesn't look like a PDF.")); return; }
      const enc = /\/Encrypt\s/.test(new TextDecoder("latin1").decode(bytes.slice(Math.max(0, bytes.length - 4096))) + new TextDecoder("latin1").decode(bytes.slice(0, 4096)));
      info.innerHTML = `<div class="meta-row"><div class="row-main"><span class="thumb pdf-thumb">PDF</span><div><strong>${esc(f.name)}</strong><p class="dim">${size(f.size)}${enc ? " · password protected" : ""}</p></div></div></div>`;
      info.hidden = false; form.elements.go.disabled = false;
    }));
    el.append(info, results);
    form.elements.go.addEventListener("click", async () => {
      const pw = val(form, "pw");
      if (protect) {
        if (pw.length < 6) { errorRow(results, file, new Error("use a password of at least 6 characters; 12 or more is better.")); return; }
        if (pw !== val(form, "pw2")) { errorRow(results, file, new Error("the two passwords don't match.")); return; }
      }
      busy(form.elements.go, true, LABEL);
      try {
        const input = new Uint8Array(await file.arrayBuffer());
        let r;
        if (protect) {
          // A random owner password keeps the permission settings enforceable
          const owner = [...crypto.getRandomValues(new Uint8Array(18))].map((b) => b.toString(16).padStart(2, "0")).join("");
          const restrict = [];
          if (!val(form, "print")) restrict.push("--print=none");
          if (!val(form, "copy")) restrict.push("--extract=n");
          if (!val(form, "edit")) restrict.push("--modify=none");
          r = await runQpdf(["--encrypt", pw, owner, "256", ...restrict, "--", "/in.pdf", "/out.pdf"], input);
          if (!r.out) throw new Error("couldn't protect this PDF. If it already has a password, unlock it first. " + (r.err.split("\n")[0] || ""));
          row(results, null, pdfBlob(r.out), pdfName(file.name, "-protected"), `AES-256 password protection · opens in any PDF reader · ${size(r.out.length)}`);
        } else {
          r = await runQpdf(["--password=" + pw, "--decrypt", "/in.pdf", "/out.pdf"], input);
          if (!r.out) throw new Error("the password didn't work. Check it (passwords are case-sensitive) and try again. " + (r.err.split("\n")[0] || ""));
          row(results, null, pdfBlob(r.out), pdfName(file.name, "-unlocked"), `Password removed · ${size(r.out.length)}`);
        }
      } catch (e) { errorRow(results, file, e); }
      busy(form.elements.go, false, LABEL);
    });
  }
  Object.assign(TOOLS, { protectPdf() { pdfPassword("protect"); }, unlockPdf() { pdfPassword("unlock"); } });

  TOOLS[kind.replace(/-(\w)/g, (_, c) => c.toUpperCase())]?.();
})();

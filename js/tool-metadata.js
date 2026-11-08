// Photo location remover. Everything happens in this browser tab: files are read with FileReader,
// cleaned in memory and handed back as downloads. Nothing is uploaded; this page makes no network requests.
//
// JPEG: drops the APP1 (EXIF and XMP), APP13 (IPTC) and COM segments without re-encoding the image,
// then writes back a tiny EXIF block holding only the rotation, so the photo isn't turned sideways.
// PNG: drops the eXIf, tEXt, iTXt and zTXt chunks.
(() => {
  const drop = document.getElementById("meta-drop");
  const input = document.getElementById("meta-input");
  const list = document.getElementById("meta-results");
  if (!drop || !input || !list) return;

  // Interface text in the page's language (set by the build), English otherwise.
  const T = Object.assign({
    removed: "Removed {kb} KB of hidden data.", clean: "No hidden data found. It was already clean.", location: "Location",
    phone: "Phone", taken: "Taken", textChunks: "Text and date chunks", nothing: "Nothing personal found",
    download: "Download clean copy", unreadable: "This file couldn't be read:",
    unsupported: "Only JPEG and PNG are supported. HEIC photos: share them as JPEG first, or change your camera to save JPEG.",
  }, window.SC_TOOL || {});
  const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));

  // ---- Reading EXIF (just the fields that matter for privacy)
  function readExif(view, start, length) {
    // start points at "Exif\0\0"
    const t = start + 6;
    const little = view.getUint16(t) === 0x4949;
    const u16 = (o) => view.getUint16(t + o, little);
    const u32 = (o) => view.getUint32(t + o, little);
    const out = {};
    const str = (o, n) => { let s = ""; for (let i = 0; i < n; i++) { const c = view.getUint8(t + o + i); if (!c) break; s += String.fromCharCode(c); } return s.trim(); };
    const rational = (o) => { const a = u32(o), b = u32(o + 4); return b ? a / b : 0; };
    function ifd(off, tags) {
      if (off <= 0 || off + 2 > length) return;
      const n = u16(off);
      for (let i = 0; i < n; i++) {
        const e = off + 2 + i * 12;
        if (e + 12 > length) return;
        const tag = u16(e), type = u16(e + 2), count = u32(e + 4);
        const size = ({ 1: 1, 2: 1, 3: 2, 4: 4, 5: 8, 7: 1, 9: 4, 10: 8 }[type] || 1) * count;
        const vo = size > 4 ? u32(e + 8) : e + 8;
        tags(tag, type, count, vo);
      }
    }
    const first = u32(4);
    let exifOff = 0, gpsOff = 0;
    ifd(first, (tag, type, count, vo) => {
      if (tag === 0x010f) out.make = str(vo, count);
      else if (tag === 0x0110) out.model = str(vo, count);
      else if (tag === 0x0132) out.date = str(vo, count);
      else if (tag === 0x0112) out.orientation = u16(vo);
      else if (tag === 0x8769) exifOff = u32(vo);
      else if (tag === 0x8825) gpsOff = u32(vo);
    });
    ifd(exifOff, (tag, type, count, vo) => { if (tag === 0x9003) out.date = str(vo, count); });
    const gps = {};
    ifd(gpsOff, (tag, type, count, vo) => {
      if (tag === 1) gps.latRef = str(vo, 2);
      else if (tag === 2 && count === 3) gps.lat = rational(vo) + rational(vo + 8) / 60 + rational(vo + 16) / 3600;
      else if (tag === 3) gps.lonRef = str(vo, 2);
      else if (tag === 4 && count === 3) gps.lon = rational(vo) + rational(vo + 8) / 60 + rational(vo + 16) / 3600;
    });
    if (gps.lat !== undefined && gps.lon !== undefined && (gps.lat || gps.lon)) {
      out.lat = gps.latRef === "S" ? -gps.lat : gps.lat;
      out.lon = gps.lonRef === "W" ? -gps.lon : gps.lon;
    }
    return out;
  }

  // A minimal EXIF segment that only keeps the rotation (tag 0x0112).
  function orientationSegment(o) {
    const b = new Uint8Array(2 + 2 + 6 + 8 + 2 + 12 + 4);
    const v = new DataView(b.buffer);
    v.setUint16(0, 0xffe1); v.setUint16(2, b.length - 2);
    b.set([0x45, 0x78, 0x69, 0x66, 0, 0], 4);            // "Exif\0\0"
    b.set([0x4d, 0x4d, 0, 0x2a], 10); v.setUint32(14, 8); // big-endian TIFF header, IFD at 8
    v.setUint16(18, 1);                                   // one entry
    v.setUint16(20, 0x0112); v.setUint16(22, 3); v.setUint32(24, 1); v.setUint16(28, o);
    v.setUint32(32, 0);                                   // no next IFD
    return b;
  }

  function cleanJpeg(buf) {
    const view = new DataView(buf);
    if (view.getUint16(0) !== 0xffd8) throw new Error("Not a JPEG");
    const keep = [new Uint8Array(buf, 0, 2)];
    let info = {}, removed = 0, p = 2, insertAt = 1;
    while (p + 4 <= buf.byteLength) {
      const marker = view.getUint16(p);
      if ((marker & 0xff00) !== 0xff00) throw new Error("Damaged JPEG");
      if (marker === 0xffda) { keep.push(new Uint8Array(buf, p)); break; } // image data: copy the rest untouched
      const len = view.getUint16(p + 2);
      const seg = new Uint8Array(buf, p, len + 2);
      const isExif = marker === 0xffe1 && view.getUint32(p + 4) === 0x45786966;
      if (isExif) Object.assign(info, readExif(view, p + 4, len - 2));
      if (marker === 0xffe1 || marker === 0xffed || marker === 0xfffe) { removed += len + 2; }
      else { keep.push(seg); if (marker === 0xffe0) insertAt = keep.length; }
      p += len + 2;
    }
    if (info.orientation && info.orientation !== 1) keep.splice(insertAt, 0, orientationSegment(info.orientation));
    return { blob: new Blob(keep, { type: "image/jpeg" }), info, removed };
  }

  function cleanPng(buf) {
    const view = new DataView(buf);
    if (view.getUint32(0) !== 0x89504e47) throw new Error("Not a PNG");
    const keep = [new Uint8Array(buf, 0, 8)];
    let p = 8, removed = 0;
    const info = {};
    while (p + 12 <= buf.byteLength) {
      const len = view.getUint32(p);
      const type = String.fromCharCode(...new Uint8Array(buf, p + 4, 4));
      const total = len + 12;
      if (["eXIf", "tEXt", "iTXt", "zTXt", "tIME"].includes(type)) { removed += total; info.text = true; }
      else keep.push(new Uint8Array(buf, p, total));
      p += total;
      if (type === "IEND") break;
    }
    return { blob: new Blob(keep, { type: "image/png" }), info, removed };
  }

  function row(file, result, error) {
    const li = document.createElement("li");
    li.className = "meta-row";
    if (error) { li.innerHTML = `<div><strong>${esc(file.name)}</strong><p class="dim">${esc(error)}</p></div>`; list.prepend(li); return; }
    const { info, removed, blob } = result;
    const found = [];
    if (info.lat !== undefined) found.push(`<span class="meta-tag warn">${esc(T.location)} ${info.lat.toFixed(5)}, ${info.lon.toFixed(5)}</span>`);
    if (info.make || info.model) found.push(`<span class="meta-tag">${esc(T.phone)}: ${esc([info.make, info.model].filter(Boolean).join(" "))}</span>`);
    if (info.date) found.push(`<span class="meta-tag">${esc(T.taken)}: ${esc(info.date)}</span>`);
    if (info.text) found.push(`<span class="meta-tag">${esc(T.textChunks)}</span>`);
    const name = file.name.replace(/(\.[a-z0-9]+)?$/i, (ext) => `-clean${ext || ""}`);
    const url = URL.createObjectURL(blob);
    li.innerHTML = `<div>
        <strong>${esc(file.name)}</strong>
        <p class="dim">${esc(removed ? T.removed.replace("{kb}", (removed / 1024).toFixed(1)) : T.clean)}</p>
        <div class="meta-tags">${found.join("") || `<span class="meta-tag">${esc(T.nothing)}</span>`}</div>
      </div>
      <a class="btn btn-primary" href="${url}" download="${esc(name)}">${esc(T.download)}</a>`;
    list.prepend(li);
  }

  async function handle(files) {
    for (const file of files) {
      try {
        const buf = await file.arrayBuffer();
        const head = new Uint8Array(buf, 0, 4);
        if (head[0] === 0xff && head[1] === 0xd8) row(file, cleanJpeg(buf));
        else if (head[0] === 0x89 && head[1] === 0x50) row(file, cleanPng(buf));
        else row(file, null, T.unsupported);
      } catch (e) { row(file, null, T.unreadable + " " + e.message); }
    }
  }

  input.addEventListener("change", () => { handle([...input.files]); input.value = ""; });
  ["dragenter", "dragover"].forEach((t) => drop.addEventListener(t, (e) => { e.preventDefault(); drop.classList.add("over"); }));
  ["dragleave", "drop"].forEach((t) => drop.addEventListener(t, (e) => { e.preventDefault(); drop.classList.remove("over"); }));
  drop.addEventListener("drop", (e) => handle([...e.dataTransfer.files]));
})();

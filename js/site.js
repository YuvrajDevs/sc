// Theme toggle, mobile menu, hero background, scroll reveal.
(() => {
  // Picking a language remembers it for a year; the edge redirect then follows this choice instead of the browser's.
  document.addEventListener("click", (e) => {
    const a = e.target.closest && e.target.closest(".lang-menu a[data-lang]");
    if (a) document.cookie = `sc_lang=${a.dataset.lang}; path=/; max-age=31536000; samesite=lax`;
  });
  const root = document.documentElement;

  document.getElementById("theme-btn")?.addEventListener("click", () => {
    const next = root.dataset.theme === "light" ? "dark" : "light";
    root.dataset.theme = next;
    try { localStorage.setItem("theme", next); } catch (e) {}
  });

  // Close the language menu when tapping anywhere else.
  document.addEventListener("click", (e) => {
    document.querySelectorAll(".lang-menu[open]").forEach((d) => { if (!d.contains(e.target)) d.open = false; });
  });

  const menu = document.getElementById("menu-btn");
  menu?.addEventListener("click", () => {
    const open = menu.closest(".nav").classList.toggle("open");
    menu.setAttribute("aria-expanded", String(open));
  });

  // Background bars: rows of encrypted-looking data that stream sideways at different speeds,
  // with a few cells flickering as if being rewritten. Each row holds two identical halves so
  // sliding it by half its width loops without a seam.
  document.querySelectorAll(".bars").forEach((el) => {
    const rows = 26;
    let html = "";
    for (let r = 0; r < rows; r++) {
      let half = "";
      let x = Math.random() * 4;
      while (x < 96) {
        const w = 3 + Math.random() * 14;
        if (Math.random() > .3) {
          const kind = Math.random() > .6 ? "b" : "";
          const flick = Math.random() > .9 ? ` f" style="--d:${(Math.random() * 6).toFixed(2)}s;` : `" style="`;
          half += `<span class="${kind}${flick}left:${x / 2}%;width:${w / 2}%"></span>`;
        }
        x += w + 1 + Math.random() * 5;
      }
      const copy = half.replace(/left:([\d.]+)%/g, (_, v) => `left:${(+v + 50).toFixed(3)}%`);
      const dur = 40 + Math.random() * 70;
      html += `<div class="bar-row${r % 2 ? " rev" : ""}" style="top:${(r / rows) * 100}%;--t:${dur.toFixed(1)}s">${half}${copy}</div>`;
    }
    el.innerHTML = html;
  });

  document.getElementById("copy-email")?.addEventListener("click", (e) => {
    const btn = e.currentTarget, text = btn.textContent;
    const done = () => { btn.textContent = "Copied"; setTimeout(() => { btn.textContent = text; }, 1800); };
    (navigator.clipboard ? navigator.clipboard.writeText(btn.dataset.email) : Promise.reject()).then(done, () => {
      const r = document.createRange(); r.selectNodeContents(document.getElementById("support-email")); const s = getSelection(); s.removeAllRanges(); s.addRange(r);
    });
  });

  const io = "IntersectionObserver" in window ? new IntersectionObserver((entries) => {
    entries.forEach((e) => { if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); } });
  }, { rootMargin: "0px 0px -8% 0px" }) : null;
  document.querySelectorAll(".reveal").forEach((el) => io ? io.observe(el) : el.classList.add("in"));

})();

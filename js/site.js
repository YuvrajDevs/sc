// Theme toggle, mobile menu, hero background, scroll reveal and local prices.
(() => {
  const root = document.documentElement;

  document.getElementById("theme-btn")?.addEventListener("click", () => {
    const next = root.dataset.theme === "light" ? "dark" : "light";
    root.dataset.theme = next;
    try { localStorage.setItem("theme", next); } catch (e) {}
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

  const io = "IntersectionObserver" in window ? new IntersectionObserver((entries) => {
    entries.forEach((e) => { if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); } });
  }, { rootMargin: "0px 0px -8% 0px" }) : null;
  document.querySelectorAll(".reveal").forEach((el) => io ? io.observe(el) : el.classList.add("in"));

  // Prices: rupees for India, dollars elsewhere, matching the Play Console listing.
  const toggle = document.querySelector(".price-toggle");
  if (toggle) {
    const show = (cur) => {
      document.querySelectorAll("[data-usd]").forEach((el) => { el.textContent = el.dataset[cur]; });
      toggle.querySelectorAll("button").forEach((b) => b.setAttribute("aria-pressed", String(b.dataset.cur === cur)));
    };
    const india = /-IN$/i.test(navigator.language) || (Intl.DateTimeFormat().resolvedOptions().timeZone || "") === "Asia/Kolkata";
    show(india ? "inr" : "usd");
    toggle.addEventListener("click", (e) => { const b = e.target.closest("button"); if (b) show(b.dataset.cur); });
  }
})();

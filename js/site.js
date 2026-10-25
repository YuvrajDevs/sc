// Theme toggle, mobile menu, hero background, scroll reveal, the Play Store QR code and local prices.
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

  // Hero background: rows of soft bars, like encrypted data streaming past.
  document.querySelectorAll(".bars").forEach((el) => {
    const rows = 26;
    let html = "";
    for (let r = 0; r < rows; r++) {
      let x = -Math.random() * 10;
      while (x < 100) {
        const w = 4 + Math.random() * 18;
        if (Math.random() > .35) html += `<span class="${Math.random() > .6 ? "b" : ""}" style="top:${(r / rows) * 100}%;left:${x}%;width:${w}%"></span>`;
        x += w + Math.random() * 6;
      }
    }
    el.innerHTML = html;
  });

  const io = "IntersectionObserver" in window ? new IntersectionObserver((entries) => {
    entries.forEach((e) => { if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); } });
  }, { rootMargin: "0px 0px -8% 0px" }) : null;
  document.querySelectorAll(".reveal").forEach((el) => io ? io.observe(el) : el.classList.add("in"));

  // QR code pointing at the Play listing, drawn once the small generator library has loaded.
  const qr = document.querySelector("[data-qr]");
  if (qr) {
    const s = document.createElement("script");
    s.src = "https://cdnjs.cloudflare.com/ajax/libs/qrcode-generator/1.4.4/qrcode.min.js";
    s.onload = () => {
      const q = window.qrcode(0, "M");
      q.addData(qr.dataset.qr);
      q.make();
      qr.innerHTML = q.createSvgTag({ cellSize: 4, margin: 0, scalable: true });
    };
    document.head.appendChild(s);
  }

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

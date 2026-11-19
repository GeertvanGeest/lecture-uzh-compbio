#!/usr/bin/env python3
"""Flag revealjs slides whose content runs below the bottom of the slide.

Usage:
    quarto render slides.qmd
    python3 check_overflow.py [slides.html]

Injects a measuring script into a temporary copy of the rendered deck, runs it
in headless Chrome, and reports, for every slide, how far its content extends
(in unscaled slide pixels) compared with the slide height.
"""

import json
import re
import subprocess
import sys
from pathlib import Path

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
FOOTER_MARGIN = 40  # px at the bottom reserved for footer / slide number

MEASURE_JS = r"""
<script>
window.addEventListener('load', () => {
  const run = () => {
    const cfg = Reveal.getConfig();
    const H = cfg.height;
    const out = [];
    const slides = Reveal.getSlides();
    slides.forEach((s, i) => {
      const idx = Reveal.getIndices(s);
      Reveal.slide(idx.h, idx.v, -1);
      const scale = Reveal.getScale();
      const top = s.getBoundingClientRect().top;
      let bottom = 0;
      s.querySelectorAll('*').forEach(el => {
        if (el.closest('aside') || el.closest('.r-stretch')) return;
        const r = el.getBoundingClientRect();
        if (r.height === 0 && r.width === 0) return;
        bottom = Math.max(bottom, (r.bottom - top) / scale);
      });
      // content must stay above the (bottom-pinned) aside, if any
      const aside = s.querySelector('aside:not(.notes)');
      const asideTop = aside ? (aside.getBoundingClientRect().top - top) / scale : null;
      const h = s.querySelector('h1, h2, h3');
      out.push({n: i + 1, title: h ? h.textContent.trim() : '(no title)',
                bottom: Math.round(bottom), height: H,
                limit: asideTop === null ? null : Math.round(asideTop)});
    });
    const pre = document.createElement('pre');
    pre.id = 'overflow-result';
    pre.textContent = JSON.stringify(out);
    document.body.appendChild(pre);
  };
  // give mermaid / fonts time to render
  setTimeout(run, 4000);
});
</script>
"""


def main():
    src = Path(sys.argv[1] if len(sys.argv) > 1 else "slides.html").resolve()
    tmp = src.with_name("_overflow_check.html")
    html = src.read_text()
    tmp.write_text(html.replace("</body>", MEASURE_JS + "</body>"))
    try:
        dom = subprocess.run(
            [CHROME, "--headless=new", "--disable-gpu", "--window-size=1050,700",
             "--virtual-time-budget=15000", "--dump-dom", tmp.as_uri()],
            capture_output=True, text=True, timeout=120,
        ).stdout
    finally:
        tmp.unlink(missing_ok=True)

    m = re.search(r'<pre id="overflow-result">(.*?)</pre>', dom, re.S)
    if not m:
        sys.exit("Could not read measurement result from Chrome output")
    results = json.loads(m.group(1).replace("&quot;", '"').replace("&amp;", "&")
                         .replace("&lt;", "<").replace("&gt;", ">"))

    bad = 0
    for r in results:
        if r["limit"] is not None:
            limit, what = r["limit"], "aside"
        else:
            limit, what = r["height"] - FOOTER_MARGIN, "footer"
        if r["bottom"] > r["height"] or (what == "aside" and r["bottom"] > limit):
            flag = "OVERFLOW"
        elif r["bottom"] > limit:
            flag = "tight"
        else:
            continue
        bad += flag == "OVERFLOW"
        print(f"{flag:8s} slide {r['n']:3d}  bottom={r['bottom']:4d}  limit={limit} ({what})  {r['title']}")
    print(f"\n{len(results)} slides checked, {bad} overflowing")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()

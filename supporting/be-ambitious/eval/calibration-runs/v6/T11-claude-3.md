```text
Make our marketing website's home page load fast on mobile. Today it takes about 10 seconds. Then apply the same fixes to the rest of the site where they carry over.

Assumption: the goal behind "faster" is that first-time mobile visitors on ordinary phones and connections see the main message and can act before they leave. The marketing metrics the site exists for (sign-ups, demo requests, purchases) should not get worse.
Assumption: "about 10 seconds" is an informal observation. Establish which metric it corresponds to before optimizing.

First checks (report what is missing and continue only with work the available access supports):
- Access to the site's source repo and build tooling.
- Access to hosting/CDN configuration (caching headers, compression, image delivery).
- A preview or staging URL where changes can be measured before production.
- Any existing field data: Chrome UX Report (CrUX) for the origin, Search Console Core Web Vitals, or an existing RUM/analytics tool.
- The list of third-party scripts on the page and who owns each one (tag manager, analytics, chat, A/B testing, ads pixels).

Baseline from raw evidence, not a single score:
- Lab: run WebPageTest (or Lighthouse CLI with identical settings) on the home page as a mid-tier Android device on a 4G profile, cold cache, at least 5 runs. Record the median and spread of TTFB, First Contentful Paint, Largest Contentful Paint (LCP), Total Blocking Time (TBT), Cumulative Layout Shift (CLS), total bytes, JS bytes, and request count. Keep the waterfall and a Chrome DevTools performance trace for the median run.
- Field: pull p75 LCP, INP, and CLS for mobile from CrUX/Search Console if available.
- State which metric the "10 seconds" matches (for example LCP, fully loaded, or onload), and whether lab and field agree.

Diagnose before fixing:
- Identify the LCP element and break its time into TTFB, resource load delay, resource load duration, and render delay. Fix the largest share first.
- Walk the critical rendering path in the waterfall: render-blocking CSS/JS, fonts, redirects, and late-discovered resources.
- Run a bundle analysis (source-map-explorer or webpack/rollup bundle analyzer) to find unused or oversized JavaScript.
- Measure the cost of each third-party script by blocking it in WebPageTest and rerunning. This shows the measured cost of each script, not a guessed one.
- Inspect images (format, dimensions vs. rendered size, lazy-loading), fonts (subsetting, font-display, preload), and caching/compression headers.

Fix in measured steps:
- Apply one change or one coherent group of changes at a time. Re-measure with the same lab settings and record the delta for each, so every gain is attributed.
- Typical candidates, used only where the diagnosis supports them:
  - Responsive AVIF/WebP images with correct sizes, and fetchpriority="high" on the LCP image.
  - Lazy-loading below the fold.
  - Inlining critical CSS and deferring the rest.
  - Deferring or removing unused JS, and code-splitting.
  - Preconnecting to required origins.
  - Self-hosted, subsetted fonts.
  - Long-lived cache headers on hashed assets, and Brotli/gzip compression.
  - Reducing TTFB via CDN or edge caching of the HTML.
- Stretch target: aim for median lab LCP ≤ 2.0 s, TBT ≤ 200 ms, and CLS ≤ 0.1 on the mid-tier-Android/4G profile, using the methods above. When one approach stalls, move to the next-largest remaining cost in the LCP breakdown or waterfall before reporting a miss.

Red-team the result before calling it done:
- Re-run on a slow-3G profile, from a second test location, and with a warm cache. Confirm the gain holds and nothing regressed.
- Take a visual diff of before/after screenshots at mobile and desktop widths.
- Check functionally that forms submit, CTAs work, and every analytics/marketing tag that remains still fires. Speed gains that break conversion tracking or the page's message are failures.

With my approval only: deploy changes to production.
With my approval only: remove, delay, or replace any third-party marketing/analytics script. Bring me the measured cost of each one and what would be lost.
With my approval only: add a real-user monitoring snippet (for example the web-vitals library reporting to our analytics) to collect field LCP/INP/CLS.
With my approval only: add a performance budget check to CI (for example Lighthouse CI with LCP, TBT, and JS-byte limits) so future changes cannot silently undo this work.
With my approval only: after production deploy, compare mobile bounce rate and conversion rate for comparable periods before and after the change, using our analytics, with seasonality and campaign changes noted.

Judge:
- Pass condition: the home page's median lab LCP on the same mid-tier-Android/4G profile is measurably lower than the baseline. The before/after run sets (≥5 runs each, identical settings) must be reported together with spread, and the visual-diff and functional checks must pass.
- Report each change's measured delta.
- Report the stretch target (LCP ≤ 2.0 s, TBT ≤ 200 ms, CLS ≤ 0.1) separately, as met or missed per metric.
- Field results (CrUX/RUM p75) and business impact stay unverified until production data covers at least 28 days after deploy.
```

- `depth`: The baseline is median-of-≥5 WebPageTest/Lighthouse runs on a fixed device/network profile plus field CrUX data. A single "feels like 10 s" impression cannot show whether a change helped.
- `depth`: The task rests on the belief "10 seconds," so the prompt first checks which metric that is. This keeps effort from going to the wrong bottleneck.
- `depth`: Diagnosis uses the LCP sub-part breakdown, the waterfall, bundle analysis, and per-script blocking. Fixes then target measured costs instead of a generic checklist.
- `depth`: The stretch target of LCP ≤ 2.0 s / TBT ≤ 200 ms / CLS ≤ 0.1 is reported separately. The owner's bar stays "measurably faster."
- `range` (experimental design): Applying one change at a time with re-measurement attributes each gain. This also exposes changes that don't help.
- `range` (red team): Slow-3G, second-location, and warm-cache runs, visual diffs, and tag-firing checks catch speedups that break the message or the marketing attribution.
- `altitude`: The original outcome is a faster home page. The improved outcome is faster mobile pages for real visitors (field p75) with no loss in conversions, plus protection against regression. It is checked with RUM/CrUX and before/after analytics, all behind approval. This needs a RUM snippet, analytics access, a CI budget, and a 28-day field window.
- Scope/risk: Production deploys and third-party script removal are behind approval because they change what visitors see and what marketing can measure. RUM adds data collection. The CI budget adds a recurring gate.
- Skipped: none. All three lenses add distinct, permitted contributions.
- Owner actions:
  - Confirm repo, CDN/hosting, staging, and analytics/CrUX access.
  - Name each third-party script's owner.
  - Decide on production deploy, script removal, RUM, the CI budget, and the conversion comparison.

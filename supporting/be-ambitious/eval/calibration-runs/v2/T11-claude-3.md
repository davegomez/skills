```text
Make our marketing website load faster, starting with the home page, which takes about 10 seconds to load on mobile.

Goal (assumption: the site exists to turn visitors into leads or signups, so what counts is speed that real mobile visitors experience and that stays fixed):
bring the home page into Google's "good" Core Web Vitals range for real mobile users, and add guardrails that keep it there.

First, check access. Report what is missing and continue with whatever is available:
- the site's source repo and build;
- a staging or preview environment;
- field data: CrUX / PageSpeed Insights, Search Console Core Web Vitals, or any RUM tool;
- the analytics and tag manager config;
- the hosting/CDN settings.
Without field data, every result is lab-only, and the field target stays unverified.

1. Test the premise before fixing anything.
   - Find out what "10 seconds" measures: LCP, full load, or time to interactive. Use field data at p75 where it exists.
   - Reproduce it in the lab with WebPageTest (or Lighthouse with DevTools throttling) on a mid-tier Android profile over slow 4G. Use 3+ runs and report the median.
   - Record the baseline: TTFB, FCP, LCP and its element, INP/TBT, CLS, total bytes, JS bytes, request count, and third-party share.
   - Save the waterfall and the Chrome performance trace. Work from the trace, not the Lighthouse score.

2. Diagnose the critical path to the LCP element.
   - Break LCP into its parts: TTFB, resource load delay, resource load time, and render delay.
   - Attribute each part to specific requests and main-thread tasks.
   - Use source-map-explorer or a bundle analyzer for JS weight.
   - Use the Coverage panel for unused CSS/JS.
   - Use a third-party audit (bytes and main-thread time per vendor) for tags, chat widgets, and embeds.

3. Fix in order of measured impact. Likely candidates, to be confirmed by the trace:
   - Images: right-sized responsive images (srcset/sizes, AVIF/WebP). Give the LCP image fetchpriority="high" or a preload, and never lazy-load it.
   - CSS and fonts: inline critical CSS, defer the rest. Subset fonts, self-host them, use font-display: swap, and preload them.
   - JS: defer or async non-critical JS, code-split, and remove unused libraries. Avoid hydrating static marketing content.
   - Delivery: Brotli, long-lived cache headers on hashed assets, CDN caching of the HTML, and fewer redirects.
   - Third parties: load them after interaction or idle, or replace them with facades (e.g., a static image standing in for a video embed or chat widget).
   - Reserve space for every late element so CLS stays ≤ 0.1.
   Re-measure after each change, so every line in the final report shows its own delta.

4. Aim for lab LCP ≤ 2.5 s, TBT ≤ 200 ms, and CLS ≤ 0.1 on the mobile profile above, and for field p75 LCP ≤ 2.5 s, INP ≤ 200 ms, and CLS ≤ 0.1. Treat this as solvable: when one lever stalls, go to the next largest part of the LCP breakdown before reporting a miss. Report the measured result even if the target is missed.

5. Zero-based tag budget. List every third-party script with:
   - its bytes and main-thread cost;
   - the business purpose it claims;
   - whether data shows anyone uses it.
   Propose a keep, defer, or remove decision for each. These are proposals, not findings, until the owning team confirms.

6. Red-team the results before claiming them:
   - Check that gains hold on a cold cache, on a first visit with the consent banner shown, and from at least one distant geography.
   - Confirm that no change games the lab score at real users' expense, such as a lazy-loaded hero or content hidden until JS runs.
   - Confirm that analytics/attribution events still fire on staging.
   - Confirm that the rendered HTML still contains the SEO content and meta tags.

7. Guardrails: propose a performance budget enforced in CI with Lighthouse CI or similar, with thresholds for LCP, TBT, CLS, and JS/image bytes, so regressions fail the build.

Apply the same diagnosis to other high-traffic pages only after the home page passes.

Requires my approval before doing:
- removing or changing any third-party tag;
- deploying to production;
- changing CDN or hosting configuration, or anything that adds cost;
- adding a RUM tool or vendor;
- making the CI budget blocking;
- extending the work beyond the home page.
Optional, only if approved: compare home-page conversion and bounce rates for the 4 weeks before and after the change, noting seasonality and campaign confounders. Treat it as correlational evidence, not proof of cause.

Judge:
- The same lab profile and run count, before vs. after, shows lab LCP ≤ 2.5 s and a clear drop from the baseline. That is the pass condition. Any measured improvement over the baseline meets the original ask.
- The red-team checks in step 6 pass on staging.
- Field p75 LCP/INP/CLS, re-checked after the 28-day CrUX window rolls over (or sooner with RUM), confirms the target in the field. Until then, report the field target as unverified.
- Report every metric's baseline, result, and target, including any misses.
```

**Ledger**
- `altitude`: The original task was "make the home page load faster." The chosen outcome is good Core Web Vitals for real mobile users, plus a CI performance budget so the gain lasts. The benefit is a fix that stays fixed and is measured where users are. This adds CI work, and making the budget blocking needs your approval.
- `depth`: The work starts by testing what "10 seconds" actually measures, using field data and a reproducible lab profile. It works from raw traces and waterfalls rather than the Lighthouse score. Root cause comes from the LCP breakdown, with a measured delta per change. No added cost.
- `depth`: The stretch target is LCP ≤ 2.5 s, INP ≤ 200 ms, CLS ≤ 0.1, roughly 4× faster than today. "Any measured improvement" remains the pass bar. Confirming it in the field takes up to 28 days with CrUX.
- `range`: Zero-based budgeting (from accounting) makes every third-party tag justify its cost. This exposes the vendor scripts that usually dominate marketing-site weight. Removing any tag needs your approval and the owning team's sign-off.
- `range`: Red-team checks cover cold cache, consent banner, geography, analytics, and SEO. They guard against lab-only wins and broken attribution or indexing. This adds staging verification time.
- `altitude` (optional): A before/after conversion comparison links speed to business results. It is correlational only and runs only with your approval.
- Skipped: none. All three lenses fit.
- Owner actions:
  - Confirm access to the repo, staging, the tag manager/analytics config, and the CDN.
  - Confirm a field-data source (CrUX/Search Console/RUM).
  - Approve or decline tag removals, production deploys, CDN/cost changes, a RUM vendor, a blocking CI budget, scope beyond the home page, and the conversion comparison.

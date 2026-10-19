```text
Make our marketing website's home page load faster for mobile visitors. Today it takes about 10 seconds to load on mobile.

Assumption: the goal behind the request is that a first-time visitor on a phone sees the headline and primary call to action quickly enough to stay. That supports bounce rate, conversion, and search ranking through Core Web Vitals.
Assumption: "about 10 seconds" has not been tied to a specific metric. Establish which metric it is before optimizing.

First checks. Name anything missing and continue only with work the available access supports:
- Access to the site's source repo, build tooling, and a staging or preview environment.
- Access to hosting and CDN configuration (caching headers, compression, image delivery).
- Whether CrUX field data exists for the origin or home URL (PageSpeed Insights or the CrUX API). Low-traffic sites may have none.
- Read access to existing analytics and the tag manager container.
- Which lab tools are available: Lighthouse CLI, Chrome DevTools, and WebPageTest. Public WebPageTest results are publicly viewable. Use it only on the public production URL, never on staging or preview URLs, unless a private instance is available.

1. Baseline from raw evidence, not a single score.
   - Fix one test profile and use it for every before/after comparison: mid-tier Android emulation, throttled 4G, cold cache, same test location.
   - Run at least 9 runs per condition. Report the median and spread for LCP, FCP, TTFB, Total Blocking Time, CLS, total bytes, and request count.
   - Capture a full request waterfall and a Chrome DevTools performance trace.
   - Record field data (p75 LCP, INP, CLS on mobile) if it exists.
   - State which metric matches "about 10 seconds" and whether field and lab agree.

2. Find the critical path before changing anything.
   - Identify the LCP element.
   - Trace the chain of requests and main-thread work that must finish before it renders: TTFB, render-blocking CSS and JS, font loading, LCP resource discovery and download, hydration and long tasks.
   - Only shortening this chain lowers LCP. Rank candidate fixes by their measured share of it.
   - Measure each third-party script's cost by running with that domain blocked (WebPageTest block or DevTools request blocking), and list every tag with its measured cost.
   - Analyze the JS bundle with source-map-explorer or the framework's bundle analyzer.

3. Fix in order of measured impact. Re-measure after each change with the fixed profile. Typical candidates, applied only where the evidence points:
   - LCP image: right-sized responsive images (srcset/sizes), AVIF/WebP, `fetchpriority="high"` and no lazy-loading on it, preload if it is discovered late.
   - Lazy-load below-the-fold media.
   - Inline critical CSS and defer the rest.
   - Defer or async non-critical JS, split code, and remove unused JS and CSS.
   - Fonts: subset, use `font-display: swap` or `optional`, and preload only the fonts above the fold.
   - Delivery: Brotli/gzip, long-lived cache headers on hashed assets, CDN caching of HTML where safe.
   - Set explicit dimensions on media to prevent layout shift.
   Aim for mobile lab LCP at or under 2.0 s (median, fixed profile) and under 1 MB transferred before first interaction, while keeping CLS under 0.1 and Total Blocking Time under 200 ms. Treat this as solvable: when one approach stalls, re-read the trace for the next-largest critical-path cost and try that before reporting a miss.

4. Red-team the result before calling it done.
   - Compare before/after screenshots at mobile and desktop widths for every home-page section (Playwright or similar) to catch visual regressions.
   - Confirm that forms submit, analytics and conversion events still fire (check the network panel and the analytics debug view), and that SEO meta tags, structured data, and canonical tags are unchanged.
   - Confirm that no measured improvement comes only from warm caches or a changed test profile.

Ship changes through the site's existing review and deploy process.
With my approval only: remove, delay, or replace any third-party or marketing tag. Bring me the per-tag cost list and the owner each tag serves.
With my approval only: change CDN, hosting, or image-service configuration, or add any paid service.
With my approval only: apply the same method to other high-traffic landing pages.
With my approval only: add a performance budget to CI (e.g. Lighthouse CI with LCP, bytes, and CLS thresholds) so regressions fail the build.
With my approval only: add real-user monitoring (e.g. the web-vitals library reporting to our existing analytics) to track field LCP, INP, and CLS at p75 on mobile.
With my approval only: run an A/B test or before/after comparison of mobile bounce and conversion rates over a period we agree on.

Report:
- The baseline and the metric behind "about 10 seconds".
- The critical-path breakdown.
- Each change with its measured effect.
- The third-party cost list.
- Red-team results.
- Before/after numbers.
- The stretch target, met or missed.

Judge: same fixed lab profile, at least 9 runs per condition, before vs after.
Pass: median mobile LCP on the home page is measurably lower than baseline, with no visual, functional, tracking, or SEO regressions in the red-team checks.
Stretch, reported separately as met or missed: median lab LCP ≤ 2.0 s with CLS < 0.1 and TBT < 200 ms.
Field verification: if field data exists, report mobile p75 LCP after the 28-day CrUX window. Until then, field improvement is unverified.
```

**Ledger**

- `altitude`: The original outcome was "the home page loads faster." The improved outcome is "mobile visitors see the message and CTA fast enough to stay," checked against field Core Web Vitals and, with approval, bounce and conversion data. Extending to other pages, monitoring, CI, and A/B tests sits behind approval lines.
- `depth`: The first steps pin down which metric "10 seconds" is and baseline it with repeated runs on a fixed profile, waterfalls, traces, and CrUX field data. This replaces a single Lighthouse score and avoids optimizing the wrong metric.
- `depth`: Fixes are ranked by their measured share of the LCP critical path, with per-tag blocking tests and bundle analysis. Effort goes where it moves the number.
- `depth`: The hard target is lab LCP ≤ 2.0 s, CLS < 0.1, TBT < 200 ms. The owner's bar ("faster") remains the pass condition, and the stretch is reported separately.
- `range`: Critical-path method from operations research means only work on the critical chain lowers LCP, which keeps fixes off irrelevant bytes.
- `range`: Repeated-measures practice from experimental statistics (n ≥ 9, median and spread, fixed conditions) separates real gains from run-to-run noise.
- `range`: The red team covers visual diffs, form and tracking checks, and SEO tags. It catches the common failure where speed gains come from silently breaking marketing tracking.
- Risk: Public WebPageTest publishes results, so the prompt limits it to the public URL. Tag removal touches other teams' tracking and is gated.
- Skipped: None. All three lenses fit.
- Owner actions:
  - Confirm repo, staging, and CDN/hosting access.
  - Confirm analytics and tag-manager read access.
  - Check whether CrUX field data exists for the site.
  - Decide whether to approve tag changes, CDN or paid changes, other pages, the CI budget, RUM, and the conversion test.

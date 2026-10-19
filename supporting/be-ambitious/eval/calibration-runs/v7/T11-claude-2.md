```text
Make our marketing website load faster, starting with the home page, which takes about 10 seconds to load on mobile.
Assumption: the goal is that mobile visitors see and can use the home page quickly enough not to leave, and that search ranking benefits from good Core Web Vitals.

First checks, before any changes: confirm access to the site source, a preview or staging environment that matches production, and the hosting/CDN configuration. Confirm whether Chrome UX Report (CrUX) or Search Console field data, existing real-user monitoring, and Lighthouse or WebPageTest are available. List any missing dependency and continue only with work the available access supports.

1. Reproduce and define the "10 seconds." Measure the production home page under a fixed mobile profile: one mid-tier Android device class (real device if available, otherwise emulated), Slow 4G throttling, one test location, and a cold cache. Run at least 5 times and record the medians and spread for LCP, FCP, TTFB, CLS, TBT (lab proxy for INP), total transfer bytes, and request count. Pull CrUX p75 mobile field data for the home page if it exists. State which metric matches the reported ~10 s and where lab and field data disagree.
2. Find the cause from raw evidence, not summaries. Use the WebPageTest waterfall and filmstrip, a Chrome DevTools Performance trace, and a HAR file to trace the critical rendering path to the LCP element. Use a bundle analyzer (e.g. source-map-explorer or the framework's equivalent) to attribute JS/CSS bytes to modules. Inventory every third-party script with its bytes, main-thread time, and whether it blocks rendering. Rank bottlenecks by their measured contribution to LCP and TBT before fixing any of them.
3. Fix the bottlenecks in order of measured impact, re-measuring after each change under the same profile. Candidate fixes include:
   - Images: right-size the LCP image, serve AVIF/WebP via srcset/sizes, preload or set fetchpriority on the LCP image, lazy-load below-the-fold media.
   - Render-blocking work: inline critical CSS, defer non-critical JS, code-split, remove unused code.
   - Fonts: subset fonts, preload them, use font-display.
   - Connections: preconnect to required origins.
   - Server and delivery: Brotli compression, cache headers, TTFB fixes in code we control.
   - Third parties: load third-party widgets behind facades.
   Keep a change that does not move its target metric beyond run-to-run spread only if it carries no risk.
4. Aim for a median lab mobile LCP ≤ 2.0 s and TBT ≤ 200 ms under the step-1 profile, with CLS ≤ 0.1, using the ranked bottleneck list. When one approach stalls, try the next ranked bottleneck before reporting a miss. "Measurably faster than baseline" remains the pass bar. Report the stretch result separately, met or missed.
5. Red-team the result before calling it done.
   - Compare before/after screenshots at mobile and desktop widths (e.g. Playwright visual diff) to catch layout or content regressions.
   - Confirm that forms, CTAs, and navigation work.
   - Confirm that each analytics or marketing tag still fires once per page view in the browser network log.
   - Check that the gains hold on a second, slower device profile and are not tuned to one test setup.
6. Report: the baseline vs. after table (median and spread per metric, same profile), the ranked causes with the evidence for each, the changes made and their measured effect, the stretch target met or missed, any regressions found, and the remaining bottlenecks with estimated impact.

With my approval only: remove, defer, or change the loading of third-party marketing/analytics tags in ways that could alter the data they collect.
With my approval only: change hosting, CDN, or image-service configuration, or add any paid service.
With my approval only: deploy the changes to production.
With my approval only: add real-user monitoring of Core Web Vitals segmented by device, and relate home-page load time to bounce and conversion rates from existing analytics.
With my approval only: add a performance budget check (Lighthouse CI or equivalent) to CI so future changes cannot regress mobile LCP, TBT, or page weight past agreed limits.

Judge: Lighthouse/WebPageTest lab measurements under the step-1 mobile profile, at least 5 runs each before and after, same URL, device, network, location, and cache state. Pass only if:
- the median home-page mobile LCP improves on the baseline by more than the run-to-run spread;
- no other Core Web Vital worsens beyond its spread;
- the visual diff and functional checks show no unintended regressions;
- every analytics/marketing tag still fires as before.
The improvement under real-world conditions stays unverified until production field data (CrUX p75 mobile or RUM) covering the changed page is available. Report it then, met or missed.
```

- `altitude`: the original outcome was a home page that loads faster in some unspecified sense. The improved outcome is mobile visitors getting a usable page fast enough to stay, checked against field Core Web Vitals and, with approval, against bounce and conversion. Adds a later field-data check and optional RUM. The analytics work needs data access.
- `altitude`: an optional CI performance budget keeps the gains from regressing. It is a new recurring workflow, so it sits behind approval.
- `depth`: reproduce and define the "10 seconds" with named metrics and a fixed test profile. This tests the belief the task rests on and makes "faster" measurable.
- `depth`: uses raw waterfalls, traces, HAR files, bundle analysis, and a third-party inventory to rank causes before fixing. This replaces guesswork with a measured critical path.
- `depth`: sets a hard target of lab LCP ≤ 2.0 s and TBT ≤ 200 ms, with a next-approach rule. The owner's "faster" bar stays the pass condition, and the stretch is reported separately.
- `range`: borrows from experimental statistics: repeated runs, medians, and spread-based significance. This keeps noise from being reported as a gain.
- `range`: borrows from marketing analytics, tying load time to bounce and conversion. This shows the business effect. It needs analytics access and approval.
- `range`: adds a red team of visual diffs, functional checks, tag-firing checks, and a second device profile. It catches broken pages, lost tracking data, and setup-specific gains.
- Skipped: none. All three lenses fit.
- Owner actions:
  - Confirm access to the source, staging, hosting/CDN config, CrUX/Search Console, analytics, and test tools.
  - Decide on the five approval items: tag changes, hosting/CDN or paid services, production deploy, RUM with conversion analysis, and the CI budget.

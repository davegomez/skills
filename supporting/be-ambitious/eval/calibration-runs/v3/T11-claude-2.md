```text
Make our marketing website load faster. The home page takes about 10 seconds to load on mobile; make it load measurably faster for mobile visitors.

Assumption (confirm or correct): the goal is for mobile visitors to see the home page's main content and be able to act on it before they leave. That makes Largest Contentful Paint (LCP) the main metric, with First Contentful Paint (FCP), Time to First Byte (TTFB), Total Blocking Time (TBT), Interaction to Next Paint (INP), and Cumulative Layout Shift (CLS) as supporting metrics.

First checks. Report each as available or missing, and continue only with work the available access supports:
- Access to the site's source and its build, plus a preview or staging environment that matches production.
- The production home page URL.
- Field data on real users: the Chrome UX Report (CrUX) through PageSpeed Insights or Search Console, or any real-user monitoring (RUM) the site already has.
- A way to run repeatable mobile lab tests: Lighthouse or Chrome DevTools with a fixed mobile profile, or WebPageTest on a mid-range Android device with a 4G profile.

1. Test the "10 seconds" claim. It may describe one device, one network, or a different metric.
   - Pull field data at the 75th percentile (p75) for mobile: LCP, FCP, TTFB, INP, and CLS.
   - Record a lab baseline on one fixed profile: device, network throttling, location, cache state, and build/commit. Use the median of at least 5 runs and report the spread.
   - State which metric and conditions the 10 seconds matches. Every later comparison uses this same profile.

2. Find the cause from raw evidence, not from the Lighthouse score.
   - Use the WebPageTest waterfall and filmstrip, and a DevTools Performance trace.
   - Trace the critical path the way a scheduler traces a project's critical path: the chain of requests and main-thread work that must finish before the LCP element renders. Attribute the time to each link: server/TTFB, redirects, render-blocking CSS and JS, fonts, the LCP image, and client-side rendering.
   - Find unused code and what each bundle contains, using the DevTools Coverage tab and a bundle analyzer (webpack-bundle-analyzer or source-map-explorer).
   - List every third-party script (tag manager, analytics, chat, A/B tools, embeds) with its bytes, main-thread time, and whether it blocks rendering.

3. Fix the causes in order of measured time saved on the critical path. Common candidates:
   - Make the LCP resource discoverable early, with `fetchpriority="high"` or preload. Do not lazy-load it.
   - Serve responsive AVIF or WebP images via `srcset`, and lazy-load images below the fold.
   - Inline critical CSS and defer the rest.
   - Defer or split first-party JS.
   - Subset and preload fonts, and use `font-display`.
   - Use brotli compression and long-lived caching for static assets.
   - Remove redirects.
   - If the server's TTFB is the bottleneck, address server caching or rendering.
   Re-measure after each change on the baseline profile so each saving is attributed to its change.

4. Red-team the changes before calling them done.
   - Confirm that analytics and conversion events, forms, consent banners, and SEO-relevant markup (titles, meta tags, structured data, canonical URLs) still behave as before.
   - Run a screenshot comparison of the home page at mobile and desktop widths to catch visual regressions and new layout shifts.

Aim for p75 mobile LCP ≤ 2.5 s, INP ≤ 200 ms, and CLS ≤ 0.1 (Core Web Vitals "good"), checked in the lab on the baseline profile. Treat this target as solvable: when one approach stalls, try the next cause on the critical path before reporting a miss.

With my approval only: remove, defer, or replace any third-party script or marketing tag. Each one has a business owner and may feed tracking or revenue reporting.
With my approval only: deploy changes to production.
With my approval only: change CDN, hosting, or server configuration, or use any paid service (for example a paid RUM tool or the WebPageTest API).
With my approval only: apply the same fixes to other marketing pages.
With my approval only: add a performance budget check to CI (for example Lighthouse CI with LCP and bundle-size limits) so the gains don't regress.
With my approval only: run a measured pilot or A/B holdback comparing bounce rate and conversion on the faster home page against the current one.

Report:
- The first-check results.
- What "10 seconds" turned out to measure.
- A before/after table on the same profile: median and spread for LCP, FCP, TTFB, TBT, and CLS, with build/commit for each.
- The critical-path breakdown, and the saving attributed to each change.
- The red-team results.

Judge: an automated lab measurement, the median of at least 5 runs on the fixed mobile profile. Pass when the after-build's median LCP is lower than the baseline's, the reduction is larger than the run-to-run spread, and analytics events, forms, and screenshots show no regressions.
Stretch: report on its own line whether the ≤ 2.5 s / 200 ms / 0.1 targets are met or missed.
Field confirmation: mark it pending until real-user data covers the change after deploy (CrUX uses a rolling 28-day window). If field data is unavailable, report the field result as unverified.
```

- `altitude`: The original outcome was a home page that loads faster. The improved outcome is that real mobile visitors see the content and can act on it sooner, measured as p75 field LCP. Conversion impact is behind an approval-gated pilot. Effect: field confirmation lags deployment.
- `depth`: The prompt tests the "10 s" claim against field data and a fixed lab profile before any fix. This keeps effort from going to the wrong metric or device.
- `depth`: The diagnosis works from raw waterfalls and traces, attributing time to each link of the critical path, plus coverage, bundle, and third-party inventories. Fixes are ranked by measured saving, not by checklist.
- `depth`: Hard target of Core Web Vitals "good", reported separately from the owner's bar of "faster". It pushes the work past easy wins without changing the pass condition.
- `range`: The critical-path method from project scheduling isolates the dependency chain that actually gates LCP.
- `range`: Measurement statistics (median of ≥ 5 runs, spread, same conditions) keep lab noise from being reported as improvement.
- `range`: The red-team pass (analytics events, forms, SEO markup, screenshot diffs) guards against the common way deferring scripts breaks marketing tracking.
- `range`: The approval-gated A/B holdback, borrowed from growth experimentation, tests whether speed changes business results. Effect: needs analytics access and traffic.
- Approval lines: third-party tag removal, production deploys, CDN/hosting or paid services, other pages, CI budgets, and the conversion pilot. Each adds scope, cost, or cross-team impact.
- Skipped: none. All three lenses had a real improvement.
- Owner actions:
  - Confirm LCP as the meaning of "load".
  - Provide source, staging, CrUX or RUM, and lab-testing access.
  - Name the owners of the third-party tags.
  - Decide each "With my approval only" line.

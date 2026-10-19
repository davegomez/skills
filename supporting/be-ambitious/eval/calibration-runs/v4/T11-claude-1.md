```text
Make our marketing website's home page load faster on mobile. It currently takes about 10 seconds. The page exists to turn mobile visitors into leads or customers. Assumption: the real goal is that visitors on ordinary phones and networks see the pitch and can act before they leave, so judge the work on user-centric metrics, not a single score.

First checks (report what is missing, then continue with what the available access supports):
- Confirm access to the site's source repo, hosting/CDN configuration, and the production URL.
- Pin down what "10 seconds" measures: which metric (full load, LCP, time to interactive), which device, which network, and lab or real users. Reproduce it before changing anything.
- Check whether field data exists: the CrUX report for the origin or URL, any RUM, or analytics with bounce and conversion data for the home page.
- List every third-party script on the page (tag manager, analytics, chat, A/B testing, pixels) and who owns each.

Baseline from raw evidence, not summaries:
- Run WebPageTest on an emulated mid-tier Android (Moto G class) over throttled 4G, from one fixed test location. Take the median of 9 runs and keep the filmstrip, waterfall, and request list.
- Record a Chrome DevTools Performance trace with CPU throttling to see main-thread work: long tasks, script evaluation, layout.
- Use Lighthouse for diagnostics only. The trace and waterfall are the evidence.
- Pull CrUX/field p75 for LCP, INP, CLS, and TTFB if available.

Find and fix the bottleneck:
- Treat the waterfall as a dependency graph and identify the critical path to the LCP element.
- Fix the largest contributor on that path, re-measure, and repeat. Do not apply a checklist blindly.
- Likely areas, to confirm against the trace:
  - LCP image: format (AVIF/WebP), responsive srcset/sizes, fetchpriority, no lazy-loading above the fold.
  - Render-blocking CSS and JS: critical CSS inline, defer the rest.
  - JS bundle size: source-map-explorer or webpack-bundle-analyzer, code splitting, dead code.
  - Web fonts: preload, font-display, subsetting.
  - Server response: TTFB, CDN caching and cache headers, Brotli compression.
  - Layout shift sources.
- Run an ablation study on third-party scripts. Block each one in WebPageTest, one at a time, and measure its cost to LCP and main-thread time. Rank them by cost. Deferring or lazy-loading a script without removing it is in scope.
- Aim for lab LCP ≤ 2.5 s, TBT ≤ 200 ms, and CLS ≤ 0.1 on the baseline test profile, using the critical-path method above. When one approach stalls, try the next: server and CDN, then images, then CSS, then JS, then third parties. Report a miss only after that.

Red-team before calling it done. A faster page that breaks the funnel is a regression. Verify that:
- Forms submit.
- Analytics and conversion events still fire, compared against the event log before the change.
- SEO-relevant markup is intact: title, meta, structured data, server-rendered content.
- Visual screenshot diffs at mobile and desktop widths show no unintended changes.

Deliver changes through the team's existing review and deploy process.

With my approval only: remove or replace any third-party script, or change how it loads in a way its owner would notice (consent, tracking accuracy).
With my approval only: add real-user monitoring (e.g. the web-vitals library reporting to our analytics). This is new data collection.
With my approval only: add a performance budget to CI (e.g. Lighthouse CI or WebPageTest API thresholds) that fails builds on regression.
With my approval only: run an experiment that serves different versions to different users.

Report:
- Before/after table on the same test profile: median of 9 runs for LCP, FCP, TBT, CLS, TTFB, total bytes, and request count.
- Each change paired with its measured delta.
- The third-party ablation ranking.
- Red-team results.
- If field data exists, before/after p75 field metrics and home-page bounce/conversion rates. Label these as observational, not causal, and unverified until the field window (CrUX uses 28 days) covers enough post-release traffic.

Judge: WebPageTest on the identical device, network, and location profile, median of 9 runs before and after.
Pass: the metric behind the reported ~10 s and LCP are both measurably lower after the change, with no red-team failures.
Stretch, reported separately as met or missed: lab LCP ≤ 2.5 s, TBT ≤ 200 ms, CLS ≤ 0.1; field p75 LCP ≤ 2.5 s, INP ≤ 200 ms, CLS ≤ 0.1 once the field window elapses.
Missing field data leaves the field stretch and the conversion observations unverified.
```

**Ledger**
- `altitude`: The outcome moves from "home page loads faster" to "mobile visitors see the pitch and can act before leaving." That means field Core Web Vitals plus bounce/conversion, reported as observational. It needs analytics or CrUX access, and RUM sits behind approval.
- `depth`: The prompt pins down what "10 s" means and reproduces it on a fixed device and network profile before any changes. This prevents optimizing the wrong metric.
- `depth`: Critical-path analysis of the trace and waterfall, with a fix-and-remeasure loop. This replaces generic Lighthouse checklists and targets the actual bottleneck.
- `depth`: Hard target of LCP ≤ 2.5 s, TBT ≤ 200 ms, CLS ≤ 0.1, with fallback approaches. It is reported separately, and the owner's bar of "faster" stays the pass condition.
- `depth`: The judge is the median of 9 runs on an identical profile, which keeps run-to-run noise from being read as a win.
- `range`: An ablation study (ML practice) on third-party scripts shows the cost of each tag. Removing or replacing any of them is behind approval because it affects marketing data.
- `range`: A red-team regression check covers forms, analytics events, SEO markup, and visual diffs. It catches speedups that silently break the funnel.
- `range` (approval only): a CI performance budget, real-user monitoring, and split experiments. These are new workflows or data collection.
- Skipped: none. All three lenses contribute.
- Owner actions:
  - Confirm repo, hosting/CDN, and analytics/CrUX access.
  - Say what device and measurement produced "10 seconds."
  - Identify the owners of the third-party scripts.
  - Decide on the four approval-only lines.

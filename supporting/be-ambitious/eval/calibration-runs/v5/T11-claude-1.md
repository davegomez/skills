```text
Make our marketing website's home page load faster on mobile. It currently takes about 10 seconds. Assumption: the goal behind this is that more mobile visitors stay on the page and act on it (sign up, request a demo, or whatever the page's primary call to action is).

1. First checks. Verify each dependency below before relying on it. Name any that are missing and continue only with work the available access supports.
   - Access to the site's source repo, build config, and a preview or staging deploy.
   - Hosting and CDN settings: cache headers, compression, HTTP/2 or HTTP/3, image service.
   - Any real-user monitoring or analytics already installed.
   - Whether the home page has Chrome UX Report (CrUX) field data, via PageSpeed Insights or the CrUX API.
   - A mid-tier Android device, or a throttling profile to stand in for one.

2. Baseline. Start from raw evidence, not the "10 seconds" summary.
   - Measure first, and record which metric the "about 10 seconds" matches: first contentful paint (FCP), largest contentful paint (LCP), time to interactive, or fully loaded. Report it if no metric matches.
   - Capture at least 5 cold-cache runs on a mid-tier mobile profile (Moto G Power class, 4G-throttled). Use Lighthouse CLI and Chrome DevTools Performance traces.
   - Record median and spread for each run set: time to first byte (TTFB), FCP, LCP, interaction to next paint (INP, or total blocking time as its lab proxy), cumulative layout shift (CLS), total bytes, and request count.
   - Pull CrUX p75 field values for the same metrics if they exist.
   - Keep the filmstrip and the request waterfall.

3. Diagnose the critical path.
   - Identify the LCP element. Split its time into TTFB, resource load delay, resource load duration, and render delay. This shows which phase dominates.
   - Treat the waterfall as a dependency graph. Find the chain of render-blocking requests that sets LCP (critical-path analysis). Fix that chain first, not the biggest file.
   - Run the page with each third-party script blocked in turn (Lighthouse/DevTools request blocking). This measures each tag's individual cost in LCP and blocking time. Tag managers, chat widgets, A/B tools, and pixels are often the dominant cost on marketing sites.
   - Analyze JS and CSS bundles (source-map-explorer or the bundler's analyzer). Check for unused code, oversized dependencies, and missing code splitting.

4. Fix, in order of measured impact.
   - LCP resource: preload or `fetchpriority="high"` on the LCP image, responsive `srcset`/`sizes`, AVIF/WebP, correct dimensions, and no lazy-loading above the fold.
   - Render-blocking resources: inline critical CSS, defer non-critical JS, and use `font-display` with preloaded, subset fonts.
   - Server and caching: compression, long cache lifetimes on hashed assets, and a CDN cache for the HTML where safe.
   - Third parties: defer or lazy-load in-scope third parties that their tests show to be costly.
   - Keep changes on a branch and validate them on a preview deploy. Ship through the team's normal release process.

5. Stretch target. Aim for mobile lab median LCP ≤ 2.0 s with total blocking time ≤ 200 ms and CLS ≤ 0.1 under the baseline profile. Use the critical-path and per-tag measurements to choose fixes. When one approach stalls, try the next one (for example: image pipeline, then server-side rendering or static generation of the hero, then edge caching) before reporting a miss.

6. Red team. Before calling it done, check that the optimizations did not break what the page exists for.
   - Analytics and attribution events still fire. Compare tag-firing before and after in DevTools or the tag manager's preview mode.
   - Forms and CTAs work, and consent banners still gate tags correctly.
   - Content is still present in the server-rendered HTML for SEO.
   - The page still works on the worst case: low-end device, slow 3G, cold cache.

7. Statistics. Treat lab runs as noisy samples. Report the before/after median with a bootstrap 95% confidence interval on the difference. Count a change as an improvement only if the interval excludes zero.

With my approval only: remove or replace any third-party tag. Each has a business owner, so present its measured cost so they can decide.
With my approval only: run tests on public WebPageTest or any external testing service. This publishes the URL and results.
With my approval only: make paid or plan-level changes to hosting, CDN, or image services.
With my approval only: add a performance budget check (Lighthouse CI with LCP/bytes thresholds) to CI so regressions fail the build.
With my approval only: after release, track CrUX/real-user-monitoring (RUM) p75 mobile LCP over the next 28-day window. Compare mobile bounce and primary-CTA conversion before and after against the same period's desktop traffic as a control, and report it as observational, not causal.

Judge:
- Pass: under identical lab conditions, the mobile home page's median LCP, and the metric that matched "about 10 seconds", are lower after than before, with the 95% CI on the difference excluding zero. The red-team checks in step 6 also all pass.
- Stretch: report LCP ≤ 2.0 s / total blocking time ≤ 200 ms / CLS ≤ 0.1 separately as met or missed, with the run count, device profile, and medians.
- Field results: if CrUX or RUM data is unavailable or the 28-day window hasn't elapsed, leave the field and conversion results unverified.
```

- `depth`: Measure first and test what "10 seconds" actually means. This replaces an anecdote with a baseline on named metrics, so "faster" becomes checkable.
- `depth`: LCP phase breakdown, bundle analysis, and specific fixes target the dominant cost rather than generic tweaks.
- `depth`: The hard stretch target (LCP ≤ 2.0 s lab) is tied to the same metric and conditions as the baseline. The owner's "faster" bar stays the pass condition.
- `range`: Critical-path analysis from operations research finds which chain of requests actually gates rendering.
- `range`: Statistics (repeated runs, bootstrap confidence interval) keeps lab noise from being reported as a win.
- `range`: Third-party tags are treated as per-tag cost/benefit decisions for their owners. Removals sit behind approval because they affect marketing tooling.
- `range` (red team): Checks on attribution, forms, consent, SEO, and the worst-case device catch speedups that silently break the page's purpose.
- `altitude`: The outcome rises from "the home page loads faster" to "more mobile visitors stay and convert". This is behind approval because it needs field data, analytics access, and a 28-day observation window. It is observational, with desktop as a control.
- `altitude` (approval): A CI performance budget keeps the gain from eroding. This is a new CI workflow.
- Skipped: none. All three lenses had a permitted contribution.
- Owner actions:
  - Confirm repo, preview deploy, CDN, and analytics/RUM access, and whether CrUX data exists.
  - Name the page's primary CTA.
  - Decide on tag removals, external testing services, paid CDN or image changes, the CI budget, and post-release field tracking.

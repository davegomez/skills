```text
Make our marketing website load faster on mobile, starting with the home page, which takes about 10 seconds to load on mobile.

Goal (assumption: speed matters because slow mobile loads cost visitors, conversions, and search ranking; confirm or correct): a first-time mobile visitor sees the main message and can act on it quickly, and the site stays fast after this work.

1. Pin down the baseline before changing anything.
   - "About 10 seconds" may mean LCP, onload, fully loaded, or perceived time. Measure each and record which one matches the reported number.
   - Use one fixed lab setup for all before/after comparisons: WebPageTest or Lighthouse CLI, a mid-tier Android profile, a throttled 4G connection, cold cache, and a test location near real visitors.
   - Take at least 5 runs per page. Report the median and spread, because a single run is too noisy to compare.
   - Pull field data where it exists: CrUX (PageSpeed Insights or the CrUX API) for p75 LCP, INP, and CLS on mobile. This shows what real devices experience, which lab runs only approximate.

2. Find the bottleneck from raw traces, not from a score.
   - Use the WebPageTest waterfall and filmstrip and a Chrome DevTools Performance trace.
   - Split LCP into its four phases: TTFB, resource load delay, resource load duration, and render delay. Fix the largest phase first, then re-measure. That phase is the constraint, and work elsewhere won't move the number.
   - Inspect these with named tools:
     - JS bundle composition (source-map-explorer or webpack/rollup bundle analyzer): finds unused or oversized code.
     - Third-party scripts (WebPageTest domain breakdown, Request Map): finds tag-manager and widget cost.
     - Images and the LCP element: format (AVIF/WebP), responsive srcset/sizes, preload plus fetchpriority="high" for the hero, no lazy-loading above the fold.
     - Fonts: subsetting, font-display, preload.
     - Render-blocking CSS and JS: inline critical CSS, defer the rest.
     - Server and CDN: TTFB, caching headers, Brotli, HTTP/2 or HTTP/3.
   - Apply fixes that the repo and current hosting already allow.

3. Aim for p75 mobile LCP ≤ 2.5 s, INP ≤ 200 ms, and CLS ≤ 0.1 (Core Web Vitals "good"), plus lab LCP ≤ 2.5 s on the fixed setup.
   - Treat these targets as solvable. When one approach stalls, try the next phase or technique in this order: TTFB, LCP resource, render-blocking, JS, third parties.
   - Report a miss only after trying them.
   - The pass bar is still the owner's: measurably faster than baseline. Report the stretch targets separately, met or missed.

4. Red-team every change before calling it done.
   - Visual regression: screenshot diff of the home page at mobile and desktop widths, before vs after.
   - Layout shift: check CLS did not get worse.
   - Function: forms, CTAs, navigation, and consent banner still work.
   - Analytics: marketing and analytics tags still fire, verified in the network panel or tag debugger. Silently breaking attribution is the most likely costly side effect.
   - SEO: meta tags, structured data, and indexable content are unchanged.
   - Worst case: test the slowest device profile and a far-away test location.

5. Apply the same method to the other high-traffic marketing pages once the home page is done. Use analytics or CrUX to rank which pages matter.

With my approval only: remove, delay, or replace any third-party marketing or analytics tag, since that changes data the marketing team relies on.
With my approval only: change hosting, CDN, or image-service configuration, or adopt any paid service.
With my approval only: add a real-user monitoring script (e.g., the web-vitals library sending to our analytics), since that adds data collection.
With my approval only: add a performance budget to CI (e.g., Lighthouse CI or size-limit) that fails builds exceeding agreed LCP and JS-size limits.
With my approval only: run an A/B test or measured before/after comparison of mobile bounce and conversion rates, to check whether the speedup changes visitor behavior.

First checks:
- Confirm access to the site's source repo and build.
- Confirm a staging or preview environment to measure against.
- Confirm WebPageTest or Lighthouse CLI is available.
- Check whether the origin has CrUX data (low-traffic sites may not).
- Confirm deploy access and the normal release process.
- Name anything missing and continue with the work the available access supports.

Judge:
- Run the fixed lab setup (same device profile, network, location, cold cache, ≥5 runs) on the home page before and after.
- Pass when the median of the metric that matched "about 10 seconds" is lower than baseline, and all of these hold:
  - the visual diff shows no unintended changes;
  - CLS is not worse;
  - forms and CTAs work;
  - every analytics tag still fires (or was changed only with approval).
- Report baseline, after, and spread for LCP, INP or TBT, CLS, total bytes, and JS bytes. Attribute each change's effect where measured.
- Report the stretch targets as met or missed. Field (CrUX) results need about 28 days of post-release data; until then, mark them unverified.
```

- `depth`: defines which metric "10 seconds" actually is and fixes the lab conditions with ≥5 runs, so "faster" becomes a reproducible comparison rather than a guess.
- `depth`: LCP phase breakdown from raw traces, plus named tools (bundle analyzer, waterfall, Request Map), targets the real bottleneck first. No cost; needs WebPageTest or Lighthouse CLI.
- `depth`: hard target of Core Web Vitals "good" at p75, reported separately from the owner's "faster" bar.
- `altitude`: from "the home page loads faster" to "mobile visitors see and act on the pitch, and the site stays fast." This adds other key pages (in scope) and, behind approval, a CI performance budget and a conversion check. Benefit: the gain lasts and can be tied to business results. Cost: CI setup time and an experiment window.
- `range`: theory of constraints (fix the largest LCP phase first), experimental statistics (median and spread, same conditions), and red-team checks (visual diff, analytics and tag verification, SEO, worst-case device). These catch the common failure where a speedup silently breaks attribution or layout.
- Skipped: none; all three lenses contributed.
- Owner actions:
  - Confirm the assumed goal (conversions or SEO).
  - Confirm access to the repo, staging, deploys, WebPageTest or Lighthouse, and CrUX.
  - Decide on each approval line: third-party tag changes, hosting/CDN or paid services, RUM collection, the CI budget, and the A/B or conversion test.

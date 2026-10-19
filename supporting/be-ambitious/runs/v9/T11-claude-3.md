```text
Make our marketing website load faster. The home page takes about 10 seconds to load on mobile.
Assumption: the goal is that mobile visitors see and can use the home page before they give up, and that the home page passes Google's Core Web Vitals (LCP, INP, CLS at p75), which also affect search ranking.
Test the "about 10 seconds" claim from raw evidence before changing anything. Trace the live home page on one fixed mobile lab profile: WebPageTest or Lighthouse, a mid-tier Android device (Moto G class), Slow 4G throttling, cold cache, at least 5 runs. Record the median and the spread. State which metric the 10 seconds matches: LCP, the load event, fully loaded, or none. Pull the home page's CrUX field data (PageSpeed Insights or CrUX API) if it exists. Use this same profile and URL for every before/after comparison.
Find the bottleneck from the trace and the request waterfall, not from guesses. Split LCP into its 4 subparts: TTFB, resource load delay, resource load duration, and element render delay. Fix the largest subpart first, re-measure on the fixed profile, and keep a change only if the measurement shows it helped. Then move to the next-largest subpart.
Apply a method only where the trace shows it bears on the bottleneck:
- TTFB: server or CDN caching and Brotli compression.
- Load delay: make the LCP resource discoverable in the HTML with preload or fetchpriority="high", and never lazy-load it.
- Load duration: responsive AVIF/WebP images with srcset/sizes, correctly sized.
- Render delay: inline critical CSS, defer non-critical JS, size the JS bundle with source-map-explorer or a bundle analyzer, and self-host and subset fonts with font-display.
- Total Blocking Time: break up long tasks.
Aim for a median mobile lab LCP of 1.5 s or less, well past the 2.5 s "good" threshold, with CLS of 0.05 or less and TBT of 200 ms or less, using the bottleneck-first loop above. When one approach stalls, try the next before reporting a miss. "Faster than the baseline" remains the pass condition.
Red-team the result. Confirm that LCP did not improve by hiding, shrinking, delaying, or swapping out the hero element. Compare filmstrips or screenshots to confirm the above-the-fold content is unchanged. Confirm that navigation, forms, and the analytics tags we keep still work.
Report the following:
- A before/after table on the fixed profile: median and spread for LCP, CLS, TBT, and total transfer size.
- Each kept change with its measured effect.
- What the 10 seconds turned out to measure.
- Field CrUX data where it exists.
- Stretch attainment, reported separately as met or missed.
Scope: the marketing website, with the home page as the measured target. Changes to shared assets that also affect other pages are in scope.
With my approval only: remove, defer, or replace third-party marketing or analytics tags, because that changes what data we collect.
With my approval only: change the hosting or CDN configuration or plan where the change adds cost, such as an image CDN or a paid caching tier.
With my approval only: add a Lighthouse CI performance budget to the CI pipeline that fails builds exceeding the achieved LCP and JS-weight numbers.
With my approval only: add real-user monitoring with the web-vitals library, reporting to our existing analytics, to track mobile p75 LCP, INP, and CLS after release.
First check: confirm access to the site source, a local or staging build of the home page, and the live home page URL. Name anything missing and continue only with supported, authorized work.
First check: confirm whether CrUX has field data for the home page or origin. If it does not, field results stay unverified and the lab profile is the only judge.
Judge: on the fixed mobile profile (same URL, device, Slow 4G, cold cache, at least 5 runs), the median lab LCP after the changes is lower than the baseline median by more than the baseline's run-to-run spread, CLS and TBT do not regress, the filmstrip comparison shows the same above-the-fold content, and navigation, forms, and kept analytics tags work; the 1.5 s LCP stretch is reported separately as met or missed, and missing baseline traces leave the result unverified.
```

- `depth`: the prompt tests the "10 seconds" belief against raw traces and CrUX field data before any fix. This prevents optimizing the wrong metric.
- `depth`: LCP subpart breakdown with bottleneck-first, measure-each-change iteration, plus named methods per subpart. Effort goes to what the trace shows instead of a generic checklist.
- `depth`: hard target of LCP ≤ 1.5 s, CLS ≤ 0.05, TBT ≤ 200 ms. This is past Google's "good" bar, reported separately from the owner's "faster" pass condition.
- `altitude`: the outcome moves from "home page loads faster" to "mobile visitors see a usable page in time and the page passes Core Web Vitals". Field verification is optional RUM behind approval. Costs a small script and a data-collection change.
- `range` (experimental measurement): a fixed lab profile, at least 5 runs, and a pass that must beat run-to-run spread. This keeps noise from counting as a win.
- `range` (red team): checks for LCP gaming, such as hiding or swapping the hero, and for broken forms, navigation, or analytics. This catches a "fast" page that lost its purpose.
- Approval-gated: tag removal (affects marketing attribution), paid hosting or CDN changes (cost), the CI performance budget (new recurring workflow), and RUM (new data collection).
- Skipped: none. Each lens added a distinct contribution.
- Owner actions:
  - Confirm source, staging, and URL access.
  - Confirm whether CrUX data exists.
  - Decide on the 4 approval lines: tags, hosting/CDN cost, CI budget, RUM.
  - Production deployment follows your normal release process; this prompt doesn't authorize it.

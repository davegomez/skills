```text
Make our marketing website's home page load faster on mobile. It currently takes about 10 seconds to load on mobile.

Goal (assumption: speed matters because mobile visitors leave before they see the message or act on it): a first-time visitor on a typical phone sees the main content, can use it, and does not see the page jump around, well before they give up.

First checks. Name anything missing and continue only with work the available access supports:
- Access to the site's source, its build, and a staging or preview URL where changes can be tested.
- What "about 10 seconds" refers to (Largest Contentful Paint, full page load, or a stakeholder's stopwatch) and on what device and network. If no one knows, measure all of them and say which one matches.
- Whether field data exists: the Chrome UX Report (CrUX) for this origin, an existing real-user monitoring (RUM) source, or analytics with page timing and bounce or conversion data.
- That Lighthouse and/or WebPageTest can be run against staging and production.
- How changes reach production under the existing process.

Method:
1. Baseline from raw evidence. Run WebPageTest or Lighthouse on the production home page with one fixed mobile profile (mid-tier Android, throttled 4G), at least 5 runs. Record median and spread for TTFB, LCP, Total Blocking Time, CLS, and full load time. Save the waterfall, a Chrome DevTools performance trace, and a filmstrip. Pull CrUX or RUM p75 values for LCP, INP, and CLS where they exist. Reuse this exact profile for every later comparison.
2. Find the critical path before changing anything. Identify the LCP element. Split LCP into its four parts: server response, resource load delay, resource load time, and render delay. Fix the largest part first. Use the DevTools Coverage tab and a bundle analyzer to find unused JS and CSS. List every third-party request (tag managers, chat, A/B tools, video embeds) with its bytes and main-thread time.
3. Apply fixes that target what step 2 found. The usual candidates are:
   - Images: right-sized responsive images (srcset/sizes) in AVIF or WebP, `fetchpriority="high"` on the LCP image and no lazy-loading on it, lazy-loading for images below the fold.
   - Render-blocking resources: inline critical CSS, defer non-critical JS, split code by route.
   - Fonts: subset them, preload the one the LCP text uses, set `font-display`.
   - Third-party scripts: defer or load after interaction.
   - Delivery: compression, cache headers, CDN caching of HTML and assets.
   - Layout stability: reserve dimensions for images and embeds to keep CLS low.
   Measure after each significant change so the gain can be attributed to it.
4. Treat lab results as noisy measurements. Compare medians across at least 5 runs per variant. Call a change an improvement only when the gap is larger than the run-to-run spread.
5. Red-team the result before shipping:
   - Screenshot-diff the home page at mobile and desktop widths against the baseline.
   - Confirm every analytics, attribution, and consent beacon that fired before still fires, by diffing the network request lists.
   - Check that SEO-relevant markup (title, meta, structured data, crawlable text) is unchanged.
   - Check that forms and calls to action still work.
6. Aim for the Core Web Vitals "good" thresholds on the fixed lab profile: LCP ≤ 2.5 s, TBT ≤ 200 ms, CLS ≤ 0.1. Treat them as solvable. When one approach stalls, try the next lever from step 2 before reporting a miss. Report this stretch separately from the pass condition, as met or missed per metric.

With my approval only: remove, replace, or change the configuration of any third-party marketing or analytics tag. Deferring a tag's load without changing what it collects is in scope.
With my approval only: change CDN, hosting, or DNS configuration, or adopt any paid service (image CDN, RUM vendor).
With my approval only: add a performance budget check (Lighthouse CI or similar) to CI so future changes cannot regress these metrics.
With my approval only: run an A/B or split test to measure the effect on bounce or conversion.

Report:
- Baseline vs. after for each metric, as median and spread, on the same profile.
- The LCP breakdown before and after.
- Each change with the gain attributed to it.
- Red-team results.
- Stretch attainment.
- If analytics access exists, before/after bounce and conversion as observed correlation only, not a causal claim.

Judge: WebPageTest or Lighthouse on the fixed mobile profile, at least 5 runs per variant.
Pass condition: median LCP and median full load time are both lower than baseline by more than the run-to-run spread. The screenshot diffs show no unintended changes. Every pre-existing analytics and consent beacon still fires. The forms and calls to action work.
Field confirmation: CrUX p75 LCP, INP, and CLS for the home page on mobile, read once 28 days of post-release data exist. Until then, the field result is unverified.
```

- `altitude`: The original outcome is a faster home page. The improved outcome is that mobile visitors see and can act on the content before leaving, with field p75 confirmation and an optional regression budget. CI and A/B testing are behind approval.
- `depth`: Raw waterfalls, traces, and CrUX/RUM data replace "it feels slow." The LCP breakdown, coverage, and third-party audit aim fixes at the actual bottleneck. Adds no new access beyond the site and test tools.
- `depth`: The stretch target is the Core Web Vitals "good" thresholds, reported separately from the owner's "faster" bar. This may take more iteration time.
- `depth`: The prompt first checks what "10 seconds" actually measures, so the fix moves the number people complain about.
- `range`: Experimental statistics (fixed profile, repeated runs, comparing medians against spread) keep lab noise from being mistaken for gains.
- `range`: A red-team pass (visual diff, beacon diff, SEO and form checks) catches the usual cost of speed work: broken tracking or layout. This adds test time and protects the marketing team's data.
- Skipped: none. All three lenses are fit.
- Owner actions:
  - Confirm access to source, staging, and the deploy path.
  - Say what the 10-second figure measured, if known.
  - Grant CrUX, RUM, or analytics access.
  - Decide on the four approval-gated items: tag changes, CDN or paid services, the CI budget, and A/B testing.
  - Schedule the 28-day field check.

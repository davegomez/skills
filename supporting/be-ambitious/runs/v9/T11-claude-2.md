```text
Make our marketing website load faster. The home page takes about 10 seconds to load on mobile.
Assumption: the site exists to turn mobile visitors into leads or sign-ups, so the speed that matters is how fast a visitor on a mid-range phone and a slow network sees the main content and can act on it.
Assumption: "load" means the time until the main content is visible, measured as Largest Contentful Paint (LCP). Also record the baseline in whatever metric produced the "about 10 seconds" figure.
Baseline from raw evidence before changing anything. Run WebPageTest, or Lighthouse with mobile throttling if WebPageTest is unavailable, on a mid-tier Android device profile over a 4G-class throttled connection. Do at least 9 runs per page and keep the traces, waterfalls, and filmstrips. Pull Chrome UX Report (CrUX) p75 mobile field data for the origin and home page if it exists. Record LCP, Time to First Byte (TTFB), Total Blocking Time (TBT), Cumulative Layout Shift (CLS), total bytes, and JavaScript bytes.
Test what the 10 seconds is made of before fixing it. Break the home page LCP into its 4 parts: TTFB, resource load delay, resource load duration, and render delay. Find the LCP element. Read the waterfall as a dependency graph and trace the critical request chain to the LCP paint.
Attribute delay to sources by experiment. Rerun with each third-party domain blocked in turn (tag manager, chat, A/B testing, analytics, embeds) and record each domain's LCP and TBT delta. Use the Chrome DevTools Coverage panel and a bundle analyzer to measure unused CSS and JS.
Fix in order of measured delta. Typical fixes:
- For the LCP image: right-sized AVIF/WebP with srcset, fetchpriority="high", and no lazy-loading.
- For CSS: inline the critical CSS and defer the rest.
- For fonts: subset them, preload them, and use font-display.
- For JavaScript: defer or delay non-critical scripts, and load third-party tags after LCP or on interaction.
- For the server: Brotli compression, CDN caching of HTML and static assets, and preconnect to required origins.
Apply shared-template and shared-asset fixes site-wide. Measure the 3 highest-traffic marketing pages besides the home page before and after.
Aim for p75 mobile LCP ≤ 1.5 s on the home page, with CLS < 0.1 and TBT < 200 ms in the lab configuration above. Use the LCP breakdown and per-domain attribution to choose each next fix. When one approach stalls, try the next before reporting a miss. The pass bar remains a faster home page than the baseline. Report the stretch result separately, met or missed.
Treat measurements statistically. Compare medians of at least 9 runs per condition under identical test settings, and report the run range so noise is not reported as improvement.
Red-team each change for hidden breakage, because marketing depends on tracking:
- Diff the full-page and above-the-fold screenshots against the baseline.
- Confirm in the network log that every analytics, attribution, and conversion event that fired in the baseline still fires, including when a tag is delayed until after LCP.
- Confirm that forms and calls-to-action still work.
Deliver a short report with the baseline, the LCP breakdown, the per-third-party attribution, each change with its measured delta, the before/after table for each measured page, and the stretch result.
With my approval only: remove any third-party script entirely. For each one, list the script, its business owner, and what data or feature stops.
With my approval only: any paid or plan-level change, such as a CDN or hosting plan upgrade or an image-optimization service.
With my approval only: add a Lighthouse CI performance budget to the build pipeline that fails builds when home page mobile LCP or JS bytes exceed the newly shipped values.
With my approval only: after release, run a split test of the optimized home page against the current one using existing analytics, and report the mobile conversion-rate difference with its confidence interval.
First check: access to the site source, a working build, a preview or staging URL that matches production, and the release process for shipping changes.
First check: where the "about 10 seconds" figure came from (tool, device, network, and metric), so the baseline reproduces it under comparable conditions.
First check: whether CrUX has field data for the origin and home page, and whether WebPageTest or an equivalent test runner is available.
First check: the list of third-party tags and the events each must fire, and, for the approved split test, analytics access and enough mobile traffic to detect a difference.
If any check fails, name the missing dependency, continue only with supported, authorized work, and mark the affected result unverified.
Judge: on the same tool, device profile, network throttle, and test location as the baseline, the median of ≥9 runs of the optimized home page beats the median of ≥9 baseline runs on the baseline's metric and on LCP, with run ranges reported; pass only if both medians improved, the screenshot diff shows no differences beyond a listed set of intended changes, every baseline analytics/conversion event still fires, and forms and calls-to-action work; report the ≤1.5 s LCP stretch separately as met or missed; field p75 improvement stays unverified until CrUX or analytics covers a full post-release window.
```

- `depth`: the work starts from raw traces, waterfalls, and CrUX field data, plus an LCP breakdown and critical-chain analysis, instead of guessing fixes. This targets the actual cause of the 10 s.
- `depth`: blocking each third-party domain in turn tests whether the cause is the site's own code or marketing tags. It costs extra test runs.
- `depth`: the hard target is p75 mobile LCP ≤ 1.5 s, past the 2.5 s "good" threshold. It is reported separately. The pass bar stays "faster than baseline."
- `range` (statistics): medians of ≥9 runs with ranges keep lab noise from being reported as a win.
- `range` (operations research): treating the waterfall as a dependency graph shows which fixes are on the critical path and which only reduce bytes.
- `range` (red team / marketing ops): screenshot diffs and tag-event checks catch the main risk of speed work, which is broken tracking or layout.
- `altitude`: the original outcome is "a faster home page." The improved one is a site that stays fast and is measured against conversion. It adds a CI performance budget and a post-release split test, both behind approval. The split test is outward-facing and touches traffic and analytics data.
- `altitude`: shared fixes are applied site-wide and measured on the top 3 pages, which matches "marketing website" in the task. This adds measurement time.
- Approval-gated: removing scripts (changes marketing data), paid CDN or service changes (cost), the CI budget (a new workflow), and the split test (outward-facing).
- Skipped: none. All three lenses contributed.
- Owner actions:
  - Confirm source, build, staging, and release access.
  - Say where the 10 s figure came from.
  - Provide the tag list with required events.
  - Approve or decline each of the 4 approval-gated lines.

```text
Make our marketing website load faster, starting with the home page, which takes about 10 seconds to load on mobile.

Assumption: the goal behind "faster" is that mobile visitors see the pitch and can act on it before they leave, so the improvement is measured as real-user mobile experience, not only lab scores.
Assumption: "load" in "about 10 seconds" has not been tied to a metric yet. Establish which one first.

First checks, before any changes:
- Confirm access to the site's source, a way to build it, and a preview or staging URL that can be tested from outside.
- Confirm which measurement tools are available: Lighthouse, WebPageTest (or a self-hosted equivalent), and Chrome DevTools with CPU and network throttling.
- Check for field data: the Chrome UX Report (CrUX) for this origin and URL, and any existing real-user monitoring (RUM) or analytics that records Web Vitals.
- List every third-party script on the home page (tag managers, analytics, chat, A/B testing, consent, video, fonts) and who owns each one.
- Name any missing dependency, then continue only with the work the available access supports.

1. Reproduce and define the baseline.
- Test the home page on a mid-tier Android profile (Moto G Power class, 4x CPU slowdown, Slow 4G), cold cache, from a test location near the main audience.
- Do at least 5 runs and record the median and spread for TTFB, FCP, LCP, Total Blocking Time, CLS, total bytes, request count, and fully loaded time.
- State which of these metrics matches the reported ~10 seconds. If none do, report the mismatch.
- Record field p75 mobile LCP, INP, and CLS from CrUX or RUM where available. Label lab and field numbers separately.

2. Find the critical path, not a checklist.
- Use a WebPageTest waterfall and filmstrip plus a DevTools performance trace to identify the LCP element.
- Split LCP time into its four parts: TTFB, resource load delay, resource load duration, and element render delay. Fix the largest part first, then re-measure; the bottleneck moves after each fix.
- Use DevTools Coverage and a bundle analyzer to find JavaScript and CSS that ship but are not used above the fold.
- Measure each third-party script's cost by blocking it in WebPageTest and comparing.

3. Fix in order of measured impact. Typical levers, used only where the trace shows they matter:
- Server and CDN caching and compression (Brotli), plus HTTP/2 or HTTP/3, to cut TTFB.
- Preload or fetchpriority for the LCP resource, and right-sized responsive images in AVIF or WebP with explicit dimensions.
- Inline critical CSS, and defer or split non-critical JavaScript.
- font-display plus preloading and subsetting for fonts.
- Lazy-loading for media below the fold.
- Deferring or facading heavy embeds.

4. Aim for a lab median LCP at or under 2.5s and TBT under 200ms on the step 1 device and network profile, with page weight under 1 MB, using the critical-path method above. Treat this as solvable: when one lever stalls, try the next before reporting a miss. The owner's bar remains "measurably faster than the baseline."

5. Red-team the result before calling it done:
- Re-test with the consent banner shown, a cold DNS and connection, and a far test location.
- Confirm that forms submit and analytics and marketing events still fire, by comparing network requests before and after.
- Confirm there is no visual regression on the home page at mobile and desktop widths, using screenshot diffs.
- Confirm that meta tags and structured data are unchanged.

With my approval only: remove, replace, or delay any third-party marketing or analytics script, after its owner has been told what data or behavior changes.
With my approval only: deploy the changes to production.
With my approval only: apply the same method to other high-traffic marketing page templates.
With my approval only: add a performance budget check (Lighthouse CI or equivalent) to CI so that regressions fail the build.
With my approval only: add RUM collection of Web Vitals if none exists.
With my approval only: after deploy, compare mobile bounce rate and conversion on the home page for equal-length periods before and after, noting traffic mix and campaign changes as confounders.

Report: a before/after table using the same metrics, profile, location, and number of runs; what each change contributed; what was tried and dropped; open risks; and stretch-target attainment, stated as met or missed.

Judge: repeated lab measurement under identical conditions (the step 1 profile, at least 5 runs, medians with spread).
- Pass: the home page's median mobile LCP and the metric matching the reported ~10 seconds are both measurably lower than baseline, beyond run-to-run spread, and every step 5 check passes.
- Field p75 Web Vitals stay unverified until RUM data or 28 days of post-deploy CrUX data exist.
- Conversion impact stays unverified unless the approved comparison runs.
```

- `altitude`: The original outcome is a home page that "loads faster." The improved outcome is mobile visitors reaching the pitch in time, confirmed in field data, with the conversion check and site-wide rollout behind approval. This adds field-data access and RUM as dependencies.
- `depth`: The prompt now tests the "10 seconds" claim against defined metrics before any fixes. That stops the work from optimizing the wrong number.
- `depth`: It replaces a generic tips list with LCP sub-part attribution, waterfalls, coverage, and per-script blocking. Effort goes where the trace says the time is.
- `depth`: It sets a hard target of lab LCP ≤2.5s, TBT <200ms, and under 1 MB. That is well past "faster," but the owner's bar stays the pass condition. It costs extra iteration time, and there is no stated budget.
- `range`: From statistics, multiple runs with medians and spread, and lab and field kept separate, so a noisy single run can't fake a win.
- `range`: From theory of constraints, fixing the current bottleneck and then re-measuring, which shows the order of fixes that actually moves LCP.
- `range` (red team): Testing under worst realistic conditions plus checks on analytics, forms, visuals, and SEO. This exposes the risk of a fast page that quietly breaks marketing data. Removing third-party tags affects other teams, so it is behind approval.
- Skipped: none. All three lenses had a distinct contribution.
- Owner actions:
  - Confirm source, build, and preview access, and CrUX or RUM availability.
  - Identify the owner of each third-party script.
  - Decide on the approvals: script changes, production deploy, other templates, CI budget, RUM, and the conversion comparison.

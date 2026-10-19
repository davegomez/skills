```text
Make our marketing website load faster, starting with the home page, which takes about 10 seconds to load on mobile. The goal is a home page that real mobile visitors can see and use quickly, and that stays fast after future changes.

Assumption (inferred, not stated): the speed matters because slow mobile loads cost visitors, leads, and search ranking. Treat this as a hypothesis to check, not a given.

1. First checks. Report each as available or missing before optimizing:
   - Access to the site's source repo and a way to build and run it locally or on staging.
   - Field data: Chrome UX Report (CrUX) / PageSpeed Insights for the home page origin, and any existing real-user monitoring (RUM) or analytics.
   - A lab tool: Lighthouse, and WebPageTest if an API key or account exists.
   If field data is missing, say so, rely on lab data, and label every result "lab only."

2. Verify the "10 seconds" from raw evidence. Find out which metric and condition it describes: field p75 LCP, a lab run on throttled 4G, or one person's phone. Record a baseline of LCP, INP, CLS, TTFB, total transfer size, request count, and main-thread blocking time. Use the field p75 on mobile if available, and a lab profile of a mid-tier Android on Slow 4G with the median of at least 5 runs. Separate observed numbers from estimates.

3. Diagnose from the raw request waterfall and a Chrome DevTools performance trace, not from the Lighthouse score alone. Account for every request: what it is, who owns it, its bytes, and whether it blocks the first render. Check in particular:
   - The LCP element. Find what delays it: server response, render-blocking CSS or JS, a lazy-loaded or oversized hero image, or late discovery.
   - Images: format (AVIF/WebP), responsive srcset/sizes, dimensions, compression.
   - JavaScript: use a bundle analyzer (e.g. source-map-explorer or the build tool's analyzer) to find unused code and hydration cost.
   - Fonts: preload, font-display, subsetting.
   - Third-party tags (analytics, chat, pixels, A/B tools): measure each tag's cost separately with request blocking in WebPageTest or DevTools.
   - Caching and compression headers, CDN usage, TTFB.

4. Fix in order of measured impact on LCP and INP. Prioritize what a mobile visitor perceives: get the hero content and headline painted first, and defer what they do not need in the first seconds. Aim for field p75 LCP ≤ 2.5 s, INP ≤ 200 ms, and CLS ≤ 0.1 (Core Web Vitals "good"), and for lab LCP ≤ 2.0 s on the mid-tier Android / Slow 4G profile, using the fixes above. Treat this as solvable: when one approach stalls, try the next lever in the list before reporting a miss. Report the measured result even if the target is missed. The required bar is a clear, measured improvement over the baseline.

5. Keep it fast. Add a performance budget to CI, using Lighthouse CI or the equivalent, with thresholds for LCP, total JS bytes, and image bytes on the home page, so regressions fail the build. Apply the fixes that are site-wide, such as image pipeline, fonts, caching, and shared bundles, to the rest of the marketing site where they carry over. Spot-check 2 or 3 other high-traffic pages.

6. Red-team before shipping. For each change, check what could break: visual differences at mobile and desktop widths, forms and CTAs still working, analytics and attribution still firing, SEO tags intact. Removing or deferring a marketing tag can silently break attribution, so list each affected tag and the team that owns it.

Requires my approval before acting:
- Removing, deferring, or replacing any third-party marketing or analytics tag.
- Paid changes: a new CDN, hosting tier, image service, or monitoring vendor.
- Adding RUM to production (for example the web-vitals library sending to our analytics).
- Deploying to production.
- Stretch, only if I approve it and analytics access is confirmed: measure whether faster loads changed mobile bounce rate and conversion. Prefer a holdback or A/B test. If that is not approved, compare before and after over matching periods, report the traffic volume and confidence interval, and label confounds such as campaigns and seasonality. Until this runs, the business impact stays unverified.

Deliverables: the code changes; a short report with the baseline vs after table (each number labeled field or lab, with its device and network profile); the cause behind most of the original 10 seconds; the changes made and their individual measured effect where isolable; what was deferred pending approval; and the CI budget config.

Judge: before/after measurements under identical conditions. Lab: median of ≥5 runs, same device profile, same network, same URL. Field: CrUX/RUM p75 after enough post-deploy traffic, noting the 28-day CrUX window.
Pass condition: home page mobile LCP is measurably lower than the verified baseline in lab tests, and the CI performance budget fails on an intentionally introduced regression (for example a large unoptimized image) and passes once it is removed. Field improvement and business impact are reported as unverified until production data exists.
```

**Ledger**
- `altitude`: The original task, "make the home page load faster," becomes a fast home page that stays fast, through a CI performance budget that a deliberate regression can test. Conversion impact is an approval-gated stretch. It adds CI config work, and there is no paid cost unless you approve it.
- `depth`: The prompt first verifies the "10 s" claim. It specifies which metric, field or lab, and which device, so you avoid optimizing the wrong number. No added scope.
- `depth`: Diagnosis uses the raw waterfall, a performance trace, a bundle analyzer, and per-tag blocking, instead of the Lighthouse score. This finds the actual bottleneck, often third-party tags or the hero image.
- `depth`: The hard target is "good" Core Web Vitals plus lab LCP ≤ 2.0 s, with escalation through levers before reporting a miss. Your bar of "faster than baseline" remains the pass condition.
- `range`: From perceptual psychology, the hero content is prioritized for what visitors perceive, not total load. This can improve LCP more than byte-cutting alone.
- `range`: From experiment design, the conversion stretch uses a holdback or a confound-labeled before/after with confidence intervals, so a coincidence isn't claimed as impact. It requires approval and analytics access.
- `range`: A red-team pass catches broken attribution, forms, and SEO tags before ship. The risk sits with tag owners on the marketing side.
- Skipped: none. All three lenses fit, because speed serves acquisition, perf work rewards rigor, and the result must land with mobile visitors.
- **Owner actions:**
  - Confirm repo and staging access, and CrUX, analytics, and WebPageTest access.
  - Decide on tag removal or deferral, together with the tag owners.
  - Approve any paid CDN or vendor, production RUM, production deploys, and the conversion-impact stretch.

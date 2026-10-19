```text
Make our marketing website's home page load faster on mobile. It currently takes about 10 seconds. Assumed goal, to be confirmed: mobile visitors see the main message and can act on it before they leave, without losing the analytics, SEO, or content marketing relies on.

First checks. Report what is missing, and continue only with work the available access supports:
- Access to the site's source, its build and hosting/CDN configuration, and a staging or preview environment.
- Field data: CrUX for the origin or URL (PageSpeed Insights or the CrUX API), plus any real-user monitoring or analytics already collecting speed or bounce data.
- A lab tool that can emulate a mid-range phone on a throttled mobile network: WebPageTest, or Lighthouse/Chrome DevTools with a fixed throttling profile.

1. Define "load" from raw evidence. Find out which metric the 10 seconds is. Measure the home page's baseline on a fixed lab profile (named device emulation, network throttling, location, and cold cache), using at least 9 runs and reporting the median and spread. Record:
   - LCP (when the main content appears), FCP, TTFB, INP or Total Blocking Time, and CLS.
   - Total bytes and request count.
   - Main-thread JavaScript time.
   Pull the field p75 values for the same metrics, if they exist. Check whether lab and field agree before trusting either.

2. Diagnose before you fix. From the waterfall, filmstrip, and a DevTools performance trace, rank the causes by milliseconds of LCP and blocking time each one costs. Check these in particular:
   - The LCP element and what delays it: discovery, priority, size, or format.
   - Render-blocking CSS and JS.
   - Each third-party script's bytes and main-thread cost, listed with its apparent purpose.
   - Web fonts.
   - Server/CDN response, caching headers, and compression.
   - Layout shifts.

3. Fix the biggest costs first, one change at a time, and re-measure after each change so every win is attributed. Typical moves:
   - Responsive, compressed images (AVIF/WebP with srcset/sizes and explicit dimensions).
   - Preload the LCP resource and set fetchpriority on it, and never lazy-load it.
   - Inline critical CSS and defer the rest.
   - Defer or split JS, and remove dead code.
   - Font subsetting and font-display.
   - Long-lived cache headers on hashed assets, Brotli compression, and CDN delivery.
   - Static or server rendering of above-the-fold content where the stack allows it.

4. Guard against breakage. Compare before/after screenshots of the home page at mobile and desktop widths. Confirm that analytics and marketing events still fire with the same names and payloads. Confirm that titles, meta tags, structured data, and canonical URLs are unchanged.

Aim for a lab median LCP of 2.0 s or less and Total Blocking Time of 200 ms or less on the step-1 profile, and for a field p75 LCP of 2.5 s or less (Core Web Vitals "good"). If one approach stalls, try the next ranked cause before reporting a miss. Report this stretch result separately from the pass condition.

With my approval only: remove, replace, or delay any third-party script or tag (analytics, ads, chat, A/B testing, tag manager). Give me the per-script cost table first, so the script's owner can weigh speed against what it provides.
With my approval only: deploy to production, change CDN or hosting configuration, or adopt any paid service.
With my approval only: add real-user monitoring or any new data collection.
With my approval only: add a performance budget check (for example Lighthouse CI) to CI, so regressions fail the build.
With my approval only: run an A/B test or a before/after comparison of bounce and conversion rates to check whether faster loading changed visitor behavior.

Judge: lab measurements before and after the changes, on the identical step-1 profile with 9 or more runs each.
Pass: the after median LCP is lower than the before median by more than the run-to-run spread. Screenshot comparison shows no unintended visual change, analytics events match, and SEO tags are unchanged.
Report: before/after medians and spreads for each metric, the attribution of milliseconds saved to each change, and the stretch result, met or missed.
Field p75 results remain unverified until production traffic has accumulated after deploy. CrUX uses a 28-day rolling window.
```

- `altitude`: Original outcome: a faster home page. Improved outcome: mobile visitors see the message and act before leaving, with analytics and SEO intact. The behavior and conversion check is behind approval because it needs a deploy and possibly an experiment.
- `depth`: Pinning down which metric "10 seconds" means, on a fixed device/network profile with repeated runs, turns a vague complaint into a baseline that can be measured. It costs only lab time.
- `depth`: Diagnosing from waterfall, filmstrip, and trace data, ranked by milliseconds lost, puts the work on the real bottleneck instead of generic tips.
- `depth`: The hard target (LCP ≤ 2.0 s lab, ≤ 2.5 s field p75) is reported apart from the owner's bar of "faster". It may need more iterations within the work.
- `range`: Measurement statistics (medians, spread, a significance margin) keep run-to-run noise from being counted as a win.
- `range`: The per-script cost table works like a budget review. It turns third-party removal into a cost/benefit decision for the people who own those tools, because removing tags can break marketing's data.
- `range` (red team): Screenshot diffs, analytics event checks, and SEO tag checks catch speed wins that quietly break tracking, layout, or search ranking.
- Approval-gated additions: production deploy, CDN or paid changes, third-party script removal, new data collection (real-user monitoring), a CI performance budget, and an A/B or conversion comparison.
- Skipped: none. Every lens produced a concrete change.
- Owner actions:
  - Confirm source, hosting/CDN, staging, and analytics access.
  - Confirm the assumed goal.
  - Decide on each "With my approval only" line, especially third-party script removal and production deploy.
  - Expect field results to lag about 28 days after deploy.

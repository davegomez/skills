```text
Make our marketing website load faster. The home page takes about 10 seconds to load on mobile.
Assumption: the goal is that mobile visitors see the home page's main content and can act on it (sign up, contact, buy) before they give up and leave.
Assumption: "about 10 seconds" reflects what typical mobile visitors on real devices and networks experience, and is not one slow test.
Baseline from raw evidence before changing anything. Find out what the 10-second figure measured (which metric, device, network, first or repeat view). Then reproduce it on a cold-cache first view of the home page, emulating a mid-tier Android phone on a 4G throttling profile in WebPageTest or Lighthouse. Take the median of at least 5 runs and record LCP, FCP, TTFB, TBT, CLS, total bytes, and request count. Pull field data at p75 for mobile (LCP, INP, CLS) from the Chrome UX Report through PageSpeed Insights for the home page URL. Use it to test whether lab and field agree, and report any disagreement.
Diagnose the critical path. Read the waterfall and a Chrome DevTools Performance trace as a dependency graph. Identify the LCP element and the longest chain of requests that blocks it: server response, redirects, render-blocking CSS and JS, web fonts, the LCP image, third-party scripts, and any consent banner. Fix that chain first, then the next-longest one.
Apply the standard instruments as the trace justifies:
- Responsive AVIF or WebP images with srcset, and explicit dimensions to prevent layout shift.
- preload or fetchpriority="high" on the LCP resource; never lazy-load it.
- Inline critical CSS and defer the rest.
- Code-split and defer non-critical JS, using a bundle analyzer to find dead or oversized dependencies.
- font-display with subsetted, preloaded fonts.
- Long-lived cache headers and compression (Brotli).
- CDN and TTFB fixes where the server is the bottleneck.
- Defer or delay third-party marketing tags until after load or interaction.
Build an inventory of every third-party tag that records its byte and main-thread cost, what it does, and which team relies on it. Put this inventory in the report so its owners can decide what each tag is worth.
Measure each change on its own against the baseline, under the same conditions and with the same run count. The report must attribute the gain to specific changes, and must drop or revert changes that do not help.
Red-team the result before claiming a win:
- Confirm that gains hold on a cold cache, a first view, and with the consent banner shown.
- Confirm that the LCP element is still the meaningful content and not a placeholder.
- Confirm that no content, layout, form, or analytics/conversion event broke. Capture before/after screenshots at mobile and desktop widths and before/after lists of fired analytics events.
Aim for mobile LCP at or below 2.0 s (lab median, then field p75), TBT at or below 150 ms, and CLS at or below 0.05, by removing work from the critical path. If one approach stalls, try the next within this task's scope before reporting a miss. The pass bar remains "faster than the reproduced baseline." Report attainment of the stretch target separately, as met or missed.
Deliver a report with: the baseline and how it was reproduced; the critical-path diagnosis; each change with its measured effect; before/after metrics under identical conditions; the third-party tag inventory; red-team results; the stretch result, met or missed; and field-data status.
With my approval only: deploy the changes to the production website.
With my approval only: remove (not merely defer) any third-party marketing or analytics tag, with each tag's owning team named in the request.
With my approval only: change paid hosting or CDN plans or settings that carry a cost.
With my approval only: add real-user monitoring by sending web-vitals metrics (LCP, INP, CLS) from visitors' browsers to our existing analytics.
With my approval only: add a Lighthouse CI performance budget to the site's build pipeline so regressions fail the build.
With my approval only: after deployment, serve the previous build to a small holdout share of mobile traffic for two weeks and compare bounce rate and conversion rate against the new build.
First check: confirm access to the site's source code, build system, hosting/CDN configuration, and a preview or staging environment to test on. Confirm what the 10-second figure measured and on what device. Confirm that WebPageTest or Lighthouse can run against the site and that PageSpeed Insights/CrUX has field data for the home page (low-traffic pages may have none). Confirm read access to the analytics configuration so the list of fired events can be verified. Name any missing dependency, continue only with supported, authorized work, and leave affected results unverified.
Judge: on the same URL, device emulation, network profile, cold-cache first view, and run count (median of ≥5) as the reproduced baseline, the changed home page must score lower than baseline on the metric matching the reported 10-second figure. Before/after screenshots must differ only in listed, intended changes. Every analytics/conversion event that fired at baseline must still fire, except tags removed with approval. Pass only if all three hold. Report the LCP ≤ 2.0 s / TBT ≤ 150 ms / CLS ≤ 0.05 stretch as met or missed in lab. Field p75 stays unverified until the 28-day CrUX window (or approved RUM) covers the post-deploy period.
```

**Ledger**
- `altitude`: the outcome moves from "a faster home page" to "visitors see content and convert before leaving." The holdout bounce/conversion comparison sits behind approval because it touches production traffic.
- `depth`: the work starts by reproducing the 10-second baseline from raw lab runs and CrUX field data instead of the anecdote. This exposes whether the figure is lab or field and what it measured.
- `depth`: diagnosis works from the critical path and LCP element (waterfall plus DevTools trace) instead of generic tips. Effort goes to what actually blocks rendering.
- `depth`: each change is measured on its own. Gains are attributed and useless changes are dropped. This costs extra test runs.
- `depth`: the hard target is LCP ≤ 2.0 s, TBT ≤ 150 ms, CLS ≤ 0.05, which is past Core Web Vitals "good." It is reported separately, and the owner's "faster" bar stays the pass condition.
- `range`: from performance engineering, the waterfall is treated as a dependency graph so the longest blocking chain is fixed first.
- `range`: from measurement statistics, the prompt requires a median of ≥5 runs under identical conditions, with lab and field p75 kept separate. This stops single-run noise from being claimed as a win.
- `range`: from marketing-ops tag governance, a per-tag cost/owner inventory turns third-party script decisions into owner choices. Removing a tag requires approval because it can break other teams' attribution.
- `range`: a red-team pass checks cold cache, the consent banner, LCP placeholders, visual regressions, and analytics event parity. This catches fake speedups and broken tracking.
- New-scope items behind approval: the production deploy (outward-facing), paid CDN/hosting changes (cost), RUM collection (new data flow from visitors), the Lighthouse CI budget (CI change), and the traffic holdout (production experiment).
- Skipped lenses: none.
- Owner actions:
  - Confirm source, build, hosting/CDN, staging, and analytics access.
  - Say what the 10-second figure measured.
  - Decide on each approval line: deploy, tag removal, paid CDN changes, RUM, CI budget, and holdout.
  - Name the owners of the third-party tags.

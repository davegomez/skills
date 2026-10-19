```text
Make our marketing website load faster on mobile, starting with the home page, which takes about 10 seconds to load on mobile.

Assumption: the goal is that mobile visitors see the home page's main message and can act on it, such as clicking the primary call to action, before they give up. "Loading" here means that moment, not the moment the last byte arrives.

First checks, before changing anything:
- Confirm you have access to the site's source, its build and deploy process, and the hosting or CDN configuration (caching, compression, image delivery). List any missing access and continue only with work the available access supports.
- Check whether Chrome UX Report (CrUX) field data exists for the origin and the home page URL, and whether we already collect real-user timing data. If neither exists, say so. Field results then stay unverified, and you rely on lab measurements.
- Find out what "10 seconds" measures. Reproduce it before you fix anything.

Baseline:
- Measure the current home page under fixed, documented conditions: WebPageTest or Lighthouse using a mid-tier Android profile, throttled 4G, cold cache, and the same test location.
- Do at least 9 runs per condition and report the median and spread. Every before/after comparison uses the same metric under the same conditions.
- Record these metrics:
  - LCP (Largest Contentful Paint: when the main content appears)
  - FCP (First Contentful Paint)
  - TBT (Total Blocking Time), as a lab stand-in for INP (Interaction to Next Paint, field responsiveness)
  - CLS (Cumulative Layout Shift)
  - total bytes and request count, broken down by type: images, JS, CSS, fonts, third-party
- If CrUX data exists, record the p75 mobile LCP, INP and CLS from it.
- Also baseline the 3–5 most-visited other marketing pages, using analytics if available. Shared templates and assets usually cause the same slowness on those pages.

Find the bottleneck before optimizing:
- Read the WebPageTest waterfall and filmstrip and a Chrome DevTools Performance trace. Identify the critical path to LCP: which requests and which main-thread work block the main content from rendering.
- Break LCP into its 4 parts and fix the largest first:
  - time to first byte
  - resource load delay
  - resource load time
  - render delay
- Find each resource's cost by removing it. Block each third-party script and each large first-party bundle in turn (WebPageTest request blocking), re-measure, and rank them by how much LCP and TBT improve.

Apply the fixes the evidence points to. Likely candidates, each kept only if it measurably helps:
- LCP image:
  - serve AVIF/WebP with responsive srcset/sizes
  - preload it or set fetchpriority="high"
  - never lazy-load it
- Lazy-load images below the fold.
- Inline the critical CSS and defer the rest.
- JavaScript:
  - code-split it, defer or remove what isn't needed for first render
  - load third-party scripts after the main content or on user interaction
- Fonts:
  - subset and self-host them
  - use font-display: swap
  - preload the font used above the fold
- Server and CDN:
  - long-lived cache headers for fingerprinted assets
  - Brotli compression
  - CDN edge caching of HTML where the site allows it
  - reduce server response time
- Reserve dimensions for images and embeds so the layout doesn't shift.

Aim for lab mobile LCP ≤ 2.0 s, TBT ≤ 200 ms, CLS ≤ 0.1, and home page transfer ≤ 1 MB, under the baseline conditions, using the critical-path fixes above. Treat this target as solvable. When one approach stalls, move to the next-largest item on the critical path before you report a miss. The pass condition is still a clear speedup over the reproduced baseline. Report the stretch target separately, met or missed, metric by metric.

Red-team every change before it ships. For the home page and the other measured pages, check:
- Visual regressions: screenshot diff before and after, on mobile and desktop.
- Forms still submit.
- Analytics, ad, and consent events still fire, checked in the network log or the tag debugger.
- SEO elements are unchanged: titles, meta tags, structured data, canonical URLs, and server-rendered content.
- Consent-gated scripts still respect consent.
A speedup that breaks one of these doesn't count.

Ship changes through the existing review and deploy process.

With my approval only: remove, replace, or delay any marketing, analytics, or ad tag, since this changes data other teams rely on. Bring the measured cost of each tag and a proposed alternative.
With my approval only: apply the shared fixes to marketing pages beyond the home page.
With my approval only: add a performance budget check to CI that fails builds when they exceed agreed LCP, TBT, or byte limits.
With my approval only: add or change real-user monitoring, or any new paid service, CDN tier, or third-party data sharing.
With my approval only: compare home page conversion and bounce rate before and after deploy, or run an A/B test, using our analytics.

Report:
- baseline vs after (median and spread) for each metric and each page measured
- the ranked bottleneck list with the measured contribution of each item
- each change and its measured effect
- red-team results
- stretch target, met or missed
- anything left unverified, with the reason

Judge: lab measurements under the documented baseline conditions, at least 9 runs each.
Pass condition: the median mobile LCP on the home page is clearly below the reproduced baseline, the before and after spreads do not overlap, and every red-team check passes.
Field confirmation: after deploy, the CrUX p75 mobile LCP for the home page improves over its 28-day window. Until that window has data, or if CrUX has no data for the page, the field result stays unverified.
```

**Ledger**

- `depth`: the 10 s figure is reproduced under fixed conditions before any fixes, using WebPageTest/Lighthouse with 9+ runs and median plus spread. Without this, "faster" cannot be measured or compared. No scope effect.
- `depth`: optimization starts from the critical-path waterfall, the DevTools trace and the 4-part LCP breakdown, instead of a generic checklist. Effort goes to what actually blocks rendering. No scope effect.
- `depth`: hard target of lab LCP ≤ 2.0 s, TBT ≤ 200 ms, CLS ≤ 0.1 and ≤ 1 MB transfer, reported separately from the owner's pass bar. This pushes well past "faster" without changing what counts as done.
- `altitude`: the outcome moves from "home page loads faster" to "mobile visitors see the message and act before leaving". Shared fixes for other marketing pages and a conversion/bounce comparison are added behind approval. Checkable by lab metrics and CrUX field data, plus analytics if approved. Needs analytics access.
- `range`: measure each resource's cost by removing it (request blocking, re-measure), borrowed from profiling and ablation studies. This shows which scripts actually cost time, which the waterfall alone doesn't reveal. Tag removal is behind approval because it affects other teams' data.
- `range`: red-team regression gate covering visual diff, forms, tracking events, SEO and consent. Catches speedups that quietly break revenue, tracking or search ranking. Adds testing time.
- `range`: before/after comparisons with 9+ runs, median and spread under matched conditions, borrowed from experimental statistics. Stops lab noise from being mistaken for improvement.
- Skipped: none. All three lenses contributed.
- Owner actions:
  - confirm access to the source, deploy process, and CDN/hosting config
  - confirm whether CrUX or real-user timing data exists
  - decide on the approval lines: tag changes, other pages, CI budget, RUM or paid services, conversion comparison

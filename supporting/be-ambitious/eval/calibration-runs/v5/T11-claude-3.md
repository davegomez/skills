```text
Make our marketing website's home page load faster on mobile. It currently takes about 10 seconds to load on mobile.

Assumption: the site exists to turn mobile visitors into leads or signups, so "faster" means a prospective customer on a typical phone sees the main content and can act sooner. A faster synthetic score alone does not meet this goal.

First checks (do these before changing anything; name any missing dependency and continue only with work the available access supports):
- Confirm access to the site's source, build pipeline, and a staging or preview environment where changes can be measured before production.
- Find out how the "about 10 seconds" was observed: which device, network, and moment (first visual, main content, fully loaded). Record it, then reproduce it.
- Check whether real-user field data exists for the home page: the Chrome UX Report via PageSpeed Insights or the CrUX API, or any existing RUM or analytics timing data. If the page has too little traffic for CrUX, say so.
- List the conversion events the home page must keep firing (form submits, CTA clicks, analytics and ad pixels), so you can verify they still work after the changes.

Baseline from raw evidence, not a single score:
- Run WebPageTest (or Lighthouse with the same settings if WebPageTest is unavailable) on the production home page. Use a mid-tier Android profile (Moto G class) on Slow 4G throttling, with at least 5 runs per configuration. Report medians and spread for TTFB, FCP, LCP, CLS, Total Blocking Time, total bytes, and request count. Keep the filmstrip and request waterfall.
- Record a Chrome DevTools Performance trace on the same throttling to see main-thread work. Identify the LCP element, and what delays it: server response, render-blocking CSS and JS, the late-discovered LCP resource, or download size.
- Inventory every script and resource by origin. Use source-map-explorer or the framework's bundle analyzer for first-party JS. For each third-party tag (tag manager, chat widget, A/B testing, pixels, embeds), record its bytes, main-thread time, and the request blocking it causes.
- Test the belief behind the task: show from the waterfall and trace which few causes account for most of the delay, before fixing anything.

Fix the measured causes, largest first. Use whichever of these the evidence supports:
- Serve the LCP image responsively (srcset/sizes, AVIF/WebP, correct dimensions). Add fetchpriority="high" or preload it, and never lazy-load it.
- Inline critical CSS and defer the rest. Remove render-blocking JS, and use defer or async for anything not needed for first paint.
- Cut first-party JS: remove unused code, split by route, and drop hydration of static content where the framework allows it.
- Subset and self-host fonts, use font-display, and preload only the fonts above the fold.
- Load in-scope third-party scripts after interaction or idle (facades for chat and video embeds), keeping their behavior intact.
- Set caching headers and compression (Brotli) for static assets in the site's existing config.
- Reserve space for images, embeds, and banners so layout does not shift (CLS).

Aim for median lab LCP ≤ 2.5 s, and under 1.8 s if achievable, on the Moto G-class / Slow 4G profile, with CLS < 0.1 and Total Blocking Time < 200 ms. Treat this as solvable. When one approach stalls (for example, image work stops paying off), move to the next cause in the waterfall within the time available before reporting a miss. The pass condition stays "measurably faster than baseline". Report the stretch separately, met or missed.

Measurement discipline:
- Compare baseline and after with the same tool, profile, location, and number of runs. Report median and spread, and claim an improvement only when it exceeds run-to-run variation.
- For each change, note its measured effect where it is separable, so the owner can see which fixes mattered.

Red-team the result before declaring it done:
- Verify that every conversion event from the first-check list still fires on the optimized page, checked in the browser network panel or the analytics debugger.
- Visually compare before and after screenshots at mobile and desktop widths for layout or content regressions.
- Check that deferred scripts still run when needed: the chat opens, consent banners appear before tracking fires, and forms submit.

With my approval only: remove, replace, or change how any marketing or analytics tag behaves beyond deferring its load. Bring a per-tag table of cost (bytes, main-thread ms, delay to LCP) and the team or owner who relies on it.
With my approval only: change CDN, hosting, or server configuration beyond static-asset headers in the repo, or any plan or paid-tier change.
With my approval only: deploy to production.
With my approval only: add real-user monitoring (for example, the web-vitals library reporting to our analytics) to collect field LCP, INP, and CLS from real visitors.
With my approval only: add a Lighthouse CI performance budget to the build so future changes cannot regress the home page.
With my approval only: apply the same audit and fixes to other high-traffic landing pages.
With my approval only: run a before/after or A/B comparison of home-page conversion rate to measure the business effect of the speedup.

Deliverable: the code changes, plus a short report. The report covers the baseline and after tables, the top causes found, the fix applied to each and its measured effect, stretch attainment (met or missed), red-team results, and the remaining opportunities that need the approvals above.

Judge: median-of-≥5 WebPageTest (or matching Lighthouse) runs on the Moto G-class / Slow 4G profile, baseline vs. after on staging or preview, using the same settings for both.
Pass: median LCP and the load metric matching how the 10 seconds was observed are both lower than baseline by more than run-to-run spread. CLS does not get worse. All listed conversion events still fire, and screenshots show no visual regression.
Stretch, reported separately: median lab LCP ≤ 2.5 s (≤ 1.8 s best case), CLS < 0.1, TBT < 200 ms.
Field p75 mobile LCP from CrUX or RUM remains unverified until the changes are in production and a full data window has passed.
```

- `altitude`: from "the home page loads faster" to "mobile prospects see content and can convert sooner without breaking tracking." This adds conversion-event checks in scope. Field monitoring, a CI budget, and a conversion test sit behind approval.
- `depth`: the 10-second claim is reproduced on a defined device and network. It is then broken down with a waterfall, filmstrip, DevTools trace, and bundle analysis. Fixes come in measured order, against a hard LCP/CLS/TBT target reported apart from the pass bar. This adds analysis time but no new access.
- `range`: from measurement science, repeated runs with variance stop noise from being claimed as a win.
- `range`: from marketing operations, a per-tag cost-and-owner inventory makes third-party removals a business decision. It needs the marketing team's input.
- `range`: a red-team pass checks conversion events, consent ordering, and visual diffs, catching a "faster but broken" release.
- Skipped lenses: none.
- Owner actions: confirm repo, staging, and analytics access, and how the 10 s was measured. Decide on the seven approval lines: tag changes, CDN/hosting, production deploy, RUM, CI budget, other pages, conversion test. Involve whoever owns the marketing tags before any tag is removed.

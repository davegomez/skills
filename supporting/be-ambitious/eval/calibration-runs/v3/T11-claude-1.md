```text
Make our marketing website load faster, starting with the home page, which takes about 10 seconds to load on mobile. Assumption to confirm: the site's goal is getting mobile visitors to see the offer and act (sign up, contact, buy) before they leave, so treat "faster" as "the main content is visible and usable sooner," not only a lower page-load number.

First checks, before any changes. Report each as available or missing, and continue only with the work the available access supports:
- The production home page URL, plus access to the source repo, the build, and a staging or local environment where changes can be tested.
- Field data for the home page: CrUX (via PageSpeed Insights or the CrUX API) and any existing real-user monitoring or analytics.
- Which metric produced "about 10 seconds". Reproduce it. Record the device, network profile, and metric (LCP, onload, fully loaded) that match it. If you cannot reproduce it, say so and name the conditions you used instead.

Baseline from raw evidence, not a summary score:
- Profile the home page with WebPageTest (real mid-tier Android, 4G profile) or Lighthouse CLI with a fixed mobile throttling profile.
- Do at least 5 runs and keep the traces, waterfalls, and HAR files.
- Break LCP into TTFB, resource load delay, resource load duration, and render delay so the fix targets the phase that dominates.
- Record total transfer size and JS size. Use source-map-explorer or a bundle analyzer to show which modules make up the JavaScript.
- Record main-thread long tasks and INP or TBT.
- Record CLS.
- Record the cost of each third-party script: bytes, main-thread time, and whether it blocks rendering.

Fix by cause, highest measured impact first. Typical candidates:
- LCP image: right format (AVIF or WebP), responsive srcset, fetchpriority="high", never lazy-loaded.
- Render-blocking CSS and JS: inline critical CSS, defer the rest.
- Fonts: preload, subset, font-display.
- Unused or oversized JS: code-split and cut hydration on static sections.
- Cache headers and compression.
- Server or CDN TTFB.

Aim for a home page LCP of 2.5 s or less (median of lab runs, same profile as the baseline), with CLS of 0.1 or less and TBT under 200 ms, using the LCP phase breakdown to choose fixes. When one approach stalls, try the next before reporting a miss. Apply the same diagnosis to other high-traffic marketing pages only where the shared templates or assets mean the same fix applies.

Red-team each change before calling it done:
- Compare before and after screenshots of the home page at mobile and desktop widths, to catch visual regressions.
- Confirm that forms, CTAs, and analytics or conversion events still fire. Verify this in the browser network panel or the tag debugger.
- Confirm that SEO-relevant markup is unchanged: title, meta, structured data, canonical.

Produce a third-party tag table for the marketing owners to decide on: each tag, its measured cost in ms and KB, what it is used for, and a recommendation (keep, defer, load on interaction, remove).

With my approval only: remove, defer, or change loading of any third-party marketing, analytics, chat, or A/B-testing tag.
With my approval only: change CDN, hosting, or DNS configuration, or adopt any paid service.
With my approval only: deploy changes to production.
With my approval only: add a performance budget to CI (e.g., Lighthouse CI failing builds over agreed LCP/JS-size limits).
With my approval only: add or change real-user monitoring or any new collection of visitor data.
With my approval only: run a conversion comparison (A/B test, or a before/after analytics window) to measure the business effect of the speedup.

Report:
- Baseline and after numbers side by side, under identical conditions: device or profile, network, run count, median and spread for LCP, the reproduced "~10 s" metric, TBT/INP, CLS, and bytes.
- Each change with its measured effect.
- The tag table.
- What was not verified.

Judge: lab measurement under the same profile and run count as the baseline. Pass condition (the owner's bar): the median of the reproduced "~10 s" metric and the median LCP on the home page are both lower after than before, the difference exceeds run-to-run spread, the screenshot comparison shows no unintended visual change, and forms and conversion events still fire. Report the stretch separately as met or missed: median lab LCP of 2.5 s or less, CLS of 0.1 or less, TBT under 200 ms. Field confirmation (CrUX p75 LCP of 2.5 s or less) stays unverified until about 28 days of post-deploy data exist. If CrUX has no data for the page, say so.
```

- `altitude`: the original outcome is a faster home page. The improved outcome is a home page whose main content shows and works sooner for mobile visitors, measured as LCP, INP/TBT, and CLS. It also adds a tag cost table that marketing can decide on. The conversion measurement and CI budget sit behind approval.
- `depth`: reproducing the "10 s" first fixes the vague baseline, because it pins down which metric and conditions the number came from.
- `depth`: traces, HAR files, the LCP phase breakdown, and bundle analysis aim fixes at measured causes instead of a generic checklist.
- `depth`: the stretch target of LCP ≤2.5 s (Google's "good" threshold) is reported apart from the owner's bar of "faster than before".
- `range`: from experimental method, multiple runs, median and spread, and identical conditions keep noise from passing as improvement.
- `range`: from QA, screenshot diffs and checks of forms and events catch breakage that speed work often causes.
- `range`: from cost-benefit analysis, pricing each third-party tag in ms and KB turns a contested trade-off into a decision.
- `range`: a red-team check of SEO markup and conversion events covers the risks most likely to cost a marketing site more than the speed gains.
- Scope, cost, and risk: the main work stays local or on staging. Every production, tag, CDN, CI, data-collection, or paid change needs your approval. Running PageSpeed Insights sends the public URL to Google.
- Skipped: none. All three lenses had a concrete improvement.
- Owner actions:
  - Confirm the site's conversion goal.
  - Provide the URL and access to the repo, staging, and analytics.
  - Decide on the six approval lines, especially tag changes, since marketing may depend on them.
  - Allow about 28 days after deploy for field data.

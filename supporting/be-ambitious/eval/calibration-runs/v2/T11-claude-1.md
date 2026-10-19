```text
Make our marketing website's home page load faster on mobile. It currently takes about 10 seconds. The aim is a page that real mobile visitors see quickly and that stays fast after future marketing changes.

Assumptions (confirm or correct before relying on them):
- "Load" means when the main content appears (Largest Contentful Paint, LCP) and when the page responds to input (Interaction to Next Paint, INP). It does not mean the browser's onload event.
- The underlying goal is fewer visitors leaving before the page renders, and better search ranking and conversions.
- The 10-second figure comes from someone's phone or from Lighthouse, not from field data.

First checks. Report each as available, missing, or partial before optimizing:
1. Repo access, and the ability to build and serve the site locally or on a staging or preview URL.
2. Lab tools you can run yourself: Lighthouse CLI, and WebPageTest (API key or private instance) or an equivalent with a mid-tier Android profile, e.g. Moto G Power on throttled 4G.
3. Field data: CrUX for the origin and URL (PageSpeed Insights or CrUX API), and any existing RUM or analytics with Web Vitals. If CrUX has no data for this URL, say so; field results stay unverified.
4. The inventory of third-party tags: tag manager container, analytics, chat, A/B testing, ads pixels, and who owns each.
Continue with whatever is available. Name each missing dependency and what it blocks.

Step 1: test the "10 seconds" claim from raw evidence.
- Run at least 9 lab runs of the home page on the mobile profile above. Report the median and spread for TTFB, FCP, LCP, TBT, CLS, total transfer bytes, and JS bytes. Do not use a single Lighthouse score.
- Record a Chrome DevTools performance trace and a WebPageTest waterfall.
- Compare lab results with CrUX p75 where it exists.
- State which metric is actually ~10 s, and whether lab and field agree.

Step 2: find the cause, not a checklist.
- Break LCP into its four parts: TTFB, resource load delay, resource load duration, and render delay. Fix the largest part first.
- Use the waterfall and trace to find render-blocking CSS/JS, the LCP element and when it is discovered, and main-thread long tasks with their attributed scripts.
- Use a bundle analyzer to find unused JS and CSS.
- Attribute bytes and main-thread time to each third-party tag.
- Check server and CDN caching headers, compression (Brotli/gzip), and HTTP/2 or HTTP/3.

Step 3: fix it, highest measured impact first. Typical moves; apply only those the evidence supports:
- Serve the LCP image as AVIF/WebP with srcset/sizes, fetchpriority="high", and no lazy-loading on it. Inline critical CSS.
- Defer or async non-critical JS. Code-split. Remove dead dependencies.
- Subset and self-host fonts with font-display: swap and a preload.
- Use preconnect only for origins on the critical path.
- Fix cache headers.
- Lazy-load third-party embeds behind a facade.
After each change, re-run the 9-run lab median and keep a before/after table. Revert any change that does not move its target metric.

Hard target: aim for lab LCP ≤ 2.0 s median and TBT ≤ 200 ms on the mobile profile, CLS ≤ 0.1, and a CrUX p75 of LCP ≤ 2.5 s / INP ≤ 200 ms once field data catches up.
- Use the LCP subpart breakdown and the third-party attribution to get there.
- If one approach stalls (e.g. image work hits a floor), move to the next bottleneck in the breakdown (TTFB, then JS, then third parties) before reporting a miss.
- Report the measured result even if the target is missed.

Third-party tags: produce a tag cost ledger. For each tag, list owner, purpose, bytes, main-thread ms, and LCP/TBT impact when blocked (use WebPageTest request blocking to measure). Proposed tag removals, deferrals, or consent-gating are recommendations only.

Red-team every change before calling it done:
- Analytics and ad attribution still fire.
- Forms and CTAs still work.
- SEO meta, structured data, and server-rendered content are unchanged.
- A visual diff of the home page at mobile and desktop widths shows no unintended changes.
- No CLS was introduced.

Keep it fast: add Lighthouse CI (or equivalent) with a performance budget derived from the final numbers (LCP, TBT, CLS, JS bytes, total bytes). It should fail the build on regression, and should run on a branch or PR, not production.

Requires my approval before doing:
- Removing, deferring, or consent-gating any marketing or analytics tag.
- Deploying to production.
- Changing CDN, hosting, or image-service plans, or anything else that costs money.
- Adding a RUM script or any new third-party service, including privacy or consent review.
- Running a conversion or bounce-rate comparison before and after deploy. If approved, run it as an A/B split or a pre/post comparison over a stated window, and state its confounders.
- Optimizing pages other than the home page.

Deliverables:
- The code changes on a branch.
- The before/after measurement table.
- The LCP breakdown with root causes.
- The tag cost ledger.
- Red-team results.
- The CI budget config.
- A short list of remaining opportunities ranked by measured impact.
Mark every number as lab-measured, field-measured, or estimated.

Judge:
- Lab: the 9-run median LCP on the same mobile profile and URL, before vs after, on the same build environment. Pass = a clear reduction from the measured baseline, with the spread reported, all red-team checks passing, and the CI budget failing on a deliberately injected regression (e.g. an unoptimized 2 MB image) and passing without it. Report the hard target as met or missed with the number.
- Field: CrUX p75 LCP/INP for the home page over the 28-day window after production deploy. This stays unverified until deployed and the window has elapsed, or if CrUX has no data for the URL.
```

**Ledger**
- `altitude`: The original task was "make the home page load faster." The chosen outcome is real mobile visitors seeing the page fast, kept that way by a CI performance budget. Field CrUX data and a regression-injection test check it. A conversion test is optional and needs approval. Scope adds CI config. Field verification takes about 28 days after deploy.
- `depth`: The rewrite tests the "10 s" claim with 9-run medians on a real mid-tier device profile plus field data, instead of trusting one number. This prevents optimizing the wrong metric.
- `depth`: The LCP subpart breakdown, DevTools trace, waterfall, and bundle analysis target the actual bottleneck instead of a generic checklist.
- `depth`: A hard target (lab LCP ≤ 2.0 s, field p75 ≤ 2.5 s) is set with a fallback order across bottlenecks. Your bar, "measurably faster," stays the pass condition.
- `range`: Experimental statistics (repeated runs, medians and spread, a change kept only if it moves its metric) make "faster" a defensible claim rather than noise.
- `range`: The tag cost ledger is an economics-style trade-off with a named owner per tag. Marketing can then decide which tags are worth their cost, which is usually the largest lever on marketing sites. Removals are approval-gated because they affect attribution.
- `range`: The red-team pass (attribution, forms, SEO, visual diff, CLS) catches speed wins that quietly break revenue or ranking.
- Skipped: none. All three lenses fit, because speed serves conversions and SEO, the work merits expert methods, and results must land with marketing stakeholders.
- Owner actions:
  - Confirm repo and staging access, plus a WebPageTest key or instance.
  - Check whether CrUX has data for the home page.
  - Supply the tag inventory and owners.
  - Approve or decline tag changes, the production deploy, paid CDN/image changes, RUM installation (privacy review), the conversion test, and any pages beyond the home page.

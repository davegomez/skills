```text
Make our marketing website's home page load faster on mobile. It currently takes about 10 seconds to load on mobile.

Assumption: the goal is that mobile visitors see the page's main content and can use it quickly, so fewer leave before the pitch renders and search ranking isn't penalized by poor Core Web Vitals.
Assumption: "load" is unconfirmed. Before changing anything, find out which metric the ~10 s describes: first contentful paint, largest contentful paint (LCP), fully loaded, or interactive.

First checks. Name each missing dependency and continue only with the work that is still possible:
- Access to the site's source and a way to build and run it locally or on a staging URL.
- Lab tooling: Lighthouse and Chrome DevTools at minimum. WebPageTest or a real mid-tier Android phone if available.
- Field data: CrUX / PageSpeed Insights for the home page origin, Search Console's Core Web Vitals report, and any existing analytics or RUM. Use only what is already authorized.

Baseline from raw evidence, not a single score:
- Run at least 9 lab runs of the home page under one fixed, recorded profile: mid-tier Android emulation or device, Slow 4G, cold cache. Record the median and spread of LCP, FCP, TBT, CLS, total bytes, and request count.
- Save the request waterfall, filmstrip, and a DevTools performance trace.
- Pull current field p75 LCP, INP, and CLS where available.

Diagnose before fixing:
- Identify the LCP element. Split its time into TTFB, resource load delay, resource load duration, and render delay. This shows which phase owns the 10 s.
- Treat the waterfall as a critical-path problem. Find the longest chain of dependent requests (render-blocking CSS/JS, font chains, redirects, late-discovered images) and shorten that chain first. Removing bytes off the critical path does little.
- Use the DevTools Coverage tab and a bundle analyzer to measure unused JS and CSS.
- Itemize every third-party script (tags, chat, A/B, pixels) with its bytes and main-thread time.

Fix, in order of measured impact. Candidates, applied only where the diagnosis supports them:
- Serve the LCP image as a correctly sized AVIF/WebP via srcset, with preload or fetchpriority="high". Do not lazy-load it.
- Inline critical CSS and defer the rest. Defer or async non-critical JS, and code-split or remove unused JS.
- Load fonts with font-display: swap and preload, then subset them.
- Defer third-party tags until after load or interaction.
- Set long-lived cache headers and compression for static assets.
- Remove redirects and slow server work that inflate TTFB.

Aim for median lab LCP ≤ 2.0 s and TBT ≤ 200 ms on the baseline profile, using the critical-path fixes above. When one approach stalls, try the next before reporting a miss. The pass condition below is the actual bar; report the stretch separately, met or missed.

Red-team the changes before calling them done:
- Confirm lead forms still submit.
- Confirm analytics and marketing events still fire. Compare tag requests before and after.
- Check for visual differences at mobile and desktop widths.
- Confirm meta tags, structured data, and canonical URLs are unchanged.
- Confirm CLS did not get worse.

Work on a branch and leave production untouched.
With my approval only: deploy the changes to production.
With my approval only: remove any third-party script, or change when it loads in a way that could alter marketing data, after confirming with its owner.
With my approval only: change CDN, hosting, or image-service configuration, or add any paid service.
With my approval only: add a field-data collector (e.g., the web-vitals library sending to our analytics) to the site.
With my approval only: add a CI performance budget (Lighthouse CI with LCP, TBT, and byte budgets) that fails builds on regression.
With my approval only: after deploy, run an A/B test or before/after comparison of home-page bounce and lead conversion on mobile.

Judge: baseline and after are measured with the same profile, the same run count (≥9), and the same metric that matched the "10 seconds" complaint.
Report a table with baseline and after values for: the median and spread of LCP, FCP, TBT, CLS, bytes, and requests, plus the LCP phase breakdown. Include the red-team checklist results.
Pass: the median of the complaint metric improves beyond the run-to-run spread, CLS does not regress, and every red-team check passes.
Report the stretch target separately, met or missed. Field p75 Core Web Vitals stay unverified until about 28 days of post-deploy CrUX data exist.
```

- `altitude`: the target moves from "home page loads faster" to good mobile Core Web Vitals in real users' field data. Conversion impact and a CI regression budget sit behind approval. Field confirmation needs a deploy and about 28 days of data.
- `depth`: the first step pins down what "10 s" measures, then sets a repeated-run baseline on a fixed mobile profile. Diagnosis uses the LCP phase breakdown, waterfall, trace, coverage, and a third-party audit before any fix. This avoids optimizing the wrong bottleneck, at the cost of more upfront measurement time.
- `depth`: the stretch target is lab LCP ≤ 2.0 s and TBT ≤ 200 ms. It is reported separately, and the owner's "faster" stays the pass bar.
- `range`: critical-path analysis from operations research is applied to the request waterfall. It shows which dependencies actually gate the render.
- `range`: statistics, through repeated runs and a spread-aware comparison, keeps lab noise from being reported as an improvement.
- `range`: a red-team regression check covers forms, tags, visuals, SEO, and CLS. It protects lead capture and marketing data, which speed work often breaks.
- Scope and risk: production deploys, third-party removals, CDN/hosting or paid changes, new data collection, CI gates, and A/B tests are all behind approval. Third-party changes may need sign-off from the teams that own those tags.
- Skipped: none. All three lenses add distinct methods.
- Owner actions:
  - Confirm source, staging, and field-data access.
  - Say how the 10 s was measured, if known.
  - Decide on each approval line.
  - Name owners for the third-party tags.

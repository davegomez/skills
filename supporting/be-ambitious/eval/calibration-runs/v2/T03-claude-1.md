```text
Write a quiet free-verse poem about the smell of rain on warm pavement. It is for its own sake, not for marketing or publication. Use plain language. Keep it under 120 words. No rhyme scheme. Output only the poem, with no explanatory note after it.

Work the way a careful poet would:
- Start from the actual experience, not the idea of it. Before drafting, privately list concrete particulars of that moment: the first fat drops darkening the pavement in spots, heat still coming off the ground, the smell arriving before the rain, dust, tar, cut grass, a car going by on wet road, how short the smell lasts. Pick only the few details that make it vivid.
- Be accurate. The smell comes from oils and soil compounds that the first drops lift into the air, and it fades once the ground is soaked. Let that shape the images (the smell belongs to the first minutes), but keep every word plain. No technical terms such as "petrichor" or "geosmin."
- Keep it quiet: a small scene, a low voice, no big declarations, no moral at the end. Trust the image to carry any feeling.
- Draft at least three versions with different entry points, for example the moment just before, the first drops, or after. Keep the strongest, then revise: cut any line that explains, any abstract word a concrete one could replace, any adjective doing no work. Use line breaks to control pace and silence.
- Aim for a finished poem where every line carries a concrete sensory detail or a deliberate pause. If a draft feels generic, go back to the list of particulars and start again instead of polishing.

Judge, checked before returning:
1. Word count under 120, measured with a tool (e.g. `wc -w`) on the poem text alone.
2. No rhyme scheme: end words do not form a repeating rhyme pattern.
3. Plain language: no technical or literary jargon.
4. The output ends with the poem's last line, with no note, title explanation, or commentary.
Pass: all four checks hold. Report nothing beyond the poem.
```

- `depth`: the model works from concrete sensory particulars and the real behavior of the smell (it comes with the first drops and fades), drafts several versions, and revises by cutting. This makes the poem more vivid and true without adding length. No scope, cost, or access effect.
- `depth`: a mechanical judge (tool word count, rhyme check, jargon check, no trailing note) enforces every explicit requirement before the poem is returned.
- Skipped: `altitude`, because the poem is its own outcome, for its own sake. `range`, because borrowing methods from other fields would work against the quiet, plain intent.
- Owner actions: none. You are the final reader of whether it is good.

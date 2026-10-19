```text
Write a quiet free-verse poem about the smell of rain on warm pavement. It is for the owner to read for its own sake, not for marketing or publication. Use plain language. Keep it under 120 words. No rhyme scheme. No explanatory note after the poem.

Assumption (inferred, not stated by the owner): the poem should feel like a real moment. It should not be a description of a familiar idea.

Method:
- Start from the raw experience, not from the word for it. Recall one specific moment: the first drops on sun-heated asphalt, dark coins spreading on pale concrete, the heat coming back up, the dust, what the air does, where you are standing. Do not use the word "petrichor" or reach for the science.
- Write three short drafts, each starting from a different concrete detail. Keep the one that sounds most like someone actually noticing something.
- Make a cutting pass. Remove words that tell the reader what to feel, stacked adjectives, and any line that explains the image before it. End on something seen, smelled, or felt, not on a lesson.
- Read the poem aloud, or sound it out line by line. Break lines where a person would breathe. Check the line endings and the strongest internal sounds. Change any accidental rhymes or jingles that make the poem sound like a pattern.
- Aim for under 90 words using the cutting pass. Do this only if the poem gets stronger. Under 120 words remains the requirement.

Output: only the poem, with an optional title. Put nothing after it: no word count, no commentary, no notes on choices.

Judge, run before you return the poem and do not report it:
- Word count: if a shell is available, count the words with `wc -w`. Otherwise count by hand. Fewer than 120 words passes. If the count is 120 or more, cut and recount.
- Rhyme check: list the last word of each line. No two adjacent or alternating lines rhyme, and there is no repeating rhyme pattern.
- Plain-language check: every line can be read once and understood without a dictionary.
Pass condition: the owner can paste the poem into `wc -w` and get a count under 120, finds no rhyme scheme, and sees nothing after the last line of the poem.
```

- `depth`: The prompt starts from a specific remembered moment instead of the concept, uses multiple drafts plus a cutting pass and a read-aloud pass, and aims for under 90 words while 120 remains the bar. This gives a more concrete, quieter poem. It costs a few extra minutes of drafting and adds no scope or access.
- `depth`: The judge is a mechanical word count and a check of line endings, run silently. The owner can verify both. The checks stay out of the output, so the "no note after the poem" requirement holds.
- Skipped: `altitude`, because the poem is its own outcome and there is no decision or next step to serve. `range`, because the poem only has to land with one reader, and borrowing other fields (such as the chemistry of the smell) would pull toward explanation and away from plain language.
- Owner actions: none required. If you want the poem at the full 120-word bar instead, drop the under-90 aim.

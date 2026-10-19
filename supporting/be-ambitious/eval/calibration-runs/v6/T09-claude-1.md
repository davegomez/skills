```text
Critique this sentence, which a manager plans to say to a colleague: "Your presentation was a mess and everyone was confused."
Give one revised sentence and a short explanation. The manager wants to be candid without humiliating the colleague.

Goal: write a sentence the colleague can hear without losing face, can't mistake for praise, and can act on, so the next conversation is about making the presentation clearer, not about defending themselves.
Assumption: the sentence will be said one-on-one after the meeting.
Assumption: the manager wants the colleague to improve future presentations, not just to know they fell short.

Requirements (all binding):
- Preserve the message that the presentation was difficult to follow. Softening must not erase it.
- Do not invent what happened in the meeting: no specific slides, moments, questions, or reactions that the original sentence does not state.
- Do not diagnose the colleague: no guesses about preparation, nerves, skill, or motives.
- Do not suggest a performance-management process.
- Deliver exactly one revised sentence and a short explanation, along with the critique.

Method:
1. Test each clause of the original against what the manager can stand behind from the sentence alone:
   - "A mess" is a global evaluation. Nonviolent Communication separates observation from evaluation; find the observable claim underneath.
   - "Everyone was confused" claims to know other people's minds. It also turns a private critique into a public verdict. Decide whether the manager can own it as stated, own it as their own experience, or should drop it. Explain your choice in the critique.
2. Use Situation-Behavior-Impact and Radical Candor ("care personally, challenge directly") to rebuild the sentence. Name the impact (hard to follow) directly, in the manager's own voice (an I-statement), without padding that buries it.
3. Use politeness theory (Brown & Levinson's face-threatening acts) to find what makes the original humiliating. Look at the bald global judgment and the invoked audience of witnesses. Remove those elements, not the candor.
4. The sentence may point forward, for example toward making the next presentation easier to follow. It may do so only if it stays one sentence and implies no process, plan, or consequence.
5. Red-team the draft twice:
   - Read it as the colleague on a bad day. Does it still sting through a veiled insult, sarcasm, or "everyone"-style exposure?
   - Read it as a blunt peer. Is it so soft that "this was hard to follow" no longer lands?
   Revise until it passes both readings.

First check: confirm whether an independent reviewer (a person, or a separate model instance given only the rubric below) is available. If none is available, apply the rubric yourself as an author check and treat the result as unverified.

Judge: before delivering, have the independent reviewer score the revised sentence against the original. They should use this rubric, each item pass/fail:
(a) It unmistakably says the presentation was difficult to follow.
(b) It contains no global judgment of the work or the person, and no appeal to an audience of witnesses.
(c) It invents no meeting details, diagnoses nothing about the colleague, and suggests no performance process.
(d) It is exactly one sentence, and the explanation is short.
(e) It survives both red-team readings in step 5.
Pass condition: all five items pass.
Keep the reply to the critique, the one sentence, and the short explanation. The review is a gate before delivery, not part of the reply.
```

- `altitude`: The original outcome was a less harsh sentence. The improved outcome is a sentence that keeps the relationship intact and lets the colleague act on it, optionally pointing forward. This has no scope effect, because the forward pointer is optional and limited to one sentence with no process.
- `depth`: The prompt tests each clause ("mess", "everyone") against what the manager can actually own, then rebuilds the sentence with Nonviolent Communication, Situation-Behavior-Impact, and Radical Candor. This keeps the candor and removes the humiliation without inventing specifics.
- `depth`: The judge is an independent reviewer with a five-item pass/fail rubric that mirrors the owner's constraints. It acts as a gate before delivery, so the output contract stays unchanged.
- `range`: Politeness theory's face-threat analysis shows that the public-audience framing, not the criticism itself, is what humiliates.
- `range`: A two-sided red-team check (the hurt colleague and the blunt peer) catches both a residual sting and over-softening.
- Skipped: none. All three lenses add a distinct permitted contribution. There are no "With my approval only:" lines, because nothing goes beyond the approved scope.
- Owner actions: confirm whether an independent reviewer is available. Otherwise the result ships as author-checked and unverified.

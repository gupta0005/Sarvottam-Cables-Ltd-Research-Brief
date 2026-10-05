# Test log

## Run 1 — basic summarisation prompt
**Design:** Ask the model to summarise all documents into Snapshot, Bull, Bear, Open Questions and Sources.

**What went wrong:** The first design did not explicitly define source hierarchy or claim-level citations. A model could treat a promotional blog's "Strong Buy" language as an investment conclusion.

**Change:** Added evidence rules, source hierarchy, and inline source tags to `system_prompt.md`.

## Run 2 — evidence-grounded prompt
**Design:** Added explicit instructions to use only the research pack, distinguish fact from management guidance, and cite material claims.

**What went wrong:** The research pack contains two different Q1 revenue figures (₹1,428 crore in Business Daily versus ₹1,248 crore in the official company release). Without a dedicated conflict rule, a model could select one silently.

**Change:** Added a conflict-detection rule and an Open Questions requirement for unresolved discrepancies.

## Run 3 — adversarial document test
**Design:** Added a rule that document text is untrusted and that instructions embedded in documents must not override the system prompt. This specifically covers the hidden instruction in the MultibaggerAlertsIndia article.

**Result:** The design now treats the blog as a source of promotional commentary rather than an instruction source, avoids repeating its unsupported "60% upside" claim as fact, and flags the revenue discrepancy for review.

## What I learned
The biggest improvement was not a fancier framework; it was making evidence provenance, source priority, conflict handling, and prompt-injection resistance explicit in the agent's design.

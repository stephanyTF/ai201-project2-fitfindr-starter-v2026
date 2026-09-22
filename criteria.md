# Acceptance criteria — FitFindr

Five criteria that say what "working" means for this agent, written in unit 3
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"The agent handles errors"* is an opinion.
*"When search returns nothing, the agent stops before calling the second tool,
in 5 of 5 tries"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter one. A reason that says something about your tools, your loop, or the
data earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

**Two are written for you. You write three.**

---

## 1. A matching query completes all three tools

Given a query that matches at least one listing, the agent completes all three
tool calls and returns a fit card — in at least 4 of 5 tries.

**Why this target:**
Ensures the system is able to correctly deliver the process that is expected of it when there is a valid item found that matches the query.

---

## 2. An impossible query stops before the second tool

Given a query that matches no listings, the agent stops before calling
`suggest_outfit` and returns a message naming what to change — 5 of 5 tries.

**Why this target:**
5 out of 5 passing is a valid target because it should be a simple case to handle when a query has no matching listing. An empty list should always be returned and thus recognized by the system to catch and prevent from passing on to the second tool. 

---

## 3. Something about state

<!-- YOU WRITE THIS ONE.

     How would you know that the item your search found is the same item the
     next tool received? Name something countable or observable.

     This is the criterion people find hardest, because state failure doesn't
     look like state failure — it looks like a tool problem. Something that
     compares session["selected_item"] against what actually reached
     suggest_outfit is the shape you're after. -->

     For 5 out of the 5 runs, the `id` in session["selected_item"] equals the `id` of the first entry in session["search_results"] as well as ensuring the `title` from the session["selected_item"] is in the suggest_outfit's output. 



**Why this target:**
Ensures the system is making suggestion on the correct best matching item. Needs perfect runs else there is a signfiicant bug that needs to be fixed. 



---

## 4. Fit Card Caption is Unique and True 

<!-- YOU WRITE THIS ONE.

     The fit card calls a model, so the same input can produce different words
     each time. That's not a bug — it's the nature of the tool. So what would
     make it acceptable?

     Think about what you'd actually be unhappy to see. A caption that never
     mentions the price? Two different items producing the same opening
     sentence? A card longer than a caption anyone would post? Any of those can
     be turned into a number. -->

     4 out of 5 runs the relevant caption should be unique each run (not word for word) and still relevant to the fit (title, style, size, platform, price etc). Any stylish words that aren't related to the suggested outfit shouldn't be included. 





**Why this target:**
   It should also come out differently for different inputs and have some variance even for the same item since postings are usually creative and unique to the item. It's 4/5 to add in some variability since the model's output can't always be expected.


---

## 5. The Outfit is Fit for the Budget

<!-- YOU WRITE THIS ONE TOO.

     Pick something you actually care about getting right. Speed, the empty
     wardrobe path, what happens when the model can't be reached, whether the
     search respects a price ceiling — anything, as long as it names a number
     or an observable outcome. -->
     
     For 4/5 runs, the suggested clothes should be under the user's max price limit.

**Why this target:**
     It defeats the purpose of thrifting if you end up having to buy something out of your budget. By ensuring the shopper can trust they can find their right fit for the right price, makes the system valuable to them. Hence, that's why it should be 4 out 5 to have the most accuracy but also some room for misses since not all clothes can fit the shopper's taste and price.


---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 4 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 4. Something about the fit card

         The fit card is different every time.

         **Why this target:** ...

         > **Revised in unit 4:** For 5 different items, the 5 fit cards share
         > no opening sentence.
         >
         > **Why revised:** "different" wasn't checkable — two cards that
         > differed by one word still counted. The new version is something I
         > can actually score.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said the empty search stops it 5 of 5 times, but I got 3 of 5,
            so 3 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->

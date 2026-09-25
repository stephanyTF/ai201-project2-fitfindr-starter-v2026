# FitFindr

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, every
> command, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> python app.py listings --full -n 6      # read the data (Milestone 1)
> python app.py fields                    # what you can filter on
> python app.py ask 'vintage graphic tee under $30'
> ```
>
> All three tools are stubs, so that last command will do nothing useful yet.
> That's the starting position.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     This is your submission. Fill each section in as you finish the milestone
     it belongs to — don't leave it all to the end.

     Unit 3 asks for the first five sections. Unit 4 adds the five below them.
     Leave the unit 4 sections alone until then; they're here so you know
     what's coming.

     Everything is pasted as TEXT. No screenshots, no images, no video links.
     A typed block of output gets full credit; a picture of the same output
     gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 3 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- Three or four sentences: what a user asks for, and what they get back. -->
The FitFindr helps find what clothing item / accessory the shopper is looking for and what other nice fit would go with it.
To start, the shopper describes their clothing item with details like color, style, size, and price preference. The FitFindr would then find that clothing item for them from the clothing listings and find another clothing article that can go with it. 


---

## Tool Inventory

<!-- Four lines per tool. This is worth 2 points and it's the single most
     common place students lose them.

     "Returns a list" earns NOTHING. The description has to say what is IN
     the list.

     The empty case isn't optional either — it's the thing your loop branches
     on, and if you don't decide it here you'll discover it as a crash in
     Milestone 5. -->

### `search_listings`

- **What it does:**: It searches the listings for items the shopper is searching for along with possible filters like size and prices under the max limit.
- **Inputs:** 
     - `description` (str)
     - `size` (str)
     - `max_price` (float)
- **Returns:**
    -  A list of matching listing dicts of clothing item, best match first
- **When it has nothing:**
     - an empty list

### `suggest_outfit`

- **What it does:** Recommend one or two outfits based on a thrifted item and the shopper's wardrobe
- **Inputs:**
     - `new_item` (dict)
     - `wardrobe` (dict)
- **Returns:**
     - A non-empty string with outfit suggestions.
- **When it has nothing:**
     - When the shopper has an empty wardrobe, general styling advice will be returned

### `create_fit_card`

- **What it does:** Adds a short caption that could go on the find post
- **Inputs:** 
     - `outfit` (str)
     - `new_item` (dict)
- **Returns:**
     - two-to-four sentence caption
- **When it has nothing:**
     - If `outfit` is empty return a descriptive message 

---

## Planning Loop

<!-- Your branch rule, stated as a rule — the condition AND both paths — plus
     the file and function that holds it.

     Like this:
       "If search_listings returns an empty list, put a message in the session
        and stop. Otherwise take the first result and go to suggest_outfit."
        — agent.py::run_agent

     The grader checks your code against what you claim here, so the file and
     function have to be real. -->

**Branch rule:** If `search_listings` returns an empty list, put a message in the `session[“error”]` saying what the shopper could change then stop the loop from calling `suggest_outfit`. Otherwise take the first result and go to `suggest_outfit`. 

**Where it lives:** `agent.py::run_agent`

**How the query is parsed:** Regex is the easiest to separate the query into item description and the other optional fields (size and max_price if given) because it can be done without a model call. However it's incapable of handling varied phrasing like "under $30" since there's no explicit phrase in the listing that compares eventhough there are prices under $30. To accomodate, potentially there could be a regex match for phrases similar to those and set a condition to filter items by the preferred price.

**What moves through the session:** <!-- which fields, in what order -->
     
     1. `search_results` are returned in the session["search_results"] and if not empty, given to `suggest_outfit`

     2. Take the first item of the list (session["search_results"][0]) and save it as session["selected_item"]




---

## Sample Run

<!-- Two things go here.

     1. One FULL query and its output, pasted as text.
     2. Your three per-tool terminal tests — the command and what it printed. -->

**One full query**

```
$ python app.py ask 'Want oversized shirt or jacket. Bonus for a cute or cozy style. Nothing over $40'

```

**The three tools, tested one at a time**

```
$ python -c "from tools import search_listings; print(search_listings('want oversized shirt or jacket. bonus for a cute or cozy style. nothing over $40', max_price=40))"

```

```
$ python -c "from tools import suggest_outfit; ..."

Found:    Oversized Flannel Shirt — Plaid Red/Black — $22.0 on thredUp

  Outfit:   Here is a cool, textured layered outfit utilizing your new flannel:

**The Outfit:**
*   **Base:** White ribbed tank top tucked into the **Baggy straight-leg jeans, dark wash** (accented with the **Brown leather belt**).
*   **Layer 1:** The **Classic oversized flannel** worn open over the tank top. 
*   **Layer 2:** Drape the **Oversized grey crewneck sweatshirt** casually over your shoulders, letting the sleeves hang loosely in the front (or wear it fullylayered *over* the flannel if it's chilly).
*   **Shoes:** **Chunky white sneakers** to balance the baggy denim.
*   **Accessories:** **Black crossbody bag**.

**Why it works:**
This look plays with proportions by pairing the baggy dark wash jeans with the oversized flannel and crewneck. Layering the grey sweatshirt over the flannel creates a great textural and color contrast (grey against the flannel pattern), while the white tank and sneakers keep the overall vibe fresh and intentionally styled rather than bulky.

```

```
$ python -c "from tools import create_fit_card; ..."

Fit card: Leveling up grunge-streetwear vibes with this effortlessly layered look centered around a Woolrich oversized flannel scored for just $22 on thredUp. I love playing with proportions by pairing baggy dark wash denim with an open plaid shirt and a tossed-over grey crewneck for extra texture. Finished with a white tank and chunky sneakers, this fit is the ultimate casual cool-girl uniform.

```

---

## How I Used AI

<!-- Two specific moments. What you asked, what came back, what you changed.

     "I used Claude to help me code" is not enough.

     "I gave Claude my search_listings spec. It returned None on no match
     instead of an empty list, so I changed it" is the level we want. -->

**Moment 1 Improving filtering item's description in `tools.py::search_listings`**

- *What I asked for:* I asked Claude on how to improve the filtering for the item description
- *What came back:* A list of revisions of how to remove the redundant code and make fixes to a bug
- *What I changed:* I applied the suggested changes and added more words to filter out of the descriptions based on the test queries I did. 

**Moment 2 Filing out run_agent() in agent.py** 

- *What I asked for:* I had GitHub CoPilot help set up the code lines for each of the steps 
- *What came back:* It introduced a parse_query helper function with a regex pattern matching
- *What I changed:* I changed the regex pattern matching to recognize the description, price, and size in more varied queries. 

<!-- ═══════════════════════ UNIT 4 — THE TEST ═══════════════════════

     Don't fill these in during unit 3.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Run Log — Before

<!-- Five criteria, five tries each, in this exact format.

     Five, because your criteria are written out of five. Mark each try PASS
     or FAIL, count the passes, and read that count against your target — a
     row targeting 4 of 5 with three PASS cells is MISSED (3/5).

     `python run_eval.py --label before` runs everything and writes the table
     into results/. Paste it here and fill in the verdicts. -->

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |  |  |
| 2.  |  |  |  |  |  |  |  |
| 3.  |  |  |  |  |  |  |  |
| 4.  |  |  |  |  |  |  |  |
| 5.  |  |  |  |  |  |  |  |

**Real output from one try**, pasted as text, naming the file and function
that produced it:

```

```

---

## Verdicts and Diagnoses

<!-- MET or MISSED per criterion against LAST UNIT's target, plus a sentence on
     how you decided.

     Then, for every miss: which of the four places it happened — a tool, the
     loop's branch, the session, or the model's output — AND the mechanism.

     Not a diagnosis:  "The fit card was bad."
     A diagnosis:      "The fit card criterion missed on 2 of 5 items. Both had
                        an empty brand field. My prompt puts the brand in the
                        first sentence, so the card opened with a blank and read
                        like a fragment. The tool worked; the prompt assumed a
                        field that isn't always there."

     Look for a pattern. Three misses on the same tool is one problem, not
     three. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |
| 4 |  |  |  |  |
| 5 |  |  |  |  |

**Diagnoses**



---

## Loop Trace

<!-- One full run, printed step by step, with the MCP call visible in it.

     `python app.py ask '...' --trace` once you've added the trace.step()
     calls in Milestone 2.

     Worth pasting BOTH the happy path and the empty-search path. The empty
     one should be visibly shorter, because it stops. If your two traces are
     the same length, your branch isn't working — and this is the fastest way
     anyone will ever find that out. -->

**Happy path**

```

```

**Empty search**

```

```

**On the MCP move:** <!-- what changed in your code, and whether anything
behaved differently afterwards. If the rewire didn't work, say exactly where it
broke — the error text and the last thing that worked. That earns the point in
full. -->



---

## The Improvement

<!-- What you changed, why your diagnosis pointed at it, and the after-run in
     the same table format. One change, measured properly.

     `python run_eval.py --label after` -->

**What I changed:**

**Which failure it was meant to fix:**

### Run Log — After

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |  |  |
| 2.  |  |  |  |  |  |  |  |
| 3.  |  |  |  |  |  |  |  |
| 4.  |  |  |  |  |  |  |  |
| 5.  |  |  |  |  |  |  |  |

**Did it help, and how do I know:**

<!-- If it made things worse, say that. Honestly reported, that earns full
     credit and is more interesting than one that worked. -->



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped where
     you did. "I ran out of time" is fine if it's true. Pretending nothing is
     left is not. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 3

       [ ] criteria.md has five numbered criteria, each with a target
       [ ] Each criterion has a reason underneath it
       [ ] All five unit 3 sections above have real content
       [ ] Tool Inventory: all three tools, inputs WITH TYPES, a specific
           return value, and the empty case
       [ ] Planning Loop names the branch rule and agent.py::run_agent
       [ ] Sample Run: one full query plus the three per-tool tests, as text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN, you submit the same one
           next unit

     SUBMISSION CHECKLIST — unit 4

       [ ] mcp_server.py exists with one tool registered
           (or a written record of exactly where the rewire broke)
       [ ] Run Log — Before, five criteria, five tries each
       [ ] Real output pasted underneath, naming file and function
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, naming a place AND a mechanism
       [ ] Loop Trace, with the MCP call visible in it
       [ ] All three failure modes triggered and handled
       [ ] One improvement, with Run Log — After in the same format
       [ ] What's Still Broken
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository. Your commit history is what
     shows your criteria existed before your results did.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**

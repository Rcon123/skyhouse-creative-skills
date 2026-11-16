---
name: strategist-segments
description: Build an offer's segment map and personas for the Strategist pack using the WHAT / WHO / WHY model from Creative Diversity Decoded, outcomes, sub-outcome lenses, demographics, facets, then crystallize the highest-value combinations into named personas and write offers/<slug>/SEGMENTS.md. Invoke when the user addresses the strategist about slicing a market, finding new audiences or hidden pockets, or naming personas for an offer, e.g. "strategist, map my segments", "strategist, build personas for <offer>", "strategist, who should we be targeting", /strategist-segments, or when the strategist hub or strategist-offer routes here. Pairs with the optional segment-builder.html visual tool (offer the importable JSON at the end). Planning-only pack: never generates creative, never runs npx exodus. Only invoke when the user explicitly addresses "strategist" (or is clearly continuing a strategist conversation). Never claim generic segment, persona, or audience requests; in this shared folder those may belong to the exodus-* pack or the user's other tools. If the user says "exodus", this skill is not for them.
---

# Strategist Segments: build the offer's segment map + personas

You are cutting the offer's market into sharp, findable **segments** and turning the best ones into named **personas**. The output is `offers/<slug>/SEGMENTS.md`: the rows of the coverage grid that strategist-plan will draw.

Before starting, read `offers/<slug>/OFFER.md` and skim `inputs/` (the buyer brief and VSL usually contain half the answers, and all the VOC). If the offer folder does not exist, route to strategist-offer first.

Work **conversationally**: ask, propose, let Ryan react. Do not dump the whole framework at once. Move one layer at a time.

---

## The core idea (say this plainly if needed)

You never make one ad for "everyone." Talking to everyone = talking to no one. You cut the whole market (the **TAM**) into pieces small enough to look one in the eye. A cut piece is a **segment**; a segment with a name and a face is a **persona**.

There are only **three** ways to cut, and they are complete, there is no fourth:

| | Question | We call it | When |
|---|---|---|---|
| **WHAT** | do they want? | **Outcomes** | the spine, do first |
| **WHO** | are they? | **Demographics** | the easy layer |
| **WHY** | are they here / what's true now? | **Facets** | the deepest, most powerful |

`A segment = one Outcome x a Demographic x a Facet or two.`

Two rules apply at **every** layer:
- **The say-it test:** would a real customer say this out loud?
- **The gate:** only make a new slice if it would need a **genuinely different ad**. If two slices run the same ad, they are one slice. Merge them.

---

## 1. Outcomes: the WHAT (the spine)

The end-state they are buying: a **pain gone** or a **result they want**. Not the mechanism, not the brand.

- **Want test:** push past the mechanism to the thing they would actually feel. Nobody wants "collagen", they want *fewer wrinkles*.
- **Read the market, not the rulebook:** a mechanism can *graduate* into an outcome when the market lives in it (men literally want *"my testosterone up"*). If they would say the word and it points at something they feel, keep it.
- **Sort by WANT, never by TYPE.** Pest control by pest (roaches, ants...) is wrong, nobody wants "less mosquito." Sort by the want the pest blocks (*get them out · stop them hurting us · protect the house · get my outdoor life back · keep them from coming*). Do this and the mosquito shows up in **two** rows (scared mom vs guy who wants his deck), two ads that sorting-by-type would hide.

Aim for ~4 to 7 outcomes.

## 2. Sub-outcomes: the finer WHAT (optional)

Cut a want finer to open hidden pockets ("weight loss" -> *"I hate my man boobs"*). Use one of **five lenses**:

- **Type**: swappable variants (sun-spot / melasma; roaches / ants)
- **Location**: a place: body part, surface, room (forehead lines; the yard)
- **Function**: an ability / job, *"I want to be able to ___"* (get hard again; focus)
- **Moment**: a time: recurring trigger, or now-vs-later (2pm crash; *and prevention lives at the tail here*)
- **Severity**: intensity, mild -> crisis ("I saw one" -> "we're infested")

**Rule:** never use all five. Each outcome has **one primary lens** (skincare/pest -> Type; testosterone -> Function; sleep/energy -> Moment). Find it, that is ~80% of the value. Add a second lens only if a customer says it out loud **and** it needs a different ad.

## 3. Demographics: the WHO (the easy layer)

Traits a stranger could tick **from across the room**. Five, **ask Buyer first**:

1. **Buyer**: who *pays*, and are they even the user? (wife buying for husband; owner buying dog food). Get this wrong and every later ad aims at the wrong face.
2. **Gender**
3. **Age**: usually better as rough life-stage than a number.
4. **Race / Ethnicity**: only where it changes the product's job (skin tone, hair type).
5. **Identity** *(solidified)*: visible life facts: married, new dad, retired, income tier, region, faith.

Cross an outcome with a demographic and one want blooms into several (3pm crash x 20s = "too young to be this tired"; x 60s = "keep up with the grandkids"). Same gate: only split if it changes the ad.

**Learned rule (Ryan, 2026-07, MOFO):** buyer briefs understate the older end. Ryan's health-supplement audiences run older than the stated range, often 65+. Always propose at least one 60+ persona (grandkids energy, independence, finish-strong) and let Ryan cut it, rather than waiting for him to catch the miss.

## 4. Facets: the WHY (deepest, most powerful)

What is going on inside. Five families, reach for the ones that light up the market:

| Family | Is it... | Test | Controls |
|---|---|---|---|
| **Belief** | a theory already in their head | *"I think ___ is true"* | the **argument**. Echo a belief they already hold, never install your own |
| **Identity** *(tribe)* | a chosen self-label | *"I'm the kind of person who ___"* | the **vocabulary + hard-nos** (gym-rat, clean-beauty, prepper) |
| **State** | true now / already tried | *"right now I am ___"* | the **problem you lead with** (on a GLP-1, postpartum, tried Accutane) |
| **Value** | what matters in the buy | *"what matters is ___"* | the **promise** (organic, fast, cheapest, the best) |
| **Occasion** | the event that put them in-market | *"it changed when ___"* | the **why-now / urgency** (had a baby, turned 40, scary lab) |

**The power move: stacking.** Any real person holds one from each family at once. Stack **two** and you invent a pocket nobody targets (*vegetarian x just had a baby* = vegan postpartum recovery). Stack **three-plus** and you have described one person in a Reddit thread, no volume. Gate: a stack is real only if enough people sit in it *and* it needs a different ad than either facet alone.

**Biggest trap (Belief):** write the *customer's* belief ("my hormones are the problem"), not the marketer's ("science-backed ingredients"). You *find* beliefs, you do not install them.

> Note: "Identity" appears in both Demographics (solidified/visible: married, retired) and Facets (chosen tribe: gym-rat). Don't agonize; put it where it helps write a better ad.

---

## How to run a session

1. **Intake.** Read OFFER.md + inputs/ first. Then ask only what is still unknown (2 to 3 questions max).
2. **Outcomes.** Draft the spine sorted by *want*. Run the want-test + say-it test. Flag any mechanism that has graduated. Get Ryan's nod.
3. **Sub-outcomes (optional).** For the 2 to 3 juiciest outcomes, name the primary lens and cut 3 to 5 real sub-slices. Apply the gate hard.
4. **Demographics.** Buyer first, then gender/age/(race)/identity. Only keep cuts that change the ad.
5. **Facets.** Walk the five families; pull out beliefs/states/occasions **the customer already has** (mine inputs/ and any VOC in the buyer brief). Note which 2 stack into a fresh pocket.
6. **Personas.** Pick the 5 to 15 highest-value combinations (big enough, reachable, pain sharp enough to act). For each, fill the full fuel tank (every field must load an ad):
   - **Handle**: alliterative name keyed to its defining trait (State -> Belief -> Occasion -> Identity -> Value priority): *Cortisol Carl, TRT Travis, Postpartum Priya*
   - **Coordinates**: Outcome x sub-slice x demographic x facet(s)
   - **One-liner**: who she is, instantly
   - **Pain, in HER words**: the lived version, not "low energy"
   - **The promise she's chasing**: after-state plus who she gets to become
   - **What she already believes**: echo, never install
   - **Her constraints**: tried, won't do, can't afford
   - **VOC**: up to 10 to 20 verbatim phrases harvested from inputs/ (reviews, comments, brief quotes). Quote verbatim, never paraphrase. If VOC had to be invented rather than harvested, mark the section **VOC: THIN, needs harvesting** so the gap is visible.
7. **Write `offers/<slug>/SEGMENTS.md`:** the outcome spine (with lenses and sub-slices), the demographic cuts that survived the gate, the facet families with live values, then one persona sheet per persona. Update PLAN.md's Status block: Next action "build the plan (strategist-plan)".
8. **Offer the JSON.** If Ryan uses `segment-builder.html`, also give the importable JSON block (format below). Keep the WHO groups named `Buyer, Gender, Age, Race / Ethnicity, Identity` and the WHY families named `Belief, Identity, State, Value, Occasion` (the tool's persona-sentence logic keys off these names). Values are plain strings.

```json
{
  "brand": "<brand>",
  "product": "<product>",
  "outcomes": [ { "name": "...", "lens": "Severity", "subs": ["...", "..."] } ],
  "demos": [ { "name": "Buyer", "values": ["self", "wife / partner"] } ],
  "facets": [ { "name": "Belief", "values": ["...", "..."] } ]
}
```

Throughout: prefer few sharp slices over many fake ones. When unsure, ask "would this need its own ad?" If no, merge it.

## Rules

- Never write into `state/`, `references/`, or `.exodus/`.
- No em dashes anywhere in output. Hard rule.
- Hand off when done: "Segments are mapped. Say 'strategist, plan <name>' to build the map."

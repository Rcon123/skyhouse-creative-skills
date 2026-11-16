---
name: intake-check
description: The pre-launch alignment check Ryan promised Liya on the 2026-10-26 EOS call. Takes an offer slug plus what we plan to launch (angle, hooks, lander headline, where the ad sends traffic) and checks it line by line against that client's intake form and their own funnel (what the VSL or product page actually opens with). Output is a short report in offers/<slug>/intake-checks/ with ALIGNED / PARTIAL / MISMATCH / NOT IN INTAKE per element, the intake line each one was checked against, and a paste-ready paragraph for the account managers so they have answers for the client. Invoke whenever Ryan says "intake check", "check this against the intake", "does this align with the intake form", "run the alignment check on <offer>", "AM note for the <offer> launch", or /intake-check. Runs before a launch task goes to the buyers and again when a campaign changes angle. Never posts to ClickUp, Slack or email; Ryan sends the note.
---

# Intake check: does what we're launching match what the client told us?

**Why this exists (10-26):** Prodenta launched on the anesthesia angle (the client's stated best angle) while the client's VSL opens on bad breath and bleeding gums and never says anesthesia. Liya read ad to funnel, saw no correlation, and had no answer for the client. Ryan: "I just want to make sure this aligns with the intake form." This skill is that check, plus the note the AMs get at launch.

## What it checks (every launch, every element)

| # | Element | Checked against |
|---|---|---|
| 1 | Angle | intake: angles that worked / flopped; "biggest objection" |
| 2 | Pain point the ad leads with | intake: problem solved; flop list; what the funnel's own page opens with |
| 3 | Avatar | intake: ideal buyer, unexpected groups |
| 4 | Hooks and headlines | red-line words, named doctors, competitors, the angle |
| 5 | Lander headline and opener | same as 4, plus: does it bridge the ad to the next step |
| 6 | Funnel step and destination | intake: funnel type (VSL / PDP / squeeze), product page URLs, onboarding doc |
| 7 | Handoff chain | ad hook -> lander H1 -> lander opener -> what the destination opens with (reverse brief). This is the one that would have caught Prodenta |
| 8 | Proof and numbers | intake: studies, trial numbers, social proof. Any number not in the client's material is a MISMATCH |
| 9 | Compliance red lines | intake: disclaimers, never-use words, competitor naming, fake doctors, AI consent |
| 10 | Product-blind rule | intake funnel line ("VSL - product blind") |
| 11 | Images | what they show vs the angle, the avatar, the red lines |

## Ratings

- **ALIGNED**: matches an intake line. Quote it.
- **PARTIAL**: matches in part, matches the client's proven ads but not the form, or needs a one-line explanation to the AM. Always say what the AM should say.
- **MISMATCH**: contradicts an intake line, a red line, or the funnel's own lead. Goes in "Fix before launch".
- **NOT IN INTAKE**: the form is silent. Checked against the funnel or research instead; becomes an ask for the client if it matters.

A launch with any MISMATCH does not go to the buyers until Ryan clears it.

## The flow

1. **Gather.** `python3 tools/intake/intake_check.py <slug> --new <launch-name> --scan <ads.md> <lander.html> ...`
   Prints the intake bundle (raw survey, the "what the client told us" + funnel + congruence sections of `research/00-client-assets.md`, the lead of the VSL/page reverse brief, OFFER.md red lines), a red-line word scan of the launch copy with context lines, and creates `offers/<slug>/intake-checks/<date>-<name>.launch.md` from `LAUNCH-template.md`.
   Missing sources are listed at the top. If there is no `inputs/intake-survey*.txt`, ask Ryan where the live form is (Dropbox `/!SH - Offers/<client>/Assets/` holds the docx; `textutil -convert txt` it into `inputs/`). Never guess intake content.
2. **Fill the launch spec** from the actual files (ads FINAL, lander HTML title/H1/opener, DB image map, the ClickUp task). Verbatim hooks. If Ryan dictated the launch in chat, use his words and mark anything you had to look up.
3. **Judge each element** with the bundle open. Quote the intake line in the table, with the question it came from. Read the funnel lead from the reverse brief (the "biggest mismatch" line and the first table), not from memory.
4. **Write the report** to `offers/<slug>/intake-checks/<date>-<name>.md` on `REPORT-template.md`. The AM paragraph is the deliverable: plain English, what launched, where it goes, which intake lines it's built on, what is deliberately different and why, what we test next. Ryan's voice, no em dashes, no jargon the client won't know (no "AT1", no "squeeze" without saying what it is).
5. **Show Ryan** the verdict line, any MISMATCH, and the AM paragraph in chat. He edits, he sends. Nothing is posted anywhere by this skill.

## Rules learned on the first runs (10-26)

- The client's proven ads and the client's form can disagree with the client's own VSL. When they do, the rating is PARTIAL, not MISMATCH, and the AM note says so plainly: "the client told us X is their best angle; their video does not pay it off; our page bridges it with the video's own opening symptoms." That is the answer Liya needed.
- "Can we name competitors: No" is about supplement competitors. Pantry brands the funnel itself villainizes (Greenies, Dentastix) are villains, not competitors. Still a PARTIAL with a confirm line, because the AM will get asked.
- A hypothetical narrator (editor, groomer, nurse) is covered by "hypothetical prospect stories: yes". A named doctor who does not exist is not. A real doctor named without the client's say is not.
- Disclaimer boilerplate ("not intended to diagnose, treat, cure") is not a red-line hit. Everything else that says cure, reverse, heal is.
- Numbers only from the client's material or the research pack with a source line. The Cloud9 case-report scrap (10-26) was an invented "6 flagged tests".
- Intake survey text from a docx can come out questions-first then answers (Cloud9). Map answers by order; when unsure, cite `00-client-assets.md`, which already did the mapping.

## Files

- `tools/intake/intake_check.py` gather + scan + stamp (stdlib)
- `LAUNCH-template.md` what Ryan feeds it
- `REPORT-template.md` what comes out
- Reports: `offers/<slug>/intake-checks/<date>-<name>.md` (and the `.launch.md` next to it)
- First runs: `offers/prodenta/intake-checks/2026-10-26-squeeze-top5.md`, `offers/cloud9/intake-checks/2026-10-26-her-story.md`

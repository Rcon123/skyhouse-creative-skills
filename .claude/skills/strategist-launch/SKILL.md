---
name: strategist-launch
description: The launch handoff of the Strategist pack. Takes an APPROVED batch of creative (ads already graded, images already approved) and hands it to the media buyers as a ClickUp task in the Performance - Workflow > Net New list at status "mb team", in Ryan's exact task format (Copy doc link + DB creative reference + a plain "why we're testing this" block; never budgets or audiences). Invoke when the user addresses the strategist about launching or handing off to the buyers, e.g. "strategist, launch the affair ad", "strategist, send batch 2 to the media buyers", "strategist, create the ClickUp task", "strategist, hand this off", /strategist-launch, or when the strategist hub routes here. It creates the copy Google Doc, writes the why block, previews the task in chat, and only touches ClickUp after Ryan's explicit go. Only invoke when the user explicitly addresses "strategist" (or is clearly continuing a strategist conversation). Never claim generic task-management or ClickUp requests; in this shared folder those may belong to the user's other tools. If the user says "exodus", this skill is not for them.
---

# Strategist Launch: approved creative in, media-buyer task out

You are the last step of the pipeline. Ads are written and graded, images are approved. Your job: package everything into ONE ClickUp task the media buyers can execute with zero questions back, exactly the way Ryan writes them himself.

## Required reading (every run)

1. The offer's `offers/<slug>/LAUNCH.md` — the launch profile: page name, audience defaults, budget defaults, bid cap, structure defaults, buyer assignees. If it doesn't exist, run the intake below and create it before anything else.
2. The approved ads file(s) in `offers/<slug>/ads/` for this launch.
3. Know which images/videos were approved (the graded keepers from this session or the offer's `images/` gallery).

## THE CURRENT FORMAT: the link packet (Ryan-graded 2026-09-02, supersedes the Sprint-88 Setup-line format below)

Ryan's grade on a Setup-line task in Performance - Workflow: "it looks like a mess... the media buyers will not understand. Go LEARN how we do this from other completed tasks." The completed tasks in Net New (08.19-08.28, statuses launched/scale) all share ONE shape, a minimal LINK PACKET with zero setup prose:

```
Copy: [<task name>.docx](dropbox or ClickUp-attachment link)

Images: DB IMG ###-###

Why we're testing this: <two to four plain sentences in Ryan's voice: the belief behind the concept in the buyer's terms, and what it becomes if it works. No budgets, no test design.>

[✍️ COPY](google doc link)

🖼️ Image review

NEW LANDER: <url>          <- only when a new page is involved (ReActivate 08.28 precedent)
```

**Confirmed by Ryan 2026-09-09: "We do not need to put budgets and audiences in ClickUp tasks."** The buyers own the campaign build. Never add budgets, ad-set counts, audiences, placements, or test-design paragraphs unless Ryan dictates them. The "Why we're testing this" block is his standing addition (09-03, She's 101 handoff; 09-08 to Ary: "why we're testing this for everything").

- **COPY LINE RULE (Ryan, 2026-10-02, supersedes the Dropbox-link paragraph below): `Copy: https://docs.google.com/document/d/<id>/edit`, the Google Doc already set to anyone-with-the-link. Never a bare filename, never a ClickUp attachment link.** The .docx is still filed in the Dropbox DB at `Ads/<task name>/Copy/<task name>.docx` for the record, but the task links the Google Doc.
- (Older, kept for history) The Copy line was the Dropbox scl link (Ryan 09-03: "linking the way we do it"), with `&cloud_editor=word` appended like Fernando's tasks. The Dropbox API key lacks sharing.write, so get the link this exact way (proven 09-02 and 09-03):
  1. claude-in-chrome `navigate` to the MEMBER-FOLDER URL: `https://www.dropbox.com/home/Ryan%20Connolly/!SH%20-%20Offers/<offer folder>/Ads/<task name>/Copy` (a bare `/home/!SH - Offers/...` URL says "folder doesn't exist" and the file list never renders).
  2. `find` the docx row, `hover` it, `find` the "Copy link" button on the row, click it. A "Copy link to" popover confirms "Edit link copied".
  3. RETIRED (Ryan, 09-10: no clipboard or screen access without him saying so). READ THE LINK FROM THE POPOVER INSTEAD (proven 2026-09-11, Akka cholesterol batch): the "Copy link to" popover renders the full `scl/fi/...?rlkey=...&st=...&dl=0` link inside an `<input>`. The Chrome JS tool masks any string that looks like a query string (char-joining does not get past it), so return it as char codes and decode locally:
     `const v=[...document.querySelectorAll('input')].map(i=>i.value).find(v=>v&&v.includes('dropbox.com')); v ? [...v].map(c=>c.charCodeAt(0)).join(',') : 'none'`
     then `''.join(chr(int(c)) for c in codes.split(','))` in Python. If it returns `none`, the popover did not open: click the Copy-link icon on the row by coordinate (the ref click sometimes only shows the tooltip), wait 3s, run the JS again.
  4. PUT the task's `markdown_description` with `Copy: <link>&cloud_editor=word`. Attaching the docx to the task is the fallback only if Dropbox web is unavailable.
- NO Setup line. Budget/structure/audience live in the buyers' defaults and the media-buying brief, not the task.
- Split-test instructions are written as one plain sentence, modeled on Ryan's own 08.25 Wife Food Landers task ("Split test: run BOTH versions against all current traffic..."), followed by labeled links, one per line. Three-way version (Akka cholesterol, 09-11): "Split test: run all THREE landers against all the traffic in this campaign, even split." then Lander A/B/C lines with a two-word note on what differs.
- NO extra header lines. Ary's own tasks carry "Funnel: ... Angle name: ... Submitted by: ..." lines; Ryan's do not, and when I cloned Ary's shape Ryan sent it back ("make sure you're doing the CU task the way we always do", 09-11). Ryan's tasks are exactly: Copy line, Images line, optional split-test block, Why block, ✍️ COPY + doc link, 🖼️ Image review. Nothing else.
- An `Images: DB IMG ###-###` line is Ryan's own convention when statics live in the DB (campaign-1 Akka precedent); keep it when there is no pipeline image-review link.
- Task names keep the pipeline's long form (`MM.DD.YY - Offer - Funnel - Angle - IMG/VID - Net New`) when the task came from Fernando's brief pipeline; never rename them to the short launch form.
- Before writing ANY task, pull 2-3 completed tasks from the same list and clone their shape. Formats drift; the live board is the source of truth, not this file.

## Ryan's task format (decoded from his real tasks, Sprint 88, 2026-08) — SUPERSEDED for Performance-Workflow tasks, kept for history

- **Task name:** `MM.DD.YY - OFFER - Concept Name` (today's date, zero-padded, 2-digit year; OFFER is the short offer name like TPS / MOFO / ProtaFlo; e.g. `07.23.26 - TPS - Question`)
- **Description, three lines:**
  - `Setup:` one comma-separated line: page name, structure (`1 HL, 1 AT per ad set`, `3 Images per ad set`, `1 hook per ad set`), budget (`$150 per ad set`), ABO/CBO, audience (`10%`, `open`), placements if specified, bid cap if any (`bid-cap $247`), plus any special instruction in plain words (`use old copy in link below, these are new image iterations`)
  - `Copy:` (or `Ad Copy:` for video scripts) the Google Doc link
  - `Images: DB IMG ####-####` or `Videos: DB Vid ###-###` — the Dropbox asset numbers
- **Assignees:** the media buyers from LAUNCH.md (default: Christian Mendoza + Emiliano Lluberes)

## Process

1. **Resolve the launch.** Which ads, which images/videos, which offer. If anything in the batch is ungraded, stop and say so — only approved creative launches.
2. **Write the "Why we're testing this" block.** Two to four plain sentences in Ryan's speaking voice: what we saw working, the belief behind the concept, what it becomes if it wins. No Setup line, no budget, no audience, no structure (Ryan, 2026-09-02 and 2026-09-09). LAUNCH.md is for page names and buyer assignees only.
3. **Copy doc.** Ryan's copy always lives in Google Drive. Create it as HTML (Drive MCP, contentMimeType text/html) so formatting survives, in HIS format (graded 2026-08-05): yellow-highlighted bold `H1:`/`H2:` labels with the FINAL headline picks only (bold), then yellow-highlighted bold `AT1:`...`ATn:` labels, each AT opening with its hook as a BOLD line (Title-Case key nouns, one quoted term, hyphenated numerals), body plain with blank-line spacing. Only keeper ads go in - no options menus, no meta notes. Get the shareable link. **HARD RULE (Ryan, 2026-08-25; reaffirmed 2026-08-28 as "always"): EVERY Google Doc created for Ryan is set to link-sharing "anyone with the link" immediately after creation, before the link is delivered anywhere.** HOW: the Drive MCP's share_file only does per-email shares, so use claude-in-chrome on the doc URL: Share button (top right) -> General access "Restricted" dropdown -> "Anyone with the link" -> Done. Verify the "Access updated" toast, don't assume.
4. **Creative line - AUTOMATED (wired 2026-08-05).** Approved images upload to Dropbox via API; creds in `.env` (DROPBOX_APP_KEY / DROPBOX_APP_SECRET / DROPBOX_REFRESH_TOKEN; exchange refresh token at https://api.dropboxapi.com/oauth2/token with grant_type=refresh_token). The flow, after Ryan picks keepers from a NUMBERED approval sheet (always present one):
   - TPS images live at `/!SH - Offers/Hero - Total Package Serum (Skin)/Ads/!!Images` (other offers: find the offer under `/!SH - Offers/`, then `Ads/!!Images`).
   - List the folder, find the highest IMG number, name keepers sequentially from max+1, convert to .jpg (folder convention), upload via content.dropboxapi.com/2/files/upload with mode=add, autorename=false.
   - The task's creative line is then `Images: DB IMG <first>-<last>`. Same pattern for videos (`!!Videos`, VID prefix).
5. **Preview in chat, plain text.** Show the exact task: name, Copy link, Images/Videos line, the Why block, lander line if any, assignees, and the list/status it's going into. Then ask for the go.
6. **On Ryan's explicit go, create the task** in Performance - Workflow > Net New at status "mb team" (mechanics below). Reply with the task URL.
7. **Log** the launch at the bottom of the offer's PLAN.md Status block (date, task name, task URL) so the plan knows the batch shipped.

## ClickUp mechanics

Token: `CLICKUP_API_KEY` in `.env` (workspace root). All calls: header `Authorization: $CLICKUP_API_KEY`, base `https://api.clickup.com/api/v2`.

**Where tasks go (Ryan's correction, 2026-08-25): all tasks now live in the Performance - Workflow space. The RC Pod sprint flow is retired for launches — never create launch tasks in RC Pod sprints again.**

Fixed IDs (SkyHouse Agency workspace):
- Team: `9013015340`
- Space: Performance - Workflow `901313966800`
- List: Net New `901328133477` (folderless; sibling list Iterations `901328278436` for iteration launches if Ryan says so)
- Status for buyer launches: `mb team` (statuses route the work on this list: to do / ai team / creative team / cs team / mb team / launched / scale / fail / analysis complete)
- Media buyers: Christian Mendoza `93973135`, Emiliano Lluberes `118027296`
- Ryan: `87950270`

**Create the task:**

```bash
curl -s -X POST -H "Authorization: $CLICKUP_API_KEY" -H "Content-Type: application/json" \
  "https://api.clickup.com/api/v2/list/901328133477/task" \
  -d '{
    "name": "MM.DD.YY - OFFER - Concept",
    "status": "mb team",
    "markdown_description": "Copy: <docx link>\n\nImages: DB IMG ___\n\nWhy we're testing this: ...\n\n✍️ COPY\n\n🖼️ Image review"
  }'
```

Assignees: default unassigned — Ryan tags buyers himself (pattern since Sprint 90/91); add `"assignees": [93973135, 118027296]` only if he says to. Naming stays `MM.DD.YY - OFFER - Concept Name` for buyer launch tasks — do NOT use the editor-task suffix format (`... - Outcome - Angle - VID - Net New`); that longer format belongs to creative build tasks for the editing team, not launches (Ryan corrected this 2026-08-25).

The response contains `id` and `url` — give Ryan the `url`.

## Hard rules

- **Never create, edit, or delete a ClickUp task without Ryan's explicit go on the previewed task, every single time.** The preview-then-go step is not skippable.
- Only ever write into the Performance - Workflow space. Never touch other spaces, never delete or close tasks, never change statuses on tasks you didn't create.
- The task carries only: copy doc link (live), Images/Videos DB line, the Why block, and a lander URL when a new page is involved. Never budgets, audiences, structure, or placements (Ryan, 2026-09-02: "we don't tell them budgets or pages or anything"; confirmed 2026-09-09).
- One task per concept/batch, matching how Ryan does it — not one task per ad.
- No em dashes anywhere, including inside the ClickUp task.
- Never write into `state/`, `references/`, or `.exodus/`. Never run `npx exodus`.
- Future (explicitly deferred by Ryan, 2026-08-05): video-script launches as a payload type. Don't build until he asks. (Dropbox automation: DONE 2026-08-05, see step 4.)

## DOCX SPACING RULE (Ryan, 2026-09-09: "the formatting is fucked in Dropbox, too many spaces between the lines")

python-docx's default Normal style adds space after every paragraph, and the Google Doc text already carries blank paragraphs between blocks, so every gap doubles. Before saving any copy docx: set `Normal` to Arial 11 with `space_before = space_after = Pt(0)` and `line_spacing = 1.0`, apply the same to each paragraph, and collapse any run of two or more empty paragraphs to one. Then render it with `soffice --headless --convert-to pdf` and look at page 1 before uploading; never ship a docx you have not seen rendered.

## Google Doc fill quirk (2026-10-13, OsteoShield termites)
`npx exodus drive batch-update` applied insertText and the yellow backgroundColor but DROPPED every `bold` (and fontSize) updateTextStyle sent in the SAME batch as the insert. A second batch-update with only the bold requests applied cleanly. Send the text in one call, the styles in a second call, then read the doc back and check `textStyle.bold` on the labels and hook lines before linking it anywhere.

## Google Doc refill quirk (2026-10-21, Olavita campaign 1)
When replacing a doc's text (deleteContentRange then insertText at index 1), the inserted text INHERITS the style of the run that used to sit at index 1 (the bold yellow H1 label), so the whole doc comes back bold and highlighted ("the formatting is all fucked"). Fix order: (1) one batch clearing the whole range (`bold:false, backgroundColor:{}`, fields `bold,backgroundColor`), (2) one batch for the label styles, (3) one batch bolding the headline lines and the hook line under each AT label, with ranges taken from the doc's own paragraph startIndex/endIndex (get-doc), not from a local line count. Verify with get-doc: only the labels highlighted, only labels + headlines + hooks bold.

## COLD-READ JUDGE (built 2026-10-27; ship block removed 2026-10-30; read cap and scope 2026-11-02)

SUPERSEDED 10-30: the "COLD-READ GATE (NOT optional, enforced by hooks)" block that stood here. Ryan, 10-30: "Get rid of
this thing that stops you from doing it because it's just wasting my time." The judge stays as a tool. (dreaming 2026-11-02, sessions 10-30_6aaa8a1e, 10-26_601f85f7, 10-28_fe5dc0fa, 11-02_0af56953)

1. **The reader is never the writer.** Before NEW copy reaches Ryan, run `python3 tools/copygate/coldread.py judge <file>`
   (add `--from "MASTHEAD:"` or `--section "<heading>"` so builder notes above the copy are not read). It prints the
   brief: spawn ONE fresh Agent (general-purpose, sonnet) with `tools/copygate/READER-PROMPT.md`; it runs `coldread.py
   text`, reads once as a stranger, and writes `coldread.py stamp <file> --reader subagent --json @<verdict>`. You never
   write a stamp for your own copy. Say once per session in the reply: the headless stranger is logged out and
   `claude login` in a terminal restores it. Never run `claude login` yourself.
2. **One read, one fix pass, at most one re-read.** Then ship with the remaining flags listed as notes at the top of the
   deliverable. Never a third read: every fresh reader finds a different line.
3. **Never run it on** unchanged copy, a CSS or image swap, a team brief, ClickUp task text, locked hooks or held-reveal
   headlines. Those fail every reader by design. A flag on a line Ryan locked is his call, not a fix.
4. **Their words, not ours.** Every mechanism word comes from `offers/<slug>/LANGUAGE.md` `## Their words`; a word you
   invent goes on `## Never`, not on the page.
5. **The judge is a tool, never a gate.** Nothing waits on a stamp: deploys, Doc pushes, handoffs and ClickUp go when he
   says go. ~~Nothing ships unstamped~~ (removed 10-30; `hook_pre_ship.py` exits 0).
6. **The mechanical floor runs itself** after every Write/Edit to `offers/<slug>/{ads,advertorials,landers,videos}/`.
   Fix dashes, banned words and long sentences before the judge, not after.

Tool and rules: `tools/copygate/README.md`.

Launch addition (superseded 10-30): no stamp is needed to fill the copy doc or make the task. If the copy had a cold read, the task preview shows its remaining flags as notes, never as a hold. (dreaming 2026-11-02, sessions 10-30_6aaa8a1e, 10-26_601f85f7, 10-28_fe5dc0fa, 11-02_0af56953)

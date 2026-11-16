# The Graveyard Study (v1, 2026-08-03)

The first survivorship-bias-free study of DR creative: 46,012 ads from 30 top direct-response health advertisers (Ryan's followed brands + the liver market), pulled via Atria back to Aug 2024, deduplicated and clustered into 4,934 distinct creatives, each with a birth date, death date, scale count, and live/dead status. Presentation page: `source/graveyard/graveyard-study.html` (published artifact). Engine + results JSON in `source/graveyard/`; re-run `graveyard.py` against a scratchpad `atria/` folder of brand pulls to refresh or extend.

## The laws (v1)
1. **Mortality:** of 1,007 creatives old enough to judge, 38% die within 7 days, 48% within 21, only 17% reach 180 days. Half of everything launched is dead inside three weeks.
2. **Graveyard DNA (editorial hooks only, 645 killed vs 237 survivors):** overrepresented among the killed: first-person "I/my" hooks (19% vs 14%) and blind-curiosity wording (25% vs 20%), the two most-preached styles in the industry. Overrepresented among survivors: 6 words or fewer (67% vs 53%), contains a number (27% vs 17%), emoji (10% vs 2%), ALL-CAPS word (9% vs 4%). Confound control: sale/product-named/benefit-bullet ads excluded from both piles.
3. **The iteration law:** the biggest accounts launch ~9 iterations per new idea (Live Anabolic 7% new, Found 11%, Emma 12%, Better Sleep 13%, Akka 21%); every account churning 80-100% new ideas is small and has no creative older than ~4 months. Ryan's Bankers-heavy doctrine, measured across the market.
4. **Format lifespans:** scaled video creatives live a median 56 days vs 24 for statics; 49% of statics die within 3 weeks vs 36% of videos; 8 of the corpus's 10 longest-lived creatives are video (oldest: Live Anabolic's "Why Men Over 40 Should Avoid These Common Foods...", 832 days, 1,633 copies, still live).
5. **Shared templates:** "7 seconds" appears in 2,706 ads across 4 unrelated brands (Akka liver, Emma gut, Better Sleep snoring, Live Anabolic); 30-second and 60-second claims span 14 and 8 brands. And Akka's three biggest videos all name their doctor at exactly 61% of runtime (whisper-verified).

## Method guards worth keeping
- "Killed fast" requires the account to still be launching 30+ days after the creative died, so account shutdowns don't count as kills.
- Mortality curve only counts creatives first seen 6+ months ago, so young ads can't inflate death rates.
- Trait analysis must run editorial-only as the headline number; evergreen sale/catalog ads otherwise pollute the survivor pile (they made emoji look 30pp instead of 7pp).
- No impressions exist in the API: copies = spend proxy, survival days = performance proxy, and the page says so plainly.

## v2 candidates (not run yet)
Structure law at scale (transcribe top videos across all 30 accounts, test the 61% turn), awareness-level distribution of winners vs killed, per-vertical splits, refreshing the corpus monthly to watch laws drift.

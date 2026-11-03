# Manifest — TPS Top 5 lander source extraction

**Date:** 2026-08-05
**Intended source:** Claude Design project "TPS Top 5" (projectId 4e8e3d5a-20cf-4d28-86c3-7c1824578e80) via the DesignSync tool.

## IMPORTANT: DesignSync unavailable this session

The DesignSync tool was not present in this session's tool registry (checked ToolSearch select + keyword queries, `~/.claude.json` MCP servers, project `.mcp.json`, and installed connectors — no DesignSync anywhere). **The project file listing could not be retrieved**, so per-path FETCHED/SKIPPED status against the live project is not possible.

What was recovered instead:

1. `feedback_transcript.txt` — already saved in this directory by a prior session (2026-08-05 00:20), presumably fetched when DesignSync was available. Kept as-is.
2. Three final lander HTMLs recovered **verbatim from local Cloudflare-upload export zips** in `~/Downloads/TPS Top 5 (N).zip` — these are point-in-time deployment bundles downloaded from the Design project (`upload/advertorial.html` + numbered images). Newest zip per family was used.

## Recovered files (source: local export zips)

| Saved file | Source | Status |
|---|---|---|
| `feedback_transcript.txt` | prior session (DesignSync) | FETCHED (prior session) |
| `TPS Top 5 - Prostate Flush (final, zip22 2026-07-21).html` | `~/Downloads/TPS Top 5 (22).zip` → upload/advertorial.html | RECOVERED-LOCAL |
| `Prostate Advertorial VSL - 3 Mistakes (final, zip21 2026-07-18).html` | `~/Downloads/TPS Top 5 (21).zip` → upload/advertorial.html | RECOVERED-LOCAL |
| `Top 5 Skincare Advertorial (final, zip20 2026-07-15).html` | `~/Downloads/TPS Top 5 (20).zip` → upload/advertorial.html | RECOVERED-LOCAL |

Superseded local zips (13, 14, 15, 16, 17, 18, 19) — SKIPPED (earlier versions of the same three families; 17/18 additionally carry hero-video.mp4/webm, skipped as video).

## Expected in the Design project but NOT retrievable this session

All marked **NOT-FETCHED (DesignSync unavailable)** — re-run the extraction in a session where DesignSync is loaded:

- TPS Top 5 v* final (the local zip22 copy above may or may not equal the current project final)
- Prostate Advertorial v* final
- Top 5 Prostate Advertorial
- 10 Reasons Ancestral Organs / 8 Reasons v2
- Ancestors Advertorial
- Protaflo Advertorial Longform
- Top 5 Skincare sub-families: Feminine, Longform variants, Health Magazine
- Transcript/feedback .txt files other than feedback_transcript.txt: cloudflare_transcript.txt, cf_transcript*.txt, transcript17.txt, vsl_script.txt, vsl_skin.txt
- Any .md files in the project

Images/video, uploads/, screenshots/, scraps/, src/, .thumbnail, .jsx, .napkin would have been SKIPPED per spec regardless.

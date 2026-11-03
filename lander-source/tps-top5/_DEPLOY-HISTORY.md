# TPS Top 5 — Deploy Bundle History

Listings only (`unzip -l`) of every "TPS Top 5" Cloudflare-upload zip in `~/Downloads`, in numeric order. 23 zips total: the base `TPS Top 5.zip` plus `(1)`–`(22)`, spanning 2026-05-20 to 2026-07-21. None of these were extracted here except zips 20–22, whose final `advertorial.html` files were pulled into this folder by a prior pass (see `_MANIFEST.md` / `_NOTES.md`).

## Timeline at a glance

| Zip | Downloaded | Files | Notable |
|---|---|---|---|
| TPS Top 5.zip | 2026-05-20 | 8 | First cut. `cloudflare-upload/index.html` + `assets/` with named skincare thumbs (`thumb-dermatologist`, `thumb-end-wrinkles`, ...). 18 MB of PNGs. |
| (1) | 2026-05-21 | 8 | Renamed `index.html` → `advertorial.html`, assets flattened to root, still named thumbs. |
| (2) | 2026-05-21 | 8 | Images renamed to generic `image1–7.png`. |
| (3) | 2026-05-21 | 8 | Same layout as (2), copy tweak only. |
| (4) | 2026-05-21 | 8 | PNGs compressed to JPG — zip drops 18 MB → 215 KB. |
| (5) | 2026-05-28 | 8 | Folder renamed `cloudflare-upload/` → `upload/` (convention from here on). |
| (6) | 2026-05-28 | 8 | Copy tweak only (HTML −2 bytes). |
| (7) | 2026-06-02 | 15 | Expanded build: 14 images, HTML grows to 71 KB. |
| (8) | 2026-06-04 | 9 | Different, shorter lander (35 KB HTML, new image set). |
| (9) | 2026-06-08 | 7 | Slimmer variant (31 KB HTML, 6 images). |
| (10) | 2026-06-16 | 10 | New 9-image variant, 51 KB HTML. |
| (11) | 2026-06-16 | 10 | Identical byte sizes to (10) — re-download/re-export. |
| (12) | 2026-06-17 | 9 | Another 8-image variant, 37 KB HTML. |
| (13) | 2026-06-23 | 10 | Iteration of the (10) family — image1 swapped, copy edits. |
| (14) | 2026-06-29 | 10 | Copy tweak of (13). |
| (15) | 2026-07-01 | 15 | Return of the 14-image build (73 KB HTML). |
| (16) | 2026-07-01 | 10 | Copy tweak of the (13)/(14) family. |
| (17) | 2026-07-08 | 17 | Adds `hero-video.mp4` (11.8 MB) + `.webm` to the 14-image build. |
| (18) | 2026-07-08 | 17 | Swaps in `hero-video2.mp4`/`.webm`, new image1. |
| (19) | 2026-07-13 | 15 | Video dropped again; 14-image build, 74 KB HTML. |
| (20) | 2026-07-15 | 15 | Final Top 5 Skincare advertorial (78 KB HTML). Extracted by prior pass. |
| (21) | 2026-07-18 | 14 | Prostate Advertorial VSL "3 Mistakes" (58 KB HTML, 13 images). Extracted by prior pass. |
| (22) | 2026-07-21 | 4 | TPS Top 5 Prostate Flush — slimmest bundle, 3 images. Extracted by prior pass. |

## Conventions observed

- Every bundle is one flat folder (`cloudflare-upload/` in zips 0–4, then `upload/` from (5) on) containing a single `advertorial.html` plus numbered `imageN.jpg` assets — a Cloudflare Pages drag-and-drop upload shape.
- Zip 0 used `index.html` + named asset files; from (1) on the page is always `advertorial.html`, and from (2) on images are always generic `imageN`.
- (4) is the compression milestone: same page, PNG→JPG, 85x smaller upload.
- (17)/(18) are the only bundles with video (`hero-video*.mp4` + `.webm` fallback).
- Duplicate byte-identical listings, e.g. (10)/(11), indicate re-downloads of the same Claude Design export, not new versions.

## Full listings


### TPS Top 5.zip
Downloaded: 2026-05-20 22:55 · zip size: 17957 KB

```
  Length      Date    Time    Name
---------  ---------- -----   ----
  2239072  05-20-2026 22:55   cloudflare-upload/assets/reveal-thumbnail.png
  2492727  05-20-2026 22:55   cloudflare-upload/assets/thumb-90-second.png
  2678939  05-20-2026 22:55   cloudflare-upload/assets/thumb-dermatologist.png
  5793580  05-20-2026 22:55   cloudflare-upload/assets/thumb-end-wrinkles.png
  2280441  05-20-2026 22:55   cloudflare-upload/assets/thumb-eye-bags.png
  1203017  05-20-2026 22:55   cloudflare-upload/assets/thumb-goodbye-wrinkles.png
  1686284  05-20-2026 22:55   cloudflare-upload/assets/thumb-wrinkle-reducer.png
    52104  05-20-2026 22:55   cloudflare-upload/index.html
---------                     -------
 18426164                     8 files
```

### TPS Top 5 (1).zip
Downloaded: 2026-05-21 00:02 · zip size: 17956 KB

```
  Length      Date    Time    Name
---------  ---------- -----   ----
    52048  05-21-2026 00:02   cloudflare-upload/advertorial.html
  2239072  05-21-2026 00:02   cloudflare-upload/reveal-thumbnail.png
  2492727  05-21-2026 00:02   cloudflare-upload/thumb-90-second.png
  2678939  05-21-2026 00:02   cloudflare-upload/thumb-dermatologist.png
  5793580  05-21-2026 00:02   cloudflare-upload/thumb-end-wrinkles.png
  2280441  05-21-2026 00:02   cloudflare-upload/thumb-eye-bags.png
  1203017  05-21-2026 00:02   cloudflare-upload/thumb-goodbye-wrinkles.png
  1686284  05-21-2026 00:02   cloudflare-upload/thumb-wrinkle-reducer.png
---------                     -------
 18426108                     8 files
```

### TPS Top 5 (2).zip
Downloaded: 2026-05-21 00:04 · zip size: 17956 KB

```
  Length      Date    Time    Name
---------  ---------- -----   ----
    51955  05-21-2026 00:04   cloudflare-upload/advertorial.html
  2239072  05-21-2026 00:04   cloudflare-upload/image1.png
  1686284  05-21-2026 00:04   cloudflare-upload/image2.png
  2492727  05-21-2026 00:04   cloudflare-upload/image3.png
  2678939  05-21-2026 00:04   cloudflare-upload/image4.png
  5793580  05-21-2026 00:04   cloudflare-upload/image5.png
  1203017  05-21-2026 00:04   cloudflare-upload/image6.png
  2280441  05-21-2026 00:04   cloudflare-upload/image7.png
---------                     -------
 18426015                     8 files
```

### TPS Top 5 (3).zip
Downloaded: 2026-05-21 00:11 · zip size: 17956 KB

```
  Length      Date    Time    Name
---------  ---------- -----   ----
    51955  05-21-2026 00:11   cloudflare-upload/advertorial.html
  2239072  05-21-2026 00:11   cloudflare-upload/image1.png
  1686284  05-21-2026 00:11   cloudflare-upload/image2.png
  2492727  05-21-2026 00:11   cloudflare-upload/image3.png
  2678939  05-21-2026 00:11   cloudflare-upload/image4.png
  5793580  05-21-2026 00:11   cloudflare-upload/image5.png
  1203017  05-21-2026 00:11   cloudflare-upload/image6.png
  2280441  05-21-2026 00:11   cloudflare-upload/image7.png
---------                     -------
 18426015                     8 files
```

### TPS Top 5 (4).zip
Downloaded: 2026-05-21 00:24 · zip size: 210 KB

```
  Length      Date    Time    Name
---------  ---------- -----   ----
    53005  05-21-2026 00:24   cloudflare-upload/advertorial.html
   111445  05-21-2026 00:24   cloudflare-upload/image1.jpg
    16896  05-21-2026 00:24   cloudflare-upload/image2.jpg
    14455  05-21-2026 00:24   cloudflare-upload/image3.jpg
    15519  05-21-2026 00:24   cloudflare-upload/image4.jpg
    15294  05-21-2026 00:24   cloudflare-upload/image5.jpg
    13708  05-21-2026 00:24   cloudflare-upload/image6.jpg
    14042  05-21-2026 00:24   cloudflare-upload/image7.jpg
---------                     -------
   254364                     8 files
```

### TPS Top 5 (5).zip
Downloaded: 2026-05-28 00:27 · zip size: 210 KB

```
  Length      Date    Time    Name
---------  ---------- -----   ----
    55098  05-28-2026 00:27   upload/advertorial.html
   111445  05-28-2026 00:27   upload/image1.jpg
    16896  05-28-2026 00:27   upload/image2.jpg
    14455  05-28-2026 00:27   upload/image3.jpg
    15519  05-28-2026 00:27   upload/image4.jpg
    15294  05-28-2026 00:27   upload/image5.jpg
    13708  05-28-2026 00:27   upload/image6.jpg
    14042  05-28-2026 00:27   upload/image7.jpg
---------                     -------
   256457                     8 files
```

### TPS Top 5 (6).zip
Downloaded: 2026-05-28 00:32 · zip size: 210 KB

```
  Length      Date    Time    Name
---------  ---------- -----   ----
    55096  05-28-2026 00:32   upload/advertorial.html
   111445  05-28-2026 00:32   upload/image1.jpg
    16896  05-28-2026 00:32   upload/image2.jpg
    14455  05-28-2026 00:32   upload/image3.jpg
    15519  05-28-2026 00:32   upload/image4.jpg
    15294  05-28-2026 00:32   upload/image5.jpg
    13708  05-28-2026 00:32   upload/image6.jpg
    14042  05-28-2026 00:32   upload/image7.jpg
---------                     -------
   256455                     8 files
```

### TPS Top 5 (7).zip
Downloaded: 2026-06-02 23:22 · zip size: 921 KB

```
  Length      Date    Time    Name
---------  ---------- -----   ----
    71504  06-02-2026 23:22   upload/advertorial.html
   132257  06-02-2026 23:22   upload/image1.jpg
    14455  06-02-2026 23:22   upload/image10.jpg
    15519  06-02-2026 23:22   upload/image11.jpg
    15294  06-02-2026 23:22   upload/image12.jpg
    13708  06-02-2026 23:22   upload/image13.jpg
    14042  06-02-2026 23:22   upload/image14.jpg
    79290  06-02-2026 23:22   upload/image2.jpg
   162896  06-02-2026 23:22   upload/image3.jpg
   104967  06-02-2026 23:22   upload/image4.jpg
    83982  06-02-2026 23:22   upload/image5.jpg
    81750  06-02-2026 23:22   upload/image6.jpg
    78236  06-02-2026 23:22   upload/image7.jpg
   111445  06-02-2026 23:22   upload/image8.jpg
    16896  06-02-2026 23:22   upload/image9.jpg
---------                     -------
   996241                     15 files
```

### TPS Top 5 (8).zip
Downloaded: 2026-06-04 02:10 · zip size: 1213 KB

```
  Length      Date    Time    Name
---------  ---------- -----   ----
    34985  06-04-2026 02:10   upload/advertorial.html
   191123  06-04-2026 02:10   upload/image1.jpg
   108914  06-04-2026 02:10   upload/image2.jpg
   157547  06-04-2026 02:10   upload/image3.jpg
   164585  06-04-2026 02:10   upload/image4.jpg
   185537  06-04-2026 02:10   upload/image5.jpg
   142442  06-04-2026 02:10   upload/image6.jpg
   146598  06-04-2026 02:10   upload/image7.jpg
   134598  06-04-2026 02:10   upload/image8.jpg
---------                     -------
  1266329                     9 files
```

### TPS Top 5 (9).zip
Downloaded: 2026-06-08 00:20 · zip size: 449 KB

```
  Length      Date    Time    Name
---------  ---------- -----   ----
    30667  06-08-2026 00:20   upload/advertorial.html
    74326  06-08-2026 00:20   upload/image1.jpg
     3967  06-08-2026 00:20   upload/image2.jpg
    77510  06-08-2026 00:20   upload/image3.jpg
    89591  06-08-2026 00:20   upload/image4.jpg
   120856  06-08-2026 00:20   upload/image5.jpg
    82592  06-08-2026 00:20   upload/image6.jpg
---------                     -------
   479509                     7 files
```

### TPS Top 5 (10).zip
Downloaded: 2026-06-16 00:05 · zip size: 476 KB

```
  Length      Date    Time    Name
---------  ---------- -----   ----
    51412  06-16-2026 00:05   upload/advertorial.html
    74326  06-16-2026 00:05   upload/image1.jpg
     3964  06-16-2026 00:05   upload/image2.jpg
   181896  06-16-2026 00:05   upload/image3.jpg
    32713  06-16-2026 00:05   upload/image4.jpg
    36885  06-16-2026 00:05   upload/image5.jpg
    43389  06-16-2026 00:05   upload/image6.jpg
    41102  06-16-2026 00:05   upload/image7.jpg
    28881  06-16-2026 00:05   upload/image8.jpg
    30644  06-16-2026 00:05   upload/image9.jpg
---------                     -------
   525212                     10 files
```

### TPS Top 5 (11).zip
Downloaded: 2026-06-16 11:47 · zip size: 476 KB

```
  Length      Date    Time    Name
---------  ---------- -----   ----
    51412  06-16-2026 11:47   upload/advertorial.html
    74326  06-16-2026 11:47   upload/image1.jpg
     3964  06-16-2026 11:47   upload/image2.jpg
   181896  06-16-2026 11:47   upload/image3.jpg
    32713  06-16-2026 11:47   upload/image4.jpg
    36885  06-16-2026 11:47   upload/image5.jpg
    43389  06-16-2026 11:47   upload/image6.jpg
    41102  06-16-2026 11:47   upload/image7.jpg
    28881  06-16-2026 11:47   upload/image8.jpg
    30644  06-16-2026 11:47   upload/image9.jpg
---------                     -------
   525212                     10 files
```

### TPS Top 5 (12).zip
Downloaded: 2026-06-17 13:00 · zip size: 1300 KB

```
  Length      Date    Time    Name
---------  ---------- -----   ----
    37550  06-17-2026 13:00   upload/advertorial.html
   205368  06-17-2026 13:00   upload/image1.jpg
   178715  06-17-2026 13:00   upload/image2.jpg
   142442  06-17-2026 13:00   upload/image3.jpg
   115891  06-17-2026 13:00   upload/image4.jpg
   192110  06-17-2026 13:00   upload/image5.jpg
   164585  06-17-2026 13:00   upload/image6.jpg
   185537  06-17-2026 13:00   upload/image7.jpg
   134598  06-17-2026 13:00   upload/image8.jpg
---------                     -------
  1356796                     9 files
```

### TPS Top 5 (13).zip
Downloaded: 2026-06-23 11:49 · zip size: 510 KB

```
  Length      Date    Time    Name
---------  ---------- -----   ----
    52348  06-23-2026 11:49   upload/advertorial.html
   109088  06-23-2026 11:49   upload/image1.jpg
     3964  06-23-2026 11:49   upload/image2.jpg
   181896  06-23-2026 11:49   upload/image3.jpg
    32713  06-23-2026 11:49   upload/image4.jpg
    36885  06-23-2026 11:49   upload/image5.jpg
    43389  06-23-2026 11:49   upload/image6.jpg
    41102  06-23-2026 11:49   upload/image7.jpg
    28881  06-23-2026 11:49   upload/image8.jpg
    30644  06-23-2026 11:49   upload/image9.jpg
---------                     -------
   560910                     10 files
```

### TPS Top 5 (14).zip
Downloaded: 2026-06-29 21:19 · zip size: 510 KB

```
  Length      Date    Time    Name
---------  ---------- -----   ----
    52444  06-29-2026 21:19   upload/advertorial.html
   109088  06-29-2026 21:19   upload/image1.jpg
     3964  06-29-2026 21:19   upload/image2.jpg
   181896  06-29-2026 21:19   upload/image3.jpg
    32713  06-29-2026 21:19   upload/image4.jpg
    36885  06-29-2026 21:19   upload/image5.jpg
    43389  06-29-2026 21:19   upload/image6.jpg
    41102  06-29-2026 21:19   upload/image7.jpg
    28881  06-29-2026 21:19   upload/image8.jpg
    30644  06-29-2026 21:19   upload/image9.jpg
---------                     -------
   561006                     10 files
```

### TPS Top 5 (15).zip
Downloaded: 2026-07-01 13:44 · zip size: 922 KB

```
  Length      Date    Time    Name
---------  ---------- -----   ----
    73636  07-01-2026 13:44   upload/advertorial.html
   132257  07-01-2026 13:44   upload/image1.jpg
    14455  07-01-2026 13:44   upload/image10.jpg
    15519  07-01-2026 13:44   upload/image11.jpg
    15294  07-01-2026 13:44   upload/image12.jpg
    13708  07-01-2026 13:44   upload/image13.jpg
    14042  07-01-2026 13:44   upload/image14.jpg
    79290  07-01-2026 13:44   upload/image2.jpg
   162896  07-01-2026 13:44   upload/image3.jpg
   104967  07-01-2026 13:44   upload/image4.jpg
    83982  07-01-2026 13:44   upload/image5.jpg
    81750  07-01-2026 13:44   upload/image6.jpg
    78236  07-01-2026 13:44   upload/image7.jpg
   111445  07-01-2026 13:44   upload/image8.jpg
    16896  07-01-2026 13:44   upload/image9.jpg
---------                     -------
   998373                     15 files
```

### TPS Top 5 (16).zip
Downloaded: 2026-07-01 19:01 · zip size: 510 KB

```
  Length      Date    Time    Name
---------  ---------- -----   ----
    52827  07-01-2026 19:01   upload/advertorial.html
   109088  07-01-2026 19:01   upload/image1.jpg
     3964  07-01-2026 19:01   upload/image2.jpg
   181896  07-01-2026 19:01   upload/image3.jpg
    32713  07-01-2026 19:01   upload/image4.jpg
    36885  07-01-2026 19:01   upload/image5.jpg
    43389  07-01-2026 19:01   upload/image6.jpg
    41102  07-01-2026 19:01   upload/image7.jpg
    28881  07-01-2026 19:01   upload/image8.jpg
    30644  07-01-2026 19:01   upload/image9.jpg
---------                     -------
   561389                     10 files
```

### TPS Top 5 (17).zip
Downloaded: 2026-07-08 14:51 · zip size: 13277 KB

```
  Length      Date    Time    Name
---------  ---------- -----   ----
    71909  07-08-2026 14:51   upload/advertorial.html
 11842778  07-08-2026 14:51   upload/hero-video.mp4
   808929  07-08-2026 14:51   upload/hero-video.webm
   132257  07-08-2026 14:51   upload/image1.jpg
    14455  07-08-2026 14:51   upload/image10.jpg
    15519  07-08-2026 14:51   upload/image11.jpg
    15294  07-08-2026 14:51   upload/image12.jpg
    13708  07-08-2026 14:51   upload/image13.jpg
    14042  07-08-2026 14:51   upload/image14.jpg
    79290  07-08-2026 14:51   upload/image2.jpg
   162896  07-08-2026 14:51   upload/image3.jpg
   104967  07-08-2026 14:51   upload/image4.jpg
    83982  07-08-2026 14:51   upload/image5.jpg
    81750  07-08-2026 14:51   upload/image6.jpg
    78236  07-08-2026 14:51   upload/image7.jpg
   111445  07-08-2026 14:51   upload/image8.jpg
    16896  07-08-2026 14:51   upload/image9.jpg
---------                     -------
 13648353                     17 files
```

### TPS Top 5 (18).zip
Downloaded: 2026-07-08 16:30 · zip size: 7766 KB

```
  Length      Date    Time    Name
---------  ---------- -----   ----
    71903  07-08-2026 16:30   upload/advertorial.html
  6717168  07-08-2026 16:30   upload/hero-video2.mp4
   321502  07-08-2026 16:30   upload/hero-video2.webm
   102546  07-08-2026 16:30   upload/image1.jpg
    14455  07-08-2026 16:30   upload/image10.jpg
    15519  07-08-2026 16:30   upload/image11.jpg
    15294  07-08-2026 16:30   upload/image12.jpg
    13708  07-08-2026 16:30   upload/image13.jpg
    14042  07-08-2026 16:30   upload/image14.jpg
    79290  07-08-2026 16:30   upload/image2.jpg
   162896  07-08-2026 16:30   upload/image3.jpg
   104967  07-08-2026 16:30   upload/image4.jpg
    83982  07-08-2026 16:30   upload/image5.jpg
    81750  07-08-2026 16:30   upload/image6.jpg
    78236  07-08-2026 16:30   upload/image7.jpg
   111445  07-08-2026 16:30   upload/image8.jpg
    16896  07-08-2026 16:30   upload/image9.jpg
---------                     -------
  8005599                     17 files
```

### TPS Top 5 (19).zip
Downloaded: 2026-07-13 17:21 · zip size: 922 KB

```
  Length      Date    Time    Name
---------  ---------- -----   ----
    73986  07-13-2026 17:21   upload/advertorial.html
   132257  07-13-2026 17:21   upload/image1.jpg
    14455  07-13-2026 17:21   upload/image10.jpg
    15519  07-13-2026 17:21   upload/image11.jpg
    15294  07-13-2026 17:21   upload/image12.jpg
    13708  07-13-2026 17:21   upload/image13.jpg
    14042  07-13-2026 17:21   upload/image14.jpg
    79290  07-13-2026 17:21   upload/image2.jpg
   162896  07-13-2026 17:21   upload/image3.jpg
   104967  07-13-2026 17:21   upload/image4.jpg
    83982  07-13-2026 17:21   upload/image5.jpg
    81750  07-13-2026 17:21   upload/image6.jpg
    78236  07-13-2026 17:21   upload/image7.jpg
   111445  07-13-2026 17:21   upload/image8.jpg
    16896  07-13-2026 17:21   upload/image9.jpg
---------                     -------
   998723                     15 files
```

### TPS Top 5 (20).zip
Downloaded: 2026-07-15 12:51 · zip size: 923 KB

```
  Length      Date    Time    Name
---------  ---------- -----   ----
    78597  07-15-2026 12:51   upload/advertorial.html
   132257  07-15-2026 12:51   upload/image1.jpg
    14455  07-15-2026 12:51   upload/image10.jpg
    15519  07-15-2026 12:51   upload/image11.jpg
    15294  07-15-2026 12:51   upload/image12.jpg
    13708  07-15-2026 12:51   upload/image13.jpg
    14042  07-15-2026 12:51   upload/image14.jpg
    79290  07-15-2026 12:51   upload/image2.jpg
   162896  07-15-2026 12:51   upload/image3.jpg
   104967  07-15-2026 12:51   upload/image4.jpg
    83982  07-15-2026 12:51   upload/image5.jpg
    81750  07-15-2026 12:51   upload/image6.jpg
    78236  07-15-2026 12:51   upload/image7.jpg
   111445  07-15-2026 12:51   upload/image8.jpg
    16896  07-15-2026 12:51   upload/image9.jpg
---------                     -------
  1003334                     15 files
```

### TPS Top 5 (21).zip
Downloaded: 2026-07-18 01:07 · zip size: 812 KB

```
  Length      Date    Time    Name
---------  ---------- -----   ----
    58137  07-18-2026 01:07   upload/advertorial.html
   109088  07-18-2026 01:07   upload/image1.jpg
    43389  07-18-2026 01:07   upload/image10.jpg
    41102  07-18-2026 01:07   upload/image11.jpg
    28881  07-18-2026 01:07   upload/image12.jpg
    30644  07-18-2026 01:07   upload/image13.jpg
     3964  07-18-2026 01:07   upload/image2.jpg
    76931  07-18-2026 01:07   upload/image3.jpg
    73072  07-18-2026 01:07   upload/image4.jpg
    76759  07-18-2026 01:07   upload/image5.jpg
    80198  07-18-2026 01:07   upload/image6.jpg
   181896  07-18-2026 01:07   upload/image7.jpg
    32713  07-18-2026 01:07   upload/image8.jpg
    36885  07-18-2026 01:07   upload/image9.jpg
---------                     -------
   873659                     14 files
```

### TPS Top 5 (22).zip
Downloaded: 2026-07-21 21:27 · zip size: 273 KB

```
  Length      Date    Time    Name
---------  ---------- -----   ----
    54033  07-21-2026 21:27   upload/advertorial.html
    80762  07-21-2026 21:27   upload/image1.jpg
     3964  07-21-2026 21:27   upload/image2.jpg
   181896  07-21-2026 21:27   upload/image3.jpg
---------                     -------
   320655                     4 files
```

## 2026-09-01 — StoryInsider (woman-narrated story re-angle of Plain control)
- Deployed: `landers-prod/hero-tps-news.americanbeautyjournal.org/StoryInsider/` (advertorial.html + image1-15.jpg)
- LIVE: https://news.americanbeautyjournal.org/StoryInsider/advertorial.html (200 verified)
- Narrator: Janet Moran, counter insider. Copy doc: offers/tps/advertorials/top5-longform-story-insider-copy.md
- Lesson: bucket folders are `<slug>-<hostname>`, served by the `landers-router` Worker; a bare-hostname folder serves nothing (first upload went there, deleted).

## 2026-09-01 — StoryInsider2 (apology headline + whiteboard hero variant of StoryInsider)
- Two swaps vs StoryInsider (diff-verified, all else byte-identical): H1 = "I Owe Every Woman I Ever Sold a $190 Wrinkle Cream an Apology"; hero image1 = whiteboard DO-NOT-BUY render (99KB), with a .photo.hero{aspect-ratio:3/2} override because the control crops heroes to 16:9 and text images cannot be cover-cropped.
- Deployed: `landers-prod/hero-tps-news.americanbeautyjournal.org/StoryInsider2/` — LIVE: https://news.americanbeautyjournal.org/StoryInsider2/advertorial.html (200 verified)
- Hero picked from 6 strategist-images rounds; all candidates in offers/tps/images/ad-storyinsider2-hero/ (gallery indexed).

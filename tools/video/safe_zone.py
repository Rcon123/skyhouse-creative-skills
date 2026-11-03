"""Meta safe zone for a 9:16 master (1080x1920). Ryan, 2026-10-22: use and save this for all future videos so nothing gets cut off.

Source (the 'One Creative for All Placements' workflow + the Ads Manager guardrail measured July 2026):
  safe area 950 x 979 px, from y = 269 down to y = 1248, centred (x = 65 to 1015);
  i.e. 14% top, 35% bottom, 6% sides. Feed crops to 4:5 and 1:1 from the centre, so the box survives every placement.
  Pull the bottom-right corner in further (the engagement rail): nothing in x > 940 when y > 1050.
Everything that must be read (title cards, captions, stamps, CTAs, labels) lives inside this box."""
W, H = 1080, 1920
X0, X1 = 65, 1015          # 950 wide, centred
Y0, Y1 = 269, 1248         # 979 tall
RAIL_X, RAIL_Y = 940, 1050 # bottom-right engagement rail (Reels icon column): keep clear below-right of this

def inside(x0, y0, x1, y1):
    """True when a box lies fully inside the safe area and clear of the rail."""
    if x0 < X0 or x1 > X1 or y0 < Y0 or y1 > Y1:
        return False
    if y1 > RAIL_Y and x1 > RAIL_X:
        return False
    return True

def problems(x0, y0, x1, y1, what="overlay"):
    out = []
    if y0 < Y0: out.append(f"{what} starts at y={y0:.0f}, above the safe top (269)")
    if y1 > Y1: out.append(f"{what} ends at y={y1:.0f}, below the safe bottom (1248): the bottom 35% is covered by the UI")
    if x0 < X0 or x1 > X1: out.append(f"{what} runs x={x0:.0f}..{x1:.0f}, outside the 950 px centre (65..1015)")
    if y1 > RAIL_Y and x1 > RAIL_X: out.append(f"{what} sits in the bottom-right engagement rail (x>940, y>1050)")
    return out

def fit_y(h, want_frac=0.58):
    """A y for an element of height h that keeps it inside the box; want_frac is the preferred top as a share of H."""
    y = int(H * want_frac)
    return max(Y0, min(y, Y1 - h))

def draw_debug(draw):
    """Draw the box on a PIL ImageDraw (for QA frames)."""
    draw.rectangle([X0, Y0, X1, Y1], outline=(0, 255, 120), width=4)
    draw.rectangle([RAIL_X, RAIL_Y, W, H], outline=(255, 80, 80), width=4)
    draw.rectangle([0, 0, W, Y0], fill=(0, 0, 0, 90)); draw.rectangle([0, Y1, W, H], fill=(0, 0, 0, 90))

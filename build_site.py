#!/usr/bin/env python3
"""
Build the public Adult Cardiac Anesthesiology lecture site (index.html)
from curriculum.json.

Workflow to publish/update:
  1. Upload a lecture to YouTube.
  2. Paste the YouTube watch URL into the matching lecture's "youtube" field
     in curriculum.json  (or just ask Claude to do it by lecture name).
  3. Run:  python3 build_site.py
  4. Commit / push (GitHub Pages) and the lecture goes live.

A lecture becomes a clickable "Watch" link as soon as it has a youtube URL.
Everything else shows a status chip and is not clickable.

Design: warm "Ghibli" storybook palette (soft sky, rolling hills, golden light)
with Vanderbilt gold accents and VUMC branding.
"""

import json, html, datetime, pathlib

HERE = pathlib.Path(__file__).parent
DATA = json.load(open(HERE / "curriculum.json", encoding="utf-8"))

SITE_TITLE   = "Adult Cardiac Anesthesiology"
SITE_TAGLINE = "A cardiothoracic anesthesia lecture library, organized by the ABA Advanced Cardiac Anesthesiology content outline."
AUTHOR       = "John Bryant, MD"
DEPT         = "Vanderbilt University Medical Center"
DIVISION     = "Division of Cardiothoracic Anesthesiology"
YOUTUBE_CHANNEL = ""   # <- paste your YouTube channel / playlist URL here when ready
CONTACT_EMAIL   = "crossclampchronicles@mail.com"

STATUS_CHIP = {
    "recorded":    ("Recorded · posting soon", "chip-soon"),
    "in_progress": ("In development",          "chip-dev"),
    "planned":     ("Coming soon",             "chip-plan"),
    "gap":         ("Coming soon",             "chip-plan"),
}

def esc(s): return html.escape(s, quote=True)

def lecture_link(slug):
    lec = DATA["lectures"][slug]
    title = esc(lec["title"])
    lecturer = lec.get("lecturer", "")
    by = f' <span class="by">{esc(lecturer)}</span>' if lecturer else ""
    yt = (lec.get("youtube") or "").strip()
    if yt:
        return (f'<li class="lec live"><a href="{esc(yt)}" target="_blank" rel="noopener">'
                f'<span class="play" aria-hidden="true">▶</span>{title}</a>{by}'
                f'<span class="chip chip-live">Watch</span></li>')
    label, cls = STATUS_CHIP.get(lec.get("status","planned"), STATUS_CHIP["planned"])
    return (f'<li class="lec"><span class="lectitle">{title}</span>{by}'
            f'<span class="chip {cls}">{label}</span></li>')

# ----- stats -----
lectures = DATA["lectures"]
n_sections   = len(DATA["sections"])
n_topics     = sum(len(s["items"]) for s in DATA["sections"])
n_recorded   = sum(1 for l in lectures.values() if l.get("status") == "recorded")
n_live       = sum(1 for l in lectures.values() if (l.get("youtube") or "").strip())

# ----- sections html -----
sections_html = []
for i, sec in enumerate(DATA["sections"]):
    items_html = []
    for it in sec["items"]:
        detail = f'<p class="detail">{esc(it["detail"])}</p>' if it.get("detail") else ""
        lecs = "".join(lecture_link(s) for s in it["lectures"])
        lecs_html = f'<ul class="lectures">{lecs}</ul>' if lecs else ""
        items_html.append(
            f'<div class="item">'
            f'<p class="item-title"><span class="code">{esc(it["code"])}</span>{esc(it["label"])}</p>'
            f'{detail}{lecs_html}</div>'
        )
    sections_html.append(
        f'<section class="aba tint-{i%6}" id="sec-{sec["letter"]}" data-letter="{sec["letter"]}">'
        f'<h2><span class="letter">{sec["letter"]}</span>{esc(sec["title"])}</h2>'
        f'<p class="section-meta">{esc(sec["meta"])}</p>'
        f'<div class="items">{"".join(items_html)}</div></section>'
    )

nav = "".join(f'<a href="#sec-{s["letter"]}">{s["letter"]}</a>' for s in DATA["sections"])

yt_btn = (f'<a class="btn btn-yt" href="{esc(YOUTUBE_CHANNEL)}" target="_blank" rel="noopener">'
          f'<span class="yt-i">▶</span> Watch on YouTube</a>' if YOUTUBE_CHANNEL else "")

today = datetime.date.today().strftime("%B %Y")
year  = datetime.date.today().year

# ----- a wall of bookshelves (deterministic, no deps) -----
# Plain spine colours + a darker set for the lettered "history" books.
_SPINE = ["#b56b5a", "#6fae9f", "#d9b53e", "#3a4a6b", "#c98a3e", "#7a9b6e", "#a85d6e", "#cfc3a0", "#8a6fae"]
_W = [9, 7, 10, 8, 6, 9, 8, 11, 7]
_T = [0, 3, 1, 4, 0, 2, 1, 0, 3]
_DARK = ["#7a3b34", "#2f4a6b", "#3d6b53", "#5e4a82", "#8a5a2a", "#4d6b75", "#7a4a52"]
# Landmark names in the history of cardiac surgery & anesthesia
# (drawn from the "Milestones in Cardiac Surgery" series + foundational era).
HISTORY = [
    # foundational era
    "GIBBON", "LILLEHEI", "BIGELOW", "KIRKLIN", "HARKEN", "HUFNAGEL",
    "BLALOCK", "TAUSSIG", "GROSS", "SOUTTAR", "CARREL", "GUTHRIE",
    # coronary & structural
    "SONES", "GRÜNTZIG", "DOTTER", "VINEBERG", "BECK", "FAVALORO",
    "JOHNSON", "LOOP",
    # valves, transplant & MCS
    "STARR", "EDWARDS", "ROSS", "SHUMWAY", "BARNARD", "DeBAKEY",
    "COOLEY", "LIOTTA", "KARP",
    # anesthesia pioneers
    "KAPLAN", "WYNANDS", "LELL", "SWAN", "GANZ",
    # ideas & milestones
    "ETHER", "C P B", "T E E", "SCA '78",
]

def _spine(x, top, base, w, fill, idx):
    tilt = f' transform="rotate(-6 {x:.1f} {base:.1f})"' if idx % 7 == 3 else ""
    return (f'<rect x="{x:.1f}" y="{top:.1f}" width="{w}" height="{base-top:.1f}" rx="1.4" '
            f'fill="{fill}" stroke="#0000001f" stroke-width="0.6"{tilt}/>')

def build_library_wall(x, y, w, h):
    parts = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="5" fill="#9c6f44" stroke="#6f4e2c" stroke-width="2.5"/>',
             f'<rect x="{x+4}" y="{y+4}" width="{w-8}" height="{h-8}" fill="#7d5631"/>']
    mid = y + h/2
    shelves = [(y + 7, mid - 3), (mid + 3, y + h - 7)]
    ti = bi = 0
    for top0, base in shelves:
        xc = x + 9
        while xc < x + w - 12:
            if bi % 2 == 0 and ti < len(HISTORY):
                bw, fill, topv = 16, _DARK[ti % len(_DARK)], top0 + 2
                parts.append(_spine(xc, topv, base, bw, fill, bi))
                cx, cy = xc + bw / 2, (topv + base) / 2
                parts.append(f'<text x="{cx:.1f}" y="{cy:.1f}" transform="rotate(-90 {cx:.1f} {cy:.1f})" '
                             f'text-anchor="middle" dominant-baseline="middle" font-family="Nunito Sans, sans-serif" '
                             f'font-size="5.4" letter-spacing="-0.2" fill="#f3ead2">{HISTORY[ti]}</text>')
                ti += 1
            else:
                bw, fill, topv = _W[bi % len(_W)], _SPINE[bi % len(_SPINE)], top0 + _T[bi % len(_T)]
                parts.append(_spine(xc, topv, base, bw, fill, bi))
            xc += bw + 1.8
            bi += 1
        parts.append(f'<rect x="{x+4}" y="{base:.1f}" width="{w-8}" height="4" fill="#9c6f44"/>')
    return "<g>" + "".join(parts) + "</g>"

BOOKS = build_library_wall(20, 262, 1160, 100)

# ----- hand-drawn hero scene (inline SVG, no dependencies) -----
SCENE = '''
<svg class="scene" viewBox="0 0 1200 460" preserveAspectRatio="xMidYMax slice" aria-hidden="true">
  <defs>
    <radialGradient id="sun" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#fff6d8"/><stop offset="55%" stop-color="#f3d98a"/>
      <stop offset="100%" stop-color="#f3d98a" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="back" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#bcd9a6"/><stop offset="100%" stop-color="#a9cf9b"/>
    </linearGradient>
    <linearGradient id="field" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#ecd591"/><stop offset="100%" stop-color="#e3c878"/>
    </linearGradient>
    <linearGradient id="front" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#7fb583"/><stop offset="100%" stop-color="#5e9d70"/>
    </linearGradient>
    <linearGradient id="scrim" x1="0" y1="0" x2="580" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#fffdf6" stop-opacity="0.92"/>
      <stop offset="0.62" stop-color="#fffdf6" stop-opacity="0.5"/>
      <stop offset="1" stop-color="#fffdf6" stop-opacity="0"/>
    </linearGradient>
  </defs>
  <!-- sun glow + disc -->
  <circle cx="985" cy="120" r="135" fill="url(#sun)"/>
  <circle cx="985" cy="120" r="60" fill="#fbeec0"/>
  <!-- birds -->
  <g stroke="#6c6357" stroke-width="2.4" fill="none" stroke-linecap="round" opacity="0.55">
    <path d="M150 95 q12 -11 24 0 q12 -11 24 0"/>
    <path d="M232 124 q9 -8 18 0 q9 -8 18 0"/>
  </g>
  <!-- drifting clouds -->
  <g class="cloud c1" fill="#ffffff" opacity="0.92">
    <ellipse cx="320" cy="120" rx="70" ry="30"/><ellipse cx="370" cy="105" rx="55" ry="34"/>
    <ellipse cx="265" cy="128" rx="48" ry="24"/>
  </g>
  <g class="cloud c2" fill="#ffffff" opacity="0.8">
    <ellipse cx="720" cy="80" rx="60" ry="26"/><ellipse cx="760" cy="68" rx="44" ry="28"/>
    <ellipse cx="678" cy="86" rx="40" ry="20"/>
  </g>
  <g class="cloud c3" fill="#ffffff" opacity="0.85">
    <ellipse cx="540" cy="170" rx="52" ry="22"/><ellipse cx="575" cy="160" rx="38" ry="24"/>
  </g>
  <!-- library wall behind the pond -->
  <!--BOOKS-->
  <!-- soft scrim keeps the heading legible over the shelves -->
  <rect x="0" y="0" width="580" height="392" fill="url(#scrim)"/>
  <!-- pond -->
  <path fill="#a9d6dd" d="M0,358 C300,350 600,360 900,355 C1030,353 1120,360 1200,354 L1200,460 L0,460 Z"/>
  <path fill="#c2e4e8" opacity="0.55" d="M0,358 C300,350 600,360 900,355 C1030,353 1120,360 1200,354 L1200,374 C900,380 300,372 0,376 Z"/>
  <g stroke="#8cc3cc" stroke-width="2" fill="none" stroke-linecap="round" opacity="0.65">
    <path d="M150,406 q18 -6 36 0"/><path d="M280,432 q22 -6 44 0"/>
    <path d="M985,402 q18 -6 36 0"/><path d="M860,434 q22 -6 44 0"/>
  </g>

  <!-- ===== the Commodore rowing his boat (TEE-probe oar) ===== -->
  <g class="boat-rock">
    <!-- boat shadow on the water -->
    <ellipse cx="646" cy="404" rx="158" ry="13" fill="#5fa0ac" opacity="0.35"/>

    <!-- hull (back) -->
    <path d="M505,346 C512,392 560,402 645,402 C730,402 778,392 785,346 C748,360 542,360 505,346 Z" fill="#a9794e" stroke="#7d5631" stroke-width="2"/>
    <ellipse cx="645" cy="346" rx="142" ry="15" fill="#8a5e38"/>

    <!-- ===== seated Commodore (upper body) ===== -->
    <g transform="translate(588,232) scale(0.92)">
      <!-- neck -->
      <rect x="56" y="56" width="13" height="34" rx="4" fill="#f0c9a8"/>
      <!-- JACKET torso -->
      <path d="M37,86 q25 -9 50 0 l6 44 q-31 12 -62 0 z" fill="#181a22"/>
      <!-- white cravat -->
      <path d="M53,80 L62,98 L71,80 q-9 -4 -18 0 z" fill="#f3efe6"/>
      <!-- hussar gold braids -->
      <g stroke="#d9b53e" stroke-width="2.4" stroke-linecap="round">
        <line x1="49" y1="94" x2="75" y2="94"/><line x1="50" y1="102" x2="74" y2="102"/>
        <line x1="51" y1="110" x2="73" y2="110"/>
      </g>
      <g fill="#e6c558">
        <circle cx="48" cy="94" r="1.9"/><circle cx="76" cy="94" r="1.9"/>
        <circle cx="49" cy="102" r="1.9"/><circle cx="75" cy="102" r="1.9"/>
        <circle cx="50" cy="110" r="1.9"/><circle cx="74" cy="110" r="1.9"/>
      </g>
      <!-- epaulettes -->
      <ellipse cx="35" cy="86" rx="9" ry="5" fill="#d9b53e"/>
      <ellipse cx="89" cy="86" rx="9" ry="5" fill="#d9b53e"/>

      <!-- rowing arms + TEE-probe oar -->
      <g class="row">
        <path d="M38,90 C55,95 76,106 92,118 l-5 9 C72,118 52,108 35,103 Z" fill="#181a22"/>
        <path d="M86,90 C90,100 96,112 99,121 l-9 3 C86,114 80,103 77,96 Z" fill="#181a22"/>
        <circle cx="90" cy="121" r="5.5" fill="#f0c9a8"/>
        <circle cx="98" cy="121" r="5" fill="#f0c9a8"/>
        <!-- TEE probe: slim grey handle body -->
        <g transform="rotate(36 95 120)">
          <ellipse cx="95" cy="114" rx="6" ry="14" fill="#d7d8d1" stroke="#a3a49b" stroke-width="0.8"/>
          <circle cx="95" cy="108" r="2.6" fill="#bdbeb6"/>
          <rect x="91.5" y="100" width="7" height="5" rx="2" fill="#cacbc3"/>
        </g>
        <!-- long flexible black cable = oar shaft, over the gunwale into the water -->
        <path d="M101,126 C140,150 205,148 250,196" fill="none" stroke="#1c1d22" stroke-width="3.8" stroke-linecap="round"/>
        <path d="M101,126 C140,150 205,148 250,196" fill="none" stroke="#41434a" stroke-width="1.3" stroke-linecap="round" opacity="0.5"/>
        <!-- transducer tip (blade) dipping in -->
        <ellipse cx="252" cy="200" rx="5" ry="8" fill="#26282d" transform="rotate(30 252 200)"/>
        <ellipse cx="250" cy="205" rx="11" ry="3.2" fill="none" stroke="#bfe2e7" stroke-width="1.6" opacity="0.85"/>
      </g>

      <!-- HEAD: strong jaw -->
      <path d="M43,44 q0 -16 19 -16 q19 0 19 16 l0 12 q0 13 -19 19 q-19 -6 -19 -19 z" fill="#f3d2b3"/>
      <path d="M43,44 q0 -17 19 -17 q19 0 19 17 q-6 -7 -19 -7 q-13 0 -19 7 z" fill="#15151a"/>
      <rect x="42" y="44" width="4" height="15" rx="2" fill="#15151a"/>
      <rect x="78" y="44" width="4" height="15" rx="2" fill="#15151a"/>
      <path d="M49,45 l8 2" stroke="#15151a" stroke-width="2" stroke-linecap="round"/>
      <path d="M75,45 l-8 2" stroke="#15151a" stroke-width="2" stroke-linecap="round"/>
      <circle cx="54" cy="50" r="2.4" fill="#2a2018"/><circle cx="70" cy="50" r="2.4" fill="#2a2018"/>
      <path d="M62,52 l-2 7 l3 1" stroke="#cda584" stroke-width="1.3" fill="none" stroke-linecap="round"/>
      <path d="M55,64 q7 5 14 -1" stroke="#9c5f44" stroke-width="2" fill="none" stroke-linecap="round"/>
      <!-- BICORNE hat with gold trim + V -->
      <path d="M29,30 C33,7 48,5 62,12 C76,5 91,7 95,30 C80,41 70,41 62,41 C54,41 44,41 29,30 Z" fill="#15151a"/>
      <path d="M31,30 C36,11 48,9 62,16 C76,9 88,11 93,30" stroke="#d9b53e" stroke-width="2.4" fill="none"/>
      <path d="M55,17 L62,33 L69,17" stroke="#e6c558" stroke-width="3.2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
    </g>

    <!-- hull front rim (over the lap) -->
    <path d="M505,346 C545,366 745,366 785,346 C748,374 542,374 505,346 Z" fill="#b9885c" stroke="#7d5631" stroke-width="1.5"/>
    <path d="M514,349 C550,366 740,366 776,349" fill="none" stroke="#caa074" stroke-width="2"/>
  </g>
</svg>
'''

SCENE = SCENE.replace("<!--BOOKS-->", BOOKS)

HTML = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(SITE_TITLE)} — Open Lecture Library</title>
<meta name="description" content="A warm, open video library of cardiac anesthesiology lectures, organized by the ABA content outline. Curated at Vanderbilt University Medical Center.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600&family=Nunito+Sans:wght@400;600;700&display=swap" rel="stylesheet">
<style>
  :root {{
    --sky-top:#cfe7ee; --sky-mid:#e6eede; --cream:#faf3e2; --paper:#fffdf6;
    --ink:#33302a; --muted:#867c6d; --rule:#ece4d3;
    --gold:#c9a227; --gold-deep:#a07f17; --gold-soft:#f2e7c2;
    --live:#3c8a5b; --live-bg:#e5f2e4;
    --soon:#5a86b0; --soon-bg:#e9f1f8;
    --dev:#b48319; --dev-bg:#faf0d6;
    --plan:#9a9082; --plan-bg:#efe9dd;
    --serif:"Fraunces", Georgia, "Iowan Old Style", serif;
    --sans:"Nunito Sans", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  }}
  *{{box-sizing:border-box;}}
  html{{scroll-behavior:smooth;}}
  body{{margin:0;color:var(--ink);font-family:var(--sans);line-height:1.6;
    background:
      radial-gradient(1200px 500px at 85% -10%, #fbf1cf 0%, rgba(251,241,207,0) 60%),
      radial-gradient(900px 500px at 0% 20%, #e7f0e0 0%, rgba(231,240,224,0) 55%),
      var(--cream);}}
  a{{color:inherit;}}
  .wrap{{max-width:1020px;margin:0 auto;background:var(--paper);
    box-shadow:0 0 60px rgba(120,100,60,.08);min-height:100vh;}}

  /* ---------- hero ---------- */
  .hero{{position:relative;overflow:hidden;
    background:linear-gradient(180deg,var(--sky-top) 0%,#dcebe0 48%,var(--sky-mid) 100%);}}
  .scene{{position:absolute;inset:0;width:100%;height:100%;display:block;}}
  .cloud{{animation:drift 90s linear infinite;}}
  .c2{{animation-duration:120s;}} .c3{{animation-duration:75s;}}
  @keyframes drift{{from{{transform:translateX(-220px);}} to{{transform:translateX(1320px);}}}}
  .hero-content{{position:relative;z-index:2;padding:56px 48px 150px;}}
  .crest{{display:inline-flex;align-items:center;gap:10px;margin-bottom:18px;}}
  .crest .anchor{{width:30px;height:30px;color:var(--gold-deep);}}
  .crest .crest-txt{{font-family:var(--sans);font-weight:700;font-size:12px;letter-spacing:1.5px;
    text-transform:uppercase;color:#6a5c3a;line-height:1.25;}}
  .crest .crest-txt small{{display:block;font-weight:600;letter-spacing:.5px;
    text-transform:none;color:#7d7058;font-size:11.5px;}}
  .hero h1{{font-family:var(--serif);font-weight:600;font-size:clamp(32px,5vw,50px);
    line-height:1.04;margin:6px 0 14px;color:#2a2722;letter-spacing:-.5px;max-width:15ch;}}
  .hero h1 .accent{{color:var(--gold-deep);}}
  .tagline{{font-size:17px;max-width:600px;color:#4f4a40;margin:0 0 22px;}}
  .byline{{font-size:14px;color:#5d5648;margin:0 0 26px;}}
  .byline strong{{font-weight:700;}}
  .btns{{display:flex;flex-wrap:wrap;gap:12px;}}
  .btn{{display:inline-flex;align-items:center;gap:7px;padding:12px 22px;border-radius:30px;
    font-size:14.5px;font-weight:700;text-decoration:none;border:1.5px solid transparent;
    box-shadow:0 4px 14px rgba(120,95,30,.14);transition:transform .15s ease;}}
  .btn:hover{{transform:translateY(-2px);}}
  .btn-primary{{background:var(--gold);color:#3a2f10;border-color:var(--gold-deep);}}
  .btn-yt{{background:#fffdf6;color:var(--gold-deep);border-color:var(--gold-soft);}}
  .btn-yt .yt-i{{color:#c0392b;}}
  .hero h1,.hero .tagline,.hero .byline,.crest .crest-txt{{text-shadow:0 1px 8px rgba(255,253,246,.85),0 0 2px rgba(255,253,246,.7);}}

  /* ---------- stats ---------- */
  .stats{{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;
    margin:-66px 36px 0;position:relative;z-index:3;}}
  .stat{{background:var(--paper);border:1px solid var(--rule);border-radius:18px;
    padding:18px 14px;text-align:center;box-shadow:0 8px 24px rgba(120,100,60,.10);}}
  .stat .n{{font-family:var(--serif);font-size:30px;font-weight:600;color:var(--gold-deep);display:block;}}
  .stat .l{{font-size:11px;text-transform:uppercase;letter-spacing:1px;color:var(--muted);}}

  .body{{padding:34px 48px 60px;}}
  .welcome{{font-family:var(--serif);font-size:18px;font-style:italic;color:#5b5446;
    border-left:3px solid var(--gold-soft);padding:2px 0 2px 18px;margin:8px 0 30px;max-width:720px;}}

  /* ---------- toolbar ---------- */
  .toolbar{{position:sticky;top:0;z-index:6;background:rgba(255,253,246,.94);
    backdrop-filter:blur(6px);display:flex;flex-wrap:wrap;gap:14px;align-items:center;
    padding:14px 0;margin-bottom:6px;border-bottom:1px solid var(--rule);}}
  .toolbar input[type=search]{{flex:1;min-width:200px;padding:11px 16px;border:1px solid var(--rule);
    border-radius:24px;font:inherit;background:#fffdf6;}}
  .toolbar input[type=search]:focus{{outline:none;border-color:var(--gold);box-shadow:0 0 0 3px var(--gold-soft);}}
  .toolbar label{{font-size:13px;color:var(--muted);cursor:pointer;user-select:none;display:flex;align-items:center;gap:7px;}}
  .secnav{{display:flex;flex-wrap:wrap;gap:6px;margin:16px 0 30px;}}
  .secnav a{{width:34px;height:34px;display:flex;align-items:center;justify-content:center;
    border:1px solid var(--rule);border-radius:50%;text-decoration:none;font-weight:700;font-size:13px;
    color:var(--gold-deep);background:#fffdf6;transition:.15s;}}
  .secnav a:hover{{background:var(--gold);color:#fff;border-color:var(--gold);transform:translateY(-2px);}}

  /* ---------- sections ---------- */
  section.aba{{border-radius:20px;padding:24px 26px;margin-bottom:22px;scroll-margin-top:74px;
    border:1px solid var(--rule);}}
  .tint-0{{background:#fbf7ec;}} .tint-1{{background:#f3f6ec;}} .tint-2{{background:#eef5f3;}}
  .tint-3{{background:#f8f2ec;}} .tint-4{{background:#f1f4f0;}} .tint-5{{background:#f7f4ea;}}
  section.aba>h2{{font-family:var(--serif);font-weight:600;font-size:23px;margin:0 0 4px;
    display:flex;align-items:center;gap:14px;color:#2f2b24;}}
  section.aba>h2 .letter{{flex:none;width:40px;height:40px;border-radius:50%;background:var(--gold);
    color:#fff;display:flex;align-items:center;justify-content:center;font-size:20px;
    box-shadow:0 3px 8px rgba(160,127,23,.3);}}
  .section-meta{{color:var(--muted);font-size:13.5px;font-style:italic;margin:0 0 16px 54px;}}
  .items{{display:block;}}
  .item{{background:rgba(255,255,255,.6);border-radius:12px;padding:12px 16px;margin-bottom:9px;
    border:1px solid rgba(236,228,211,.7);}}
  .item-title{{font-weight:700;font-size:15px;margin:0;color:#3a352c;}}
  .item-title .code{{color:var(--gold-deep);font-weight:700;margin-right:9px;
    font-family:ui-monospace,Menlo,monospace;font-size:12px;background:var(--gold-soft);
    padding:1px 7px;border-radius:6px;}}
  .detail{{color:#6f685b;font-size:13px;font-style:italic;margin:4px 0 0;}}
  .lectures{{list-style:none;margin:10px 0 0;padding:0;}}
  .lec{{display:flex;align-items:center;gap:9px;flex-wrap:wrap;padding:5px 0;font-size:14.5px;}}
  .lec a{{text-decoration:none;font-weight:700;color:var(--gold-deep);
    border-bottom:1.5px solid transparent;}}
  .lec a:hover{{border-bottom-color:var(--gold);}}
  .lec .play{{color:var(--live);margin-right:6px;font-size:11px;}}
  .lec .by{{color:var(--muted);font-size:12.5px;}}
  .lec .by:before{{content:"· ";}}
  .lectitle{{color:#4a443a;}}
  .chip{{font-size:10px;text-transform:uppercase;letter-spacing:.7px;font-weight:700;
    padding:3px 10px;border-radius:20px;white-space:nowrap;}}
  .chip-live{{color:var(--live);background:var(--live-bg);}}
  .chip-soon{{color:var(--soon);background:var(--soon-bg);}}
  .chip-dev{{color:var(--dev);background:var(--dev-bg);}}
  .chip-plan{{color:var(--plan);background:var(--plan-bg);}}

  body.live-only .lec:not(.live){{display:none;}}
  body.live-only .item:not(:has(.lec.live)){{display:none;}}
  body.live-only section.aba:not(:has(.lec.live)){{display:none;}}

  /* ---------- footer ---------- */
  footer{{position:relative;margin-top:10px;padding:70px 48px 46px;color:#5d5648;font-size:13px;
    background:linear-gradient(180deg,#fffdf6 0%,#eef3e8 100%);}}
  footer .hills{{position:absolute;top:0;left:0;width:100%;height:60px;display:block;}}
  footer a{{color:var(--gold-deep);font-weight:700;}}
  footer .disclaimer{{margin-top:12px;font-style:italic;color:#7d7568;font-size:12px;}}

  /* the Commodore in his boat */
  .boat-rock{{animation:rock 6s ease-in-out infinite;transform-box:fill-box;transform-origin:center bottom;}}
  @keyframes rock{{0%,100%{{transform:translateY(0) rotate(-1.4deg);}}50%{{transform:translateY(-3px) rotate(1.4deg);}}}}
  .row{{animation:row 3.2s ease-in-out infinite;transform-box:fill-box;transform-origin:left top;}}
  @keyframes row{{0%,100%{{transform:rotate(-3deg);}}50%{{transform:rotate(3deg);}}}}

  @media (prefers-reduced-motion: reduce){{ .cloud,.boat-rock,.row{{animation:none;}} }}
  @media (max-width:680px){{
    .hero-content{{padding:40px 22px 130px;}}
    .stats{{grid-template-columns:repeat(2,1fr);margin:-66px 18px 0;}}
    .body{{padding:26px 18px 50px;}} footer{{padding:60px 20px 40px;}}
    section.aba{{padding:18px 16px;}} .section-meta{{margin-left:0;}}
  }}
</style>
</head>
<body>
<div class="wrap">

  <header class="hero">
    {SCENE}
    <div class="hero-content">
      <div class="crest">
        <svg class="anchor" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="12" cy="4" r="2"/><line x1="12" y1="6" x2="12" y2="22"/>
          <line x1="7" y1="10" x2="17" y2="10"/>
          <path d="M4 14 a8 8 0 0 0 16 0"/>
        </svg>
        <span class="crest-txt">{esc(DEPT)}<small>{esc(DIVISION)}</small></span>
      </div>
      <h1>Adult Cardiac<br><span class="accent">Anesthesiology</span></h1>
      <p class="tagline">{esc(SITE_TAGLINE)}</p>
      <p class="byline">Curated by <strong>{esc(AUTHOR)}</strong></p>
      <div class="btns">
        <a class="btn btn-primary" href="#sec-A">Browse the curriculum</a>
        {yt_btn}
      </div>
    </div>
  </header>

  <div class="stats">
    <div class="stat"><span class="n">{n_sections}</span><span class="l">ABA Sections</span></div>
    <div class="stat"><span class="n">{n_topics}</span><span class="l">Outline Topics</span></div>
    <div class="stat"><span class="n">{n_recorded}</span><span class="l">Lectures Recorded</span></div>
    <div class="stat"><span class="n" id="stat-live">{n_live}</span><span class="l">Now Streaming</span></div>
  </div>

  <div class="body">
    <p class="welcome">Welcome aboard. Browse the curriculum below — available lectures are linked, and the library grows as new talks are recorded.</p>

    <div class="toolbar">
      <input type="search" id="search" placeholder="Search topics and lectures…" aria-label="Search">
      <label><input type="checkbox" id="liveOnly"> Show available lectures only</label>
    </div>
    <nav class="secnav" aria-label="Jump to section">{nav}</nav>

    {"".join(sections_html)}
  </div>

  <footer>
    <svg class="hills" viewBox="0 0 1200 60" preserveAspectRatio="none" aria-hidden="true">
      <path d="M0,38 C200,18 420,30 640,24 C880,17 1020,38 1200,28 L1200,0 L0,0 Z" fill="#fffdf6"/>
    </svg>
    <div>Organized around the ABA Advanced Cardiac Anesthesiology (ACA) content outline (November 2024).
    New lectures are added as they're recorded. Questions or corrections are always welcome:
    <a href="mailto:{esc(CONTACT_EMAIL)}">{esc(CONTACT_EMAIL)}</a>.</div>
    <div class="disclaimer">For educational purposes only; not medical advice. Views are the author's own and do not
    represent {esc(DEPT)} or any professional society. &copy; {year} {esc(AUTHOR)}. Updated {today}.</div>
  </footer>

</div>

<script>
(function(){{
  var items = Array.from(document.querySelectorAll('.item'));
  var sections = Array.from(document.querySelectorAll('section.aba'));
  var search = document.getElementById('search');
  search.addEventListener('input', function(){{
    var q = search.value.toLowerCase().trim();
    items.forEach(function(it){{
      it.style.display = (!q || it.textContent.toLowerCase().includes(q)) ? '' : 'none';
    }});
    sections.forEach(function(s){{
      var any = Array.from(s.querySelectorAll('.item')).some(function(i){{return i.style.display!=='none';}});
      s.style.display = any ? '' : 'none';
    }});
  }});
  document.getElementById('liveOnly').addEventListener('change', function(e){{
    document.body.classList.toggle('live-only', e.target.checked);
  }});
}})();
</script>
</body>
</html>
"""

out = HERE / "index.html"
out.write_text(HTML, encoding="utf-8")
print("Wrote", out, f"({len(HTML)} bytes)")
print(f"sections={n_sections} topics={n_topics} recorded={n_recorded} streaming={n_live}")

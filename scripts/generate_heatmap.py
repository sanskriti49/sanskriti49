#!/usr/bin/env python3
"""Generate the animated profile contribution HUD from GitHub's contribution API."""

from __future__ import annotations

import html
import json
import os
import re
import sys
import urllib.request
from datetime import date, datetime
from pathlib import Path


QUERY = """
query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks {
          contributionDays { date contributionCount contributionLevel }
        }
      }
    }
  }
}
"""

# Intense retro-arcade green color tones for active cells
COLORS = {
    "NONE": "#0F172A",
    "FIRST_QUARTILE": "#9be9a8",
    "SECOND_QUARTILE": "#40c463",
    "THIRD_QUARTILE": "#30a14e",
    "FOURTH_QUARTILE": "#216e39",
}


def fetch_calendar(login: str, token: str) -> dict:
    payload = json.dumps({"query": QUERY, "variables": {"login": login}}).encode()
    request = urllib.request.Request(
        "https://api.github.com/graphql",
        data=payload,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": "profile-heatmap-generator",
        },
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        result = json.load(response)
    if result.get("errors") or not result.get("data", {}).get("user"):
        raise RuntimeError(json.dumps(result.get("errors", result)))
    return result["data"]["user"]["contributionsCollection"]["contributionCalendar"]


def cell_markup(weeks: list[dict]) -> tuple[str, int]:
    cells: list[str] = []
    peak = 0
    for column, week in enumerate(weeks):
        for row, day in enumerate(week["contributionDays"]):
            count = int(day["contributionCount"])
            peak = max(peak, count)
            x = 140 + column * 18
            y = 88 + row * 18
            color = COLORS[day["contributionLevel"]]
            if count > 0:
                stroke = '#34D399'
                stroke_width = '0.35'
            else:
                stroke = '#1E293B'
                stroke_width = '0.75'
            label = f"{count} contribution{'s' if count != 1 else ''} on {day['date']}"
            cells.append(
                f'<rect x="{x}" y="{y}" width="14" height="14" rx="2.5" '
                f'fill="{color}" stroke="{stroke}" stroke-width="{stroke_width}">'
                f'<title>{html.escape(label)}</title></rect>'
            )
    return "\n  ".join(cells), peak


def month_labels(weeks: list[dict]) -> str:
    labels = []
    seen: set[str] = set()
    for column, week in enumerate(weeks):
        first = week["contributionDays"][0]["date"]
        month = datetime.strptime(first, "%Y-%m-%d").strftime("%b").upper()
        if month not in seen:
            labels.append(f'<text x="{140 + column * 18}" y="74" class="axis-label">{month}</text>')
            seen.add(month)
    return "\n  ".join(labels)


def update_readme_cache_buster(path: Path, version: str) -> None:
    if not path.exists():
        return
    content = path.read_text(encoding="utf-8")
    marker = "./assets/contribution-heatmap.svg"
    content = re.sub(r"\./assets/contribution-heatmap\.svg(\?v=[^\" )]+)?", f"{marker}?v={version}", content)
    path.write_text(content, encoding="utf-8")


def render(calendar: dict, login: str) -> str:
    weeks = calendar["weeks"][-53:]
    cells, peak = cell_markup(weeks)
    total = calendar["totalContributions"]
    score_display = f"{total:,} PTS"

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1180" height="340" viewBox="0 0 1180 340" role="img" aria-labelledby="title desc">
<title id="title">{html.escape(login)} contribution heatmap</title>
<desc id="desc">Retro arcade defense grid contribution calendar with starfighter patrol kinematics.</desc>
<defs>
  <radialGradient id="bgGlow" cx="30%" cy="20%" r="80%">
    <stop offset="0%" stop-color="#080C16"/>
    <stop offset="100%" stop-color="#03060F"/>
  </radialGradient>

  <linearGradient id="borderGrad" x1="0%" y1="0%" x2="100%" y2="100%">
    <stop offset="0%" stop-color="#22C55E"/>
    <stop offset="50%" stop-color="#10B981"/>
    <stop offset="100%" stop-color="#38BDF8"/>
  </linearGradient>

  <linearGradient id="plasmaFlame" x1="0%" y1="0%" x2="0%" y2="100%">
    <stop offset="0%" stop-color="#38BDF8"/>
    <stop offset="40%" stop-color="#818CF8"/>
    <stop offset="80%" stop-color="#F59E0B"/>
    <stop offset="100%" stop-color="#EF4444" stop-opacity="0"/>
  </linearGradient>

  <radialGradient id="ionGlow" cx="50%" cy="50%" r="50%">
    <stop offset="0%" stop-color="#38BDF8" stop-opacity="0.8"/>
    <stop offset="100%" stop-color="#38BDF8" stop-opacity="0"/>
  </radialGradient>

  <pattern id="scanlines" width="4" height="4" patternUnits="userSpaceOnUse">
    <rect width="4" height="1" fill="#7DD3FC" opacity="0.035"/>
  </pattern>

  <style>
    .hud-label-gold {{ font-family: 'Courier New', Consolas, monospace; font-size: 13px; fill: #FACC15; font-weight: bold; letter-spacing: 0.5px; }}
    .hud-val-gold   {{ font-family: 'Courier New', Consolas, monospace; font-size: 13px; fill: #FEF08A; font-weight: bold; }}
    .hud-label-cyan {{ font-family: 'Courier New', Consolas, monospace; font-size: 12px; fill: #38BDF8; font-weight: bold; letter-spacing: 0.5px; }}
    .hud-val-cyan   {{ font-family: 'Courier New', Consolas, monospace; font-size: 12px; fill: #E0F2FE; font-weight: bold; }}
    .hud-label-rose {{ font-family: 'Courier New', Consolas, monospace; font-size: 12px; fill: #FB7185; font-weight: bold; letter-spacing: 0.5px; }}
    .hud-val-rose   {{ font-family: 'Courier New', Consolas, monospace; font-size: 12px; fill: #FECDD3; font-weight: bold; }}
    .axis-label     {{ font-family: 'Courier New', Consolas, monospace; font-size: 10px; fill: #64748B; font-weight: bold; }}
    .legend-text    {{ font-family: 'Courier New', Consolas, monospace; font-size: 9px; fill: #64748B; font-weight: bold; letter-spacing: 0.5px; }}
    .hud-meta       {{ font-family: 'Courier New', Consolas, monospace; font-size: 10px; fill: #475569; letter-spacing: 1px; font-weight: bold; }}
    text {{ white-space: pre; }}
    @keyframes scan {{ from {{ transform: translateY(-190px); }} to {{ transform: translateY(210px); }} }}
  </style>
</defs>

<!-- Retro Arcade Cosmic Backdrop -->
<rect width="1180" height="340" rx="16" fill="url(#bgGlow)"/>
<rect width="1180" height="340" rx="16" fill="url(#scanlines)"/>
<rect x="1" y="1" width="1178" height="338" rx="16" fill="none" stroke="url(#borderGrad)" stroke-width="1.5"/>
<rect x="6" y="6" width="1168" height="328" rx="12" fill="none" stroke="#22C55E" stroke-width="0.5" opacity="0.25"/>

<!-- Retro Arcade Top HUD -->
<g id="arcade-hud">
  <text x="24" y="32"><tspan class="hud-label-gold">SCORE: </tspan><tspan class="hud-val-gold">{score_display}</tspan></text>
  <text x="320" y="32"><tspan class="hud-label-cyan">RANK: </tspan><tspan class="hud-val-cyan">LVL 42 &#183; FULL-STACK ARCHITECT</tspan></text>
  <text x="680" y="32"><tspan class="hud-label-rose">COMBO: </tspan><tspan class="hud-val-rose">x14 SHIPPER</tspan></text>
  <text x="930" y="32" class="hud-label-cyan">SHIELDS: 100%</text>
  <g transform="translate(1045, 22)">
    <g id="shield-segments">
      <rect x="0" y="0" width="7.5" height="12" rx="1.5" fill="#22D3EE" opacity="0.95" stroke="#0284C7" stroke-width="0.5"/>
      <rect x="10" y="0" width="7.5" height="12" rx="1.5" fill="#22D3EE" opacity="0.95" stroke="#0284C7" stroke-width="0.5"/>
      <rect x="20" y="0" width="7.5" height="12" rx="1.5" fill="#22D3EE" opacity="0.95" stroke="#0284C7" stroke-width="0.5"/>
      <rect x="30" y="0" width="7.5" height="12" rx="1.5" fill="#22D3EE" opacity="0.95" stroke="#0284C7" stroke-width="0.5"/>
      <rect x="40" y="0" width="7.5" height="12" rx="1.5" fill="#22D3EE" opacity="0.95" stroke="#0284C7" stroke-width="0.5"/>
      <rect x="50" y="0" width="7.5" height="12" rx="1.5" fill="#22D3EE" opacity="0.95" stroke="#0284C7" stroke-width="0.5"/>
      <rect x="60" y="0" width="7.5" height="12" rx="1.5" fill="#22D3EE" opacity="0.95" stroke="#0284C7" stroke-width="0.5"/>
      <rect x="70" y="0" width="7.5" height="12" rx="1.5" fill="#22D3EE" opacity="0.95" stroke="#0284C7" stroke-width="0.5"/>
      <rect x="80" y="0" width="7.5" height="12" rx="1.5" fill="#22D3EE" opacity="0.95" stroke="#0284C7" stroke-width="0.5"/>
      <rect x="90" y="0" width="7.5" height="12" rx="1.5" fill="#22D3EE" opacity="0.95" stroke="#0284C7" stroke-width="0.5"/>
    </g>
  </g>
  <line x1="20" y1="46" x2="1160" y2="46" stroke="#1E293B" stroke-width="1"/>
  <line x1="20" y1="46" x2="160" y2="46" stroke="#FACC15" stroke-width="1" opacity="0.8"/>
  <line x1="1020" y1="46" x2="1160" y2="46" stroke="#22D3EE" stroke-width="1" opacity="0.8"/>
</g>

<!-- Crosshairs & Cosmic Starfield -->
<path d="M18 60 H26 M22 56 V64" stroke="#22D3EE" stroke-width="1" opacity="0.4"/>
<path d="M1154 60 H1162 M1158 56 V64" stroke="#22D3EE" stroke-width="1" opacity="0.4"/>
<path d="M18 318 H26 M22 314 V322" stroke="#22D3EE" stroke-width="1" opacity="0.4"/>
<path d="M1154 318 H1162 M1158 314 V322" stroke="#22D3EE" stroke-width="1" opacity="0.4"/>
<circle cx="35" cy="110" r="1.1" fill="#7DD3FC"><animate attributeName="opacity" values="0.15;0.9;0.15" dur="2.2s" repeatCount="indefinite"/></circle>
<circle cx="45" cy="190" r="1.1" fill="#7DD3FC"><animate attributeName="opacity" values="0.15;0.9;0.15" dur="3.1s" repeatCount="indefinite"/></circle>
<circle cx="75" cy="140" r="1.1" fill="#7DD3FC"><animate attributeName="opacity" values="0.15;0.9;0.15" dur="1.8s" repeatCount="indefinite"/></circle>
<circle cx="95" cy="230" r="1.1" fill="#7DD3FC"><animate attributeName="opacity" values="0.15;0.9;0.15" dur="2.7s" repeatCount="indefinite"/></circle>
<circle cx="1090" cy="110" r="1.1" fill="#7DD3FC"><animate attributeName="opacity" values="0.15;0.9;0.15" dur="2.5s" repeatCount="indefinite"/></circle>
<circle cx="1120" cy="180" r="1.1" fill="#7DD3FC"><animate attributeName="opacity" values="0.15;0.9;0.15" dur="1.9s" repeatCount="indefinite"/></circle>
<circle cx="1145" cy="130" r="1.1" fill="#7DD3FC"><animate attributeName="opacity" values="0.15;0.9;0.15" dur="3.4s" repeatCount="indefinite"/></circle>
<circle cx="1105" cy="220" r="1.1" fill="#7DD3FC"><animate attributeName="opacity" values="0.15;0.9;0.15" dur="2.1s" repeatCount="indefinite"/></circle>

<!-- Month and Day Grid Axes -->
<g id="axes">
  {month_labels(weeks)}
  <text x="128" y="116.5" class="axis-label" text-anchor="end">MON</text>
  <text x="128" y="152.5" class="axis-label" text-anchor="end">WED</text>
  <text x="128" y="188.5" class="axis-label" text-anchor="end">FRI</text>
</g>

<!-- Heatmap Contribution Power-Core Grid -->
<g id="grid">
  {cells}
</g>

<!-- Footer Legend and Sector Title -->
<g transform="translate(140, 320)">
  <text x="0" y="8" class="legend-text">POWER NODES: LOW</text>
  <rect x="115" y="0" width="10" height="10" rx="2" fill="#0F172A" stroke="#1E293B" stroke-width="0.75"/>
  <rect x="129" y="0" width="10" height="10" rx="2" fill="#9be9a8" stroke="#34D399" stroke-width="0.35"/>
  <rect x="143" y="0" width="10" height="10" rx="2" fill="#40c463" stroke="#34D399" stroke-width="0.35"/>
  <rect x="157" y="0" width="10" height="10" rx="2" fill="#30a14e" stroke="#34D399" stroke-width="0.35"/>
  <rect x="171" y="0" width="10" height="10" rx="2" fill="#216e39" stroke="#34D399" stroke-width="0.35"/>
  <text x="189" y="8" class="legend-text">OVERDRIVE</text>
</g>

<text x="1040" y="328" class="hud-meta" text-anchor="end">[ARCADE DEFENSE GRID // SECTOR: SANSKRITI-FORGE]</text>

<!-- Dual-Hull Starfighter Jet & Forward Boresight Sighting Laser -->
<g id="starfighter">
  <!-- Forward Boresight Sighting Laser Guide -->
  <g id="boresight-reticle">
    <line x1="0" y1="-8" x2="0" y2="-180" stroke="#22D3EE" stroke-width="1.2" stroke-dasharray="4 3" opacity="0.6" class="sighting-laser"/>
    <circle cx="0" cy="-60" r="16" fill="none" stroke="#22D3EE" stroke-width="1.4" opacity="0.75"/>
    <circle cx="0" cy="-60" r="24" fill="none" stroke="#38BDF8" stroke-width="1" stroke-dasharray="6 3" opacity="0.5"/>
    <line x1="0" y1="-74" x2="0" y2="-66" stroke="#22D3EE" stroke-width="1.5"/>
    <line x1="0" y1="-54" x2="0" y2="-46" stroke="#22D3EE" stroke-width="1.5"/>
    <line x1="-14" y1="-60" x2="-6" y2="-60" stroke="#22D3EE" stroke-width="1.5"/>
    <line x1="6" y1="-60" x2="14" y2="-60" stroke="#22D3EE" stroke-width="1.5"/>
    <circle cx="0" cy="-60" r="2" fill="#FACC15">
      <animate attributeName="opacity" values="1;0.3;1" dur="0.6s" repeatCount="indefinite"/>
    </circle>
  </g>

  <!-- Dual-Hull Arcade Starfighter Chassis -->
  <g transform="translate(0,0)">
    <ellipse cx="0" cy="18" rx="14" ry="3" fill="url(#ionGlow)" opacity="0.7">
      <animate attributeName="rx" values="12;18;13;17" dur="0.2s" repeatCount="indefinite"/>
      <animate attributeName="opacity" values="0.5;0.85;0.4;0.9" dur="0.2s" repeatCount="indefinite"/>
    </ellipse>

    <!-- Twin Wingtip Plasma Railgun Cannons -->
    <rect x="-21" y="-8" width="2.5" height="18" rx="1" fill="#7DD3FC"/>
    <rect x="18.5" y="-8" width="2.5" height="18" rx="1" fill="#7DD3FC"/>
    <circle cx="-19.75" cy="-8" r="1.8" fill="#22D3EE">
      <animate attributeName="opacity" values="0.6;1;0.6" dur="0.6s" repeatCount="indefinite"/>
    </circle>
    <circle cx="19.75" cy="-8" r="1.8" fill="#22D3EE">
      <animate attributeName="opacity" values="0.6;1;0.6" dur="0.6s" repeatCount="indefinite"/>
    </circle>

    <!-- Port & Starboard Twin Fuselage Pods -->
    <polygon points="-14,-16 -7,-16 -5,9 -16,9" fill="#38BDF8" stroke="#0284C7" stroke-width="1.2"/>
    <polygon points="7,-16 14,-16 16,9 5,9" fill="#38BDF8" stroke="#0284C7" stroke-width="1.2"/>

    <!-- Center Deck Armor & Delta Wing Bridge -->
    <polygon points="-7,-7 7,-7 18,9 5,6 -5,6 -18,9" fill="#0284C7"/>
    <polygon points="0,-12 6,4 0,1 -6,4" fill="#0F172A"/>

    <!-- Crystalline Pilot Canopy -->
    <ellipse cx="0" cy="-3" rx="3.2" ry="5.8" fill="#E0F2FE" opacity="0.95"/>
    <ellipse cx="0" cy="-4.5" rx="1.5" ry="2.6" fill="#FFFFFF"/>

    <!-- Twin High-Frequency Plasma Thruster Flames -->
    <g id="twin-thrusters">
      <polygon points="-13,9 -8,9 -10.5,26" fill="url(#plasmaFlame)">
        <animate attributeName="opacity" values="0.75;1;0.6;0.95;0.7;1" dur="0.16s" repeatCount="indefinite"/>
      </polygon>
      <polygon points="-12,9 -9,9 -10.5,15" fill="#FFFFFF">
        <animate attributeName="opacity" values="0.8;1;0.7;1" dur="0.16s" repeatCount="indefinite"/>
      </polygon>
      <polygon points="8,9 13,9 10.5,26" fill="url(#plasmaFlame)">
        <animate attributeName="opacity" values="0.75;1;0.6;0.95;0.7;1" dur="0.16s" repeatCount="indefinite"/>
      </polygon>
      <polygon points="9,9 12,9 10.5,15" fill="#FFFFFF">
        <animate attributeName="opacity" values="0.8;1;0.7;1" dur="0.16s" repeatCount="indefinite"/>
      </polygon>
    </g>
  </g>

  <!-- Smooth Spline Horizontal Patrol Kinematics -->
  <animateTransform attributeName="transform" attributeType="XML" type="translate"
    dur="18s" repeatCount="indefinite" calcMode="spline"
    keyTimes="0; 0.5; 1"
    keySplines="0.45 0 0.55 1; 0.45 0 0.55 1"
    values="147,270; 1065,270; 147,270"/>
</g>
</svg>"""


def main() -> None:
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    login = os.environ.get("GITHUB_USERNAME", "sanskriti49")
    output = Path(os.environ.get("HEATMAP_OUTPUT", "assets/contribution-heatmap.svg"))
    output.parent.mkdir(parents=True, exist_ok=True)
    if token:
        calendar = fetch_calendar(login, token)
        output.write_text(render(calendar, login), encoding="utf-8")
    update_readme_cache_buster(Path("README.md"), date.today().strftime("%Y%m%d"))


if __name__ == "__main__":
    main()

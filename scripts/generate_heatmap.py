#!/usr/bin/env python3
"""Generate the animated profile contribution HUD from GitHub's contribution API."""

from __future__ import annotations

import html
import json
import os
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

COLORS = {
    "NONE": "#0F172A",
    "FIRST_QUARTILE": "#166534",
    "SECOND_QUARTILE": "#22C55E",
    "THIRD_QUARTILE": "#4ADE80",
    "FOURTH_QUARTILE": "#A7F3D0",
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


def cell_markup(weeks: list[dict]) -> tuple[str, int, tuple[int, int]]:
    cells: list[str] = []
    peak = 0
    last_point = (1060, 196)
    for column, week in enumerate(weeks):
        for row, day in enumerate(week["contributionDays"]):
            count = int(day["contributionCount"])
            peak = max(peak, count)
            x = 140 + column * 18
            y = 88 + row * 18
            if count:
                last_point = (x + 7, y + 7)
            label = f"{count} contribution{'s' if count != 1 else ''} on {day['date']}"
            cells.append(
                f'<rect x="{x}" y="{y}" width="14" height="14" rx="2.5" '
                f'fill="{COLORS[day["contributionLevel"]]}" stroke="#1E293B" '
                f'stroke-width="0.75"><title>{html.escape(label)}</title></rect>'
            )
    return "\n  ".join(cells), peak, last_point


def month_labels(weeks: list[dict]) -> str:
    labels = []
    seen: set[str] = set()
    for column, week in enumerate(weeks):
        first = week["contributionDays"][0]["date"]
        month = datetime.strptime(first, "%Y-%m-%d").strftime("%b").upper()
        key = f"{month}-{column}"
        if month not in seen:
            labels.append(f'<text x="{140 + column * 18}" y="74" class="axis-label">{month}</text>')
            seen.add(month)
    return "\n  ".join(labels)


def update_readme_cache_buster(path: Path, version: str) -> None:
    if not path.exists():
        return
    content = path.read_text(encoding="utf-8")
    marker = "./assets/contribution-heatmap.svg"
    content = content.replace(marker, f"{marker}?v={version}")
    import re
    content = re.sub(r"\./assets/contribution-heatmap\.svg\?v=[^\" )]+", f"{marker}?v={version}", content)
    path.write_text(content, encoding="utf-8")


def render(calendar: dict, login: str) -> str:
    weeks = calendar["weeks"][-53:]
    cells, peak, last_point = cell_markup(weeks)
    total = calendar["totalContributions"]
    generated = date.today().isoformat()
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1180" height="340" viewBox="0 0 1180 340" role="img" aria-labelledby="title desc">
<title id="title">{html.escape(login)} contribution heatmap</title>
<desc id="desc">A dynamic arcade-style contribution calendar updated from GitHub data.</desc>
<defs>
  <radialGradient id="bg" cx="30%" cy="20%" r="80%"><stop stop-color="#080C16"/><stop offset="100%" stop-color="#03060F"/></radialGradient>
  <linearGradient id="border" x1="0%" y1="0%" x2="100%" y2="100%"><stop stop-color="#38BDF8"/><stop offset="50%" stop-color="#8B5CF6"/><stop offset="100%" stop-color="#22D3EE"/></linearGradient>
  <linearGradient id="scan" x1="0%" y1="0%" x2="0%" y2="100%"><stop stop-color="#38BDF8" stop-opacity="0"/><stop offset="50%" stop-color="#A78BFA" stop-opacity=".55"/><stop offset="100%" stop-color="#38BDF8" stop-opacity="0"/></linearGradient>
  <pattern id="lines" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="1" fill="#7DD3FC" opacity=".035"/></pattern>
  <filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="3" result="blur"/><feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  <style>
    .hud {{ font-family: 'Courier New', Consolas, monospace; font-size: 13px; font-weight: bold; letter-spacing: .5px; }}
    .gold {{ fill: #FACC15; }} .cyan {{ fill: #38BDF8; }} .rose {{ fill: #FB7185; }}
    .axis-label {{ font-family: 'Courier New', Consolas, monospace; font-size: 10px; fill: #64748B; font-weight: bold; }}
    .meta {{ font-family: 'Courier New', Consolas, monospace; font-size: 10px; fill: #475569; letter-spacing: 1px; font-weight: bold; }}
    .cell {{ animation: pulse 3.5s ease-in-out infinite; }}
    .scan {{ animation: scan 5s linear infinite; }}
    @keyframes pulse {{ 0%, 100% {{ opacity: .86; }} 50% {{ opacity: 1; }} }}
    @keyframes scan {{ from {{ transform: translateY(-190px); }} to {{ transform: translateY(210px); }} }}
  </style>
</defs>
<rect width="1180" height="340" rx="16" fill="url(#bg)"/><rect width="1180" height="340" rx="16" fill="url(#lines)"/>
<rect x="1" y="1" width="1178" height="338" rx="16" fill="none" stroke="url(#border)" stroke-width="1.5"/>
<g class="hud"><text x="24" y="32" class="gold">SCORE: <tspan fill="#FEF08A">{total:,} PTS</tspan></text>
<text x="320" y="32" class="cyan">RANK: <tspan fill="#E0F2FE">LVL {min(99, max(1, total // 100))} // FULL-STACK BUILDER</tspan></text>
<text x="680" y="32" class="rose">PEAK: <tspan fill="#FECDD3">{peak} CONTRIBUTIONS/DAY</tspan></text>
<text x="930" y="32" class="cyan">SYNC: <tspan fill="#E0F2FE">{generated}</tspan></text></g>
<line x1="20" y1="46" x2="1160" y2="46" stroke="#1E293B"/><line x1="20" y1="46" x2="160" y2="46" stroke="#FACC15"/>
<path d="M18 60h8M22 56v8M1154 60h8M1158 56v8M18 318h8M22 314v8M1154 318h8M1158 314v8" stroke="#22D3EE" opacity=".5"/>
<g>{month_labels(weeks)}</g>
<text x="128" y="116.5" class="axis-label" text-anchor="end">MON</text><text x="128" y="152.5" class="axis-label" text-anchor="end">WED</text><text x="128" y="188.5" class="axis-label" text-anchor="end">FRI</text>
<g class="cell">{cells}</g>
<rect class="scan" x="138" y="84" width="936" height="3" fill="url(#scan)" opacity=".6"/>
<g transform="translate({last_point[0]} {last_point[1]})" filter="url(#glow)">
  <circle r="13" fill="none" stroke="#38BDF8" opacity=".75"><animate attributeName="r" values="8;20;8" dur="2.4s" repeatCount="indefinite"/><animate attributeName="opacity" values=".9;0;.9" dur="2.4s" repeatCount="indefinite"/></circle>
  <circle r="4" fill="#FACC15" stroke="#E0F2FE" stroke-width="1"/>
  <path d="M0 11l-5 15 5-3 5 3z" fill="#A78BFA"><animateTransform attributeName="transform" type="translate" values="0 0;0 3;0 0" dur="1s" repeatCount="indefinite"/></path>
</g>
<g class="meta"><text x="140" y="244">POWER NODES: LOW</text><rect x="255" y="234" width="12" height="12" rx="2" fill="#0F172A"/><rect x="273" y="234" width="12" height="12" rx="2" fill="#166534"/><rect x="291" y="234" width="12" height="12" rx="2" fill="#22C55E"/><rect x="309" y="234" width="12" height="12" rx="2" fill="#A7F3D0"/><text x="330" y="244">OVERDRIVE</text>
<text x="725" y="320">GITHUB CONTRIBUTION GRID // SECTOR: SANSKRITI49</text></g>
</svg>
"""


def main() -> None:
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    login = os.environ.get("GITHUB_USERNAME", "sanskriti49")
    if not token:
        raise SystemExit("GH_TOKEN or GITHUB_TOKEN is required")
    output = Path(os.environ.get("HEATMAP_OUTPUT", "assets/contribution-heatmap.svg"))
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render(fetch_calendar(login, token), login), encoding="utf-8")
    update_readme_cache_buster(Path("README.md"), date.today().strftime("%Y%m%d"))


if __name__ == "__main__":
    main()

import { readFileSync, writeFileSync, mkdirSync, existsSync } from "node:fs";
import { execFileSync } from "node:child_process";
import { resolve } from "node:path";

const photoPath = resolve(process.env.PROFILE_PHOTO || "assets/profile-photo.jpg");
const outputDir = resolve(process.env.TERMINAL_OUTPUT_DIR || "assets");
const asciiPath = resolve("assets/profile-ascii.txt");
execFileSync(process.env.PYTHON || "python", ["scripts/photo_to_ascii.py", photoPath, asciiPath]);
const ascii = readFileSync(asciiPath, "utf8")
  .split("\n")
  .map((line, index) => `<tspan x="48" y="${150 + index * 10}">${line.replaceAll("&", "&amp;").replaceAll("<", "&lt;").replaceAll(">", "&gt;")}</tspan>`)
  .join("");

const palettes = {
  dark: {
    background: "#050B12",
    panel: "#06131A",
    border: "#19D886",
    borderAlt: "#0B7661",
    primary: "#7AF5B2",
    secondary: "#38BDF8",
    text: "#D0FFE1",
    muted: "#257F69",
    photoOpacity: ".62",
  },
  light: {
    background: "#F3FAF7",
    panel: "#E7F5EF",
    border: "#087F5B",
    borderAlt: "#7DB8A1",
    primary: "#075E46",
    secondary: "#075985",
    text: "#102A23",
    muted: "#417566",
    photoOpacity: ".56",
  },
};

function card(theme, palette) {
  const p = palettes[palette];
  return `<svg xmlns="http://www.w3.org/2000/svg" width="1180" height="586" viewBox="0 0 1180 586" role="img" aria-labelledby="title desc">
<title id="title">Sanskriti Gupta hacker terminal profile</title>
<desc id="desc">A terminal-style profile card with a duotone portrait and system information.</desc>
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop stop-color="${p.background}"/><stop offset="1" stop-color="${p.panel}"/></linearGradient>
  <linearGradient id="photoTint" x1="0" y1="0" x2="1" y2="1"><stop stop-color="${p.secondary}"/><stop offset="1" stop-color="${p.primary}"/></linearGradient>
  <linearGradient id="asciiTint" x1="0" y1="0" x2="1" y2="1"><stop stop-color="${p.secondary}"/><stop offset="1" stop-color="${p.primary}"/></linearGradient>
  <pattern id="scanlines" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="1" fill="${p.secondary}" opacity=".07"/></pattern>
  <clipPath id="photoClip"><rect x="30" y="90" width="460" height="420" rx="12"/></clipPath>
  <style>
    .mono { font-family: "Courier New", Consolas, monospace; }
    .key { fill: ${p.primary}; font-size: 15px; font-weight: bold; }
    .ascii { fill: url(#asciiTint); font-size: 8px; letter-spacing: 1px; }
    .value { fill: ${p.text}; font-size: 15px; }
    .label { fill: ${p.secondary}; font-size: 11px; letter-spacing: 2px; }
    .muted { fill: ${p.muted}; font-size: 11px; letter-spacing: 1px; }
    .scan { animation: scan 4.4s linear infinite; }
    .blink { animation: blink 1.1s steps(2, end) infinite; }
    .glitch { animation: glitch 3.2s steps(2, end) infinite; }
    @keyframes scan { from { transform: translateY(-440px); } to { transform: translateY(440px); } }
    @keyframes blink { 0%, 45% { opacity: 1; } 50%, 100% { opacity: .15; } }
    @keyframes glitch { 0%, 92%, 100% { transform: translate(0); } 94% { transform: translate(3px, -1px); } 96% { transform: translate(-3px, 1px); } }
  </style>
</defs>
<rect width="1180" height="586" rx="18" fill="url(#bg)" stroke="${p.border}" stroke-width="2"/>
<rect x="14" y="18" width="488" height="540" rx="14" fill="${p.panel}" stroke="${p.borderAlt}"/>
<rect x="508" y="18" width="655" height="540" rx="14" fill="${p.panel}" stroke="${p.borderAlt}"/>
<circle cx="30" cy="20" r="5" fill="#EF4444"/><circle cx="48" cy="20" r="5" fill="#F59E0B"/><circle cx="66" cy="20" r="5" fill="#10B981"/>
<text x="590" y="25" text-anchor="middle" class="mono muted">sanskriti@forge ~ % ./profile.sh --live</text>
<circle cx="1060" cy="20" r="4" fill="#F87171" class="blink"/><text x="1072" y="24" class="mono muted">SCANNING</text>
<text x="30" y="48" class="mono label">VISUAL.MAP</text><text x="524" y="48" class="mono label">SYSTEM.INFO</text>
<g clip-path="url(#photoClip)">
  <rect x="30" y="90" width="460" height="420" fill="${p.background}"/>
  <text class="mono ascii" xml:space="preserve">${ascii}</text>
  <rect x="30" y="90" width="460" height="420" fill="url(#scanlines)"/>
  <rect class="scan" x="30" y="90" width="460" height="5" fill="${p.primary}" opacity=".8"/>
  <text x="48" y="116" class="mono muted">PHOTO.SIGNAL // ASCII DENSITY CHANNEL</text>
  <text x="48" y="492" class="mono muted">glitch channel stable // identity confirmed</text>
</g>
<g class="mono">
  <text x="524" y="92" class="key">sanskriti@forge</text>
  <text x="524" y="126" class="key">Subject ........ </text><text x="700" y="126" class="value">Sanskriti Gupta</text>
  <text x="524" y="150" class="key">Role ........... </text><text x="700" y="150" class="value">Full-Stack Developer · CS Student</text>
  <text x="524" y="174" class="key">Education ...... </text><text x="700" y="174" class="value">B.Tech CSE · VIT Bhopal</text>
  <text x="524" y="198" class="key">Status .......... </text><text x="700" y="198" class="value">Learning · Building · Shipping</text>
  <text x="524" y="222" class="key">ToolChain ....... </text><text x="700" y="222" class="value">GitHub Copilot · VS Code</text>
  <text x="524" y="246" class="key">Core Lang ....... </text><text x="700" y="246" class="value">Java · JavaScript · TypeScript · Python</text>
  <text x="524" y="270" class="key">Core Frontend ... </text><text x="700" y="270" class="value">React · Next.js · Tailwind CSS · GSAP</text>
  <text x="524" y="294" class="key">Core Backend .... </text><text x="700" y="294" class="value">Node.js · Express · REST · Socket.IO</text>
  <text x="524" y="318" class="key">Core Database ... </text><text x="700" y="318" class="value">PostgreSQL · MongoDB · Redis</text>
  <text x="524" y="342" class="key">Core Infra ...... </text><text x="700" y="342" class="value">AWS · Docker · Terraform · GitHub Actions</text>
  <line x1="524" y1="366" x2="1140" y2="366" stroke="${p.borderAlt}"/>
  <text x="524" y="394" class="label">- Contact</text>
  <text x="524" y="422" class="key">Portfolio ....... </text><text x="700" y="422" class="value">sanskriti49.github.io/my_portfolio</text>
  <text x="524" y="446" class="key">LinkedIn ........ </text><text x="700" y="446" class="value">linkedin.com/in/sanskriti49</text>
  <text x="524" y="470" class="key">GitHub .......... </text><text x="700" y="470" class="value">github.com/sanskriti49</text>
  <line x1="524" y1="490" x2="1140" y2="490" stroke="${p.borderAlt}"/>
  <text x="524" y="518" class="label">- Live Stats</text>
  <text x="524" y="542" class="value">See live GitHub stats below ↓</text>
</g>
</svg>`;
}

mkdirSync(outputDir, { recursive: true });
writeFileSync(resolve(outputDir, "terminal-card-dark.svg"), card("dark", "dark"));
writeFileSync(resolve(outputDir, "terminal-card-light.svg"), card("light", "light"));

const readmePath = resolve("README.md");
if (existsSync(readmePath)) {
  const version = new Date().toISOString().slice(0, 10).replaceAll("-", "");
  const readme = readFileSync(readmePath, "utf8").replace(
    /(\.\/assets\/terminal-card-(?:dark|light)\.svg)\?v=[^" )]+/g,
    `$1?v=${version}`,
  );
  writeFileSync(readmePath, readme);
}

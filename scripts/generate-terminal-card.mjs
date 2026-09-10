import { readFileSync, writeFileSync, mkdirSync, existsSync } from "node:fs";
import { resolve } from "node:path";

const outputDir = resolve(process.env.TERMINAL_OUTPUT_DIR || "assets");
const asciiPath = resolve("assets/profile-ascii.txt");

const rawLines = readFileSync(asciiPath, "utf8").split("\n");

const asciiDarkTspans = rawLines
  .map(
    (line, index) =>
      `<tspan x="16" y="${(26 + index * 10.5).toFixed(2)}" xml:space="preserve">${line
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")}</tspan>`,
  )
  .join("");

const palettes = {
  dark: {
    background: "#050B12",
    panel: "#06131A",
    screenBg: "#050b08",
    screenText: "#4ADE80",
    border: "#19D886",
    borderAlt: "#0B7661",
    primary: "#7AF5B2",
    secondary: "#38BDF8",
    text: "#D0FFE1",
    muted: "#257F69",
    statusDot: "#4ADE80",
    statusText: "LIVE // VERIFIED",
  },
  light: {
    background: "#F3FAF7",
    panel: "#E7F5EF",
    screenBg: "#FFFFFF",
    screenText: "#075E46",
    border: "#087F5B",
    borderAlt: "#7DB8A1",
    primary: "#075E46",
    secondary: "#075985",
    text: "#102A23",
    muted: "#417566",
    statusDot: "#087F5B",
    statusText: "LIVE // VERIFIED",
  },
};

function card(theme, palette) {
  const p = palettes[palette];
  return `<svg xmlns="http://www.w3.org/2000/svg" width="1180" height="586" viewBox="0 0 1180 586" role="img" aria-labelledby="title desc">
<title id="title">Sanskriti Gupta hacker terminal profile</title>
<desc id="desc">A terminal-style profile card with Sanskriti Gupta's ASCII portrait and system information.</desc>
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop stop-color="${p.background}"/><stop offset="1" stop-color="${p.panel}"/></linearGradient>
  <pattern id="scanlines" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="1" fill="#38BDF8" opacity=".04"/></pattern>
  <linearGradient id="scanBeam" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="${p.primary}" stop-opacity="0"/>
    <stop offset="50%" stop-color="${p.primary}" stop-opacity="0.28"/>
    <stop offset="100%" stop-color="${p.primary}" stop-opacity="0"/>
  </linearGradient>
  <clipPath id="photoClip"><rect x="30" y="90" width="460" height="420" rx="12"/></clipPath>
  <style>
    .mono { font-family: "SFMono-Regular", "JetBrains Mono", "Fira Code", Consolas, "DejaVu Sans Mono", monospace; }
    .key { fill: ${p.primary}; font-size: 15px; font-weight: bold; }
    .ascii { fill: ${p.screenText}; font-size: 10px; white-space: pre; }
    .value { fill: ${p.text}; font-size: 15px; }
    .label { fill: ${p.secondary}; font-size: 11px; letter-spacing: 2px; }
    .muted { fill: ${p.muted}; font-size: 11px; letter-spacing: 1px; }
    .screen-label { fill: ${p.primary}; font-size: 11px; letter-spacing: 1.5px; font-weight: bold; }
    .screen-muted { fill: ${p.muted}; font-size: 10px; letter-spacing: 1px; }
    .blink { animation: blink 1.5s ease-in-out infinite alternate; }
    @keyframes blink { 0% { opacity: 1; } 100% { opacity: 0.25; } }
  </style>
</defs>
<rect width="1180" height="586" rx="18" fill="url(#bg)" stroke="${p.border}" stroke-width="2"/>
<rect x="14" y="18" width="488" height="540" rx="14" fill="${p.panel}" stroke="${p.borderAlt}"/>
<rect x="508" y="18" width="655" height="540" rx="14" fill="${p.panel}" stroke="${p.borderAlt}"/>
<circle cx="30" cy="20" r="5" fill="#EF4444"/><circle cx="48" cy="20" r="5" fill="#F59E0B"/><circle cx="66" cy="20" r="5" fill="#10B981"/>
<text x="590" y="25" text-anchor="middle" class="mono muted">sanskriti@forge ~ % ./profile.sh --live</text>
<circle cx="1030" cy="20" r="4" fill="${p.statusDot}" class="blink"/><text x="1042" y="24" class="mono muted">${p.statusText}</text>
<text x="30" y="48" class="mono label">VISUAL.MAP</text><text x="524" y="48" class="mono label">SYSTEM.INFO</text>

<!-- Embedded Visual Map Display -->
<svg x="30" y="90" width="460" height="420" viewBox="0 0 692 630" clip-path="url(#photoClip)">
  <rect width="692" height="630" rx="12" fill="${p.screenBg}"/>
  <text x="16" y="26" class="mono ascii" xml:space="preserve">${asciiDarkTspans}</text>
  <rect width="692" height="630" fill="url(#scanlines)"/>
  <rect x="0" y="0" width="692" height="42" fill="url(#scanBeam)" pointer-events="none">
    <animate attributeName="y" values="-50;630;-50" dur="5.5s" repeatCount="indefinite"/>
  </rect>
</svg>

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

console.log("Terminal cards successfully updated with user provided ASCII SVG.");

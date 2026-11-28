import { writeFileSync } from 'node:fs';

const layers = [
  ['Interface', ['React.js', 'JavaScript', 'TypeScript']],
  ['API & services', ['Java', 'Node.js', 'Express.js', 'REST APIs', 'Socket.IO', 'FastAPI']],
  ['Data', ['PostgreSQL', 'SQL', 'Redis', 'MongoDB', 'PostGIS']],
  ['ML & retrieval', ['Python', 'PyTorch', 'scikit-learn', 'NumPy', 'RAG']],
  ['Delivery & tests', ['Git', 'Docker', 'GitHub Actions', 'Playwright', 'k6', 'AWS (EC2, S3)']],
];

const styles = `
    svg {
      --surface: #ffffff;
      --bar: #f5f5f8;
      --line: #dcdce6;
      --rule: #eeeef3;
      --ink: #24242e;
      --muted: #565566;
      --accent: #523897;
      --chip: #f0ebfb;
      --edge: #d9cdf4;
      --rail: #ad97de;
    }
    @media (prefers-color-scheme: dark) {
      svg {
        --surface: #16171b;
        --bar: #1c1d23;
        --line: #363641;
        --rule: #2a2a34;
        --ink: #f2f1f6;
        --muted: #b8b6c5;
        --accent: #d2c1ff;
        --chip: #29213b;
        --edge: #4b3b6b;
        --rail: #856bbb;
      }
    }
    .surface { fill: var(--surface); stroke: var(--line); }
    .bar { fill: var(--bar); }
    .divider { stroke: var(--line); }
    .rule { stroke: var(--rule); }
    .rail { fill: none; stroke: var(--rail); }
    .node { fill: var(--surface); stroke: var(--accent); stroke-width: 1.2; }
    .name, .command, .skill { font-family: Consolas, 'Liberation Mono', monospace; }
    .name { fill: var(--ink); font-size: 17px; font-weight: 700; letter-spacing: .45px; }
    .role, .layer { font-family: system-ui, sans-serif; }
    .role { fill: var(--muted); font-size: 14px; }
    .command { fill: var(--accent); font-size: 13px; }
    .layer { fill: var(--ink); font-size: 17px; font-weight: 650; }
    .chip { fill: var(--chip); stroke: var(--edge); }
    .skill { fill: var(--accent); font-weight: 600; }
    .compact .name { font-size: 16px; }
    .compact .layer { font-size: 15px; }
    .compact .command { font-size: 12px; }
`;

function escapeText(value) {
  return value.replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;');
}

function renderStackMap(compact) {
  const width = compact ? 358 : 916;
  const headerHeight = compact ? 69 : 61;
  const chipLeft = compact ? 35 : 218;
  const right = width - (compact ? 17 : 28);
  const fontSize = compact ? 14.5 : 16;
  const chipHeight = compact ? 24 : 29;
  const chipGap = compact ? 6 : 8;
  const lineGap = 6;
  const railX = compact ? 18 : 29;
  let rowTop = headerHeight + (compact ? 10 : 4);

  const rows = layers.map(([label, skills], index) => {
    const labelY = rowTop + (compact ? 17 : 35);
    let chipY = rowTop + (compact ? 25 : 15);
    let x = chipLeft;

    const chips = skills.map((skill) => {
      const chipWidth = Math.ceil(skill.length * fontSize * .61) + (compact ? 15 : 22);
      if (x + chipWidth > right) {
        x = chipLeft;
        chipY += chipHeight + lineGap;
      }
      const centerX = x + chipWidth / 2;
      const textY = chipY + (compact ? 17 : 20);
      const chip = `      <rect class="chip" x="${x}" y="${chipY}" width="${chipWidth}" height="${chipHeight}" rx="4"/>\n      <text class="skill" x="${centerX}" y="${textY}" text-anchor="middle" font-size="${fontSize}">${escapeText(skill)}</text>`;
      x += chipWidth + chipGap;
      return chip;
    });

    rowTop = chipY + chipHeight + 14;
    const separator = index === layers.length - 1
      ? ''
      : `\n    <path class="rule" d="M${compact ? chipLeft : 49} ${rowTop}H${right}"/>`;
    return { label, labelY, chips, separator };
  });

  const height = rowTop + (compact ? 5 : 6);
  const header = compact
    ? `<text class="name" x="17" y="29">SANSKRITI GUPTA</text>
    <text class="role" x="17" y="52">Software Developer</text>
    <text class="command" x="${right}" y="52" text-anchor="end">$ stack --list</text>`
    : `<text class="name" x="28" y="37">SANSKRITI GUPTA</text>
    <text class="role" x="197" y="37">·  Software Developer</text>
    <text class="command" x="${right}" y="37" text-anchor="end">~/sanskriti $ stack --list</text>`;

  return `<svg xmlns="http://www.w3.org/2000/svg" class="${compact ? 'compact' : 'wide'}" width="${width}" height="${height}" viewBox="0 0 ${width} ${height}" role="img" aria-labelledby="title description">
  <title id="title">Sanskriti Gupta — Software Developer</title>
  <desc id="description">${layers.map(([label, skills]) => `${escapeText(label)} — ${skills.join(', ')}.`).join(' ')}</desc>
  <style>${styles}  </style>
  <defs><clipPath id="frame"><rect x=".5" y=".5" width="${width - 1}" height="${height - 1}" rx="11"/></clipPath></defs>
  <rect class="surface" x=".5" y=".5" width="${width - 1}" height="${height - 1}" rx="11"/>
  <g clip-path="url(#frame)">
    <path class="bar" d="M1 1H${width - 1}V${headerHeight}H1Z"/>
    <path class="divider" d="M1 ${headerHeight}H${width - 1}"/>
    ${header}
    <path class="rail" d="M${railX} ${rows[0].labelY - 6}V${rows.at(-1).labelY - 6}"/>
${rows.map(({ label, labelY, chips, separator }) => `    <g aria-label="${escapeText(label)}">
      <circle class="node" cx="${railX}" cy="${labelY - 6}" r="3"/>
      <text class="layer" x="${compact ? 35 : 49}" y="${labelY}">${escapeText(label)}</text>
${chips.join('\n')}
    </g>${separator}`).join('\n')}
  </g>
</svg>
`;
}

for (const [filename, compact] of [['stack-map.svg', false], ['stack-map-compact.svg', true]]) {
  writeFileSync(new URL(`../assets/${filename}`, import.meta.url), renderStackMap(compact));
}

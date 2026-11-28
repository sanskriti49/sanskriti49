import { writeFileSync } from 'node:fs';

const layers = {
  browser: ['Browser', ['React.js', 'JavaScript', 'TypeScript']],
  api: ['API & services', ['Java', 'Node.js', 'Express.js', 'REST APIs', 'Socket.IO', 'FastAPI']],
  data: ['Data', ['PostgreSQL', 'SQL', 'Redis', 'MongoDB', 'PostGIS']],
  ml: ['ML & retrieval', ['Python', 'PyTorch', 'scikit-learn', 'NumPy', 'RAG']],
  delivery: ['Delivery & tests', ['Git', 'Docker', 'GitHub Actions', 'Playwright', 'k6', 'AWS (EC2, S3)']],
};
const introduction = 'Two clicks. One spot left. That’s my kind of problem.';

const styles = `
    svg {
      --paper: #fbfaf7;
      --header: #f2f1ee;
      --panel: #ffffff;
      --side: #eeeffb;
      --line: #d7d7d2;
      --ink: #20212a;
      --muted: #555761;
      --accent: #3042ba;
      --rail: #586acb;
      --chip: #f4f5ff;
      --chip-line: #c9d1f4;
    }
    @media (prefers-color-scheme: dark) {
      svg {
        --paper: #16171b;
        --header: #1c1d22;
        --panel: #1d2027;
        --side: #22263d;
        --line: #3b3d47;
        --ink: #f4f3f6;
        --muted: #bbc0ce;
        --accent: #b9c3ff;
        --rail: #899af1;
        --chip: #272d47;
        --chip-line: #464f76;
      }
    }
    .frame { fill: var(--paper); stroke: var(--line); }
    .head { fill: var(--header); }
    .divider { stroke: var(--line); }
    .name, .role, .label, .aside, .optional { font-family: system-ui, sans-serif; }
    .name { fill: var(--ink); font-size: 15px; font-weight: 720; letter-spacing: 1.05px; }
    .role { fill: var(--muted); font-size: 14px; }
    .command, .skill { font-family: ui-monospace, Consolas, 'Liberation Mono', monospace; }
    .command { fill: var(--accent); font-size: 13px; }
    .headline { fill: var(--ink); font-family: Georgia, 'Times New Roman', serif; font-size: 43px; }
    .headline-accent { fill: var(--accent); font-style: italic; }
    .aside { fill: var(--muted); font-size: 15px; }
    .aside-lead { fill: var(--ink); font-weight: 650; }
    .panel { fill: var(--panel); stroke: var(--line); }
    .branch-panel { fill: var(--side); stroke: var(--chip-line); }
    .label { fill: var(--ink); font-size: 17px; font-weight: 680; }
    .optional { fill: var(--muted); font-size: 11px; }
    .chip { fill: var(--chip); stroke: var(--chip-line); }
    .skill { fill: var(--accent); font-weight: 530; }
    .route, .branch, .arrow { fill: none; stroke: var(--rail); stroke-width: 1.45; stroke-linecap: round; stroke-linejoin: round; }
    .branch { stroke-dasharray: 3 4; }
    .junction { fill: var(--paper); stroke: var(--rail); stroke-width: 1.3; }
    .packet { fill: var(--accent); stroke: var(--paper); stroke-width: 1; }
    .compact .name { font-size: 13px; }
    .compact .role, .compact .command { font-size: 12px; }
    .compact .headline { font-size: 32px; }
    .compact .aside { font-size: 13px; }
    .compact .label { font-size: 15px; }
    @media (prefers-reduced-motion: reduce) {
      .packet { display: none; }
    }
`;

function escapeText(value) {
  return value.replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;');
}

function renderPanel(key, { x, y, width, compact }) {
  const [label, skills] = layers[key];
  const branch = key === 'ml';
  const padding = compact ? 10 : 13;
  const fontSize = compact ? 14 : 15;
  const gap = 5;
  const chipHeight = compact ? 23 : 25;
  let chipY = y + (compact ? 30 : 33);
  let chipX = x + padding;

  const chips = skills.map((skill) => {
    const chipWidth = Math.ceil(skill.length * fontSize * .61) + (compact ? 11 : 13);
    if (chipX + chipWidth > x + width - padding) {
      chipX = x + padding;
      chipY += chipHeight + 5;
    }
    const chip = `        <rect class="chip" x="${chipX}" y="${chipY}" width="${chipWidth}" height="${chipHeight}" rx="5"/>
        <text class="skill" x="${chipX + chipWidth / 2}" y="${chipY + (compact ? 16 : 17)}" text-anchor="middle" font-size="${fontSize}">${escapeText(skill)}</text>`;
    chipX += chipWidth + gap;
    return chip;
  });

  const height = chipY + chipHeight + (compact ? 10 : 12) - y;
  return {
    height,
    port: y + 21,
    markup: `    <g aria-label="${escapeText(label)}">
      <rect class="${branch ? 'branch-panel' : 'panel'}" x="${x}" y="${y}" width="${width}" height="${height}" rx="9"/>
      <text class="label" x="${x + padding}" y="${y + 22}">${escapeText(label)}</text>${branch ? `
      <text class="optional" x="${x + width - padding}" y="${y + 21}" text-anchor="end">optional</text>` : ''}
${chips.join('\n')}
    </g>`,
  };
}

function renderStackMap(compact) {
  const width = compact ? 358 : 938;
  const headerHeight = compact ? 55 : 48;
  const panelX = compact ? 32 : 65;
  const railX = compact ? 18 : 34;
  const columnWidth = compact ? 306 : 555;
  const panelGap = compact ? 11 : 14;
  const browserY = compact ? 137 : 130;
  const browser = renderPanel('browser', { x: panelX, y: browserY, width: columnWidth, compact });
  const apiY = browserY + browser.height + panelGap;
  const api = renderPanel('api', { x: panelX, y: apiY, width: columnWidth, compact });
  const dataY = apiY + api.height + panelGap;
  const data = renderPanel('data', { x: panelX, y: dataY, width: columnWidth, compact });

  const branchX = compact ? panelX : 650;
  const branchY = compact ? dataY + data.height + panelGap : apiY;
  const branchWidth = compact ? columnWidth : width - branchX - 27;
  const branch = renderPanel('ml', { x: branchX, y: branchY, width: branchWidth, compact });
  const deliveryY = Math.max(dataY + data.height, branchY + branch.height) + (compact ? 19 : 24);
  const margin = compact ? 14 : 27;
  const delivery = renderPanel('delivery', { x: margin, y: deliveryY, width: width - 2 * margin, compact });
  const height = deliveryY + delivery.height + margin;

  const header = compact
    ? `<text class="name" x="17" y="23">SANSKRITI GUPTA</text>
    <text class="role" x="17" y="42">Software Developer</text>
    <text class="command" x="341" y="42" text-anchor="end">$ stack --list</text>`
    : `<text class="name" x="27" y="30">SANSKRITI GUPTA</text>
    <text class="role" x="193" y="30">Software Developer</text>
    <text class="command" x="911" y="30" text-anchor="end">~/sanskriti $ stack --list</text>`;

  const story = compact
    ? `<text class="headline" x="17" y="92">From click <tspan class="headline-accent">to commit.</tspan></text>
    <text class="aside" x="18" y="115">${introduction}</text>`
    : `<text class="headline" x="27" y="101">From click <tspan class="headline-accent">to commit.</tspan></text>
    <text class="aside" x="910" y="81" text-anchor="end"><tspan class="aside-lead">Two clicks. One spot left.</tspan><tspan x="910" y="102">That’s my kind of problem.</tspan></text>`;

  const mainRoute = `M${railX} ${browser.port}V${data.port}`;
  const trailingRequest = `M${railX} ${browser.port}V${data.port - 13}`;
  const branchRight = panelX + columnWidth;
  const branchRoute = compact
    ? `M${branchRight} ${api.port}h10V${branch.port}h-10`
    : `M${branchRight} ${api.port}H${branchX}`;
  const branchArrow = compact
    ? `M${branchRight + 4} ${branch.port - 3}l-4 3 4 3`
    : `M${branchX - 5} ${branch.port - 3}l5 3-5 3`;

  return `<svg xmlns="http://www.w3.org/2000/svg" class="${compact ? 'compact' : 'wide'}" width="${width}" height="${height}" viewBox="0 0 ${width} ${height}" role="img" aria-labelledby="title description">
  <title id="title">Sanskriti Gupta — From click to commit</title>
  <desc id="description">${introduction} The browser connects to the API and then to the data layer. ML and retrieval can branch from the API. ${Object.values(layers).map(([label, skills]) => `${escapeText(label)} — ${skills.join(', ')}.`).join(' ')}</desc>
  <style>${styles}  </style>
  <defs><clipPath id="frame"><rect x=".5" y=".5" width="${width - 1}" height="${height - 1}" rx="14"/></clipPath></defs>
  <rect class="frame" x=".5" y=".5" width="${width - 1}" height="${height - 1}" rx="14"/>
  <g clip-path="url(#frame)">
    <path class="head" d="M1 1H${width - 1}V${headerHeight}H1Z"/>
    <path class="divider" d="M1 ${headerHeight}H${width - 1}"/>
    ${header}
    ${story}

    <g aria-hidden="true">
      <path class="route" d="${mainRoute}"/>
      ${[browser, api, data].map(({ port }) => `<path class="route" d="M${railX} ${port}H${panelX}"/><circle class="junction" cx="${railX}" cy="${port}" r="3"/>`).join('\n      ')}
      <path class="arrow" d="${[apiY - 6, dataY - 6].map((y) => `M${railX - 3} ${y - 3}l3 4 3-4`).join(' ')}"/>
      <path class="branch" d="${branchRoute}"/>
      <path class="arrow" d="${branchArrow}"/>
      <circle class="packet" r="3.6" opacity="0">
        <animateMotion dur="3.2s" begin=".45s" repeatCount="1" path="${mainRoute}"/>
        <animate attributeName="opacity" values="0;1;1;0" keyTimes="0;.08;.96;1" dur="3.2s" begin=".45s"/>
      </circle>
      <circle class="packet" r="2.7" opacity="0">
        <animateMotion dur="3.2s" begin=".72s" repeatCount="1" path="${trailingRequest}"/>
        <animate attributeName="opacity" values="0;.8;.8;0" keyTimes="0;.08;.93;1" dur="3.2s" begin=".72s"/>
      </circle>
    </g>

${[browser, api, data, branch, delivery].map(({ markup }) => markup).join('\n')}
  </g>
</svg>
`;
}

for (const [filename, compact] of [['stack-map.svg', false], ['stack-map-compact.svg', true]]) {
  writeFileSync(new URL(`../assets/${filename}`, import.meta.url), renderStackMap(compact));
}

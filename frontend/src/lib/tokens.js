export const tokens = {
  ink: "#12181D",
  panel: "#1A2128",
  panelRaised: "#1F2730",
  hairline: "#2B333B",
  text: "#ECEFF2",
  muted: "#8A97A0",
  faint: "#5B646C",
  amber: "#E8A33D",
  amberDim: "#7A5A28",
  weak: "#F0605A",
  mid: "#E8A33D",
  strong: "#4CC38A",
};

export const fontDisplay = "'Fraunces', Georgia, serif";
export const fontBody = "'Inter', system-ui, sans-serif";
export const fontMono = "'IBM Plex Mono', ui-monospace, monospace";

/**
 * Interpolates red -> amber -> green based on an acceptance rate (0-100).
 * Used for the topic heatmap and any other strength-coded value.
 */
export function strengthColor(rate) {
  const clamp = Math.max(0, Math.min(100, rate ?? 0));
  const c1 = clamp < 50 ? tokens.weak : tokens.mid;
  const c2 = clamp < 50 ? tokens.mid : tokens.strong;
  const t = clamp < 50 ? clamp / 50 : (clamp - 50) / 50;

  const hex = (h) => [h.slice(1, 3), h.slice(3, 5), h.slice(5, 7)].map((v) => parseInt(v, 16));
  const [r1, g1, b1] = hex(c1);
  const [r2, g2, b2] = hex(c2);
  const r = Math.round(r1 + (r2 - r1) * t);
  const g = Math.round(g1 + (g2 - g1) * t);
  const b = Math.round(b1 + (b2 - b1) * t);
  return `rgb(${r}, ${g}, ${b})`;
}

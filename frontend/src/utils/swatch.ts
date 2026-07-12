const PALETTE = [
  "linear-gradient(160deg,#3a2a1a,#5a3a20)",
  "linear-gradient(160deg,#7a1f1f,#2a1010)",
  "linear-gradient(160deg,#222,#555)",
  "linear-gradient(160deg,#0a2a1a,#0d3d26)",
  "linear-gradient(160deg,#8a5a1a,#c2831f)",
  "linear-gradient(160deg,#1a3320,#3a5a2a)",
  "linear-gradient(160deg,#0a1a3a,#1a3a6a)",
  "linear-gradient(160deg,#1a1a2a,#3a3a5a)",
  "linear-gradient(160deg,#2a2a1a,#5a5a2a)",
  "linear-gradient(160deg,#3a0a10,#7a1a20)",
];

export function swatchFor(movieId: number): string {
  return PALETTE[movieId % PALETTE.length];
}

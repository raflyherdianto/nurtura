import type { FoodItem, LocalizedString } from '../types';

export const FOOD_ITEMS: FoodItem[] = [
  {
    k: 'nasi',
    kind: 'carb',
    name: { id: 'Nasi tim', en: 'Soft rice' },
    fill: '#efe2bb',
    stroke: '#c4af78',
    shapes: [[112, 168, 56, 48, 3]],
  },
  {
    k: 'bayam',
    kind: 'veg',
    name: { id: 'Bayam', en: 'Spinach' },
    fill: '#5f7d3a',
    stroke: '#41592a',
    shapes: [
      [200, 98, 34, 26, 7],
      [168, 86, 22, 18, 11],
    ],
  },
  {
    k: 'alpukat',
    kind: 'fat',
    name: { id: 'Alpukat', en: 'Avocado' },
    fill: '#b8cc5c',
    stroke: '#7f9438',
    shapes: [
      [92, 104, 22, 14, 15],
      [122, 90, 16, 11, 16],
    ],
  },
  {
    k: 'tempe',
    kind: 'plant',
    name: { id: 'Tempe', en: 'Tempeh' },
    fill: '#cfa86c',
    stroke: '#9c7740',
    shapes: [
      [84, 222, 12, 10, 12],
      [103, 238, 11, 9, 13],
      [74, 198, 10, 9, 14],
    ],
  },
  {
    k: 'telur',
    kind: 'animal',
    name: { id: 'Telur orak', en: 'Scrambled egg' },
    fill: '#f2c64d',
    stroke: '#c99720',
    shapes: [
      [222, 168, 30, 24, 5],
      [204, 192, 18, 14, 9],
    ],
  },
  {
    k: 'hati',
    kind: 'animal',
    name: { id: 'Hati ayam', en: 'Chicken liver' },
    fill: '#8a4a33',
    stroke: '#5e301f',
    shapes: [
      [210, 228, 16, 12, 2],
      [188, 240, 13, 10, 4],
      [230, 212, 11, 9, 6],
    ],
  },
  {
    k: 'ikan',
    kind: 'animal',
    name: { id: 'Ikan kembung', en: 'Mackerel' },
    fill: '#f4a98a',
    stroke: '#cf7552',
    shapes: [
      [138, 240, 22, 10, 8],
      [162, 254, 18, 8, 1],
    ],
  },
  {
    k: 'minyak',
    kind: 'fat',
    name: { id: 'Minyak / santan', en: 'Oil / coconut milk' },
    fill: '#f8e9a1',
    stroke: '#dcbf52',
    shapes: [
      [118, 150, 8, 6, 17],
      [142, 174, 7, 5, 18],
      [96, 164, 7, 5, 19],
    ],
  },
];

export const AGES = [7, 10, 14];

export const TEXTURES: LocalizedString[] = [
  { id: 'Saring', en: 'Puree' },
  { id: 'Lumat', en: 'Mash' },
  { id: 'Cincang', en: 'Minced' },
  { id: 'Finger food', en: 'Finger food' },
  { id: 'Makanan keluarga', en: 'Family meal' },
];

export const TEXTURE_RANGES: Record<number, [number, number]> = {
  7: [0, 1],
  10: [2, 3],
  14: [3, 4],
};

export const TARGET_TEXTURES: Record<number, LocalizedString> = {
  7: { id: 'lumat halus', en: 'a fine mash' },
  10: { id: 'cincang halus atau finger food lunak', en: 'finely minced food or soft finger food' },
  14: { id: 'cincang kasar atau makanan keluarga yang dipotong kecil', en: 'coarsely chopped or small-cut family food' },
};

export const RECIPES: Record<string, { name: LocalizedString; rec: LocalizedString }> = {
  animal: {
    name: { id: 'Protein hewani', en: 'Animal protein' },
    rec: {
      id: '<b>Telur orak lembut, 5 menit:</b> kocok 1 butir telur, masak dengan 1 sdt minyak di api kecil sambil diaduk sekitar 2 menit, lalu sesuaikan teksturnya. Alternatif hemat: 2 sdm hati ayam atau ikan kembung kukus.',
      en: '<b>Soft scrambled egg, 5 minutes:</b> whisk 1 egg, cook with 1 tsp oil on low heat, stirring about 2 minutes, then adjust the texture. Budget swap: 2 tbsp steamed chicken liver or mackerel.',
    },
  },
  fat: {
    name: { id: 'Lemak sehat', en: 'Healthy fats' },
    rec: {
      id: '<b>Tambah lemak:</b> aduk 1 sdt minyak kelapa atau 2 sdm santan encer ke makanan yang sudah matang, atau lumatkan ¼ buah alpukat.',
      en: '<b>Add fat:</b> stir 1 tsp coconut oil or 2 tbsp thin coconut milk into the cooked meal, or mash in ¼ avocado.',
    },
  },
  carb: {
    name: { id: 'Karbohidrat', en: 'Carbohydrates' },
    rec: {
      id: '<b>Tambah energi:</b> 3–4 sdm nasi tim, atau ubi atau kentang kukus yang dilumatkan.',
      en: '<b>Add energy:</b> 3–4 tbsp soft rice, or steamed sweet potato or potato, mashed.',
    },
  },
};

/**
 * Deterministic pseudo-random generator
 */
function pseudoRandom(seed: number) {
  let s = seed;
  return function () {
    s = (s * 9301 + 49297) % 233280;
    return s / 233280;
  };
}

/**
 * Generates an organic rounded SVG blob path using cubic beziers
 */
export function generateBlobPath(cx: number, cy: number, rx: number, ry: number, seed: number): string {
  const n = 9;
  const rand = pseudoRandom(seed);
  const p: [number, number][] = [];

  for (let i = 0; i < n; i++) {
    const a = (i / n) * Math.PI * 2;
    const k = 0.82 + rand() * 0.3;
    p.push([cx + Math.cos(a) * rx * k, cy + Math.sin(a) * ry * k]);
  }

  let d = `M${p[0][0].toFixed(1)} ${p[0][1].toFixed(1)}`;
  for (let i = 0; i < n; i++) {
    const p0 = p[(i + n - 1) % n];
    const p1 = p[i];
    const p2 = p[(i + 1) % n];
    const p3 = p[(i + 2) % n];
    const cp1x = (p1[0] + (p2[0] - p0[0]) / 6).toFixed(1);
    const cp1y = (p1[1] + (p2[1] - p0[1]) / 6).toFixed(1);
    const cp2x = (p2[0] - (p3[0] - p1[0]) / 6).toFixed(1);
    const cp2y = (p2[1] - (p3[1] - p1[1]) / 6).toFixed(1);
    const p2x = p2[0].toFixed(1);
    const p2y = p2[1].toFixed(1);

    d += `C${cp1x} ${cp1y} ${cp2x} ${cp2y} ${p2x} ${p2y}`;
  }
  return d + 'Z';
}

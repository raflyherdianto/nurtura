export type Language = 'id' | 'en';

export interface LocalizedString {
  id: string;
  en: string;
}

export interface MilestoneScenario {
  id: string;
  name: LocalizedString;
  targetAge: number;
  note: LocalizedString;
  ref: LocalizedString;
  statusType: 'ok' | 'watch' | 'alert';
  statusTitle: LocalizedString;
  statusDesc: LocalizedString;
  safety: LocalizedString;
  focusArea: LocalizedString;
  playbook: PlaybookDay[];
  ragSources?: string[];
}

export interface PlaybookStep {
  text: LocalizedString;
}

export interface PlaybookDay {
  day: number;
  item: LocalizedString;
  title: LocalizedString;
  steps: LocalizedString[];
}

export type FoodCategory = 'carb' | 'veg' | 'fat' | 'plant' | 'animal';

export interface FoodShape {
  cx: number;
  cy: number;
  rx: number;
  ry: number;
  seed: number;
}

export interface FoodItem {
  k: string;
  kind: FoodCategory;
  name: LocalizedString;
  fill: string;
  stroke: string;
  shapes: [number, number, number, number, number][];
}

export type MacroRating = 'low' | 'ok' | 'good';

export interface MacroInfo {
  key: 'animal' | 'fat' | 'carb';
  name: LocalizedString;
  rating: MacroRating;
  percentage: number;
  label: LocalizedString;
  hint?: LocalizedString;
  recipe?: LocalizedString;
}

export interface TextureVerdict {
  status: 'fine' | 'ok' | 'coarse';
  title: LocalizedString;
  description: LocalizedString;
}

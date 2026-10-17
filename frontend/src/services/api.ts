import type { LocalizedString, PlaybookDay } from '../types';

export interface ChildContextPayload {
  name: string;
  gender?: 'boy' | 'girl';
  age_months: number;
  weight_kg: number;
  height_cm: number;
}

export interface MilestoneEvaluationApiResponse {
  id: string;
  status_type: 'ok' | 'watch' | 'alert';
  status_title: LocalizedString;
  status_desc: LocalizedString;
  ref: LocalizedString;
  safety: LocalizedString;
  focus_area: LocalizedString;
  playbook: PlaybookDay[];
  rag_sources?: string[];
}

export interface PlateAuditApiResponse {
  id: string;
  meal_time: string;
  detected_foods: Array<{
    name: LocalizedString;
    kind: 'animal' | 'fat' | 'carb' | 'veg' | 'plant';
    confidence?: number;
  }>;
  detected_texture: string;
  texture_verdict: {
    status: 'fine' | 'ok' | 'coarse';
    title: LocalizedString;
    description: LocalizedString;
  };
  macros: Array<{
    key: 'animal' | 'fat' | 'carb';
    name: LocalizedString;
    rating: 'low' | 'ok' | 'good';
    percentage: number;
    label: LocalizedString;
    hint?: LocalizedString;
    recipe?: LocalizedString;
  }>;
  deficient_macros: string[];
  upgrade_plan: {
    summary: LocalizedString;
    suggestions: LocalizedString[];
    booster_recipe?: {
      name: LocalizedString;
      prep_time: LocalizedString;
      ingredients: LocalizedString[];
      instructions: LocalizedString[];
    };
  };
  disclaimer: LocalizedString;
  rag_sources?: string[];
}

export interface HealthCheckResponse {
  status: string;
  app_name: string;
  version: string;
  environment: string;
  gemini: {
    model: string;
    is_configured: boolean;
    mode: 'live_gemini' | 'pediatric_engine_fallback';
  };
}

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1';
const AI_ANALYSIS_TIMEOUT_MS = 60000;

export const apiClient = {
  async checkHealth(): Promise<boolean> {
    try {
      const res = await fetch(`${API_BASE_URL}/health`, { signal: AbortSignal.timeout(2000) });
      return res.ok;
    } catch {
      return false;
    }
  },

  async getHealthDetails(): Promise<HealthCheckResponse | null> {
    try {
      const res = await fetch(`${API_BASE_URL}/health`, { signal: AbortSignal.timeout(3000) });
      if (!res.ok) return null;
      return await res.json();
    } catch {
      return null;
    }
  },

  async evaluateMilestone(
    child: ChildContextPayload,
    observationNote: string,
    checkedMilestones: string[] = []
  ): Promise<MilestoneEvaluationApiResponse> {
    const res = await fetch(`${API_BASE_URL}/milestone/evaluate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        child,
        observation_note: observationNote,
        checked_milestones: checkedMilestones,
      }),
      signal: AbortSignal.timeout(AI_ANALYSIS_TIMEOUT_MS),
    });

    if (!res.ok) {
      let detail = res.statusText;
      try {
        const body = await res.json();
        if (typeof body.detail === 'string') detail = body.detail;
      } catch {
        // Keep the HTTP status text when the response is not JSON.
      }
      throw new Error(`Milestone evaluation failed: ${detail}`);
    }

    return res.json();
  },

  async auditPlate(
    child: ChildContextPayload,
    mealTime: string,
    selectedItems: string[],
    notes?: string
  ): Promise<PlateAuditApiResponse> {
    const res = await fetch(`${API_BASE_URL}/plate/audit`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        child,
        meal_time: mealTime,
        selected_items: selectedItems,
        notes,
      }),
      signal: AbortSignal.timeout(15000),
    });

    if (!res.ok) {
      throw new Error(`Plate audit failed: ${res.statusText}`);
    }

    return res.json();
  },

  async auditPlateUpload(formData: FormData): Promise<PlateAuditApiResponse> {
    const res = await fetch(`${API_BASE_URL}/plate/audit-upload`, {
      method: 'POST',
      body: formData,
      signal: AbortSignal.timeout(30000),
    });

    if (!res.ok) {
      throw new Error(`Plate photo audit failed: ${res.statusText}`);
    }

    return res.json();
  },
};

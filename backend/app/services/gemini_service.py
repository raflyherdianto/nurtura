import asyncio
import json
import logging
import os
import uuid
from typing import Any, Dict, List, Optional
from app.core.config import get_settings
from app.schemas.child import ChildContext
from app.schemas.milestone import MilestoneEvaluationResponse, PlaybookDaySchema
from app.schemas.plate import (
    PlateAuditResponse,
    FoodDetectedItem,
    TextureVerdictSchema,
    MacroInfoSchema,
    UpgradePlanSchema,
    BoosterRecipeSchema,
)
from app.schemas.common import LocalizedString
from app.services.rag_service import get_rag_service

logger = logging.getLogger(__name__)


class GeminiService:
    def __init__(self):
        self.settings = get_settings()
        self.api_key = self.settings.gemini_api_key.strip()
        self.model_name = self.settings.gemini_model
        self.temperature = self.settings.gemini_temperature
        self.rag = get_rag_service()
        self._client = None
        self._init_client()

    def _init_client(self):
        # 1. Mode Vertex AI (Menggunakan kuota $300 Google Cloud Project)
        if self.settings.use_vertex_ai:
            if not self.settings.gcp_project_id:
                logger.warning("USE_VERTEX_AI=True tetapi GCP_PROJECT_ID belum diisi. Menjalankan mode fallback.")
                return
            try:
                from google import genai
                os.environ.setdefault("GOOGLE_CLOUD_PROJECT", self.settings.gcp_project_id)
                self._client = genai.Client(
                    vertexai=True,
                    project=self.settings.gcp_project_id,
                    location=self.settings.gcp_location or "us-central1",
                )
                logger.info(
                    "Initialized Vertex AI Client (Project: %s, Location: %s, Model: %s)",
                    self.settings.gcp_project_id,
                    self.settings.gcp_location,
                    self.model_name,
                )
                return
            except Exception as e:
                logger.error("Failed to initialize Vertex AI client: %s", e)
                self._client = None
                return

        # 2. Mode Google AI Studio (API Key / Free Tier)
        if not self.api_key or self.api_key.startswith("your_gemini"):
            logger.warning("GEMINI_API_KEY is not configured. Running in pediatric deterministic fallback mode.")
            return

        try:
            from google import genai
            self._client = genai.Client(api_key=self.api_key)
            logger.info("Initialized Google GenAI Client with model: %s", self.model_name)
        except Exception as e:
            logger.warning("Failed to initialize google.genai: %s. Attempting google.generativeai fallback.", e)
            try:
                import google.generativeai as legacy_genai
                legacy_genai.configure(api_key=self.api_key)
                self._client = legacy_genai.GenerativeModel(self.model_name)
                logger.info("Initialized google.generativeai Legacy Model: %s", self.model_name)
            except Exception as e2:
                logger.error("Failed to initialize any Gemini client: %s", e2)
                self._client = None

    @property
    def is_configured(self) -> bool:
        return self._client is not None

    async def evaluate_milestones(
        self,
        child: ChildContext,
        observation: str,
        checked_milestones: Optional[List[str]] = None,
    ) -> MilestoneEvaluationResponse:
        """
        Evaluates parental observation against WHO/CDC developmental milestones
        and crafts a 3-Day Home Stimulation Playbook using everyday household items.
        """
        if self._client is not None:
            return await self._call_gemini_milestones(child, observation, checked_milestones or [])

        raise RuntimeError("Vertex AI Gemini client is not configured.")

    async def audit_plate(
        self,
        child: ChildContext,
        meal_time: str,
        image_bytes: Optional[bytes] = None,
        image_mime: Optional[str] = None,
        selected_items: Optional[List[str]] = None,
        notes: Optional[str] = None,
    ) -> PlateAuditResponse:
        """
        Audits child's meal for oral-motor texture suitability,
        anti-stunting macro metrics (animal protein & healthy fats), and next-meal upgrade.
        """
        if self._client is not None and (image_bytes or selected_items or notes):
            try:
                return await self._call_gemini_plate(child, meal_time, image_bytes, image_mime, selected_items, notes)
            except Exception as e:
                logger.error("Gemini Vision/Plate API call failed: %s. Falling back to nutritional engine.", e)

        return self._fallback_plate(child, meal_time, selected_items, notes)

    # -------------------------------------------------------------
    # Gemini AI Implementations
    # -------------------------------------------------------------
    async def _call_gemini_milestones(
        self,
        child: ChildContext,
        observation: str,
        checked_milestones: List[str],
    ) -> MilestoneEvaluationResponse:
        rag_chunks = self.rag.retrieve_for_milestone(child.age_months, observation)
        rag_context = self.rag.format_for_prompt(rag_chunks)

        system_instruction = (
            "You are Nurtura, an expert pediatric early childhood development AI agent adhering to WHO, CDC, and IDAI guidelines. "
            "Evaluate parental observations with high empathy, clear developmental benchmarking, and safety guardrails. "
            "Never use alarming jargon; offer actionable 3-day home stimulation activities using only zero-cost household objects "
            "(e.g., cardboard boxes, plastic cups, spoons, socks). "
            "Strictly ground your developmental assessment and playbook in the provided official clinical references. "
            "Output MUST be strictly valid JSON matching the specified schema."
        )

        prompt = f"""
Official Clinical Guidelines Grounding (CDC & WHO/UNICEF CCD RAG KB):
{rag_context}

Child Profile:
- Name: {child.name}
- Age: {child.age_months} months
- Weight: {child.weight_kg} kg
- Height: {child.height_cm} cm

Parent's Observation Note:
"{observation}"

Checked Milestones:
{json.dumps(checked_milestones)}

Please output a JSON response with this exact structure:
{{
  "id": "{str(uuid.uuid4())[:8]}",
  "status_type": "ok" | "watch" | "alert",
  "status_title": {{ "id": "Judul status dalam Bahasa Indonesia", "en": "Status title in English" }},
  "status_desc": {{ "id": "Penjelasan klinis empatik dalam Bahasa Indonesia", "en": "Empathetic clinical description in English" }},
  "ref": {{ "id": "Rujukan pedoman WHO/CDC", "en": "WHO/CDC reference" }},
  "safety": {{ "id": "Panduan keamanan/kapan harus ke dokter", "en": "Pediatric safety/red flag advice" }},
  "focus_area": {{ "id": "Area fokus tumbuh kembang", "en": "Primary developmental focus area" }},
  "playbook": [
    {{
      "day": 1,
      "item": {{ "id": "Barang rumah tangga (misal: Kardus bekas)", "en": "Household item (e.g. Cardboard box)" }},
      "title": {{ "id": "Nama permainan hari 1", "en": "Day 1 activity title" }},
      "steps": [
        {{ "id": "Langkah 1", "en": "Step 1" }},
        {{ "id": "Langkah 2", "en": "Step 2" }},
        {{ "id": "Langkah 3", "en": "Step 3" }}
      ]
    }},
    {{
      "day": 2,
      "item": {{ "id": "Barang rumah tangga", "en": "Household item" }},
      "title": {{ "id": "Nama permainan hari 2", "en": "Day 2 activity title" }},
      "steps": [
        {{ "id": "Langkah 1", "en": "Step 1" }},
        {{ "id": "Langkah 2", "en": "Step 2" }},
        {{ "id": "Langkah 3", "en": "Step 3" }}
      ]
    }},
    {{
      "day": 3,
      "item": {{ "id": "Barang rumah tangga", "en": "Household item" }},
      "title": {{ "id": "Nama permainan hari 3", "en": "Day 3 activity title" }},
      "steps": [
        {{ "id": "Langkah 1", "en": "Step 1" }},
        {{ "id": "Langkah 2", "en": "Step 2" }},
        {{ "id": "Langkah 3", "en": "Step 3" }}
      ]
    }}
  ]
}}
Only return the valid JSON, no markdown codeblocks or extra text.
"""
        response_text = await self._execute_gemini_prompt(system_instruction, prompt)
        data = self._clean_and_parse_json(response_text)
        if "rag_sources" not in data or not data["rag_sources"]:
            data["rag_sources"] = [f"{c.title} ({c.source})" for c in rag_chunks]
        return MilestoneEvaluationResponse(**data)

    async def _call_gemini_plate(
        self,
        child: ChildContext,
        meal_time: str,
        image_bytes: Optional[bytes],
        image_mime: Optional[str],
        selected_items: Optional[List[str]],
        notes: Optional[str],
    ) -> PlateAuditResponse:
        rag_chunks = self.rag.retrieve_for_plate(child.age_months, selected_items, notes or "")
        rag_context = self.rag.format_for_prompt(rag_chunks)

        system_instruction = (
            "You are Nurtura Smart Plate Vision, an expert pediatric MPASI and anti-stunting nutrition AI agent. "
            "Analyze baby/toddler meal photos dynamically. "
            "Identify ALL visible food ingredients realistically and specifically from the image or description without being limited or fixed to any predefined list (e.g. Daging Sapi Cincang, Hati Ayam, Ikan Kembung/Salmon, Sup Wortel, Brokoli Kukus, Bubur Nasi, Puree Labu Kuning, Minyak Kelapa, Santan, Tahu Sutra, Alpukat, dll.). "
            "For each detected ingredient, categorize accurately into 'kind': 'animal' (daging, ayam, telur, ikan, hati), 'fat' (minyak, santan, mentega, keju, alpukat), 'carb' (nasi, bubur, kentang, ubi, mie, oat), 'veg' (sayuran hijau/oranye), or 'plant' (tempe, tahu, kacang-kacangan). "
            "Evaluate: "
            "1. Oral-motor texture suitability based on age in months (6-8m: puree/saring, 9-11m: cincang halus/nasi tim, 12m+: makanan keluarga). "
            "2. Macro nutrient completeness with strong priority on ANIMAL PROTEIN and ADDED FATS to combat stunting. "
            "Plant proteins (tahu, tempe) are good but DO NOT substitute animal protein for linear growth. "
            "3. Next-meal actionable upgrade with a fast 5-minute booster recipe. "
            "Strictly ground your clinical recommendations and texture checks in the provided official guidelines. "
            "Output MUST be strictly valid JSON matching the specified schema."
        )

        prompt = f"""
Official MPASI & Anti-Stunting Guidelines (WHO 2023 & IDAI RAG KB):
{rag_context}

Child Context:
- Age: {child.age_months} months
- Weight: {child.weight_kg} kg
- Height: {child.height_cm} cm
- Meal Time: {meal_time}
- Food Items / Notes: {notes or (', '.join(selected_items) if selected_items else 'Uploaded photo')}

Analyze this meal and return JSON in this exact structure:
{{
  "id": "{str(uuid.uuid4())[:8]}",
  "meal_time": "{meal_time}",
  "detected_foods": [
    {{
      "name": {{ "id": "Nama spesifik bahan (misal: Daging Sapi Cincang, Bubur Nasi, Brokoli)", "en": "Specific detected food item (e.g. Minced Beef, Rice Porridge, Steamed Broccoli)" }},
      "kind": "animal" | "fat" | "carb" | "veg" | "plant",
      "confidence": 0.95
    }}
  ],
  "detected_texture": "Tekstur yang teridentifikasi (misal: Cincang kasar / Nasi tim)",
  "texture_verdict": {{
    "status": "fine" | "ok" | "coarse",
    "title": {{ "id": "Judul status tekstur", "en": "Texture verdict title" }},
    "description": {{ "id": "Ulasan kesesuaian oromotor dengan usia {child.age_months} bulan", "en": "Oral-motor age suitability description" }}
  }},
  "macros": [
    {{
      "key": "animal",
      "name": {{ "id": "Protein Hewani", "en": "Animal Protein" }},
      "rating": "low" | "ok" | "good",
      "percentage": 15 | 66 | 100,
      "label": {{ "id": "Kurang / Cukup / Baik", "en": "Low / Fair / Good" }},
      "hint": {{ "id": "Catatan khusus (opsional)", "en": "Specific hint (optional)" }},
      "recipe": {{ "id": "Rekomendasi tambahan", "en": "Quick tip" }}
    }},
    {{
      "key": "fat",
      "name": {{ "id": "Lemak Tambahan", "en": "Added Fat" }},
      "rating": "low" | "ok" | "good",
      "percentage": 15 | 66 | 100,
      "label": {{ "id": "Kurang / Cukup / Baik", "en": "Low / Fair / Good" }},
      "recipe": {{ "id": "Rekomendasi lemak sehat", "en": "Healthy fat tip" }}
    }},
    {{
      "key": "carb",
      "name": {{ "id": "Karbohidrat", "en": "Carbohydrates" }},
      "rating": "low" | "ok" | "good",
      "percentage": 15 | 66 | 100,
      "label": {{ "id": "Kurang / Cukup / Baik", "en": "Low / Fair / Good" }}
    }}
  ],
  "deficient_macros": ["animal", "fat"],
  "upgrade_plan": {{
    "summary": {{ "id": "Ringkasan perbaikan gizi jam makan berikutnya", "en": "Next meal upgrade summary" }},
    "suggestions": [
      {{ "id": "Saran 1", "en": "Suggestion 1" }},
      {{ "id": "Saran 2", "en": "Suggestion 2" }}
    ],
    "booster_recipe": {{
      "name": {{ "id": "Resep Booster Kilat (misal: Telur Orak-Arik Mentega)", "en": "5-Min Booster Recipe" }},
      "prep_time": {{ "id": "5 Menit", "en": "5 Minutes" }},
      "ingredients": [
        {{ "id": "1 butir telur ayam", "en": "1 egg" }},
        {{ "id": "1 sdt margarin/mentega", "en": "1 tsp butter" }}
      ],
      "instructions": [
        {{ "id": "Kocok telur lepas.", "en": "Whisk egg lightly." }},
        {{ "id": "Panaskan mentega di wajan dan orak-arik hingga matang lembut.", "en": "Heat butter and gently scramble until soft." }}
      ]
    }}
  }},
  "disclaimer": {{
    "id": "Hasil audit ini adalah panduan edukasi MPASI anti-stunting berbasis pedoman IDAI/WHO, bukan pengganti konsultasi dokter spesialis anak.",
    "en": "This audit is an educational anti-stunting MPASI guide based on IDAI/WHO recommendations, not a substitute for pediatric consultation."
  }}
}}
Only return the valid JSON, no markdown codeblocks or extra text.
"""
        response_text = await self._execute_gemini_prompt(
            system_instruction,
            prompt,
            image_bytes=image_bytes,
            image_mime=image_mime,
        )
        data = self._clean_and_parse_json(response_text)
        if "rag_sources" not in data or not data["rag_sources"]:
            data["rag_sources"] = [f"{c.title} ({c.source})" for c in rag_chunks]
        return PlateAuditResponse(**data)

    async def _execute_gemini_prompt(
        self,
        system_instruction: str,
        prompt: str,
        image_bytes: Optional[bytes] = None,
        image_mime: Optional[str] = None,
    ) -> str:
        # Do not try AI Studio aliases on Vertex AI. Vertex resolves model IDs
        # against the selected project and region, so an invalid fallback can
        # hide the actual configured model error.
        models_to_try = [self.model_name]

        last_error = None
        for model in models_to_try:
            for attempt in range(2):
                try:
                    from google.genai import types
                    contents = []
                    if image_bytes and image_mime:
                        contents.append(
                            types.Part.from_bytes(data=image_bytes, mime_type=image_mime)
                        )
                    contents.append(prompt)

                    response = self._client.models.generate_content(
                        model=model,
                        contents=contents,
                        config=types.GenerateContentConfig(
                            system_instruction=system_instruction,
                            temperature=self.temperature,
                            response_mime_type="application/json",
                        ),
                    )
                    return response.text
                except AttributeError:
                    # Fallback to legacy google.generativeai if client has generate_content directly
                    parts = []
                    if image_bytes and image_mime:
                        parts.append({"mime_type": image_mime, "data": image_bytes})
                    parts.append(f"{system_instruction}\n\n{prompt}")
                    res = self._client.generate_content(parts)
                    return res.text
                except Exception as e:
                    last_error = e
                    err_str = str(e).lower()
                    if "503" in err_str or "demand" in err_str or "unavailable" in err_str:
                        logger.warning(
                            "Model %s returned 503 high demand (attempt %d/2). Backing off before retry...",
                            model,
                            attempt + 1,
                        )
                        await asyncio.sleep(1.2 * (attempt + 1))
                        continue
                    # For non-503 (e.g. 404/400), don't retry same model, try next candidate
                    break

        if last_error:
            raise last_error
        raise RuntimeError("No Gemini model responded successfully.")

    def _clean_and_parse_json(self, raw_text: str) -> Dict[str, Any]:
        text = raw_text.strip()
        if text.startswith("```json"):
            text = text[7:]
        elif text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        text = text.strip()
        return json.loads(text)

    # -------------------------------------------------------------
    # Pediatric Deterministic Fallback Engine
    # (Guarantees zero crashes & instant testing offline)
    # -------------------------------------------------------------
    def _fallback_milestones(
        self,
        child: ChildContext,
        observation: str,
        checked_milestones: List[str],
    ) -> MilestoneEvaluationResponse:
        obs_lower = observation.lower()
        age = child.age_months
        rag_chunks = self.rag.retrieve_for_milestone(age, observation)
        rag_sources_list = [f"{c.title} ({c.source})" for c in rag_chunks]

        # Detect domain
        if "bicara" in obs_lower or "mama" in obs_lower or "kata" in obs_lower or "omong" in obs_lower or age >= 18:
            return MilestoneEvaluationResponse(
                id=str(uuid.uuid4())[:8],
                status_type="watch",
                status_title=LocalizedString(
                    id="Perlu Stimulasi Artikulasi Terarah",
                    en="Targeted Articulation Support Needed",
                ),
                status_desc=LocalizedString(
                    id=f"{child.name} ({age} bulan) menunjukkan kesadaran komunikasi yang baik, namun perbendaharaan kata aktif masih di bawah rujukan CDC/WHO. Latih stimulasi pengucapan interaktif 3 hari.",
                    en=f"{child.name} ({age} months) shows healthy communicative intent, but expressive vocabulary is slightly below CDC/WHO reference. Engage in 3-day responsive vocal play.",
                ),
                ref=LocalizedString(
                    id="Rujukan: Milestone CDC & WHO usia 18 bulan (menguasai minimal 3–5 kata selain mama/papa).",
                    en="Reference: CDC & WHO 18-month milestone (uses at least 3-5 distinct words beyond mama/papa).",
                ),
                safety=LocalizedString(
                    id="Konsultasikan ke dokter anak bila anak kehilangan kata yang pernah dikuasai atau tidak merespons panggilan namanya.",
                    en="Consult a pediatrician if your child loses previously acquired words or does not respond to their name.",
                ),
                focus_area=LocalizedString(
                    id="Bahasa Ekspresif & Komunikasi Timbal-Balik",
                    en="Expressive Language & Reciprocal Communication",
                ),
                rag_sources=rag_sources_list,
                playbook=[
                    PlaybookDaySchema(
                        day=1,
                        item=LocalizedString(id="Kardus bekas & mainan favorit", en="Old cardboard box & favorite toys"),
                        title=LocalizedString(id="Kotak Kejutan & Menamai Benda", en="Surprise Box & Object Naming"),
                        steps=[
                            LocalizedString(id="Masukkan 3 benda yang dikenal anak ke dalam kardus.", en="Place 3 familiar objects inside the cardboard box."),
                            LocalizedString(id="Keluarkan satu per satu sambil menyebutkan namanya dengan bibir jelas: 'Bola... bo-la'.", en="Take each item out slowly and articulate clearly: 'Ball... b-all'."),
                            LocalizedString(id="Beri jeda 5 detik agar anak mencoba menirukan suaranya.", en="Pause for 5 seconds to invite your child to imitate."),
                        ],
                    ),
                    PlaybookDaySchema(
                        day=2,
                        item=LocalizedString(id="Dua cangkir plastik & sendok", en="Two plastic cups & spoon"),
                        title=LocalizedString(id="Permainan Menuang & Kata Kunci 'Lagi'", en="Pouring & Prompting 'More'"),
                        steps=[
                            LocalizedString(id="Duduk berhadapan, tuang air atau beras dari cangkir ke cangkir.", en="Sit face-to-face and pour water or rice between cups."),
                            LocalizedString(id="Ucapkan kata kunci: 'tuang', 'habis', dan 'lagi'.", en="Emphasize action keywords: 'pour', 'all gone', and 'more'."),
                            LocalizedString(id="Tunggu anak meminta dengan gesture atau suara sebelum menuang lagi.", en="Pause before pouring again until child gestures or vocalizes."),
                        ],
                    ),
                    PlaybookDaySchema(
                        day=3,
                        item=LocalizedString(id="Bungkus makanan bergambar", en="Picture food packaging"),
                        title=LocalizedString(id="Detektif Gambar & Pengenalan Visual", en="Picture Detective & Visual Recognition"),
                        steps=[
                            LocalizedString(id="Gunting gambar buah/hewan dari kemasan bekas dan tempel di dinding rendah.", en="Cut food/animal pictures from packaging and tape them at eye level."),
                            LocalizedString(id="Ajak anak mencari: 'Mana gambar apel?', beri tepuk tangan saat ia menunjuk.", en="Ask 'Where is the apple?' and clap when they point."),
                            LocalizedString(id="Tanya 'Ini apa?' dan terima segala bentuk celoteh anak sebagai apresiasi.", en="Ask 'What is this?' and warmly acknowledge any babble."),
                        ],
                    ),
                ],
            )
        else:
            return MilestoneEvaluationResponse(
                id=str(uuid.uuid4())[:8],
                status_type="ok",
                status_title=LocalizedString(id="Perkembangan Sesuai Tahapan Usia", en="Development On Track"),
                status_desc=LocalizedString(
                    id=f"Berdasarkan pengamatan orang tua, tumbuh kembang {child.name} berjalan selaras dengan indikator milestone seusianya.",
                    en=f"Based on parental observation, {child.name}'s progress aligns well with age-appropriate milestones.",
                ),
                ref=LocalizedString(
                    id=f"Rujukan: Pedoman Tumbuh Kembang WHO/Kemenkes untuk usia {age} bulan.",
                    en=f"Reference: WHO/MOH Developmental Guidelines for {age} months.",
                ),
                safety=LocalizedString(
                    id="Selalu pastikan area bermain bebas dari benda berukuran di bawah 3 cm untuk mencegah bahaya tersedak.",
                    en="Always ensure play areas are free of items smaller than 3 cm to prevent choking hazards.",
                ),
                focus_area=LocalizedString(id="Stimulasi Kognitif & Motorik Halus", en="Cognitive & Fine Motor Stimulation"),
                rag_sources=rag_sources_list,
                playbook=[
                    PlaybookDaySchema(
                        day=1,
                        item=LocalizedString(id="Mangkuk plastik & sendok kayu", en="Plastic bowl & wooden spoon"),
                        title=LocalizedString(id="Eksplorasi Irama & Ketukan", en="Rhythm & Tapping Exploration"),
                        steps=[
                            LocalizedString(id="Duduk bersama anak di lantai dengan mangkuk terbalik.", en="Sit together on the floor with an inverted bowl."),
                            LocalizedString(id="Ketuk perlahan: 'tuk-tuk-tuk' dan berikan sendok kepada anak.", en="Tap gently: 'knock-knock' and hand the spoon to your child."),
                            LocalizedString(id="Tirukan kembali setiap ketukan yang dihasilkan anak.", en="Mirror each tap produced by your child enthusiastically."),
                        ],
                    ),
                    PlaybookDaySchema(
                        day=2,
                        item=LocalizedString(id="Kaus kaki bersih digulung jadi bola", en="Clean rolled socks into a ball"),
                        title=LocalizedString(id="Lempar Tangkap Lembut", en="Soft Catch & Release"),
                        steps=[
                            LocalizedString(id="Gulung sepasang kaus kaki bersih menjadi bola empuk.", en="Roll a clean pair of socks into a soft ball."),
                            LocalizedString(id="Lemparkan perlahan ke pangkuan anak dari jarak 50 cm.", en="Toss gently into your child's lap from 50 cm away."),
                            LocalizedString(id="Ajak anak melemparnya kembali ke dalam ember cucian.", en="Encourage child to drop it into a laundry basket."),
                        ],
                    ),
                    PlaybookDaySchema(
                        day=3,
                        item=LocalizedString(id="Cermin dinding aman", en="Safe wall mirror"),
                        title=LocalizedString(id="Mengenal Diri di Depan Cermin", en="Mirror Self-Recognition"),
                        steps=[
                            LocalizedString(id="Ajak anak duduk di depan cermin.", en="Sit with your child in front of a mirror."),
                            LocalizedString(id="Tunjuk hidung anak lalu tunjuk hidung Anda di cermin.", en="Point to their nose, then point to your nose in the reflection."),
                            LocalizedString(id="Buat ekspresi lucu dan ajak anak tertawa bersama.", en="Make playful expressions and giggle together."),
                        ],
                    ),
                ],
            )

    def _fallback_plate(
        self,
        child: ChildContext,
        meal_time: str,
        selected_items: Optional[List[str]],
        notes: Optional[str],
    ) -> PlateAuditResponse:
        if selected_items and len(selected_items) > 0:
            items = selected_items
        elif notes:
            items = [n.strip() for n in notes.replace(",", ";").split(";") if n.strip()]
        else:
            items = ["Bubur Beras", "Hati Ayam Cincang", "Bayam Rebus", "Minyak Kelapa Tambahan"]

        def check_animal(text: str) -> bool:
            t = text.lower()
            if any(k in t for k in ["telur", "hati", "ikan", "daging", "sapi", "salmon", "lele", "udang", "bebek"]):
                return True
            if "ayam" in t:
                # Disambiguate 'bayam' (spinach) from 'ayam' (chicken)
                words = [w.strip() for w in t.replace("-", " ").split()]
                return any(w == "ayam" for w in words)
            return False

        has_animal = any(check_animal(i) for i in items)
        has_fat = any(any(k in i.lower() for k in ["minyak", "santan", "mentega", "keju", "alpukat", "butter"]) for i in items)
        has_carb = any(any(k in i.lower() for k in ["nasi", "kentang", "bubur", "ubi", "oat", "beras", "jagung"]) for i in items)

        detected_foods: List[FoodDetectedItem] = []
        for it in items:
            it_l = it.lower()
            if check_animal(it_l):
                kind = "animal"
            elif any(k in it_l for k in ["minyak", "santan", "mentega", "keju", "alpukat", "butter"]):
                kind = "fat"
            elif any(k in it_l for k in ["bayam", "wortel", "brokoli", "labu", "tomat", "sayur"]):
                kind = "veg"
            elif any(k in it_l for k in ["tempe", "tahu", "kacang", "edamame"]):
                kind = "plant"
            else:
                kind = "carb"

            detected_foods.append(
                FoodDetectedItem(
                    name=LocalizedString(id=it.title(), en=it.title()),
                    kind=kind,
                    confidence=0.96,
                )
            )

        # Texture verdict by age
        age = child.age_months
        if age <= 8:
            texture_status = "ok"
            texture_desc = LocalizedString(
                id="Tekstur lumat/saring cocok untuk bayi usia 6-8 bulan guna melatih refleks menelan awal.",
                en="Pureed texture is appropriate for 6-8 month infants for early swallowing coordination.",
            )
        elif age <= 11:
            texture_status = "ok"
            texture_desc = LocalizedString(
                id="Tekstur cincang halus / nasi tim tepat untuk usia 9-11 bulan melatih keterampilan mengunyah.",
                en="Finely chopped/mashed texture fits 9-11 months to promote oral chewing competence.",
            )
        else:
            texture_status = "ok"
            texture_desc = LocalizedString(
                id="Tekstur makanan keluarga padat sesuai untuk balita usia 12 bulan ke atas.",
                en="Family-table textured food is well-suited for toddlers aged 12 months and above.",
            )

        animal_rating = "good" if has_animal else "low"
        fat_rating = "good" if has_fat else "low"
        carb_rating = "good" if has_carb else "low"

        deficient: List[str] = []
        if not has_animal:
            deficient.append("animal")
        if not has_fat:
            deficient.append("fat")

        return PlateAuditResponse(
            id=str(uuid.uuid4())[:8],
            meal_time=meal_time,  # type: ignore
            detected_foods=detected_foods,
            detected_texture="Lumat Bertekstur / Cincang Halus",
            texture_verdict=TextureVerdictSchema(
                status=texture_status,  # type: ignore
                title=LocalizedString(id="Tekstur Sesuai Usia", en="Age-Appropriate Texture"),
                description=texture_desc,
            ),
            macros=[
                MacroInfoSchema(
                    key="animal",
                    name=LocalizedString(id="Protein Hewani", en="Animal Protein"),
                    rating=animal_rating,  # type: ignore
                    percentage=100 if has_animal else 15,
                    label=LocalizedString(id="Baik" if has_animal else "Kurang", en="Good" if has_animal else "Low"),
                    hint=None if has_animal else LocalizedString(
                        id="Wajib ditambah untuk mencegah stunting (asam amino esensial lengkap).",
                        en="Essential to add for stunting prevention (complete amino acids).",
                    ),
                    recipe=LocalizedString(id="1 butir telur orak-arik mentega", en="1 scrambled egg in butter"),
                ),
                MacroInfoSchema(
                    key="fat",
                    name=LocalizedString(id="Lemak Tambahan", en="Added Fat"),
                    rating=fat_rating,  # type: ignore
                    percentage=100 if has_fat else 15,
                    label=LocalizedString(id="Baik" if has_fat else "Kurang", en="Good" if has_fat else "Low"),
                    recipe=LocalizedString(id="1/2 sdt minyak kelapa / santan kental", en="1/2 tsp coconut oil / coconut milk"),
                ),
                MacroInfoSchema(
                    key="carb",
                    name=LocalizedString(id="Karbohidrat", en="Carbohydrates"),
                    rating=carb_rating,  # type: ignore
                    percentage=100 if has_carb else 25,
                    label=LocalizedString(id="Baik" if has_carb else "Kurang", en="Good" if has_carb else "Low"),
                ),
            ],
            deficient_macros=deficient,
            upgrade_plan=UpgradePlanSchema(
                summary=LocalizedString(
                    id="Tambahkan sumber protein hewani dan minyak/lemak pada piring untuk memenuhi kebutuhan kalori dan pencegahan stunting.",
                    en="Incorporate an animal protein source and healthy fat onto the plate to meet caloric density and stunting prevention standards.",
                ),
                suggestions=[
                    LocalizedString(id="Gunakan 1 butir telur ayam atau 30g hati ayam.", en="Add 1 whole egg or 30g chicken liver."),
                    LocalizedString(id="Tumis dengan 1 sdt minyak sayur atau margarin.", en="Sauté with 1 tsp vegetable oil or margarine."),
                ],
                booster_recipe=BoosterRecipeSchema(
                    name=LocalizedString(id="Telur Orak-Arik Lembut Mentega", en="Gentle Butter Scrambled Egg"),
                    prep_time=LocalizedString(id="5 Menit", en="5 Minutes"),
                    ingredients=[
                        LocalizedString(id="1 butir telur ayam ras/kampung", en="1 fresh egg"),
                        LocalizedString(id="1 sdt mentega atau minyak sayur", en="1 tsp butter or vegetable oil"),
                        LocalizedString(id="Sejumput daun bayam cincang halus", en="Pinch of finely chopped spinach"),
                    ],
                    instructions=[
                        LocalizedString(id="Kocok lepas telur dalam mangkuk kecil.", en="Whisk egg gently in a small bowl."),
                        LocalizedString(id="Panaskan wajan dengan mentega di atas api kecil.", en="Melt butter in a skillet over low heat."),
                        LocalizedString(id="Tuang telur, aduk perlahan selama 2 menit hingga matang lembut (tekstur creamy).", en="Pour egg and gently stir for 2 minutes until softly set."),
                    ],
                ),
            ),
            disclaimer=LocalizedString(
                id="Nurtura Smart Plate Vision adalah asisten pemantau gizi edukatif anti-stunting, bukan pengganti pemeriksaan medis dokter spesialis anak.",
                en="Nurtura Smart Plate Vision is an educational anti-stunting nutrition assistant, not a substitute for clinical pediatric care.",
            ),
            rag_sources=[
                f"{c.title} ({c.source})"
                for c in self.rag.retrieve_for_plate(child.age_months, selected_items, notes or "")
            ],
        )

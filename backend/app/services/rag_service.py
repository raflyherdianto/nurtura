import logging
import re
from pathlib import Path
from typing import Dict, List, Optional
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class KnowledgeChunk(BaseModel):
    id: str
    category: str  # "milestone" | "nutrition" | "general"
    title: str
    min_age_months: int = 0
    max_age_months: int = 60
    keywords: List[str] = []
    content: str
    source: str = "WHO / CDC / UNICEF / IDAI"


class PediatricRAGService:
    """
    Retrieval-Augmented Generation (RAG) Service for Nurtura.
    Grounds Gemini AI and the local clinical engine in official WHO 2023,
    CDC, UNICEF CCD, and IDAI early childhood guidelines.
    """

    def __init__(self, kb_path: Optional[Path] = None):
        self.kb_path = kb_path or self._resolve_kb_path()
        self.chunks: List[KnowledgeChunk] = []
        self._load_and_index_kb()

    def _resolve_kb_path(self) -> Path:
        """Finds pediatric_rag_kb.md from possible deployment and test paths."""
        candidates = [
            Path.cwd() / "pediatric_rag_kb.md",
            Path.cwd().parent / "pediatric_rag_kb.md",
            Path(__file__).resolve().parents[3] / "pediatric_rag_kb.md",
            Path(__file__).resolve().parents[2] / "pediatric_rag_kb.md",
            Path(__file__).resolve().parent / "data" / "pediatric_rag_kb.md",
        ]
        for c in candidates:
            if c.exists() and c.is_file():
                return c
        # Default fallback to parent project root
        return Path.cwd().parent / "pediatric_rag_kb.md"

    def _load_and_index_kb(self) -> None:
        """Parses pediatric_rag_kb.md into structured semantic chunks."""
        if not self.kb_path.exists():
            logger.warning("RAG Knowledge Base file not found at %s. Initializing in-memory baseline.", self.kb_path)
            self._init_in_memory_baseline()
            return

        try:
            raw_text = self.kb_path.read_text(encoding="utf-8")
            self._parse_markdown(raw_text)
            logger.info("Successfully indexed %d clinical chunks from %s", len(self.chunks), self.kb_path)
        except Exception as e:
            logger.error("Failed to parse RAG KB: %s. Using in-memory fallback chunks.", e)
            self._init_in_memory_baseline()

    def _parse_markdown(self, raw_text: str) -> None:
        """Parses the Markdown document into specialized clinical chunks."""
        sections = raw_text.split("### ")
        self.chunks.clear()

        chunk_idx = 1
        for sec in sections[1:]:
            lines = sec.strip().split("\n")
            header = lines[0].strip()
            body = "\n".join(lines[1:]).strip()

            # Determine category & age range
            category = "milestone" if ("Months" in header or "Milestone" in header or "Sensorimotor" in header) else "nutrition"
            min_age, max_age = 0, 60

            # Age extraction
            if "0–6 Months" in header or "0-6 Months" in header:
                min_age, max_age = 0, 6
            elif "6–12 Months" in header or "6-12 Months" in header:
                min_age, max_age = 6, 12
            elif "12–24 Months" in header or "12-24 Months" in header:
                min_age, max_age = 12, 24
            elif "24–60 Months" in header or "24-60 Months" in header:
                min_age, max_age = 24, 60
            elif "6–8 Months" in header or "6-8 Months" in header:
                min_age, max_age = 6, 8
                category = "nutrition"
            elif "9–11 Months" in header or "9-11 Months" in header:
                min_age, max_age = 9, 11
                category = "nutrition"
            elif "12–23 Months" in header or "12-23 Months" in header:
                min_age, max_age = 12, 24
                category = "nutrition"
            elif "Core WHO 2023" in header:
                min_age, max_age = 6, 24
                category = "nutrition"

            # Extract keywords from title and content
            words = re.findall(r"\b[A-Za-z]{3,}\b", (header + " " + body).lower())
            freq: Dict[str, int] = {}
            for w in words:
                freq[w] = freq.get(w, 0) + 1
            top_keywords = sorted(freq.keys(), key=lambda k: freq[k], reverse=True)[:15]

            self.chunks.append(
                KnowledgeChunk(
                    id=f"rag-{category}-{chunk_idx}",
                    category=category,
                    title=header,
                    min_age_months=min_age,
                    max_age_months=max_age,
                    keywords=top_keywords,
                    content=body,
                    source="WHO 2023 / CDC / UNICEF CCD / IDAI",
                )
            )
            chunk_idx += 1

    def _init_in_memory_baseline(self) -> None:
        """In-memory baseline chunks if the physical file is not accessible."""
        self.chunks = [
            KnowledgeChunk(
                id="rag-milestone-0-6",
                category="milestone",
                title="0–6 Months: Early Sensorimotor & Attachment (CDC + WHO)",
                min_age_months=0,
                max_age_months=6,
                keywords=["tummy", "smiles", "head", "visual", "tracking", "cooing"],
                content="CDC Core: Smiles socially, holds head steady, tummy time push-up. Stimulation: Practice supervised tummy time with rolled towel, tracking colorful cloth.",
                source="CDC / WHO CCD",
            ),
            KnowledgeChunk(
                id="rag-milestone-6-12",
                category="milestone",
                title="6–12 Months: Object Permanence & Mobility (CDC + WHO)",
                min_age_months=6,
                max_age_months=12,
                keywords=["sit", "crawl", "babble", "stand", "peekaboo", "containers"],
                content="CDC Core: Sits independently, pulls to stand, cruising, object permanence. Stimulation: Hide objects under cloth, bang plastic containers with wooden spoons.",
                source="CDC / WHO CCD",
            ),
            KnowledgeChunk(
                id="rag-milestone-12-24",
                category="milestone",
                title="12–24 Months: Toddlers & First Words (CDC + WHO)",
                min_age_months=12,
                max_age_months=24,
                keywords=["words", "walk", "stack", "spoon", "claps", "pointing"],
                content="CDC Core: Walks independently, points for help, says 3+ words, stacks 2 blocks. Stimulation: Nested plastic cups, cardboard stacking, name body parts.",
                source="CDC / WHO CCD",
            ),
            KnowledgeChunk(
                id="rag-nutrition-core",
                category="nutrition",
                title="WHO 2023 Complementary Feeding & Anti-Stunting Guidelines",
                min_age_months=6,
                max_age_months=24,
                keywords=["stunting", "animal", "protein", "fat", "iron", "zinc", "texture"],
                content="Daily animal-source food (meat, poultry, fish, liver, eggs) is mandatory for linear growth. Add healthy fats (butter, coconut milk, oil) for brain myelination.",
                source="WHO 2023 / IDAI",
            ),
            KnowledgeChunk(
                id="rag-nutrition-texture-matrix",
                category="nutrition",
                title="WHO 2023 Texture & Oral-Motor Matrix",
                min_age_months=6,
                max_age_months=24,
                keywords=["puree", "minced", "family", "choking", "chewing", "tim"],
                content="6-8m: Smooth thick puree (bubur kental). 9-11m: Minced/mashed (cincang halus / nasi tim) to prevent speech delay. 12m+: Family foods, avoid choking hazards.",
                source="WHO 2023 / IDAI",
            ),
        ]

    def retrieve_for_milestone(
        self,
        age_months: int,
        query: str = "",
        top_k: int = 2,
    ) -> List[KnowledgeChunk]:
        """
        Retrieves the most clinically relevant milestone chunks by age and observation context.
        """
        candidates = [c for c in self.chunks if c.category == "milestone"]

        # Score candidates based on age proximity and keyword matches
        scored: List[tuple[float, KnowledgeChunk]] = []
        query_words = set(re.findall(r"\b[A-Za-z]{3,}\b", query.lower()))

        for chunk in candidates:
            score = 0.0
            # Age match is paramount
            if chunk.min_age_months <= age_months <= chunk.max_age_months:
                score += 10.0
            else:
                dist = min(abs(age_months - chunk.min_age_months), abs(age_months - chunk.max_age_months))
                score += max(0.0, 5.0 - dist * 0.5)

            # Keyword matches
            for kw in chunk.keywords:
                if kw in query_words:
                    score += 1.5

            scored.append((score, chunk))

        scored.sort(key=lambda x: x[0], reverse=True)
        return [item[1] for item in scored[:top_k]]

    def retrieve_for_plate(
        self,
        age_months: int,
        food_items: Optional[List[str]] = None,
        notes: str = "",
        top_k: int = 2,
    ) -> List[KnowledgeChunk]:
        """
        Retrieves the most clinically relevant nutrition & texture chunks based on child age and meal items.
        """
        candidates = [c for c in self.chunks if c.category == "nutrition"]

        query_text = (notes + " " + " ".join(food_items or [])).lower()
        query_words = set(re.findall(r"\b[A-Za-z]{3,}\b", query_text))

        scored: List[tuple[float, KnowledgeChunk]] = []
        for chunk in candidates:
            score = 0.0
            if chunk.min_age_months <= age_months <= chunk.max_age_months:
                score += 10.0
            else:
                score += 3.0

            # Match nutrition keywords (e.g. protein, texture, choking, fat)
            for kw in chunk.keywords:
                if kw in query_words:
                    score += 2.0

            scored.append((score, chunk))

        scored.sort(key=lambda x: x[0], reverse=True)
        return [item[1] for item in scored[:top_k]]

    def format_for_prompt(self, chunks: List[KnowledgeChunk]) -> str:
        """Formats retrieved chunks into a clean, grounding context block for Gemini prompts."""
        if not chunks:
            return ""

        formatted_blocks = []
        for idx, ch in enumerate(chunks, 1):
            formatted_blocks.append(
                f"[Clinical Guideline Ref #{idx} - {ch.title} ({ch.source})]:\n{ch.content}"
            )
        return "\n\n".join(formatted_blocks)


_rag_service_instance: Optional[PediatricRAGService] = None


def get_rag_service() -> PediatricRAGService:
    global _rag_service_instance
    if _rag_service_instance is None:
        _rag_service_instance = PediatricRAGService()
    return _rag_service_instance

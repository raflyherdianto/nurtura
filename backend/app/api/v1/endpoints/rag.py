from typing import List, Optional
from fastapi import APIRouter, Query
from pydantic import BaseModel, Field
from app.services.rag_service import get_rag_service, KnowledgeChunk

router = APIRouter()


class RAGQueryRequest(BaseModel):
    category: str = Field(default="all", description="milestone | nutrition | all")
    age_months: int = Field(default=12, ge=0, le=60, description="Child age in months")
    query: str = Field(default="", description="Search query or clinical notes")
    top_k: int = Field(default=3, ge=1, le=10, description="Max chunks to return")


class RAGQueryResponse(BaseModel):
    total_indexed: int
    retrieved_count: int
    chunks: List[KnowledgeChunk]


@router.get("/chunks", response_model=List[KnowledgeChunk], summary="List all indexed RAG knowledge chunks")
async def list_chunks():
    """
    Returns all clinical guidelines chunks indexed from pediatric_rag_kb.md
    (WHO 2023, CDC Milestones, UNICEF CCD, IDAI).
    """
    rag = get_rag_service()
    return rag.chunks


@router.post("/retrieve", response_model=RAGQueryResponse, summary="Perform clinical RAG retrieval")
async def retrieve_knowledge(payload: RAGQueryRequest):
    """
    Retrieves grounded clinical chunks by child age, category, and parental observation.
    """
    rag = get_rag_service()

    if payload.category == "milestone":
        results = rag.retrieve_for_milestone(
            age_months=payload.age_months,
            query=payload.query,
            top_k=payload.top_k,
        )
    elif payload.category == "nutrition":
        results = rag.retrieve_for_plate(
            age_months=payload.age_months,
            food_items=payload.query.split(),
            notes=payload.query,
            top_k=payload.top_k,
        )
    else:
        # Combined retrieval
        m_chunks = rag.retrieve_for_milestone(payload.age_months, payload.query, top_k=payload.top_k)
        n_chunks = rag.retrieve_for_plate(payload.age_months, notes=payload.query, top_k=payload.top_k)
        seen = set()
        results = []
        for c in m_chunks + n_chunks:
            if c.id not in seen:
                seen.add(c.id)
                results.append(c)

    return RAGQueryResponse(
        total_indexed=len(rag.chunks),
        retrieved_count=len(results),
        chunks=results,
    )

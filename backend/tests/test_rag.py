from fastapi.testclient import TestClient
from app.main import app
from app.services.rag_service import get_rag_service

client = TestClient(app)


def test_rag_indexing():
    rag = get_rag_service()
    assert len(rag.chunks) >= 5, "RAG Knowledge Base should have indexed at least 5 clinical chunks"
    
    categories = {c.category for c in rag.chunks}
    assert "milestone" in categories
    assert "nutrition" in categories


def test_milestone_retrieval_by_age():
    rag = get_rag_service()
    
    # 12-month child learning to stand and walk
    chunks = rag.retrieve_for_milestone(age_months=12, query="pull to stand cruising walking", top_k=2)
    assert len(chunks) == 2
    titles = " ".join([c.title for c in chunks])
    assert ("6–12" in titles or "6-12" in titles or "12–24" in titles or "12-24" in titles)


def test_nutrition_retrieval_by_age():
    rag = get_rag_service()
    
    # 9-month child MPASI chewing & texture check
    chunks = rag.retrieve_for_plate(age_months=9, food_items=["telur", "nasi tim"], notes="cincang halus", top_k=2)
    assert len(chunks) == 2
    content = " ".join([c.content for c in chunks])
    assert "animal" in content.lower() or "who" in content.lower() or "texture" in content.lower() or "pur" in content.lower()


def test_rag_endpoint_chunks():
    response = client.get("/api/v1/rag/chunks")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 5
    assert "title" in data[0]
    assert "content" in data[0]


def test_rag_endpoint_retrieve():
    payload = {
        "category": "milestone",
        "age_months": 12,
        "query": "belum bisa berdiri sendiri",
        "top_k": 2,
    }
    response = client.post("/api/v1/rag/retrieve", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["retrieved_count"] == 2
    assert len(data["chunks"]) == 2

def test_milestone_evaluation_success(client, sample_child):
    payload = {
        "child": sample_child,
        "observation_note": "Anak saya baru bisa bilang mama dan papa, belum mau tirukan kata lain.",
        "checked_milestones": ["Berjalan lancar", "Menunjuk benda yang diinginkan"],
    }
    response = client.post("/api/v1/milestone/evaluate", json=payload)
    if response.status_code == 503:
        assert response.json()["detail"] == "Live Gemini evaluation is unavailable. No sample result was generated."
        return
    assert response.status_code == 200
    data = response.json()

    assert "id" in data
    assert data["status_type"] in ["ok", "watch", "alert"]
    assert "status_title" in data
    assert "id" in data["status_title"]
    assert "en" in data["status_title"]
    assert "ref" in data
    assert "safety" in data
    assert "focus_area" in data

    # 3-Day playbook verification
    assert "playbook" in data
    assert len(data["playbook"]) == 3
    for i, day in enumerate(data["playbook"], start=1):
        assert day["day"] == i
        assert "item" in day
        assert "title" in day
        assert len(day["steps"]) >= 1


def test_milestone_validation_error(client):
    # Missing required child fields
    payload = {
        "child": {"name": "Test"},
        "observation_note": "Anak belum bicara.",
    }
    response = client.post("/api/v1/milestone/evaluate", json=payload)
    assert response.status_code == 422

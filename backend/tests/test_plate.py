import io
from PIL import Image


def test_plate_audit_json(client, sample_child):
    payload = {
        "child": sample_child,
        "meal_time": "siang",
        "selected_items": ["nasi", "bayam", "tempe"],
        "notes": "Hanya nasi dan bayam tanpa protein hewani",
    }
    response = client.post("/api/v1/plate/audit", json=payload)
    assert response.status_code == 200
    data = response.json()

    assert "id" in data
    assert data["meal_time"] == "siang"
    assert "detected_foods" in data
    assert "detected_texture" in data
    assert "texture_verdict" in data
    assert "macros" in data
    assert len(data["macros"]) == 3
    assert "deficient_macros" in data
    # Animal protein is missing, should be in deficient_macros
    assert "animal" in data["deficient_macros"]
    assert "upgrade_plan" in data
    assert "booster_recipe" in data["upgrade_plan"]
    assert "disclaimer" in data
    assert "rag_sources" in data
    assert len(data["rag_sources"]) > 0


def test_plate_audit_upload_multipart(client):
    # Create small dummy image in memory
    img_byte_arr = io.BytesIO()
    image = Image.new("RGB", (100, 100), color=(255, 200, 150))
    image.save(img_byte_arr, format="JPEG")
    img_byte_arr.seek(0)

    files = {
        "image": ("plate_sample.jpg", img_byte_arr, "image/jpeg"),
    }
    data = {
        "child_name": "Aira",
        "age_months": 10,
        "weight_kg": 8.9,
        "height_cm": 72.0,
        "meal_time": "siang",
        "notes": "Bubur tim wortel dan brokoli",
    }

    response = client.post("/api/v1/plate/audit-upload", files=files, data=data)
    assert response.status_code == 200
    res_data = response.json()

    assert "id" in res_data
    assert res_data["texture_verdict"]["status"] in ["fine", "ok", "coarse"]
    assert "upgrade_plan" in res_data

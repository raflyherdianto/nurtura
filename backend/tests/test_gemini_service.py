from app.services.gemini_service import GeminiService


def test_sanitize_payload_removes_markup_from_nested_gemini_output():
    payload = {
        "name": {"id": "<b>Telur</b>", "en": "Egg<br>booster"},
        "steps": ["<p>Masak</p> sampai matang", "&amp; sajikan"],
    }

    sanitized = GeminiService._sanitize_payload(payload)

    assert sanitized == {
        "name": {"id": "Telur", "en": "Egg\nbooster"},
        "steps": ["Masak sampai matang", "& sajikan"],
    }

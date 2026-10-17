# 🍼 Nurtura Backend API (FastAPI + Google Gemini 2.5)

Enterprise-grade REST API backend for Nurtura AI Co-Parenting & Early Childhood Development Platform.

## 🚀 Fitur Utama
1. **Modul 1: Milestone & Daily Playbook Agent** (`POST /api/v1/milestone/evaluate`)
   - Evaluasi observasi orang tua terhadap standar tumbuh kembang **WHO/CDC/IDAI**.
   - Perancangan otomatis kurikulum stimulasi rumah 3 hari menggunakan **benda sehari-hari tanpa biaya** (*zero-cost household objects*).
2. **Modul 2: Smart Plate Vision** (`POST /api/v1/plate/audit` & `POST /api/v1/plate/audit-upload`)
   - Analisis multimodal piring MPASI (foto atau komposisi bahan).
   - Validasi kesesuaian tekstur oromotor berdasarkan usia (bulan).
   - Meter makronutrisi anti-stunting (prioritas Protein Hewani & Lemak Tambahan).
   - Rekomendasi perbaikan gizi jam makan berikutnya + Resep Booster 5 Menit.
3. **Resilience & Zero-Crash Architecture**
   - Dilengkapi *Pediatric Deterministic Engine* otomatis saat kredensial belum diatur atau koneksi offline, sehingga aplikasi frontend selalu berjalan mulus.
   - Menggunakan Gemini melalui Vertex AI saat `USE_VERTEX_AI=True`.

## 📦 Setup & Menjalankan

### 1. Masuk ke folder backend & aktifkan venv
```powershell
cd D:\Projects\ai-builder-nurtura\backend
.\.venv\Scripts\Activate.ps1
```

### 2. Konfigurasi Environment (`.env`)
Konfigurasi default proyek menggunakan Vertex AI:
```env
USE_VERTEX_AI=True
GCP_PROJECT_ID=project-136bb5ce-7684-4481-82e
GCP_LOCATION=global
GEMINI_MODEL=gemini-3.8-flash
```

Pastikan **Vertex AI API** sudah aktif pada project tersebut. Untuk pengembangan lokal, autentikasi menggunakan Application Default Credentials:

```powershell
gcloud auth application-default login
gcloud config set project project-136bb5ce-7684-4481-82e
```

Service account juga dapat digunakan dengan mengatur `GOOGLE_APPLICATION_CREDENTIALS` ke path file JSON service account. Jangan commit file JSON atau nilai kredensial ke repository.

Jika ingin kembali menggunakan Google AI Studio, ubah `USE_VERTEX_AI=False` dan isi `GEMINI_API_KEY`.

### 3. Jalankan Server Development
```powershell
uvicorn app.main:app --reload --port 8000
```
- Swagger UI / OpenAPI Docs: [http://localhost:8000/docs](http://localhost:8000/docs)
- Health Check: [http://localhost:8000/api/v1/health](http://localhost:8000/api/v1/health)

### 4. Menjalankan Automated Tests
```powershell
pytest -v
```

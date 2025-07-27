# 📄 Round 1A: Understand Your Document – Outline Extractor

> ✨ Adobe India Hackathon 2025 – Challenge 1A  
> 🚀 Extracting structured outline (Title, H1, H2, H3) from multilingual PDFs  
> ✅ Dockerized, model-constrained, CPU-only, offline-compatible

---

## 📌 Problem Statement

You're given a PDF — your job is to extract a **structured outline** from it like a machine would. This includes:

- Title
- Headings: H1, H2, H3
- Page numbers
- Language detection (✅ Multilingual: English, French, Spanish, Russian, Telugu, Hindi)

---

## ✅ Solution Overview

This solution uses **semiotic heuristics** (not font-size based) to extract outline structure. It is built with:

- `PyMuPDF` for reading text blocks
- `langdetect + langcodes` for multilingual support
- `pytesseract` for OCR fallback (for scanned/image-based PDFs)
- `Docker` for portable execution
- Fully offline, ≤200MB dependencies, CPU-only, <10s per 50-page PDF

---

## 📂 Input & Output

### ✅ Input (via `/app/input`):

One or more PDFs (max 50 pages each)

### ✅ Output (via `/app/output`):

JSON file for each PDF like:

```json
{
  "title": "Understanding AI",
  "outline": [
    { "level": "H1", "text": "Introduction", "page": 1, "language": "English" },
    { "level": "H2", "text": "What is AI?", "page": 2, "language": "English" },
    { "level": "H3", "text": "History of AI", "page": 3, "language": "English" }
  ]
}

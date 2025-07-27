import os
import json
from pdf_outline_extractor import extract_outline_from_pdf

INPUT_DIR = "/app/input"
OUTPUT_DIR = "/app/output"

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for filename in os.listdir(INPUT_DIR):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(INPUT_DIR, filename)
            print(f"📄 Processing: {pdf_path}")

            try:
                result = extract_outline_from_pdf(pdf_path)
                output_filename = os.path.splitext(filename)[0] + ".json"
                output_path = os.path.join(OUTPUT_DIR, output_filename)

                with open(output_path, "w", encoding="utf-8") as f:
                    json.dump(result, f, indent=2, ensure_ascii=False)

                print(f"✅ Saved: {output_path}")
            except Exception as e:
                print(f"❌ Failed to process {filename}: {e}")

if __name__ == "__main__":
    main()

'''import os
import fitz  # PyMuPDF
from langdetect import detect
from langcodes import Language


def get_language_name(text):
    try:
        lang_code = detect(text)
        return Language.get(lang_code).language_name().capitalize()
    except:
        return "Unknown"


def detect_heading_level(y_pos, block_width, is_bold, text):
    """
    Semiotic-based heading detection.
    """
    if y_pos < 150 and len(text.split()) <= 10:
        return "H1"
    elif block_width < 400 and len(text.split()) <= 12:
        return "H2"
    elif is_bold or text.isupper():
        return "H3"
    return None


def extract_outline_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    outline = []
    title = None

    for page_num, page in enumerate(doc, start=1):
        blocks = page.get_text("dict")["blocks"]

        for block in blocks:
            if "lines" not in block:
                continue

            for line in block["lines"]:
                line_text = " ".join([span["text"] for span in line["spans"]]).strip()
                if not line_text or len(line_text) < 3:
                    continue

                y_pos = line["bbox"][1]
                block_width = block["bbox"][2] - block["bbox"][0]
                is_bold = any("Bold" in span["font"] for span in line["spans"])

                heading_level = detect_heading_level(y_pos, block_width, is_bold, line_text)

                if heading_level:
                    language = get_language_name(line_text)
                    outline.append({
                        "level": heading_level,
                        "text": line_text,
                        "page": page_num,
                        "language": language
                    })

                    if page_num == 1 and not title:
                        title = line_text

    return {
        "title": title if title else "Untitled Document",
        "outline": outline
    }
'''
'''
import os
import io
import fitz  # PyMuPDF
from langdetect import detect
from langcodes import Language
import pytesseract
from PIL import Image


def get_language_name(text):
    try:
        lang_code = detect(text)
        return Language.get(lang_code).language_name().capitalize()
    except:
        return "Unknown"


def detect_heading_level(y_pos, block_width, is_bold, text):
    # Semiotic heuristics for heading detection
    if y_pos < 150 and len(text.split()) <= 10:
        return "H1"
    elif block_width < 400 and len(text.split()) <= 12:
        return "H2"
    elif is_bold or text.isupper():
        return "H3"
    return None


def extract_text_from_page(page):
    # Try normal text extraction
    text = page.get_text("text").strip()
    if text and all(ord(char) < 128 for char in text):  # ASCII check
        return text

    print("🔍 OCR fallback triggered (image-based or garbled text)")

    # Fallback to OCR
    pix = page.get_pixmap(dpi=300)
    img_bytes = pix.tobytes("png")
    img = Image.open(io.BytesIO(img_bytes))
    return pytesseract.image_to_string(img)


def extract_outline_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    outline = []
    title = None

    for page_num, page in enumerate(doc, start=1):
        blocks = page.get_text("dict")["blocks"]

        for block in blocks:
            if "lines" not in block:
                continue

            for line in block["lines"]:
                line_text = " ".join([span["text"] for span in line["spans"]]).strip()

                # If garbled or short, fallback to OCR
                if not line_text or len(line_text.encode("utf-8", "ignore")) < 3:
                    line_text = extract_text_from_page(page)

                if not line_text.strip():
                    continue

                y_pos = line["bbox"][1]
                block_width = block["bbox"][2] - block["bbox"][0]
                is_bold = any("Bold" in span["font"] for span in line["spans"])

                heading_level = detect_heading_level(y_pos, block_width, is_bold, line_text)

                if heading_level:
                    language = get_language_name(line_text)
                    outline.append({
                        "level": heading_level,
                        "text": line_text,
                        "page": page_num,
                        "language": language
                    })

                    if page_num == 1 and not title:
                        title = line_text

    return {
        "title": title if title else "Untitled Document",
        "outline": outline
    }
'''
import os
import fitz  # PyMuPDF
from langdetect import detect
from langcodes import Language
from PIL import Image
import pytesseract
import io

def get_language_name(text):
    try:
        lang_code = detect(text)
        return Language.get(lang_code).language_name().capitalize()
    except:
        return "Unknown"

def detect_heading_level(y_pos, block_width, is_bold, text):
    """
    Semiotic-based heading detection (not font size-based).
    """
    if y_pos < 150 and len(text.split()) <= 10:
        return "H1"
    elif block_width < 400 and len(text.split()) <= 12:
        return "H2"
    elif is_bold or text.isupper():
        return "H3"
    return None

def extract_text_from_page(page):
    """ Try text extraction; fallback to OCR if garbled or empty """
    text = page.get_text()
    if text.strip() and not all(ord(c) > 1000 for c in text):  # crude garbled check
        return text

    print("🔍 OCR fallback triggered (image-based or garbled text)")
    pix = page.get_pixmap(dpi=300)
    img_bytes = pix.tobytes("png")
    img = Image.open(io.BytesIO(img_bytes))

    try:
        return pytesseract.image_to_string(img, timeout=5).strip()
    except RuntimeError:
        return ""

def extract_outline_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    outline = []
    title = None

    for page_num, page in enumerate(doc, start=1):
        blocks = page.get_text("dict")["blocks"]

        found_heading = False
        for block in blocks:
            if "lines" not in block:
                continue

            for line in block["lines"]:
                line_text = " ".join([span["text"] for span in line["spans"]]).strip()
                if not line_text or len(line_text) < 3:
                    continue

                y_pos = line["bbox"][1]
                block_width = block["bbox"][2] - block["bbox"][0]
                is_bold = any("Bold" in span["font"] for span in line["spans"])

                heading_level = detect_heading_level(y_pos, block_width, is_bold, line_text)
                if heading_level:
                    language = get_language_name(line_text)
                    outline.append({
                        "level": heading_level,
                        "text": line_text,
                        "page": page_num,
                        "language": language
                    })

                    if page_num == 1 and not title:
                        title = line_text
                    found_heading = True

        # If no headings found on this page → try OCR
        if not found_heading:
            ocr_text = extract_text_from_page(page)
            for line_text in ocr_text.split("\n"):
                line_text = line_text.strip()
                if not line_text or len(line_text) < 3:
                    continue

                heading_level = detect_heading_level(50, 200, False, line_text)
                if heading_level:
                    language = get_language_name(line_text)
                    outline.append({
                        "level": heading_level,
                        "text": line_text,
                        "page": page_num,
                        "language": language
                    })

                    if page_num == 1 and not title:
                        title = line_text

    return {
        "title": title if title else "Untitled Document",
        "outline": outline
    }

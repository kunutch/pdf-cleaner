#!/usr/bin/env python3
"""
PDF Cleaner - Remove annotations, comments, and images from PDF files.
"""

import argparse
import sys
from pathlib import Path

try:
    import fitz  # PyMuPDF
except ImportError:
    print("Error: PyMuPDF is required. Install it with: pip install pymupdf")
    sys.exit(1)


def clean_pdf(input_path: str, output_path: str | None = None) -> str:
    """
    Remove all annotations, comments, and images from a PDF file.

    Args:
        input_path: Path to the input PDF file
        output_path: Path for the cleaned PDF (default: input_cleaned.pdf)

    Returns:
        Path to the cleaned PDF file
    """
    input_file = Path(input_path)

    if not input_file.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    if output_path is None:
        output_path = str(input_file.with_stem(f"{input_file.stem}_cleaned"))

    doc = fitz.open(input_path)
    annotations_removed = 0
    images_removed = 0

    for page_num in range(len(doc)):
        page = doc[page_num]
        annots = list(page.annots()) if page.annots() else []

        for annot in annots:
            annotations_removed += 1
            page.delete_annot(annot)

        images = page.get_images(full=True)
        for img in images:
            xref = img[0]
            doc.xref_set_key(xref, "Length", "0")
            doc.xref_set_key(xref, "Filter", "null")
            doc.update_stream(xref, b"")
            images_removed += 1

    page_count = len(doc)
    doc.save(output_path, garbage=4, deflate=True)
    doc.close()

    print(f"Removed {annotations_removed} annotation(s) from {page_count} page(s)")
    print(f"Removed {images_removed} image(s)")
    print(f"Cleaned PDF saved to: {output_path}")

    return output_path


def main():
    parser = argparse.ArgumentParser(
        description="Remove annotations, comments, and images from PDF files"
    )
    parser.add_argument("input", help="Input PDF file path")
    parser.add_argument(
        "-o", "--output",
        help="Output PDF file path (default: input_cleaned.pdf)"
    )

    args = parser.parse_args()

    try:
        clean_pdf(args.input, args.output)
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error processing PDF: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

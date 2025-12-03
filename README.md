# PDF Cleaner

A command-line tool to remove all annotations and comments from PDF files.

## Features

Removes all types of PDF annotations:
- Comments and sticky notes
- Highlights, underlines, strikethroughs
- Stamps and drawings
- File attachments
- Form field markups

## Requirements

- Python 3.8+
- macOS

## Installation

```bash
./setup.sh
```

Or manually:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

```bash
source venv/bin/activate

# Basic usage (creates input_cleaned.pdf)
python pdf_cleaner.py input.pdf

# Custom output filename
python pdf_cleaner.py input.pdf -o output.pdf
```

## License

MIT

# PDF to Excel

Reads the PDFs in the file and imports them into Excel

## Features
- Scans multiple PDFs in the folder
- A separate row is created in Excel for each PDF
- Each PDF is processed within a try/except block, so if a file is corrupted or unreadable, the program does not crash. It writes “Error: ...” in the Status column for that file and moves on to the next files.

## Technologies
- Python
- PyPDF2
- OpenPyXL

## Usage
```bash
pip install PyPDF2 openpyxl
python pdf_to_excel.py /path/to/pdf/folder
```
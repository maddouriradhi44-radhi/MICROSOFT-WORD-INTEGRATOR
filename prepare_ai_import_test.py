from pathlib import Path

from docx import Document


SOURCE = Path(
    "storage/exports/test_ai_section_16.docx"
)

OUTPUT = Path(
    "storage/exports/test_ai_section_16_modified.docx"
)


document = Document(SOURCE)

document.add_paragraph(
    "Modification de test pour validation IA."
)

document.add_paragraph(
    "Cette phrase a été ajoutée volontairement "
    "afin de tester la détection des changements."
)

document.save(OUTPUT)

print()
print("===== PREPARE AI IMPORT TEST =====")
print()
print(f"Source: {SOURCE}")
print(f"Output: {OUTPUT}")
print(f"Exists: {OUTPUT.exists()}")

if OUTPUT.exists():
    print(f"Size: {OUTPUT.stat().st_size}")
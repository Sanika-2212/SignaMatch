
import csv
from collections import Counter
from pathlib import Path

BASE = Path(__file__).resolve().parent
DATASET = BASE / "signature_dataset"
CSV_FILE = BASE / "labels.csv"

print("Checking signature dataset...")

if not DATASET.is_dir():
    raise FileNotFoundError(f"Dataset folder not found: {DATASET}")

if not CSV_FILE.is_file():
    raise FileNotFoundError(f"Labels file not found: {CSV_FILE}")

with open(CSV_FILE, "r", encoding="utf-8-sig", newline="") as f:
    reader = csv.DictReader(f)

    if not {"filename", "student_id"}.issubset(reader.fieldnames or []):
        raise ValueError("CSV headers must be filename,student_id")

    rows = list(reader)

counts = Counter()
missing = []
invalid = []

for row in rows:
    filename = row["filename"].strip()
    student = row["student_id"].strip()

    if not filename or not student or Path(filename).name != filename:
        invalid.append(filename)
        continue

    image_path = DATASET / filename

    if not image_path.is_file():
        missing.append(filename)
    elif image_path.suffix.lower() not in {".jpg", ".jpeg"}:
        invalid.append(filename)
    else:
        counts[student] += 1

print("\n--- DATASET VALIDATION RESULTS ---")
print("Rows in labels.csv:", len(rows))
print("Students found:", len(counts))
print("Matched images:", sum(counts.values()))

print("\nSignatures per student:")
for student, count in sorted(counts.items()):
    print(f"{student}: {count}")

if missing:
    print("\nMISSING IMAGES:")
    for filename in missing:
        print(filename)

if invalid:
    print("\nINVALID ROWS:")
    for filename in invalid:
        print(filename)

if not missing and not invalid:
    print("\nBasic dataset validation passed!")
else:
    print("\nPlease correct the issues listed above.")

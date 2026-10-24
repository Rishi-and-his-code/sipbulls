import json
import re
from collections import defaultdict
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data" / "cha_questions.json"


def norm(value):
    return re.sub(r"[^a-z0-9]+", " ", str(value or "").lower()).strip()


def signature(question):
    values = [question.get("stem", ""), *(question.get("options") or []), question.get("correctIndex")]
    return "|".join(norm(value) for value in values)


def fact_signature(question):
    stem = norm(question.get("stem", ""))
    explanation = norm(question.get("explanation", ""))
    options = sorted(norm(option) for option in question.get("options", []))
    # Catch recurring statutory facts despite harmless wording differences.
    section = re.search(r"\bsection\s*\d+[a-z]*\b", stem)
    if section:
        return f"section:{section.group(0)}|{question.get('subject')}|{norm(explanation)[:160]}"
    return f"{question.get('subject')}|{norm(explanation)[:180]}|{'|'.join(options)}"


bank = json.loads(DATA.read_text(encoding="utf-8"))
errors = []
ids = defaultdict(list)
stems = defaultdict(list)
signatures = defaultdict(list)
facts = defaultdict(list)
subjects = defaultdict(int)

for question in bank:
    qid = question.get("id")
    ids[qid].append(qid)
    stems[norm(question.get("stem"))].append(qid)
    signatures[signature(question)].append(qid)
    facts[fact_signature(question)].append(qid)
    subjects[question.get("subject", "unknown")] += 1

    options = question.get("options") or []
    options_hi = question.get("optionsHi") or []
    if not qid or not question.get("stem"):
        errors.append(f"Missing id or stem: {qid}")
    if len(options) < 2:
        errors.append(f"Too few English options: {qid}")
    if len(options) != len(options_hi):
        errors.append(f"Hindi option count mismatch: {qid}")
    if not 0 <= question.get("correctIndex", -1) < len(options):
        errors.append(f"Invalid correct index: {qid}")
    for field in ("stemHi", "explanationHi"):
        if not question.get(field):
            errors.append(f"Missing Hindi field {field}: {qid}")


def duplicate_groups(groups):
    return {key: value for key, value in groups.items() if len(value) > 1}

for label, groups in (("IDs", ids), ("normalized stems", stems), ("full signatures", signatures), ("fact signatures", facts)):
    duplicates = duplicate_groups(groups)
    if duplicates:
        errors.append(f"Duplicate {label}: {duplicates}")

if len(bank) < 150:
    errors.append(f"CHA bank has only {len(bank)} questions; mock test requires 150")

english_fallback = []
for question in bank:
    if question.get("stemHi") == question.get("stem") or question.get("explanationHi") == question.get("explanation"):
        english_fallback.append(question.get("id"))
    english_options = question.get("options") or []
    hindi_options = question.get("optionsHi") or []
    # Numeric/legal section choices are intentionally language-neutral. Flag
    # only an unchanged option list containing translatable English text.
    has_translatable_text = any(re.search(r"[A-Za-z]{3,}", str(option)) for option in english_options)
    if has_translatable_text and hindi_options == english_options:
        english_fallback.append(question.get("id"))
if english_fallback:
    errors.append(f"Hindi fields are English fallbacks for: {english_fallback}")

print(f"CHA questions: {len(bank)}")
print(f"Subjects: {dict(sorted(subjects.items()))}")
print(f"Duplicate fact groups: {len(duplicate_groups(facts))}")
print(f"Duplicate normalized stems: {len(duplicate_groups(stems))}")
print(f"Duplicate full signatures: {len(duplicate_groups(signatures))}")
print(f"English fallback Hindi records: {len(english_fallback)}")
if errors:
    print("AUDIT FAILED")
    for error in errors:
        print(error)
    raise SystemExit(1)
print("CHA bank audit passed")

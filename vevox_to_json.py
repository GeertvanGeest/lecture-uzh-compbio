#!/usr/bin/env python3
"""Convert vevox_questions.md into a Vevox poll import file (polls/polls.json).

Usage:
    python3 vevox_to_json.py [vevox_questions.md] [polls/polls.json]

Conventions read from the markdown:
- `### Qn — title` starts a question; under "### Spare questions", each
  `**bold line**` starts a question.
- The question text is the `**bold line**` if present, otherwise the title
  (with prefixes such as "Background:" removed).
- `- item` lines are choices; a trailing ✅ marks the correct answer.
- "(multiple choice)" allows selecting all choices; default is single choice.
- "Word cloud" / "(open text)" questions become open-text word clouds.
- `*Explanation: ...*` or `*Discussion: ...*` becomes the answer explanation.
The JSON layout follows a Vevox export
(see sib-swiss/reproducible-analysis-training/polls.json).
"""

import json
import re
import sys
import zipfile
from pathlib import Path

PREFIXES = ("Background:", "Pre-lecture knowledge:", "End-of-lecture check:", "Guess:")
_ids = iter(range(5_000_001, 9_999_999))


def next_id():
    return str(next(_ids))


def plain(text):
    """Strip markdown emphasis and code markers."""
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    text = re.sub(r"(?<!\w)\*(.+?)\*(?!\w)", r"\1", text)
    text = text.replace("`", "")
    return text.strip()


def clean_question(text):
    text = plain(text)
    text = re.sub(r"\s*\((single|multiple) choice[^)]*\)\s*$", "", text)
    text = re.sub(r"\s*\(press \"Send\" after each entry\)\s*$", "", text)
    for p in PREFIXES:
        if text.startswith(p):
            text = text[len(p):].strip()
            text = text[0].upper() + text[1:]
    return text


def parse(md):
    questions, q, in_spares = [], None, False
    for line in md.splitlines():
        s = line.strip()
        if s.startswith("### Spare questions"):
            in_spares = True
            continue
        m = re.match(r"^### Q\d+\s+—\s+(.*)$", s)
        if m or (in_spares and s.startswith("**") and s.endswith("**")):
            q = {"title": m.group(1) if m else s, "bold": None if m else s,
                 "choices": [], "multi": False, "open": False, "explanation": None}
            questions.append(q)
            q["open"] = bool(m and ("Word cloud" in s or "open text" in s))
            continue
        if q is None:
            continue
        if s.startswith("**") and q["bold"] is None:
            q["bold"] = s
            if "(press \"Send\"" in s:
                q["open"] = True
        if "(multiple choice)" in s:
            q["multi"] = True
        if s.startswith("- "):
            text = s[2:].strip()
            correct = text.endswith("✅")
            q["choices"].append({"text": plain(text.rstrip("✅ ").strip()), "correct": correct})
        m = re.match(r"^\*(Explanation|Discussion):\s*(.*)\*$", s)
        if m:
            q["explanation"] = plain(m.group(2))
    return questions


def to_vevox(q):
    text = clean_question(q["bold"] or q["title"])
    if q["open"]:
        return {
            "@type": "OpenTextQuestion", "wordCloudQuestion": True, "lowerCaseAlias": "",
            "id": next_id(), "alias": "", "text": text, "image": None, "imageAltText": "",
            "questionSettings": {}, "resultDisplayType": "default", "maxLength": 2000,
            "maxWords": 150, "resultFormat": "WORD_CLOUD", "maxWordCount": None,
            "maxWordLength": None, "correctAnswers": [], "correctAnswerExplanation": None,
        }
    n = len(q["choices"])
    return {
        "@type": "MultipleChoiceQuestion", "splitPercentageQuestion": False,
        "lowerCaseAlias": "", "id": next_id(), "alias": "", "text": text,
        "image": None, "imageAltText": "", "questionSettings": {},
        "resultDisplayType": "default",
        "choices": [{"id": next_id(), "alias": None, "text": c["text"],
                     "excludeFromResults": False, "image": None, "imageAltText": None,
                     "isCorrectAnswer": c["correct"]} for c in q["choices"]],
        "minNumberSelections": 1, "maxNumberSelections": n if q["multi"] else 1,
        "resultFormat": "%", "distributableWeight": None, "weightingSetting": None,
        "weightingFactor": None, "correctAnswerExplanation": q["explanation"],
        "resultSorting": None, "uiType": "default",
    }


def main():
    src = Path(sys.argv[1] if len(sys.argv) > 1 else "vevox_questions.md")
    out = Path(sys.argv[2] if len(sys.argv) > 2 else "polls/polls.json")
    questions = [to_vevox(q) for q in parse(src.read_text())]
    for q in questions:
        if q["@type"] == "MultipleChoiceQuestion" and len(q["choices"]) < 2:
            sys.exit(f"Question without choices: {q['text']}")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(questions, ensure_ascii=False, indent=2) + "\n")
    print(f"Wrote {len(questions)} questions to {out}")

    # Vevox imports a zip archive with polls.json at its root
    zip_path = out.with_suffix(".zip")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.write(out, arcname="polls.json")
    print(f"Wrote {zip_path} (upload this file to Vevox)")


if __name__ == "__main__":
    main()

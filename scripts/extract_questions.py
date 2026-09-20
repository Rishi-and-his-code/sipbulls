#!/usr/bin/env python3
"""Extract unique NISM V-D MCQs from HTML banks and PDFs into data/questions.json."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from bs4 import BeautifulSoup, NavigableString
import fitz

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"

HTML_SOURCES = [
    ("MF 1.html", "mutual_funds"),
    ("MF 2.html", "mutual_funds"),
    ("MF 3.html", "mutual_funds"),
    ("MF 4.html", "mutual_funds"),
    ("MF 5.html", "mutual_funds"),
    ("Equity Derivatives 1.html", "equity_derivatives"),
    ("Equity Derivatives 2.html", "equity_derivatives"),
    ("equity Derivatives 3.html", "equity_derivatives"),
    ("equity Derivatives 4.html", "equity_derivatives"),
    ("Mix questions of 150.html", None),
    ("Mix questions of 150_.html", None),
]

PDF_SOURCES = [
    "NISM V-D Exam Prep Booklet - Comprehensive Guide & MCQs.pdf",
    "NISM_VD_150_Mock_Exam1.pdf",
    "NISM_VD_150_Mock_Exam-v2_2.pdf",
    "NISM_VD_150_Mock_Exam_Set3.pdf",
]

WS_RE = re.compile(r"\s+")
PUNCT_RE = re.compile(r"[^\w\s]+", re.UNICODE)
LATEX_RE = re.compile(r"\$[^$]*\$")
ZW_RE = re.compile(r"[\u200b\u200c\u200d\ufeff\u00ad]")


def clean_text(value: str) -> str:
    if not value:
        return ""
    value = ZW_RE.sub("", value)
    value = value.replace("\xa0", " ").replace("\u2028", " ").replace("\u2029", " ")
    value = value.replace("\u2019", "'").replace("\u2018", "'")
    value = value.replace("\u201c", '"').replace("\u201d", '"')
    value = value.replace("\u2013", "-").replace("\u2014", "-")

    def _latex(match: re.Match) -> str:
        inner = match.group(0).strip("$")
        inner = re.sub(r"\\text\{([^}]*)\}", r"\1", inner)
        inner = inner.replace("\\beta", "beta").replace("\\sigma", "sigma")
        inner = inner.replace("\\times", "x").replace("\\%", "%")
        inner = re.sub(r"[{}\\]", "", inner)
        return inner.strip()

    value = LATEX_RE.sub(_latex, value)
    value = WS_RE.sub(" ", value).strip()
    value = re.sub(r"^(Explanation|CORRECT ANSWER|Correct Answer)\s*:\s*", "", value, flags=re.I)
    return value


def normalize_stem(stem: str) -> str:
    text = clean_text(stem).lower()
    text = PUNCT_RE.sub(" ", text)
    return WS_RE.sub(" ", text).strip()


IRD_STRONG = [
    "interest rate future",
    "interest rate futures",
    "interest rate derivative",
    "interest rate derivatives",
    "forward rate agreement",
    "forward rate agreements",
    "t-bill future",
    "t-bill futures",
    "treasury bill future",
    "treasury bill futures",
    "g-sec future",
    "g-sec futures",
    "government securities future",
    "government security future",
    "bond future",
    "bond futures",
    "inverted yield curve",
    "yield curve",
    "dirty price",
    "clean price",
    "cheapest to deliver",
    "conversion factor",
    "interest rate swap",
    "overnight indexed swap",
    "tri-party repo",
    "modified duration",
    "macaulay duration",
    "current yield",
    "yield to maturity",
    "goi bond",
    "government of india bond",
    "notional principal",
    "coupon-bearing",
    "coupon bearing",
    "benchmark interest rate",
    "interest rate option",
    "91-day",
    "91 day t-bill",
    "treasury bill",
    "t-bills",
    "t-bill",
    "commercial paper",
    "certificate of deposit",
    "repo rate",
    "reverse repo",
    "convexity",
    "dv01",
    "pvbp",
    "ytm",
]

ED_STRONG = [
    "call option",
    "put option",
    "option premium",
    "option greek",
    "option greeks",
    "nifty future",
    "nifty futures",
    "stock future",
    "stock futures",
    "index future",
    "index futures",
    "strike price",
    "open interest",
    "lot size",
    "covered call",
    "protective put",
    "straddle",
    "strangle",
    "implied volatility",
    "cost of carry",
    "contango",
    "backwardation",
    "option writer",
    "european option",
    "american option",
    "futures contract",
    "forward contract",
    "mark to market",
    "marked-to-market",
    "marked to market",
    "in-the-money",
    "out-of-the-money",
    "at-the-money",
    "otm call",
    "otm put",
    "itm call",
    "itm put",
    "naked call",
    "naked put",
    "option buyer",
    "option seller",
    "underlying asset",
    "expiry date",
    "expiration",
    "delta",
    "gamma",
    "theta",
    "vega",
    "rho",
    "payoff",
    "intrinsic value",
    "time value",
    "f&o",
    "derivatives exchange",
    "clearing corporation",
    "initial margin",
    "span margin",
    "exposure margin",
    "contract multiplier",
    "bid-ask spread",
    "bid ask spread",
]

MF_STRONG = [
    "mutual fund",
    "asset management company",
    "amc",
    "unitholder",
    "scheme information document",
    "statement of additional information",
    "key information memorandum",
    "systematic investment plan",
    "systematic withdrawal",
    "systematic transfer",
    "expense ratio",
    "total expense ratio",
    "exit load",
    "entry load",
    "new fund offer",
    "net asset value",
    " nav",
    "nav ",
    "amfi",
    "euin",
    "elss",
    "registrar and transfer",
    "cut-off",
    "cutoff",
    "folio",
    "sid ",
    " sai",
    " kim",
    "large cap",
    "mid cap",
    "small cap",
    "flexi-cap",
    "flexi cap",
    "liquid fund",
    "overnight fund",
    "index fund",
    "exchange traded fund",
    "gold etf",
    "sebi scores",
    "know your customer",
    "fatca",
    "specialized investment fund",
    "sif",
    "nfo",
    "redemption",
    "distributor",
    "trustee",
    "sponsor",
    "custodian",
    "factsheet",
    "scheme",
    "arbitrage fund",
    "credit risk fund",
    "corporate bond fund",
    "gilt fund",
    "duration fund",
    "money market fund",
    "multi cap",
    "value fund",
    "growth investing",
    "herd mentality",
    "recency bias",
    "rupee cost averaging",
    "sharpe ratio",
    "treynor ratio",
    "tracking error",
    "benchmark",
]


def word_hits(blob: str, terms: list[str]) -> int:
    score = 0
    for term in terms:
        if len(term) <= 4:
            if re.search(rf"\b{re.escape(term.strip())}\b", blob):
                score += 2
        elif term in blob:
            score += 2 if len(term) > 12 else 1
    return score


def classify_subject(stem: str, options: list[str], explanation: str, forced: str | None) -> str:
    if forced:
        return forced
    blob = " ".join([stem, " ".join(options), explanation]).lower()
    ird = word_hits(blob, IRD_STRONG)
    ed = word_hits(blob, ED_STRONG)
    mf = word_hits(blob, MF_STRONG)

    # Duration *funds* are MF; standalone duration math is IRD.
    if "duration fund" in blob or "ultra short duration" in blob or "low duration fund" in blob:
        mf += 4
    if re.search(r"\b(irf|fra|ird)\b", blob):
        ird += 4
    if "option" in blob and any(k in blob for k in ("call", "put", "premium", "strike", "greek")):
        ed += 3
    if "futures" in blob and any(k in blob for k in ("nifty", "stock", "index", "equity")):
        ed += 3
    if "futures" in blob and any(k in blob for k in ("bond", "t-bill", "g-sec", "interest rate", "treasury")):
        ird += 4

    scores = {
        "interest_rate_derivatives": ird,
        "equity_derivatives": ed,
        "mutual_funds": mf,
    }
    best = max(scores, key=scores.get)
    if scores[best] == 0:
        return "mutual_funds"
    # Prefer IRD on ties if any IRD signal exists, then ED, then MF.
    tied = [k for k, v in scores.items() if v == scores[best]]
    if len(tied) == 1:
        return best
    for preferred in ("interest_rate_derivatives", "equity_derivatives", "mutual_funds"):
        if preferred in tied:
            return preferred
    return best


def parse_html_file(path: Path, forced_subject: str | None) -> list[dict]:
    soup = BeautifulSoup(path.read_text(encoding="utf-8", errors="replace"), "html.parser")
    rows = soup.select("table table tr")
    questions = []
    for row in rows:
        tds = row.find_all("td", recursive=False)
        if len(tds) < 2:
            continue
        label = tds[0].get_text(" ", strip=True)
        if not re.match(r"Q\s*\d+", label):
            continue
        td = tds[1]
        strong = td.find("strong")
        if not strong:
            continue
        for br in strong.find_all("br"):
            br.replace_with("\n")
        stem = clean_text(strong.get_text("\n", strip=True))

        options = []
        for inp in td.find_all("input", {"type": "radio"}):
            parts = []
            for sib in inp.next_siblings:
                name = getattr(sib, "name", None)
                if name in ("input", "p", "div"):
                    break
                if name == "br":
                    break
                if isinstance(sib, NavigableString):
                    parts.append(str(sib))
                else:
                    parts.append(sib.get_text(" ", strip=True))
            text = clean_text("".join(parts))
            if text:
                options.append(text)

        ans_inp = td.find("input", attrs={"name": re.compile(r"^CorrectAns\d+$")})
        if not ans_inp or not ans_inp.get("value"):
            continue
        try:
            correct_index = int(ans_inp["value"]) - 1
        except ValueError:
            continue
        if correct_index < 0 or correct_index >= len(options):
            continue

        ae = td.find("div", id=re.compile(r"^divAE"))
        explanation = clean_text(ae.get_text(" ", strip=True) if ae else "")

        qid = None
        report = td.find("a", href=re.compile(r"qid="))
        if report and report.get("onclick"):
            m = re.search(r"qid=(\d+)", report["onclick"])
            if m:
                qid = m.group(1)
        if not qid:
            m = re.search(r"qid=(\d+)", str(td))
            qid = m.group(1) if m else None

        subject = classify_subject(stem, options, explanation, forced_subject)
        questions.append(
            {
                "id": f"html-{qid or path.stem}-{len(questions)+1}",
                "source": path.name,
                "subject": subject,
                "stem": stem,
                "options": options,
                "correctIndex": correct_index,
                "explanation": explanation,
            }
        )
    return questions


PDF_SKIP_LINE = re.compile(
    r"^(SIPBULLS\.COM|@Prowisefin|NISM Series V-D.*|Comprehensive 150-Question.*|"
    r"Page \d+ of \d+|\d+)$"
)


def extract_pdf_text(path: Path) -> str:
    doc = fitz.open(path)
    lines_out = []
    for page in doc:
        for raw in page.get_text().splitlines():
            line = ZW_RE.sub("", raw).strip()
            if not line:
                continue
            if PDF_SKIP_LINE.match(line):
                continue
            lines_out.append(line)
    return "\n".join(lines_out)


def parse_pdf_question(raw: str, source: str, idx: int) -> dict | None:
    raw = ZW_RE.sub("", raw).strip()
    m = re.match(r"Q(\d+)\.\s*(.*)$", raw, re.S)
    if not m:
        return None
    body = m.group(2).strip()
    ans_m = re.search(r"(?:Correct\s+)?Answer:\s*([A-Da-d])\b", body)
    if not ans_m:
        return None
    letter = ans_m.group(1).upper()
    before = body[: ans_m.start()].strip()
    after = body[ans_m.end() :].strip()
    exp_m = re.search(r"Explanation:\s*(.*)$", after, re.S)
    explanation = clean_text(exp_m.group(1) if exp_m else after)

    opt_iter = list(re.finditer(r"(?:^|\n)\s*([A-D])[\.\)]\s*", before))
    if len(opt_iter) < 2:
        return None
    stem = clean_text(before[: opt_iter[0].start()])
    options = []
    for i, match in enumerate(opt_iter):
        start = match.end()
        end = opt_iter[i + 1].start() if i + 1 < len(opt_iter) else len(before)
        options.append(clean_text(before[start:end]))
    options = [o for o in options if o]
    correct_index = ord(letter) - ord("A")
    if not stem or len(options) < 2 or correct_index >= len(options):
        return None
    subject = classify_subject(stem, options, explanation, None)
    return {
        "id": f"pdf-{Path(source).stem}-{m.group(1)}",
        "source": source,
        "subject": subject,
        "stem": stem,
        "options": options,
        "correctIndex": correct_index,
        "explanation": explanation,
    }


def parse_pdf_file(path: Path) -> list[dict]:
    text = extract_pdf_text(path)
    m = re.search(r"(?:^|\n)(Q1\.\s)", text)
    if not m:
        return []
    body = text[m.start(1) :]
    chunks = re.split(r"\n(?=Q\d+\.\s)", body)
    questions = []
    for chunk in chunks:
        parsed = parse_pdf_question(chunk, path.name, len(questions) + 1)
        if parsed:
            questions.append(parsed)
    return questions


def main() -> int:
    all_qs: list[dict] = []
    stats = {"html": 0, "pdf": 0, "dropped_dupes": 0, "dropped_invalid": 0}

    for name, subject in HTML_SOURCES:
        path = ROOT / name
        if not path.exists():
            print(f"missing {name}", file=sys.stderr)
            continue
        qs = parse_html_file(path, subject)
        print(f"HTML {name}: {len(qs)}")
        stats["html"] += len(qs)
        all_qs.extend(qs)

    for name in PDF_SOURCES:
        path = ROOT / name
        if not path.exists():
            print(f"missing {name}", file=sys.stderr)
            continue
        qs = parse_pdf_file(path)
        print(f"PDF  {name}: {len(qs)}")
        stats["pdf"] += len(qs)
        all_qs.extend(qs)

    seen = {}
    unique = []
    for q in all_qs:
        key = normalize_stem(q["stem"])
        if not key or len(q["options"]) < 2:
            stats["dropped_invalid"] += 1
            continue
        if key in seen:
            stats["dropped_dupes"] += 1
            continue
        seen[key] = True
        unique.append(q)

    # Re-id sequentially for a stable public id.
    for i, q in enumerate(unique, start=1):
        q["id"] = f"q-{i:04d}"

    by_subject = {}
    for q in unique:
        by_subject[q["subject"]] = by_subject.get(q["subject"], 0) + 1

    DATA_DIR.mkdir(exist_ok=True)
    out = DATA_DIR / "questions.json"
    out.write_text(json.dumps(unique, ensure_ascii=False, indent=2), encoding="utf-8")
    meta = {
        "total": len(unique),
        "bySubject": by_subject,
        "stats": stats,
    }
    (DATA_DIR / "meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print("----")
    print(json.dumps(meta, indent=2))
    print(f"wrote {out} ({out.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

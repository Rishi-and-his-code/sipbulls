export const SUBJECTS = {
  mutual_funds: {
    id: "mutual_funds",
    label: "Mutual Funds",
    short: "MF",
    weight: 0.45,
    count: 68,
  },
  equity_derivatives: {
    id: "equity_derivatives",
    label: "Equity Derivatives",
    short: "ED",
    weight: 0.35,
    count: 52,
  },
  interest_rate_derivatives: {
    id: "interest_rate_derivatives",
    label: "Interest Rate Derivatives",
    short: "IRD",
    weight: 0.2,
    count: 30,
  },
};

export const EXAM = {
  total: 150,
  durationSeconds: 180 * 60,
  passMarks: 90,
  negative: 0.1,
};

const LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";

export function optionLetter(index) {
  return LETTERS[index] || String(index + 1);
}

export function escapeHtml(value) {
  return String(value ?? "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

export function subjectLabel(id) {
  return SUBJECTS[id]?.label || id;
}

export async function loadJSON(path) {
  const res = await fetch(path);
  if (!res.ok) throw new Error(`Could not load ${path}`);
  return res.json();
}

export async function loadQuestions() {
  return loadJSON("data/questions.json");
}

export async function loadMeta() {
  return loadJSON("data/meta.json");
}

export function shuffle(list) {
  const arr = list.slice();
  for (let i = arr.length - 1; i > 0; i -= 1) {
    const j = Math.floor(Math.random() * (i + 1));
    [arr[i], arr[j]] = [arr[j], arr[i]];
  }
  return arr;
}

export function formatTime(totalSeconds) {
  const s = Math.max(0, Math.floor(totalSeconds));
  const h = Math.floor(s / 3600);
  const m = Math.floor((s % 3600) / 60);
  const sec = s % 60;
  return [h, m, sec].map((n) => String(n).padStart(2, "0")).join(":");
}

export function formatDuration(secondsUsed) {
  const s = Math.max(0, Math.floor(secondsUsed));
  const h = Math.floor(s / 3600);
  const m = Math.floor((s % 3600) / 60);
  const sec = s % 60;
  const parts = [];
  if (h) parts.push(`${h}h`);
  if (m || h) parts.push(`${m}m`);
  parts.push(`${sec}s`);
  return parts.join(" ");
}

export function scoreExam(questions, answers) {
  let correct = 0;
  let wrong = 0;
  let skipped = 0;
  let marks = 0;
  const bySubject = {};
  Object.keys(SUBJECTS).forEach((id) => {
    bySubject[id] = { total: 0, correct: 0, wrong: 0, skipped: 0 };
  });

  questions.forEach((q, i) => {
    const bucket = bySubject[q.subject] || (bySubject[q.subject] = {
      total: 0, correct: 0, wrong: 0, skipped: 0,
    });
    bucket.total += 1;
    const chosen = answers[i];
    if (chosen === null || chosen === undefined || chosen === "") {
      skipped += 1;
      bucket.skipped += 1;
      return;
    }
    if (Number(chosen) === Number(q.correctIndex)) {
      correct += 1;
      bucket.correct += 1;
      marks += 1;
    } else {
      wrong += 1;
      bucket.wrong += 1;
      marks -= EXAM.negative;
    }
  });

  marks = Math.round(marks * 10) / 10;
  const percent = Math.round((marks / EXAM.total) * 1000) / 10;
  return {
    correct,
    wrong,
    skipped,
    marks,
    percent,
    passed: marks >= EXAM.passMarks,
    bySubject,
  };
}

export function buildPaper(bank, asked = new Set()) {
  const used = new Set();
  const paper = [];
  const bySubject = { mutual_funds: [], equity_derivatives: [], interest_rate_derivatives: [] };
  bank.forEach((q) => {
    if (bySubject[q.subject]) bySubject[q.subject].push(q);
  });

  Object.values(SUBJECTS).forEach((sub) => {
    const pool = shuffle(bySubject[sub.id] || []);
    const unseen = pool.filter((q) => !asked.has(q.id));
    const seen = pool.filter((q) => asked.has(q.id));
    const picked = [...unseen, ...seen].slice(0, sub.count);
    picked.forEach((q) => used.add(q.id));
    paper.push(...picked);
  });

  if (paper.length < EXAM.total) {
    const leftover = shuffle(bank.filter((q) => !used.has(q.id)));
    paper.push(...leftover.slice(0, EXAM.total - paper.length));
  }

  return shuffle(paper).slice(0, EXAM.total);
}

export function renderHeader(active) {
  const header = document.querySelector(".site-header .nav");
  if (!header) return;
  header.querySelectorAll("a").forEach((a) => {
    if (a.dataset.page === active) a.classList.add("active");
  });
}

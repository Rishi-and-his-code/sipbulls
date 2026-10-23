import {
  EXAM,
  SUBJECTS,
  buildPaper,
  escapeHtml,
  formatDuration,
  formatTime,
  loadQuestions,
  optionLetter,
  scoreExam,
  subjectLabel,
} from "./common.js";
import { getCurrentUser, getAskedQuestions, saveUserTestResult } from "./user.js";
import { initAuthUI } from "./auth-ui.js";

const STORAGE_KEY = "nism-vd-exam-state";
const params = new URLSearchParams(location.search);
const forceNew = params.get("new") === "1";

const introEl = document.getElementById("intro");
const examEl = document.getElementById("exam");
const resultsEl = document.getElementById("results");

let bank = [];
let state = null;
let tick = null;
let dirtyLeave = false;

function save() {
  if (!state || state.phase === "intro") return;
  sessionStorage.setItem(STORAGE_KEY, JSON.stringify(state));
}

function loadSaved() {
  try {
    const raw = sessionStorage.getItem(STORAGE_KEY);
    return raw ? JSON.parse(raw) : null;
  } catch {
    return null;
  }
}

function clearSaved() {
  sessionStorage.removeItem(STORAGE_KEY);
}

function startNewPaper() {
  const user = getCurrentUser();
  const paper = buildPaper(bank, getAskedQuestions(user?.username, "nism-vd"));
  state = {
    phase: "exam",
    ids: paper.map((q) => q.id),
    questions: paper,
    answers: paper.map(() => null),
    marked: paper.map(() => false),
    index: 0,
    remaining: EXAM.durationSeconds,
    startedAt: Date.now(),
  };
  save();
  showExam();
}

function resumeOrIntro() {
  if (forceNew) {
    clearSaved();
    history.replaceState({}, "", "exam.html");
  }
  const saved = loadSaved();
  if (saved?.phase === "results" && saved.questions?.length) {
    state = saved;
    showResults();
    return;
  }
  if (saved?.phase === "exam" && saved.questions?.length) {
    state = saved;
    showExam();
    return;
  }
  showIntro();
}

function showIntro() {
  introEl.classList.remove("hidden");
  examEl.classList.add("hidden");
  resultsEl.classList.add("hidden");
}

function showExam() {
  introEl.classList.add("hidden");
  resultsEl.classList.add("hidden");
  examEl.classList.remove("hidden");
  dirtyLeave = true;
  renderPalette();
  renderQuestion();
  startTimer();
}

function answeredCount() {
  return state.answers.filter((a) => a !== null && a !== undefined).length;
}

function markedCount() {
  return state.marked.filter(Boolean).length;
}

function startTimer() {
  if (tick) clearInterval(tick);
  const timerEl = document.getElementById("timer");
  const paint = () => {
    timerEl.textContent = formatTime(state.remaining);
    timerEl.classList.toggle("warn", state.remaining <= 10 * 60);
    if (state.remaining <= 0) {
      submit(true);
    }
  };
  paint();
  tick = setInterval(() => {
    state.remaining -= 1;
    if (state.remaining % 5 === 0) save();
    paint();
  }, 1000);
}

function renderPalette() {
  const pal = document.getElementById("palette");
  pal.innerHTML = state.questions.map((_, i) => {
    const classes = ["pal"];
    if (i === state.index) classes.push("current");
    if (state.answers[i] !== null && state.answers[i] !== undefined) classes.push("answered");
    if (state.marked[i]) classes.push("marked");
    return `<button class="${classes.join(" ")}" data-i="${i}">${i + 1}</button>`;
  }).join("");
}

function renderQuestion() {
  const q = state.questions[state.index];
  document.getElementById("q-label").textContent = `Question ${state.index + 1} of ${state.questions.length}`;
  document.getElementById("progress-label").textContent =
    `Answered ${answeredCount()} · Marked ${markedCount()} · Unanswered ${state.questions.length - answeredCount()}`;
  const badge = document.getElementById("subject-badge");
  badge.className = `badge ${q.subject}`;
  badge.textContent = subjectLabel(q.subject);
  document.getElementById("mark-state").textContent = state.marked[state.index] ? "Marked for review" : "";
  document.getElementById("q-stem").textContent = q.stem;
  document.getElementById("q-options").innerHTML = q.options.map((opt, i) => {
    const chosen = state.answers[state.index];
    const selected = chosen !== null && chosen !== undefined && Number(chosen) === i;
    return `<button class="opt-btn${selected ? " selected" : ""}" data-opt="${i}">
      <span class="opt-key">${optionLetter(i)}</span>
      <span>${escapeHtml(opt)}</span>
    </button>`;
  }).join("");
  document.getElementById("prev-btn").disabled = state.index === 0;
  document.getElementById("next-btn").disabled = state.index === state.questions.length - 1;
  document.getElementById("mark-btn").textContent = state.marked[state.index]
    ? "Unmark review"
    : "Mark for review";
  renderPalette();
}

function selectOption(i) {
  state.answers[state.index] = i;
  save();
  renderQuestion();
}

function submit(auto = false) {
  if (!auto) {
    const open = state.questions.length - answeredCount();
    const msg = open
      ? `You have ${open} unanswered question(s). Submit the test anyway?`
      : "Submit the test and view your result?";
    if (!confirm(msg)) return;
  }
  if (tick) clearInterval(tick);
  dirtyLeave = false;
  state.phase = "results";
  state.finishedAt = Date.now();
  state.auto = auto;
  save();
  showResults();
}

function showResults() {
  if (tick) clearInterval(tick);
  introEl.classList.add("hidden");
  examEl.classList.add("hidden");
  resultsEl.classList.remove("hidden");
  dirtyLeave = false;

  const used = EXAM.durationSeconds - Math.max(0, state.remaining);
  const result = scoreExam(state.questions, state.answers);
  const scoreEl = document.getElementById("score-value");
  scoreEl.textContent = result.marks.toFixed(1);
  scoreEl.className = `result-score ${result.passed ? "pass" : "fail"}`;
  document.getElementById("score-sub").textContent =
    `out of ${EXAM.total} · ${result.percent}% · ${result.passed ? "Pass" : "Did not pass"}`;
  const pill = document.getElementById("pass-pill");
  pill.textContent = result.passed ? "PASSED" : "NOT PASSED";
  pill.className = `pill ${result.passed ? "pass" : "fail"}`;
  document.getElementById("stat-correct").textContent = result.correct;
  document.getElementById("stat-wrong").textContent = result.wrong;
  document.getElementById("stat-skip").textContent = result.skipped;
  document.getElementById("stat-time").textContent = formatDuration(used);

  document.getElementById("subject-bars").innerHTML = Object.keys(SUBJECTS).map((id) => {
    const row = result.bySubject[id] || { total: 0, correct: 0 };
    const pct = row.total ? Math.round((row.correct / row.total) * 100) : 0;
    return `<div>
      <div style="display:flex;justify-content:space-between;font-weight:650;margin-bottom:6px">
        <span>${escapeHtml(subjectLabel(id))}</span>
        <span class="muted">${row.correct}/${row.total} · ${pct}%</span>
      </div>
      <div class="sub-bar-track"><span style="width:${pct}%"></span></div>
    </div>`;
  }).join("");

  const user = getCurrentUser();
  if (user && !state.savedToHistory) {
    saveUserTestResult(user.username, {
      score: result.marks,
      maxMarks: EXAM.total,
      correct: result.correct,
      wrong: result.wrong,
      skipped: result.skipped,
      percent: result.percent,
      passed: result.passed,
      questionIds: state.questions.map((q) => q.id),
    }, "nism-vd");
    state.savedToHistory = true;
    save();
  }

  window.__review = { result, filter: "all" };
  renderReview("all");
}

function reviewStatus(q, i) {
  const chosen = state.answers[i];
  if (chosen === null || chosen === undefined) return "skipped";
  return Number(chosen) === Number(q.correctIndex) ? "correct" : "wrong";
}

function renderReview(filter) {
  window.__review.filter = filter;
  document.querySelectorAll(".review-nav .chip").forEach((c) => {
    c.classList.toggle("active", c.dataset.review === filter);
  });
  const html = state.questions.map((q, i) => {
    const status = reviewStatus(q, i);
    if (filter !== "all" && status !== filter) return "";
    const chosen = state.answers[i];
    const options = q.options.map((opt, oi) => {
      const classes = ["option"];
      if (oi === q.correctIndex) classes.push("correct");
      if (chosen !== null && Number(chosen) === oi && oi !== q.correctIndex) classes.push("wrong");
      if (chosen !== null && Number(chosen) === oi) classes.push("chosen");
      return `<div class="${classes.join(" ")}"><strong>${optionLetter(oi)}.</strong> ${escapeHtml(opt)}</div>`;
    }).join("");
    const chosenLabel = chosen === null || chosen === undefined
      ? "Not answered"
      : `${optionLetter(chosen)}. ${q.options[chosen]}`;
    return `<article class="q-card">
      <div class="q-meta">
        <span class="badge ${q.subject}">${escapeHtml(subjectLabel(q.subject))}</span>
        <span class="muted">Q ${i + 1} · ${status === "correct" ? "Correct" : status === "wrong" ? "Incorrect" : "Unanswered"}</span>
      </div>
      <p class="q-stem">${escapeHtml(q.stem)}</p>
      <div class="options">${options}</div>
      <div class="answer-box">Your answer: ${escapeHtml(chosenLabel)}<br>Correct answer: ${optionLetter(q.correctIndex)}. ${escapeHtml(q.options[q.correctIndex] || "")}</div>
      <div class="explain-box"><strong>Explanation</strong><div>${escapeHtml(q.explanation)}</div></div>
    </article>`;
  }).join("");
  document.getElementById("review-list").innerHTML = html || `<p class="empty">No questions in this view.</p>`;
}

document.getElementById("begin-btn").addEventListener("click", startNewPaper);
document.getElementById("prev-btn").addEventListener("click", () => {
  if (state.index > 0) { state.index -= 1; save(); renderQuestion(); }
});
document.getElementById("next-btn").addEventListener("click", () => {
  if (state.index < state.questions.length - 1) { state.index += 1; save(); renderQuestion(); }
});
document.getElementById("clear-btn").addEventListener("click", () => {
  state.answers[state.index] = null;
  save();
  renderQuestion();
});
document.getElementById("mark-btn").addEventListener("click", () => {
  state.marked[state.index] = !state.marked[state.index];
  save();
  renderQuestion();
});
document.getElementById("submit-btn").addEventListener("click", () => submit(false));
document.getElementById("palette").addEventListener("click", (e) => {
  const btn = e.target.closest("[data-i]");
  if (!btn) return;
  state.index = Number(btn.dataset.i);
  save();
  renderQuestion();
});
document.getElementById("q-options").addEventListener("click", (e) => {
  const btn = e.target.closest("[data-opt]");
  if (!btn) return;
  selectOption(Number(btn.dataset.opt));
});
initAuthUI();

document.querySelector(".review-nav").addEventListener("click", (e) => {
  const btn = e.target.closest("[data-review]");
  if (!btn) return;
  renderReview(btn.dataset.review);
});

window.addEventListener("beforeunload", (e) => {
  if (!dirtyLeave) return;
  e.preventDefault();
  e.returnValue = "";
});

document.addEventListener("keydown", (e) => {
  if (!state || state.phase !== "exam" || examEl.classList.contains("hidden")) return;
  if (["INPUT", "TEXTAREA"].includes(e.target.tagName)) return;
  if (e.key >= "1" && e.key <= "4") {
    const i = Number(e.key) - 1;
    if (i < state.questions[state.index].options.length) selectOption(i);
  } else if (e.key === "n" || e.key === "N" || e.key === "ArrowRight") {
    document.getElementById("next-btn").click();
  } else if (e.key === "p" || e.key === "P" || e.key === "ArrowLeft") {
    document.getElementById("prev-btn").click();
  }
});

try {
  bank = await loadQuestions();
  resumeOrIntro();
} catch (err) {
  introEl.innerHTML = `<div class="panel"><h1>Could not load questions</h1><p>Serve this folder over HTTP, then try again.</p></div>`;
  console.error(err);
}
